/* 힐링엔터테인먼트 홈페이지 — 공통 스크립트 (외부 라이브러리 없음) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ================================================================
     여기부터 사장님 · 큰길브리지가 고치는 곳
     ================================================================ */

  /* 문의 폼 전송처 — 비어 있으면 폰은 문자 앱, PC 는 내용 복사 + 전화 안내.
     Apps Script(문의 서버) 주소를 넣으면 그쪽으로 JSON 이 간다. */
  var FORM_ENDPOINT = '';
  var SMS_TO = '010-5620-2153';
  var COMPANY = '힐링엔터테인먼트';
  /* 카카오톡 채널 주소 — 채널을 만들면 여기에 넣는다 (예: 'https://pf.kakao.com/_xxxxx/chat').
     비어 있으면 카톡 단추가 문의 페이지의 안내로 간다. */
  var KAKAO_URL = '';

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
  function workCard(w, k) {
    return '<figure data-k="' + k + '" data-c="' + w.c + '" tabindex="0" role="button" aria-label="' + w.t + ' 크게 보기">' +
      '<img src="' + IMG + 'th/' + w.f + '" alt="' + w.t + '" loading="lazy" width="800" height="600">' +
      '<figcaption><em>' + w.o + '</em><b>' + w.t + '</b></figcaption></figure>';
  }
  var gal = $('#gal'), pf = $('#pfGrid'), list = [];
  if (gal) { var pick = (gal.getAttribute('data-pick') || '').split(',').map(Number); list = pick.map(function (k) { return WORKS[k]; }).filter(Boolean); gal.innerHTML = list.map(workCard).join(''); }
  if (pf) { list = WORKS; pf.innerHTML = list.map(workCard).join(''); }
  var grid = gal || pf, lb = $('#lb');
  if (grid && lb) {
    var figs = $$('figure', grid), lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), lbK = 0, lastFocus = null;
    var visible = function () { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); };
    var openLb = function (k) { var w = list[k]; lbK = k; lbImg.src = IMG + w.f; lbImg.alt = w.t; lbT.textContent = w.t; lbM.textContent = w.o; if (!lb.classList.contains('on')) lastFocus = document.activeElement; lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('#lbX').focus(); };
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
      $$('button', filters).forEach(function (b) {
        var f = b.getAttribute('data-f'), n = f === 'all' ? WORKS.length : WORKS.filter(function (w) { return w.c.split(' ').indexOf(f) >= 0; }).length;
        b.insertAdjacentHTML('beforeend', '<small>' + n + '</small>');
      });
      filters.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        $$('button', filters).forEach(function (x) { x.classList.remove('act'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('act'); b.setAttribute('aria-pressed', 'true');
        var f = b.getAttribute('data-f');
        figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
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
    if (FORM_ENDPOINT) {
      data.at = new Date().toISOString(); data.page = location.href; data.service = COMPANY + ' 견적문의'; data.message = text;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}).then(function () { done(true); });
      return;
    }
    if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true); return; }
    try { if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {}); } catch (e) {}
    done(false);
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
