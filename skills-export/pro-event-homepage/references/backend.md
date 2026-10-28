# 백엔드 — Google Apps Script 서버 3개 + 바깥 서비스

사이트 자체는 정적 파일뿐(GitHub Pages). 서버 일은 전부 Google Apps Script 웹앱이 한다.
**비밀번호·토큰은 코드·문서·카톡·메일에 적지 않는다. 각 스크립트의 「프로젝트 설정 → 스크립트 속성」에만.**

## 주소 (공개 페이지에 이미 박혀 있는 웹앱 주소)

| 서버 | 웹앱 주소 | 쓰는 곳 | 코드 |
|---|---|---|---|
| 공용 문의 서버 | `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec` | `assets/app.js` `FORM_ENDPOINT`, `quote.html` `문의서버`, `contract.html`(서명 대체 경로) | **이 레포에 없음** — 큰길브리지가 여러 고객사와 같이 쓰는 서버. 요청의 `page` 주소에 든 레포 이름(pro-event)으로 회사를 구분(app.js 259행 주석) |
| 계약 서버 | `https://script.google.com/macros/s/AKfycbxRVcKWlhn8f3MansjmczcSKXTNyLvWfF99d9lhJDhC4SQcX5-CISQ6s0SGYGFL_L7gRQ/exec` | quote(저장함)·contract·statement(잠금)·schedule·office·admin-lock | `apps-script/contract/Code.gs` (VERSION `2026-10-02b`) |
| 갤러리(사진) 서버 | `https://script.google.com/macros/s/AKfycbzPv-ZoZVhBWVabYWhdsm1vZ39mFBe8UfhoxDkwgnrEHSbZKodJE4t9lkuI3yqI5OZr/exec` | upload.html, office.html 상태 표시 | `apps-script/gallery/Code.gs` |

주소의 원본 값은 `tools/port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL`(주석: 2026-10-03 배포). 주소를 바꾸면 거기 넣고 `python tools/port_docs.py` 를 다시 돌려야 모든 업무 화면에 퍼진다.
`assets/app.js` 의 `FORM_ENDPOINT` 와 `quote.html` 의 `문의서버` 는 따로 적혀 있다(port_docs 가 문의 서버 주소는 치환하지 않음 — 확인 필요: 원본 큰길 레포에 같은 주소가 있는지).

## 계약 서버 (apps-script/contract)

| 요청 | 하는 일 |
|---|---|
| `GET` (파라미터 없음) | 상태 `{ok, service:'pro-contract', version, box:'ready'|'no-pw', sched:'ready'|'no-pw', time}` — office.html 이 이걸로 연결 상태 표시 |
| `GET ?id=ID` | 계약서 조회(손님 화면) |
| `POST {action:'store', contract, hash}` | 저장, 짧은 ID 발급 |
| `POST {action:'sign', id, contract, sig, signer, ts, hash, html, to, subject}` | 서명 접수 → PDF → 드라이브 → 메일 → 대장 |
| `POST {action:'ping'}` | 상태 |
| `POST {action:'boxList', pw, 목록?}` / `boxPut` / `boxDel` | 견적서 보관함(최대 100). **`boxList` 는 관리자 암호 확인 용도로도 쓰인다**(admin-lock.js, admin_gate.py) |
| `POST {action:'schedList'|'schedSave'|'schedCheck'|'schedDel', pw, …, 누가}` | 행사 일정(최대 300). `CREW_PW` 로도 열림 |

- 설정 상수(Code.gs 26~36행): `ROOT_FOLDER_NAME='프로이벤트 계약서'`, `SHEET_NAME='계약 대장'`, `COMPANY_NAME`, `COMPANY_EMAIL`(회사 메일), `MANAGER_EMAIL`(관리하는 큰길브리지 사본 — 빼려면 `''`), `ALLOW_RESIGN=false`, `BOX_FILE`, `BOX_MAX=100`, `SCHED_FILE`, `SCHED_MAX=300`, `VERSION`.
- 스크립트 속성: `BOX_PW`(대표 = 보관함·관리자 화면·문서함), `CREW_PW`(직원 = 일정만).
- 데이터: 드라이브 `프로이벤트 계약서/_data/ID.json`(지우면 링크가 죽음), `_data/견적서-보관함.json`, `_data/행사일정.json`, `연도/계약서_….pdf`, `서명_….png`, 스프레드시트 `계약 대장`.
- 모든 POST 는 `LockService` 로 20초 잠금.
- 권한: 드라이브·스프레드시트·메일. Gmail 무료 발송 한도 100통/일(README).

## 갤러리 서버 (apps-script/gallery)

| 요청 | 하는 일 |
|---|---|
| `GET` | `{ok, 이름, 브랜치:'photos', 설정완료:{UPLOAD_PW, GITHUB_TOKEN, GITHUB_REPO}}` |
| `POST {pw, action:'photo', cat, event, eventId, index, web}` | `photos/<cat>/<eventId>-NNN.jpg` 를 photos 브랜치에 커밋 |
| `action:'cover'` | 대표 썸네일 2장 저장 |
| `action:'finish'` | `photos/photos.json` 앞에 새 사진 추가(중복 무시) + `repository_dispatch`(event_type `photos-updated`) 신호 |
| `action:'edit'` / `'delete'` | 행사 정보 수정(cat 값만 바꿈) / 사진 삭제 |

- 스크립트 속성: `UPLOAD_PW`, `GITHUB_TOKEN`(fine-grained, 이 레포만, Contents: Read and write), `GITHUB_REPO=brizymedia/pro-event`.
- 드라이브 안 씀. 편집기에서 `권한받기` → `점검` 함수 실행으로 설치 확인.
- `photos.json` 은 읽고-고치고-쓰기라 `LockService.tryLock(30000)` 로 한 번에 하나만.
- `repository_dispatch` 를 받는 워크플로는 **이 레포에 없다**(.github 없음). 대문은 photos.json 을 직접 읽으므로 없어도 동작한다. 신호 응답이 204 가 아니면 「자동 갱신 대기」만 뜬다.

## 배포 규칙 (두 서버 공통, README 그대로)

1. script.google.com 새 프로젝트 → `Code.gs` 붙여넣기 → 스크립트 속성 넣기.
2. 배포 → 새 배포 → 웹 앱, **다음 사용자로 실행: 나**, **액세스: 모든 사용자**(손님 폰에서 열려야 함).
3. **코드를 고친 뒤에는 「배포 관리 → 연필 → 버전: 새 버전 → 배포」.** 「새 배포」를 만들면 주소가 바뀐다 → 모든 화면의 주소를 다시 바꿔야 함.
4. 「저장」만 해서는 웹앱에 반영되지 않는다.
5. 배포 확인: 주소를 브라우저로 열어 상태 JSON(`box:"ready"` 등) 확인. office.html 의 「서버 연결 상태」도 같은 것을 본다.

## 바깥 서비스

| 무엇 | 주소 | 비고 |
|---|---|---|
| 유입 통계 | `https://www.ai-make.co.kr/stats/stats.js` `data-site="pro"` | 큰길브리지 유입 서버. index·quote·contract·office 등 머리에 |
| FormSubmit | `https://formsubmit.co/ajax/<메일>` | quote.html 문의 서버 실패 시 대체 |
| 사진 목록 | `https://raw.githubusercontent.com/brizymedia/pro-event/photos/photos/photos.json` | app.js, upload.html |
| 사진 파일 | `https://cdn.jsdelivr.net/gh/brizymedia/pro-event@photos/` | jsDelivr 캐시 |
| 유튜브 | `youtube-nocookie.com/embed/<id>`, 썸네일 `img.youtube.com/vi/<id>/maxresdefault.jpg` | |
| 글꼴 | Google Fonts(Unbounded), jsDelivr(Pretendard), code.iconify.design(업무 화면 아이콘) | |

확인 필요: 클론에는 `main` 브랜치만 있어 `photos` 브랜치가 실제로 있는지, photos.json 이 비었는지는 이 클론으로 확인하지 못했다.
