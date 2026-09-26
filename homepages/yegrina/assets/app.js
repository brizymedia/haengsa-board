/* 한국체대 예그리나 홈페이지 — 공통 스크립트 (외부 라이브러리 없음) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };

  /* ---------- 문의 폼 전송처 ----------
     FORM_ENDPOINT 가 비어 있으면 휴대폰에서는 문자 앱(대표 휴대폰)이 열리고, PC 에서는 내용을 복사해 준다.
     문의 서버(Apps Script) 주소를 넣으면 그쪽으로 JSON 이 가고, 서버가 knsuyegrina@naver.com 으로 메일을 보낸다. */
  var FORM_ENDPOINT = '';
  var SMS_TO = '010-9481-1934';
  var TEL = '02-482-1934';
  var COMPANY = '한국체대 예그리나';

  /* ---------- 공지 (소식 페이지 「공지」 탭 · 대문 공지) — 새 글은 맨 앞에 ----------
     b: 본문(선택, 줄바꿈 가능) · n: true 면 NEW 표시 */
  var NOTICES = [
    { d: '2026.09.26', t: '한국체대 예그리나 홈페이지를 새로 열었습니다.', n: true, b: '유아체육 수업 · 운동회 · 물놀이 · 놀이기구 렌탈 문의를 홈페이지에서도 받습니다.\n문의 폼을 남겨 주시면 확인 후 연락드립니다.' },
    { d: '2026.09.26', t: '2027년 봄 운동회 · 체육대회 상담을 받고 있습니다.', n: true, b: '운동회는 최소 6개월 전에 문의해 주시는 것이 좋습니다.\n날짜 · 장소(실내/야외) · 인원을 알려 주시면 프로그램을 맞춰 드립니다.' },
    { d: '2026.09.26', t: '2027년 신학기 유아체육 수업은 1월에 상담해 주세요.', b: '어린이집 · 유치원 유아체육 수업(동화체육 등)은 보통 신학기 전 1월에 정합니다.' },
    { d: '2026.09.26', t: '놀이기구 · 물놀이 · 천막 등 렌탈은 한 달 전부터 예약 가능합니다.' }
  ];

  /* ---------- 자료실 (소식 페이지 「자료실」 탭) ---------- */
  var FILES = [
    { d: '2026.09.26', t: '행사 · 수업 문의 전 체크리스트', f: 'assets/files/yegrina-checklist.txt', s: '1KB' }
  ];

  /* ---------- 현장 사진 (assets/img/works/w01 ~) ----------
     home: 1 이면 대문 사진 줄에도 나온다 · c: event 운동회·체육대회 · church 교회 행사 · water 물놀이 · rental 놀이기구·렌탈 · class 예체능 수업 · stage 발표회·무대 */
  var WORKS = [
    {f: "w01.webp", t: "초등학교 운동회 — 운동장 세팅", o: "운동회 · 초등학교 · 2026", c: "event", w: 800, h: 601, home: 1},
    {f: "w02.webp", t: "무지개 에어 장애물 달리기", o: "운동회 · 초등학교 · 2026", c: "event", w: 800, h: 601, home: 1},
    {f: "w03.webp", t: "대형 공 굴리기 단체 게임", o: "운동회 · 초등학교 · 2026", c: "event", w: 800, h: 601},
    {f: "w04.webp", t: "만국기 걸린 체육관 · 환영 아치", o: "운동회 · 실내 체육관 · 2026", c: "event", w: 800, h: 601},
    {f: "w05.webp", t: "가족한마음 체육대회 환영 아치", o: "체육대회 · 어린이집 · 유치원 · 2024", c: "event", w: 800, h: 601, home: 1},
    {f: "w06.webp", t: "온 가족이 함께하는 잔디 운동장 게임", o: "체육대회 · 어린이집 · 유치원 · 2024", c: "event", w: 800, h: 374},
    {f: "w07.webp", t: "잔디 운동장 공 모으기 게임", o: "체육대회 · 매년 찾는 원 · 2025", c: "event", w: 600, h: 800},
    {f: "w08.webp", t: "깃발 뒤집기 게임", o: "체육대회 · 매년 찾는 원 · 2025", c: "event", w: 600, h: 800},
    {f: "w09.webp", t: "유치원 가족 운동회 — 실내 체육관 세팅", o: "실내 체육대회 · 유치원 · 2024", c: "event", w: 800, h: 601},
    {f: "w10.webp", t: "진행 선생님들", o: "실내 체육대회 · 유치원 · 2024", c: "event", w: 800, h: 601},
    {f: "w11.webp", t: "전교인 한마음 체육대회 — 체육관 전경", o: "교회 체육대회 · 2026", c: "church", w: 800, h: 370, home: 1},
    {f: "w12.webp", t: "전 세대가 함께하는 레크리에이션", o: "교회 체육대회 · 2026", c: "church", w: 800, h: 370},
    {f: "w13.webp", t: "선수 입장", o: "교회 체육대회 · 2026", c: "church", w: 600, h: 800},
    {f: "w14.webp", t: "무대 진행 — 홍팀 · 청팀 점수판", o: "교회 체육대회 · 2026", c: "church stage", w: 800, h: 601},
    {f: "w15.webp", t: "부서별 단체 경기", o: "교회 체육대회 · 2026", c: "church", w: 800, h: 370},
    {f: "w16.webp", t: "대형 공 · 에어 캐릭터 세팅", o: "교회 체육대회 · 2026", c: "church", w: 800, h: 370},
    {f: "w17.webp", t: "풍선 이어달리기 진행", o: "교회 체육대회 · 2024", c: "church", w: 800, h: 534, home: 1},
    {f: "w18.webp", t: "풍선 기둥 · 단체 게임", o: "교회 체육대회 · 2024", c: "church", w: 533, h: 800},
    {f: "w19.webp", t: "에어 워터슬라이드 · 수영장", o: "물놀이 · 여름성경학교 · 2024", c: "water", w: 800, h: 601, home: 1},
    {f: "w20.webp", t: "유아용 낮은 수영장 여러 개", o: "물놀이 · 여름성경학교 · 2024", c: "water", w: 800, h: 601},
    {f: "w21.webp", t: "여름성경학교 환영 아치 · 포토존", o: "물놀이 · 여름성경학교 · 2024", c: "water", w: 800, h: 601},
    {f: "w22.webp", t: "비 오는 날 실내놀이터로 변경", o: "렌탈 · 실내놀이터 · 2024", c: "rental", w: 800, h: 601, home: 1},
    {f: "w23.webp", t: "에어 바운스 · 자이언트 빅블럭", o: "렌탈 · 실내놀이터 · 2024", c: "rental", w: 800, h: 601},
    {f: "w24.webp", t: "파라슈트 팝콘 튀기기 게임", o: "수업 · 유아체육 · 2024", c: "class", w: 800, h: 601, home: 1},
    {f: "w25.webp", t: "동화체육 — 창작동화로 여는 수업", o: "수업 · 동화체육 · 2024", c: "class", w: 436, h: 800},
    {f: "w26.webp", t: "유아 골프 퍼팅 수업", o: "수업 · 유아골프 · 2024", c: "class", w: 800, h: 374},
    {f: "w27.webp", t: "발표회 사회 — 객석과 함께", o: "발표회 · 사회 · 2026", c: "stage", w: 450, h: 800, home: 1},
    {f: "w28.webp", t: "교회 발표회 무대 진행", o: "발표회 · 사회 · 2026", c: "stage", w: 600, h: 800},
    {f: "w29.webp", t: "발표회 단상 진행", o: "발표회 · 사회 · 2026", c: "stage", w: 450, h: 800}
  ];
  var IMG = 'assets/img/works/';

  /* ---------- 블로그 글 (네이버 블로그 yegrinai — 「이벤트.행사」 · 「예체능 교육」 · 「렌탈」만) ---------- */
  var BLOG = [
    { d: '2026.06.29', c: '이벤트.행사', t: '전교인 체육대회', u: 'https://blog.naver.com/yegrinai/224330870862' },
    { d: '2026.03.06', c: '이벤트.행사', t: '초등학교 운동회', u: 'https://blog.naver.com/yegrinai/224207058180' },
    { d: '2026.03.05', c: '이벤트.행사', t: '발표회 진행 사회자', u: 'https://blog.naver.com/yegrinai/224205487218' },
    { d: '2025.07.10', c: '이벤트.행사', t: '다년간 연속 체육대회 운동회', u: 'https://blog.naver.com/yegrinai/223928519118' },
    { d: '2024.07.26', c: '렌탈', t: '실내놀이터 대여, 여름성경학교 놀이터대여', u: 'https://blog.naver.com/yegrinai/223526106582' },
    { d: '2024.07.17', c: '예체능 교육', t: '유아체육 파라슈트 수업', u: 'https://blog.naver.com/yegrinai/223516124692' },
    { d: '2024.07.16', c: '이벤트.행사', t: '여름성경학교 물놀이 행사, 포토존, 에어아바타까지 한번에', u: 'https://blog.naver.com/yegrinai/223514941397' },
    { d: '2024.07.03', c: '이벤트.행사', t: '실내체육대회 · 어린이집 · 유치원 체육대회', u: 'https://blog.naver.com/yegrinai/223500145912' },
    { d: '2024.07.02', c: '이벤트.행사', t: '전교인 체육대회, 교회체육대회', u: 'https://blog.naver.com/yegrinai/223498960203' },
    { d: '2024.07.01', c: '예체능 교육', t: '유아 골프수업', u: 'https://blog.naver.com/yegrinai/223497846692' },
    { d: '2024.06.28', c: '예체능 교육', t: '동화체육을 소개합니다 (유아체육)', u: 'https://blog.naver.com/yegrinai/223494511834' },
    { d: '2024.06.28', c: '회사 연혁', t: '회사 연혁', u: 'https://blog.naver.com/yegrinai/223494433970' },
    { d: '2024.06.28', c: '이벤트.행사', t: '가족한마음 체육대회, 어린이집 · 유치원 체육대회', u: 'https://blog.naver.com/yegrinai/223494283947' }
  ];

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- 상단: 진행 공 · 폰 메뉴 · 현재 메뉴 · 맨 위로 ---------- */
  var trk = $('#track'), totop = $('#totop');
  var trkBar = trk && $('i', trk), trkBall = trk && $('b', trk);
  var frame = $('#heroFrame');
  function onScroll() {
    var y = window.scrollY, max = document.documentElement.scrollHeight - window.innerHeight;
    if (trkBar) { var p = max > 0 ? y / max * 100 : 0; trkBar.style.width = p + '%'; trkBall.style.left = p + '%'; }
    if (totop) totop.classList.toggle('on', y > 700);
    if (frame && !reduce) { // 히어로 액자가 스크롤에 따라 살짝 물러난다
      var h = frame.offsetHeight, q = clamp(y / h, 0, 1);
      frame.style.transform = 'scale(' + (1 - q * .07).toFixed(4) + ')';
      frame.style.borderRadius = (34 + q * 30).toFixed(1) + 'px';
      frame.style.opacity = (1 - q * .35).toFixed(3);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); onScroll();
  if (totop) totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  var here = (location.pathname.split('/').pop() || 'index.html');
  $$('.menu a, .sheet nav a').forEach(function (a) { if (a.getAttribute('href') === here) a.classList.add('act'); });

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

  /* ---------- 히어로 영상: 폭 보고 고르기, 움직임 줄이기면 포스터만 ---------- */
  var hv = $('#heroVideo');
  if (hv) {
    if (reduce) { hv.removeAttribute('autoplay'); hv.pause && hv.pause(); }
    else {
      var src = hv.getAttribute(window.innerWidth <= 760 ? 'data-sm' : 'data-src');
      if (!hv.canPlayType('video/mp4; codecs="avc1.42E01E"') && hv.canPlayType('video/webm; codecs="vp9"')) src = src.replace(/\.mp4$/, '.webm'); // H.264 못 트는 브라우저는 webm
      hv.src = src;
      var pr = hv.play && hv.play(); if (pr && pr.catch) pr.catch(function () {});
    }
  }
  // 히어로 제목: 글자마다 통통 튀어 오르게
  var ht = $('#heroTitle');
  if (ht && !reduce) {
    var k = 0;
    $$('.ln', ht).forEach(function (ln) {
      var walk = function (node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var f = document.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(function (wd) { // 낱말은 한 덩어리로 (한글 낱자 줄바꿈 방지)
              if (!wd) return;
              if (/^\s+$/.test(wd)) { f.appendChild(document.createTextNode(' ')); return; }
              var w = document.createElement('span'); w.className = 'wd';
              wd.split('').forEach(function (ch) { var s = document.createElement('span'); s.className = 'ch'; s.style.setProperty('--i', k++); s.textContent = ch; w.appendChild(s); });
              f.appendChild(w);
            });
            n.parentNode.replaceChild(f, n);
          } else if (n.nodeType === 1) walk(n);
        });
      };
      walk(ln);
    });
  }

  /* ---------- 키워드 띠 ---------- */
  var roll = $('#roll');
  if (roll) { var words = roll.getAttribute('data-words').split('|'); var one = words.map(function (w) { return '<span>' + w + '</span>'; }).join(''); roll.innerHTML = one + one; }

  /* ---------- 등장 ---------- */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); e.target.classList.add('go'); io.unobserve(e.target); } });
  }, { threshold: .15, rootMargin: '0px 0px -6% 0px' });
  $$('.rv, .balls, .lanes, .certs').forEach(function (el) { io.observe(el); });
  $$('.certs li').forEach(function (li, i) { li.style.transitionDelay = (i * 40) + 'ms'; });

  /* ---------- 숫자 ---------- */
  var cio = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return; cio.unobserve(e.target);
      var el = e.target, to = +el.getAttribute('data-count'), from = +(el.getAttribute('data-from') || 0), t0 = null, dur = 1400;
      if (reduce) { el.textContent = to; return; }
      (function step(ts) { if (!t0) t0 = ts; var q = Math.min(1, (ts - t0) / dur); q = 1 - Math.pow(1 - q, 3); el.textContent = Math.round(from + (to - from) * q); if (q < 1) requestAnimationFrame(step); })(performance.now());
    });
  }, { threshold: .5 });
  $$('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------- 쌓이는 카드: 뒤 카드가 올라오면 앞 카드가 살짝 작아지고 어두워진다 ---------- */
  var cards = $$('.card3');
  if (cards.length && !reduce) {
    var stackTick = function () {
      cards.forEach(function (c, i) {
        var nx = cards[i + 1]; if (!nx) { c.style.transform = ''; c.style.filter = ''; return; }
        var r = nx.getBoundingClientRect(), top = parseFloat(getComputedStyle(nx).top) || 0, h = c.offsetHeight;
        var q = clamp(1 - (r.top - top) / h, 0, 1);
        c.style.transform = 'scale(' + (1 - q * .06).toFixed(4) + ')';
        c.style.filter = 'brightness(' + (1 - q * .22).toFixed(3) + ')';
      });
    };
    window.addEventListener('scroll', function () { requestAnimationFrame(stackTick); }, { passive: true }); stackTick();
  }

  /* ---------- 연혁: 트랙이 차오르고 지나간 해에 불이 켜진다 ---------- */
  var hist = $('.hist');
  if (hist) {
    var railI = $('.rail i', hist), yrs = $$('.yr', hist);
    var histTick = function () {
      var r = hist.getBoundingClientRect(), mid = window.innerHeight * .55;
      var p = clamp((mid - r.top) / r.height, 0, 1);
      railI.style.height = (p * 100) + '%';
      yrs.forEach(function (y) { y.classList.toggle('on', y.getBoundingClientRect().top < mid); });
    };
    window.addEventListener('scroll', function () { requestAnimationFrame(histTick); }, { passive: true }); histTick();
  }

  /* ---------- 문의 띠 색종이 ---------- */
  $$('.confetti').forEach(function (box) {
    if (reduce) return;
    var cols = ['#FFC928', '#FF6B4A', '#38A8F5', '#C6F16D', '#fff'], h = '';
    for (var i = 0; i < 22; i++) h += '<i style="left:' + (Math.random() * 100).toFixed(1) + '%;background:' + cols[i % cols.length] + ';animation-duration:' + (6 + Math.random() * 7).toFixed(1) + 's;animation-delay:' + (-Math.random() * 12).toFixed(1) + 's"></i>';
    box.innerHTML = h;
  });

  /* ---------- 사진: 대문 줄 · 현장사진 격자 · 라이트박스 ---------- */
  function fig(w, k, cls) {
    return '<figure data-k="' + k + '" data-c="' + w.c + '"' + (cls ? ' class="' + cls + '"' : '') + '><img src="' + IMG + 's/' + w.f + '" alt="' + esc(w.t) + '" loading="lazy" width="' + (w.w || 800) + '" height="' + (w.h || 600) + '">' +
      '<figcaption><small>' + esc(w.o) + '</small>' + esc(w.t) + '</figcaption></figure>';
  }
  var strip = $('#strip'), grid = $('#pfGrid'), list = [];
  if (strip) { list = WORKS.filter(function (w) { return w.home; }); strip.innerHTML = list.map(function (w, k) { return fig(w, k); }).join(''); }
  if (grid) { list = WORKS; grid.innerHTML = list.map(function (w, k) { return fig(w, k); }).join(''); }
  var host = strip || grid, lb = $('#lb');
  if (host && lb) {
    var figs = $$('figure', host), lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), cur = 0;
    var vis = function () { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); };
    var openLb = function (k) { var w = list[k]; cur = k; lbImg.src = IMG + w.f; lbImg.alt = w.t; lbT.textContent = w.t; lbM.textContent = w.o; lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('#lbX').focus(); };
    var closeLb = function () { lb.classList.remove('on'); document.body.style.overflow = ''; };
    var stepLb = function (d) { var v = vis(), i = v.indexOf(cur); openLb(v[(i + d + v.length) % v.length]); };
    host.addEventListener('click', function (e) { var f = e.target.closest('figure'); if (f) openLb(+f.getAttribute('data-k')); });
    $('#lbX').addEventListener('click', closeLb);
    $('#lbPrev').addEventListener('click', function () { stepLb(-1); });
    $('#lbNext').addEventListener('click', function () { stepLb(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) { if (!lb.classList.contains('on')) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowLeft') stepLb(-1); if (e.key === 'ArrowRight') stepLb(1); });
    var filters = $('#filters');
    if (filters) filters.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      $$('button', filters).forEach(function (x) { x.classList.remove('act'); x.setAttribute('aria-pressed', 'false'); });
      b.classList.add('act'); b.setAttribute('aria-pressed', 'true');
      var f = b.getAttribute('data-f');
      figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
    });
  }
  // 줄 넘김 단추
  $$('[data-strip]').forEach(function (b) {
    b.addEventListener('click', function () { var s = $('#' + b.getAttribute('data-strip')); s.scrollBy({ left: (+b.getAttribute('data-d')) * s.clientWidth * .8, behavior: reduce ? 'auto' : 'smooth' }); });
  });

  /* ---------- 공지 · 블로그 목록 ---------- */
  var hn = $('#homeNotice');
  if (hn) hn.innerHTML = NOTICES.slice(0, 4).map(function (n) { return '<li><b>' + esc(n.t) + (n.n ? '<span class="new">NEW</span>' : '') + '</b><small>' + n.d + '</small></li>'; }).join('') || '<li class="empty">등록된 공지가 없습니다.</li>';
  var hb = $('#homeBlog');
  if (hb) hb.innerHTML = BLOG.slice(0, 4).map(function (b) { return '<a class="row" href="' + b.u + '" target="_blank" rel="noopener"><b><span class="cat">' + esc(b.c) + '</span>' + esc(b.t) + '</b><small>' + b.d + '</small></a>'; }).join('');

  var pn = $('#paneNotice'), pbd = $('#paneBoard'), pf = $('#paneFiles');
  if (pn) pn.innerHTML = '<div class="row hd"><span class="n">번호</span><span>제목</span><span class="d">날짜</span></div>' + (NOTICES.length ? NOTICES.map(function (n, i) {
    var title = esc(n.t) + (n.n ? '<span class="new" style="margin-left:8px;font-size:11px;font-weight:800;padding:1px 7px;border-radius:999px;background:#FF6B4A;color:#fff">NEW</span>' : '');
    return '<div class="row"><span class="n">' + (NOTICES.length - i) + '</span>' + (n.b ? '<details><summary>' + title + '</summary><p>' + esc(n.b) + '</p></details>' : '<b style="font-weight:600">' + title + '</b>') + '<span class="d">' + n.d + '</span></div>';
  }).join('') : '<div class="empty">등록된 공지가 없습니다.</div>');
  if (pbd) pbd.innerHTML = '<div class="row hd"><span class="n">분류</span><span>제목 (네이버 블로그로 이동)</span><span class="d">날짜</span></div>' + BLOG.map(function (b) {
    return '<a class="row" href="' + b.u + '" target="_blank" rel="noopener"><span class="n">' + esc(b.c) + '</span><b style="font-weight:600">' + esc(b.t) + ' ↗</b><span class="d">' + b.d + '</span></a>';
  }).join('');
  if (pf) pf.innerHTML = '<div class="row hd"><span class="n">번호</span><span>자료</span><span class="d">날짜</span></div>' + (FILES.length ? FILES.map(function (f, i) {
    return '<div class="row"><span class="n">' + (FILES.length - i) + '</span><span><b style="font-weight:600">' + esc(f.t) + '</b> <a class="file" href="' + f.f + '" download>내려받기 (' + f.s + ')</a></span><span class="d">' + f.d + '</span></div>';
  }).join('') : '<div class="empty">등록된 자료가 없습니다.</div>');
  var cN = $('#cntNotice'), cB = $('#cntBoard'), cF = $('#cntFiles');
  if (cN) cN.textContent = NOTICES.length; if (cB) cB.textContent = BLOG.length; if (cF) cF.textContent = FILES.length;

  /* ---------- 탭 ---------- */
  $$('.tabs').forEach(function (tabs) {
    var bs = $$('button', tabs), panes = bs.map(function (b) { return $('#' + b.getAttribute('aria-controls')); });
    function show(i) { bs.forEach(function (b, k) { b.classList.toggle('on', k === i); b.setAttribute('aria-selected', k === i); panes[k].classList.toggle('on', k === i); }); }
    bs.forEach(function (b, i) { b.addEventListener('click', function () { show(i); history.replaceState(null, '', '#' + b.getAttribute('data-hash')); }); });
    var h = location.hash.slice(1); bs.forEach(function (b, i) { if (b.getAttribute('data-hash') === h) show(i); });
  });

  /* ---------- 하는 일: 소메뉴 현재 위치 ---------- */
  var sn = $('.subnav');
  if (sn) {
    var sl = $$('a', sn), secs = sl.map(function (a) { return $(a.getAttribute('href')); });
    var snTick = function () { var k = 0; secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < window.innerHeight * .4) k = i; }); sl.forEach(function (a, i) { a.classList.toggle('act', i === k); }); };
    window.addEventListener('scroll', function () { requestAnimationFrame(snTick); }, { passive: true }); snTick();
  }

  /* ---------- 문의 보내기 (문의 폼 · 채용 지원 공용) ---------- */
  function isMobile() { return /iPhone|iPad|Android/i.test(navigator.userAgent); }
  function send(text, data, done, service) {
    if (FORM_ENDPOINT) {
      data.at = new Date().toISOString(); data.page = location.href; data.service = service; data.message = text;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}).then(function () { done(true); });
      return;
    }
    if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {});
    done(false);
  }
  function val(form, k) { var el = form.elements[k]; if (!el) return ''; if (el.length && !el.tagName) return Array.prototype.slice.call(el).filter(function (x) { return x.checked; }).map(function (x) { return x.value; }).join(', '); return (el.value || '').trim(); }

  var form = $('#quoteForm');
  if (form) {
    var fd = $('#formDone');
    var qs = location.hash.match(/^#s=(\w+)/); // 하는 일에서 넘어온 종류 미리 고르기
    if (qs) { var pre = $('input[name="kind"][value^="' + { event: '운동회', class: '유아', rental: '렌탈', water: '물놀이' }[qs[1]] + '"]', form); if (pre) pre.checked = true; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // 스팸 봇 함정
      var d = {}; ['name', 'tel', 'org', 'kind', 'date', 'place', 'people', 'msg'].forEach(function (k) { d[k] = val(form, k); });
      if (!d.name || !d.tel) { alert('담당자 이름과 연락처는 꼭 적어 주세요.'); (d.name ? form.elements.tel : form.elements.name).focus(); return; }
      if (!$('#fAgree').checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); return; }
      var text = '[' + COMPANY + ' 문의]\n담당자: ' + d.name + '\n연락처: ' + d.tel + '\n기관: ' + (d.org || '-') + '\n문의 종류: ' + (d.kind || '-') + '\n날짜: ' + (d.date || '-') + '\n장소: ' + (d.place || '-') + '\n인원: ' + (d.people || '-') + '\n내용: ' + (d.msg || '-');
      send(text, d, function (sent) {
        fd.classList.add('on');
        if (!sent) $('p', fd).innerHTML = '문의 내용을 복사해 두었습니다.<br><b>' + TEL + '</b> 로 전화 주시거나 <b>' + SMS_TO + '</b> 로 문자에 붙여 넣어 보내 주세요.';
      }, '행사 · 수업 문의');
    });
  }
  var jf = $('#jobForm');
  if (jf) {
    var jd = $('#jobDone');
    jf.addEventListener('submit', function (e) {
      e.preventDefault();
      if (jf.elements.website && jf.elements.website.value) return;
      var d = {}; ['name', 'tel', 'part', 'area', 'certs', 'msg'].forEach(function (k) { d[k] = val(jf, k); });
      if (!d.name || !d.tel) { alert('이름과 연락처는 꼭 적어 주세요.'); (d.name ? jf.elements.tel : jf.elements.name).focus(); return; }
      if (!$('#jAgree').checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); return; }
      var text = '[' + COMPANY + ' 채용 문의]\n이름: ' + d.name + '\n연락처: ' + d.tel + '\n지원 분야: ' + (d.part || '-') + '\n활동 지역: ' + (d.area || '-') + '\n자격 · 경력: ' + (d.certs || '-') + '\n하고 싶은 말: ' + (d.msg || '-');
      send(text, d, function (sent) {
        jd.classList.add('on');
        if (!sent) $('p', jd).innerHTML = '내용을 복사해 두었습니다.<br><b>' + SMS_TO + '</b> 로 문자에 붙여 넣어 보내 주시거나 knsuyegrina@naver.com 으로 이력서와 함께 보내 주세요.';
      }, '채용 문의');
    });
  }
})();
