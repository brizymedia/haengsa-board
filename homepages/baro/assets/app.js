/* 바로기획 홈페이지 — 공통 스크립트 (외부 라이브러리 없음)
   글 목록 · 공지 · 자료실 · 현장 사진은 이 파일 맨 위 배열만 고치면 모든 페이지에 반영된다. */
(function () {
  'use strict';

  /* ---------- 문의 폼 전송처 ----------
     FORM_ENDPOINT 가 비어 있으면: 휴대폰은 문자 앱이 열리고(내용 채워짐), PC 는 내용을 복사해 준 뒤 전화 안내.
     문의 서버(Apps Script) 주소를 넣으면 그쪽으로 JSON 이 가고, 서버가 mot2256@naver.com 으로 메일을 보낸다. */
  var FORM_ENDPOINT = '';
  var SMS_TO = '010-2758-0655';
  var COMPANY = '바로기획';

  /* ---------- 공지사항 (위가 최신. n:true 면 NEW 표시) ---------- */
  var NOTICES = [
    { d: '2026.09.26', t: '바로기획 홈페이지를 새로 열었습니다.', b: '행사 사진 · 하는 일 · 문의 폼을 한곳에 모았습니다. 궁금한 점은 010-2758-0655 로 편하게 연락 주세요.', n: true },
    { d: '2026.09.26', t: '가을 체육대회 · 운동회 · 지역축제 일정 상담을 받고 있습니다.', b: '가을은 행사가 몰리는 시기입니다. 날짜가 정해지면 미리 연락 주시면 음향 · 천막 · MC 일정을 먼저 잡아 드립니다.', n: true },
    { d: '2026.09.26', t: '상담 시간 안내 — 오전 8시 ~ 저녁 8시 (전화 · 문자)', b: '문자와 홈페이지 문의는 언제든 남겨 주세요. 상담 시간에 차례로 연락드립니다.' }
  ];

  /* ---------- 자료실 (행사 준비에 도움 되는 블로그 글) ---------- */
  var FILES = [
    { d: '2026.08.21', t: '체육대회 준비 순서 12단계 — 실패 없는 진행표', k: '체크리스트', u: 'https://blog.naver.com/mot2256789/224385173795' },
    { d: '2026.08.18', t: '가을 체육대회 인기 종목 15가지 — 연령별 추천', k: '종목표', u: 'https://blog.naver.com/mot2256789/224377631654' },
    { d: '2026.07.24', t: '체육대회 게임도구 필수 준비물 10가지', k: '준비물', u: 'https://blog.naver.com/mot2256789/224354478157' },
    { d: '2026.09.08', t: '성공적인 행사기획을 위한 7단계 진행 순서', k: '기획', u: 'https://blog.naver.com/mot2256789/224403507156' },
    { d: '2026.09.09', t: '개업 · 이전 행사 커팅식 때 반드시 준비할 것 7가지', k: '커팅식', u: 'https://blog.naver.com/mot2256789/224403816953' },
    { d: '2026.09.22', t: '천막 · 테이블 · 의자 렌탈 확인사항 6가지', k: '렌탈', u: 'https://blog.naver.com/mot2256789/224419629857' },
    { d: '2026.09.23', t: '음향렌탈 업체 고를 때 유의사항 6가지', k: '음향', u: 'https://blog.naver.com/mot2256789/224419915506' },
    { d: '2026.09.03', t: '물놀이행사 성공 사례로 보는 핵심 준비 단계 4가지', k: '물놀이', u: 'https://blog.naver.com/mot2256789/224399894409' },
    { d: '2026.07.27', t: '야외 체육대회 vs 실내 체육대회 — 장단점 5가지', k: '비교', u: 'https://blog.naver.com/mot2256789/224354535200' }
  ];

  /* ---------- 네이버 블로그 글 (2026-09-26 RSS 기준 최근 50편 — 새 글은 맨 앞에 추가) ---------- */
  var BLOG = [
    { d: "2026.09.23", t: "안산 화성 음향렌탈 행사대행업체 선정시 유의사항6가지", u: "https://blog.naver.com/mot2256789/224419915506" },
    { d: "2026.09.22", t: "천막 테이블 의자 렌탈 확인사항 6가지", u: "https://blog.naver.com/mot2256789/224419629857" },
    { d: "2026.09.21", t: "시흥 수원 체육대회 이벤트행사 예산 절약 꿀팁 6가지", u: "https://blog.naver.com/mot2256789/224416122368" },
    { d: "2026.09.19", t: "안산 에어바운스 대여 체크리스트 7가지", u: "https://blog.naver.com/mot2256789/224413899322" },
    { d: "2026.09.18", t: "안산 화성 체육대회 각종게임도구및 행사용품대여 가성비꿀팁 7가지", u: "https://blog.naver.com/mot2256789/224413552984" },
    { d: "2026.09.17", t: "교회체육대회 행사전문업체 선정시 가장 유의 할점6가지", u: "https://blog.naver.com/mot2256789/224412356891" },
    { d: "2026.09.16", t: "화성물놀이축제 대형물놀이행사 무사히 치룰수있는 꿀팁6가지", u: "https://blog.naver.com/mot2256789/224411415195" },
    { d: "2026.09.15", t: "화성 풍선장식 전문업체 선정 6가지 꿀팁", u: "https://blog.naver.com/mot2256789/224410933761" },
    { d: "2026.09.14", t: "경기 안산 천막렌탈 업체 선택 시 꼭 알아두어야할 5가지", u: "https://blog.naver.com/mot2256789/224410323800" },
    { d: "2026.09.11", t: "소인원 명랑운동회 가성비좋은 이벤트행사업체 선정 6가지이유", u: "https://blog.naver.com/mot2256789/224406143426" },
    { d: "2026.09.10", t: "화성 체육대회 행사경력15년이상 가성비좋은 행사대행업체 선정노하우7가지", u: "https://blog.naver.com/mot2256789/224405863011" },
    { d: "2026.09.09", t: "개업이전행사 커팅식할 때 반드시 준비해야 할 것 7가지", u: "https://blog.naver.com/mot2256789/224403816953" },
    { d: "2026.09.08", t: "성공적인 행사기획을 위한 7단계 진행 순서, 궁금하신가요?", u: "https://blog.naver.com/mot2256789/224403507156" },
    { d: "2026.09.07", t: "안산 체육대회 대행업체20년경력 전문업체가 알려주는 준비 꿀팁", u: "https://blog.naver.com/mot2256789/224400746149" },
    { d: "2026.09.04", t: "체육대회 레크레이션 이벤트행사mc가중요한 5가지 이유", u: "https://blog.naver.com/mot2256789/224400631028" },
    { d: "2026.09.03", t: "물놀이행사 성공 사례로 보는핵심 준비 단계 4가지", u: "https://blog.naver.com/mot2256789/224399894409" },
    { d: "2026.09.02", t: "화성 천막렌탈 업체 선택 시 꼭 확인해야 할 5가지", u: "https://blog.naver.com/mot2256789/224398308558" },
    { d: "2026.09.01", t: "안산 행사 풍선장식 색상 조합 꿀팁 6가지", u: "https://blog.naver.com/mot2256789/224396279185" },
    { d: "2026.08.31", t: "용인 워터슬라이드 렌탈 업체 선정 시 확인할 5가지", u: "https://blog.naver.com/mot2256789/224395601984" },
    { d: "2026.08.28", t: "안산 커팅식 행사 준비물 5가지 총정리", u: "https://blog.naver.com/mot2256789/224393003161" },
    { d: "2026.08.27", t: "새솔동 물놀이축제 비가 와도 성공적으로 끝낼 수 있는 7가지 비법", u: "https://blog.naver.com/mot2256789/224392145062" },
    { d: "2026.08.21", t: "체육대회 준비 순서 12단계 완벽 정리 실패 없는 진행표", u: "https://blog.naver.com/mot2256789/224385173795" },
    { d: "2026.08.19", t: "안산 체육대회 행사용품대여 업체 고르는 기준 6가지 총정리", u: "https://blog.naver.com/mot2256789/224382111924" },
    { d: "2026.08.18", t: "가을 체육대회 인기 종목 15가지 연령별 추천 총정리", u: "https://blog.naver.com/mot2256789/224377631654" },
    { d: "2026.08.14", t: "안산 화성 행사MC섭외 및 레크리에이션 강사 섭외 이벤트업체", u: "https://blog.naver.com/mot2256789/224377499278" },
    { d: "2026.08.13", t: "안산 행사대행 이벤트전문업체 선정 꿀팁 6가지", u: "https://blog.naver.com/mot2256789/224376542619" },
    { d: "2026.08.12", t: "가을운동회 체육대회 이벤트업체 선정 미리미리 준비하세요~", u: "https://blog.naver.com/mot2256789/224374959385" },
    { d: "2026.08.11", t: "화성 안산 행사용품대여 이벤트업체 선정 꿀팁 7가지", u: "https://blog.naver.com/mot2256789/224374172571" },
    { d: "2026.08.07", t: "화성 체육대회사회자 전문MC섭외 잘하는 이벤트업체 선정 노하우 5가지", u: "https://blog.naver.com/mot2256789/224370975311" },
    { d: "2026.08.06", t: "안산 화성 행사용천막렌탈업체 선정시 유의사항 꿀팁 7가지", u: "https://blog.naver.com/mot2256789/224369862578" },
    { d: "2026.08.05", t: "물놀이축제 행사사고없이 안전하게 진행하는이벤트업체 선정 노하우 6가지", u: "https://blog.naver.com/mot2256789/224368846070" },
    { d: "2026.08.04", t: "체육대회 게임도구 및 명랑운동회게임도구 렌탈 인기종목 7가지", u: "https://blog.naver.com/mot2256789/224363838041" },
    { d: "2026.08.03", t: "안산 화성 천막 렌탈 시꼭 알아야 할 5가지", u: "https://blog.naver.com/mot2256789/224363763799" },
    { d: "2026.07.31", t: "화성 안산 가을체육대회 행사대행업체 선정미리 준비해야 할 이유 6가지", u: "https://blog.naver.com/mot2256789/224363107324" },
    { d: "2026.07.30", t: "커팅식 오픈행사 및 개업행사전문이벤트업체 선정 5가지 꿀팁", u: "https://blog.naver.com/mot2256789/224360624942" },
    { d: "2026.07.29", t: "수원 체육대회 이벤트전문업체 전문 MC 섭외로 달라진 현장 4가지(바로기획)", u: "https://blog.naver.com/mot2256789/224360419895" },
    { d: "2026.07.28", t: "화성 물놀이행사업체 선정준비 실패 없는 5가지 기준", u: "https://blog.naver.com/mot2256789/224359430681" },
    { d: "2026.07.27", t: "야외 체육대회 vs 실내 체육대회비교 장단점 5가지", u: "https://blog.naver.com/mot2256789/224354535200" },
    { d: "2026.07.24", t: "체육대회 게임도구 필수 준비물 10가지", u: "https://blog.naver.com/mot2256789/224354478157" },
    { d: "2026.07.23", t: "경기 화성 안산체육대회 렌탈 운동회 렌탈용품 설치 및 대여업체", u: "https://blog.naver.com/mot2256789/224354026563" },
    { d: "2026.07.22", t: "지역축제 주민자치회 행사성공적으로 치르는 노하우 7가지 대공", u: "https://blog.naver.com/mot2256789/224353251992" },
    { d: "2026.07.21", t: "물놀이장 렌탈업체 선정 시유의사항 6가지", u: "https://blog.naver.com/mot2256789/224352949787" },
    { d: "2026.07.20", t: "화성 안산 운동회대행업체 선정꿀팁 6가지", u: "https://blog.naver.com/mot2256789/224350150949" },
    { d: "2026.07.16", t: "명랑운동회대행 체육대회대행 이벤트업체가행사 성공적으로 치를 수 있는 노하우 5가지", u: "https://blog.naver.com/mot2256789/224348434014" },
    { d: "2026.07.15", t: "가을 체육대회 이벤트업체 선정실패 없는 5가지 기준", u: "https://blog.naver.com/mot2256789/224347212855" },
    { d: "2026.07.14", t: "안산 화성 행사대행 전문업체이벤트 행사용품 렌탈 전문업체", u: "https://blog.naver.com/mot2256789/224346085524" },
    { d: "2026.07.13", t: "체육대회 및 이벤트행사용품 렌탈가성비 행사대행업체 조건 5가지", u: "https://blog.naver.com/mot2256789/224342269674" },
    { d: "2026.07.10", t: "용인 수원 시흥 물놀이행사업체 워터슬라이드 수영장 대여 잘해주는 곳", u: "https://blog.naver.com/mot2256789/224342207464" },
    { d: "2026.07.09", t: "동탄 어린이집 유치원 운동회잘하는 이벤트업체 찾는 노하우 5가지", u: "https://blog.naver.com/mot2256789/224340284412" },
    { d: "2026.07.08", t: "안산 화성 천막 테이블 의자행사용품 렌탈 업체 선정 꿀팁 5가지", u: "https://blog.naver.com/mot2256789/224339192450" }
  ];

  /* ---------- 현장 사진 (assets/img/p = 크게 1600px, assets/img/t = 목록 800px, 파일 이름 = f) ----------
     c: sports 체육대회 · festival 지역축제 · water 물놀이 · ceremony 커팅식·오픈 · gear 음향·장비·장식
     출처는 assets/img/SOURCES.md (전부 바로기획 네이버 블로그 사진) */
  var IMG_P = 'assets/img/p/', IMG_T = 'assets/img/t/';
  var WORKS = [
    { f: 's03', t: '운동장 천막 · 입장 아치 · 축포', o: '체육대회 · 수원 교회 연합 · 2026', c: 'sports' },
    { f: 's06', t: '단체 이어달리기 게임', o: '체육대회 · 수원 교회 연합 · 2026', c: 'sports' },
    { f: 's02', t: '대형 공 굴리기 게임', o: '체육대회 · 수원 교회 연합 · 2026', c: 'sports' },
    { f: 's09', t: '운동장 게임 진행', o: '체육대회 · 수원 교회 연합 · 2026', c: 'sports' },
    { f: 's12', t: '게임도구 세팅', o: '체육대회 · 수원 교회 연합 · 2026', c: 'sports gear' },
    { f: 'k23', t: '실내 체육관 낙하산 게임', o: '체육대회 · 실내', c: 'sports' },
    { f: 'h21', t: '팀별 게임 준비', o: '체육대회', c: 'sports' },
    { f: 'm01', t: '수노을 물놀이축제 전경', o: '물놀이축제 · 화성 새솔동 · 2026', c: 'water festival' },
    { f: 'm21', t: '대형 풀장 · 물대포', o: '물놀이축제 · 화성 새솔동 · 2026', c: 'water festival' },
    { f: 'm09', t: '대형 에어 물놀이 기구', o: '물놀이축제 · 화성 새솔동 · 2026', c: 'water' },
    { f: 'y01', t: '학교 운동장 물놀이장 전경', o: '물놀이 행사 · 용인다움학교 · 2026', c: 'water' },
    { f: 'y07', t: '물놀이 풀 · 워터슬라이드', o: '물놀이 행사 · 용인다움학교 · 2026', c: 'water' },
    { f: 'y03', t: '물고기 잡기 체험 풀', o: '물놀이 행사 · 용인다움학교 · 2026', c: 'water' },
    { f: 'f02', t: '파라솔 쉼터 · 주민 축제', o: '지역축제 · 수노을 그린 축제 · 2026', c: 'festival' },
    { f: 'f06', t: '야외무대 태권도 공연', o: '지역축제 · 수노을 그린 축제 · 2026', c: 'festival' },
    { f: 'f12', t: '야외무대 댄스 공연', o: '지역축제 · 수노을 그린 축제 · 2026', c: 'festival' },
    { f: 'f04', t: '안내 · 체험 부스 천막', o: '지역축제 · 수노을 그린 축제 · 2026', c: 'festival gear' },
    { f: 'f09', t: '체험 부스 거리', o: '지역축제 · 수노을 그린 축제 · 2026', c: 'festival' },
    { f: 'h22', t: '야외무대 · LED 공연', o: '지역행사 · 화성 어울림 한마당', c: 'festival gear' },
    { f: 'k21', t: '야외 공연 · 밴드 음향', o: '공연 섭외 · 지역행사', c: 'festival gear' },
    { f: 'a17', t: '무대 · 스피커 · 조명 세팅', o: '음향 · 무대 · 문화 축제 · 2026', c: 'gear festival' },
    { f: 'a07', t: '음향 부스 · 무대 운영', o: '음향 · 무대 · 문화 축제 · 2026', c: 'gear' },
    { f: 's05', t: '음향 믹서 운영', o: '음향 · 수원 교회 연합 체육대회', c: 'gear sports' },
    { f: 'h23', t: '음향 장비 · 게임도구', o: '장비 · 행사용품', c: 'gear' },
    { f: 'h26', t: '대규모 야외 좌석 세팅', o: '행사용품 · 야외 행사', c: 'gear' },
    { f: 'c16', t: '개원식 테이프 커팅', o: '커팅식 · 안산 · 2026', c: 'ceremony' },
    { f: 'c03', t: '레드카펫 · 오색띠 커팅 세팅', o: '커팅식 · 안산 · 2026', c: 'ceremony' },
    { f: 'c11', t: '풍선 아치 장식', o: '커팅식 · 안산 · 2026', c: 'ceremony gear' }
  ];
  var HOME_PICKS = ['s03', 'm21', 'c16', 'f06', 'a07', 'y01', 'k23', 'c11'];

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M9 7h8v8"/></svg>';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- 머리글 · 폰 메뉴 · 맨 위로 ---------- */
  var hd = $('#hd'), totop = $('#totop');
  function onScroll() {
    var y = window.scrollY;
    if (hd) hd.classList.toggle('solid', y > 40);
    if (totop) totop.classList.toggle('on', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  var page = (location.pathname.split('/').pop() || 'index.html');
  $$('.hd nav a, .sheet nav a').forEach(function (a) { if (a.getAttribute('href') === page) a.classList.add('act'); });

  var burger = $('#burger'), sheet = $('#sheet');
  function closeSheet() { sheet.classList.remove('on'); burger.classList.remove('x'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
  if (burger && sheet) {
    burger.addEventListener('click', function () {
      var on = sheet.classList.toggle('on'); burger.classList.toggle('x', on); burger.setAttribute('aria-expanded', on);
      document.body.style.overflow = on ? 'hidden' : '';
    });
    $$('a, .x', sheet).forEach(function (a) { a.addEventListener('click', closeSheet); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet.classList.contains('on')) closeSheet(); });
  }

  /* ---------- 히어로 영상 (폰은 작은 파일, 동작 줄이기 설정이면 사진만) ---------- */
  $$('video[data-src]').forEach(function (v) {
    if (reduce) { v.removeAttribute('autoplay'); return; }
    v.muted = true; v.setAttribute('muted', '');
    v.src = window.innerWidth < 900 ? v.getAttribute('data-src-sm') : v.getAttribute('data-src');
    function tryPlay() { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    tryPlay(); v.addEventListener('canplay', tryPlay, { once: true });
    document.addEventListener('pointerdown', function () { if (v.paused && !v.dataset.userPaused) tryPlay(); }, { once: true });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { if (v.paused && !v.dataset.userPaused) tryPlay(); } else if (!v.paused) v.pause(); });
    }, { threshold: .05 }).observe(v);
  });
  $$('[data-toggle-video]').forEach(function (b) {
    var v = document.getElementById(b.getAttribute('data-toggle-video')); if (!v) return;
    function sync() { b.classList.toggle('paused', v.paused); b.setAttribute('aria-label', v.paused ? '영상 재생' : '영상 멈춤'); }
    v.addEventListener('play', sync); v.addEventListener('pause', sync); sync();
    b.addEventListener('click', function () { if (v.paused) { v.dataset.userPaused = ''; v.play(); } else { v.dataset.userPaused = '1'; v.pause(); } });
  });

  /* ---------- 등장 효과 ---------- */
  var rvEls = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var rio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    rvEls.forEach(function (el) { rio.observe(el); });
  } else rvEls.forEach(function (el) { el.classList.add('in'); });

  /* ---------- 하는 일 목록 (대문) — 누르면 펼치고 옆 사진 바꿈 ---------- */
  var svl = $('#svlist');
  if (svl) {
    var lis = $$('li', svl), stageImgs = $$('#stage img'), cap = $('#stage .cap');
    function openSv(i) {
      lis.forEach(function (li, k) { li.classList.toggle('on', k === i); $('button', li).setAttribute('aria-expanded', k === i); });
      stageImgs.forEach(function (im, k) { im.classList.toggle('on', k === i); });
      if (cap) cap.innerHTML = '<b>' + esc($('.t', lis[i]).firstChild.textContent) + '</b>' + esc(stageImgs[i] ? stageImgs[i].alt : '');
    }
    lis.forEach(function (li, i) {
      $('button', li).addEventListener('click', function () { openSv(i); });
      li.addEventListener('mouseenter', function () { if (window.innerWidth > 960) openSv(i); });
    });
    openSv(0);
  }

  /* ---------- 현장 사진 (대문 8장 · 현장사진 페이지 전체) ---------- */
  function figHtml(w, k) {
    return '<figure data-k="' + k + '" data-c="' + w.c + '" tabindex="0">' +
      '<img src="' + IMG_T + w.f + '.webp" alt="' + esc(w.t) + '" loading="lazy" width="800" height="600">' +
      '<figcaption><small>' + esc(w.o) + '</small>' + esc(w.t) + '</figcaption></figure>';
  }
  var gal = $('#gal'), pf = $('#pfGrid'), list = [];
  if (gal) { list = HOME_PICKS.map(function (f) { return WORKS.filter(function (w) { return w.f === f; })[0]; }).filter(Boolean); gal.innerHTML = list.map(figHtml).join(''); }
  if (pf) {
    list = WORKS; pf.innerHTML = list.map(figHtml).join('');
    $$('#filters button').forEach(function (b) {
      var f = b.getAttribute('data-f'), n = f === 'all' ? WORKS.length : WORKS.filter(function (w) { return w.c.split(' ').indexOf(f) >= 0; }).length;
      b.insertAdjacentHTML('beforeend', '<span class="c">' + n + '</span>');
    });
  }
  var grid = gal || pf, lb = $('#lb');
  if (grid && lb) {
    var figs = $$('figure', grid), lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), lbK = 0, lastFocus = null;
    function visible() { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); }
    function openLb(k) { var w = list[k]; lbK = k; lbImg.src = IMG_P + w.f + '.webp'; lbImg.alt = w.t; lbT.textContent = w.t; lbM.textContent = w.o; if (!lb.classList.contains('on')) lastFocus = document.activeElement; lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('#lbX').focus(); }
    function closeLb() { lb.classList.remove('on'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
    function stepLb(d) { var v = visible(), i = v.indexOf(lbK); openLb(v[(i + d + v.length) % v.length]); }
    grid.addEventListener('click', function (e) { var f = e.target.closest('figure'); if (f) openLb(+f.getAttribute('data-k')); });
    grid.addEventListener('keydown', function (e) { var f = e.target.closest('figure'); if (f && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openLb(+f.getAttribute('data-k')); } });
    $('#lbX').addEventListener('click', closeLb);
    $('#lbPrev').addEventListener('click', function () { stepLb(-1); });
    $('#lbNext').addEventListener('click', function () { stepLb(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE') closeLb(); });
    document.addEventListener('keydown', function (e) { if (!lb.classList.contains('on')) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowLeft') stepLb(-1); if (e.key === 'ArrowRight') stepLb(1); });
    var sx = 0;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) stepLb(dx < 0 ? 1 : -1); }, { passive: true });
    var filters = $('#filters');
    if (filters) filters.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      $$('button', filters).forEach(function (x) { x.classList.remove('act'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('act'); b.setAttribute('aria-pressed', 'true');
      var f = b.getAttribute('data-f');
      figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
    });
  }

  /* ---------- 블로그 글 미리보기 (대문 · 회사소개) ---------- */
  $$('[data-blog]').forEach(function (el) {
    var n = +el.getAttribute('data-blog') || 5;
    el.innerHTML = BLOG.slice(0, n).map(function (b) { return '<a href="' + b.u + '" target="_blank" rel="noopener"><small>' + b.d + '</small><b>' + esc(b.t) + '</b>' + ARR + '</a>'; }).join('');
  });
  $$('[data-notice]').forEach(function (el) {
    var n = +el.getAttribute('data-notice') || 3;
    el.innerHTML = NOTICES.length ? NOTICES.slice(0, n).map(function (x) { return '<li><small>' + x.d + '</small><b>' + esc(x.t) + (x.n ? '<span class="new">NEW</span>' : '') + '</b></li>'; }).join('') : '<li><b>등록된 공지가 없습니다.</b></li>';
  });

  /* ---------- 공지 · 블로그 · 자료실 페이지 ---------- */
  var tabs = $('#btabs');
  if (tabs) {
    var tbs = $$('button', tabs), panes = $$('.pane');
    function showTab(id) {
      tbs.forEach(function (b) { var on = b.getAttribute('data-t') === id; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
      panes.forEach(function (p) { p.classList.toggle('on', p.id === id); });
    }
    tbs.forEach(function (b) { b.addEventListener('click', function () { showTab(b.getAttribute('data-t')); history.replaceState(null, '', '#' + b.getAttribute('data-t')); }); });
    $('[data-t="notice"] small', tabs).textContent = NOTICES.length;
    $('[data-t="blog"] small', tabs).textContent = BLOG.length;
    $('[data-t="files"] small', tabs).textContent = FILES.length;
    var h = location.hash.slice(1); showTab(['notice', 'blog', 'files'].indexOf(h) >= 0 ? h : 'notice');

    // 공지
    var nb = $('#noticeBoard');
    nb.innerHTML = NOTICES.length ? NOTICES.map(function (x, i) {
      return '<li><span class="no' + (x.n ? ' pin' : '') + '">' + (x.n ? '공지' : NOTICES.length - i) + '</span><b>' + esc(x.t) + (x.b ? '<small>' + esc(x.b) + '</small>' : '') + '</b><span class="d">' + x.d + '</span></li>';
    }).join('') : '<li class="empty">등록된 공지가 없습니다.</li>';

    // 블로그 (검색 + 쪽 나눔)
    var bb = $('#blogBoard'), pager = $('#blogPager'), q = $('#blogQ'), PER = 10, pg = 0, rows = BLOG;
    function drawBlog() {
      var total = Math.max(1, Math.ceil(rows.length / PER)); pg = Math.min(pg, total - 1);
      bb.innerHTML = rows.length ? rows.slice(pg * PER, pg * PER + PER).map(function (b) {
        return '<a class="row" href="' + b.u + '" target="_blank" rel="noopener"><span class="no">' + (BLOG.length - BLOG.indexOf(b)) + '</span><b>' + esc(b.t) + '</b><span class="d">' + b.d + '</span></a>';
      }).join('') : '<li class="empty">찾는 글이 없습니다.</li>';
      var h2 = ''; for (var i = 0; i < total; i++) h2 += '<button type="button" class="' + (i === pg ? 'on' : '') + '" data-p="' + i + '">' + (i + 1) + '</button>';
      pager.innerHTML = total > 1 ? h2 : '';
    }
    pager.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; pg = +b.getAttribute('data-p'); drawBlog(); bb.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); });
    q.addEventListener('input', function () { var k = q.value.trim(); rows = k ? BLOG.filter(function (b) { return b.t.indexOf(k) >= 0; }) : BLOG; pg = 0; drawBlog(); });
    drawBlog();

    // 자료실
    var FI = '<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg></span>';
    $('#fileBoard').innerHTML = FILES.map(function (f) {
      return '<a class="row" href="' + f.u + '" target="_blank" rel="noopener">' + FI + '<b>' + esc(f.t) + '<small>' + esc(f.k) + ' · 블로그에서 보기</small></b><span class="d">' + f.d + '</span></a>';
    }).join('');
  }

  /* ---------- 문의 보내기 ---------- */
  function isMobile() { return /iPhone|iPad|Android/i.test(navigator.userAgent); }
  function send(text, data, done) {
    if (FORM_ENDPOINT) {
      data.at = new Date().toISOString(); data.page = location.href; data.service = COMPANY + ' 행사 문의'; data.message = text;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}).then(function () { done(true); });
      return;
    }
    if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {});
    done(false);
  }
  var form = $('#quoteForm');
  if (form) {
    var doneBox = $('#formDone');
    var pre = location.hash.match(/^#type=(.+)$/);
    if (pre && form.elements.type) { try { var want = decodeURIComponent(pre[1]); $$('option', form.elements.type).forEach(function (o) { if (o.value.indexOf(want) >= 0) form.elements.type.value = o.value; }); } catch (e) {} }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // 스팸 봇 함정
      var d = {}; ['name', 'tel', 'org', 'type', 'date', 'place', 'people', 'msg'].forEach(function (k) { d[k] = form.elements[k] ? form.elements[k].value.trim() : ''; });
      d.need = $$('input[name="need"]:checked', form).map(function (x) { return x.value; }).join(', ');
      if (!d.name || !d.tel) { alert('성함과 연락처는 꼭 적어 주세요.'); (d.name ? form.elements.tel : form.elements.name).focus(); return; }
      if (!$('#fAgree').checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); return; }
      var text = '[' + COMPANY + ' 행사 문의]\n성함: ' + d.name + '\n연락처: ' + d.tel + '\n기관 · 회사: ' + (d.org || '-') + '\n행사 종류: ' + d.type + '\n날짜: ' + (d.date || '-') + '\n장소: ' + (d.place || '-') + '\n인원: ' + (d.people || '-') + '\n필요한 것: ' + (d.need || '-') + '\n내용: ' + (d.msg || '-');
      send(text, d, function (sent) {
        doneBox.classList.add('on');
        if (!sent) $('p', doneBox).innerHTML = '문의 내용을 복사해 두었습니다.<br><b>' + SMS_TO + '</b> 로 문자에 붙여 넣어 보내시거나 전화 주세요.';
      });
    });
    var again = $('#formAgain'); if (again) again.addEventListener('click', function () { doneBox.classList.remove('on'); form.reset(); });
  }
})();
