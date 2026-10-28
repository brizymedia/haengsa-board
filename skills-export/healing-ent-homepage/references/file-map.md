# 파일 지도 (커밋 8ecc69b, 파일 173개 · 약 18MB)

표의 「만드는 법」이 「생성」이면 손으로 고치지 말고 생성기를 고쳐 다시 돌린다.

## 공개 페이지 (손으로 고침, 사장님 수정 모드 있음)

| 파일 | 줄 | 내용 | 비고 |
|---|---|---|---|
| `index.html` | 267 | 대문 | LocalBusiness JSON-LD 는 여기만 |
| `about.html` | 186 | 회사소개 · 대표 MC · 일하는 방식 · 회사 정보 · 오시는 길 | `#greeting #mc #way #office` |
| `service.html` | 167 | 하는 일 5분야 · 이런 행사도 6 · 비용 · 진행 순서 | `#corp #school #fest #mic #sound #more #price #process` |
| `portfolio.html` | 142 | 대표 실적 8분야(더 보기 접힘) + 현장 사진 필터 | `#signature #gallery #filters #pfGrid` |
| `video.html` | 125 | 분류 단추 + 유튜브 44편 + 채널 링크 | `#vfilters #vgrid data-vlist="all"` |
| `notice.html` | 120 | 공지 · 게시판(BLOG) · 자료실(FILES) 탭 | `#tabs`, 주소 `#notice #blog #files`. **stories · areas 의 틀 원본** |
| `contact.html` | 142 | 연락 방법 4 · 견적 문의서(요청 사항 칸 포함) · FAQ 4 | 폼 id `cq*` (대문 폼은 `hq*`) |

공통: 머리(로고 · 메뉴 9: 회사소개 · 하는 일 · 현장 갤러리 · 영상 · 공지 · 블로그 · 행사 이야기 · 자동 견적 · 견적문의) · 폰 시트 메뉴 11 ·
바닥(CONTACT · COMPANY · `.ftl` 링크 6 · 「홈페이지 제작 큰길브리지」 www.ai-make.co.kr) · `.quick` · `.totop` ·
`<meta name="es-edit">` · `assets/app.js?v=20261004` · `assets/edit.js?v=1` · stats.js.

## 업무 화면 (생성 — `tools/port_docs.py`, 원본 큰길이벤트 레포)

| 파일 | 줄 | 검색 | 서버 |
|---|---|---|---|
| `quote.html` | 1994 | index,follow (손님용이라) | 문의 서버 · 계약 서버(저장함) |
| `quote-catalog.js` | 116 | — | 품목표 `CATALOG`(8묶음, 전부 `price:null`) + 견적 코드 읽기. quote · schedule 이 같이 씀 |
| `contract.html` | 1227 | noindex | 계약 서버 |
| `statement.html` | 504 | noindex | 없음 |
| `schedule.html` | 853 | noindex | 계약 서버 `sched*` |
| `upload.html` | 1263 | noindex | 갤러리 서버 |
| `office.html` | 160 | noindex | 계약 · 갤러리 서버 상태 확인 (port_docs `office()` + `admin_gate.apply()`) |
| `admin-lock.js` | 85 | — | 계약 서버 `boxList` |

## 공통 자원

| 파일 | 내용 |
|---|---|
| `assets/style.css` (782줄) | 전 공개 페이지 + stories · areas 공통. blog 는 안 씀 |
| `assets/app.js` (432줄) | 데이터 배열 + 모든 동작. 끝에 「관리자 모드」 바닥 링크 추가 IIFE |
| `assets/edit.js` (295줄) | 사장님 수정 모드 (es-company 것을 가져와 열쇠 · 이름만 바꿈) |
| `assets/img/logo-h.svg` · `logo-h-white.svg/.png` · `logo-mark.svg` · `favicon.svg` | 큰길브리지 제작 로고(마이크 + 소리 물결). white png 는 메일 머리용 |
| `assets/img/og.jpg` | 1200×630 공유 이미지(로고 + 문구 + works/w4) |
| `assets/img/mc-lee-studio.webp` · `mc-lee.webp` | 대표 MC 사진. studio 는 SOURCES.md 에 출처 없음(확인 필요) |
| `assets/img/works/w1~w28.webp` (+`th/`) | 현장 사진 1600px / 800px. 블로그 글 4편에서 |
| `assets/img/works/b1~b4.webp` (+`th/`) | 보육인대회 사진(긴 변 966px) — stories/childcare-conference 에만 |
| `assets/img/sig/*.webp` 9장 | 대표 MC 프로필 PDF 쪽에서 자른 대표 실적 사진 |
| `assets/img/SOURCES.md` | 사진 · 영상 · 로고 출처 |
| `assets/video/` | hero.mp4(1920×1080 H.264 23.2초 약 5.7MB) · hero_sm.mp4(960×540 약 1.7MB) · hero_sm.webm(VP9 960×540 약 1.5MB) · hero_poster.webp |
| `assets/files/healing-checklist.pdf` | 자료실 「행사 문의 준비표」 |

## 생성 페이지

| 폴더 | 생성기 | 원본 |
|---|---|---|
| `stories/` index + 5편 (jeonnong-festival · childcare-conference · union-workshop · elementary-sportsday · school-sports-daedong) | `python3 tools/make_pages.py` | 파일 안 `STORIES` |
| `areas/` index + 9 (nowon · dobong · gangbuk · jungnang · seongbuk · dongdaemun · uijeongbu · eunpyeong · namyangju) | 같은 명령 | 파일 안 `AREAS` · `SERVICES` |
| `blog/` index · 지역 모음 9 · 글 10 (`blog/<한글 slug>/index.html`) | `node scripts/build-blog.mjs` | `_blog/posts/*.json` |
| `rss.xml` · `sitemap.xml` · `llms.txt` 블로그 부분 | build-blog (sitemap 앞부분은 make_pages) | — |

## 원본 자료 · 도구

| 파일 | 내용 |
|---|---|
| `_blog/GUIDE.md` | 블로그 규칙서(HD기획 → 큰길 → 힐링). 글 쓰기 전에 반드시 |
| `_blog/regions.json` | 지역 9: slug · 이름 · 비중(합 1) · 이동 · 동네 · 많은행사 · 주의 · 현장기록 |
| `_blog/keywords.json` | 주제 14 + 지역전용 3, 성수기 달, 검색량(아직 비어 있음 → blog-plan 이 0.15 로 봄) |
| `_blog/photos.json` | 블로그에 써도 되는 사진 묶음 · 제외 · 지역(동대문 · 은평만) |
| `_blog/sources.json` | 사람이 확인한 공식 출처(확인일 2026-09-11) — 이 도메인은 여기 주소만 허용 |
| `scripts/build-blog.mjs` (425) · `blog-check.mjs` (258) · `blog-plan.mjs` (87) | Node 22 ESM, 의존성 없음 |
| `tools/make_pages.py` (232) | 행사 이야기 · 지역 페이지 · sitemap |
| `tools/port_docs.py` (520) | 업무 화면 옮기기. 맨 위 「회사 설정」 칸만 회사별 |
| `tools/admin_gate.py` (90) | office.html 잠금 화면 주입(바로기획 원본, 고객사 레포마다 같은 내용) |
| `tools/apply_edits.py` (123) | 사장님 수정 반영 |
| `apps-script/contract/` · `apps-script/gallery/` | Code.gs + 설치 README |
| `llms.txt` · `robots.txt` · `sitemap.xml`(44개 주소) · `.nojekyll` · `README.md`(업무 도구 표) | — |

## 원본 계보

- 처음 시안: `/home/user/haengsa-board/homepages/healing/` (지금 레포와 README 만 다름 — 시안 README 에 납품 전 확인 목록 · 프로필 PDF · 리틀리 반영 기록이 있다) + 공통 지침 `homepages/_tools/BRIEF.md`.
- 틀: es-company(수정 모드 · 폼 대체 동작) → 이 회사에 맞게 다시 설계.
- 업무 도구: 큰길이벤트기획(keungil-event) 원본 → 바로기획 기준본 → `port_docs.py` (README: 2026-10-03).
- 행사 이야기 · 지역 페이지: 바로기획 `tools/make_pages.py` 이식(2026-10-03). 블로그: HD기획 `_blog` 루틴 이식(2026-10-28).
