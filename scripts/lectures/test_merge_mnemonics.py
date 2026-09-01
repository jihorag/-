import unittest
from merge_mnemonics import extract_mnemonics, already_has

MD = """### 제1관 취득원가

본문입니다.

#### 🧠 암기법

> 🔑 **취득원가 세 가지 — "매·전·기"**
> 매입원가 · 전환원가 · 기타 원가.
> 운반비는 매입원가에 붙는다.

### 제2관 매입할인

본문입니다.

#### 🧠 암기법

> 🔑 **할인은 빼는 것 — "깎으면 줄어든다"**
> 수익으로 잡지 않는다.
"""


class ExtractTest(unittest.TestCase):
    def test_관마다_따로_뽑는다(self):
        got = dict(extract_mnemonics(MD))
        self.assertEqual(set(got), {'제1관 취득원가', '제2관 매입할인'})

    def test_인용_기호를_떼고_두_줄까지(self):
        got = dict(extract_mnemonics(MD))
        tip = got['제1관 취득원가']
        self.assertNotIn('>', tip)
        self.assertEqual(len(tip.split('\n')), 2)
        self.assertIn('매·전·기', tip)

    def test_암기법이_없으면_빈_목록(self):
        self.assertEqual(extract_mnemonics('### 관\n\n본문\n'), [])

    def test_앞머리_이모지를_뗀다(self):
        got = dict(extract_mnemonics(MD))
        for tip in got.values():
            self.assertNotIn('🔑', tip)


class IdempotentTest(unittest.TestCase):
    def test_이미_있으면_다시_넣지_않는다(self):
        point = {'turns': [{'who': 'mate', 'text': '외우는 법 — 「매·전·기」'}]}
        self.assertTrue(already_has(point, '외우는 법 — 「매·전·기」'))
        self.assertFalse(already_has(point, '다른 말'))


if __name__ == '__main__':
    unittest.main()
