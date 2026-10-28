# 백엔드 — Google Apps Script 3개

비밀값(암호 · 토큰)은 **스크립트 속성에만** 있고 코드 · 문서 · 이 스킬 어디에도 없다. 아래에는 공개 주소만 적는다.

## 서버 목록

| 이름 | 웹 앱 주소(/exec) | 코드 | 쓰는 곳 |
|---|---|---|---|
| 공용 문의 서버 | `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec` | **이 레포에 없음**(큰길브리지와 같이 씀) | `assets/app.js FORM_ENDPOINT` · `quote.html 문의서버` · `contract.html 문의서버` |
| 계약 서버 `hd-contract` | `https://script.google.com/macros/s/AKfycbztMKCIMH6nJmTXdqq4cuDvLi4diPSGuJRag6uAeukUf8wJGyMAkqFX3T4ZbHihIRWVcg/exec` | `apps-script/contract/Code.gs` | contract · quote 저장함 · schedule · admin-lock.js · office.html 잠금/상태 |
| 갤러리 서버 | `https://script.google.com/macros/s/AKfycbwL8NthOvri0RIuY0IBRtXUeU_Hk36e76Ie6dXchYdaPDjn-x1eiPho1-7xqLTVrhtA/exec` | `apps-script/gallery/Code.gs` | upload.html · office.html 상태 |

계약 · 갤러리 주소는 `tools/port_docs.py` `CONTRACT_URL` · `GALLERY_URL` 에 들어 있고(주석: 계약 서버 2026-10-03 배포), port_docs.py 가 각 화면에 박아 넣는다.
README 의 「배포 전」 표기는 낡은 것. 실제 응답(ready/no-pw)은 office.html 상태 칸에서 확인 — 이 분석에서는 호출하지 않았다(확인 필요).

## 공용 문의 서버 (요청 형식만 — 코드에서 확인한 것)

- `POST`, `Content-Type: text/plain;charset=utf-8`(CORS 사전 요청을 피하려는 형식), 본문 JSON.
- 대문 폼이 보내는 칸: `name`(기관이 있으면 「이름 (기관)」) · `tel` · `phone` · `org` · `type` · `date` · `people` · `msg` · `message`(정리된 전문) · `service`(「[HD기획] ○○ 문의」) · `at`(KST) · `page` · `website:''`.
- 견적서가 보내는 칸: `name phone email service message at page website`.
- 응답 `{ ok: true }` 일 때만 성공으로 친다. 메일은 대표(16zone@hanmail.net)와 큰길브리지로 간다(app.js 주석 · office.html).

## 계약 서버 `apps-script/contract/Code.gs`

설정 상수: `ROOT_FOLDER_NAME 'HD기획 계약서'` · `SHEET_NAME '계약 대장'` · `COMPANY_NAME` · `COMPANY_EMAIL '16zone@hanmail.net'` · `MANAGER_EMAIL`(큰길브리지 관리 계정, 사본 수신, 빼려면 `''`) · `ALLOW_RESIGN false` · `BOX_FILE '견적서-보관함.json'` · `BOX_MAX 100` · `SCHED_FILE '행사일정.json'` · `SCHED_MAX 300` · `VERSION '2026-10-02b'`.

| 요청 | 하는 일 | 암호 |
|---|---|---|
| `GET` | `{ok, service:'hd-contract', version, box:'ready'|'no-pw', sched:'ready'|'no-pw', time}` | — |
| `GET ?id=<ID>` | 계약 원문 · 상태 읽기(고객 짧은 링크) | — |
| `POST ping` | `{ok, version:1}` | — |
| `POST store` | 계약 저장 → 짧은 ID 발급(`_data/ID.json`) | — |
| `POST sign` | 서명 저장 · PDF 생성(드라이브 `연도/`) · 회사 + 관리자 + 고객 메일 · 대장 기록 | — |
| `POST boxList` | 보관함 목록(올릴 `목록` 이 있으면 합침) — **관리자 잠금 확인에도 씀** | `BOX_PW` |
| `POST boxPut` / `boxDel` | 보관함 넣기 / 빼기 | `BOX_PW` |
| `POST schedList` / `schedSave` / `schedCheck` / `schedDel` | 행사 일정 | `CREW_PW` 또는 `BOX_PW` |

스크립트 속성: `BOX_PW`(대표 · 보관함 · 관리자 모드), `CREW_PW`(직원 · 일정만).
데이터: 내 드라이브 `HD기획 계약서/` — `_data/ID.json`(지우면 링크가 죽음) · `_data/견적서-보관함.json` · `_data/행사일정.json` · `연도/계약서_….pdf` · `서명_….png` · 스프레드시트 `계약 대장`.
메일 한도: 무료 Gmail 하루 100통(README).

## 갤러리 서버 `apps-script/gallery/Code.gs`

- 구글 드라이브를 **쓰지 않는다**. 1600px 사본만 GitHub `brizymedia/hd-event` 의 **`photos` 가지** `photos/<분류>/<행사ID>-<번호>.jpg` 로 올린다. 대표 썸네일은 `photos/_cover/<id>-sq.jpg` · `-wide.jpg`. 목록은 `photos/photos.json`(새 사진이 앞으로).
- 요청: `GET` 상태(`설정완료` 등) / `POST photo · cover · finish · edit · delete`. finish · edit · delete 는 잠금(`LockService`)으로 동시 업로드를 막는다(「다른 업로드가 처리 중입니다」).
- 스크립트 속성: `UPLOAD_PW` · `GITHUB_TOKEN`(fine-grained, 이 레포만, Contents Read and write) · `GITHUB_REPO`(`brizymedia/hd-event`).
- 편집기에서 실행하는 함수: `권한받기`(UrlFetch 권한 승인) · `점검`(속성 있음/없음 · photos 가지 연결 로그).
- `갤러리다시만들기()` 는 `repository_dispatch` `photos-updated` 를 보낸다. **이 레포에는 그 이벤트를 받는 워크플로가 없다**(README 의 Actions 「갤러리 페이지 · 사이트맵 자동 갱신」과 `scripts/prepare-gallery-photos.mjs` 는 큰길이벤트에서 옮겨 온 문구). portfolio.html 이 photos.json 을 직접 읽으므로 사진 표시는 이것과 상관없다.

## 배포 규칙 (두 README 공통)

1. https://script.google.com → 새 프로젝트 → `Code.gs` 붙여넣기 → 이름 저장.
2. (갤러리) 스크립트 속성 3개 → `권한받기` 실행 → `점검` 실행. (계약) 스크립트 속성 `BOX_PW` · `CREW_PW`.
3. 배포 → 새 배포 → 웹 앱 → **다음 사용자로 실행: 나 · 액세스: 모든 사용자** → 승인(고급 → 안전하지 않은 페이지로 이동 → 허용).
4. 웹 앱 주소를 `tools/port_docs.py` 의 `CONTRACT_URL` / `GALLERY_URL` 에 넣고 `python tools/port_docs.py <큰길이벤트 레포>` → 커밋.
5. **코드를 고치면** 배포 → 배포 관리 → 연필 → 버전: 새 버전 → 배포. 새 배포를 만들면 주소가 바뀌어 모든 화면을 다시 생성해야 한다. 계약 서버는 `VERSION` 을 올려 GET 응답으로 반영을 확인.
6. 계약 서버 GET 이 `"box":"ready"` 면 보관함 준비 완료, `"no-pw"` 면 속성 없음.
7. 주소를 잃으면 배포 → 배포 관리에서 다시 본다.

## 문제 해결 요약

| 증상 | 확인 |
|---|---|
| 「서버 응답을 읽을 수 없습니다」 / 「서버가 이상한 답」 | 액세스가 「모든 사용자」인지, 새 버전으로 재배포 |
| 고객 폰 「계약서를 불러오지 못했습니다」 | 문자에서 링크가 잘렸는지 → 카톡 · 메일로 |
| 메일이 안 옴 | 스팸함, Gmail 일일 한도 |
| 깃허브 저장 401 / 403 / 404 | 토큰 만료 · 권한(Contents) · `GITHUB_REPO` 오타 |
| 사진은 올라갔는데 안 보임 | jsDelivr · raw 캐시(1~2분, portfolio 는 5분 단위 캐시 깨기) → 새로고침 |
| 관리자 화면이 안 열림 | 계약 서버 연결, `BOX_PW` 설정, 기기에 저장된 옛 암호(자동으로 지우고 다시 묻는다) |
