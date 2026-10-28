# 파일 지도 — 이벤트와 교육연구소 (c0c4773 기준)

표기: **[생성]** = 다른 파일이 만든 결과(손 수정 금지) · **[원본]** = 사람이 고치는 파일 · **[이식]** = 큰길이벤트 레포에서 port_docs.py 가 옮긴 결과.

## 루트

| 파일 | 줄 | 구분 | 하는 일 |
|---|---|---|---|
| `index.html` | 153 | [생성] build_site | 대문 |
| `about.html` | 97 | [생성] | 회사 소개 |
| `ceo.html` | 99 | [생성] | 대표 소개 |
| `event.html` | 101 | [생성] | 행사 5대상 |
| `education.html` | 81 | [생성] | 교육 6 |
| `portfolio.html` | 88 | [생성] | 사진 97장 · 실적 학교 · 후기 (한 줄이 길어 40KB) |
| `contact.html` | 84 | [생성] | 문의 폼 · FAQ |
| `notice.html` | 66 | [생성] | 공지 |
| `notice-admin.html` | 119 | [생성] | 공지 관리자(인라인 스크립트, noindex) |
| `404.html` | 52 | [생성] | 없는 페이지 |
| `sitemap.xml` · `robots.txt` · `llms.txt` | | [생성] build_site + (sitemap · llms 의 블로그 부분) build-blog | |
| `rss.xml` | | [생성] build-blog | 블로그 RSS |
| `quote.html` | 2027 | [이식] | 자동 견적서(손님 / `?admin=1` 발행) |
| `quote-catalog.js` | 114 | [이식] (CATALOG 는 port_docs.py 상수) | 견적 품목 35개 + 견적 코드 풀이 `견적풀기()` |
| `contract.html` | 1257 | [이식] | 전자계약서 |
| `statement.html` | 504 | [이식] | 거래명세서 |
| `schedule.html` | 897 | [이식] | 행사 일정 · 체크리스트 |
| `upload.html` | 1265 | [이식] | 사진 올리기 + 블로그 · 인스타 글 |
| `office.html` | 160 | [생성] port_docs `office()` + admin_gate | 대표 전용 업무 문서함(noindex, 공개 링크는 바닥글 「관리자 모드」) |
| `admin-lock.js` | 85 | [이식] | `?admin=1` 화면 잠금(계약 서버 `boxList`) |
| `README.md` | | [원본] | 납품 기록 · 고치는 법 · 확인할 것 · 오픈 체크리스트 · 계약 항목 점검표 |

없는 것: `CNAME` · `.nojekyll` · `.github/` · `favicon.svg`(업무 화면이 참조) · `stamp-edu.png` · `stories/`(quote 메뉴가 참조) · `apps-script/*/README.md`(Code.gs 가 참조) · `.claude/launch.json`(README 가 언급, 레포 밖).

## tools/

| 파일 | 줄 | 하는 일 |
|---|---|---|
| `build_site.py` | 776 | ★ 공개 페이지 · sitemap · robots · llms 생성 (`references/content.md`). Python 3.12+ |
| `blog_shell.py` | 36 | build_site 를 import 해 `{base, basePath, noindex, ver, name, nameEn, tel, email, nblog, ogImage, header, footer, cta}` JSON 출력. 상대 주소 앞에 `@@R@@` 표시(블로그가 `../` 로 바꿈) |
| `port_docs.py` | 588 | 업무 도구 이식기. 「회사 설정」(ID `edu` · 이름 · 주소 · TEL · EMAIL · REPO · HOME · CODE_PRE `EE-` · CONTRACT_URL · GALLERY_URL · LOGO_FILE · MAIL_LOGO · STAMP · COLORS · OFFICE · EXAMPLES · QUOTE_TITLE/DESC · CATALOG · UPLOAD_CATS · UPLOAD_REGIONS · UPLOAD_PAIRS · NAV_SITE). 끝에 남은 큰길 흔적(TRACES)을 파일마다 출력. 원본 경로 기본 `~/Documents/클로드코드` |
| `admin_gate.py` | 90 | office.html 에 `<!--GATE-->…<!--/GATE-->` 잠금 화면(CSS · 폼 · 스크립트) 씌움 · 여러 번 돌려도 한 번만. 「바로기획 tools/admin_gate.py 가 원본」이라고 주석 |
| `apply_edits.py` | 118 | 수정 모드 JSON(파일 또는 메일 본문)을 8개 페이지(index · about · ceo · event · education · portfolio · contact · notice)에 반영, 사진은 `assets/img/` 아래만 허용 · PIL 로 1920px 이하 재저장 |

## scripts/ · _blog/ · blog/

| 파일 | 하는 일 |
|---|---|
| `scripts/build-blog.mjs` (279) | `_blog/posts` → `blog/`(지우고 새로) · rss.xml · sitemap/llms 블로그 부분. `python tools/blog_shell.py` 를 부름 |
| `scripts/blog-check.mjs` (240) | 글 검사(실패 시 exit 1). `--new 파일` |
| `scripts/blog-plan.mjs` (11) | keywords.json 중 안 쓴 주제 출력 |
| `_blog/GUIDE.md` | 쓰는 규칙(사람도 이걸 먼저 고침) |
| `_blog/company.json` | 쓸 수 있는 회사 사실 17문장 · 허용숫자 · 약속키워드 |
| `_blog/keywords.json` | 주제 10개(topic · category · k · s) |
| `_blog/photos.json` | 블로그용 사진 11장(g01~g10 · story-2011, g09 제외) + 보이는것 |
| `_blog/sources.json` | 공식 출처 3개(기상청 특보 기준 · 소비자원 에어바운스 · 정책브리핑 유원시설) |
| `_blog/posts/*.json` | 글 10편(2026-10-21) |
| `blog/` | [생성] index · event/ · edu/ · 글 10개 폴더 |

## assets/

| 파일 | 구분 | 내용 |
|---|---|---|
| `style.css` (425) | [원본] | 공통 스타일. 맨 위 `@import` Pretendard · Jua |
| `blog.css` (63) | [원본] | 블로그 전용(`.bl-*`) |
| `app.js` (199) | [원본] | 공통 스크립트 10기능 |
| `edit.js` (295) | [원본] | 사장님 수정 모드(자체 SHA-256 구현) |
| `data/schools.json` | [원본] | 실적 학교 4지역 94곳 |
| `data/notices.json` | [원본] | 정적 공지 3개 |

### assets/img/ (약 15MB)

| 파일 | 크기 | 쓰임 |
|---|---|---|
| `logo-h.png` | 1400×207 | 머리글 · 바닥글(흰 알약 위) 가로 로고(웃는 얼굴 마크 + 글자) |
| `logo-h-white.png` | 1400×207 | 메일 머리(어두운 바탕) — port_docs `MAIL_LOGO` |
| `logo-arch.png` | 1100×841 | 아치형 로고 — JSON-LD `logo` |
| `logo-mark.png` | 512×469 | 웃는 얼굴 마크 — 사진 자리표시 |
| `favicon.png` | 256×256 | 파비콘 · apple-touch-icon · 업무 화면 머리 마크 |
| `og.jpg` | 1200×630 | 공유 이미지 |
| `hero-event.webp` · `hero-edu.webp` | 1280×721 | 히어로 좌 · 우 |
| `ceo.webp` | 496×870 | 소장 사진(아치 안, `mix-blend-mode:multiply`) |
| `g01~g10.webp` | 900~1200px | 기존 시안 사진 |
| `p/<접두어>NN.webp` | 긴 변 655~1400px | 2026-10-25 대표님 사진 87장: school 29 · church 23 · sci 12 · magic 8 · univ 6 · gov 5 · corp 4 |
| `story-2011.webp` | 884×622 | 2011 위즈 한마음 체육대회(ceo · 블로그) |
| `review-kakao.webp` | 900×740 | 카톡 후기 캡처(포트폴리오) |

### assets/video/ (약 15MB)
`sci-v1~5.mp4` + `.jpg` · `magic-v1.mp4` + `.jpg` (`references/content.md` 5장).

## apps-script/

| 파일 | 줄 | 내용 |
|---|---|---|
| `contract/Code.gs` | 537 | [이식] 계약 · 저장함 · 일정 서버 (`references/backend.md`) |
| `gallery/Code.gs` | 484 | [이식] 사진 업로드 서버 + port_docs 가 덧붙인 공지 기능(7장) |

## 원본 계보
- 디자인 · 구조: 콘텐츠 기획안(docx, 레포 밖)의 구조 · 문구를 옮김(README). 기존 시안(`index.html` 한 장, 사진 g01~g10 · 학교 목록 · 후기 · 대표 번호 · 메일)의 자료를 이어받음.
- 업무 도구: 큰길이벤트기획 레포 → `port_docs.py`.
- 블로그: HD기획 `_blog` · `build-blog.mjs` · `blog-check.mjs` 를 주제 글 중심으로 옮김.
- 수정 모드 · photos 고아 가지: 「es-company 방식」(README) — es-company 레포는 이 분석에서 보지 않음.
- 관리자 잠금: 바로기획 `admin_gate.py` 가 원본(주석).
