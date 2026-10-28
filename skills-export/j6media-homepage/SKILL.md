---
name: j6media-homepage
description: 제이식스미디어(J6 MEDIA, 남양주 별내 음향·조명 렌탈·설치 회사) 홈페이지(brizymedia/j6media, www.j6media.co.kr)를 고치거나 처음부터 다시 만들 때 쓴다. 「제이식스」「J6」「j6media」「김호진 대표 사이트」「음향 회사 홈페이지」, 견적서·전자계약·거래명세서·행사 일정·사진 올리기·행사 이야기·지역 페이지·사장님 수정 모드·히어로 영상 이야기가 나오면 이 스킬을 먼저 읽는다.
---

# 제이식스미디어(J6 MEDIA) 홈페이지

큰길브리지(주식회사 브리지미디어)가 만들어 납품한 고객 홈페이지다.
빌드 도구 없는 **순수 정적 사이트**(HTML + CSS 한 장 + JS 두 장)에, 큰길이벤트기획에서 옮겨 온
**업무 화면 5종**(견적·계약·명세서·일정·사진 올리기)과 **Google Apps Script 서버 2개**가 붙어 있다.

> 이 문서는 2026-10-28 에 레포 `main`(커밋 `8708190`, 커밋 1개뿐) 을 읽고 썼다.
> 코드에서 확인한 것만 적었고, 확인하지 못한 것은 **「확인 필요」** 라고 표시했다.
> 코드 사본은 넣지 않았다. 작업 전에 레포를 내려받는다:
> `git clone https://github.com/brizymedia/j6media.git`

세부 자료는 `references/` 에 있다.

| 파일 | 내용 |
|---|---|
| `references/file-map.md` | 모든 파일이 하는 일, 크기, 누가 만드는지(손 · 생성기 · 이식기) |
| `references/design-tokens.md` | CSS 변수 전부, 글꼴, 간격, 반응형 기준, 컴포넌트 클래스 사전 |
| `references/sections.md` | 대문 · 서브 페이지 · 생성 페이지의 섹션 순서와 문구 위치 |
| `references/workflows.md` | 공지 · 사진 · 블로그 · 이야기 · 지역 · 견적→계약→명세서 · 사장님 수정 반영 절차와 명령 |
| `references/backend.md` | Apps Script 두 서버의 액션 · 필드 · 스크립트 속성 · 배포 규칙 |

---

## 1. 회사 정보 (사이트에 공개된 것만)

| 항목 | 값 | 코드 위치 |
|---|---|---|
| 상호 | 제이식스미디어 (J6 MEDIA) — 별칭 J6미디어 | `index.html` JSON-LD `alternateName` |
| 대표 | 김호진 | 바닥글 · `about.html` |
| 업종 | 예배 · 공연 · 행사 음향 · 조명 렌탈과 현장 운영, 음향 · 영상 · 방송장비 제안 · 설치 | `llms.txt` |
| 사업자등록번호 | 485-01-02512 | 바닥글 · `about.html#info` |
| 주소 | 경기도 남양주시 순화궁로 282 에이스하이엔드타워별내 319호 | 바닥글 · JSON-LD (좌표 37.6524324, 127.1293090) |
| 이메일 | j6_media@naver.com | 바닥글 · 문의 수신 |
| 전화 · 문자 | 대표 휴대폰(사이트 모든 페이지에 공개돼 있으나 이 문서엔 적지 않음) | `assets/app.js` 의 `SMS_TO`, `tools/make_pages.py` 의 `TEL` |
| 영업 | 월~토 09:00~18:00, 일요일 휴무 | 바닥글 · JSON-LD `openingHoursSpecification` |
| 채널 | 인스타그램 `j6_media`, 네이버 블로그 `martin301`, 네이버 플레이스 `1026343689`, 페이스북 Hojin Kim(링크 없음) | 바닥글 `.sns` · `about.html` |
| 슬로건 | 「2005년부터 2026년까지, 계속 이어온 음향의 길.」 / 「안정적으로, 멋지게, 예술적으로」 | 대문 히어로 |
| 대표 연혁 | 2001–04 선한소리음향선교회 → 2005–06 ㈜웨이오디오 → 2007–18 나들목교회 → 2019–21 사운드피플컴퍼니 → 2022– 제이식스미디어 | 대문 `#history` · `about.html#history` (두 곳에 같은 목록) |
| 하는 일 6분야 | 교회행사 · 기업행사 · 지자체 행사 · 학교행사 · 전시 · 공연 · 음향 · 영상 · 방송장비 설치 | `service.html` 앵커 `#church #corp #gov #school #show #install` |
| 취급 브랜드 14 | LSS · NEXO · SA · QANON · GALLO · YAMAHA · BEHRINGER · MIDAS · A&H · BELDEN · NEUTRIK · KANALS · SHURE · SENNHEISER | 대문 마퀴 · `equipment.html#brands` |

**쓰지 말 것**: 계좌번호(이식기가 일부러 지움), 서버 암호, GitHub 토큰, `meta[name=es-edit]` 의 해시값, 개인 휴대폰을 새 문서에 옮겨 적기.

## 2. 레포 · 도메인 · 배포

- 레포: `brizymedia/j6media`, 가지 `main`(사이트) + `photos`(사진 올리기 결과, 서버가 씀).
  이 클론에는 `photos` 가지가 없었다 — 원격에 있는지 **확인 필요**.
- 배포: **GitHub Pages, `main` 루트 그대로**. `.nojekyll` 있음, `.github/workflows` **없음**(빌드 없음).
  push 하면 끝.
- 도메인: `CNAME` = `www.j6media.co.kr`. 그런데 **canonical · og:url · JSON-LD · sitemap · robots · llms.txt ·
  `make_pages.py` BASE · `port_docs.py` HOME · upload.html `홈주소` 는 전부 `https://brizymedia.github.io/j6media/`**.
  `robots.txt` 머리 주석도 "도메인이 정해지면 Sitemap 주소를 바꿀 것"이라고 한다.
  → 새 도메인이 실제로 연결됐는지 **확인 필요**. 연결됐다면 위 전부를 한 번에 바꿔야 한다(§10 함정 1).
- 유입 통계: 모든 페이지 `<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="j6">` (큰길브리지 유입 서버).
- 검색 차단: `robots.txt` 가 `contract · statement · upload · schedule · office` 를 Disallow, 그 다섯은 `noindex,nofollow` 메타도 있다.
  `quote.html` 은 일부러 index (손님용과 관리자용 주소가 같아서).

## 3. 파일 지도 (요약 — 전체는 `references/file-map.md`)

```
index.html                대문 (히어로 영상 · 하는 일 6 · 강점 · 실적 탭 · 연혁 · 사진 · 공지/오시는길/상담 · CTA)
about.html service.html equipment.html portfolio.html notice.html contact.html   서브 6쪽 (손으로 씀)
assets/style.css          공통 스타일 한 장 (?v=6)
assets/app.js             공통 스크립트 + 데이터(NOTICES · FILES · WORKS · BLOG) (?v=20261004)
assets/edit.js            사장님 수정 모드 (?edit=열쇠)
assets/img/               로고 · og.jpg · works/wN.webp(1600) tN.webp(800) · brands/*.png · SOURCES.md
assets/video/             hero.mp4(1920×1080) hero_sm.mp4 · hero_sm.webm(960×540) hero_poster.webp
stories/  areas/          생성 페이지 — tools/make_pages.py 가 만든다 (손으로 고치지 말 것)
quote.html quote-catalog.js contract.html statement.html schedule.html upload.html admin-lock.js office.html
                          업무 화면 — tools/port_docs.py 가 큰길이벤트 원본에서 옮긴다 (손으로 고치지 말 것)
apps-script/contract/     계약 · 견적저장함 · 일정 서버 (Code.gs + README)
apps-script/gallery/      사진 업로드 서버 (Code.gs + README)
tools/make_pages.py       이야기 · 지역 페이지 + sitemap.xml 생성
tools/port_docs.py        업무 화면 이식기
tools/admin_gate.py       office.html 잠금 화면 씌우기 (port_docs 가 부름)
tools/apply_edits.py      사장님 수정 요청 JSON 반영기
llms.txt sitemap.xml robots.txt CNAME .nojekyll
```

**누가 만드는 파일인지가 가장 중요하다.** 손으로 고치는 것은 서브 6쪽 · 대문 · style.css · app.js · edit.js 뿐이다.

## 4. 디자인 체계 (요약 — 전체는 `references/design-tokens.md`)

분위기: "따뜻 · 친근. 밝은 아이보리 바탕 + 앰버(무대 조명) + 웜 차콜(밤 무대)" (style.css 머리 주석).

| 토큰 | hex | 쓰임 |
|---|---|---|
| `--bg` | `#FBF6EE` | 기본 바탕(아이보리) |
| `--bg2` | `#F5ECDF` | `.sec.sand` 띠 |
| `--paper` | `#FFFFFF` | 카드 |
| `--ink` / `--ink2` / `--mute` | `#2B211B` / `#5A4A3E` / `#86766A` | 글자 3단 |
| `--line` | `#EADFCF` | 선 |
| `--amb` / `--amb-d` | `#E58A2B` / `#B45F12` | 주 강조 / 진한 강조(글자용) |
| `--glow` / `--cream` | `#FFC870` / `#FFF4E2` | 어두운 바탕 위 강조 / 밝은 글자 |
| `--night` / `--night2` | `#221913` / `#33271E` | 밤 무대 섹션 · 바닥글 · 업무 화면 바탕 |

- 글꼴(구글 폰트 한 줄): 본문 **Noto Sans KR** 400–700 (`--kr`), 제목 **Gowun Batang** 700 (`--kr-h`),
  영문 장식 **Fraunces** 이탤릭 600/700 (`--en`). 업무 화면 5종은 따로 **Pretendard**(jsDelivr) + iconify-icon.
- 모서리 `--r: 20px`, `--r-s: 12px`, 단추 999px. 그림자 `--shadow: 0 18px 40px -22px rgba(74,44,16,.35)`.
- 폭 `--wrap: 1200px`, `.wrap { width: min(1200px, 100% - 40px) }` (640 이하 `100% - 32px`).
- 섹션 위아래 `clamp(72px, 10vw, 120px)`. 제목 `.h2` `clamp(28px, 4.2vw, 44px)` 고운바탕, `em` 은 앰버 + 형광펜 밑줄.
- 반응형 기준 **1080 / 860 / 640px** (+ 이야기·지역 전용 960 / 600). 1080 이하 햄버거, 640 이하 폰 하단 고정 단추 `.quick`.
- `body { word-break: keep-all }` — 한글 낱자 떨어짐 방지. 빼지 말 것.
- `prefers-reduced-motion` 이면 모든 애니메이션 끔 + 히어로 영상 대신 포스터.

핵심 컴포넌트: `.hd`(고정 머리, 대문에서는 `.on-dark` 로 흰 글씨→스크롤 40px 넘으면 `.solid`), `.sheet`(모바일 전체 메뉴),
`.hero`, `.phead`(서브 페이지 어두운 머리 + 사진 + `.crumb`), `.marquee`, `.sec-head`, `.btn-amb/-ink/-line/-ghost/-w`,
`.reveal`(스크롤 등장), `.works6`(목록 hover → 왼쪽 사진 교체), `.rtabs/.rpane`(실적 탭), `.tl`(연혁 5칸→세로),
`.gal`(사진 격자 + `.lb` 라이트박스), `.trio3/.box`, `.ctaband`, `.ft`, `.quick`, `.totop`, `.progress`.

## 5. 페이지별 구성 (요약 — 순서와 문구 위치는 `references/sections.md`)

- **대문** `index.html`: 히어로(영상) → 브랜드 마퀴 → 소개(단어 점등 문장 `#litQuote` + 콜라주) → `#service` 하는 일 6(sand)
  → Why J6 강점 2(night) → `#record` 실적 탭 6 → `#history` 연혁(sand) → `#gallery` 사진 8장(`data-pick="41,36,57,44,45,47,48,50"`)
  → 공지 · 오시는 길 · 바로 상담(sand) → CTA 띠.
- **서브 6쪽**: 모두 `.phead`(배경 사진 + eyebrow + h1 + 설명 + 이동경로) → 본문 → 같은 CTA 띠 → 같은 바닥글.
  about(인사말·연혁·회사정보 표·지도카드) / service(6분야 지그재그 + 설치 사례 15곳) / equipment(음향 8 · 조명 5 · 브랜드 로고 14) /
  portfolio(필터 8 + 사진 격자 + 블로그 목록) / notice(탭 3: 공지 · 게시판 · 자료실) / contact(연락 방법 + 문의 폼 + FAQ 6).
- **행사 이야기 5편 + 목록**, **지역 9곳 + 목록**: `make_pages.py` 표에서 생성.
- **업무 화면**: 어두운 웜차콜 바탕의 별도 디자인(Pretendard, glass 카드). 사이트 공통 CSS 를 쓰지 않는다.

## 6. 공통 스크립트 기능 (`assets/app.js`)

파일 맨 위가 **데이터 칸**이다. 대부분의 내용 수정은 여기서 끝난다.

| 상수 | 하는 일 |
|---|---|
| `FORM_ENDPOINT` | 문의 서버(큰길브리지 공용 Apps Script) 주소. 문의 폼 · 수정 모드 · 견적 문의가 같이 쓴다 |
| `NOTICES` | 공지 `{d, t, b, n:NEW, top:고정}` → 대문 `#noticeList`(4개) · `notice.html#noticeBoard` |
| `FILES` | 자료실 `{d, t, k:LINK/PAGE/FILE, u}` → `#fileBoard` |
| `WORKS` | 현장 사진 57장 `{i:번호, t:제목, o:분야·지역·연도, c:'church corp gov school show install gear' 중 공백 구분}` |
| `UP_LIST` `UP_IMG` `UP_CAT` | `photos` 가지의 `photos/photos.json` 과 jsDelivr 사진 주소 — 현장 사진 페이지에서 WORKS 앞에 붙임 |
| `BLOG` | 네이버 블로그 글 42개 `{d, t, u}` (새 글은 맨 앞) → `#blogList` |

기능: 스크롤 시 머리 `.solid` · 진행 막대 · 맨 위로 / 현재 페이지 메뉴 `.act` / 햄버거 시트(Esc 닫기) /
히어로 영상 소스 고르기(mp4 못 틀면 webm, 폭 900 미만 `_sm`, 움직임 줄이기면 안 틂, 정지·재생 단추 `#vbtn`) /
마퀴 글자 두 번 이어 붙이기 / `.reveal` 등장 / `#litQuote` 단어 점등 / `#wlist` hover·focus → `#wstage` 사진 교체 /
`[data-tabs]` 공용 탭(`#btabs` 는 주소 `#notice #board #files` 와 연동) / 갤러리 · 필터 · 개수 표시 · 라이트박스(←→ Esc 스와이프) /
공지 · 자료실 · 블로그 목록(더 보기) / 문의 폼 전송(`#k=교회` 해시로 분야 미리 체크, 스팸 함정 `website`, 동의 필수,
서버가 `{ok:true}` 를 안 주면 폰은 문자 앱, PC 는 클립보드 복사) / 바닥글 끝에 「관리자 모드」 작은 링크 → `office.html` 자동 추가.

## 7. 업무 화면 (흐름과 상태 저장 — 상세는 `references/workflows.md`, `references/backend.md`)

**원칙: 견적서에는 서버가 없다.** 견적 하나 = 주소 뒤 `#q=` 에 담긴 base64url 코드. 화면 간 이동도 해시로 넘긴다.

```
quote.html (손님)            ─ 문의 보내기 → 문의 서버 → 대표 메일 (실패 시 FormSubmit 예비 경로)
quote.html?admin=1 (대표)    ─ 견적 작성 · 인쇄 · 메일 · 링크(#q=) · 견적서 저장함
   ├ 「계약서 작성」  → contract.html?admin=1#c=…   → 고객 서명 링크 contract.html?c=ID&s=… → PDF · 메일 · 대장
   ├ 「거래명세서」   → statement.html?admin=1#t=…  → 인쇄 · PDF
   └ 「일정으로」     → schedule.html#new=…         → 행사 카드 + 체크리스트 (직원과 공유)
upload.html                  ─ 사진 → 갤러리 서버 → photos 가지 → portfolio.html 에 자동 표시 + 블로그 · 인스타 글 초안
office.html                  ─ 대표 전용 도구 모음 · 서버 연결 상태 · 암호 안내 (대표 암호 잠금)
```

- 손님 화면(`admin=1` 없음): 직인 · 품목명 · 규격 · 단가 · 할인 · 인쇄를 막는다(`손님가리기()`). 단가는 전부 `price:null`(협의) — 가격표 없음.
- 관리자 화면(`?admin=1`)은 `admin-lock.js` 가 가린다: 계약 서버에 `{action:'boxList', pw}` 를 보내 ok 면 열고 localStorage 에 기억.
- 기기 저장 키: `j6-quote-box-pw`(대표 암호) · `j6-quote-box-v1`(저장함 목록) · `j6-sched-pw` · `j6-sched-who` ·
  `kg_contract_co`(계약 회사정보+서버주소) · `kg_stmt_bank`(명세서 계좌) · `j6_srv j6_pw j6_cat j6_ev`(사진 올리기).
  `kg_` 두 개는 이식 때 안 바뀐 큰길 이름이다(동작엔 지장 없음, 같은 브라우저에서 큰길 사이트와 섞일 수 있음 — 확인 필요).
- 계약 번호 · 명세서 번호 앞글자 `J6-YYYYMMDD-XXX`. 계약 종류 2가지: 행사 용역(우리가 을) / 출연(우리가 갑, 개인 3.3% · 사업자 부가세 10%).
- 직인 파일 `assets/img/stamp-j6.png` 는 **아직 없다** → 계약서 · 명세서에 「(인)」 자리만 나온다(가짜 도장 금지).

## 8. Apps Script 서버 (주소만 — 비밀값은 스크립트 속성에만)

| 서버 | 주소 (`/exec`) | 스크립트 속성 | 쓰는 화면 |
|---|---|---|---|
| 문의 서버 (큰길브리지 공용, **코드가 이 레포에 없음**) | `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec` | 확인 필요 | contact 폼 · quote 문의 · edit.js 수정 요청 |
| 계약 서버 `apps-script/contract` | `https://script.google.com/macros/s/AKfycbxO7crgcZh7SSPAgwbPctHL-ZGF9LVj9O1yZuIbqyVta0PkzKJCsFOoGcThtWXPJyretw/exec` | `BOX_PW`(대표) · `CREW_PW`(직원) | contract · quote 저장함 · schedule · admin-lock · office 잠금 |
| 갤러리 서버 `apps-script/gallery` | `https://script.google.com/macros/s/AKfycbz1JKFYh-cUS-GmPCEB26U4rJ-IWmLVFlncxKE4pKO843W1bY-NAnU5rmxupGCXAAisIw/exec` | `UPLOAD_PW` · `GITHUB_TOKEN` · `GITHUB_REPO` | upload |

배포 규칙(두 README 공통): 웹 앱 · **실행: 나 · 액세스: 모든 사용자**. 코드를 고치면 **배포 관리 → 연필 → 새 버전**(새 배포를 만들면 주소가 바뀜).
계약 서버는 `VERSION` 상수를 올리고 `…/exec` GET 으로 `version · box · sched` 를 확인한다.
주소가 바뀌면 `tools/port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL` 을 고치고 이식기를 다시 돌린다(화면 5종 + office 에 박힘).
액션 · 필드 전체는 `references/backend.md`.

## 9. 생성기 · 자동화 (명령은 레포 루트에서)

| 명령 | 하는 일 | 고칠 곳 |
|---|---|---|
| `python tools/make_pages.py` | `stories/` 6쪽(목록+5) · `areas/` 10쪽(목록+9) 생성 + **`sitemap.xml` 통째로 다시 씀**(lastmod=오늘) | 파일 안 `STORIES` · `AREAS` · `SERVICES` 표 |
| `python tools/port_docs.py [큰길이벤트 레포 경로]` | 견적 · 계약 · 명세서 · 일정 · 사진 올리기 · admin-lock · 서버 코드 2개 · office.html 을 큰길이벤트 원본에서 다시 옮김. 끝에 "남은 큰길 흔적" 출력 | 「회사 설정」 칸(ID · 이름 · 색 · 예시 문구 · `CATALOG` · 사진 칸 · 지역표 · 서버 주소) |
| `python tools/apply_edits.py 수정파일.json` (또는 메일 본문 .txt) | 사장님 수정 요청 반영 — 원문 innerHTML 을 찾아 바꾸고 사진을 같은 이름으로 덮어씀. 못 찾으면 「수동 확인」 | — (대상 페이지는 `PAGES` 7개뿐) |

- `make_pages.py` 는 머리글 · 바닥글을 **`notice.html` 에서 잘라 온다**(`<section class="phead">` 앞 / `</main>` 뒤).
  notice.html 머리 · 바닥을 바꾸면 이 스크립트를 다시 돌려야 16쪽이 따라온다. 생성 페이지에서는 `es-edit` 메타와 `edit.js` 를 뺀다.
  하위 폴더 깊이에 맞춰 상대 주소에 `../` 를 자동으로 붙인다.
- `port_docs.py` 기본 원본 경로는 `~/Documents/클로드코드`(큰길이벤트 레포). 원본이 없으면 돌릴 수 없다.
- 블로그 글 자동 수집 · 사진 목록 자동 생성 스크립트는 **없다**. `BLOG` · `WORKS` · `SOURCES.md` 는 손으로 고친다.
- 사진 업로드 서버가 보내는 `repository_dispatch(photos-updated)` 와 README 의 "6시간마다 자동 작업"·`gallery.html`·
  `scripts/prepare-gallery-photos.mjs` 는 **큰길이벤트 쪽 이야기**다. 이 레포엔 워크플로도 그 파일도 없다.
  여기서는 `portfolio.html` 이 `photos.json` 을 직접 읽으므로 신호가 없어도 된다.

## 10. 사장님 수정 모드 (`assets/edit.js`)

1. 큰길브리지가 대표에게 `사이트주소/?edit=열쇠` 를 문자로 보낸다. 열쇠의 SHA-256 이 각 페이지 `<meta name="es-edit">` 와 같아야 켜진다
   (`index · about · service · equipment · portfolio · notice · contact` 7쪽에만 있음). 열쇠는 sessionStorage `j6-edit-key`, `?edit=off` 로 끔.
2. 글자 칸(leaf 요소)이 `contenteditable` 이 되고, `main` 안 사진(img · background-image)을 누르면 파일을 골라 바꾼다(1920px JPEG 0.86 로 줄임).
   자동 생성 목록(`#gal #pfGrid #blogList #noticeList #noticeBoard #fileBoard #litQuote .marquee` · 폼 등)은 제외 → 그건 app.js 데이터로 고친다.
3. 고친 것은 IndexedDB `j6-edit` 에 페이지별로 보관(여러 페이지 오가도 유지).
4. 「수정 내용 보내기」: 글 수정은 문의 서버로 메일(본문 끝에 JSON), 사진이 있으면 `제이식스미디어-수정요청-YYYYMMDDHHMM.json` 파일을 공유/내려받기.
5. 큰길브리지가 `python tools/apply_edits.py 파일` → `git diff` 확인 → push. 사진은 `assets/img/` 아래만 허용, 1920px 로 줄여 원래 확장자로 저장(PIL 필요).

**주의**: 수정 모드는 `cssPath` 선택자와 **원문 innerHTML** 로 위치를 찾는다. 대표가 고치는 사이에 같은 문장을 손으로 바꾸면 「수동 확인」이 뜬다.

## 11. 히어로 영상 만드는 법

현재 영상(`assets/img/SOURCES.md` 기록): 대표 원본 사진 **w41 · w36 · w39 · w45 · w47 · w42 · w57** 7장,
사진마다 **3.8초 좌우 흐름 + 0.8초 교차 전환**, 2026-09-27 교체. 실측: 길이 21.8초(=7×3.8−6×0.8), 30fps,
`hero.mp4` H.264 1920×1080 약 2.6Mbps(7.0MB) · `hero_sm.mp4` H.264 960×540(2.4MB) · `hero_sm.webm` VP9 960×540(2.9MB) · `hero_poster.webp` 1920×1080.

만든 스크립트는 레포에 **없다**. 같은 규격으로 다시 만들려면 ffmpeg 로(예시 — 실제 쓰인 명령은 확인 필요):

```bash
# 사진마다 4.6초짜리 좌우 흐름 클립 → xfade 0.8초로 이어 붙이기 (offset = 3.8 × n)
ffmpeg -loop 1 -t 4.6 -i assets/img/works/w41.webp -vf "scale=2304:-2,crop=1920:1080:'(iw-1920)*t/4.6':'(ih-1080)/2',fps=30,format=yuv420p" c1.mp4
# … c2~c7 같은 방식, 그다음
ffmpeg -i c1.mp4 -i c2.mp4 … -filter_complex "[0][1]xfade=transition=fade:duration=0.8:offset=3.8[a];[a][2]xfade=…:offset=7.6[b];…" -an -movflags +faststart -crf 26 assets/video/hero.mp4
ffmpeg -i assets/video/hero.mp4 -vf scale=960:-2 -an -movflags +faststart -crf 28 assets/video/hero_sm.mp4
ffmpeg -i assets/video/hero.mp4 -vf scale=960:-2 -an -c:v libvpx-vp9 -b:v 0 -crf 36 assets/video/hero_sm.webm
ffmpeg -i assets/video/hero.mp4 -frames:v 1 assets/video/hero_poster.webp
```

소리는 없다(`muted` 자동재생). 파일 이름을 바꾸면 `index.html` 의 `data-src / data-src-sm / data-src-webm / poster` 와 `<link rel=preload>` 를 같이 바꾼다.

## 12. 사진 출처 규칙

- 현장 사진은 **전부 대표 소유**: w1~w30 은 대표 네이버 블로그(martin301) 글 사진, w31~w57 은 대표가 보낸 원본 폴더(파일 이름 가나다순 번호).
  출처 표는 `assets/img/SOURCES.md` — **새 사진을 넣으면 여기에 줄을 추가**한다.
- 규격: `works/wN.webp` 1600px(긴 변) + `works/tN.webp` 800px 썸네일. 번호는 이어서 붙인다(다음은 w58).
- 브랜드 로고: 각 회사 공식 사이트 또는 위키미디어 공용에서 받아 `#2B211B` 단색 투명 PNG 로 맞춤. KANALS 는 공식 로고를 못 찾아 글자로 둠.
  `equipment.html` 에 "각 로고는 해당 회사의 상표" 고지가 있다 — 지우지 말 것.
- 스톡 · AI 생성 사진은 쓰지 않았다. 사진 문구는 블로그 원문 · 대표 확인분 사실만(`make_pages.py` 머리 주석).
- upload.html 로 올린 사진은 `photos` 가지에 워터마크(「제이식스미디어」) 찍힌 1600px 사본만 올라간다.

## 13. 검증 절차 (레포에 자동 검증 스크립트는 없음)

```bash
cd j6media
python -m http.server 8000            # 루트에서 띄워야 상대 주소가 맞는다 (file:// 로 열면 fetch 가 막힘)
node --check assets/app.js && node --check assets/edit.js && node --check admin-lock.js && node --check quote-catalog.js
python -m py_compile tools/*.py
```

1. 브라우저 **375px**(폰)과 **1280px**(PC)에서 대문 · 서브 6쪽 · 이야기 1쪽 · 지역 1쪽을 연다.
   - 가로 스크롤이 생기지 않는지, 375 에서 하단 `.quick` 단추가 바닥글을 덮지 않는지(바닥글 `padding-bottom:120px`).
   - 1080 이하 햄버거 → 시트 열림/닫힘, 860 이하 `.works6` 사진판 숨고 썸네일 표시.
2. **콘솔 오류 0** 확인(특히 `app.js` 는 `#gal`·`#pfGrid` 등이 없는 페이지에서도 안 깨져야 한다).
3. 대문: 영상 재생 · 정지 단추 · 단어 점등 · 실적 탭 · 사진 라이트박스.
   portfolio: 필터 개수 표시, `photos.json` 을 못 읽어도 WORKS 만으로 나와야 함.
4. contact 폼: 성함 · 연락처 · 동의 없으면 막히는지. 실제 전송은 대표 메일로 가니 시험 전송 땐 미리 알릴 것.
5. 업무 화면은 `?admin=1` 잠금 화면이 뜨는지, 손님 `quote.html` 에서 단가 · 인쇄가 숨는지.
6. 서버를 건드렸으면 `…/exec` 를 브라우저로 열어 `ok:true` · `box:"ready"` · `sched:"ready"`(계약), `설정완료` 전부 true(갤러리).
7. 고친 CSS/JS 는 캐시 꼬리표를 올린다: `style.css?v=6`, `app.js?v=20261004`, `edit.js?v=1` — **모든 HTML 에서 같이**(§14-2).

## 14. 반복되는 함정 · 고칠 때 같이 고칠 곳

1. **도메인 이중**: CNAME 은 `www.j6media.co.kr`, 나머지는 github.io 주소. 바꿀 때 같이 고칠 곳 —
   모든 HTML 의 canonical · og:url · og:image · JSON-LD(`@id`, url, logo, image, BreadcrumbList),
   `sitemap.xml`(→ `make_pages.py` 의 `BASE` 와 `sitemap()` 이 다시 쓰므로 거기서), `robots.txt` Sitemap, `llms.txt` 링크,
   `port_docs.py` 의 `HOME` · `MAIL_LOGO`, upload.html `홈주소`(이식기 결과), README.
2. **캐시 꼬리표**: `?v=` 는 페이지마다 하드코딩. `grep -rn "style.css?v=" --include=*.html` 로 전부 바꾼다(생성 페이지는 notice.html 을 고친 뒤 `make_pages.py`).
3. **머리글 · 바닥글 · CTA 띠는 손으로 쓴 7벌**(대문 + 서브 6쪽)이고, 생성 16쪽은 `notice.html` 것을 잘라 쓴다. 메뉴 · 연락처 · 바닥글을 바꾸면
   대문 + 서브 6쪽을 모두 고치고 `make_pages.py` 를 다시 돌린다. 업무 화면 메뉴는 `port_docs.py` 의 `NAV_SITE` 로.
4. **연혁 · 하는 일 · 설치 사례가 여러 곳에 중복**: 연혁은 대문 `#history` + `about.html#history` + `llms.txt`,
   하는 일 목록은 대문 `#service`·`#record` + `service.html` + `llms.txt` + JSON-LD `hasOfferCatalog` + `make_pages.py SERVICES` + `quote-catalog.js`.
5. **생성 · 이식 결과물을 손으로 고치지 말 것**: `stories/ areas/ sitemap.xml` → `make_pages.py`,
   `quote* contract statement schedule upload office admin-lock.js apps-script/*/Code.gs` → `port_docs.py` 규칙으로.
6. **사진 번호 ↔ 데이터**: 새 사진은 `WORKS` 에 `{i, t, o, c}` 추가 + `SOURCES.md` 기록. 대문 갤러리는 `data-pick` 번호, 섹션 배경은 인라인 `style="background-image:url(assets/img/works/wN.webp)"`.
   이야기 · 지역 사진은 `make_pages.py` 의 `photos=[…]`.
7. **분야 코드 7개**(church corp gov school show install gear)가 app.js `WORKS.c` · `UP_CAT` · portfolio 필터 `data-f` ·
   `port_docs.py UPLOAD_CATS` slug 에 모두 같아야 한다.
8. **문의 서버 응답 규칙**: `{ok:true}` 일 때만 성공으로 친다. 서버가 바뀌면 app.js `FORM_ENDPOINT` · edit.js `SEND_ENDPOINT` · quote.html `문의서버`(이식기 원본 쪽) 세 군데.
   quote 의 예비 경로 FormSubmit 수신 주소는 큰길브리지 메일이다(quote.html `견적_수신_이메일`).
9. **수정 모드 대상 페이지**: 새 서브 페이지를 만들면 `es-edit` 메타 + `edit.js` 를 넣고 `apply_edits.py` 의 `PAGES` 에도 추가.
10. **noindex 업무 화면**을 sitemap · 메뉴에 넣지 말 것. robots Disallow 와 meta noindex 를 같이 유지.
11. **직인 없음**: `stamp-j6.png` 가 생기면 `assets/img/` 에 넣기만 하면 계약서 · 명세서에 찍힌다. 그림으로 흉내 내지 말 것.
12. **대문 `#litQuote`** 는 JS 가 단어마다 `<span class="w">` 로 쪼갠다. 안에 `<em>` 외 태그를 넣으면 깨진다(수정 모드에서도 제외됨).

## 15. 처음부터 다시 만드는 순서

1. 빈 레포에 `.nojekyll` · `CNAME` · `README.md`. GitHub Pages 를 `main` / 루트로.
2. `assets/style.css` — §4 토큰 → 공통 조각(.btn .eyebrow .h2 .sec .reveal) → 머리 · 시트 → 히어로 · phead → 섹션 컴포넌트 → 바닥 · quick → 반응형(1080/860/640) → 이야기 · 지역.
3. 로고 · 파비콘 · og.jpg(1200×630) · 현장 사진 `wN/tN.webp` · `SOURCES.md` · 브랜드 로고.
4. `index.html` — 머리 · 시트 · 히어로 · 섹션 9개 · 바닥 · quick · totop · 라이트박스 틀(`references/sections.md` 순서대로). head 에 메타 · OG · geo · JSON-LD(LocalBusiness · WebSite) · 폰트 · stats.js · 포스터 preload.
5. `assets/app.js` — 데이터 칸(NOTICES · FILES · WORKS · BLOG · 서버 주소) → §6 기능 순서대로. 관리자 모드 링크 IIFE 는 파일 끝.
6. 서브 6쪽 — 대문의 머리 · 바닥을 복사하고 `.hd` 에서 `on-dark` 를 뺀다. 각 쪽 JSON-LD 에 BreadcrumbList, contact 는 FAQPage 추가.
7. 히어로 영상(§11) · `edit.js` + 7쪽에 `es-edit` 메타(새 열쇠의 SHA-256 — 열쇠는 문서에 남기지 말 것).
8. `tools/make_pages.py` 로 이야기 · 지역 · sitemap. `robots.txt` · `llms.txt` 작성.
9. 업무 화면: 큰길이벤트 원본을 받아 `tools/port_docs.py` 실행(원본이 없으면 이 단계는 큰길브리지에 요청 — 확인 필요).
10. Apps Script 두 개 배포(`references/backend.md`) → 스크립트 속성 → `CONTRACT_URL` · `GALLERY_URL` 넣고 이식기 재실행.
11. §13 검증 → push → 배포 주소 확인.

## 16. 확인 필요 목록

- `www.j6media.co.kr` 가 실제로 연결됐는지, 연결 후 canonical 등을 바꿀 계획인지.
- 원격에 `photos` 가지와 `photos/photos.json` 이 있는지(클론엔 없음).
- 문의 서버(큰길브리지 공용 Apps Script)의 코드 · 수신자 · 속성 — 이 레포에 없음.
- 히어로 영상을 만든 실제 명령 · 도구.
- 회사 공통 규칙 문서(`brizymedia-common` 스킬)와 대조하지 못함 — 이 문서를 쓸 때 그 파일이 없었다.
