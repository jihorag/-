import unittest
from build_rag_chunks import split_chunks, terms_of

MD = """# G01 경제학의 기초

### 1. 경제학의 정의

경제학은 희소한 자원의 배분을 다루는 학문이다.

#### 가. 미시경제학

개별 경제주체의 선택을 본다.

#### 나. 거시경제학

경제 전체의 총량을 본다.
"""


class SplitTest(unittest.TestCase):
    def test_소제목마다_청크가_하나씩(self):
        cs = split_chunks(MD)
        self.assertEqual(len(cs), 3)

    def test_제목_경로를_보존한다(self):
        cs = split_chunks(MD)
        self.assertEqual(cs[1]['path'], ['1. 경제학의 정의', '가. 미시경제학'])

    def test_본문이_들어간다(self):
        cs = split_chunks(MD)
        self.assertIn('개별 경제주체', cs[1]['text'])

    def test_너무_짧은_토막은_버린다(self):
        cs = split_chunks("### 빈 절\n\n### 다음\n\n내용이 충분히 긴 문단입니다. 검색에 쓸 만합니다.\n")
        self.assertEqual(len(cs), 1)


class TermsTest(unittest.TestCase):
    def test_어절과_2gram_을_함께_뽑는다(self):
        t = terms_of('한계대체율은 무차별곡선의 기울기다')
        self.assertIn('한계대체율은', t)
        self.assertIn('한계', t)

    def test_한_글자_어절은_버린다(self):
        self.assertNotIn('의', terms_of('의 것'))


if __name__ == '__main__':
    unittest.main()
