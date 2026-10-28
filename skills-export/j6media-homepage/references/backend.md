# Apps Script 백엔드 — 액션 · 필드 · 속성 · 배포

비밀값(암호 · 토큰)은 **절대 코드 · 문서에 적지 않는다.** 전부 Apps Script 「프로젝트 설정 → 스크립트 속성」에만 있다.
여기 적힌 주소(`/exec`)는 공개 웹 앱 주소라 문서에 적어도 된다.

모든 요청은 `fetch(주소, { method:'POST', headers:{'Content-Type':'text/plain;charset=utf-8'}, body: JSON.stringify({...}) })`
(text/plain 이라 CORS 사전 요청이 없다). 응답은 JSON, 성공 판정은 `ok === true`.

---

## 1. 문의 서버 (큰길브리지 공용) — 코드 없음

- 주소: `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec`
- 쓰는 곳: `assets/app.js FORM_ENDPOINT`(문의 폼), `assets/edit.js SEND_ENDPOINT`(수정 요청), `quote.html 문의서버`(견적 문의, 이식 결과).
- 보내는 필드(코드에서 확인): `name, phone, email, service, message, page, at, website(빈 값 = 스팸 함정)` (+ 문의 폼은 `tel org date place people msg kind` 도 같이 실림).
- app.js 주석: 서버가 j6_media@naver.com 으로 메일을 보내고 큰길브리지도 받는다. 서버 코드 · 수신자 설정은 이 레포에 없다 — **확인 필요**.
- 실패 시: 문의 폼은 폰=문자 앱(`sms:` + 본문), PC=클립보드 복사. 견적 문의는 FormSubmit(`formsubmit.co/ajax/<큰길브리지 메일>`)로 한 번 더.

---

## 2. 계약 서버 `apps-script/contract/Code.gs`

- 주소: `https://script.google.com/macros/s/AKfycbxO7crgcZh7SSPAgwbPctHL-ZGF9LVj9O1yZuIbqyVta0PkzKJCsFOoGcThtWXPJyretw/exec`
  (`port_docs.py` 주석: 2026-10-03 배포, 큰길브리지 계정)
- 이 주소가 박힌 곳: `contract.html 서버주소_기본`, `quote/contract/statement` 의 `admin-lock.js data-server`, `schedule.html 서버`, quote 저장함, `office.html` 잠금 · 상태 핑.
  → 바꿀 땐 `tools/port_docs.py CONTRACT_URL` 고치고 이식기 재실행.

### 상수

| 상수 | 값 |
|---|---|
| `ROOT_FOLDER_NAME` | `제이식스미디어 계약서` (내 드라이브에 자동 생성) |
| `SHEET_NAME` | `계약 대장` |
| `COMPANY_NAME` / `COMPANY_EMAIL` | 제이식스미디어 / j6_media@naver.com |
| `MANAGER_EMAIL` | 큰길브리지 관리 메일(서명본 사본 수신, `''` 로 끌 수 있음) |
| `ALLOW_RESIGN` | false (서명된 계약 재서명 금지) |
| `BOX_FILE` / `BOX_MAX` | `견적서-보관함.json` / 100 |
| `SCHED_FILE` / `SCHED_MAX` | `행사일정.json` / 300 |
| `VERSION` | `2026-10-02b` — 고칠 때마다 올린다 |

### 스크립트 속성

| 속성 | 뜻 |
|---|---|
| `BOX_PW` | 대표 암호 — 견적서 보관함, 일정, `?admin=1` 화면 잠금, office.html 잠금 |
| `CREW_PW` | 직원 암호 — 일정 · 체크리스트만 (보관함 · 관리자 화면은 안 열림) |

### GET

| 요청 | 응답 |
|---|---|
| `…/exec` | `{ ok, service:'j6-contract', version, box:'ready'|'no-pw', sched:'ready'|'no-pw', time }` — 배포 · 속성 확인용 |
| `…/exec?id=<ID>` | 계약 조회 `{ ok, id, status:'pending'|'signed', contract, hash, (signed면) signedAt, signer, pdfUrl, sig }` |

### POST `action`

| action | 보낼 것 | 하는 일 · 응답 |
|---|---|---|
| `ping` | — | `{ok:true, version:1}` |
| `store` | `contract`(cl · ev 필수), `hash` | 드라이브 `_data/<ID>.json` 저장, 대장에 「발송」 → `{ok, id}` |
| `sign` | `id`, `contract`, `sig`(data:image/png;base64), `signer{name,tel,email}`, `html`, `hash`, `ts`, `ua`, `tz`, `to{company,customer}`, `subject` | HTML→PDF(연도 폴더, 링크 보기 공유), 서명 PNG 보관, SHA-256 재계산 · 비교, 메일(회사 · 관리 · 고객 · 서명자, PDF 첨부), 대장 「서명완료」 → `{ok, id, pdfUrl, hash, hashMatch, mailedTo}`; 이미 서명됐으면 `{already:true}` |
| `boxList` | `pw`(BOX_PW), 선택 `목록[]` | 보관함 읽기. 목록을 같이 보내면 코드 기준으로 합쳐 저장 → `{ok, 목록}`. **admin-lock.js 가 암호 확인용으로도 씀** |
| `boxPut` | `pw`, `항목{코드, 제목, 고객, 행사일, 금액, 항목(품목 수), 때}` | 같은 `코드` 는 최신 것 하나만 |
| `boxDel` | `pw`, `코드` | 빼기 |
| `schedList` | `pw`(CREW_PW 또는 BOX_PW) | 일정 목록(날짜 오름차순, 날짜 없는 것 맨 뒤) |
| `schedSave` | `pw`, `누가`, `행사{id?, 제목*, 날짜, 끝날짜, 집합, 시작, 장소, 고객, 담당, 우리담당, 인원, 비고, 끝났나, 견적코드, 항목[]?}` | 개요 덮어쓰기. 항목을 보내면 항목도 통째 교체(최대 200). `만든때 · 고친때 · 고친이` 기록 |
| `schedCheck` | `pw`, `id`, `항목`(품목 id), `됨`, `누가` | 체크 하나만 바꿈(동시 수정 충돌 방지) |
| `schedDel` | `pw`, `id` | 행사 삭제 |

품목(체크리스트 한 줄): `{ id, 이름*, 메모, 출처, 됨, 누가, 때 }`. 글자 길이는 서버가 잘라 낸다(`글_()`).
모든 POST 는 `LockService.getScriptLock()` 20초 대기 안에서 돈다.

### 드라이브 구조

```
제이식스미디어 계약서/
  _data/<ID>.json           계약 원문 · 상태 · 서명 메타 (링크가 읽음 — 지우지 말 것)
  _data/견적서-보관함.json
  _data/행사일정.json
  <연도>/계약서_<번호>_<고객>_<행사>.pdf, 서명_<번호>_<이름>.png
  계약 대장 (스프레드시트)
```

권한: 드라이브 · 스프레드시트 · 메일(MailApp, 무료 계정 하루 100통 한도 — README).

---

## 3. 갤러리(사진 업로드) 서버 `apps-script/gallery/Code.gs`

- 주소: `https://script.google.com/macros/s/AKfycbz1JKFYh-cUS-GmPCEB26U4rJ-IWmLVFlncxKE4pKO843W1bY-NAnU5rmxupGCXAAisIw/exec`
- 박힌 곳: `upload.html 서버주소_기본`(이식 결과), `office.html` 상태 핑. → `port_docs.py GALLERY_URL`.
- 드라이브를 쓰지 않는다. GitHub Contents API 로 레포 `photos` 가지에 직접 쓴다(원본은 폰에만 남음).

### 스크립트 속성

| 속성 | 뜻 |
|---|---|
| `UPLOAD_PW` | 사진 올리기 비밀번호 |
| `GITHUB_TOKEN` | fine-grained PAT, 레포 `brizymedia/j6media` 만, `Contents: Read and write` |
| `GITHUB_REPO` | `brizymedia/j6media` |

편집기에서 `권한받기`(UrlFetch 권한) · `점검`(속성 있음/없음 + photos 가지 사진 수 로그) 함수를 실행해 확인.

### GET

`…/exec` → `{ ok:true, 이름:'제이식스미디어 사진 업로드 서버', 브랜치:'photos', 설정완료:{UPLOAD_PW, GITHUB_TOKEN, GITHUB_REPO: true/false} }`

### POST `action` (모두 `pw` = UPLOAD_PW 필요)

| action | 보낼 것 | 하는 일 |
|---|---|---|
| `photo` | `eventId`(예 `20260824-4ll6`), `index`, `cat`(slug), `event{name,date,place,…}`, `web`(base64 JPEG) | `photos/<cat>/<eventId>-<001>.jpg` 커밋 → `{ok, path}` |
| `cover` | `eventId`, `square`, `wide`(base64) | `photos/_cover/<id>-sq.jpg`(1080²) · `<id>-wide.jpg`(1200×630) |
| `finish` | `photos[]`, `cat` | `photos/photos.json` 앞에 추가(path 중복 무시), 새 칸이면 항목 생성, 개수 맞추기, 저장 후 `repository_dispatch: photos-updated` 신호 → `{ok, added, total, 갤러리갱신}` |
| `edit` | `old{event,date}`, `new{event*,date,place,desc,cat}`, `cat` | event+date 가 같은 사진들의 정보를 바꾸고 caption=event. cat 이 바뀌면 값만 옮김(파일은 그대로) → `{ok, changed, moved}` |
| `delete` | `paths[]` | 파일 삭제(이미 없으면 지운 것으로) + 목록에서 제거, 개수 맞추기 |

`finish · edit · delete` 는 잠금(`잠그고`) 안에서 — 동시에 두 기기가 올리면 「다른 업로드가 처리 중」.

### photos.json 한 장 (upload.html 이 보내는 필드)

`{ path, cat, event, date, place, caption, desc }` — app.js 는 `path`(필수) · `event` · `cat` · `place` · `date` 를 읽어
`{u: jsDelivr 주소, t: event, o: '분야 · 장소 · 날짜', c: cat}` 로 바꿔 WORKS 앞에 붙인다. 파일 최상위는 `{ updated, categories[], photos[] }` (서버 `목록읽기()` 기준, 실제 원격 파일 내용은 확인 필요).

### 주의

- `repository_dispatch` 를 받아 줄 워크플로가 이 레포에 **없다**(큰길이벤트용 설계). 신호 실패는 무시되고, 이 사이트는 photos.json 을 직접 읽으므로 상관없다.
- README 의 `gallery.html` · `scripts/prepare-gallery-photos.mjs` · 「6시간마다 자동 작업」도 큰길이벤트 이야기다.
- 토큰 만료(401) · 권한 부족(403) · 레포 오타(404)는 README 문제 해결 표 참고.

---

## 배포 규칙 (두 서버 공통)

1. script.google.com → 새 프로젝트 → `Code.gs` 붙여 넣기 → 저장.
2. 스크립트 속성 넣기(위 표). 갤러리는 `권한받기` · `점검` 실행.
3. 배포 → 새 배포 → 유형 **웹 앱**, **다음 사용자로 실행: 나**, **액세스: 모든 사용자** → 권한 승인.
4. 받은 `/exec` 주소를 `tools/port_docs.py` 에 넣고 `python tools/port_docs.py` (원본 레포 필요) → push.
5. 코드 수정 뒤에는 **배포 관리 → 연필 → 버전: 새 버전 → 배포**. 「새 배포」를 만들면 주소가 바뀌어 4단계를 다시 해야 한다.
6. 확인: `/exec` 를 브라우저로 열기(계약: `box`·`sched` 가 `ready`, 갤러리: `설정완료` 전부 true), `office.html` 의 「서버 연결 상태」.
