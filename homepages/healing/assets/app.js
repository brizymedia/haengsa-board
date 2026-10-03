/* 힐링엔터테인먼트 홈페이지 — 공통 스크립트 (외부 라이브러리 없음) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ================================================================
     여기부터 사장님 · 큰길브리지가 고치는 곳
     ================================================================ */

  /* 문의 폼 전송처 — 큰길브리지 공용 문의 서버(앱스 스크립트). 서버가 page 주소의 레포 이름(healing-ent)으로 회사를 알아보고
     leehh2153@gmail.com 으로 메일을 보낸다. 비우거나 서버가 실패하면 폰은 문자 앱, PC 는 내용 복사 + 전화 안내. */
  var FORM_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec';
  var SMS_TO = '010-5620-2153';
  var COMPANY = '힐링엔터테인먼트';
  /* 카카오톡 주소 — 지금은 리틀리(litt.ly/healingmc)에 걸린 오픈채팅 주소.
     카카오톡 채널을 따로 만들면 바꾼다 (예: 'https://pf.kakao.com/_xxxxx/chat'). 비우면 카톡 단추가 문의 페이지 안내로 간다. */
  var KAKAO_URL = 'https://open.kakao.com/me/vvipevent';

  /* 유튜브 영상 — 리틀리(litt.ly/healingmc)의 영상 레퍼런스를 옮김.
     id: 유튜브 영상 주소의 11자리, s: true = 쇼츠(세로), c: 분류(VCATS 의 키). 맨 앞에 넣으면 먼저 보인다. */
  var PROMO_ID = 'bIoatdv9iYw';   // 힐링엔터 홍보영상 — 대문 · 영상 페이지 맨 위
  var VCATS = { school: '학교행사 · 수학여행', sportsday: '명랑 운동회', sports: '체육대회', corp: '기업행사', gov: '지자체 · 관공서', abroad: '해외 워크숍', ceo: '최고경영자과정 · 골프', plan: '축제 · 행사 기획' };
  var VIDEOS = [
    { id: 'vX7UPCX1Yi8', t: '3,000명 대형 컨벤션 행사 기획 (TF팀 감독)', c: 'plan' },
    { id: '0Li2oNlEELo', t: '창립 기념식 토탈 기획 · 연출 · 진행 (2018~2024)', c: 'plan' },
    { id: 'JmzffC6j9CM', t: '체육대회 영상 모음', c: 'sports' },
    { id: 'Ak_muW7V_4I', t: '대규모 체육대회 1,000명 — 서울지구 회원가족 체육대회 (오전)', c: 'sports' },
    { id: 'W5jhNvQiMCc', t: '대규모 체육대회 1,000명 — 서울지구 회원가족 체육대회 (오후)', c: 'sports' },
    { id: 'f_rJmpxNNw0', t: '대규모 체육대회 2,000명 — 서울시 공무원 한마음 대회', c: 'sports' },
    { id: 'JIqo4EcOT9k', t: '총동문회 연합 체육대회 — 대한건축사협회 최고위과정', c: 'sports' },
    { id: 'vH9JHKMx8XY', t: '가족과 함께하는 운동회', c: 'sports' },
    { id: 'wHW-2wgG32E', t: '몸빼바지 달리기 계주 하이라이트', c: 'sports', s: true },
    { id: '_Lo2yS8CG0c', t: '운동회 하이라이트 대동놀이 — 떼창', c: 'sportsday' },
    { id: 'okgRprbXDwI', t: '운동회 하이라이트 대동놀이 — 랜덤플레이', c: 'sportsday' },
    { id: '4KR4f01SZHs', t: '운동회 대동놀이 랜덤플레이', c: 'sportsday', s: true },
    { id: 'VI1fjwWhiyw', t: '3일 동안 진행한 실내 운동회 (학년 청백 대항전)', c: 'sportsday' },
    { id: 'LiU0HBBKnRg', t: '고등학교 운동회', c: 'sportsday' },
    { id: 'Ywjebe5nY3Q', t: '다양한 게임 도구로 즐기는 운동회', c: 'sportsday', s: true },
    { id: 'fJmBNfOrNa4', t: '명랑 운동회', c: 'sportsday', s: true },
    { id: 'EftCT64aOAw', t: '수학여행 350명 떼창', c: 'school' },
    { id: 'DMWRK0NsyvY', t: '수학여행 레크리에이션 — 음향 · 조명까지', c: 'school' },
    { id: 'AIjqcuDzVK8', t: '노래 한 곡으로 남기는 학창 시절 추억', c: 'school' },
    { id: 'Y9aFsYtwrqM', t: '청소년 행사 — 댄스 & 합창', c: 'school' },
    { id: 'hyAWxp-HrcI', t: '랜덤플레이 댄스 레크리에이션', c: 'school' },
    { id: 'YkgquM92_pk', t: '고등학교 축제 레크리에이션', c: 'school' },
    { id: 'JoZbZNBtKjY', t: '청소년 행사 레크리에이션 — 대동놀이', c: 'school', s: true },
    { id: 'HeRBY4SNQaQ', t: '청소년 축제 떼창', c: 'school', s: true },
    { id: 'n_Q_zNMjNW8', t: '공무원 워크숍, 분위기가 바뀌는 순간', c: 'gov', s: true },
    { id: 'Qxjkq8KKn8g', t: '국공립 어린이집 보육인 대회', c: 'gov', s: true },
    { id: 'zJZkxKNJsGg', t: '서울지구 회원대회 전체 진행', c: 'gov' },
    { id: 'NKChmjzaU-8', t: '소극적인 참가자도 적극적으로 — 참여형 진행', c: 'gov' },
    { id: '5vd6DY4euCU', t: '남성 참가자들의 자발적인 댄스', c: 'gov' },
    { id: 'jHJ-0PXOVUI', t: '10대부터 80대까지 함께 즐기는 캠프', c: 'gov' },
    { id: '4gv95zFG4GU', t: '임원이 노래하면 생기는 일', c: 'corp' },
    { id: 'sEcArfuz-XU', t: '보험회사 행사 — 하이라이트 댄스 신고식', c: 'corp', s: true },
    { id: 'T8aOXlwAS2I', t: '보험회사 행사 — 단체 아파트 게임', c: 'corp', s: true },
    { id: 'HPlsIC13qKQ', t: '보험회사 여성 조직 행사 — 마지막 하이라이트', c: 'corp', s: true },
    { id: 'xMtX37708TA', t: '영업 조직 제주도 워크숍 — 노래방 레크리에이션', c: 'corp', s: true },
    { id: 'hHGcPma4fCE', t: '영업 조직 대관 행사 진행', c: 'corp', s: true },
    { id: 'qosb2fdEysU', t: '어린이집 선생님 해외 연수 레크리에이션', c: 'abroad' },
    { id: '3SQJGKG5Ycc', t: '동남아 해외 초대 행사 — 단독 대관 파티', c: 'abroad' },
    { id: 'WsNublJEim4', t: '크루즈 선상 파티 진행', c: 'abroad' },
    { id: 'ITQsUAIYQUA', t: '해외 행사, 함께 즐기는 참여형 진행', c: 'abroad' },
    { id: 'WR8B5auMXZ4', t: '한국프로골프연맹 스포츠 대회 총괄 진행', c: 'ceo' },
    { id: 'hdaEng6joyA', t: '골프대회 시상식 레크리에이션', c: 'ceo' },
    { id: '0nQdUndpGdQ', t: '최고경영자과정 워크숍 레크리에이션', c: 'ceo' },
    { id: 'YmwLSZ9uOaA', t: '소규모 인원도 즐겁게', c: 'ceo' }
  ];

  /* 공지사항 — 맨 앞에 한 줄 추가하면 대문 · 공지 페이지에 바로 뜬다. n: true = NEW 표시, pin: true = 상단 고정 */
  var NOTICES = [
    { d: '2026.09.30', t: '힐링엔터테인먼트 홈페이지를 새로 열었습니다.', n: true, pin: true,
      b: '기업행사 · 체육대회 · 학교행사 · 지역축제 · 워크숍 상담을 홈페이지에서도 받습니다. 견적 문의에 날짜 · 지역 · 인원 · 행사 종류만 남겨 주세요.' },
    { d: '2026.09.30', t: '행사 중에는 전화 연결이 어렵습니다. 카카오톡 · 문자를 남겨 주시면 확인 후 연락드립니다.', n: true,
      b: '상담 가능 시간은 평일 10시~18시입니다. 행사는 연중무휴로 진행합니다.' },
    { d: '2026.09.30', t: '가을 체육대회 · 운동회 · 워크숍 일정 상담을 받고 있습니다.',
      b: '행사 날짜가 정해지면 먼저 알려 주세요. 장소 · 인원 · 진행 시간에 맞춰 프로그램을 함께 구성합니다.' }
  ];

  /* 자료실 — 내려받을 파일. u 는 사이트 안의 파일 경로 */
  var FILES = [
    { d: '2026.09.30', t: '행사 문의 준비표 (인쇄용 PDF)', u: 'assets/files/healing-checklist.pdf', s: 'PDF', b: '날짜 · 장소 · 인원 · 행사 종류 · 진행 시간 · 필요한 장비를 미리 적어 두는 한 장짜리 표입니다.' }
  ];

  /* 현장 사진 (assets/img/works/w1~ ↔ 제목)
     c: school 학교행사 · corp 기업·단체 · fest 지역축제 · stage 무대·음향 */
  var WORKS = [
    {"f": "w1.webp", "t": "연합 워크숍, MC 이현호 진행", "o": "워크숍 · 체육관", "c": "corp"},
    {"f": "w2.webp", "t": "전교생이 함께하는 운동회 준비 체조", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w3.webp", "t": "상권 활성화 축제 무대 공연", "o": "지역축제 · 서울 동대문구", "c": "fest stage"},
    {"f": "w4.webp", "t": "팀 대항 과녁 게임", "o": "워크숍 · 체육관", "c": "corp"},
    {"f": "w5.webp", "t": "대형 공 굴리기 · 단체 게임", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w6.webp", "t": "MC와 함께하는 운동장 게임", "o": "학교 체육대회 · 운동장", "c": "school"},
    {"f": "w7.webp", "t": "동별 팀 응원 · 오프닝", "o": "워크숍 · 체육관", "c": "corp"},
    {"f": "w8.webp", "t": "거리 축제 음향 · 관람석 운영", "o": "지역축제 · 서울 동대문구", "c": "fest stage"},
    {"f": "w9.webp", "t": "만국기 아래 단체 줄다리기 준비", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w10.webp", "t": "팀별 대형으로 모인 참가자들", "o": "워크숍 · 체육관", "c": "corp"},
    {"f": "w11.webp", "t": "무대 앞 주민 관람석", "o": "지역축제 · 서울 동대문구", "c": "fest"},
    {"f": "w12.webp", "t": "어깨동무로 함께 움직이는 대동놀이", "o": "학교 체육대회 · 운동장", "c": "school"},
    {"f": "w13.webp", "t": "색색의 경기용품으로 꾸민 경기장", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w14.webp", "t": "축제 무대 음향 · 조명 세팅", "o": "지역축제 · 음향 · 조명", "c": "fest stage"},
    {"f": "w15.webp", "t": "내빈석 · 에어 아치 세팅", "o": "워크숍 · 준비", "c": "corp"},
    {"f": "w16.webp", "t": "학년별 이어달리기 · 단체 경기", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w17.webp", "t": "주민 참여 판매 · 체험 부스", "o": "지역축제 · 체험 부스", "c": "fest"},
    {"f": "w18.webp", "t": "운동장 전체를 쓰는 체육대회 구성", "o": "학교 체육대회 · 운동장", "c": "school"},
    {"f": "w19.webp", "t": "마지막 단체 경기 준비", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w20.webp", "t": "축제 무대와 음향 장비", "o": "지역축제 · 무대", "c": "fest stage"},
    {"f": "w21.webp", "t": "행사 전 체육관 경기장 세팅", "o": "워크숍 · 준비", "c": "corp"},
    {"f": "w22.webp", "t": "반환점 달리기 경기", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w23.webp", "t": "축제장 입구 아치 · 동선", "o": "지역축제 · 서울 동대문구", "c": "fest"},
    {"f": "w24.webp", "t": "본부석 · 음향 · 캐릭터 풍선 세팅", "o": "학교 운동회 · 준비", "c": "school stage"},
    {"f": "w25.webp", "t": "팀별로 모여 앉은 학생들", "o": "학교 체육대회 · 운동장", "c": "school"},
    {"f": "w26.webp", "t": "대형 공과 함께하는 개회 순서", "o": "학교 운동회 · 운동장", "c": "school"},
    {"f": "w27.webp", "t": "팀별 간식 · 물품 준비", "o": "워크숍 · 준비", "c": "corp"},
    {"f": "w28.webp", "t": "운동장 경기 사이 정리 시간", "o": "학교 운동회 · 운동장", "c": "school"}
  ];
  var IMG = 'assets/img/works/';

  /* 행사 이야기 — 네이버 블로그 글 (새 글은 맨 앞에 추가) */
  var BLOG = [
    {"d": "2026.09.21", "t": "학교체육대회, 지금 준비해도 늦지 않을 5단계", "u": "https://blog.naver.com/leehh2153/224419005274"},
    {"d": "2026.09.14", "t": "초등학교운동회업체, 우리 학교에 어울리는 게임과 대동놀이", "u": "https://blog.naver.com/leehh2153/224410849320"},
    {"d": "2026.09.13", "t": "학교체육대회업체, 선택 전 실제 현장부터 비교해보세요", "u": "https://blog.naver.com/leehh2153/224410240152"},
    {"d": "2026.09.11", "t": "초등학교 운동회 업체, 현장 사진으로 살펴보는 5가지 준비 기준", "u": "https://blog.naver.com/leehh2153/224408721656"},
    {"d": "2025.09.24", "t": "서울 노원 어린이집·유치원 운동회 업체, 20년간 3,000회 진행으로 증명된 5가지 이유", "u": "https://blog.naver.com/leehh2153/224019779149"},
    {"d": "2025.09.12", "t": "서울 청소년 행사 사회자·레크레이션, 20년 경력 MC가 공개하는 실패 없는 진행 비법 3가지", "u": "https://blog.naver.com/leehh2153/224005087379"},
    {"d": "2025.07.14", "t": "노원구 초등학교 운동회업체는 기획력 싸움! 20년 노하우 대동놀이로 확실히 다릅니다", "u": "https://blog.naver.com/leehh2153/223932999152"},
    {"d": "2025.07.07", "t": "해외연수 사회자, 기업 워크숍 MC, 팀빌딩 진행자? 이 5가지 체크 없이 섭외하지 마세요", "u": "https://blog.naver.com/leehh2153/223924512794"},
    {"d": "2025.05.19", "t": "관공서 행사MC, 3,000회 진행자가 밝히는 성공 공식", "u": "https://blog.naver.com/leehh2153/223870476811"},
    {"d": "2025.04.17", "t": "중고등학교 레크레이션, 10분 만에 분위기 터진 비법 BEST 3", "u": "https://blog.naver.com/leehh2153/223837170436"},
    {"d": "2025.02.14", "t": "수학여행MC? 저렴한 비용만 보고 선택했다가 망친 사례", "u": "https://blog.naver.com/leehh2153/223760278913"},
    {"d": "2025.01.08", "t": "MC 섭외부터 레크레이션 강사까지, 완벽한 행사 MC 선택 가이드 5가지", "u": "https://blog.naver.com/leehh2153/223718514042"},
    {"d": "2025.01.06", "t": "신년회 사회자 섭외방법과 주의사항", "u": "https://blog.naver.com/leehh2153/223715996954"},
    {"d": "2024.12.27", "t": "전국 국공립 어린이집 보육인대회: 준비 팁과 성공 전략", "u": "https://blog.naver.com/leehh2153/223706695894"},
    {"d": "2024.12.25", "t": "대동놀이와 함께한 500명, 국공립 어린이집 보육인들의 특별한 하이라이트", "u": "https://blog.naver.com/leehh2153/223704847391"},
    {"d": "2024.12.23", "t": "전농동 상권 활성화 축제, 추운 날씨 속 뜨거운 열정의 기록", "u": "https://blog.naver.com/leehh2153/223702427949"},
    {"d": "2024.12.19", "t": "전농동 상권 활성화 프로젝트, 특별한 하루를 즐기다!", "u": "https://blog.naver.com/leehh2153/223698887175"},
    {"d": "2024.12.18", "t": "신년회와 회사 연말파티를 완벽하게! 송년회 사회자 선택 꿀팁", "u": "https://blog.naver.com/leehh2153/223697453432"},
    {"d": "2024.12.16", "t": "송년회의 밤, 기업 연말 행사 사회자와 레크레이션으로 성공적인 모임을 완성하는 꿀팁 3가지", "u": "https://blog.naver.com/leehh2153/223694938674"},
    {"d": "2024.12.11", "t": "기업 연회장에서 송년의 밤 행사, 송영회 전문 사회자가 완벽한 식순으로 마무리하다", "u": "https://blog.naver.com/leehh2153/223689556576"},
    {"d": "2024.12.10", "t": "송년회 식전행사? 레크리에이션 강사만 아는 특별한 아이디어 3가지", "u": "https://blog.naver.com/leehh2153/223688366013"}
  ];

  /* ================================================================ */

  /* ---------- 카톡 단추 ---------- */
  $$('[data-kakao]').forEach(function (a) {
    if (KAKAO_URL) { a.href = KAKAO_URL; a.target = '_blank'; a.rel = 'noopener'; }
    else { a.href = 'contact.html#ways'; a.removeAttribute('target'); var s = a.querySelector('.kstate'); if (s) s.textContent = '채널 준비 중 — 지금은 문자로 남겨 주세요'; }
  });

  /* ---------- 유튜브 영상 (썸네일만 먼저, 누르면 재생 — 페이지가 무거워지지 않게) ---------- */
  var PLAY_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function thumb(id) { return 'https://i.ytimg.com/vi/' + id + '/hqdefault.jpg'; }
  function embed(id) { return 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1'; }
  function watch(v) { return v.s ? 'https://www.youtube.com/shorts/' + v.id : 'https://www.youtube.com/watch?v=' + v.id; }
  function vcard(v) {
    return '<button type="button" class="vcard" data-yt="' + v.id + '"' + (v.s ? ' data-short' : '') + ' data-c="' + v.c + '">' +
      '<span class="th" style="background-image:url(' + thumb(v.id) + ')"><i class="pl">' + PLAY_SVG + '</i>' + (v.s ? '<em>쇼츠</em>' : '') + '</span>' +
      '<small>' + esc(VCATS[v.c] || '') + '</small><b>' + esc(v.t) + '</b></button>';
  }
  // 대표 영상(홍보영상): 그 자리에서 재생
  $$('[data-promo]').forEach(function (el) {
    el.innerHTML = '<span class="th" style="background-image:url(' + thumb(PROMO_ID) + ')"></span><i class="pl big">' + PLAY_SVG + '</i><span class="cap"><small>힐링엔터테인먼트</small><b>홍보영상 보기</b></span>';
    el.addEventListener('click', function () {
      el.innerHTML = '<iframe src="' + embed(PROMO_ID) + '" title="힐링엔터테인먼트 홍보영상" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      el.classList.add('on');
    }, { once: true });
  });
  // 영상 카드 목록: data-vlist="all" 또는 "id,id,id"
  $$('[data-vlist]').forEach(function (box) {
    var want = box.getAttribute('data-vlist'), list = VIDEOS;
    if (want !== 'all') list = want.split(',').map(function (id) { return VIDEOS.filter(function (v) { return v.id === id; })[0]; }).filter(Boolean);
    box.innerHTML = list.map(vcard).join('');
  });
  // 분류 단추
  var vf = $('#vfilters');
  if (vf) {
    vf.innerHTML = '<button class="act" data-f="all" aria-pressed="true">전체 <small>' + VIDEOS.length + '</small></button>' +
      Object.keys(VCATS).map(function (k) { var n = VIDEOS.filter(function (v) { return v.c === k; }).length; return n ? '<button data-f="' + k + '" aria-pressed="false">' + VCATS[k] + ' <small>' + n + '</small></button>' : ''; }).join('');
    vf.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      $$('button', vf).forEach(function (x) { x.classList.toggle('act', x === b); x.setAttribute('aria-pressed', x === b); });
      var f = b.getAttribute('data-f');
      $$('#vgrid .vcard').forEach(function (c) { c.hidden = f !== 'all' && c.getAttribute('data-c') !== f; });
    });
  }
  // 재생 창
  var ym = null;
  function openYT(id, isShort) {
    var v = VIDEOS.filter(function (x) { return x.id === id; })[0] || { id: id, s: isShort, t: '' };
    if (!ym) {
      ym = document.createElement('div'); ym.className = 'ym'; ym.setAttribute('role', 'dialog'); ym.setAttribute('aria-modal', 'true');
      ym.innerHTML = '<div class="ymb"><button type="button" class="x" aria-label="닫기">×</button><div class="fr"></div><p class="meta"><b></b><a target="_blank" rel="noopener">유튜브에서 보기 ↗</a></p></div>';
      document.body.appendChild(ym);
      ym.addEventListener('click', function (e) { if (e.target === ym || e.target.closest('.x')) closeYT(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && ym.classList.contains('on')) closeYT(); });
    }
    ym.classList.toggle('short', !!v.s);
    $('.fr', ym).innerHTML = '<iframe src="' + embed(v.id) + '" title="' + esc(v.t || '영상') + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
    $('.meta b', ym).textContent = v.t || '';
    $('.meta a', ym).href = watch(v);
    ym.classList.add('on'); document.documentElement.style.overflow = 'hidden';
    $('.x', ym).focus();
  }
  function closeYT() { ym.classList.remove('on'); $('.fr', ym).innerHTML = ''; document.documentElement.style.overflow = ''; }
  document.addEventListener('click', function (e) {
    var c = e.target.closest('[data-yt]'); if (!c) return;
    e.preventDefault(); openYT(c.getAttribute('data-yt'), c.hasAttribute('data-short'));
  });

  /* ---------- 머리 · 모바일 메뉴 · 맨 위로 ---------- */
  var hd = $('.hd'), totop = $('#totop');
  function onScroll() {
    var y = window.scrollY;
    if (hd) hd.classList.toggle('stuck', y > 8);
    if (totop) totop.classList.toggle('on', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  var cur = (location.pathname.split('/').pop() || 'index.html');
  $$('.hd .menu a, .sheet nav a').forEach(function (a) { if ((a.getAttribute('href') || '').split('#')[0] === cur) a.classList.add('act'); });

  var burger = $('#burger'), sheet = $('#sheet');
  function closeSheet() { if (!sheet) return; sheet.classList.remove('on'); burger.classList.remove('x'); burger.setAttribute('aria-expanded', 'false'); burger.setAttribute('aria-label', '메뉴 열기'); document.body.style.overflow = ''; }
  if (burger && sheet) {
    burger.addEventListener('click', function () {
      var on = sheet.classList.toggle('on'); burger.classList.toggle('x', on); burger.setAttribute('aria-expanded', on);
      burger.setAttribute('aria-label', on ? '메뉴 닫기' : '메뉴 열기');
      document.body.style.overflow = on ? 'hidden' : '';
    });
    $$('a', sheet).forEach(function (a) { a.addEventListener('click', closeSheet); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet.classList.contains('on')) closeSheet(); });
  }

  /* ---------- 히어로 영상 (폭을 보고 파일 고르기 · 줄인 동작이면 포스터만) ---------- */
  // mp4(H.264)를 못 트는 브라우저는 webm 으로
  function pickSrc(v, w) {
    if (!v.canPlayType('video/mp4; codecs="avc1.42E01E"') && v.getAttribute('data-src-webm')) return v.getAttribute('data-src-webm');
    return w < 900 ? v.getAttribute('data-src-sm') : v.getAttribute('data-src');
  }
  var video = $('#heroVideo'), vbtn = $('#vbtn');
  if (video) {
    if (reduce) { video.removeAttribute('autoplay'); video.preload = 'none'; if (vbtn) vbtn.hidden = true; }
    else {
      var vw = window.innerWidth * Math.min(window.devicePixelRatio || 1, 2);
      video.src = pickSrc(video, vw);
      video.muted = true; video.setAttribute('muted', '');
      var tryPlay = function () { var p = video.play(); if (p && p.catch) p.catch(function () {}); };
      tryPlay(); video.addEventListener('canplay', tryPlay, { once: true });
      video.addEventListener('playing', function () { if (vbtn) vbtn.classList.add('playing'); });
      video.addEventListener('pause', function () { if (vbtn) vbtn.classList.remove('playing'); });
      document.addEventListener('pointerdown', function () { if (video.paused && !video.dataset.userPaused) tryPlay(); }, { once: true });
      if (vbtn) vbtn.addEventListener('click', function () {
        if (video.paused) { video.dataset.userPaused = ''; tryPlay(); } else { video.dataset.userPaused = '1'; video.pause(); }
      });
    }
  }
  /* ---------- 히어로 숫자 올라가기 (20 · 3,000) ---------- */
  if (!reduce) $$('.hero .cnt').forEach(function (el) {
    // rAF 가 멈춘 창(백그라운드 · 미리보기)에서도 끝값에 닿도록 타이머로 돌린다
    var to = +el.getAttribute('data-to'), dur = to > 100 ? 1800 : 1300, t0 = Date.now() + 350;
    el.textContent = '0';
    var id = setInterval(function () {
      var k = Math.max(0, Math.min(1, (Date.now() - t0) / dur)), e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(to * e).toLocaleString('ko-KR');
      if (k >= 1) clearInterval(id);
    }, 30);
  });

  // 영상 페이지의 두 번째 영상도 같은 방식
  $$('video[data-src-sm]:not(#heroVideo)').forEach(function (v) {
    if (reduce) return;
    var w = window.innerWidth * Math.min(window.devicePixelRatio || 1, 2);
    v.src = pickSrc(v, w); v.muted = true;
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); }); }, { threshold: .25 }).observe(v);
  });

  /* ---------- 키워드 띠 (내용을 두 번 이어 붙여 끊김 없이) ---------- */
  $$('.marq .track').forEach(function (t) { t.innerHTML += t.innerHTML; });

  /* ---------- 등장 ---------- */
  var rvEls = $$('.rv');
  function checkRv() {
    var h = window.innerHeight;
    rvEls = rvEls.filter(function (el) { if (el.getBoundingClientRect().top < h * .94) { el.classList.add('in'); return false; } return true; });
  }
  if (reduce) rvEls.forEach(function (el) { el.classList.add('in'); });
  else { window.addEventListener('scroll', checkRv, { passive: true }); window.addEventListener('resize', checkRv); window.addEventListener('load', checkRv); checkRv(); setTimeout(checkRv, 500); }

  /* ---------- 갤러리 (대문 일부 · 현장 갤러리 전체) ---------- */
  /* 현장 갤러리 페이지는 WORKS(위 배열) + 대표님이 upload.html 로 올린 사진(photos 가지의 photos.json)을 합쳐 보여준다.
     UP_CAT 키 = upload.html 의 사진 칸 slug = WORKS 의 c 값 · 갤러리 필터(data-f) */
  var UP_LIST = 'https://raw.githubusercontent.com/brizymedia/healing-ent/photos/photos/photos.json';
  var UP_IMG = 'https://cdn.jsdelivr.net/gh/brizymedia/healing-ent@photos/';
  var UP_CAT = { school: '학교행사', corp: '기업 · 단체 워크숍', fest: '지역축제', stage: '무대 · 음향' };
  function srcT(w) { return w.u || IMG + 'th/' + w.f; }
  function srcP(w) { return w.u || IMG + w.f; }
  function workCard(w, k) {
    return '<figure data-k="' + k + '" data-c="' + esc(w.c) + '" tabindex="0" role="button" aria-label="' + esc(w.t) + ' 크게 보기">' +
      '<img src="' + srcT(w) + '" alt="' + esc(w.t) + '" loading="lazy" width="800" height="600">' +
      '<figcaption><em>' + esc(w.o) + '</em><b>' + esc(w.t) + '</b></figcaption></figure>';
  }
  var gal = $('#gal'), pf = $('#pfGrid'), list = [], figs = [];
  function counts() {
    $$('#filters button').forEach(function (b) {
      var f = b.getAttribute('data-f'), n = f === 'all' ? list.length : list.filter(function (w) { return w.c.split(' ').indexOf(f) >= 0; }).length;
      var c = $('small', b); if (c) c.textContent = n; else b.insertAdjacentHTML('beforeend', '<small>' + n + '</small>');
    });
  }
  function applyFilter() {
    var act = $('#filters .act'), f = act ? act.getAttribute('data-f') : 'all';
    figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
  }
  if (gal) { var pick = (gal.getAttribute('data-pick') || '').split(',').map(Number); list = pick.map(function (k) { return WORKS[k]; }).filter(Boolean); gal.innerHTML = list.map(workCard).join(''); figs = $$('figure', gal); }
  if (pf) {
    list = WORKS.slice(); pf.innerHTML = list.map(workCard).join(''); figs = $$('figure', pf); counts();
    fetch(UP_LIST + '?t=' + Math.floor(Date.now() / 300000), { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (!j || !j.photos || !j.photos.length) return;
      var up = j.photos.filter(function (x) { return x && x.path; }).map(function (x) {
        return { u: UP_IMG + x.path.split('/').map(encodeURIComponent).join('/'), t: x.event || '행사 현장', o: [UP_CAT[x.cat] || '현장', x.place, (x.date || '').replace(/-/g, '.')].filter(Boolean).join(' · '), c: x.cat || 'etc' };
      });
      list = up.concat(WORKS); pf.innerHTML = list.map(workCard).join(''); figs = $$('figure', pf); counts(); applyFilter();
    }).catch(function () {});
  }
  var grid = gal || pf, lb = $('#lb');
  if (grid && lb) {
    var lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), lbK = 0, lastFocus = null;
    var visible = function () { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); };
    var openLb = function (k) { var w = list[k]; lbK = k; lbImg.src = srcP(w); lbImg.alt = w.t; lbT.textContent = w.t; lbM.textContent = w.o; if (!lb.classList.contains('on')) lastFocus = document.activeElement; lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('#lbX').focus(); };
    var closeLb = function () { lb.classList.remove('on'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); };
    var stepLb = function (d) { var v = visible(), i = v.indexOf(lbK); openLb(v[(i + d + v.length) % v.length]); };
    grid.addEventListener('click', function (e) { var f = e.target.closest('figure'); if (f) openLb(+f.getAttribute('data-k')); });
    grid.addEventListener('keydown', function (e) { var f = e.target.closest('figure'); if (f && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openLb(+f.getAttribute('data-k')); } });
    $('#lbX').addEventListener('click', closeLb); $('#lbPrev').addEventListener('click', function () { stepLb(-1); }); $('#lbNext').addEventListener('click', function () { stepLb(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) { if (!lb.classList.contains('on')) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowLeft') stepLb(-1); if (e.key === 'ArrowRight') stepLb(1); });
    var sx = 0;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) stepLb(dx < 0 ? 1 : -1); }, { passive: true });
    var filters = $('#filters');
    if (filters) {
      filters.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        $$('button', filters).forEach(function (x) { x.classList.remove('act'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('act'); b.setAttribute('aria-pressed', 'true');
        applyFilter();
      });
    }
  }

  /* ---------- 공지 (대문 요약) ---------- */
  var nl = $('#noticeList');
  if (nl) nl.innerHTML = NOTICES.length ? NOTICES.slice(0, 4).map(function (n) { return '<li><b>' + n.t + (n.n ? '<span class="new">NEW</span>' : '') + '</b><small>' + n.d + '</small></li>'; }).join('') : '<li class="empty">등록된 공지가 없습니다.</li>';

  /* ---------- 공지 · 게시판 · 자료실 (notice.html) ---------- */
  var bN = $('#boardNotice'), bB = $('#boardBlog'), bF = $('#boardFiles');
  if (bN) bN.innerHTML = NOTICES.length ? NOTICES.map(function (n, i) {
    return '<li><span class="no' + (n.pin ? ' pin' : '') + '">' + (n.pin ? '공지' : NOTICES.length - i) + '</span><b>' + n.t + (n.n ? ' <span class="new" style="display:inline-block;padding:1px 7px;border-radius:6px;background:var(--or);color:#fff;font-size:11px;font-family:var(--en)">NEW</span>' : '') + '</b><small>' + n.d + '</small>' + (n.b ? '<p>' + n.b + '</p>' : '') + '</li>';
  }).join('') : '<li class="empty">등록된 공지가 없습니다.</li>';
  if (bB) {
    var LIM = 10, shown = LIM;
    bB.innerHTML = BLOG.map(function (b, i) { return '<li' + (i >= shown ? ' hidden' : '') + '><span class="no">' + (BLOG.length - i) + '</span><a href="' + b.u + '" target="_blank" rel="noopener"><b>' + b.t + '</b></a><small>' + b.d + '</small></li>'; }).join('');
    var mb = $('#blogMore');
    if (mb) { if (BLOG.length <= LIM) mb.hidden = true; mb.addEventListener('click', function () { shown += LIM; $$('li', bB).forEach(function (li, i) { li.hidden = i >= shown; }); if (shown >= BLOG.length) mb.hidden = true; }); }
  }
  if (bF) bF.innerHTML = FILES.length ? FILES.map(function (f, i) {
    return '<li><span class="no">' + (FILES.length - i) + '</span><b>' + f.t + '</b><small><a class="dl" href="' + f.u + '" download><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>' + (f.s || '받기') + '</a></small>' + (f.b ? '<p>' + f.b + '</p>' : '') + '</li>';
  }).join('') : '<li class="empty">등록된 자료가 없습니다.</li>';

  var tabs = $('#tabs');
  if (tabs) {
    var tb = $$('button', tabs), panes = $$('.pane');
    var show = function (i) { tb.forEach(function (b, k) { b.classList.toggle('on', k === i); b.setAttribute('aria-selected', k === i); }); panes.forEach(function (p, k) { p.classList.toggle('on', k === i); }); };
    tb.forEach(function (b, i) { b.addEventListener('click', function () { show(i); history.replaceState(null, '', '#' + b.getAttribute('data-t')); }); });
    var h = location.hash.replace('#', ''); tb.forEach(function (b, i) { if (b.getAttribute('data-t') === h) show(i); });
  }

  /* ---------- 문의 보내기 ---------- */
  function isMobile() { return /iPhone|iPad|Android/i.test(navigator.userAgent); }
  function send(text, data, done) {
    function local() {
      if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true); return; }
      try { if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {}); } catch (e) {}
      done(false);
    }
    if (!FORM_ENDPOINT) { local(); return; }
    /* 문의 서버(큰길브리지와 함께 쓰는 앱스 스크립트) → 대표님 메일 + 큰길브리지 메일. 서버가 「ok」라고 답할 때만 보낸 것으로 친다 */
    data.at = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' }); data.page = location.href; data.service = '[' + COMPANY + '] ' + (data.type || '행사') + ' 문의';
    data.message = text; data.phone = data.tel || ''; data.website = '';
    fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok) done(true); else local(); })
      .catch(local);
  }
  $$('form.qform').forEach(function (form) {
    var done = $('.done', form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // 스팸 봇 함정
      var v = function (k) { var el = form.elements[k]; if (!el) return ''; if (el.length && !el.tagName) { var c = Array.prototype.filter.call(el, function (x) { return x.checked; })[0]; return c ? c.value : ''; } return (el.value || '').trim(); };
      var d = { name: v('name'), tel: v('tel'), type: v('type'), date: v('date'), region: v('region'), people: v('people'), msg: v('msg') };
      if (!d.name || !d.tel) { alert('성함과 연락처는 꼭 적어 주세요.'); (d.name ? form.elements.tel : form.elements.name).focus(); return; }
      var ag = $('input[name=agree]', form); if (ag && !ag.checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); ag.focus(); return; }
      var text = '[' + COMPANY + ' 견적문의]\n성함: ' + d.name + '\n연락처: ' + d.tel + '\n행사 종류: ' + (d.type || '-') + '\n날짜: ' + (d.date || '-') + '\n지역: ' + (d.region || '-') + '\n인원: ' + (d.people || '-') + (d.msg ? '\n요청: ' + d.msg : '');
      send(text, d, function (sent) {
        if (!done) { alert(sent ? '문의가 접수되었습니다.' : '문의 내용을 복사해 두었습니다. ' + SMS_TO + ' 로 문자 주세요.'); return; }
        done.classList.add('on');
        if (!sent) $('p', done).innerHTML = '문의 내용을 복사해 두었습니다.<br><b>' + SMS_TO + '</b> 로 문자에 붙여 넣어 보내 주시거나 전화 주세요.<br><small>행사 중엔 통화가 어려울 수 있어요. 문자 · 카톡을 남겨 주시면 연락드립니다.</small>';
      });
    });
    var again = $('.again', form);
    if (again) again.addEventListener('click', function () { done.classList.remove('on'); form.reset(); });
  });
})();
