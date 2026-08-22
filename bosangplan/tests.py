# -*- coding: utf-8 -*-
"""보상플랜 계산 모델 단위 테스트 38항목

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


class TestHeadcount(unittest.TestCase):
    """인원으로 계산하기 — 직추천 몇 명, 조직 몇 명이면 어떻게 되나."""

    def test_25_person_cycle_cv(self):
        # 220,000원 구매 = 110,000CV (공개 예시). 한 기수는 그 절반
        self.assertEqual(plan.person_cycle_cv(), 55_000)

    def test_26_legs_split_evenly(self):
        total, weak, strong = plan.org_legs(4, 10, balance=0.5)
        self.assertEqual(total, 44)
        self.assertEqual(weak + strong, total)
        self.assertEqual(weak, 22)

    def test_27_lopsided_legs_hurt(self):
        _t, weak_even, _s = plan.org_legs(4, 10, balance=0.5)
        _t, weak_bad, _s = plan.org_legs(4, 10, balance=0.2)
        self.assertLess(weak_bad, weak_even)

    def test_28_balance_is_symmetric(self):
        # 0.2 든 0.8 이든 약한 쪽은 같다
        self.assertEqual(plan.org_legs(4, 10, 0.2)[1], plan.org_legs(4, 10, 0.8)[1])

    def test_29_director_needs_two_referrals(self):
        # 실적이 충분해도 직추천이 1명이면 디렉터가 안 된다
        got = plan.achieved_rank(weak_cv=5_000_000, cum_pv=10**9, direct=1)
        self.assertEqual(got.name, "매니아")

    def test_30_director_with_two_referrals(self):
        got = plan.achieved_rank(weak_cv=2_100_000, cum_pv=10**9, direct=2)
        self.assertEqual(got.name, "디렉터")

    def test_31_cum_pv_blocks_emerald(self):
        # 소실적은 에메랄드급이지만 누적 PV 가 모자라면 디렉터에서 멈춘다
        got = plan.achieved_rank(weak_cv=3_500_000, cum_pv=1_000_000, direct=4)
        self.assertEqual(got.name, "디렉터")

    def test_32_rank_never_skips_a_step(self):
        # 그린다이아는 누적 PV 조건이 미공개지만, 앞단 다이아몬드에서 막히면 못 간다
        got = plan.achieved_rank(weak_cv=19_000_000, cum_pv=50_000_000, direct=4)
        self.assertEqual(got.name, "에메랄드")

    def test_33_by_headcount_totals(self):
        r = plan.by_headcount(direct=4, downline_each=10)
        self.assertEqual(r["조직_총인원"], 44)
        self.assertEqual(r["약한레그_인원"] + r["강한레그_인원"], 44)
        self.assertEqual(r["소실적_CV"], r["약한레그_인원"] * r["1인당_기수CV"])

    def test_34_monthly_is_two_cycles(self):
        r = plan.by_headcount(direct=4, downline_each=10)
        self.assertEqual(r["월_수당_세전"], r["수당_합계_세전"] * 2)

    def test_35_bigger_org_pays_more(self):
        small = plan.by_headcount(direct=4, downline_each=10)["월_수당_세전"]
        big = plan.by_headcount(direct=4, downline_each=50)["월_수당_세전"]
        self.assertGreater(big, small)

    def test_36_next_rank_gap(self):
        gap = plan.next_rank_gap("매니아", 1_210_000, 55_000)
        self.assertEqual(gap["다음_직급"], "디렉터")
        self.assertEqual(gap["약한레그_추가인원"], 17)   # 890,000CV ÷ 55,000 올림

    def test_37_crown_has_no_next(self):
        self.assertIsNone(plan.next_rank_gap("크라운", 10**9, 55_000))

    def test_38_matrix_shape(self):
        m = plan.matrix(directs=(2, 4), downlines=(0, 10, 50))
        self.assertEqual(len(m), 2)
        self.assertEqual(len(m[0]), 3)
        self.assertIn("직급", m[0][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
