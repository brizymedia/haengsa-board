# 업무 도구를 다른 고객사 홈페이지에 옮기는 법 (바로기획 = 기준본)

큰길이벤트기획(`~/Documents/클로드코드`)의 업무 도구를 고객사 사이트에 옮긴다. **바로기획(`~/Documents/baro-event`)이 완성된 기준본**이다.
바로기획 커밋 `3461ec5`(10종 첫 이식) · `e6ed9cf`(서버 연결) · `53d962b`(일정 · 문서함 · 최신화)를 `git show` 로 보면 무엇을 어디에 했는지 다 나온다.

## 넣을 것 (12가지)
| # | 기능 | 결과물 | 만드는 법 |
|---|---|---|---|
| 1 | 자동 견적서(손님용) | `quote.html` + `quote-catalog.js` | `tools/port_docs.py` |
| 2 | 관리자 견적서 발행(메일 · 인쇄 · PDF) | `quote.html?admin=1` | 〃 |
| 3 | 견적서 저장함 | 견적서 안 단추 | 〃 |
| 4 | 전자계약서(폰 서명) | `contract.html?admin=1` | 〃 |
| 5 | 거래명세서 | `statement.html?admin=1` | 〃 |
| 6 | 사진 올리기 + 블로그 · 인스타 글 | `upload.html` + photos 가지 + 사진 페이지가 photos.json 합쳐 보이기 | 〃 + `assets/app.js` |
| 7 | 행사 이야기 5편 | `stories/` | `tools/make_pages.py` |
| 8 | 지역 페이지 9곳 | `areas/` | 〃 |
| 9 | 문의 알림 | 문의 폼 → 공용 문의 서버 | `assets/app.js` 의 전송처 |
| 10 | 유입 현황 + AI 검색 | 전 페이지 `stats.js` 태그 · `llms.txt` · `sitemap.xml` · `robots.txt` | 손으로 + make_pages |
| 11 | 행사 일정 · 체크리스트 | `schedule.html` | `tools/port_docs.py` |
| 12 | 대표 전용 업무 문서함 | `office.html` | `tools/port_docs.py` (`office()`) |
| + | 서버 코드 | `apps-script/contract/Code.gs`(계약 · 저장함 · 일정) · `apps-script/gallery/Code.gs`(사진) + 각 README.md | `tools/port_docs.py` + README 는 바로기획 것 복사 후 이름 바꿈 |

## 순서
1. **회사 정보 모으기** — 사이트 README · `assets/app.js` · about · 바닥글. 공개 README 는 짧게 줄여 놨으니 내부 메모는 `C:\클로드코드2` 레포에서
   `git show origin/claude/dazzling-gates-elzjbq:homepages/<폴더>/README.md` (폴더: j6media · baro · healing · yegrina · haengsaon). HD기획 · 프로이벤트는
   `C:\Users\gilau\.claude\projects\C-------2\memory\hd-event-site.md` · `pro-event-renewal.md` 와 각 레포 README.
2. **`tools/port_docs.py`** — 바로기획 것을 복사해 「회사 설정」 칸만 고친다(아래 규칙은 손대지 않음. 어쩔 수 없이 고쳐야 하면 일반화해서 고치고 보고).
   - 서버 주소 `CONTRACT_URL` · `GALLERY_URL` 은 **빈 문자열**(아직 배포 전 — 형님 구글 계정으로 따로 배포한다).
   - `CATALOG` 는 그 회사가 실제로 하는 일 · 장비로(가격은 전부 `price:null`). id 는 큰길 규칙(a 음향 · b 조명/무대 · d 천막/무대 · f 인력 · h 체험 · g 기타 · p 행사 진행)을 따르면 된다.
   - `COLORS` 는 큰길 주황 계열 → 그 회사 색, `OFFICE` 도 그 회사 색. 문서 화면(견적서 등)은 어두운 바탕이므로 바탕색은 그 회사의 가장 어두운 색으로.
   - `LOGO_FILE` 은 네모 마크(파비콘 SVG 도 됨), `MAIL_LOGO` 는 **PNG**(메일 프로그램은 SVG 를 못 보여 준다. 없으면 SVG 를 playwright 로 찍어 PNG 를 만든다).
   - `NAV_SITE` · `GALLERY_PAGE` 는 그 사이트 실제 페이지 이름으로.
   - 돌린 뒤 「남은 큰길 흔적」이 주석 말고는 없어야 한다.
3. **`tools/make_pages.py`** — 바로기획 것을 복사해 `STORIES` · `AREAS` · `SERVICES` · `BASE` · `BLOG` · 전화 · 사진 이름 · 틀 페이지(`shell()`)를 그 회사 것으로.
   - **사실만.** 행사 이야기는 그 회사 사이트 글 · 블로그 글(사이트 `app.js` 의 BLOG 목록 · 사진 설명 · 회사소개 · 네이버 블로그 원문 — 필요하면 firecrawl 로 원문을 읽는다)에 있는 것만. 숫자 · 후기 · 고객 말을 지어내지 않는다. 모르는 칸은 비운다.
   - 지역 9곳은 본사 주변 실제 활동 지역. 이동 시간은 OSRM(`https://router.project-osrm.org/route/v1/driving/경도,위도;경도,위도?overview=false`) 으로 본사 → 각 시청, 5분 단위 반올림, 「막히지 않을 때 기준」 표기. 그 지역 실적은 기록이 있을 때만.
   - 생성 페이지가 쓰는 CSS(`.phead` `.story` `.scards` `.scard` `.sgrid` `.area3` `.apics` `.asvc` `.arow(s)` `.callband` `.alist` `.snote` `.h2s` `.h3s` 등)는 바로기획 `git show 3461ec5 -- assets/style.css` 에 있다 → 그 사이트 `style.css` 끝에 그 사이트 색 변수로 옮긴다.
4. **사이트 본문 손보기** (바로기획 `3461ec5` 의 index · about · contact · notice · portfolio · service · app.js 변경을 참고)
   - 메뉴 · 바닥글에 「자동 견적서(quote.html)」 「행사 이야기(stories/)」 「운영 지역(areas/)」 링크. **office · schedule 은 공개 링크 금지.**
   - 모든 공개 페이지 `<head>` 에 `<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="ID"></script>` (생성 페이지에도 들어가게 shell 에 있으면 됨).
   - 문의 폼 전송처 = 공용 문의 서버 `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec`
     (`text/plain` JSON, `page: location.href`, `service` 에 회사 이름 포함 — 서버가 page 의 레포 이름으로 회사를 알아본다). 실패하면 기존 문자 · 복사 대체 동작 유지.
   - 사진 페이지가 photos 가지의 `photos/photos.json` 을 합쳐 보이게(바로기획 app.js 의 UP_LIST · UP_IMG · UP_CAT 부분). `UP_CAT` 키 = `UPLOAD_CATS` 의 slug.
   - `llms.txt`(바로기획 형식, 사실만) · `robots.txt`(contract · statement · upload · schedule · office Disallow) · `sitemap.xml`(make_pages 가 씀).
5. **photos 가지** — 바로기획 `photos` 가지와 같은 모양(`README.md` + `photos/photos.json`, categories 는 UPLOAD_CATS, count 0)을 고아 가지로 만들어 push.
6. **검증(필수)** — `python -m http.server <내 포트>` 로 띄우고 playwright(Python 3.13: `C:\Users\gilau\AppData\Local\Programs\Python\Python313\python.exe`, `channel='chrome'`)로 폭 375 · 1280 에서
   모든 페이지(기존 + 새 페이지 + `quote.html?admin=1` · `contract.html?admin=1` · `statement.html?admin=1` · schedule · office · upload)를 열어
   스크립트 오류 0 · 가로 넘침 0 · 깨진 그림 0 · 견적서 품목 수 > 0 · 손님 화면(admin 없음)에 직인/인쇄 단추 없음을 확인. Claude 브라우저 창(pane)은 쓰지 말 것(총괄이 쓰는 중).
7. **커밋 · push** — 한국어 메시지(무엇을 · 왜) + 끝줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `git -c rebase.autoStash=true pull --rebase` 뒤 push.
   haengsa-board · ai-make · 큰길이벤트 레포는 건드리지 않는다(총괄이 한다).

## 지킬 것
- 비밀(암호 · 열쇠 · 토큰)은 어디에도 적지 않는다. 수정 모드 열쇠도.
- 기존 디자인 · 문구는 필요한 곳만 손댄다. 결과 HTML 을 손으로 고치지 말고 스크립트 규칙으로.
- Windows: Python 실행 전 `PYTHONIOENCODING=utf-8`. 파일은 `newline='\n'` 로 쓴다. 레포를 Temp 에 두지 말 것.
