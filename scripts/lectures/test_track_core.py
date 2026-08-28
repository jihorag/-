import unittest

from track_core import (make_point_id, order_spans, chunk_lectures,
                        parse_points, check_track, diff_ids, LOW_SEVERITY_PREFIX)


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

    def test_recovers_unescaped_sum(self):
        """실패 사례 원문: 린달 조건 $\\sum MB = MC$ 가 백슬래시 하나로 들어와
        json.loads 가 'Invalid \\escape' 로 죽던 케이스."""
        raw = ('[{"title":"t","gist":"g",'
               '"body":"한계비용($MC$)과 같아야 한다는 린달 조건($\\sum MB = MC$)이다."}]')
        pts = parse_points(raw)
        self.assertEqual(len(pts), 1)
        self.assertIn('\\sum MB = MC', pts[0]['body'])

    def test_recovers_frac_without_formfeed_corruption(self):
        """가장 중요한 케이스: \\f 는 JSON에서 그 자체로는 유효한 이스케이프(폼피드)라
        \\frac 만 있으면 json.loads 가 예외 없이 성공해버리고 body 안에
        폼피드 문자 + 'rac{1}{1-c}' 로 조용히 깨진다. 1차 파싱이 성공해도 결과에
        제어문자 흔적이 있으면 재검사·재파싱해야 이 케이스를 잡는다 — \\sum 같은
        무효 이스케이프를 곁들이지 않은, \\frac 단독 입력이다."""
        raw = ('[{"title":"t","gist":"g",'
               '"body":"수렴 조건은 $\\frac{1}{1-c}$ 이다."}]')
        pts = parse_points(raw)
        self.assertEqual(len(pts), 1)
        body = pts[0]['body']
        self.assertIn('\\frac{1}{1-c}', body)
        self.assertNotIn('\f', body)

    def test_recovers_times(self):
        """\\times 단독 입력. \\t 는 JSON 유효 이스케이프(탭)라 1차 파싱이 성공해버린다."""
        raw = '[{"title":"t","gist":"g","body":"$A \\times B$ 로 계산한다."}]'
        pts = parse_points(raw)
        self.assertEqual(len(pts), 1)
        self.assertIn('\\times', pts[0]['body'])
        self.assertNotIn('\t', pts[0]['body'])

    def test_recovers_bar(self):
        """\\bar 단독 입력. \\b 는 JSON 유효 이스케이프(백스페이스)라 1차 파싱이 성공해버린다."""
        raw = '[{"title":"t","gist":"g","body":"$Y = f(L, \\bar{K})$ 로 쓴다."}]'
        pts = parse_points(raw)
        self.assertEqual(len(pts), 1)
        self.assertIn('\\bar{K}', pts[0]['body'])
        self.assertNotIn('\b', pts[0]['body'])

    def test_properly_escaped_input_untouched(self):
        """정상적으로 이스케이프된 응답은 첫 시도(json.loads)에서 바로 성공해야
        하고, 복구 경로를 타지 않아 줄바꿈·역슬래시 원래 의미가 유지된다."""
        raw = r'[{"title":"t","gist":"g","body":"첫 줄\n둘째 줄","note":"real backslash: \\"}]'
        pts = parse_points(raw)
        self.assertEqual(len(pts), 1)
        self.assertEqual(pts[0]['body'], '첫 줄\n둘째 줄')
        self.assertEqual(pts[0]['note'], 'real backslash: \\')

    def test_tab_not_followed_by_letter_preserved(self):
        """탭 뒤에 영문자가 아닌 문자(숫자·한글·공백)가 오면 정상적인 본문 탭으로
        보고 깨짐으로 오판하지 않는다."""
        raw = '[{"title":"t","gist":"g","body":"항목1\\t항목2 그리고 탭\\t123"}]'
        pts = parse_points(raw)
        self.assertEqual(len(pts), 1)
        self.assertIn('\t', pts[0]['body'])


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

    def test_anchor_within_tolerance_not_reported(self):
        """앵커가 [36강 6:06] 표기에서 읽힌 초라 구간 시작보다 살짝 이를 수 있다.
        허용치(5초) 안이면 거짓 경고를 내지 않는다."""
        align = {'L': [{'no': 2, 'start': 366.1, 'end': 500.0}]}
        issues = check_track(self._track(point={'src': [{'lec': 2, 't': 366}]}),
                             align, {'supply-demand'})
        self.assertEqual(issues, [])

    def test_anchor_beyond_tolerance_still_reported(self):
        align = {'L': [{'no': 2, 'start': 366.1, 'end': 500.0}]}
        issues = check_track(self._track(point={'src': [{'lec': 2, 't': 300}]}),
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

    def test_anchor_unknown_lecture_reported_as_high_severity(self):
        """앵커의 강 번호가 이 관의 spans 에 아예 없으면 진짜 신호 — 접두사 없이
        '이 관에 없는 강의' 성격이 드러나는 문구로 보고되고, 낮은 심각도 접두사는
        붙지 않는다."""
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(point={'src': [{'lec': 99, 't': 100}]}),
                             align, {'supply-demand'})
        self.assertTrue(any('이 관에 없는 강의' in i for i in issues))
        self.assertFalse(any(i.startswith(LOW_SEVERITY_PREFIX) for i in issues))

    def test_anchor_same_lecture_out_of_range_is_low_severity(self):
        """강 번호는 이 관의 spans 에 있지만 시각만 허용치 밖이면 시각 추정 오차로
        보고 낮은 심각도 접두사를 붙여 진짜 신호(다른 강의를 가리키는 앵커)와
        구분한다."""
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(point={'src': [{'lec': 2, 't': 9999}]}),
                             align, {'supply-demand'})
        self.assertTrue(any(i.startswith(LOW_SEVERITY_PREFIX) for i in issues))
        self.assertFalse(any('이 관에 없는 강의' in i for i in issues))

    def test_chunk_partial_failure_reported(self):
        """청크 일부가 실패한 채 저장된 관(chunks_ok < chunks_total)은 강의 일부
        유실 의심으로 보고된다."""
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        t = self._track()
        t['leaves'][0]['chunks_ok'] = 1
        t['leaves'][0]['chunks_total'] = 3
        issues = check_track(t, align, {'supply-demand'})
        self.assertTrue(any('청크' in i for i in issues))

    def test_chunk_fields_absent_not_reported(self):
        """chunks_ok/chunks_total 필드가 없는(이 검사 이전에 저장된) 관은
        청크 관련 문제를 보고하지 않는다."""
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(), align, {'supply-demand'})
        self.assertFalse(any('청크' in i for i in issues))

    def test_chunk_full_success_not_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        t = self._track()
        t['leaves'][0]['chunks_ok'] = 3
        t['leaves'][0]['chunks_total'] = 3
        issues = check_track(t, align, {'supply-demand'})
        self.assertFalse(any('청크' in i for i in issues))

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
