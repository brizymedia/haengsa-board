# 블로그 체계 — 이벤트와 교육연구소

HD기획 `_blog` 체계(원조, `hd-event-homepage/references/blog-system.md`)를 옮기되 **지역 글 → 주제 글**, 회사 사실 근거(company.json) · 효과/의학/통계 표현 금지 · 사진 캡션 제목 고정 규칙을 더했다(GUIDE 6장).

```
_blog/posts/<YYYY-MM-DD>-<slug>.json   원본
_blog/GUIDE.md                         쓰는 규칙(사람도 먼저 고침)
_blog/company.json keywords.json photos.json sources.json
      │ node scripts/blog-plan.mjs              안 쓴 주제
      │ node scripts/blog-check.mjs [--new 파일]  통과해야 올림(실패 exit 1)
      ▼ python tools/build_site.py && node scripts/build-blog.mjs
blog/index.html · blog/event/ · blog/edu/ · blog/<slug>/   (blog/ 는 매번 지우고 새로)
rss.xml(최근 50) · sitemap.xml 의 /blog/ 줄만 교체 · llms.txt 「## 블로그 (행사 준비 체크리스트 · 교육 이야기)」 절 교체
```

## 이 사이트만의 점
- 사이트 공통 값(BASE · noindex · VER · 이름 · 머리글 · 바닥글 · 상담 띠)은 `tools/blog_shell.py` 가 build_site 에서 읽는다 — `build-blog.mjs` 에 도메인 · 전화가 없다. **`python` 명령이 3.12+ 여야 한다**(build_site f-string).
- 링크는 **전부 상대 주소**(`@@R@@` → 깊이만큼 `../`). 글 안 내부 링크는 `/event.html` 처럼 루트 기준으로 쓰면 빌더가 상대로 바꾼다. og · canonical · JSON-LD 만 BASE 절대주소.
- 분야 2개(`event` 행사 · `edu` 교육). 예약 slug `event · edu · page`.
- 스타일 `assets/blog.css`(`.bl-*`) + style.css. 사진 없는 글 카드는 분야 글자 자리표시(`.bl-ph`).
- 공개 HTML 에는 `edu-edit` 메타가 없어 수정 모드 불가.

## 글 JSON 칸
`slug date category topic title description keyword{main,sub} lead points cover? sections[{h2,blocks}] faq[{q,a}] 근거[{내용,출처}] sources[{name,url}]`
blocks: `p · ul · ol · table{head,rows} · img{path,alt,caption} · tip`. 꾸밈은 `**굵게**` · `[글](/주소|https://…)`.

## 검사기가 막는 것 (blog-check.mjs)
- 형식: 필수 칸, slug 규칙(한글 · 영소문자 · 숫자 · `-`, 70자), 파일 이름 = `<date>-<slug>.json`, date ≤ 오늘(KST), category · topic 이 keywords.json 과 일치, topic 중복 금지, keyword.main = keywords.json `k`.
- 분량: title 15~50 · description 70~160 · lead 80~420 · points 3~5 · sections 4~8 · faq 2~6 · 본문 1800자 이상(2500 미만은 주의) · 표 1개 이상 · 핵심 키워드가 title · description · lead 에(본문 12회 초과 주의).
- 금지 표현: 가격(원) · 무료/당일 회신/할인 · 1위/최초 · 100%/보장 · 퍼센트 · 연혁/경력 연수 · 후기/만족도/리뷰 · 행사 건수 · 「~해 왔습니다」 · 다른 회사 이름 · **효과 단정 · 의학 표현(치료 · 진단 · 처방 · 치유 — 「심리치료」만 예외)** · 「연구에 따르면」류 · 작성자 메모.
- 숫자: `○○곳` 은 company.json `허용숫자` 만, 연도는 허용 목록 밖이면 주의.
- 사진: photos.json 에 있고 `제외` 아님, 파일 존재, 한 글에 같은 사진 두 번 금지, alt 8~120자, 캡션에 photos.json `제목` 그대로, 목록에 없는 연도 · 학교 이름 금지.
- 링크: 내부 링크 2개 이상, `/contact.html` 또는 `/quote.html` 1개 이상, `/event.html` 또는 `/education.html` 1개 이상, 없는 내부 주소 금지, 외부는 https.
- 출처: sources 는 sources.json 주소만, 법 · 기준 · 기관 · 특보 이야기를 하면 sources 필수.
- 근거: 2개 이상, 본문에 그대로 있는 구절, company.json 근거 1개 이상(45자 이하, company.json 사실 문장 안에 있어야), sources 를 달았으면 그 출처 근거 1개 이상.
- 회사 약속: 회사를 주어로 한 문장은 `약속키워드`(사전 상담 · 현장 답사 · 대체 프로그램 · 현장 사진 · 소장이 직접 · 직접 진행) 범위 안이어야.
- 중복: 다른 글과 4글자 조각 30% 초과 겹침 금지(20% 초과 주의).

## 현재 상태 (2026-10-28 이 분석에서 실행)
- 글 10편, 모두 2026-10-21: event 5(초등운동회 · 유아운동회 · 어린이날부스 · 공연 · 체육대회) · edu 5(감정교육 · 임원리더십 · 발표회 · 과학마술 · 진로). 표지 사진 있는 글 6, 없는 글 4(교육 글 대부분 — 블로그 목록에 교육 사진이 없어서).
- `node scripts/blog-check.mjs` → 「통과 (주의 1건)」: 매직쇼 · 버블쇼 글 본문 2493자.
- `node scripts/blog-plan.mjs` → 「모든 주제를 썼습니다 — keywords.json 에 새 주제를 추가하세요」.
- keywords.json 의 검색량은 조사하지 않았다고 파일에 적혀 있다.
- 블로그 사진 목록은 g01~g10 · story-2011 뿐. 2026-10-25 에 받은 p/ 사진 87장(과학수업 사진 포함)은 아직 photos.json 에 없다 → 교육 글에 사진을 넣으려면 사진을 직접 열어 보고 photos.json 에 추가(제목은 WORKS 제목 그대로).

## 새 글 쓰는 순서
1. `keywords.json` 에 주제 추가(검색량 근거가 없으면 그 사실을 적어 둠) → `blog-plan`.
2. 법 · 기준 이야기가 필요하면 공식 페이지를 직접 열어 `sources.json` 에 `{name,url,확인일,사실}` 추가(못 열면 쓰지 않음).
3. 회사 이야기는 `company.json` 문장 범위 안에서만.
4. `_blog/posts/<오늘>-<slug>.json` 작성 → `node scripts/blog-check.mjs --new _blog/posts/<파일>` 통과까지(사실을 꾸며서 통과시키지 않는다).
5. `python tools/build_site.py && node scripts/build-blog.mjs` → `/blog/` 확인 → 커밋. 검색 등록은 도메인 · NOINDEX 해제 뒤(IndexNow 키 파일도 도메인 뒤에 만든다 — GUIDE).
