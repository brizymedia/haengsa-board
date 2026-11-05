# 한국체대 예그리나 홈페이지

정적 사이트 — GitHub Pages 로 배포: https://www.knsuyegrina.co.kr/

제작: 큰길브리지 (주식회사 브리지미디어)

## 업무 도구 (2026-10-03, 바로기획 기준본에서 옮김)

| 기능 | 주소 | 서버 |
|---|---|---|
| 자동 견적서(손님용) · 견적서 발행 · 저장함 | `quote.html` · `quote.html?admin=1` | 문의 서버(공용) · 저장함 같이 보기는 계약 서버 |
| 전자계약서 · 거래명세서 | `contract.html?admin=1` · `statement.html?admin=1` | 계약 서버(`apps-script/contract`, 배포 전) |
| 행사 일정 · 체크리스트 · 대표 전용 문서함 | `schedule.html` · `office.html` (공개 링크 없음) | 계약 서버 |
| 사진 올리기 + 블로그 · 인스타 글 | `upload.html` → `photos` 가지 → 현장사진 페이지 | 갤러리 서버(`apps-script/gallery`, 배포 전) |
| 행사 이야기 5편 · 지역 9곳 · sitemap | `stories/` · `areas/` | 없음 — `python tools/make_pages.py` |
| 행사 준비 블로그 10편(2026-10-28) | `blog/` · `rss.xml` | 없음 — 원본 `_blog/`(규칙 `_blog/GUIDE.md`), `node scripts/blog-check.mjs --new …` → `node scripts/build-blog.mjs`. make_pages.py 를 돌리면 sitemap 의 블로그 주소가 빠지니 build-blog 를 다시 돌릴 것 |
| 유입 현황 · AI 검색 | `stats.js` · `llms.txt` · `robots.txt` | 큰길브리지 유입 서버 |

- 서류 · 업로드 화면은 큰길이벤트 원본에서 `python tools/port_docs.py` 로 옮긴다(결과 HTML 을 손으로 고치지 말 것). 서버를 배포하면 `CONTRACT_URL` · `GALLERY_URL` 에 넣고 다시 돌린다.
- 직인: `assets/img/stamp-yegrina.png`(투명 PNG)가 생기면 계약서 · 명세서에 찍힌다. 없으면 「(인)」 자리만.
