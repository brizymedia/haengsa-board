# -*- coding: utf-8 -*-
"""보상플랜 계산 모델 단위 테스트 24항목

  cd bosangplan && python tests.py

공시 수치는 서로 맞물려야 한다. 분포표 인원·금액 합계가 총계와 어긋나면
데이터를 잘못 옮긴 것이므로 여기서 걸린다.
"""
import unittest

import plan


class TestData(unittest.TestCase):
    """공시 데이터 검산 — 옮겨 적다 틀리면 여기서 잡힌다."""

    def test_01_distribution_headcount(self):
        total = sum(c for _l, _h, c, _a in plan.DISTRIBUTION)
        self.assertEqual(total, plan.FTC["등록_판매원수"])

    def test_02_distribution_amount(self):
        total = sum(a for _l, _h, _c, a in plan.DISTRIBUTION)
        self.assertEqual(total, plan.FTC["후원수당_총액"])

    def test_03_payout_ratio(self):
        got = plan.FTC["후원수당_총액"] / plan.FTC["총매출액_부가세포함"]
        self.assertAlmostEqual(got, plan.FTC["후원수당_지급률"], places=4)

    def test_04_ratio_under_legal_cap(self):
        self.assertLess(plan.FTC["후원수당_지급률"], plan.LEGAL_CAP)

    def test_05_earners_equal_nonzero_brackets(self):
        earners = sum(c for low, _h, c, _a in plan.DISTRIBUTION if low >= 1)
        self.assertEqual(earners, plan.FTC["수당_수령_판매원수"])

    def test_06_zero_bracket_is_majority(self):
        zero = [c for low, _h, c, _a in plan.DISTRIBUTION if low == 0][0]
        self.assertGreater(zero / plan.FTC["등록_판매원수"], 0.5)


class TestRanks(unittest.TestCase):
    def test_07_ten_ranks(self):
        self.assertEqual(len(plan.RANKS), 10)

    def test_08_unknown_rank_raises(self):
        with self.assertRaises(ValueError):
            plan.rank_by_name("플래티넘")

    def test_09_leg_cv_monotonic(self):
        legs = [r.leg_cv for r in plan.RANKS if r.leg_cv is not None]
        self.assertEqual(legs, sorted(legs))

    def test_10_dignity_monotonic(self):
        pay = [r.dignity for r in plan.RANKS if r.leg_cv is not None]
        self.assertEqual(pay, sorted(pay))

    def test_11_below_director_has_no_dignity(self):
        for name in ("회원", "멤버", "매니아"):
            self.assertEqual(plan.rank_by_name(name).dignity, 0)


class TestDignityRank(unittest.TestCase):
    """직급과 소실적 중 낮은 쪽이 품위유지 기준이 된다."""

    def test_12_high_rank_low_volume(self):
        # 블루다이아 직급인데 실적은 그린다이아 수준
        got = plan.dignity_rank(plan.rank_by_name("블루다이아몬드"), 19_000_000)
        self.assertEqual(got.name, "그린다이아몬드")

    def test_13_low_rank_high_volume(self):
        # 실적은 크라운급인데 직급이 디렉터면 디렉터 기준
        got = plan.dignity_rank(plan.rank_by_name("디렉터"), 200_000_000)
        self.assertEqual(got.name, "디렉터")

    def test_14_exact_threshold_counts(self):
        got = plan.dignity_rank(plan.rank_by_name("다이아몬드"), 10_000_000)
        self.assertEqual(got.name, "다이아몬드")

    def test_15_one_short_of_threshold(self):
        got = plan.dignity_rank(plan.rank_by_name("다이아몬드"), 9_999_999)
        self.assertEqual(got.name, "에메랄드")


class TestPayout(unittest.TestCase):
    def test_16_referral_matches_published_example(self):
        # 사업자 공개 예시: 110,000CV 의 12% = 13,200원
        p = plan.cycle_payout(rank_name="멤버", referral_cv=110_000)
        self.assertEqual(p["추천보너스"], 13_200)

    def test_17_referral_second_example(self):
        # 사업자 공개 예시: 70만CV 의 12% = 84,000원
        p = plan.cycle_payout(rank_name="멤버", referral_cv=700_000)
        self.assertEqual(p["추천보너스"], 84_000)

    def test_18_no_subscription_no_payout(self):
        p = plan.cycle_payout(rank_name="다이아몬드", weak_cv=10_000_000,
                              referral_cv=700_000, subscription_cv=0)
        self.assertFalse(p["구독_충족"])
        self.assertEqual(p["수당_합계_세전"], 0)

    def test_19_net_is_gross_less_tax_and_cost(self):
        p = plan.cycle_payout(rank_name="디렉터", weak_cv=2_100_000, referral_cv=440_000)
        self.assertEqual(p["기수_실수령"],
                         p["수당_합계_세전"] + p["원천징수_3.3%"] + p["구독_구매비용"])

    def test_20_annual_is_24_cycles(self):
        p = plan.cycle_payout(rank_name="디렉터", weak_cv=2_100_000)
        self.assertEqual(p["연환산_세전"], p["수당_합계_세전"] * plan.CYCLES_PER_YEAR)


class TestPercentile(unittest.TestCase):
    def test_21_top_bracket(self):
        got = plan.percentile(120_000_000)
        self.assertEqual(got["이_구간까지_누적_인원"], 41)

    def test_22_ten_million_is_top_398(self):
        got = plan.percentile(12_000_000)
        self.assertEqual(got["이_구간까지_누적_인원"], 398)

    def test_23_zero_is_everyone(self):
        got = plan.percentile(0)
        self.assertEqual(got["상위_비율"], 100.0)

    def test_24_any_payout_is_top_30pct(self):
        got = plan.percentile(1)
        self.assertEqual(got["이_구간까지_누적_인원"], plan.FTC["수당_수령_판매원수"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
