---
name: hd-event-homepage
description: HD기획(서울 금천구 행사 기획·대행사, www.hdplan.co.kr, 레포 brizymedia/hd-event) 홈페이지를 처음부터 다시 만들거나 이어서 고칠 때 쓴다. "HD기획", "hdplan", "hd-event", "HD기획 블로그 글", "_blog 이식", "build-blog", "blog-check", "견적서·계약서·거래명세서·행사 일정·사진 올리기", "지역 페이지·행사 이야기 다시 만들기" 같은 말이 나오면 이 스킬을 먼저 읽는다.
---

# HD기획 홈페이지 (brizymedia/hd-event)

큰길브리지(브리지미디어)가 납품한 정적 홈페이지. 서버 없이 HTML·CSS·JS 파일만으로 돌고,
업무 화면 뒤쪽만 Google Apps Script 두 개를 쓴다. **이 사이트의 `_blog/` 블로그 체계가 원조**라
다른 고객 사이트들이 이것을 옮겨 갔다(이식법은 `references/blog-system.md`).

이 스킬에는 코드 복사본이 없다. 사이트 전체는 레포를 받아서 쓴다.

```bash
git clone https://github.com/brizymedia/hd-event.git   # 사이트 전체 받기
cd hd-event && npx -y http-server . -p 8178 -c-1        # 미리보기 → http://localhost:8178
```
`file://` 로 열면 영상·글꼴·fetch 가 안 된다(README 기준). 반드시 로컬 서버로 본다.

세부 문서:

| 파일 | 내용 |
|---|---|
| `references/file-map.md` | 파일 하나하나의 역할 · 생성물/원본 구분 |
| `references/design-tokens.md` | 색 hex · 글꼴 · 간격 · 반응형 기준 · 컴포넌트 클래스 |
| `references/sections.md` | 페이지별 섹션 구성(대문 14구획 · 포트폴리오 · 지역 · 이야기 · 블로그) |
| `references/blog-system.md` | `_blog` 원본 → 생성기 → `/blog/` · 검사기 · 계획기 · llms.txt · rss · **다른 사이트 이식 절차** |
| `references/workflows.md` | 견적 · 계약 · 명세서 · 일정 · 사무실 · 사진 올리기 흐름과 상태 저장 |
| `references/backend.md` | Apps Script 두 개(계약 · 갤러리)와 공용 문의 서버, 배포 규칙 |

---

## 1. 회사 정보 (사이트에 공개된 것만)

- 상호 **HD기획** (영문 HD Planning / 업무 화면 `HD PLANNING`) · 대표 **엄원식** · 개인사업자(README)
- 주소 서울시 금천구 시흥대로26길 69-24 · 이메일 16zone@hanmail.net
- 대표 전화: 사이트에 공개된 010 휴대폰 번호 한 개. 이 스킬에는 적지 않는다 —
  `index.html` 머리 `.tel`, `tools/port_docs.py` `TEL`, `tools/make_pages.py` `TEL`, `scripts/build-blog.mjs` `TEL` 에 있다.
- 운영 지역 서울 · 광명 · 남양주(직접 답사). 슬로건 「행사의 처음부터 끝까지, 한 팀이 책임집니다.」
- 약속(사이트 문구): 견적 문의 1영업일 안에 1차 구성안과 함께 회신, 행사장 답사 · 1차 구성안 무료, 담당자가 바뀌지 않음.
- 사업자등록번호: **아직 없음**(README · `port_docs.py BIZNO=''`). 받으면 푸터 COMPANY 줄과 `BIZNO` 에 넣고 다시 생성.
- 납품 근거: 큰길브리지 계약 KB-20260906-273(기업형, 2026-09-06). 벤치마킹: 나인엠씨(구조) + 프로이벤트 리뉴얼(사진·영상).
- 관리: 큰길브리지 1533-7295 · www.ai-make.co.kr (office.html 하단 문구).

## 2. 레포 · 도메인 · 배포

- 레포 `brizymedia/hd-event`, 기본 가지 `main`. 사진 업로드용 `photos` 가지를 따로 쓴다(포트폴리오가 런타임에 읽음, `references/backend.md`).
- 도메인 `CNAME` = `www.hdplan.co.kr`. canonical · og · sitemap · robots · JSON-LD 가 모두 이 주소.
- 배포: **GitHub Pages 가 main 을 그대로 서비스**(빌드 단계 없음). 레포에 `.github/workflows/` 없음.
  생성기(`node scripts/build-blog.mjs`, `python tools/make_pages.py`, `python tools/port_docs.py`)는 사람이 로컬에서 돌리고 결과를 커밋한다.
- `_blog/` 는 밑줄 폴더라 GitHub Pages(Jekyll)가 공개하지 않는다(build-blog.mjs 주석). `.nojekyll` 은 없다.
- 루트 `<32자 hex>.txt` 는 IndexNow 소유 확인 파일, 같은 값이 `_blog/indexnow-key.txt` 에 있다(값은 여기 적지 않음).
- 유입 통계: 모든 공개 페이지 `<head>` 에 `https://www.ai-make.co.kr/stats/stats.js` `data-site="hd"` (큰길브리지 유입 서버, 레포 밖).
- 로컬 클론의 git 기록은 커밋 1개뿐이었다(`b00b25a 2026-10-28 블로그 생성기: llms.txt 블로그 목록이 다시 돌릴 때마다 겹치던 것 고침`). 얕은 클론이라 이전 기록은 「확인 필요」. 날짜 흐름은 README 기준: 09-06 계약 → 09-13 오픈 공지 → 09-26 검색 공개 → 10-03 업무 도구 이식 → 10-04 관리자 모드 → 10-13 블로그 이식 → 10-28 llms.txt 중복 수정.

## 3. 파일 지도 (요약 — 자세히는 `references/file-map.md`)

```
index.html          대문 한 장(섹션 앵커 메뉴). 손으로 고치는 원본
portfolio.html      포트폴리오 19장 + 업로드 사진. make_pages.py 가 이 파일의 머리·꼬리를 「틀」로 빌린다
assets/style.css    공통 스타일(?v=3)          assets/app.js  공통 스크립트(?v=20261004)
assets/img/         sys/ slider* hero_poster(워터마크 없음) · works/ biz/(프로이벤트 워터마크)
assets/video/       hero_md.mp4(720p) · hero_sm.mp4(폰)
stories/ areas/     생성물 ← tools/make_pages.py
blog/ rss.xml       생성물 ← scripts/build-blog.mjs (+ sitemap.xml · llms.txt 의 블로그 부분)
_blog/              블로그 원본(posts/*.json, GUIDE.md, regions/keywords/photos/sources.json)
quote.html quote-catalog.js contract.html statement.html schedule.html upload.html office.html admin-lock.js
                    업무 화면 = 큰길이벤트 원본에서 tools/port_docs.py 로 옮긴 생성물(손 수정 금지)
apps-script/        contract/ · gallery/ Code.gs + README (port_docs.py 가 옮김)
tools/              port_docs.py · make_pages.py · admin_gate.py
scripts/            build-blog.mjs · blog-check.mjs · blog-plan.mjs
llms.txt rss.xml sitemap.xml robots.txt CNAME
```

**원본 / 생성물 구분이 이 사이트의 핵심 규칙이다.** 생성물 HTML 을 직접 고치면 다음 실행 때 사라진다.

| 고칠 것 | 고치는 곳 | 다시 돌릴 것 |
|---|---|---|
| 대문 글 · 섹션 | `index.html` | — |
| 공지사항 | `assets/app.js` 맨 위 `NOTICES` | — |
| 포트폴리오 목록(사진 번호↔제목) | `assets/app.js` `WORKS` | — |
| 행사 이야기 · 지역 페이지 | `tools/make_pages.py` `STORIES` · `AREAS` · `SERVICES` | `python tools/make_pages.py` → **그다음 반드시** `node scripts/build-blog.mjs` |
| 블로그 글 | `_blog/posts/<날짜>-<slug>.json` | `node scripts/blog-check.mjs --new <파일>` → `node scripts/build-blog.mjs` |
| 견적 품목 | `tools/port_docs.py` `CATALOG` | `python tools/port_docs.py <큰길이벤트 레포 경로>` |
| 업무 화면 문구 · 색 · 서버 주소 | `tools/port_docs.py` 「회사 설정」 | 위와 같음 |

## 4. 디자인 체계 (요약 — `references/design-tokens.md`)

- 톤: **화이트 + 잉크 + 오렌지레드 포인트**. 대문·공개 페이지는 흰 바탕, 업무 화면(견적·계약 등)은 어두운 바탕 `#0B0E15`.
- 핵심 토큰(`assets/style.css :root`): `--acc #F0472B` · `--acc2 #FF7A4D` · `--ink #111318` · `--navy #101522` · `--txt #22252D` · `--muted #6B7180` · `--bg2 #F4F5F7` · `--line #E4E6EB` · `--r 16px` · `--max 1280px` · `--gutter clamp(18px,4.5vw,64px)`.
- 글꼴: 본문 **Pretendard Variable**(jsDelivr v1.3.9 dynamic-subset), 영문 라벨·숫자 **Montserrat 600/700/800**(Google Fonts). 업무 화면은 Pretendard static.
- `body{word-break:keep-all}` — 빼면 한글이 낱자로 끊긴다.
- 반응형 기준 **1100 / 900 / 600px** (지역·이야기 쪽은 1100 / 960 / 600). 900 이하에서 상단 띠의 슬로건·전화가 사라지고 햄버거 + 폰 하단 빠른 단추(`.quick`)가 나온다.
- 반복 패턴: `.sec-head`(영문 꼬리표 `.en-t` + h2 + 설명), `.reveal`(스크롤 등장), 사진은 `background-image` 카드, 어두운 그라데이션 덮개, `.btn-pri` 주황 단추.
- 로고는 이미지가 아니라 CSS: `.logo .mark`(검은 네모 「HD」 + 오른쪽 아래 주황 점) + 「HD기획 / EVENT PLANNING」. 파비콘 `assets/img/favicon.svg`, 메일용 `logo-h-white.png`.

## 5. 페이지 구성 (요약 — `references/sections.md`)

대문 `index.html` 순서: 상단 흰 띠(`.top`) → 검은 메뉴 띠(`.bar`, sticky) → 폰 메뉴(`.sheet`) →
① 히어로 슬라이더 5장 ② 핵심 가치 4탭(기획·연출·운영·신뢰) ③ 바로가기 3장(`.trio`) ④ 회사소개 + 숫자 4개(`#about`)
⑤ 사업분야 8(`#business`) ⑥ 프로세스 5단계(`#process`) ⑦ 갤러리 9장(`#gallery`) ⑧ 현장 영상 + 준비물 안내(`#video`)
⑨ 콘텐츠 3타일(`#contents`) ⑩ 고객후기 4(`#review`) ⑪ 공지 · 견적 받는 법 · 오시는 길(`#notice`) ⑫ 견적 문의 폼(`#contact`)
→ 푸터 → 폰 하단 빠른 단추 → 맨 위로 → 라이트박스.

## 6. 스크립트 기능 (`assets/app.js`, 외부 라이브러리 없음)

1. 상단 띠: 스크롤 시 `.bar.stuck`(미니 로고·CTA 표시), 현재 섹션 메뉴에 `.act`, 맨 위로 단추(700px 이후).
2. 폰 메뉴 `#burger` ↔ `#sheet` 열고 닫기(body 스크롤 잠금).
3. 히어로 슬라이더: 6초 자동, 점·이전/다음·스와이프(50px), 마우스 올리면 멈춤, 탭 숨기면 멈춤, `prefers-reduced-motion` 이면 자동 넘김 끔. `data-src` 를 배경으로 넣음.
4. 가치 탭 `#vtabs` ↔ `#vpanes`.
5. `.reveal` 등장(스크롤 검사 + 0.6초·2초 재검사), `[data-count]` 숫자 올라가기(IntersectionObserver).
6. 갤러리: 대문 `#gal` 은 `WORKS` 앞 9장, 포트폴리오 `#pfGrid` 는 전체 + `photos` 가지의 `photos.json` 을 fetch 해 앞에 붙임. 필터 `#filters [data-f]`, 라이트박스(←→·Esc).
7. 현장 영상 `#player`: 화면폭×DPR < 900 이면 `hero_sm.mp4`, 아니면 `hero_md.mp4` 를 그때 붙임. 누르면 소리 켜고 재생.
8. 공지 `NOTICES` 앞 5개를 `#noticeList` 에(n:true 면 NEW).
9. 문의 폼 `#quoteForm`: 숨은 `website` 칸 스팸 함정 → `FORM_ENDPOINT`(공용 문의 서버)로 JSON POST(`text/plain`) → `{ok:true}` 일 때만 완료. 실패하면 폰은 `sms:` 문자 앱, PC 는 내용 복사 + 전화 안내.
10. 관리자 모드 입구: 모든 `<footer>` 끝에 작은 「관리자 모드」 링크 → `office.html`(app.js 맨 아래 별도 IIFE).

## 7. 업무 화면 (요약 — `references/workflows.md`)

`office.html`(대표 전용 문서함, 공개 링크 없음, 대표 암호 잠금)이 입구.
흐름: 문의 메일 → `quote.html?admin=1` 견적 발행·저장함 → 「계약서 작성」 → `contract.html?admin=1` 서명 링크 → 고객 폰 서명 → PDF 메일
→ 「행사 일정」 `schedule.html` 체크리스트 → 「사진 올리기」 `upload.html` → 「거래명세서」 `statement.html?admin=1`.

- 화면 사이 데이터는 **주소 해시에 base64url JSON** 으로 넘긴다: 견적 `#q=` · 계약 `#c=` · 명세서 `#t=` · 일정 `#new=` / `#e=<id>`.
- `?admin=1` 화면은 `admin-lock.js` 가 잠근다 — 계약 서버에 `{action:'boxList', pw}` 를 보내 ok 면 연다. 암호는 코드에 없고 서버 스크립트 속성 `BOX_PW`.
- 암호 3종: 보관함(대표) `BOX_PW` · 직원 `CREW_PW`(일정만) · 사진 올리기 `UPLOAD_PW`. 기기에는 localStorage `hd-quote-box-pw` · `hd-sched-pw` · `hd_pw`(선택).
- 손님용 `quote.html` 은 금액·직인을 숨긴다(카탈로그 34품목 전부 `price:null`). **"총액이 바로 나온다"고 쓰지 말 것.**

## 8. 백엔드 (요약 — `references/backend.md`)

| 서버 | 쓰는 곳 | 코드 |
|---|---|---|
| 공용 문의 서버(큰길브리지와 공유) | 대문 문의 폼 · 견적 문의 · 계약 서명 알림 | 이 레포에 없음 |
| 계약 서버 `hd-contract` | 계약 · 견적 저장함 · 행사 일정 · 관리자 잠금 | `apps-script/contract/Code.gs` |
| 갤러리 서버 | 사진 올리기 → GitHub `photos` 가지 | `apps-script/gallery/Code.gs` |

배포 규칙: 웹 앱, **실행 = 나, 액세스 = 모든 사용자**. 코드를 고치면 「배포 관리 → 연필 → 새 버전」(새 배포를 만들면 주소가 바뀐다).
비밀값(암호 · GitHub 토큰)은 **스크립트 속성에만**. 주소는 `port_docs.py CONTRACT_URL / GALLERY_URL` 에 넣고 `port_docs.py` 를 다시 돌린다.

## 9. 블로그 체계 (핵심 — 전부는 `references/blog-system.md`)

```
_blog/posts/<YYYY-MM-DD>-<slug>.json   ← 원본(사람/루틴이 씀)
_blog/GUIDE.md                         ← 쓰는 규칙(사람도 이걸 먼저 고친다)
_blog/regions.json  keywords.json  photos.json  sources.json   ← 근거 자료
        │ node scripts/blog-plan.mjs   (다음에 쓸 지역 · 주제 고르기, --json 은 루틴용)
        │ node scripts/blog-check.mjs --new <파일>   (통과해야 올림, 실패 시 exit 1)
        ▼ node scripts/build-blog.mjs
/blog/index.html · /blog/page/N/ · /blog/<지역>/ · /blog/<slug>/   (blog/ 는 매번 지우고 새로 만듦)
/rss.xml(최근 50) · sitemap.xml 의 /blog/ 줄만 교체 · llms.txt 「## 블로그」 절만 교체
```

- 글 JSON 칸: `slug date region topic title description keyword{main,sub} lead points cover sections[{h2,blocks}] faq 근거 sources`.
  blocks 는 `p · ul · ol · table{head,rows} · img{path,alt,caption} · tip`. 꾸밈은 `**굵게**` 와 `[글](/주소|https://…)` 뿐.
- 검사기가 막는 것: 가격(원) · 1위/최초 · 100%/보장 · 연혁·경력 · 후기·만족도 · 행사 건수 · 참가 인원 · "~해 왔습니다" · 경쟁사 이름(프로이벤트·나인엠씨) · 작성자 메모,
  photos.json 에 없거나 `제외` 인 사진 · 같은 묶음 사진 2장 · 지역 모르는 사진에 지역 캡션, 공식 기관 도메인인데 sources.json 에 없는 주소,
  견적 항목표에 견적서에 없는 품목, 동네에 특징 붙이기, 지역 문의 통계 지어내기, `근거` 3개 미만·본문에 없는 근거, 같은 지역·같은 주제 중복, 다른 글과 4글자 조각 30% 초과 겹침.
- 분량: title 15~50자 · description 70~160 · lead 80~420 · points 3~5 · sections 4개 이상 · faq 2~6 · 본문 1800자 이상(2500 권장) · 사진 3장 이상.
- 2026-10-13 에 10편(금천 2편 + 나머지 8곳 각 1편). 현재 `blog-check` 전체 통과, `blog-plan` 남은 후보 116개(2026-10-28 실행).
- 회사 사실은 GUIDE 4장 목록뿐. 현장기록은 영등포 「국회 개방행사 놀이존 운영(2024)」 하나. **works/ · biz/ 사진은 전부 제외**(워터마크).

## 10. 지역 페이지 · 행사 이야기

`python tools/make_pages.py` 한 번이 `stories/`(5편 + 목록) · `areas/`(9곳 + 목록) · `sitemap.xml` 전체를 다시 쓴다.
- 틀: `portfolio.html` 의 `<main id="top">` 앞(머리)과 `</main>` 뒤(꼬리)를 빌리고 라이트박스만 뺀다. 그래서 **메뉴를 바꾸면 portfolio.html 을 고친 뒤 돌린다.**
- 경로: 생성 후 상대 경로에 `../` 를 붙이고 `@@` 표시를 `../` 로 바꾼다(두 폴더 모두 한 단계 아래).
- STORIES 근거는 `app.js WORKS`(제목·분야·연도)뿐, 숫자·후기 없음. AREAS 이동 시간은 금천 본사 → 구청·시청 OSRM(2026-10-03, 5분 반올림).
- ⚠ `make_pages.py` 의 `sitemap()` 은 sitemap.xml 을 **통째로** 새로 쓴다 → 블로그 줄이 사라진다. **항상 이어서 `node scripts/build-blog.mjs`** 를 돌린다.

## 11. 사장님 수정 모드 · 관리자 모드

- 관리자 모드: 푸터 끝 「관리자 모드」 → `office.html`. `tools/admin_gate.py` 가 `<!--GATE-->…<!--/GATE-->` 잠금 화면을 씌운다(여러 번 돌려도 한 번만). 대표 암호(`BOX_PW`)로만 열리고, 맞으면 기기에 기억 + `sessionStorage hd-office`. 「잠그기」 단추 있음.
- 사장님 글 수정 모드: `office.html` 안내문에 「주소 뒤 `?edit=열쇠` → 글 직접 고치기 → 『저장 파일 받기』로 보내면 반영」이라고 적혀 있으나, **이 레포 안에는 `?edit=` 를 처리하는 코드가 없다.** 외부 `stats.js` 가 처리하는지 **확인 필요.**

## 12. 히어로 · 영상

- 히어로는 **사진 슬라이더**(영상 아님). 5장: `hero_poster.webp` → `sys/h2_4` → `sys/h3_2` → `slider2` → `sys/h1_8`. 첫 장만 `<h1>`, 나머지는 `<p class="h1">`(h1 중복 방지).
- 7초 켄번스(`@keyframes kb`), 점 진행바 6초(`fill`), 글자는 `up` 애니메이션 순차.
- 「현장 영상」은 `#video` 섹션의 `<video data-src data-src-sm poster=hero_poster>`. 영상은 프로이벤트 현장 몽타주(워터마크 포함) — HD기획 영상이 생기면 `assets/video/` 교체(README).

## 13. 사진 출처 규칙

- `assets/img/works/`(19) · `biz/`(8) 에 「CREATIVE PLAN PROEVENT」 워터마크. 대문 히어로·사업분야·타일은 워터마크 없는 `sys/ · slider* · hero_poster` 만 쓴다. 갤러리·포트폴리오·이야기는 아직 works/ 를 쓴다 → **HD기획 사진으로 교체 필요**(바꿀 때 `WORKS` 와 `make_pages.py STORIES.photos` 같이).
- 블로그는 `_blog/photos.json` 목록만. `slider1`(얼굴) · `slider4`(단체 얼굴) · `sys/h1_1`(자료 화면) 제외.
- 새 사진은 `upload.html`(긴 변 1600px JPEG 사본, 워터마크 선택) → `photos` 가지. 원본은 폰에만 남는다.
- AI 그림 · 얼굴 크게 나온 사진 · 장소를 바꿔 쓰는 캡션 금지(GUIDE 2장).

## 14. 검증 절차

```bash
# 1) 문법
for f in scripts/*.mjs assets/app.js admin-lock.js quote-catalog.js; do node --check "$f"; done
python -c "import ast;[ast.parse(open(f,encoding='utf-8').read()) for f in ['tools/make_pages.py','tools/port_docs.py','tools/admin_gate.py']]"
# 2) 블로그
node scripts/blog-check.mjs            # 「통과」가 나와야 함
# 3) 화면 — 서버를 띄우고 375px · 1280px 두 폭에서 본다
npx -y http-server . -p 8178 -c-1
```
- 375px: 가로 스크롤 없음, 하단 빠른 단추가 마지막 내용을 가리지 않음(`body{padding-bottom:56px}`), 가치 탭 2×2, 갤러리 2열, 폼 1열.
- 1280px: 검은 메뉴 띠 9개 링크가 한 줄에 들어가는지(스크롤 전 미니 로고·CTA 는 투명). **이 분석에서는 브라우저로 직접 보지 못함 — 확인 필요.**
- 콘솔 오류 0. 대문 · portfolio · stories/ · areas/ · blog/ · quote · contract?admin=1 · office 를 각각 연다.
- 업무 화면은 서버(Apps Script) 응답에 기대므로 오프라인에서는 「연결 안 됨」이 정상.

## 15. 반복되는 함정과 같이 고칠 곳

1. **메뉴가 네 군데**: `index.html`(`.bar .menu` + `.sheet nav` + 푸터 `.ftl`) · `portfolio.html`(같은 세 곳, → stories/areas 로 복제) · `scripts/build-blog.mjs` 의 `머리`/`꼬리` 템플릿 · 업무 화면은 `port_docs.py NAV_SITE`.
2. **회사 정보가 열 군데 넘게**: index(JSON-LD · 상단 · 폰메뉴 · 오시는 길 · 문의 · 푸터 · 빠른 단추) · portfolio · `make_pages.py TEL` · `build-blog.mjs TEL·꼬리·상담` · `llms.txt` · `_blog/GUIDE.md` 4장 · `port_docs.py` 회사 설정 · `apps-script/*/Code.gs` · `app.js SMS_TO·COMPANY`.
3. `make_pages.py` 뒤엔 반드시 `build-blog.mjs` (sitemap 블로그 줄 복구).
4. 캐시 꼬리표: CSS `style.css?v=3`, JS `app.js?v=20261004`. 고치면 index · portfolio 의 꼬리표를 올리고 `make_pages.py` 를 다시 돌린다.
5. 블로그는 **루트 절대 경로**(`/blog/`, `/assets/…`). 도메인 루트(www.hdplan.co.kr)에서만 맞다. `github.io/hd-event/` 같은 하위 경로에서는 깨진다. 나머지 페이지는 상대 경로.
6. README 일부가 낡았다: 「도메인 없음」(CNAME 있음), 서버 「배포 전」(office.html · port_docs.py 에 주소가 들어가 있음), `port_docs.py BLOG=''  # 블로그 없음`.
7. `apps-script/gallery/README.md` 가 말하는 Actions 「갤러리 페이지 · 사이트맵 자동 갱신」과 `scripts/prepare-gallery-photos.mjs` 는 **이 레포에 없다**(큰길이벤트 것을 옮긴 문구). `갤러리다시만들기()` 의 `repository_dispatch(photos-updated)` 를 받는 워크플로도 없음. 포트폴리오는 photos.json 을 직접 읽으므로 동작에는 지장 없음.
8. `quote.html` `견적_수신_이메일` · `contract.html` `회사_수신_이메일`(FormSubmit 폴백 · 수신 표시)은 HD기획 메일이 아니라 **큰길브리지 관리 계정 메일**로 되어 있다. 의도인지 **확인 필요**. 계약 서버 `MANAGER_EMAIL` 도 같은 관리 계정(의도적: 사본 수신).
9. 업무 화면 localStorage 일부 키가 큰길 이름 그대로(`kg_contract_co`, `kg_stmt_bank`). 출처(origin)가 달라 충돌은 없지만 바꿀 땐 기존 저장값이 사라진다.
10. 대문 「20,000명」 숫자 · 후기 4개는 **예시**(README). 대표 확인 전 블로그 · 이야기에 쓰지 않는다.
11. 공지 날짜(`NOTICES`)는 2026.09 기준 그대로 — 대표에게 받아 갱신.
12. 견적 품목을 바꾸면 블로그 검사기의 「견적 낱말」도 바뀐다(`blog-check.mjs` 가 `quote-catalog.js` 의 `name:` 을 읽음).
13. office.html 서버 상태 칸은 갤러리 서버 응답의 `설정완료 === false` 일 때 「설정 미완료」를 띄우는데, 서버는 `설정완료` 를 `{UPLOAD_PW:true, …}` **객체**로 준다 → 속성이 빠져도 「연결됨」만 보인다. 실제 점검은 Apps Script 편집기의 `점검` 함수로.

## 16. 처음부터 다시 만드는 순서

1. 레포 생성 · `CNAME` · `robots.txt`(업무 화면 5개 Disallow) · 파비콘.
2. `assets/style.css` 토큰과 공통 컴포넌트 → `index.html` 14구획(`references/sections.md`) → `assets/app.js` 10기능.
3. `portfolio.html`(필터 7개 + `#pfGrid` + 라이트박스). 사진은 워터마크 없는 것부터.
4. `tools/make_pages.py` 로 stories/ · areas/ · sitemap.xml.
5. 업무 도구: 큰길이벤트 원본 레포를 받아 `python tools/port_docs.py <원본 경로>` → quote · contract · statement · schedule · upload · office · admin-lock · apps-script 생성 → `admin_gate.apply()` 자동 호출.
6. Apps Script 두 개 배포(`references/backend.md`) → 주소를 `port_docs.py` 에 넣고 다시 돌림 → 스크립트 속성 `BOX_PW` · `CREW_PW` · `UPLOAD_PW` · `GITHUB_TOKEN` · `GITHUB_REPO`.
7. `_blog/` 자료 다섯 개 + `scripts/` 세 개 → 글 쓰기 → `blog-check` → `build-blog`.
8. `llms.txt` 머리 부분은 손으로, 「## 블로그」 절은 생성기에 맡긴다.
9. 검증(14장) → 커밋 · 푸시 → Pages 반영 → IndexNow · 네이버 서치어드바이저 · 구글 서치콘솔(소유 확인 태그는 아직 없음).

## 17. 지켜야 할 것

- 사실만. 확인 못 한 숫자 · 후기 · 실적 · 장비 기종은 쓰지 않는다. 모르면 「확인 필요」.
- 비밀값(암호 · 토큰)을 코드 · 문서 · 커밋에 넣지 않는다. 계좌번호도 넣지 않는다(`port_docs.py` 가 큰길 계좌를 빈칸으로 바꾼다).
- 결과 HTML 손 수정 금지(blog/ · stories/ · areas/ · 업무 화면). 원본과 생성기를 고친다.
- 다른 회사 이름(프로이벤트 · 나인엠씨)을 공개 글에 쓰지 않는다.
