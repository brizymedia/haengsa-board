# 생성 페이지 — 행사 이야기 · 지역 페이지 · 블로그 · 검색 파일

세 생성기 모두 **index.html 의 머리·머리글·바닥글을 빌려** 쓴다(`<main id="top">` 앞 = 머리, `</main>` 뒤 = 바닥).
그래서 대문 메뉴·바닥글·`robots` 를 고치면 **둘 다 다시 돌린다**:

```bash
python tools/make_pages.py        # stories/ · areas/ · sitemap.xml(블로그 줄 보존)
node scripts/build-blog.mjs       # blog/ · rss.xml · sitemap.xml(블로그 부분) · llms.txt(블로그 절)
```

빌려 올 때 바꾸는 것(make_pages `shell()` = build-blog `틀()`): 커튼 제거, 라이트박스 제거, `href="#about"` → `href="index.html#about"`, 로고 링크 → `index.html`, `<link rel="canonical">`·`og:url` 자리 추가. 블로그는 메뉴 「블로그」에 `aria-current`.
그 뒤 페이지 깊이만큼 상대 주소 앞에 `../` 를 붙인다(`href|src|poster` 와 CSS `url(assets/…)`). 사이트가 하위 폴더(`/pro-event/`)라 절대경로 `/` 를 쓰지 않는 구조. 생성 페이지도 `assets/app.js` 를 그대로 싣는다(대문 전용 기능은 요소가 없으면 안 돎).

## 행사 이야기 · 지역 (tools/make_pages.py)

- 내용은 파일 안 `STORIES`(5편) · `AREAS`(9곳) · `SERVICES` 표만 고친다. **사실만**(홈페이지 포트폴리오 · 원본 사이트 게시물 · 네이버 블로그 · 대표 확인분).
- STORIES 항목: `slug, title, cat, date, place, area(지역 slug), lead, facts[(이름,값)], body[문단], photos[w13/b8/cy1 …], blog(네이버 글 번호), video(유튜브 id), quote[견적 품목 id]`.
  - 사진 이름 규칙 `pic()`: `cy*`·`ot*` → `assets/img/stories/`, `w*` → `works/`, 나머지 → `biz/`.
- AREAS 항목: `slug, name, hall(구청/시청), min, km, hq(본사), branch(지사), done[기록], photos`. 분·km 은 「서울 본사(역삼동 중심)→각 구청·시청, OSRM 막히지 않을 때, 2026-10-03 조회, 5분 단위 반올림」.
- 기록(done)이 없으면 「아직 이 페이지에 적을 만큼 정리된 기록이 없습니다」 문구 — 지어내지 않는다.
- 각 페이지: `.phead` 머리 → 본문(`.story` 사이드 카드 dl / `.area3` 이동 시간·한 행사·사진) → 「다른 이야기」/「이런 행사」 → `.callband` 상담 띠(전화 2개 + 자동 견적서 + 문의 폼).
- 출력: `stories/<slug>.html` + `stories/index.html`, `areas/<slug>.html` + `areas/index.html`, `sitemap.xml`(BASE + quote + 위 페이지들, lastmod = 오늘, 기존 `/blog/` 줄은 보존).
- 실행 결과 메시지: `행사 이야기 6 · 지역 10 · sitemap.xml 갱신`(index 포함 개수).

## 블로그 (scripts/ + _blog/)

규칙서 `_blog/GUIDE.md` 가 정본. 요약:

1. `node scripts/blog-plan.mjs` — 지역(regions.json `비중`)·주제(keywords.json 검색량 × 성수기 × 지역전용) 추천. 같은 지역 같은 topic 은 한 번만.
2. 글 JSON 작성: `_blog/posts/<YYYY-MM-DD>-<slug>.json` — `slug, date, region, topic, title(15~50), description(70~160), keyword{main,sub}, lead(80~420), points(3~5), cover{path,alt,caption}, sections(4~8){h2, blocks}, faq(2~6), 근거(3+), sources`.
   blocks: `p` `ul` `ol` `table{head,rows}` `img` `tip`. 꾸밈은 `**굵게**` 와 `[글자](/주소|https://…)` 만. 주소는 **레포 루트 기준 `/quote.html`** 로 쓰면 빌드가 상대 주소로 바꾼다.
3. `node scripts/blog-check.mjs --new _blog/posts/<파일>` 통과할 때까지 고친다(검사기 통과용 억지 문장 금지 — 그럴 거면 글을 버림).
4. `node scripts/build-blog.mjs` — `blog/` 를 **지우고** 새로 만든다. 결과 HTML 손수정 금지.
5. 검색 등록 전(noindex)이라 네이버 서치어드바이저·IndexNow 알림은 하지 않는다.

블로그에서 **쓰면 안 되는 것**(GUIDE 2장, 검사기가 일부 막음): 가격(원), 1위·최초·No.1, 100%·보장, 경력 연수·설립 이래, 후기·만족도, 행사 건수, 우리 행사 참가 인원 수, 대문의 「2006년부터·729회·NO.1·20년 차·20,000명·전문 MC 8인·라인업 60+」, 회사가 약속한 적 없는 서비스(케이터링·이동식 화장실·셔틀 등), 동네 이름에 특징 붙이기, 다른 회사 이름(HD기획·나인엠씨·큰길이벤트 포함), 얼굴이 크게 나온 사진·목록에 없는 사진·AI 그림·`_raw/` 원본.
→ 대문에는 숫자 자랑이 있지만 블로그에는 없다. 두 곳의 기준이 다르다는 점을 기억할 것.

빌드 산출물: 글 페이지(BlogPosting·BreadcrumbList·FAQPage JSON-LD, 읽는 시간 = 본문 글자수/500), 목록(24개씩), 지역 모음(글 없는 지역은 noindex,follow), `rss.xml`(최근 50), sitemap(`/blog/` 줄 교체), llms.txt(「## 블로그」 절).
블로그 전용 CSS 는 `build-blog.mjs` 안 `CSS` 상수(`.bp` `.bchips` `.bpager` 등) — 각 페이지 `<style>` 로 들어간다.

## 검색 · AI 검색 파일

| 파일 | 누가 씀 | 메모 |
|---|---|---|
| `sitemap.xml` | make_pages(대문·견적·stories·areas) + build-blog(blog) | 지금 38개 URL. 주소는 `https://brizymedia.github.io/pro-event/…` |
| `rss.xml` | build-blog | |
| `llms.txt` | 위쪽 회사 정보·대표 실적·주요 페이지는 손으로, 「## 블로그」 절은 build-blog | **함정: 블로그 절이 빌드할 때마다 한 벌씩 늘어난다**(아래) |
| `robots.txt` | 손으로 | contract·statement·upload·schedule·office Disallow. 주석: 하위 폴더 주소에서는 로봇이 안 읽음 → 도메인 연결 후 Sitemap 주소 교체 |
| `<meta name="robots">` | index.html `noindex,nofollow`(시안) → 생성 페이지가 물려받음 | quote.html 만 `index,follow`. 업무 화면은 port_docs `noindex()` |

### llms.txt 블로그 절 중복 (확인된 버그)

`build-blog.mjs` 끝부분 정규식 `/^## 블로그[^]*?(?=^## |\s*$)/m` 에서 `\s*$` 가 m 플래그 때문에 **제목 줄 끝에서 바로** 걸린다 → 제목 줄만 바뀌고 옛 목록이 아래에 남는다.
지금 레포의 llms.txt 에 블로그 목록이 이미 여러 벌 들어 있고, 사본에서 빌드를 한 번 더 돌리면 12줄이 또 붙는 것을 확인했다(2026-10-28).
고치려면 lookahead 를 문서 끝 `(?![^]*\S)` 또는 다음 `^## ` 만으로 바꾸고, llms.txt 의 중복 목록을 한 벌만 남긴다. 고친 뒤 두 번 연속 빌드해 `git diff llms.txt` 가 비는지 확인.
