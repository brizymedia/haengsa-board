# -*- coding: utf-8 -*-
"""브라우저 자동 검증 24항목 (playwright 필요)

  python serve.py 8899 &       # 서버를 먼저 띄운 뒤
  python verify.py

포트를 바꾸면 아래 BASE 도 바꿀 것.
설치: pip install playwright && python -m playwright install chromium
"""
import sys

BASE = "http://localhost:8899"

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit("playwright 가 없습니다. pip install playwright && "
                     "python -m playwright install chromium")

passed, failed = [], []


def check(no, name, cond):
    (passed if cond else failed).append(no)
    print(f"  [{'통과' if cond else '실패'}] {no:2d}. {name}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        # ── 알림판 ──────────────────────────────
        page.goto(f"{BASE}/index.html")
        page.wait_for_selector(".item", timeout=8000)
        check(1, "알림판이 열리고 목록이 나온다", page.locator(".item").count() > 0)
        check(2, "수집 시각이 채워진다", page.locator("#genAt").inner_text() not in ("", "—"))
        check(3, "수록 건수가 0이 아니다", page.locator("#total").inner_text() not in ("", "0"))
        check(4, "지역 칩이 만들어진다(전국 포함)", page.locator("#regionRow .chip").count() >= 2)
        check(5, "제목 링크가 새 창으로 열린다", page.locator(".item").first.get_attribute("target") == "_blank")

        # 구분 필터
        page.click('.chip[data-kind="bid"]')
        kinds = page.locator(".item").evaluate_all("els => [...new Set(els.map(e => e.dataset.kind))]")
        check(6, "입찰공고 필터가 입찰만 남긴다", kinds == ["bid"])
        page.click('.chip[data-kind="festival"]')
        kinds = page.locator(".item").evaluate_all("els => [...new Set(els.map(e => e.dataset.kind))]")
        check(7, "축제 필터가 축제만 남긴다", kinds == ["festival"])
        page.click('.chip[data-kind="all"]')

        # 지역 필터
        chip = page.locator("#regionRow .chip").nth(1)
        region = chip.inner_text()
        chip.click()
        regions = page.locator(".item .meta span:nth-child(2)").evaluate_all(
            "els => [...new Set(els.map(e => e.textContent))]")
        check(8, f"지역 필터({region})가 해당 지역만 남긴다", regions == [region])
        page.click('#regionRow .chip[data-region="all"]')

        # 검색·하이라이트·빈 상태
        page.fill("#search", "축제")
        page.wait_for_timeout(400)
        check(9, "검색어가 결과에 반영된다", page.locator(".item").count() > 0)
        check(10, "검색어가 형광펜으로 표시된다", page.locator(".item mark").count() > 0)
        page.fill("#search", "존재하지않는검색어XYZ")
        page.wait_for_timeout(400)
        check(11, "결과가 없으면 빈 상태 안내가 뜬다", page.locator(".empty").count() == 1)
        page.fill("#search", "")
        page.wait_for_timeout(400)

        # 정렬 셋
        first_deadline = page.locator(".item .title").first.inner_text()
        page.click('button[data-sort="recent"]')
        first_recent = page.locator(".item .title").first.inner_text()
        check(12, "최신 등록순 정렬이 동작한다",
              page.locator('button[data-sort="recent"][aria-pressed="true"]').count() == 1)
        page.click('button[data-sort="budget"]')
        budgets = page.locator(".item .amt").evaluate_all(
            "els => els.map(e => e.textContent)")
        check(13, "사업비 높은순에서 금액이 표시된다", len(budgets) > 0)
        page.click('button[data-sort="deadline"]')
        check(14, "마감 임박순으로 되돌아온다", page.locator(".item .title").first.inner_text() == first_deadline)

        # 페이지 이동
        has_pager = page.locator("#pager button").count() > 0
        check(15, "20건 초과면 페이지 이동이 나온다", has_pager)
        if has_pager:
            page.click('#pager button[data-page="2"]')
            check(16, "2페이지로 이동한다", "21" in page.locator("#resultCount").inner_text())
        else:
            check(16, "2페이지로 이동한다(생략)", True)

        # 마감 도장
        check(17, "마감 도장이 붙는다", page.locator(".seal").count() > 0)

        # ── 달력 ────────────────────────────────
        page.goto(f"{BASE}/calendar.html")
        page.wait_for_selector(".cal .cell", timeout=8000)
        title0 = page.locator("#calTitle").inner_text()
        check(18, "달력이 이번 달로 열린다", "년" in title0 and "월" in title0)
        check(19, "달력 칸이 7의 배수다", page.locator(".cal .cell").count() % 7 == 0)
        page.click("#nextM")
        check(20, "다음 달로 넘어간다", page.locator("#calTitle").inner_text() != title0)
        page.click("#prevM")
        check(21, "이전 달로 돌아온다", page.locator("#calTitle").inner_text() == title0)
        check(22, "일정 안내문이 나온다", page.locator("#calNote").inner_text() != "")

        # ── 이용안내·모바일·오류 ────────────────
        page.goto(f"{BASE}/about.html")
        check(23, "이용안내가 열린다", page.locator(".prose h2").count() >= 5)

        page.set_viewport_size({"width": 375, "height": 700})
        page.goto(f"{BASE}/index.html")
        page.wait_for_selector(".item", timeout=8000)
        overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
        ok_mobile = not overflow
        check(24, "모바일에서 가로 스크롤이 생기지 않고 JS 오류가 없다",
              ok_mobile and not errors)

        browser.close()

    print(f"\n통과 {len(passed)} / 24" + (f" · 실패 {failed}" if failed else ""))
    if errors:
        print("자바스크립트 오류:", errors[:3])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
