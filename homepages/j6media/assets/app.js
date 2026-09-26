/* 제이식스미디어(J6 MEDIA) 홈페이지 — 공통 스크립트 (외부 라이브러리 없음) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 문의 폼 전송처 ----------
     FORM_ENDPOINT 가 비어 있으면 휴대폰에서는 문자 앱이 열리고, PC 에서는 내용을 복사해 준다.
     문의 접수 서버(Apps Script) 주소를 넣으면 그쪽으로 JSON 이 간다. */
  var FORM_ENDPOINT = '';
  var SMS_TO = '010-4450-4212';
  var COMPANY = '제이식스미디어';

  /* ---------- 공지 (여기만 고치면 대문 · 공지 페이지에 반영. n:true = NEW 표시, top:true = 맨 위 고정) ---------- */
  var NOTICES = [
    { d: '2026.09.21', t: '제이식스미디어 홈페이지를 새로 열었습니다.', n: true, top: true, b: '예배 · 공연 · 행사 음향과 조명, 음향 · 영상 · 방송장비 설치까지 한곳에서 안내해 드립니다.\n문의는 전화 · 문자(010-4450-4212) 또는 「견적 문의」 페이지에 남겨 주세요.' },
    { d: '2026.09.21', t: '영업시간 안내 — 월~토 09:00~18:00, 일요일 휴무', n: true, b: '월요일부터 토요일까지 오전 9시~오후 6시에 상담합니다. 일요일은 쉽니다.\n문의 폼과 문자는 언제든 남기실 수 있습니다.' },
    { d: '2025.11.26', t: '사무실 이전 안내 — 에이스하이엔드타워별내 319호', b: '제이식스미디어 사무실을 경기도 남양주시 순화궁로 282 에이스하이엔드타워별내 319호로 옮겼습니다.\n방문 상담은 미리 연락 주시고 오시면 됩니다.' }
  ];
  /* ---------- 자료실 (u: 파일 · 링크 주소, k: 종류 표시) ---------- */
  var FILES = [
    { d: '2026.02.19', t: '제이식스미디어 소개 브로셔 (블로그)', k: 'LINK', u: 'https://blog.naver.com/martin301/224187831107' },
    { d: '2026.09.21', t: '보유 장비 · 취급 브랜드 안내', k: 'PAGE', u: 'equipment.html' },
    { d: '2026.09.21', t: '행사 문의 전에 정리해 두면 좋은 것 (체크리스트)', k: 'PAGE', u: 'contact.html#ready' }
  ];

  /* ---------- 현장 사진 (assets/img/works/wN.webp ↔ 제목) ----------
     c: church 교회행사 · corp 기업행사 · gov 지자체 · school 학교 · show 전시·공연 · install 설치 */
  var WORKS = [
    { i: 1, t: '더스테이힐링파크 야외 공연 — 무대와 객석', o: '기업행사 · 가평 · 2024', c: 'corp' },
    { i: 2, t: '숲속 무대 공연 음향 · 영상', o: '기업행사 · 가평 · 2024', c: 'corp' },
    { i: 3, t: '강신욱 음악 전시 「꿈의 해석」 이머시브 사운드', o: '전시 · 공연 · 서울 C스퀘어 · 2023', c: 'show' },
    { i: 4, t: '조명바턴에 매단 스피커와 피아노 영상', o: '전시 · 공연 · 서울 C스퀘어 · 2023', c: 'show' },
    { i: 5, t: '자동 연주 피아노 · 신디사이저 · 스피커 셋팅', o: '전시 · 공연 · 서울 C스퀘어 · 2023', c: 'show' },
    { i: 6, t: '서울라이트 빛섬축제 레이저 무대', o: '축제 · 서울 · 2025', c: 'gov' },
    { i: 7, t: '빛섬축제 빛의 터널', o: '축제 · 서울 · 2025', c: 'gov' },
    { i: 8, t: '빛섬축제 메인무대 공연', o: '축제 · 서울 · 2025', c: 'gov' },
    { i: 9, t: '빛섬축제 입구 조형물', o: '축제 · 서울 · 2025', c: 'gov' },
    { i: 10, t: '원주 오크밸리리조트 그랜드볼룸 수련회 찬양', o: '교회행사 · 원주 · 2026', c: 'church' },
    { i: 11, t: '믹서 자리에서 본 그랜드볼룸', o: '교회행사 · 원주 · 2026', c: 'church' },
    { i: 12, t: 'NEXO 스피커 · 서브우퍼 스택', o: '교회행사 · 원주 · 2026', c: 'church gear' },
    { i: 13, t: '무대 쪽 랙과 신호 배선', o: '교회행사 · 원주 · 2026', c: 'church gear' },
    { i: 14, t: '부천국제판타스틱영화제 AI 국제 콘퍼런스 콘솔', o: '지자체 행사 · 부천아트센터 · 2025', c: 'gov' },
    { i: 15, t: 'AI 국제 콘퍼런스 대담 무대', o: '지자체 행사 · 부천아트센터 · 2025', c: 'gov' },
    { i: 16, t: '부천국제판타스틱영화제 제막식 음향', o: '지자체 행사 · 부천시청 잔디광장 · 2026', c: 'gov' },
    { i: 17, t: '제막식 현장 믹서 운영', o: '지자체 행사 · 부천시청 잔디광장 · 2026', c: 'gov' },
    { i: 18, t: '하나복네트워크 본강좌 세미나 음향', o: '교회행사 · 곤지암 소망수양관 · 2026', c: 'church' },
    { i: 19, t: '2026 S/S FASHION KODE 패션쇼 런웨이', o: '전시 · 공연 · 서울 · 2025', c: 'show' },
    { i: 20, t: '패션쇼 무대 조명 · 음향 셋팅', o: '전시 · 공연 · 서울 · 2025', c: 'show' },
    { i: 21, t: '패션쇼 본 공연', o: '전시 · 공연 · 서울 · 2025', c: 'show' },
    { i: 22, t: '패션쇼 후면 스피커', o: '전시 · 공연 · 서울 · 2025', c: 'show gear' },
    { i: 23, t: '이문동교회 본당 음향 · 영상 리모델링', o: '설치 · 서울 이문동 · 2025', c: 'install church' },
    { i: 24, t: '이문동교회 본당 스피커 · 전광판', o: '설치 · 서울 이문동 · 2025', c: 'install church' },
    { i: 25, t: '이문동교회 음향 랙', o: '설치 · 서울 이문동 · 2025', c: 'install gear' },
    { i: 26, t: '밀알두레학교 체육한마당 음향 지원', o: '학교행사 · 2025', c: 'school' },
    { i: 27, t: '더스테이힐링파크 어린이날 축제 음향 운영', o: '기업행사 · 가평 · 2025', c: 'corp' },
    { i: 28, t: '힐링키즈 페스티벌 무대 스피커', o: '기업행사 · 가평 · 2025', c: 'corp' },
    { i: 29, t: 'NEXO 라인어레이 M12 · MSUB18 입고', o: '장비 · 2025', c: 'gear' },
    { i: 30, t: '현장으로 나가는 장비 케이스', o: '장비 · 2025', c: 'gear' }
  ];
  var IMG = 'assets/img/works/';

  /* ---------- 현장 이야기 (네이버 블로그 martin301 — 새 글은 맨 앞에 추가) ---------- */
  var BLOG = [
    { d: "2026.08.31", t: "원주오크밸리리조트 그랜드볼룸 음향랜탈", u: "https://blog.naver.com/martin301/224396313056" },
    { d: "2026.08.07", t: "기흥 솔숨 음향시스템", u: "https://blog.naver.com/martin301/224371236657" },
    { d: "2026.06.15", t: "파주 NEXO 이머시브 트레이닝 센터 셋팅중", u: "https://blog.naver.com/martin301/224316593428" },
    { d: "2026.06.10", t: "부천국제판타스틱영화제 제막식 행사 음향", u: "https://blog.naver.com/martin301/224311909715" },
    { d: "2026.06.02", t: "하나복 본강좌", u: "https://blog.naver.com/martin301/224304136814" },
    { d: "2026.02.19", t: "제이식스미디어 소개 브로셔", u: "https://blog.naver.com/martin301/224187831107" },
    { d: "2025.11.26", t: "제이식스미디어 사무실 이전", u: "https://blog.naver.com/martin301/224088348666" },
    { d: "2025.10.23", t: "2026 S/S FASHION KODE패션쇼 음향", u: "https://blog.naver.com/martin301/224051310828" },
    { d: "2025.10.06", t: "서울라이트 빛섬축제", u: "https://blog.naver.com/martin301/224033523934" },
    { d: "2025.07.18", t: "나인블럭 화성시청점 bgm시스템 설치", u: "https://blog.naver.com/martin301/223938640874" },
    { d: "2025.07.06", t: "부천국제영화제 AI컨퍼런스 진행", u: "https://blog.naver.com/martin301/223923883853" },
    { d: "2025.07.03", t: "dpa4098 70cm, ev pxm-12mp-eu설치", u: "https://blog.naver.com/martin301/223920688355" },
    { d: "2025.06.24", t: "나인블럭 수원교동점 음향시스템 설치!! 9BLOCK", u: "https://blog.naver.com/martin301/223910380610" },
    { d: "2025.06.03", t: "2025 하나복 본강좌 음향(6월2-4일)", u: "https://blog.naver.com/martin301/223887322301" },
    { d: "2025.05.23", t: "2025 KOBA 코바쇼(방송영상장비전시회)", u: "https://blog.naver.com/martin301/223875099117" },
    { d: "2025.05.07", t: "nexo msub18+p12조합으로 첫 개시", u: "https://blog.naver.com/martin301/223857431498" },
    { d: "2025.05.01", t: "라인어레이 스피커 NEXO M12 + MSUB18", u: "https://blog.naver.com/martin301/223851777650" },
    { d: "2025.04.15", t: "제주 p16hq, p16d 납품", u: "https://blog.naver.com/martin301/223833792253" },
    { d: "2025.04.07", t: "더스테이힐링파크 카페 외부방수스피커 설치", u: "https://blog.naver.com/martin301/223825275834" },
    { d: "2025.04.03", t: "나인블럭카페 역삼 한국기술센터점 BGM음향시스템", u: "https://blog.naver.com/martin301/223821049758" },
    { d: "2025.04.03", t: "이문동교회 리모델링, 교회음향영상시스템", u: "https://blog.naver.com/martin301/223821012265" },
    { d: "2025.03.25", t: "2025년 두번째 교회음향 지원사업_포천 태광성서교회", u: "https://blog.naver.com/martin301/223809202265" },
    { d: "2025.03.24", t: "2025년 첫번째 교회음향 지원사업1_제주대륜교회 설치", u: "https://blog.naver.com/martin301/223808032832" },
    { d: "2025.03.06", t: "2025년 첫번째 교회음향 지원사업_1 (제주대륜교회)", u: "https://blog.naver.com/martin301/223786373427" },
    { d: "2025.03.06", t: "100인치 TV설치(목동OOO교회)", u: "https://blog.naver.com/martin301/223786330994" },
    { d: "2025.01.04", t: "아르코무대예술교육원 레이저 프로젝터교체 (파나소닉16,000안시)", u: "https://blog.naver.com/martin301/223714798431" },
    { d: "2025.01.02", t: "신논현역 치과 BGM음향시스템", u: "https://blog.naver.com/martin301/223712517221" },
    { d: "2024.07.31", t: "리모델링 준비 이동설치", u: "https://blog.naver.com/martin301/223531967247" },
    { d: "2024.06.04", t: "정원 스피커 설치_ 더스테이힐링파크 별빛정원", u: "https://blog.naver.com/martin301/223469068209" },
    { d: "2024.06.03", t: "더스테이힐링파크 공연", u: "https://blog.naver.com/martin301/223467972536" },
    { d: "2024.05.09", t: "고고다이노 전국투어_천안", u: "https://blog.naver.com/martin301/223441847686" },
    { d: "2024.04.24", t: "소개와 추천", u: "https://blog.naver.com/martin301/223426253779" },
    { d: "2024.03.21", t: "나인블럭 고기동 라이브러리 앤 팻 카페음향", u: "https://blog.naver.com/martin301/223391122966" },
    { d: "2024.01.07", t: "신당동 bar vision", u: "https://blog.naver.com/martin301/223315224071" },
    { d: "2023.12.16", t: "제주성안교회 다음세대 예배실 리모델링 마무리", u: "https://blog.naver.com/martin301/223294706015" },
    { d: "2023.11.20", t: "하나복네트워크 심화강좌", u: "https://blog.naver.com/martin301/223269854532" },
    { d: "2023.11.04", t: "퐁당아카데미 * 리빙사운드 제주세미나", u: "https://blog.naver.com/martin301/223255376073" },
    { d: "2023.09.12", t: "제이식스미디어 회사 소개 브로셔", u: "https://blog.naver.com/martin301/223209635839" },
    { d: "2023.09.12", t: "강신욱 작가님 음악 전시 '꿈의 해석' 셋팅", u: "https://blog.naver.com/martin301/223209619397" },
    { d: "2023.06.30", t: "9BLOCK 퍼피파크 PUPPY PARK", u: "https://blog.naver.com/martin301/223137384384" },
    { d: "2023.06.24", t: "카페 음향 유지보수(9BLOCK)", u: "https://blog.naver.com/martin301/223137381460" },
    { d: "2023.02.12", t: "하나복네트워크 동역회원수양회 음향", u: "https://blog.naver.com/martin301/223012920321" }
  ];

  /* ---------- 머리 · 진행 막대 · 맨 위로 ---------- */
  var hd = $('#hd'), totop = $('#totop'), prog = $('#progress');
  function onScroll() {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (hd) hd.classList.toggle('solid', y > 40);
    if (totop) totop.classList.toggle('on', y > 700);
    if (prog) prog.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  // 현재 페이지 메뉴 표시
  var cur = (location.pathname.split('/').pop() || 'index.html');
  $$('.hd .menu a, .sheet nav a').forEach(function (a) { if (a.getAttribute('href') === cur) a.classList.add('act'); });

  var burger = $('#burger'), sheet = $('#sheet');
  function closeSheet() { sheet.classList.remove('on'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
  if (burger && sheet) {
    burger.addEventListener('click', function () { sheet.classList.add('on'); burger.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; });
    $$('a, .x', sheet).forEach(function (a) { a.addEventListener('click', closeSheet); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet.classList.contains('on')) closeSheet(); });
  }

  /* ---------- 히어로 영상 (폰은 작은 영상, 움직임 줄이기 설정이면 포스터만) ---------- */
  var video = $('#heroVideo');
  if (video) {
    var vbtn = $('#vbtn');
    // H.264(mp4)를 못 트는 브라우저는 webm(VP9)으로
    var pickSrc = function () { if (!video.canPlayType('video/mp4; codecs="avc1.42E01E"')) return video.getAttribute('data-src-webm'); return window.innerWidth < 900 ? video.getAttribute('data-src-sm') : video.getAttribute('data-src'); };
    if (reduce) { video.removeAttribute('autoplay'); if (vbtn) vbtn.classList.add('paused'); }
    else {
      video.src = pickSrc();
      video.muted = true; video.setAttribute('muted', '');
      var tryPlay = function () { var p = video.play(); if (p && p.catch) p.catch(function () {}); };
      tryPlay(); video.addEventListener('canplay', tryPlay, { once: true });
      document.addEventListener('pointerdown', function () { if (video.paused && !video.dataset.userPaused) tryPlay(); }, { once: true });
      document.addEventListener('visibilitychange', function () { if (!document.hidden && !video.dataset.userPaused) tryPlay(); });
    }
    if (vbtn) vbtn.addEventListener('click', function () {
      if (!video.src) video.src = pickSrc();
      if (video.paused) { video.dataset.userPaused = ''; video.play(); vbtn.classList.remove('paused'); vbtn.setAttribute('aria-label', '배경 영상 멈춤'); }
      else { video.dataset.userPaused = '1'; video.pause(); vbtn.classList.add('paused'); vbtn.setAttribute('aria-label', '배경 영상 재생'); }
    });
  }

  /* ---------- 마퀴 (브랜드 글자 두 번 이어 붙이기) ---------- */
  $$('.marquee .track').forEach(function (t) { t.innerHTML += t.innerHTML; });

  /* ---------- 등장 ---------- */
  var revealEls = $$('.reveal');
  function checkReveal() {
    var h = window.innerHeight;
    revealEls = revealEls.filter(function (el) { if (el.getBoundingClientRect().top < h * .92) { el.classList.add('in'); return false; } return true; });
  }
  window.addEventListener('scroll', checkReveal, { passive: true }); window.addEventListener('resize', checkReveal); window.addEventListener('load', checkReveal);
  checkReveal(); setTimeout(checkReveal, 600);

  /* ---------- 단어 점등 (소개 문장이 스크롤에 따라 불이 켜짐) ---------- */
  var q = $('#litQuote');
  if (q) {
    var html = q.innerHTML.split(/(<em>.*?<\/em>|\s+)/).map(function (w) {
      if (!w || /^\s+$/.test(w)) return w;
      var hl = /^<em>/.test(w); w = w.replace(/<\/?em>/g, '');
      return '<span class="w' + (hl ? ' hl' : '') + '">' + w + '</span>';
    }).join('');
    q.innerHTML = html;
    var ws = $$('.w', q);
    var light = function () {
      var r = q.getBoundingClientRect(), vh = window.innerHeight;
      var k = reduce ? 1 : Math.max(0, Math.min(1, (vh * .85 - r.top) / (r.height + vh * .35)));
      var n = Math.round(ws.length * k);
      ws.forEach(function (w, i) { w.classList.toggle('lit', i < n); });
    };
    window.addEventListener('scroll', light, { passive: true }); light();
  }

  /* ---------- 하는 일 목록 (고르면 왼쪽 사진이 바뀜) ---------- */
  var wl = $('#wlist'), stage = $('#wstage');
  if (wl && stage) {
    var items = $$('li', wl), pics = $$('div', stage), lab = $('b', stage);
    var pick = function (i) {
      items.forEach(function (li, k) { li.classList.toggle('on', k === i); });
      pics.forEach(function (p, k) { p.classList.toggle('on', k === i); });
      if (lab) lab.textContent = items[i].getAttribute('data-en') || '';
    };
    items.forEach(function (li, i) { li.addEventListener('mouseenter', function () { pick(i); }); li.addEventListener('focusin', function () { pick(i); }); });
    pick(0);
  }

  /* ---------- 탭 공용 (실적 · 게시판) ---------- */
  $$('[data-tabs]').forEach(function (bar) {
    var bs = $$('button', bar), ps = $$(bar.getAttribute('data-tabs'));
    bs.forEach(function (b, i) {
      b.setAttribute('role', 'tab');
      b.addEventListener('click', function () {
        bs.forEach(function (x, k) { x.classList.toggle('on', k === i); x.setAttribute('aria-selected', k === i); });
        ps.forEach(function (p, k) { p.classList.toggle('on', k === i); });
        if (bar.id === 'btabs') history.replaceState(null, '', '#' + (b.getAttribute('data-id') || ''));
      });
    });
    var fromHash = function () { if (bar.id !== 'btabs' || !location.hash) return; var t = bar.querySelector('[data-id="' + location.hash.slice(1) + '"]'); if (t && !t.classList.contains('on')) t.click(); };
    fromHash(); window.addEventListener('hashchange', fromHash);
  });

  /* ---------- 갤러리 · 라이트박스 ---------- */
  function workCard(w, k) {
    return '<figure data-k="' + k + '" data-c="' + w.c + '" tabindex="0">' +
      '<img src="' + IMG + 't' + w.i + '.webp" alt="' + w.t + '" loading="lazy" width="800" height="600">' +
      '<figcaption><em>' + w.o + '</em>' + w.t + '</figcaption></figure>';
  }
  var gal = $('#gal'), pf = $('#pfGrid'), list = [];
  if (gal) { var pickK = (gal.getAttribute('data-pick') || '').split(',').map(Number); list = pickK.map(function (i) { return WORKS.filter(function (w) { return w.i === i; })[0]; }).filter(Boolean); gal.innerHTML = list.map(workCard).join(''); }
  if (pf) { list = WORKS; pf.innerHTML = list.map(workCard).join(''); }
  var grid = gal || pf, lb = $('#lb');
  if (grid && lb) {
    var figs = $$('figure', grid), lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), lbK = 0, lastFocus = null;
    var visible = function () { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); };
    var openLb = function (k) { var w = list[k]; lbK = k; lbImg.src = IMG + 'w' + w.i + '.webp'; lbImg.alt = w.t; lbT.textContent = w.t; lbM.textContent = w.o; if (!lb.classList.contains('on')) lastFocus = document.activeElement; lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('#lbX').focus(); };
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
      $$('button', filters).forEach(function (b) { var f = b.getAttribute('data-f'); var n = f === 'all' ? WORKS.length : WORKS.filter(function (w) { return w.c.split(' ').indexOf(f) >= 0; }).length; b.insertAdjacentHTML('beforeend', ' <small>' + n + '</small>'); });
      filters.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        $$('button', filters).forEach(function (x) { x.classList.remove('act'); }); b.classList.add('act');
        var f = b.getAttribute('data-f');
        figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
      });
    }
  }

  /* ---------- 공지 (대문 요약 · 공지 페이지 게시판) ---------- */
  var sorted = NOTICES.slice().sort(function (a, b) { return (b.top ? 1 : 0) - (a.top ? 1 : 0) || (a.d < b.d ? 1 : -1); });
  var nl = $('#noticeList');
  if (nl) nl.innerHTML = sorted.length ? sorted.slice(0, 4).map(function (n) { return '<li><b>' + n.t + (n.n ? '<span class="new">NEW</span>' : '') + '</b><small>' + n.d + '</small></li>'; }).join('') : '<li>등록된 공지가 없습니다.</li>';
  var nb = $('#noticeBoard');
  if (nb) {
    nb.innerHTML = sorted.length ? sorted.map(function (n, i) {
      return '<div class="row" tabindex="0" role="button" aria-expanded="false"><span class="no' + (n.top ? ' pin' : '') + '">' + (n.top ? '공지' : String(sorted.length - i).padStart(2, '0')) + '</span><b>' + n.t + (n.n ? '<span class="new" style="display:inline-block;margin-left:6px;font:700 10.5px/1 var(--kr);color:#fff;background:var(--amb);padding:3px 6px;border-radius:5px">NEW</span>' : '') + '</b><small>' + n.d + '</small>' + (n.b ? '<div class="body">' + n.b + '</div>' : '') + '</div>';
    }).join('') : '<div class="empty">등록된 공지가 없습니다.</div>';
    var tog = function (r) { var o = r.classList.toggle('open'); r.setAttribute('aria-expanded', o); };
    nb.addEventListener('click', function (e) { var r = e.target.closest('.row'); if (r) tog(r); });
    nb.addEventListener('keydown', function (e) { var r = e.target.closest('.row'); if (r && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); tog(r); } });
  }
  var fb = $('#fileBoard');
  if (fb) fb.innerHTML = FILES.length ? FILES.map(function (f) {
    var ext = /^https?:/.test(f.u);
    return '<div class="row"><span class="ic">' + f.k + '</span><span><b>' + f.t + '</b><br><small style="text-align:left">' + f.d + '</small></span><a class="btn btn-line" href="' + f.u + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + (f.k === 'FILE' ? '내려받기' : '열기') + '</a></div>';
  }).join('') : '<div class="empty">등록된 자료가 없습니다.</div>';

  /* ---------- 현장 이야기 (블로그 글 목록) ---------- */
  var bl = $('#blogList');
  if (bl) {
    var LIMIT = +bl.getAttribute('data-limit') || 10, shown = LIMIT;
    bl.innerHTML = BLOG.map(function (b, k) { return '<a href="' + b.u + '" target="_blank" rel="noopener"' + (k >= shown ? ' class="hide"' : '') + '><small>' + b.d + '</small><b>' + b.t + '</b><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M9 7h8v8"/></svg></a>'; }).join('');
    var more = $('#blogMore');
    if (more) {
      if (BLOG.length <= LIMIT) more.hidden = true;
      more.addEventListener('click', function () { shown += LIMIT; $$('a', bl).forEach(function (a, k) { a.classList.toggle('hide', k >= shown); }); if (shown >= BLOG.length) more.hidden = true; });
    }
  }

  /* ---------- 문의 보내기 ---------- */
  function isMobile() { return /iPhone|iPad|Android/i.test(navigator.userAgent); }
  function send(text, data, done) {
    if (FORM_ENDPOINT) {
      data.at = new Date().toISOString(); data.page = location.href; data.service = COMPANY + ' 행사 · 설치 문의'; data.message = text;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}).then(function () { done(true); });
      return;
    }
    if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {});
    done(false);
  }
  var form = $('#quoteForm');
  if (form) {
    var fdone = $('#formDone');
    // 대문 · 하는 일에서 넘어온 분야 (#k=교회행사)
    var km = location.hash.match(/k=([^&]+)/);
    if (km) { var want = decodeURIComponent(km[1]); $$('input[name=kind]', form).forEach(function (c) { if (c.value.indexOf(want) === 0) c.checked = true; }); }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // 스팸 봇 함정
      var d = {}; ['name', 'tel', 'org', 'date', 'place', 'people', 'msg'].forEach(function (k) { d[k] = form.elements[k] ? form.elements[k].value.trim() : ''; });
      d.kind = $$('input[name=kind]:checked', form).map(function (c) { return c.value; }).join(', ');
      if (!d.name || !d.tel) { alert('성함과 연락처는 꼭 적어 주세요.'); (d.name ? form.elements.tel : form.elements.name).focus(); return; }
      if (!$('#fAgree').checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); return; }
      var text = '[' + COMPANY + ' 문의]\n성함: ' + d.name + '\n연락처: ' + d.tel + '\n단체 · 회사: ' + (d.org || '-') + '\n분야: ' + (d.kind || '-') + '\n날짜: ' + (d.date || '-') + '\n장소: ' + (d.place || '-') + '\n규모: ' + (d.people || '-') + '\n내용: ' + (d.msg || '-');
      send(text, d, function (sent) {
        fdone.classList.add('on');
        if (!sent) $('p', fdone).innerHTML = '문의 내용을 복사해 두었습니다.<br><b>' + SMS_TO + '</b> 로 문자에 붙여 넣어 보내 주시거나 전화 주세요.';
      });
    });
    var again = $('#formAgain');
    if (again) again.addEventListener('click', function () { fdone.classList.remove('on'); });
  }
})();
