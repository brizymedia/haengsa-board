# 공모사업 주간 글 루틴

매주 월요일, 공모사업 갱신(GRANT_ROUTINE.md) **다음에** 돈다. 새로 확인된 공모가 있으면 같은 사실을 세 곳에 **서로 다른 글**로 올린다.

| 어디에 | 무엇을 | 누가 올리나 |
|---|---|---|
| 큰길이벤트(큰길이벤트.com) `/life/` | 칼럼 글 1개 (행사 담당자 · 총무 · 단체 입장) | 이 루틴이 push |
| 이벤트 코리아(www.event-korea.co.kr) `/column/` | 칼럼 글 1개 (이벤트 회사 · 프리랜서 입장) | 이 루틴이 push |
| 네이버 블로그 `blog.naver.com/ty-health` | 네이버용 원고 1개 → https://큰길이벤트.com/naver/ 에 복사 단추로 나옴 | **형님이 붙여넣어 발행** |

**네이버는 자동으로 올리지 않는다.** 네이버가 글쓰기 오픈API 를 닫았고 매크로·자동 입력은 계정 제재 대상이다. 루틴은 원고를 올려 두기까지만 한다.
**사람이 보지 않고 라이브에 올라가므로 지어내지 않는 것이 전부다.** 새 공모가 없으면 글을 쓰지 않는다 — 0건은 정상이다. 억지로 채우지 않는다.

## 0. 지켜야 할 것

- 사실(기관 · 사업 이름 · 접수 기간 · 마감 · 신청처)은 **`collector/grants_curated.json` 항목과, `validate_grants.py --peek` 로 읽은 그 항목의 공식 페이지 원문**에서만 가져온다. 검색 요약 · 블로그 · 카페 · 뉴스는 사실의 근거가 아니다.
- 지원내용 · 자격 · 제출서류를 쓸 때는 이번에 `--peek` 로 읽은 원문에 있는 것만, **자기 말로 줄여** 쓰고 출처 링크를 단다. 원문 문장을 그대로 옮기지 않는다. 지원금 **금액은 쓰지 않는다**(검사기가 「숫자+원」을 막는다).
- 원문에서 확인하지 못한 것은 「공고문에서 확인하세요」로 쓴다. 짐작하지 않는다.
- 이전 공모 글(`keungil-event/_column/posts/2026-10-09-grant-application-event-prep.json`, `event-korea/_column/posts/2026-10-09-arts-fund-2027-event-company.json`)에 이미 출처를 달아 둔 일반 요령(NCAS 가입 · 제출 순서 등)은 **그 출처 그대로** 다시 써도 된다. 문장은 새로 쓴다.
- 지원금을 받게 해 준다 · 선정 가능성 · 컨설팅 약속, 가격, 연혁 · 실적 · 후기, 「100% · 무조건 · 보장 · 1위 · 최초」는 쓰지 않는다. 회사 사실은 큰길이벤트 `_blog/GUIDE.md` 4장 목록만.
- 키 · 토큰 · 개인정보는 출력하거나 파일에 쓰지 않는다. 이 문서 · `validate_grants.py` · `grant.py` 는 고치지 않는다.

## 1. 새로 쓸 공모 고르기

1. 작업 폴더 `C:\클로드코드2`. `git pull --rebase`(다른 변경이 있으면 `-c rebase.autoStash=true`). 한국 날짜: `python -c "from datetime import datetime,timedelta;print((datetime.utcnow()+timedelta(hours=9)).date())"`.
2. `collector/grants_posted.json` 의 `posted`(이미 글로 다룬 공모 id → 글 날짜)와 `collector/grants_curated.json` 의 `items` 를 비교한다.
   **새 공모 = 목록에 있고, `posted` 에 없고, 마감이 오늘 이후인 것.** `deadline` 이 없는 「일정 미정」 항목은 일정이 정해지기 전에는 새 공모로 치지 않는다(다음 주에 다시 본다).
3. 같은 기관 · 같은 공고 페이지(`url`)의 항목들은 **한 묶음**으로 본다(예: 아르코 분야별 5건 = 1묶음).
4. 새 공모가 없으면 → **글을 쓰지 않는다.** 보고만 하고 끝낸다(「새 공모 없음」).
5. 새 묶음이 여럿이면 가장 마감이 급하거나 행사 · 공연 · 축제 단체에 쓸모 있는 **한 묶음만** 고른다. 나머지는 `posted` 에 넣지 말고 그대로 둔다(다음 주에 이어서). 한 주에 사이트마다 글 1개를 넘기지 않는다.

## 2. 원문 읽기

고른 묶음의 `url` 마다 `python collector/validate_grants.py --peek <url> [키워드 …]` (30회 이하, robots · 요청 간격은 도구가 지킨다). 읽고 정리할 것:
접수 기간 · 마감 시각, 신청 방법과 신청처, 대상(법인 · 단체 · 개인 중 누구), 이 사업이 지원하는 일의 종류(한 줄), 제출 서류 이름(있으면), 문의처 이름(전화번호는 쓰지 않는다).
읽을 수 없으면(404 · 스크립트로만 그려지는 페이지) 그 묶음은 글을 쓰지 않고 보고한다.

## 3. 글 세 개 쓰기 (같은 사실, 다른 글)

세 글은 **목차부터 다르게** 쓴다. 겹치면 검사기가 막는다(칼럼 글끼리 30%, 네이버 원고는 원글과 25%).

### 3-1. 큰길이벤트 — 작업 폴더 `C:\Users\gilau\Documents\클로드코드` (원격 brizymedia/keungil-event)

1. 먼저 `_column/GUIDE.md` 를 읽는다(특히 2 · 3 · 8장). 형식 모델은 `_column/posts/2026-10-09-grant-application-event-prep.json`(문장을 베끼지 않는다).
2. `git pull --rebase origin main`(다른 변경이 있으면 `-c rebase.autoStash=true`). 이 저장소 main 은 갤러리 봇이 자주 커밋한다.
3. `_column/posts/<오늘>-grant-<yyyymmdd>-<짧은영문>.json` — `category: "industry"`, `topic: "arts-grant"`, 제목에 기관 · 사업 이름과 「공모」, **마감일이 제목이나 첫 문장에**. 읽는 사람: 행사 담당자 · 총무 · 마을 · 동문회 · 단체 대표. 흐름: 무엇이 열렸나(표: 사업 · 기간 · 신청처) → 누가 신청하나 → 신청 전에 모아 둘 행사 자료 → 마감 날 막히지 않으려면 → 장비·무대 업체에는 언제 무엇을 요청하나(일반 요령임을 밝힌다). 내부 링크에 `/#grants`(공모사업 구역)와 `/quote.html`. 표지 사진은 `_column/photos.json` 에서(GUIDE 8장).
4. `node scripts/column.mjs check <새 파일> --also ../event-korea/_column/posts` 가 통과할 때까지. 세 번 고쳐도 안 되면 그 글은 버리고 보고한다. **검사를 통과시키려고 억지 문장을 끼우지 않는다.**
5. `node scripts/column.mjs build` → `git add _column life robots.txt sitemap.xml rss.xml`(생기는 파일만) → 커밋(한국어, 끝에 `Co-Authored-By: Claude …`) → `git push origin main`. 거절되면 `git pull --rebase origin main` 후 build 다시, push.

### 3-2. 이벤트 코리아 — 작업 폴더 `C:\Users\gilau\Documents\event-korea` (원격 brizymedia/event-korea)

1. `_column/GUIDE.md` 를 읽는다. 형식 모델은 `_column/posts/2026-10-09-arts-fund-2027-event-company.json`(문장을 베끼지 않는다).
2. 읽는 사람: **이벤트 회사 · 프리랜서**. 같은 공모를 「단체가 신청한다」가 아니라 「이벤트 회사가 신청자가 되는가, 제작 파트너로 붙는가」, 포트폴리오 · 사업자 서류 · 협력 계약 쪽으로 푼다(원문에서 확인한 범위에서만).
3. 큰길이벤트 글과 목차 · 표 · 도입이 겹치지 않게 쓴다. 표지 사진은 큰길이벤트 사진이면 캡션 맨 앞에 「큰길이벤트기획 현장 —」(자매 회사 사진 표기 규칙).
4. `node scripts/column.mjs check <새 파일> --also ../클로드코드/_column/posts` → `node scripts/column.mjs build` → `git add _column column robots.txt sitemap.xml` → 커밋 → push. 거절되면 `git pull --rebase origin main` 후 build 다시.
   (충돌이 생성 파일 `column/**` 에서만 나면 upstream 쪽을 택하고 build 로 다시 만든다.)

### 3-3. 네이버 블로그(ty-health)용 원고 — 큰길이벤트 저장소 `_column/naver/`

1. `_blog/GUIDE.md` 9장 형식. 파일 이름은 **큰길이벤트 글(3-1)과 똑같이** `_column/naver/<그 글의 파일 이름>`.
2. 홈페이지 글을 요약하지 말고 **도입부터 새로 쓴다**. 원글에 없는 숫자는 쓰지 않는다. 표 · 링크 · `**굵게**` · `#` 소제목 없음, 문단 6개 이상 · 700~2500자, 사진 2장 이상(`_column/photos.json` 에서, 설명의 행사 이름은 목록과 같게), 태그 3~10개.
3. `node scripts/naver-column-check.mjs <파일 이름>` 이 통과할 때까지. 통과하면 3-1 과 함께 커밋 · push(갤러리 워크플로가 `/naver/` 페이지를 다시 만든다).
4. **형님이 해야 할 일**은 보고에 한 줄로 적는다: 「https://큰길이벤트.com/naver/ 에서 복사해 ty-health 에 발행」.
   (어대리(Aside CLI)로 발행하는 `collector/publish_naver.py` 는 2026-10-10 첫 글을 올리는 데 쓰였고 준비돼 있지만, **이 루틴에는 아직 연결하지 않았다** — 형님 확인 뒤에 연결한다. 루틴은 이 스크립트를 실행하지 않는다.)

## 4. 올린 뒤

1. `collector/grants_posted.json` 의 `posted` 에 이번에 다룬 묶음의 공모 id 를 오늘 날짜로 넣는다.
2. `git add collector/grants_posted.json collector/naver_published.json` → 커밋(`공모사업 글 YYYY-MM-DD — 큰길이벤트 · 이벤트 코리아 · 네이버`) → push.
3. 두 사이트 글 주소(`https://큰길이벤트.com/life/<slug>/`, `https://www.event-korea.co.kr/column/<slug>/`)를 1분 뒤 열어 200 인지만 확인한다(Pages 반영이 늦으면 한 번 더). 안 열리면 보고에 적는다.

## 5. 실패했을 때

- 한 곳에서 막혀도 다른 곳은 계속한다. 막힌 곳은 그 글 파일을 남기지 말고(커밋 안 한 채로 두지 말고) 지운 뒤 보고한다.
- push 가 계속 거절되면 멈추고 어디서 막혔는지만 보고한다(강제로 밀지 않는다).
- 세 곳 모두 못 올렸으면 `grants_posted.json` 을 고치지 않는다(다음 주에 다시 시도한다).

## 6. 보고 (한국어, 짧게)

```
공모사업 글 YYYY-MM-DD
다룬 공모: 기관 · 사업 · 마감
큰길이벤트: 제목 — 주소
이벤트 코리아: 제목 — 주소
네이버 원고: 제목 — https://큰길이벤트.com/naver/ (형님이 ty-health 에 붙여넣어 발행)
못 쓴 것: …(이유)
확인이 필요한 점: (없으면 「없음」)
```
새 공모가 없으면: `공모사업 글 YYYY-MM-DD — 새 공모 없음(글 없음)` 한 줄과 다음 주에 이어 볼 것(미정 항목 · 남은 묶음)만.
