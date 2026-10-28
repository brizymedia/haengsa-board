# 백엔드 — Apps Script 2개 + 공용 문의 서버

배포 계정: 형님(큰길브리지) 구글 계정(README). 웹 앱 배포: **실행 = 나, 액세스 = 모든 사용자**.
코드를 고치면 「배포 → 배포 관리 → 연필 → 버전: 새 버전 → 배포」(새 배포를 만들면 `/exec` 주소가 바뀐다).
비밀값(암호 · 토큰)은 **스크립트 속성에만**. Code.gs 가 「README.md 참고」라고 하지만 `apps-script/*/README.md` 는 이 레포에 없다.
2026-10-28 현재 두 서버 주소는 `port_docs.py` 에서 빈칸(`CONTRACT_URL = ''`, `GALLERY_URL = ''`) — 배포 여부 확인 필요.

## 1. 공용 문의 서버 (레포 밖, 큰길브리지 소유)

- 주소는 `assets/app.js FORM_ENDPOINT` · `assets/edit.js SEND_ENDPOINT` · `quote.html 문의서버` 에 같은 `/exec` 가 들어 있다(코드: README 가 말하는 `ai-make/문의폼-AppsScript-코드.gs`, 이 레포에 없음).
- 요청: `POST text/plain` JSON `{name, phone, email, service, message, page, at, website}` → `{ok:true}`.
- `service` 머리: 문의 폼 `[이벤트와 교육연구소] <문의 종류>`, 견적 `[이벤트와 교육연구소] 자동 견적서 문의`, 수정 모드 `이벤트와 교육연구소 홈페이지 수정 요청`.
- README 오픈 체크리스트 5: 이 서버에 대표 메일 수신을 추가해야 한다 — 그 전에는 **큰길브리지 메일로만 간다**.

## 2. 계약 서버 `apps-script/contract/Code.gs` (537줄, service `edu-contract`, VERSION `2026-10-13a`)

| 요청 | 하는 일 |
|---|---|
| `GET` | 상태 `{ok, service, version, box:'ready'|'no-pw', sched:'ready'|'no-pw', time}` (office.html 이 읽음) |
| `GET ?id=ID` | 계약서 조회(고객 화면) |
| `POST store {contract, hash}` | 계약 저장 → 짧은 ID |
| `POST sign {id, contract, sig, signer, ts, hash, html, to, subject}` | 서명 접수 → PDF → 드라이브 → 메일 → 대장 기록 |
| `POST ping` | 상태 |
| `POST boxList {pw, 목록?}` · `boxPut {pw, 항목}` · `boxDel {pw, 코드}` | 견적서 보관함(`BOX_PW`). **boxList 는 관리자 잠금 확인에도 쓰인다**(admin-lock.js · office 잠금) |
| `POST schedList · schedSave · schedCheck · schedDel {pw, …}` | 행사 일정(`BOX_PW` 또는 `CREW_PW`) |

- 설정 상수: `ROOT_FOLDER_NAME '이벤트와 교육연구소 계약서'`(내 드라이브 자동 생성) · `SHEET_NAME '계약 대장'` · `COMPANY_EMAIL` = 대표 메일 · `MANAGER_EMAIL` = 큰길브리지 관리 계정(사본, 빼려면 `''`) · `ALLOW_RESIGN false` · 보관함 `견적서-보관함.json`(최대 300) · 일정 `행사일정.json`(최대 300) · 보관함 메일 재수집 10분.
- 스크립트 속성: **`BOX_PW`**(대표 · 보관함 · 관리자 모드) · **`CREW_PW`**(직원 · 일정만). `BOX_MAIL_AT` 은 서버가 스스로 씀.
- 모든 POST 는 `LockService` 20초 대기.

## 3. 갤러리 서버 `apps-script/gallery/Code.gs` (484줄)

| 요청 (모두 `pw` = `UPLOAD_PW` 필요) | 하는 일 |
|---|---|
| `GET` | `{ok, 이름, 브랜치:'photos', 설정완료:{UPLOAD_PW, GITHUB_TOKEN, GITHUB_REPO}}` |
| `photo` | 사진 한 장 → photos 가지 `photos/…` |
| `cover` | 대표(정사각) 이미지 |
| `finish` | `photos/photos.json` 갱신(잠금) + `repository_dispatch photos-updated` 시도 |
| `edit` · `delete` | 사진 정보 수정 · 삭제 |
| `notice-list` · `notice-save` · `notice-delete` | **공지**(port_docs 가 `NOTICE_GS` 로 덧붙인 7장) → `photos/notices.json` |

- 스크립트 속성: **`UPLOAD_PW`** · **`GITHUB_TOKEN`**(Contents 쓰기) · **`GITHUB_REPO`** = `brizymedia/edu-event`.
- 편집기에서 돌리는 함수: `권한받기()`(UrlFetch 권한) · `점검()`(속성 · photos 가지 확인 로그).
- 공지 목록 읽기도 비밀번호가 필요하다(공개 화면은 서버가 아니라 raw.githubusercontent 의 notices.json 을 직접 읽는다).
- `repository_dispatch` 를 받는 워크플로는 없다(큰길 원본의 gallery.html 재생성용 흔적). 포트폴리오는 photos.json 을 직접 읽으므로 지장 없음.
- office.html 상태 칸은 `설정완료 === false` 일 때만 「설정 미완료」를 띄우는데 서버는 객체를 주므로 속성이 빠져도 「연결됨」으로 보인다 — 실제 점검은 `점검()` 으로.

## 4. photos 고아 가지

```
photos (orphan)
└─ photos/
   ├─ photos.json    {photos:[{path, cat, event, place, date, …}], categories:[…]}   ← 갤러리 서버가 씀, 포트폴리오가 읽음
   ├─ notices.json   {updated, notices:[{id,d,t,b,n}]}                          ← 공지 관리자가 씀, index · notice 가 읽음
   └─ <사진 파일들>                                                            ← jsDelivr gh/brizymedia/edu-event@photos/ 로 서비스
```
README: 빈 `photos/photos.json` · `photos/notices.json` 으로 미리 만들어 둔다. 클론에 없어서 존재 여부 확인 필요.
photos.json 의 정확한 필드는 큰길 원본 upload.html · Code.gs `목록갱신()` 기준(app.js 는 `path · cat · event · place · date` 만 읽는다).

## 5. 연결 순서

1. 계약 서버 새 프로젝트 → Code.gs 붙여넣기 → 속성 `BOX_PW` · `CREW_PW` → 웹 앱 배포 → `/exec`.
2. 갤러리 서버 새 프로젝트 → Code.gs → 속성 3개 → `권한받기()` → 배포 → `/exec` → `점검()`.
3. `port_docs.py` 에 `CONTRACT_URL` · `GALLERY_URL` → `python tools/port_docs.py <큰길이벤트 레포>` → `python tools/build_site.py` → `node scripts/build-blog.mjs`.
4. 확인: `office.html` 잠금 → 대표 암호로 열림 · 상태 칸 초록, `quote.html?admin=1` 잠김, `notice-admin.html` 로그인 · 공지 저장 → 몇 분 뒤 대문 공지, `upload.html` 테스트 사진 → 포트폴리오 맨 앞.
