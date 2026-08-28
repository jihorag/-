import unittest

from track_core import (make_point_id, order_spans, chunk_lectures,
                        parse_points, check_track, diff_ids)


class TestPointId(unittest.TestCase):
    def test_zero_padded_and_stable(self):
        self.assertEqual(make_point_id('M01', 0, 1), 'M01-L00-p01')
        self.assertEqual(make_point_id('M01', 12, 7), 'M01-L12-p07')


class TestOrderSpans(unittest.TestCase):
    """강좌가 여럿이면 강좌별로 묶어 정렬한다.

    회계(재무 63강 + 원가 21강)·법규(도승하 36강 + 김희상 39강)는 둘 다 1강부터
    시작한다. 강번호로만 정렬하면 두 강좌가 지그재그로 섞이고, 트랙은 순서 자체가
    산출물이라 여기서 틀리면 전부 틀린다.
    """
    def test_groups_by_course_then_number(self):
        meta = {
            'a-1': {'no': 1, 'course': 'A'},
            'a-2': {'no': 2, 'course': 'A'},
            'b-1': {'no': 1, 'course': 'B'},
        }
        spans = [
            {'lecture_id': 'b-1', 'start': 10.0},
            {'lecture_id': 'a-2', 'start': 5.0},
            {'lecture_id': 'a-1', 'start': 30.0},
            {'lecture_id': 'a-1', 'start': 10.0},
        ]
        got = [(s['lecture_id'], s['start']) for s in order_spans(spans, meta)]
        self.assertEqual(got, [('a-1', 10.0), ('a-1', 30.0), ('a-2', 5.0), ('b-1', 10.0)])

    def test_unknown_lecture_goes_last_not_dropped(self):
        meta = {'a-1': {'no': 1, 'course': 'A'}}
        spans = [{'lecture_id': 'ghost', 'start': 0.0}, {'lecture_id': 'a-1', 'start': 0.0}]
        got = [s['lecture_id'] for s in order_spans(spans, meta)]
        self.assertEqual(got, ['a-1', 'ghost'])


class TestChunkLectures(unittest.TestCase):
    """긴 관은 잘라내지 않고 나눠 호출한다.

    generate_notes.py 는 MAX_TRANSCRIPT 를 넘으면 앞뒤만 남기고 가운데를 버린다.
    트랙에서 그러면 중간 논점이 통째로 사라지고, 그게 정확히 이 프로젝트가
    없애려는 손실이다.
    """
    def test_splits_without_dropping(self):
        blocks = [{'no': i, 'transcript': 'x' * 20000} for i in range(1, 6)]
        chunks = chunk_lectures(blocks, max_chars=45000)
        self.assertEqual(sum(len(c) for c in chunks), 5)
        self.assertTrue(all(c for c in chunks))

    def test_single_oversize_block_kept_whole(self):
        blocks = [{'no': 1, 'transcript': 'x' * 90000}]
        chunks = chunk_lectures(blocks, max_chars=45000)
        self.assertEqual(chunks, [blocks])


class TestParsePoints(unittest.TestCase):
    def test_strips_code_fence(self):
        raw = '```json\n[{"title":"t","gist":"g","body":"b"}]\n```'
        self.assertEqual(parse_points(raw)[0]['title'], 't')

    def test_object_wrapper_accepted(self):
        raw = '{"points": [{"title":"t","gist":"g","body":"b"}]}'
        self.assertEqual(len(parse_points(raw)), 1)

    def test_garbage_returns_empty(self):
        self.assertEqual(parse_points('설명입니다. JSON 아님'), [])


class TestCheckTrack(unittest.TestCase):
    def _track(self, **over):
        pt = {'seq': 1, 'id': 'M01-L00-p01', 'title': 't', 'gist': 'g', 'body': 'b',
              'viz': None, 'check': {'q': 'q', 'a': 'a'},
              'src': [{'lec': 2, 't': 100}]}
        pt.update(over.pop('point', {}))
        return {'unit_code': 'M01', 'phase': 'basic',
                'leaves': [{'leaf_id': 'L', 'title': 'T', 'points': [pt, dict(pt), dict(pt)]}],
                'orphans': []}

    def test_clean_track_has_no_issues(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        self.assertEqual(check_track(self._track(), align, {'supply-demand'}), [])

    def test_anchor_outside_span_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(point={'src': [{'lec': 2, 't': 9999}]}),
                             align, {'supply-demand'})
        self.assertTrue(any('앵커' in i for i in issues))

    def test_unknown_template_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(point={'viz': {'template': 'nope', 'params': {}}}),
                             align, {'supply-demand'})
        self.assertTrue(any('nope' in i for i in issues))

    def test_point_count_out_of_range_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        t = self._track()
        t['leaves'][0]['points'] = t['leaves'][0]['points'] * 41
        self.assertTrue(any('논점 수' in i for i in check_track(t, align, set())))

    def test_leaf_id_none_skips_anchor_check(self):
        """leaf_id가 None인 관은 앵커 검사를 건너뛰고 다른 문제는 보고하지 않는다."""
        t = self._track()
        t['leaves'][0]['leaf_id'] = None
        align = {}  # 아무 항목도 없음
        issues = check_track(t, align, {'supply-demand'})
        self.assertEqual(issues, [])  # 앵커 관련 문제 없음


class TestDiffIds(unittest.TestCase):
    def test_removed_ids_reported(self):
        """논점이 사라진 경우 removed에 그 id가 들어간다."""
        old = {
            'unit_code': 'M01',
            'leaves': [{'leaf_id': 'L', 'points': [
                {'id': 'M01-L00-p01'},
                {'id': 'M01-L00-p02'}
            ]}],
            'orphans': []
        }
        new = {
            'unit_code': 'M01',
            'leaves': [{'leaf_id': 'L', 'points': [
                {'id': 'M01-L00-p01'}
            ]}],
            'orphans': []
        }
        result = diff_ids(old, new)
        self.assertEqual(result['removed'], ['M01-L00-p02'])
        self.assertEqual(result['added'], [])

    def test_added_ids_reported(self):
        """논점이 새로 생긴 경우 added에 그 id가 들어간다."""
        old = {
            'unit_code': 'M01',
            'leaves': [{'leaf_id': 'L', 'points': [
                {'id': 'M01-L00-p01'}
            ]}],
            'orphans': []
        }
        new = {
            'unit_code': 'M01',
            'leaves': [{'leaf_id': 'L', 'points': [
                {'id': 'M01-L00-p01'},
                {'id': 'M01-L00-p02'}
            ]}],
            'orphans': []
        }
        result = diff_ids(old, new)
        self.assertEqual(result['removed'], [])
        self.assertEqual(result['added'], ['M01-L00-p02'])

    def test_old_track_none_treats_all_as_added(self):
        """old_track이 None이어도 터지지 않고 전부 added로 잡힌다. 반환값은 정렬된 리스트."""
        new = {
            'unit_code': 'M01',
            'leaves': [{'leaf_id': 'L', 'points': [
                {'id': 'M01-L00-p03'},
                {'id': 'M01-L00-p01'},
                {'id': 'M01-L00-p02'}
            ]}],
            'orphans': []
        }
        result = diff_ids(None, new)
        self.assertEqual(result['removed'], [])
        self.assertEqual(result['added'], ['M01-L00-p01', 'M01-L00-p02', 'M01-L00-p03'])


if __name__ == '__main__':
    unittest.main()
