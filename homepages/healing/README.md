# 힐링엔터테인먼트 홈페이지

정적 사이트 — GitHub Pages 로 배포: https://www.healingenter.co.kr/

제작: 큰길브리지 (주식회사 브리지미디어)

## 업무 도구 (2026-10-03, 큰길이벤트기획 기능을 바로기획 기준본대로 옮김)

| 기능 | 주소 | 서버 |
|---|---|---|
| 자동 견적서(손님용) | `quote.html` | 문의 서버(공용) |
| 견적서 발행 · 저장함(관리자) | `quote.html?admin=1` | 저장함 폰·PC 같이 보기는 계약 서버 |
| 전자계약서 | `contract.html?admin=1` | 계약 서버(`apps-script/contract`) — 없으면 서명 통보만 메일로 |
| 거래명세서 | `statement.html?admin=1` | 없음 |
| 사진 올리기 + 블로그 · 인스타 글 만들기 | `upload.html` | 갤러리 서버(`apps-script/gallery`) → `photos` 가지 → 현장 갤러리 페이지 |
| 행사 이야기 | `stories/` | 없음 — `python tools/make_pages.py` |
| 지역 페이지 | `areas/` | 없음 — 같은 명령 |
| 행사 준비 블로그 | `blog/` (지역별 글) · `rss.xml` | 없음 — 원본 `_blog/posts/*.json` → `node scripts/blog-check.mjs --new <파일>` → `node scripts/build-blog.mjs` (규칙 `_blog/GUIDE.md`) |
| 문의 알림 | `contact.html` 폼 · 견적서 | 문의 서버 → 대표 메일 + 큰길브리지 |
| 행사 일정 · 체크리스트 | `schedule.html` | 계약 서버(일정 기능 — 스크립트 속성 `CREW_PW` 필요) |
| 대표 전용 업무 문서함 | `office.html` | 없음 — 도구 모음 · 서버 연결 상태 · 암호 안내(noindex) |
| 유입 현황 · AI 검색 | `stats.js` · `llms.txt` · `sitemap.xml` · `robots.txt` | 큰길브리지 유입 서버 |

- 서류 3종 · `upload.html` · `schedule.html` · `quote-catalog.js` · 서버 코드 · `office.html` 은 큰길이벤트 원본에서 `python tools/port_docs.py` 로 옮긴다(원본이 바뀌면 다시 돌리면 됨). 힐링엔터테인먼트 쪽 손수정은 그 스크립트 안에 규칙으로 넣을 것.
- 직인: `assets/img/stamp-healing.png` (투명 PNG) 가 생기면 계약서 · 명세서에 찍힌다. 없으면 「(인)」 자리만.
- 계약 · 갤러리 서버는 아직 배포 전(서버 없이도 견적 · 계약 · 명세서는 동작). 배포하면 `tools/port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL` 에 주소를 넣고 다시 돌린다.
