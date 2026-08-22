# -*- coding: utf-8 -*-
"""(주)비아블 '셀비아' 보상플랜 계산 모델

무엇을 하는 프로그램인가
  한 기수(15일)에 받게 될 수당을 항목별로 계산하고, 그 결과가
  공정거래위원회가 공개한 실제 판매원 분포에서 어느 자리인지 되짚어 준다.
  "얼마 벌 수 있나"보다 "그 금액을 받으려면 몇 등이어야 하나"가 핵심이다.

숫자의 출처 등급 — 이 구분을 지우지 말 것
  [공시]   공정거래위원회 사업자정보공개, 2025년도 실적 (2026년 공개)
  [규정]   (주)비아블 회원관리규정 — 회사 홈페이지 공개분
  [사업자] 현직 사업자 블로그 공개분. 회사 공식 확정치가 아니다
  [가정]   공개된 곳이 없어 이 프로그램이 임의로 둔 값. 반드시 직접 확인할 것

실행
  python plan.py                     # 기본 시나리오 3개를 함께 보여준다
  python plan.py --rank 디렉터 --weak 2100000 --strong 5000000 --referral 300000
  python plan.py --json              # 결과를 JSON 으로
"""
import argparse
import json
from dataclasses import dataclass

# ─────────────────────────────────────────────────────────────
# 회사 실적 — 공정거래위원회 사업자정보공개 (2025년도 실적)
# ─────────────────────────────────────────────────────────────
FTC = {
    "연도": "2025년도 실적 (2026년 공개)",
    "총매출액_부가세포함": 91_297_719_916,   # [공시]
    "재무제표상_매출액": 82_997_927_197,     # [공시]
    "후원수당_총액": 31_648_246_777,         # [공시]
    "후원수당_지급률": 0.3466,               # [공시] 법정 상한 35%
    "등록_판매원수": 56_117,                 # [공시]
    "수당_수령_판매원수": 16_902,            # [공시]
    "당기순이익": 5_143_930_087,             # [공시]
    "최근3년_시정조치": "내역 없음",          # [공시]
}

# 연간 후원수당 금액 구간별 판매원 수와 지급액 [공시]
# (하한, 상한 또는 None, 인원, 구간 총지급액)  — 높은 금액부터
# 인원 합계 56,117명 / 금액 합계 31,648,246,777원. 둘 다 공시 총계와 맞는다 (tests.py 가 검산)
DISTRIBUTION = [
    (100_000_000, None,          41, 11_611_382_734),
    ( 50_000_000, 100_000_000,   51,  3_624_754_940),
    ( 30_000_000,  50_000_000,   78,  2_993_506_492),
    ( 20_000_000,  30_000_000,   78,  1_878_566_199),
    ( 10_000_000,  20_000_000,  150,  2_168_841_221),
    (  5_000_000,  10_000_000,  339,  2_317_581_765),
    (  1_000_000,   5_000_000, 1_858,  4_005_219_482),
    (    500_000,   1_000_000, 2_008,  1_434_500_042),
    (          1,     500_000, 12_299, 1_613_893_902),
    (          0,           1, 39_215,             0),
]

LEGAL_CAP = 0.35        # [규정] 회원관리규정 제11조 — 총매출액의 35% 초과 불가
CYCLES_PER_YEAR = 24    # [사업자] 월 2기수 (1~15일 / 16~말일)
WITHHOLDING = 0.033     # 사업소득 원천징수 3.3%


@dataclass(frozen=True)
class Rank:
    """직급 한 단계.

    cum_pv    승급에 필요한 누적 PV. 확인 안 된 단계는 None
    leg_cv    품위유지보너스 소실적 기준 CV (기수당)
    dignity   품위유지보너스 (원, 기수당)
    """
    name: str
    cum_pv: int | None
    leg_cv: int | None
    dignity: int


# 직급 10단계. 아래로 갈수록 높다.
# 누적 PV 는 멤버·매니아·에메랄드·다이아몬드만 공개분이 있다. [사업자]
# 소실적 기준 CV 와 품위유지보너스는 디렉터 이상 7단계가 공개돼 있다. [사업자]
RANKS = [
    Rank("회원",         None,          None,        0),
    Rank("멤버",         10_000,        None,        0),
    Rank("매니아",       700_000,       None,        0),
    Rank("디렉터",       None,          2_100_000,   150_000),
    Rank("에메랄드",     14_000_000,    3_500_000,   300_000),
    Rank("다이아몬드",   100_000_000,   10_000_000,  750_000),
    Rank("그린다이아몬드", None,        19_000_000,  1_400_000),
    Rank("블루다이아몬드", None,        34_000_000,  2_300_000),
    Rank("레드다이아몬드", None,        65_000_000,  4_000_000),
    Rank("크라운",       None,          135_000_000, 6_000_000),
]

# 표에 넣을 짧은 이름. 화면(simulator.html)과 같은 표기를 쓴다.
SHORT = {
    "회원": "회원", "멤버": "멤버", "매니아": "매니아", "디렉터": "디렉터",
    "에메랄드": "에메랄드", "다이아몬드": "다이아", "그린다이아몬드": "그린다",
    "블루다이아몬드": "블루다", "레드다이아몬드": "레드다", "크라운": "크라운",
}

RANK_INDEX = {r.name: i for i, r in enumerate(RANKS)}

# ─────────────────────────────────────────────────────────────
# 수당률
# ─────────────────────────────────────────────────────────────
REFERRAL_RATE = 0.12   # [사업자] 추천보너스. 110,000CV × 12% = 13,200원 예시로 확인
SPONSOR_RATE = 0.10    # [가정] 후원(바이너리)보너스. 공개된 곳이 없다
CV_RATIO = 0.50        # [사업자] 회원가 대비 CV 비율. 실제는 품목별 32~73%
SUBSCRIPTION_CV = 10_000  # [사업자] 구독 기준. 디렉터 기준값만 확인됨


def rank_by_name(name: str) -> Rank:
    if name not in RANK_INDEX:
        raise ValueError(f"모르는 직급: {name} — {', '.join(RANK_INDEX)}")
    return RANKS[RANK_INDEX[name]]


def dignity_rank(rank: Rank, weak_cv: int) -> Rank:
    """품위유지보너스는 직급과 소실적을 동시에 만족해야 한다.

    직급이 블루다이아라도 소실적이 그린다이아 수준이면 그린다이아 기준만 지급된다.
    그래서 '직급'과 '소실적이 닿는 최고 단계' 중 낮은 쪽을 택한다. [사업자]
    """
    reached = RANKS[0]
    for r in RANKS:
        if r.leg_cv is not None and weak_cv >= r.leg_cv:
            reached = r
    return min(reached, rank, key=lambda x: RANK_INDEX[x.name])


def cycle_payout(rank_name="디렉터", weak_cv=0, strong_cv=0, referral_cv=0,
                 subscription_cv=SUBSCRIPTION_CV, referral_rate=REFERRAL_RATE,
                 sponsor_rate=SPONSOR_RATE, cv_ratio=CV_RATIO) -> dict:
    """한 기수(15일) 수당을 항목별로 계산한다."""
    rank = rank_by_name(rank_name)

    # 구독을 채우지 못하면 발생한 수당을 받아갈 수 없다. [사업자]
    subscribed = subscription_cv >= SUBSCRIPTION_CV

    referral = int(referral_cv * referral_rate)
    sponsor = int(weak_cv * sponsor_rate)          # 바이너리는 약한 레그 기준
    eff = dignity_rank(rank, weak_cv)
    dignity = eff.dignity

    gross = (referral + sponsor + dignity) if subscribed else 0
    tax = int(gross * WITHHOLDING)
    cost = int(subscription_cv / cv_ratio) if cv_ratio else 0
    net = gross - tax - cost

    return {
        "직급": rank.name,
        "품위유지_적용직급": eff.name,
        "구독_충족": subscribed,
        "추천보너스": referral,
        "후원보너스": sponsor,
        "품위유지보너스": dignity,
        "수당_합계_세전": gross,
        "원천징수_3.3%": -tax,
        "구독_구매비용": -cost,
        "기수_실수령": net,
        "연환산_세전": gross * CYCLES_PER_YEAR,
        "연환산_실수령": net * CYCLES_PER_YEAR,
    }


def percentile(annual: int) -> dict:
    """연간 수당 금액이 실제 판매원 56,117명 중 어느 자리인지 돌려준다. [공시]"""
    total = FTC["등록_판매원수"]
    above = 0
    for low, high, count, _amt in DISTRIBUTION:
        if annual >= low:
            above += count
            return {
                "구간": _label(low, high),
                "이_구간까지_누적_인원": above,
                "상위_비율": round(above / total * 100, 3),
                "전체_등록_판매원": total,
            }
        above += count
    return {"구간": "0원", "이_구간까지_누적_인원": total,
            "상위_비율": 100.0, "전체_등록_판매원": total}


def _label(low, high):
    if high is None:
        return f"연 {low // 100_000_000}억원 이상"
    if low == 0:
        return "0원"
    return f"연 {low:,}원 이상 ~ {high:,}원 미만"


def implied_check() -> dict:
    """가정한 수당률이 회사 전체로는 말이 되는지 되짚는다.

    회사가 실제로 푼 돈은 매출의 34.66%다. 개인 계산에 넣은 요율이 아무리
    커도 전체 합이 35%를 넘을 수는 없고, 넘으면 회원관리규정 제11조의 CAP 이
    걸려 전원 지급률이 일괄로 깎인다.
    """
    return {
        "회사_실제_지급률": FTC["후원수당_지급률"],
        "법정_상한": LEGAL_CAP,
        "여유": round(LEGAL_CAP - FTC["후원수당_지급률"], 4),
        "설명": "상한에 0.34%p 남기고 붙어 있다. 개인 수당률을 올려 잡을수록 "
                "CAP(전원 일괄 삭감) 가능성을 함께 봐야 한다.",
    }


# ─────────────────────────────────────────────────────────────
# 인원으로 계산하기 — "직추천 몇 명, 조직 몇 명이면 어떻게 되나"
# ─────────────────────────────────────────────────────────────
PERSON_MONTHLY_SPEND = 220_000   # [사업자] 셀비아 앰플 1세트 회원가
# 같은 예시에서 220,000원 = 110,000CV 로 CV_RATIO 0.5 가 확인된다.


def person_cycle_cv(monthly_spend=PERSON_MONTHLY_SPEND, cv_ratio=CV_RATIO):
    """한 사람이 한 기수(15일)에 만드는 CV. 월 구매액의 절반이 한 기수 몫이다."""
    return monthly_spend * cv_ratio / 2


def org_legs(direct, downline_each, balance=0.5):
    """직추천 수와 1인당 하위 인원으로 조직을 A·B 두 레그로 나눈다.

    balance 는 약한 레그가 차지하는 몫. 0.5 면 정확히 반반이다.
    바이너리는 약한 쪽으로 정산하므로 균형이 무너질수록 손해다.
    """
    total = direct * (1 + downline_each)
    weak_share = min(balance, 1 - balance)
    weak = int(round(total * weak_share))
    return total, weak, total - weak


def achieved_rank(weak_cv, cum_pv, direct):
    """소실적 CV·누적 PV·직추천 수로 직급을 판정한다.

    아래에서 위로 올라가다 하나라도 못 넘으면 거기서 멈춘다. 조건이 공개된
    항목만 검사하므로(미공개는 통과 처리) 실제보다 후하게 나올 수 있다. [사업자]
    """
    best = RANKS[0]
    director = RANK_INDEX["디렉터"]
    for r in RANKS[1:]:
        if r.leg_cv is not None and weak_cv < r.leg_cv:
            break
        if r.cum_pv is not None and cum_pv < r.cum_pv:
            break
        if RANK_INDEX[r.name] >= director and direct < 2:
            break   # 디렉터부터는 A·B 양쪽에 직추천이 하나씩 있어야 한다
        best = r
    return best


def by_headcount(direct=4, downline_each=10, monthly_spend=PERSON_MONTHLY_SPEND,
                 balance=0.5, months=12, cv_ratio=CV_RATIO,
                 referral_rate=REFERRAL_RATE, sponsor_rate=SPONSOR_RATE):
    """인원만 넣으면 직급과 수당을 돌려준다."""
    per = person_cycle_cv(monthly_spend, cv_ratio)
    total, weak_n, strong_n = org_legs(direct, downline_each, balance)
    weak_cv = int(weak_n * per)
    strong_cv = int(strong_n * per)
    referral_cv = int(direct * per)          # 직추천한 사람 본인들의 구매분
    cum_pv = int(total * per * 2 * months)   # 누적 PV 는 소멸 없이 쌓인다 [사업자]

    rank = achieved_rank(weak_cv, cum_pv, direct)
    p = cycle_payout(rank_name=rank.name, weak_cv=weak_cv, strong_cv=strong_cv,
                     referral_cv=referral_cv, referral_rate=referral_rate,
                     sponsor_rate=sponsor_rate, cv_ratio=cv_ratio)
    p.update({
        "직추천_인원": direct,
        "1인당_하위인원": downline_each,
        "조직_총인원": total,
        "약한레그_인원": weak_n,
        "강한레그_인원": strong_n,
        "1인당_기수CV": int(per),
        "소실적_CV": weak_cv,
        "누적_PV": cum_pv,
        "월_수당_세전": p["수당_합계_세전"] * 2,
        "월_실수령": p["기수_실수령"] * 2,
    })
    return p


def next_rank_gap(rank_name, weak_cv, per_person_cv):
    """다음 직급까지 약한 레그에 몇 명이 더 필요한지 알려준다."""
    i = RANK_INDEX[rank_name]
    for r in RANKS[i + 1:]:
        if r.leg_cv is None:
            continue
        need_cv = max(0, r.leg_cv - weak_cv)
        return {"다음_직급": r.name, "부족한_CV": need_cv,
                "약한레그_추가인원": int(-(-need_cv // per_person_cv)) if per_person_cv else 0}
    return None


def matrix(directs=(2, 3, 4, 6, 8, 10), downlines=(0, 2, 5, 10, 25, 50, 100), **kw):
    """직추천 수 × 1인당 하위 인원 조합표. 칸마다 직급과 월 수당."""
    out = []
    for d in directs:
        row = []
        for dl in downlines:
            r = by_headcount(direct=d, downline_each=dl, **kw)
            row.append({"직추천": d, "하위": dl, "총인원": r["조직_총인원"],
                        "직급": r["직급"], "월수당": r["월_수당_세전"]})
        out.append(row)
    return out


SCENARIOS = [
    ("갓 시작 — 본인 구독만, 추천 1명",
     dict(rank_name="멤버", weak_cv=0, strong_cv=0, referral_cv=110_000)),
    ("자리 잡음 — 디렉터, 양쪽 레그 가동",
     dict(rank_name="디렉터", weak_cv=2_100_000, strong_cv=5_000_000, referral_cv=440_000)),
    ("상위권 — 다이아몬드",
     dict(rank_name="다이아몬드", weak_cv=10_000_000, strong_cv=25_000_000, referral_cv=880_000)),
]


def _won(n):
    return f"{n:,}원"


def report_headcount(direct, down, months=12, **kw):
    """인원으로 넣었을 때의 한 화면 요약."""
    r = by_headcount(direct=direct, downline_each=down, months=months, **kw)
    pc = percentile(r["연환산_세전"])
    gap = next_rank_gap(r["직급"], r["소실적_CV"], r["1인당_기수CV"])
    nxt = ("최고 직급" if gap is None
           else f"{gap['다음_직급']}까지 약한 쪽에 {gap['약한레그_추가인원']:,}명 더")
    return "\n".join([
        f"■ 직추천 {direct}명 · 1인당 하위 {down}명 · {months}개월 활동",
        f"   조직 {r['조직_총인원']:,}명  =  약한 레그 {r['약한레그_인원']:,}명 + "
        f"강한 레그 {r['강한레그_인원']:,}명",
        f"   직급 {r['직급']}   ({nxt})",
        "",
        f"   추천보너스      {_won(r['추천보너스']):>14}",
        f"   후원보너스      {_won(r['후원보너스']):>14}   [가정 요율]",
        f"   품위유지보너스  {_won(r['품위유지보너스']):>14}",
        f"   ─────────────────────────────",
        f"   기수 수당(세전) {_won(r['수당_합계_세전']):>14}",
        f"   월 수당(세전)   {_won(r['월_수당_세전']):>14}",
        f"   월 실수령       {_won(r['월_실수령']):>14}",
        "",
        f"   ↳ 연 세전 {_won(r['연환산_세전'])} 은 실제 판매원 {pc['전체_등록_판매원']:,}명 중",
        f"     상위 {pc['이_구간까지_누적_인원']:,}명 이내 = 상위 {pc['상위_비율']}%",
        "",
    ])


def _w(text):
    """터미널 표시 폭. 한글·전각은 두 칸으로 센다."""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def _pad(text, width, right=True):
    gap = " " * max(0, width - _w(text))
    return gap + text if right else text + gap


def report_matrix(months=12, **kw):
    """직추천 × 하위 인원 조합표를 글자로 그린다."""
    directs = (2, 3, 4, 6, 8, 10, 12)
    downs = (0, 2, 5, 10, 25, 50, 100)
    grid = matrix(directs=directs, downlines=downs, months=months, **kw)
    lines = [" 직추천 × 1인당 하위 인원 → 직급 / 월 수당(세전, 만원)", ""]
    lines.append(_pad("", 8, False) + "".join(_pad(f"{d}명", 9) for d in downs))
    for row, d in zip(grid, directs):
        top = _pad(f"{d}명", 8) + "".join(_pad(SHORT[c["직급"]], 9) for c in row)
        bot = _pad("", 8, False) + "".join(
            _pad(f"{round(c['월수당'] / 10_000):,}만", 9) for c in row)
        lines += [top, bot, ""]
    return "\n".join(lines)


def report(title, kwargs):
    p = cycle_payout(**kwargs)
    pc = percentile(p["연환산_세전"])
    lines = [
        f"■ {title}",
        f"   직급 {p['직급']}   품위유지 적용 {p['품위유지_적용직급']}   "
        f"구독 {'충족' if p['구독_충족'] else '미충족 → 수당 0원'}",
        f"   추천보너스      {_won(p['추천보너스']):>14}",
        f"   후원보너스      {_won(p['후원보너스']):>14}   [가정 요율]",
        f"   품위유지보너스  {_won(p['품위유지보너스']):>14}",
        f"   ─────────────────────────────",
        f"   기수 수당(세전) {_won(p['수당_합계_세전']):>14}",
        f"   원천징수 3.3%   {_won(p['원천징수_3.3%']):>14}",
        f"   구독 구매비용   {_won(p['구독_구매비용']):>14}",
        f"   기수 실수령     {_won(p['기수_실수령']):>14}",
        f"   연환산 실수령   {_won(p['연환산_실수령']):>14}",
        "",
        f"   ↳ 이 수당(연 세전 {_won(p['연환산_세전'])})을 받으려면",
        f"     실제 판매원 {pc['전체_등록_판매원']:,}명 중 "
        f"상위 {pc['이_구간까지_누적_인원']:,}명 이내 = 상위 {pc['상위_비율']}%",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="(주)비아블 셀비아 보상플랜 계산기")
    ap.add_argument("--rank", default=None, help="직급명 (예: 디렉터)")
    ap.add_argument("--weak", type=int, default=0, help="소실적 레그 기수 CV")
    ap.add_argument("--strong", type=int, default=0, help="대실적 레그 기수 CV")
    ap.add_argument("--referral", type=int, default=0, help="직접 추천분 기수 CV")
    ap.add_argument("--subscription", type=int, default=SUBSCRIPTION_CV, help="본인 구독 CV")
    ap.add_argument("--sponsor-rate", type=float, default=SPONSOR_RATE, help="후원보너스 요율 [가정]")
    ap.add_argument("--direct", type=int, default=None, help="직접 추천한 사람 수 (인원 기준 계산)")
    ap.add_argument("--down", type=int, default=10, help="추천한 1인당 하위 인원")
    ap.add_argument("--months", type=int, default=12, help="활동 개월 수")
    ap.add_argument("--matrix", action="store_true", help="직추천 × 하위 인원 조합표")
    ap.add_argument("--json", action="store_true", help="JSON 으로 출력")
    a = ap.parse_args()

    if a.matrix:
        print(report_matrix(months=a.months, sponsor_rate=a.sponsor_rate))
        return

    if a.direct is not None:
        print(report_headcount(a.direct, a.down, months=a.months,
                               sponsor_rate=a.sponsor_rate))
        return

    if a.rank:
        kw = dict(rank_name=a.rank, weak_cv=a.weak, strong_cv=a.strong,
                  referral_cv=a.referral, subscription_cv=a.subscription,
                  sponsor_rate=a.sponsor_rate)
        runs = [("입력한 조건", kw)]
    else:
        runs = SCENARIOS

    if a.json:
        out = []
        for title, kw in runs:
            p = cycle_payout(**kw)
            out.append({"시나리오": title, "결과": p,
                        "실제_위치": percentile(p["연환산_세전"])})
        print(json.dumps({"회사실적": FTC, "계산": out,
                          "정합성": implied_check()},
                         ensure_ascii=False, indent=2))
        return

    print("=" * 62)
    print(" (주)비아블 '셀비아' 보상플랜 계산기")
    print(f" 기준 실적: {FTC['연도']} — 공정거래위원회 사업자정보공개")
    print("=" * 62)
    print()
    for title, kw in runs:
        print(report(title, kw))

    chk = implied_check()
    print("─" * 62)
    print(f" 회사 실제 후원수당 지급률 {chk['회사_실제_지급률'] * 100:.2f}% "
          f"/ 법정 상한 {chk['법정_상한'] * 100:.0f}%")
    print(f" {chk['설명']}")
    print()
    print(" 실제 분포 (등록 판매원 56,117명, 2025년도)")
    cum = 0
    for low, high, count, _amt in DISTRIBUTION:
        cum += count
        print(f"   {_label(low, high):>34}  {count:>7,}명   누적 상위 {cum / 56_117 * 100:6.2f}%")
    print()
    print(" ※ [가정] 표시 항목은 공개된 근거가 없다. 추천인에게 공식 마케팅플랜을 받아 확인할 것.")


if __name__ == "__main__":
    main()
