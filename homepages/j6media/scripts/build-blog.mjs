/**
 * 제이식스미디어 블로그 — _blog/posts/*.json 을 홈페이지 글로 만든다
 * ──────────────────────────────────────────────────────
 *   /blog/               글 목록 (최신순, 24개씩 → /blog/page/2/)
 *   /blog/<지역>/        지역별 모음 (예: /blog/namyangju/)
 *   /blog/<글주소>/      글 하나
 *   /rss.xml             블로그 RSS
 *   sitemap.xml · llms.txt 의 블로그 부분도 같이 갱신한다
 *
 * 원본은 _blog/ 에 둔다. 밑줄로 시작하는 폴더는 GitHub Pages(Jekyll)가 공개하지 않는다.
 * blog/ 는 매번 지우고 새로 만든다 — 결과 HTML 을 손으로 고치지 말고 원본 JSON 이나 이 템플릿을 고친다.
 * (바로기획 scripts/build-blog.mjs 를 제이식스미디어에 맞게 옮긴 것.)
 *  - 사이트 틀(머리글 · 휴대폰 메뉴 · 바닥글)은 notice.html 에서 빌려 온다 — tools/make_pages.py 와 같은 방식.
 *    그래서 메뉴를 고칠 때는 notice.html 을 고치고 make_pages.py → 이 스크립트 순서로 다시 돌리면 된다.
 *  - 모양은 assets/style.css(변수 · 클래스, 맨 끝 「행사 준비 블로그」 절)를 쓴다.
 *  - 사진은 /assets/img/works/wN.webp(목록 카드는 같은 번호 tN.webp).
 *  - 이 사이트의 다른 페이지처럼 링크는 상대 주소(../)로 바꿔 쓴다. 글 JSON 안에서는 / 로 시작하는 주소로 적는다.
 *  - 기준 주소(canonical · sitemap · llms · rss)는 CNAME 의 www.j6media.co.kr.
 *
 * 실행:  node scripts/build-blog.mjs      글 형식 · 규칙: _blog/GUIDE.md   ·   검사: node scripts/blog-check.mjs
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SITE = 'https://www.j6media.co.kr';
export const BRAND = '제이식스미디어';
const TEL = '010-4450-4212';
const 쪽당 = 24;

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 글 안에서는 **굵게** 와 [글자](주소) 만 쓴다. 주소는 / 로 시작하거나 https:// 여야 한다.
 *  / 로 시작하는 주소는 사이트 기준 상대 주소(앞의 / 를 뗀 것)로 바꿔 두고, 페이지를 쓸 때 깊이에 맞춰 ../ 를 붙인다. */
export function 인라인(글) {
  return esc(글)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(((?:\/|https:\/\/)[^)\s]*)\)/g, (m, t, u) =>
      u.startsWith('/') ? `<a href="${u.slice(1) || 'index.html'}">${t}</a>` : `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
}
export const 글자만 = (글) => String(글 ?? '').replace(/\*\*(.+?)\*\*/g, '$1').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');
export const 날짜글 = (d) => { const m = String(d || '').match(/^(\d{4})-(\d{2})-(\d{2})$/); return m ? `${m[1]}년 ${+m[2]}월 ${+m[3]}일` : String(d || ''); };
export const 글주소 = (slug) => `/blog/${encodeURIComponent(slug)}/`;

export function 지역표(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'regions.json'), 'utf8'));
  const 표 = new Map(j.지역.map((r) => [r.slug, r]));
  표.set('common', { slug: 'common', 이름: '행사 준비 공통', 서비스페이지: '', 이동: '', 비중: 0 });
  return 표;
}

/** photos.json 의 묶음을 사진 한 장씩 풀어 경로 → 정보 로 */
export function 사진목록(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'photos.json'), 'utf8'));
  const 표 = new Map();
  j.묶음.forEach((g, i) => { (g.path || []).forEach((p) => 표.set(p, { ...g, path: p, 묶음번호: i })); });
  return 표;
}

export function 글읽기(ROOT) {
  const 폴더 = resolve(ROOT, '_blog', 'posts');
  if (!existsSync(폴더)) return [];
  return readdirSync(폴더).filter((f) => f.endsWith('.json')).map((f) => {
    const p = JSON.parse(readFileSync(resolve(폴더, f), 'utf8'));
    Object.defineProperty(p, '_파일', { value: f, enumerable: false });
    return p;
  }).sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : a.slug < b.slug ? -1 : 1));
}

/** 본문 글자 — 읽는 시간·검사·중복 비교에 쓴다 */
export function 본문글(p) {
  const 조각 = [p.lead, ...(p.points || [])];
  for (const s of p.sections || []) {
    조각.push(s.h2);
    for (const b of s.blocks || []) {
      if (b.p) 조각.push(b.p);
      if (b.tip) 조각.push(b.tip);
      if (b.ul) 조각.push(...b.ul);
      if (b.ol) 조각.push(...b.ol);
      if (b.table) 조각.push(...(b.table.head || []), ...(b.table.rows || []).flat());
    }
  }
  for (const f of p.faq || []) 조각.push(f.q, f.a);
  return 조각.map(글자만).join('\n');
}

export function 글이미지들(p) {
  const 목록 = p.cover ? [p.cover] : [];
  for (const s of p.sections || []) for (const b of s.blocks || []) if (b.img) 목록.push(b.img);
  return 목록;
}

const 작은사진 = (path) => String(path).replace('/assets/img/works/w', '/assets/img/works/t');
const 사이트경로 = (path) => String(path).replace(/^\//, '');   // '/assets/…' → 'assets/…' (나중에 ../ 를 붙인다)

const ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>';

/** notice.html 에서 머리글 · 휴대폰 메뉴 · 바닥글을 빌려 온다(make_pages.py 의 shell() 과 같은 자리) */
function 틀(ROOT) {
  const s = readFileSync(resolve(ROOT, 'notice.html'), 'utf8').replace(/\r\n/g, '\n');
  const 머리끝 = s.indexOf('</head>');
  const 몸시작 = s.indexOf('<body>') + '<body>'.length;
  const 본문시작 = s.indexOf('<section class="phead">');
  const 본문끝 = s.indexOf('</main>') + '</main>'.length;
  if (머리끝 < 0 || 본문시작 < 0 || 본문끝 < 7) throw new Error('notice.html 의 틀을 찾지 못했다(<section class="phead"> · </main>)');
  const 헤드 = s.slice(0, 머리끝);
  const 링크 = (re) => { const m = 헤드.match(re); return m ? m[0] : ''; };
  return {
    아이콘: 링크(/<link rel="icon"[^\n]*/),
    글꼴: [링크(/<link rel="preconnect"[^\n]*/), 링크(/<link href="https:\/\/fonts\.googleapis\.com[^\n]*/)].join('\n'),
    스타일: 링크(/<link rel="stylesheet" href="assets\/style\.css[^"]*">/),
    통계: 링크(/<script defer src="https:\/\/www\.ai-make\.co\.kr\/stats\/stats\.js"[^>]*><\/script>/),
    위: s.slice(몸시작, 본문시작)
      .replace(/(<nav class="menu"[^>]*>[\s\S]*?)<a href="blog\/">/, '$1<a href="blog/" class="act" aria-current="page">')
      .replace(/(<div class="sheet"[\s\S]*?<nav>[\s\S]*?)<a href="blog\/">/, '$1<a href="blog/" class="act">'),
    아래: s.slice(본문끝).replace(/<script src="assets\/edit\.js[^"]*"><\/script>\n?/, ''),   // 대표님 수정 모드는 기본 페이지에만
  };
}

/** 사이트 기준 상대 주소에 깊이만큼 ../ 를 붙인다(make_pages.py 의 page() 와 같은 규칙) */
function 깊이맞춤(html, 깊이) {
  const pre = '../'.repeat(깊이);
  return html
    .replace(/(href|src|poster)="(?!https?:|mailto:|tel:|sms:|#|\/|\.\.\/|data:)([^"]*)"/g, (m, a, u) => `${a}="${pre}${u}"`)
    .replace(/url\((?!https?:)(assets\/[^)]+)\)/g, (m, u) => `url(${pre}${u})`);
}

export function buildBlog(옵션 = {}) {
  const ROOT = 옵션.ROOT;
  const 사진주소 = (path) => SITE + String(path).split('/').map(encodeURIComponent).join('/');   // 절대 주소(og · JSON-LD 용)
  const 지역 = 지역표(ROOT);
  const posts = 글읽기(ROOT);
  const T = 틀(ROOT);
  const 발행처 = { '@type': 'LocalBusiness', '@id': SITE + '/#business', name: BRAND, url: SITE + '/', logo: SITE + '/assets/img/logo.png', telephone: '+82-10-4450-4212' };
  const 제이슨 = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;

  rmSync(resolve(ROOT, 'blog'), { recursive: true, force: true });
  const 쓰기 = (폴더, html) => {
    const d = resolve(ROOT, 폴더);
    mkdirSync(d, { recursive: true });
    const 깊이 = 폴더.split('/').length;     // blog → 1, blog/x → 2, blog/page/2 → 3
    writeFileSync(resolve(d, 'index.html'), 깊이맞춤(html, 깊이), 'utf8');
  };

  const 머리 = ({ 제목, 설명, 경로, 이미지, 종류 = 'website', 더넣기 = '', 색인 = true }) => `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(제목)}</title>
<meta name="description" content="${esc(설명)}">
<meta name="robots" content="${색인 ? 'index,follow,max-image-preview:large' : 'noindex,follow'}">
<meta name="theme-color" content="#221913">
<link rel="canonical" href="${SITE}${경로}">
<link rel="alternate" type="application/rss+xml" title="${BRAND} 행사 준비 블로그" href="${SITE}/rss.xml">
<meta property="og:type" content="${종류}">
<meta property="og:site_name" content="제이식스미디어 J6 MEDIA">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="${esc(제목)}">
<meta property="og:description" content="${esc(설명)}">
<meta property="og:url" content="${SITE}${경로}">
<meta property="og:image" content="${esc(이미지)}">
<meta name="twitter:card" content="summary_large_image">
${더넣기}
${T.아이콘}
${T.글꼴}
${T.스타일}
${T.통계}
</head>
<body>${T.위}`;

  const 꼬리 = (본문) => `${본문}\n</main>${T.아래}`;

  const 페이지머리 = ({ 배경, 눈썹, 제목, 소개, 길 }) => `<section class="phead">
  <div class="bg" style="background-image:url(${사이트경로(배경)})"></div>
  <div class="wrap">
    <p class="eyebrow">${눈썹}</p>
    <h1>${esc(제목)}</h1>
    <p>${소개}</p>
    <div class="crumb"><a href="index.html">홈</a>${길.map(([n, h]) => `<span>›</span>${h ? `<a href="${h}">${esc(n)}</a>` : `<span>${esc(n)}</span>`}`).join('')}</div>
  </div>
</section>

<main>`;

  const 상담 = `<section class="sec" style="padding-top:clamp(48px,6vw,72px)">
  <div class="wrap">
    <div class="ctaband">
      <div class="eq" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <div><h2>행사 날짜가 잡히셨나요?</h2><p>날짜와 장소, 대략의 규모만 알려 주세요. 현장에 맞는 구성을 함께 찾아 드립니다. (월~토 09:00~18:00)</p></div>
      <div class="btns"><a class="btn btn-w" href="tel:${TEL}">${PHONE}${TEL}</a><a class="btn btn-ink" href="quote.html">자동 견적서${ARROW}</a></div>
    </div>
  </div>
</section>`;

  const 카드 = (p) => {
    const r = 지역.get(p.region);
    return `<a class="stcard" href="blog/${encodeURIComponent(p.slug)}/"><img src="${esc(사이트경로(작은사진(p.cover.path)))}" alt="${esc(p.cover.alt)}" loading="lazy" decoding="async" width="800" height="500">`
      + `<span><small>${esc(r ? r.이름 : '')} · ${esc(날짜글(p.date))}</small>${esc(p.title)}<em>${esc(p.description)}</em></span></a>`;
  };

  const 개수 = new Map();
  posts.forEach((p) => 개수.set(p.region, (개수.get(p.region) || 0) + 1));
  const 칩 = (현재) => `<nav class="bchips" aria-label="지역별 글">
    <a href="blog/"${현재 === '' ? ' class="act" aria-current="page"' : ''}>전체<small>${posts.length}</small></a>
    ${[...지역.values()].filter((r) => 개수.get(r.slug)).map((r) =>
      `<a href="blog/${r.slug}/"${현재 === r.slug ? ' class="act" aria-current="page"' : ''}>${esc(r.이름)}<small>${개수.get(r.slug)}</small></a>`).join('\n    ')}
  </nav>`;
  const 지역이름 = (r) => (r.도 ? `${r.도} ${r.시군}` : r.시군);

  /* ── 글 페이지 ── */
  const 이미지html = (im, 표지) => `<figure class="bfig${표지 ? ' cover' : ''}">
    <img src="${esc(사이트경로(im.path))}" alt="${esc(im.alt)}" ${표지 ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" width="1600" height="${표지 ? 900 : 1200}">
    <figcaption>${인라인(im.caption)}</figcaption>
  </figure>`;
  const 블록 = (b) => {
    if (b.p) return `<p>${인라인(b.p)}</p>`;
    if (b.tip) return `<div class="btip">${인라인(b.tip)}</div>`;
    if (b.ul) return `<ul>${b.ul.map((x) => `<li>${인라인(x)}</li>`).join('')}</ul>`;
    if (b.ol) return `<ol>${b.ol.map((x) => `<li>${인라인(x)}</li>`).join('')}</ol>`;
    if (b.table) return `<div class="btbl"><table><thead><tr>${b.table.head.map((h) => `<th scope="col">${인라인(h)}</th>`).join('')}</tr></thead><tbody>${
      b.table.rows.map((row) => `<tr>${row.map((c) => `<td>${인라인(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    if (b.img) return 이미지html(b.img, false);
    return '';
  };

  for (const p of posts) {
    const r = 지역.get(p.region) || { 이름: '', 서비스페이지: '' };
    const 지역글 = p.region !== 'common';
    const 경로 = 글주소(p.slug);
    const 분 = Math.max(1, Math.round(본문글(p).length / 500));
    const 관련 = [...posts.filter((o) => o !== p && o.region === p.region),
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic === p.topic),
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic !== p.topic)].slice(0, 3);

    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        ...(지역글 ? [{ '@type': 'ListItem', position: 3, name: r.이름 + ' 행사 준비', item: `${SITE}/blog/${p.region}/` }] : []),
        { '@type': 'ListItem', position: 지역글 ? 4 : 3, name: p.title, item: SITE + 경로 } ] },
      { '@type': 'BlogPosting', '@id': SITE + 경로, headline: p.title, description: p.description,
        image: 글이미지들(p).map((im) => 사진주소(im.path)),
        datePublished: p.date, dateModified: p.updated || p.date, inLanguage: 'ko',
        keywords: [p.keyword.main, ...(p.keyword.sub || [])].join(', '),
        author: { '@type': 'Organization', name: BRAND, url: SITE + '/' },
        publisher: 발행처,
        mainEntityOfPage: { '@type': 'WebPage', '@id': SITE + 경로 },
        ...(지역글 ? { spatialCoverage: { '@type': 'Place', name: 지역이름(r) } } : {}) },
      ...((p.faq || []).length ? [{ '@type': 'FAQPage', '@id': SITE + 경로 + '#faq',
        mainEntity: p.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: 글자만(f.a) } })) }] : []),
    ] };

    const 본문 = `
<section class="sec white" style="padding-top:clamp(40px,6vw,64px)">
  <div class="wrap">
  <article class="bpost">
  <div class="bmeta">
    ${지역글 ? `<a class="chip" href="blog/${p.region}/">${esc(r.이름)} 글 모음</a>` : ''}
    ${r.서비스페이지 ? `<a class="chip" href="${사이트경로(r.서비스페이지)}">${esc(r.이름)} 음향 · 설치 안내</a>` : ''}
    <span class="chip">${esc(날짜글(p.date))}</span>
    <span class="chip">읽는 시간 약 ${분}분</span>
  </div>
  <p class="blead">${인라인(p.lead)}</p>
  ${이미지html(p.cover, true)}
  <div class="bpoints"><b>이 글의 요점</b><ul>${p.points.map((x) => `<li>${인라인(x)}</li>`).join('')}</ul></div>
  <nav class="btoc" aria-label="목차"><b>목차</b><ol>${p.sections.map((s, i) => `<li><a href="#s${i + 1}">${esc(s.h2)}</a></li>`).join('')}</ol></nav>
  <div class="bbody">
${p.sections.map((s, i) => `<h2 id="s${i + 1}">${esc(s.h2)}</h2>\n${s.blocks.map(블록).join('\n')}`).join('\n')}
  </div>
  ${(p.faq || []).length ? `<section class="bfaq" id="faq"><h2>자주 묻는 질문</h2>${p.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${인라인(f.a)}</p></details>`).join('')}</section>` : ''}
  ${(p.sources || []).length ? `<div class="bsrc"><b>확인한 자료</b> (${esc(날짜글(p.updated || p.date))} 기준)<ul>${p.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>`).join('')}</ul></div>` : ''}
  </article>
  </div>
</section>
${관련.length ? `<section class="sec sand"><div class="wrap"><div class="sec-head"><div class="t"><p class="eyebrow">More Posts</p><h2 class="h2">같이 보면 <em>좋은 글</em>.</h2></div><a class="btn btn-line" href="blog/">전체 보기${ARROW}</a></div><div class="stcards">${관련.map(카드).join('\n')}</div></div></section>` : ''}
${상담}`;

    const html = 머리({ 제목: `${p.title} | ${BRAND}`, 설명: p.description, 경로, 이미지: 사진주소(p.cover.path), 종류: 'article',
      더넣기: `<meta property="article:published_time" content="${p.date}">\n${제이슨(ld)}` })
      + 페이지머리({ 배경: p.cover.path, 눈썹: `Blog · ${esc(지역글 ? r.이름 + ' 행사 준비' : '행사 준비')}`, 제목: p.title, 소개: esc(p.description),
        길: [['블로그', 'blog/'], ...(지역글 ? [[r.이름, `blog/${p.region}/`]] : []), ['글', '']] })
      + 꼬리(본문);
    쓰기(`blog/${p.slug}`, html);
  }

  /* ── 목록 (/blog/, /blog/page/N/) ── */
  const 대표이미지 = posts[0] ? 사진주소(posts[0].cover.path) : `${SITE}/assets/img/og.jpg`;
  const 쪽수 = Math.max(1, Math.ceil(posts.length / 쪽당));
  const 지역들 = [...지역.values()].filter((r) => r.slug !== 'common').map((r) => r.이름).join(' · ');
  for (let n = 1; n <= 쪽수; n++) {
    const 조각 = posts.slice((n - 1) * 쪽당, n * 쪽당);
    const 경로 = n === 1 ? '/blog/' : `/blog/page/${n}/`;
    const 쪽나눔 = 쪽수 > 1 ? `<nav class="bpager" aria-label="쪽 이동">${Array.from({ length: 쪽수 }, (_, i) => i + 1).map((k) =>
      k === n ? `<span aria-current="page">${k}</span>` : `<a href="${k === 1 ? 'blog/' : `blog/page/${k}/`}">${k}</a>`).join('')}</nav>` : '';
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' } ] },
      { '@type': 'Blog', '@id': SITE + '/blog/', name: `${BRAND} 행사 준비 블로그`, inLanguage: 'ko', publisher: 발행처,
        blogPost: 조각.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug), datePublished: p.date, image: 사진주소(p.cover.path) })) } ] };
    const 소개 = '예배 · 수련회 · 세미나 · 공연 · 학교 축제 · 공식 행사를 맡은 담당자가 먼저 확인할 음향 · 조명 준비를 지역별로 정리합니다.';
    const html = 머리({
      제목: n === 1 ? `행사 준비 블로그 — 남양주 · 서울 · 경기 행사 음향 · 조명 준비 정보 | ${BRAND}` : `행사 준비 블로그 ${n}쪽 | ${BRAND}`,
      설명: `${지역들}에서 행사를 준비하는 담당자를 위한 글. 교회 수련회 · 세미나 · 야외 공연 · 학교 축제 · 제막식의 음향 · 조명, 무선마이크와 교회 음향 설치 상담 준비까지 현장 기준으로 정리합니다.`,
      경로, 이미지: 대표이미지, 더넣기: 제이슨(ld) })
      + 페이지머리({ 배경: posts[0] ? posts[0].cover.path : '/assets/img/works/w41.webp', 눈썹: 'Blog · Event Guide', 제목: '행사 준비 블로그', 소개: esc(소개), 길: [['블로그', '']] })
      + 꼬리(`
<section class="sec">
  <div class="wrap">
  ${칩('')}
  ${posts.length ? `<div class="stcards">${조각.map(카드).join('\n')}</div>` : '<div class="bempty">첫 글을 준비하고 있습니다.</div>'}
  ${쪽나눔}
  <p class="snote">현장 기록은 <a href="stories/index.html">행사 이야기</a>, 대표가 직접 쓰는 현장 소식은 <a href="https://blog.naver.com/martin301" target="_blank" rel="noopener">네이버 블로그(martin301)</a>에 있습니다.</p>
  </div>
</section>
${상담}`);
    쓰기(n === 1 ? 'blog' : `blog/page/${n}`, html);
  }

  /* ── 지역 모음 (/blog/<지역>/) ── */
  const 허브 = [];
  for (const r of 지역.values()) {
    const 목록 = posts.filter((p) => p.region === r.slug);
    if (r.slug === 'common' && !목록.length) continue;
    const 경로 = `/blog/${r.slug}/`;
    const 허브제목 = r.slug === 'common' ? '행사 준비 공통 정보' : `${r.이름} 행사 준비 정보`;
    const 소개 = r.slug === 'common'
      ? '지역과 상관없이 행사 준비에 두루 쓰이는 글입니다.'
      : `${esc(r.이름)}에서 행사를 준비하는 담당자를 위한 글입니다. ${esc(r.이동)}.`;
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: 허브제목, item: SITE + 경로 } ] },
      { '@type': 'CollectionPage', '@id': SITE + 경로, name: 허브제목, inLanguage: 'ko',
        hasPart: 목록.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug) })) } ] };
    const html = 머리({
      제목: `${허브제목} — 예배 · 세미나 · 공연 · 학교 축제 음향 · 조명 | ${BRAND}`,
      설명: r.slug === 'common' ? '지역과 상관없이 행사 준비에 두루 필요한 음향 · 조명 내용을 현장 기준으로 정리한 글 모음입니다.' : `${r.이름}에서 행사를 준비할 때 확인할 것들. 예배 · 수련회 · 세미나 · 공연 · 학교 축제 · 공식 행사의 음향 · 조명과 장비 설치 상담 준비까지 현장 기준으로 정리한 글 모음입니다.`,
      경로, 이미지: 목록[0] ? 사진주소(목록[0].cover.path) : 대표이미지, 색인: 목록.length > 0, 더넣기: 제이슨(ld) })
      + 페이지머리({ 배경: 목록[0] ? 목록[0].cover.path : (posts[0] ? posts[0].cover.path : '/assets/img/works/w41.webp'),
        눈썹: r.slug === 'common' ? 'Blog · Guide' : `Blog · ${esc(지역이름(r))}`, 제목: 허브제목, 소개, 길: [['블로그', 'blog/'], [r.이름, '']] })
      + 꼬리(`
<section class="sec">
  <div class="wrap">
  ${칩(r.slug)}
  ${목록.length ? `<div class="stcards">${목록.map(카드).join('\n')}</div>`
    : `<div class="bempty">${esc(r.이름)} 글은 곧 올라옵니다. 그동안 다른 지역 글을 참고해 보세요.</div>${posts.length ? `<div class="stcards">${posts.slice(0, 6).map(카드).join('\n')}</div>` : ''}`}
  ${r.서비스페이지 ? `<p class="snote">${esc(r.이름)}에서 한 일과 이동 시간은 <a href="${사이트경로(r.서비스페이지)}">${esc(r.이름)} 음향 · 설치 안내</a>에 있습니다.</p>` : ''}
  </div>
</section>
${상담}`);
    쓰기(`blog/${r.slug}`, html);
    if (목록.length) 허브.push({ loc: 경로, lastmod: 목록[0].updated || 목록[0].date });
  }

  /* ── sitemap.xml — 기존 항목은 두고 /blog/ 부분만 바꾼다 ── */
  const 블로그주소 = posts.length ? [
    { loc: '/blog/', lastmod: posts[0].updated || posts[0].date },
    ...허브,
    ...posts.map((p) => ({ loc: 글주소(p.slug), lastmod: p.updated || p.date })),
  ] : [];
  const sm = resolve(ROOT, 'sitemap.xml');
  if (existsSync(sm)) {
    let xml = readFileSync(sm, 'utf8').replace(/\r\n/g, '\n');
    xml = xml.replace(/\s*<url><loc>[^<]*\/blog\/[^<]*<\/loc>[^]*?<\/url>/g, '');
    const 추가 = 블로그주소.map((u) => `  <url><loc>${SITE}${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>\n`).join('');
    xml = xml.replace(/\s*<\/urlset>\s*$/, '\n' + 추가 + '</urlset>\n');
    writeFileSync(sm, xml, 'utf8');
  }

  /* ── llms.txt — 「## 블로그」 절을 다시 쓴다 ── */
  const ll = resolve(ROOT, 'llms.txt');
  if (existsSync(ll) && posts.length) {
    let t = readFileSync(ll, 'utf8').replace(/\r\n/g, '\n');
    const 절 = `## 블로그 (행사 준비 정보, 지역별)\n- [행사 준비 블로그](${SITE}/blog/): 남양주 · 서울 · 경기 지역별 행사 음향 · 조명 준비 체크리스트\n` +
      posts.map((p) => `- [${p.title}](${SITE}${글주소(p.slug)}): ${p.description}`).join('\n') + '\n';
    /* 「## 블로그」부터 다음 「## 」 절 앞(없으면 끝)까지 바꾼다 — 두 번 돌려도 목록이 겹치지 않는다(바로기획에서 고친 식) */
    const 시작 = t.search(/^## 블로그/m);
    if (시작 < 0) t = t.trimEnd() + '\n\n' + 절;
    else {
      const 뒤 = t.slice(시작 + 1);
      const 다음 = 뒤.search(/^## /m);
      t = t.slice(0, 시작) + 절 + (다음 >= 0 ? '\n' + 뒤.slice(다음) : '');
    }
    writeFileSync(ll, t, 'utf8');
  }

  /* ── rss.xml ── */
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>${esc(BRAND)} 행사 준비 블로그</title><link>${SITE}/blog/</link><description>남양주 · 서울 · 경기에서 행사 음향 · 조명을 준비하는 담당자를 위한 글</description><language>ko</language>
${posts.slice(0, 50).map((p) => `<item><title>${esc(p.title)}</title><link>${SITE}${글주소(p.slug)}</link><guid>${SITE}${글주소(p.slug)}</guid><description>${esc(p.description)}</description><pubDate>${new Date(p.date + 'T09:00:00+09:00').toUTCString()}</pubDate></item>`).join('\n')}
</channel></rss>
`;
  writeFileSync(resolve(ROOT, 'rss.xml'), rss, 'utf8');

  return { posts, 블로그주소 };
}

/* 혼자 실행할 때 */
const 이파일 = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(process.argv[1]) === 이파일) {
  const ROOT = resolve(dirname(이파일), '..');
  const { posts, 블로그주소 } = buildBlog({ ROOT });
  console.log(`blog/: 글 ${posts.length}개 · sitemap 항목 ${블로그주소.length}개 · rss.xml · llms.txt 갱신`);
}
