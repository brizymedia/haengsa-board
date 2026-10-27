/**
 * 한국체대 예그리나 블로그 — _blog/posts/*.json 을 홈페이지 글로 만든다
 * ──────────────────────────────────────────────────────────────
 *   blog/               글 목록 (최신순, 24개씩 → blog/page/2/)
 *   blog/<지역>/        지역별 모음 (예: blog/namyangju/)
 *   blog/<글주소>/      글 하나
 *   rss.xml             블로그 RSS
 *   sitemap.xml · llms.txt 의 블로그 부분도 같이 갱신한다
 *
 * 원본은 _blog/ 에 둔다. blog/ 는 매번 지우고 새로 만든다 — 결과 HTML 을 손으로 고치지 말고 원본 JSON 이나 이 템플릿을 고친다.
 * (HD기획 scripts/build-blog.mjs 를 예그리나에 맞게 옮긴 것.)
 *
 * 이 사이트는 brizymedia.github.io/yegrina/ 처럼 하위 폴더에 올라가 있다. 그래서 글 JSON 안의 주소는 사이트 루트 기준
 * (/quote.html, /assets/img/…)으로 쓰고, 여기서 페이지 깊이에 맞는 상대 주소(../../quote.html)로 바꾼다.
 * 머리글 · 폰 메뉴 · 바닥글은 notice.html 에서 빌려 온다(tools/make_pages.py 와 같은 방식) — 메뉴를 고치려면 notice.html 을 고친다.
 *
 * 실행:  node scripts/build-blog.mjs      글 형식 · 규칙: _blog/GUIDE.md   ·   검사: node scripts/blog-check.mjs
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SITE = 'https://brizymedia.github.io/yegrina';
export const BRAND = '한국체대 예그리나';
const TEL = '02-482-1934';
const 쪽당 = 24;

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 사이트 루트 기준 주소(/x) → 이 페이지에서 쓸 상대 주소 */
const 상대 = (pre, u) => (String(u).startsWith('/') ? pre + String(u).slice(1) : u);

/** 글 안에서는 **굵게** 와 [글자](주소) 만 쓴다. 주소는 / 로 시작하거나 https:// 여야 한다. */
export function 인라인(글, pre = '') {
  return esc(글)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(((?:\/|https:\/\/)[^)\s]*)\)/g, (m, t, u) =>
      u.startsWith('/') ? `<a href="${상대(pre, u)}">${t}</a>` : `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
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

/** photos.json 의 묶음을 사진 한 장씩 풀어 경로 → 정보 로. '묶음' 이름이 같으면 같은 장면 묶음이다. */
export function 사진목록(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'photos.json'), 'utf8'));
  const 표 = new Map();
  j.묶음.forEach((g, i) => { (g.path || []).forEach((p) => 표.set(p, { ...g, path: p, 묶음번호: g.묶음 ?? i })); });
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

/* 사이트 공통 style.css 위에 블로그 부분만 더한다(색은 style.css 의 변수) */
const CSS = `
.ph-head.bl-ph{min-height:300px}.ph-head.bl-ph h1{font-family:'Noto Sans KR',system-ui,sans-serif;font-weight:900;font-size:clamp(26px,4vw,42px);letter-spacing:-.03em;line-height:1.3;max-width:900px}
.bl-art{max-width:780px;margin:0 auto;padding:44px 0 20px}
.bl-meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 22px}
.bl-meta a,.bl-meta span{font-size:13px;font-weight:700;padding:6px 13px;border-radius:999px;background:#fff;box-shadow:inset 0 0 0 1px var(--line);color:var(--mute)}
.bl-meta a{background:var(--mint);box-shadow:none;color:var(--g7)}.bl-meta a:hover{background:var(--g2)}
.bl-lead{font-size:18px;line-height:1.9;color:var(--ink);margin:0 0 26px}.bl-lead a{color:var(--g7);font-weight:700}
.bl-art figure{margin:0 0 28px}.bl-art figure img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:18px;background:var(--mint)}
.bl-art figure.cover img{aspect-ratio:16/10}
.bl-art figcaption{font-size:13.5px;color:var(--mute);margin-top:8px;line-height:1.6}
.bl-points{background:var(--mint);border-radius:18px;padding:20px 24px;margin:0 0 28px}
.bl-points b{display:block;font-size:12px;font-weight:800;letter-spacing:.14em;color:var(--g5);margin-bottom:8px}
.bl-points ul{margin:0;padding-left:18px}.bl-points li{line-height:1.75;margin:4px 0;color:var(--ink)}
.bl-toc{border-left:4px solid var(--sun);padding:2px 0 2px 16px;margin:0 0 36px}
.bl-toc b{font-size:13px;color:var(--mute)}.bl-toc ul{margin:6px 0 0;padding:0;list-style:none}.bl-toc li{line-height:1.9}.bl-toc a:hover{color:var(--g5)}
.bl-body h2,.bl-faq h2{font-size:23px;line-height:1.4;letter-spacing:-.025em;margin:44px 0 14px;font-weight:900;color:var(--g9);scroll-margin-top:96px}
.bl-body p,.bl-faq p{font-size:16.5px;line-height:1.95;margin:0 0 18px}
.bl-body ul,.bl-body ol{margin:0 0 20px;padding-left:20px}.bl-body li{line-height:1.85;margin:5px 0}
.bl-body b{color:var(--g9)}.bl-body a,.bl-faq a,.bl-src a{color:var(--g7);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.bl-tbl{overflow-x:auto;margin:0 0 22px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1px var(--line)}
.bl-tbl table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:520px}
.bl-tbl th,.bl-tbl td{padding:11px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);line-height:1.6}
.bl-tbl th{background:var(--mint);font-weight:800;white-space:nowrap;color:var(--g9)}.bl-tbl tbody tr:last-child td{border-bottom:0}
.bl-tip{background:#FFF6D6;border-radius:14px;padding:15px 19px;margin:0 0 22px;font-size:15.5px;line-height:1.8}
.bl-tip::before{content:'현장 메모';display:block;font-size:11px;font-weight:800;letter-spacing:.14em;color:#B7791F;margin-bottom:3px}
.bl-faq details{background:#fff;border-radius:14px;margin:0 0 8px;padding:0 18px;box-shadow:inset 0 0 0 1px var(--line)}
.bl-faq summary{cursor:pointer;font-weight:700;padding:14px 0;line-height:1.6;color:var(--g9)}.bl-faq details p{margin:0 0 14px}
.bl-src{margin-top:32px;font-size:13.5px;color:var(--mute);line-height:1.7}.bl-src ul{padding-left:18px;margin:6px 0 0}.bl-src a{color:var(--mute);font-weight:500}
.bl-list{padding:44px 0 30px}
.bl-intro{max-width:760px;font-size:17px;color:var(--mute);margin:0 0 22px}.bl-intro a{color:var(--g7);font-weight:700;text-decoration:underline}
.bl-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.bl-card{display:block;background:#fff;border-radius:20px;overflow:hidden;box-shadow:inset 0 0 0 1px var(--line);transition:transform .3s,box-shadow .3s}
.bl-card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
.bl-card img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;background:var(--mint)}
.bl-card .in{padding:15px 17px 18px}.bl-card .r{font-size:12px;font-weight:800;color:var(--g5);margin-bottom:6px}
.bl-card .t{font-size:16.5px;font-weight:800;line-height:1.45;letter-spacing:-.02em;color:var(--g9)}
.bl-card .s{font-size:13.5px;color:var(--mute);line-height:1.6;margin-top:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.bl-chips{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 28px}
.bl-chips a{font-size:14px;font-weight:700;padding:8px 15px;border-radius:999px;background:#fff;box-shadow:inset 0 0 0 1px var(--line)}
.bl-chips a[aria-current]{background:var(--g9);color:#fff;box-shadow:none}.bl-chips small{font-weight:600;margin-left:4px;opacity:.6}
.bl-pager{display:flex;gap:7px;justify-content:center;margin-top:32px}
.bl-pager a,.bl-pager span{padding:8px 14px;border-radius:10px;font-weight:700;font-size:14px;background:#fff;box-shadow:inset 0 0 0 1px var(--line)}.bl-pager span{background:var(--g9);color:#fff}
.bl-empty{background:#fff;border-radius:16px;padding:22px;color:var(--mute);line-height:1.8;margin-bottom:24px;box-shadow:inset 0 0 0 1px var(--line)}
.bl-more{padding:10px 0 40px}.bl-more h2{font-size:21px;margin:0 0 16px;font-weight:900}
@media (max-width:640px){.bl-art{padding-top:30px}.bl-lead{font-size:17px}.bl-body h2,.bl-faq h2{font-size:21px}}
@media (prefers-reduced-motion:reduce){.bl-card{transition:none}.bl-card:hover{transform:none}}
`.trim();

const SVG_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>';
const SVG_QUOTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h5"/></svg>';
const SVG_MSG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg>';

export function buildBlog(옵션 = {}) {
  const ROOT = 옵션.ROOT;
  const 사진주소 = (path) => SITE + String(path).split('/').map(encodeURIComponent).join('/');   // 절대 주소(og · JSON-LD 용)
  const 작은사진 = (path) => { const s = String(path).replace('/works/', '/works/s/'); return existsSync(resolve(ROOT, '.' + s)) ? s : path; };
  const 지역 = 지역표(ROOT);
  const posts = 글읽기(ROOT);
  const 제이슨 = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;

  /* notice.html 의 머리 · 꼬리를 빌린다 */
  const 원본 = readFileSync(resolve(ROOT, 'notice.html'), 'utf8').replace(/\r\n/g, '\n');
  const 틀위 = 원본.slice(0, 원본.indexOf('<main>'));
  const 틀아래 = 원본.slice(원본.indexOf('</main>') + '</main>'.length);

  rmSync(resolve(ROOT, 'blog'), { recursive: true, force: true });
  const 쓰기 = (폴더, html) => {
    const d = resolve(ROOT, 폴더);
    mkdirSync(d, { recursive: true });
    writeFileSync(resolve(d, 'index.html'), html, 'utf8');
  };

  const 페이지 = ({ 제목, 설명, 경로, 이미지, 종류 = 'website', 더넣기 = '', 색인 = true, main }) => {
    const pre = '../'.repeat(경로.split('/').filter(Boolean).length);
    const 바꿈 = (s, 식, 값) => s.replace(식, (m, a) => a + 값);
    let top = 틀위;
    top = top.replace(/<title>[^]*?<\/title>/, () => `<title>${esc(제목)}</title>`);
    top = 바꿈(top, /(<meta name="description" content=")[^"]*/, esc(설명));
    top = 바꿈(top, /(<meta property="og:description" content=")[^"]*/, esc(설명));
    top = 바꿈(top, /(<meta property="og:title" content=")[^"]*/, esc(제목));
    top = 바꿈(top, /(<meta name="robots" content=")[^"]*/, 색인 ? 'index,follow,max-image-preview:large' : 'noindex,follow');
    top = 바꿈(top, /(<link rel="canonical" href=")[^"]*/, SITE + 경로);
    top = 바꿈(top, /(<meta property="og:url" content=")[^"]*/, SITE + 경로);
    top = 바꿈(top, /(<meta property="og:image" content=")[^"]*/, esc(이미지));
    top = 바꿈(top, /(<meta property="og:type" content=")[^"]*/, 종류);
    top = top.replace(/<meta property="og:image:(width|height)"[^>]*>\n?/g, '');
    top = top.replace(/<script type="application\/ld\+json">\{"@context": "https:\/\/schema.org", "@type": "BreadcrumbList"[^]*?<\/script>\n?/, '');
    top = top.replace(/<meta name="yg-edit"[^>]*>\n?/, '');
    top = top.replace(/ class="act"/g, '').replace(/class="act" /g, '');
    top = top.replace(/<a href="blog\/">블로그<\/a>/, '<a href="blog/" class="act" aria-current="page">블로그</a>');
    top = top.replace('</head>', `<link rel="alternate" type="application/rss+xml" title="${BRAND} 행사 준비 블로그" href="rss.xml">\n${더넣기}\n<style>${CSS}</style>\n</head>`);
    const bottom = 틀아래.replace(/<script src="assets\/edit\.js[^"]*"><\/script>\n?/, '');
    let out = top + '<main>\n' + main + '\n</main>' + bottom;
    out = out.replace(/(href|src)="(?!https?:|mailto:|tel:|sms:|#|\/|\.\.\/|data:)([^"]+)"/g, (m, a, b) => `${a}="${pre}${b}"`);
    out = out.replace(/url\((?!https?:)(assets\/[^)]+)\)/g, (m, a) => `url(${pre}${a})`);
    return { html: out, pre };
  };

  const 머리판 = (배경, 부스러기, h1, p, pre, 추가클래스 = '') => `<section class="ph-head${추가클래스}"><div class="bg" style="background-image:url(${esc(상대(pre, 배경))})"></div><div class="wrap">
  <div class="crumb"><a href="${pre}index.html">HOME</a>${부스러기.map(([t, h]) => `<span>›</span>${h ? `<a href="${상대(pre, h)}">${esc(t)}</a>` : `<span>${esc(t)}</span>`}`).join('')}</div>
  <h1>${esc(h1)}</h1>${p ? `<p>${esc(p)}</p>` : ''}</div></section>`;

  const 상담 = (pre) => `<section class="sec" style="padding-top:20px"><div class="wrap"><div class="cta rv"><div class="confetti" aria-hidden="true"></div>
  <div style="position:relative;z-index:1"><h2>행사 날짜가 정해졌다면<br>예그리나가 준비합니다.</h2><p>날짜 · 장소(실내/야외) · 인원만 알려 주셔도 프로그램과 참고 비용을 안내해 드립니다.</p></div>
  <div class="ways"><a href="tel:${TEL}"><span class="ic">${SVG_TEL}</span><span><small>대표전화 · 평일 11~19시</small>${TEL}</span></a><a href="${pre}quote.html"><span class="ic">${SVG_QUOTE}</span><span><small>항목만 골라 문의</small>자동 견적서</span></a><a href="${pre}contact.html"><span class="ic">${SVG_MSG}</span><span><small>홈페이지 문의 폼</small>예약 · 문의 남기기</span></a></div>
  </div></div></section>`;

  const 카드 = (p, pre) => {
    const r = 지역.get(p.region);
    return `<a class="bl-card" href="${상대(pre, 글주소(p.slug))}">
      <img src="${esc(상대(pre, 작은사진(p.cover.path)))}" alt="${esc(p.cover.alt)}" loading="lazy" decoding="async" width="800" height="500">
      <div class="in"><div class="r">${esc(r ? r.이름 : '')} · ${esc(날짜글(p.date))}</div><div class="t">${esc(p.title)}</div><div class="s">${esc(p.description)}</div></div>
    </a>`;
  };

  const 개수 = new Map();
  posts.forEach((p) => 개수.set(p.region, (개수.get(p.region) || 0) + 1));
  const 칩 = (현재, pre) => `<nav class="bl-chips" aria-label="지역별 글">
    <a href="${pre}blog/"${현재 === '' ? ' aria-current="page"' : ''}>전체<small>${posts.length}</small></a>
    ${[...지역.values()].filter((r) => 개수.get(r.slug)).map((r) =>
      `<a href="${pre}blog/${r.slug}/"${현재 === r.slug ? ' aria-current="page"' : ''}>${esc(r.이름)}<small>${개수.get(r.slug)}</small></a>`).join('\n    ')}
  </nav>`;

  /* ── 글 페이지 ── */
  const 이미지html = (im, 표지, pre) => `<figure${표지 ? ' class="cover"' : ''}>
    <img src="${esc(상대(pre, im.path))}" alt="${esc(im.alt)}" ${표지 ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" width="1600" height="1000">
    <figcaption>${인라인(im.caption, pre)}</figcaption>
  </figure>`;
  const 블록 = (b, pre) => {
    if (b.p) return `<p>${인라인(b.p, pre)}</p>`;
    if (b.tip) return `<div class="bl-tip">${인라인(b.tip, pre)}</div>`;
    if (b.ul) return `<ul>${b.ul.map((x) => `<li>${인라인(x, pre)}</li>`).join('')}</ul>`;
    if (b.ol) return `<ol>${b.ol.map((x) => `<li>${인라인(x, pre)}</li>`).join('')}</ol>`;
    if (b.table) return `<div class="bl-tbl"><table><thead><tr>${b.table.head.map((h) => `<th scope="col">${인라인(h, pre)}</th>`).join('')}</tr></thead><tbody>${
      b.table.rows.map((row) => `<tr>${row.map((c) => `<td>${인라인(c, pre)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    if (b.img) return 이미지html(b.img, false, pre);
    return '';
  };

  for (const p of posts) {
    const r = 지역.get(p.region) || { 이름: '', 서비스페이지: '' };
    const 지역글 = p.region !== 'common';
    const 경로 = 글주소(p.slug);
    const pre = '../../';
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
        publisher: { '@id': SITE + '/#business' },
        mainEntityOfPage: { '@type': 'WebPage', '@id': SITE + 경로 },
        ...(지역글 ? { spatialCoverage: { '@type': 'Place', name: `${r.도} ${r.시군}` } } : {}) },
      ...((p.faq || []).length ? [{ '@type': 'FAQPage', '@id': SITE + 경로 + '#faq',
        mainEntity: p.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: 글자만(f.a) } })) }] : []),
    ] };

    const main = 머리판(p.cover.path, [['블로그', '/blog/'], ...(지역글 ? [[r.이름, `/blog/${p.region}/`]] : [])], p.title, '', pre, ' bl-ph') + `
<section><div class="wrap"><article class="bl-art">
  <div class="bl-meta">
    <span>${esc(날짜글(p.date))}</span>
    ${지역글 ? `<a href="${pre}blog/${p.region}/">${esc(r.이름)} 글 모음</a>` : ''}
    ${r.서비스페이지 ? `<a href="${상대(pre, r.서비스페이지)}">${esc(r.이름)} 행사 안내</a>` : ''}
    <span>읽는 시간 약 ${분}분</span>
  </div>
  <p class="bl-lead">${인라인(p.lead, pre)}</p>
  ${이미지html(p.cover, true, pre)}
  <div class="bl-points"><b>이 글의 요점</b><ul>${p.points.map((x) => `<li>${인라인(x, pre)}</li>`).join('')}</ul></div>
  <nav class="bl-toc" aria-label="목차"><b>목차</b><ul>${p.sections.map((s, i) => `<li><a href="#s${i + 1}">${esc(s.h2)}</a></li>`).join('')}</ul></nav>
  <div class="bl-body">
${p.sections.map((s, i) => `<h2 id="s${i + 1}">${esc(s.h2)}</h2>\n${s.blocks.map((b) => 블록(b, pre)).join('\n')}`).join('\n')}
  </div>
  ${(p.faq || []).length ? `<section class="bl-faq" id="faq"><h2>자주 묻는 질문</h2>${p.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${인라인(f.a, pre)}</p></details>`).join('')}</section>` : ''}
  ${(p.sources || []).length ? `<div class="bl-src"><b>확인한 자료</b> (${esc(날짜글(p.updated || p.date))} 기준)<ul>${p.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>`).join('')}</ul></div>` : ''}
</article></div></section>
${관련.length ? `<section class="bl-more"><div class="wrap"><h2>같이 보면 좋은 글</h2><div class="bl-cards">${관련.map((o) => 카드(o, pre)).join('\n')}</div></div></section>` : ''}
${상담(pre)}`;
    const { html } = 페이지({ 제목: `${p.title} | ${BRAND}`, 설명: p.description, 경로, 이미지: 사진주소(p.cover.path), 종류: 'article',
      더넣기: `<meta property="article:published_time" content="${p.date}">\n${제이슨(ld)}`, main });
    쓰기(`blog/${p.slug}`, html);
  }

  /* ── 목록 (blog/, blog/page/N/) ── */
  const 대표이미지 = posts[0] ? 사진주소(posts[0].cover.path) : `${SITE}/assets/img/og.jpg`;
  const 쪽수 = Math.max(1, Math.ceil(posts.length / 쪽당));
  for (let n = 1; n <= 쪽수; n++) {
    const 조각 = posts.slice((n - 1) * 쪽당, n * 쪽당);
    const 경로 = n === 1 ? '/blog/' : `/blog/page/${n}/`;
    const pre = n === 1 ? '../' : '../../../';
    const 쪽나눔 = 쪽수 > 1 ? `<nav class="bl-pager" aria-label="쪽 이동">${Array.from({ length: 쪽수 }, (_, i) => i + 1).map((k) =>
      k === n ? `<span aria-current="page">${k}</span>` : `<a href="${pre}${k === 1 ? 'blog/' : `blog/page/${k}/`}">${k}</a>`).join('')}</nav>` : '';
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' } ] },
      { '@type': 'Blog', '@id': SITE + '/blog/', name: `${BRAND} 행사 준비 블로그`, inLanguage: 'ko', publisher: { '@id': SITE + '/#business' },
        blogPost: 조각.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug), datePublished: p.date, image: 사진주소(p.cover.path) })) } ] };
    const main = 머리판('/assets/img/works/w05.webp', [['블로그', n > 1 ? '/blog/' : ''], ...(n > 1 ? [[`${n}쪽`, '']] : [])], '행사 준비 블로그',
      '운동회 · 전교인 체육대회 · 발표회 · 물놀이 · 놀이기구 렌탈을 준비하는 원장님 · 선생님 · 담당자를 위한 지역별 체크리스트입니다.', pre) + `
<section class="bl-list"><div class="wrap">
  <p class="bl-intro">남양주 별내 사무실에서 가까운 지역부터, 행사를 맡은 분이 먼저 확인할 것들을 정리합니다. 날짜와 장소, 날씨와 안전, 프로그램과 견적까지 현장 기준으로 씁니다.</p>
  ${칩('', pre)}
  ${posts.length ? `<div class="bl-cards">${조각.map((p) => 카드(p, pre)).join('\n')}</div>` : '<div class="bl-empty">첫 글을 준비하고 있습니다.</div>'}
  ${쪽나눔}
</div></section>
${상담(pre)}`;
    const { html } = 페이지({
      제목: n === 1 ? `행사 준비 블로그 — 남양주 · 의정부 · 노원 · 구리 운동회 · 체육대회 · 발표회 준비 | ${BRAND}` : `행사 준비 블로그 ${n}쪽 | ${BRAND}`,
      설명: '남양주 · 의정부 · 노원 · 양주 · 구리 · 중랑 · 하남 · 포천 · 강동에서 어린이 행사를 준비하는 분을 위한 글. 운동회 · 전교인 체육대회 · 발표회 사회 · 물놀이 · 에어바운스 · 유아체육 수업까지 현장 기준으로 정리합니다.',
      경로, 이미지: 대표이미지, 더넣기: 제이슨(ld), main });
    쓰기(n === 1 ? 'blog' : `blog/page/${n}`, html);
  }

  /* ── 지역 모음 (blog/<지역>/) ── */
  const 허브 = [];
  for (const r of 지역.values()) {
    const 목록 = posts.filter((p) => p.region === r.slug);
    if (r.slug === 'common' && !목록.length) continue;
    const 경로 = `/blog/${r.slug}/`;
    const pre = '../../';
    const 허브제목 = r.slug === 'common' ? '행사 준비 공통 정보' : `${r.이름} 행사 준비 정보`;
    const 소개 = r.slug === 'common'
      ? '지역과 상관없이 행사 준비에 두루 쓰이는 글입니다.'
      : `${esc(r.이름)}(${esc(r.도)} ${esc(r.시군)})에서 어린이 행사를 준비하는 분을 위한 글입니다. ${esc(r.이동)}.${r.서비스페이지 ? ` 서비스 안내는 <a href="${상대(pre, r.서비스페이지)}">${esc(r.이름)} 행사 안내 페이지</a>에 있습니다.` : ''}`;
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: 허브제목, item: SITE + 경로 } ] },
      { '@type': 'CollectionPage', '@id': SITE + 경로, name: 허브제목, inLanguage: 'ko',
        hasPart: 목록.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug) })) } ] };
    const main = 머리판(목록[0] ? 목록[0].cover.path : '/assets/img/works/w05.webp', [['블로그', '/blog/'], [r.이름, '']], 허브제목, '', pre) + `
<section class="bl-list"><div class="wrap">
  <p class="bl-intro">${소개}</p>
  ${칩(r.slug, pre)}
  ${목록.length ? `<div class="bl-cards">${목록.map((p) => 카드(p, pre)).join('\n')}</div>`
    : `<div class="bl-empty">${esc(r.이름)} 글은 곧 올라옵니다. 그동안 다른 지역 글을 참고해 보세요.</div>${posts.length ? `<div class="bl-cards">${posts.slice(0, 6).map((p) => 카드(p, pre)).join('\n')}</div>` : ''}`}
</div></section>
${상담(pre)}`;
    const { html } = 페이지({
      제목: `${허브제목} — 운동회 · 체육대회 · 발표회 · 물놀이 · 놀이기구 | ${BRAND}`,
      설명: r.slug === 'common' ? '지역과 상관없이 어린이 행사 준비에 두루 필요한 내용을 현장 기준으로 정리한 글 모음입니다.' : `${r.이름}에서 어린이 행사를 준비할 때 확인할 것들. 운동회 · 전교인 체육대회 · 발표회 · 물놀이 · 놀이기구 렌탈 · 유아체육 수업을 현장 기준으로 정리한 글 모음입니다.`,
      경로, 이미지: 목록[0] ? 사진주소(목록[0].cover.path) : 대표이미지, 색인: 목록.length > 0, 더넣기: 제이슨(ld), main });
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
    let xml = readFileSync(sm, 'utf8');
    xml = xml.replace(/\s*<url><loc>[^<]*\/blog\/[^<]*<\/loc>[^]*?<\/url>/g, '');
    const 추가 = 블로그주소.map((u) => `  <url><loc>${SITE}${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>\n`).join('');
    xml = xml.replace(/\n?<\/urlset>\s*$/, '\n' + 추가 + '</urlset>\n');
    writeFileSync(sm, xml, 'utf8');
  }

  /* ── llms.txt — 「## 블로그」 절을 다시 쓴다 ── */
  const ll = resolve(ROOT, 'llms.txt');
  if (existsSync(ll) && posts.length) {
    let t = readFileSync(ll, 'utf8').replace(/\r\n/g, '\n');
    const 절 = `## 블로그 (행사 준비 정보, 지역별)\n- [행사 준비 블로그](${SITE}/blog/): 남양주 · 의정부 · 노원 · 양주 · 구리 · 중랑 · 하남 · 포천 · 강동 어린이 행사 준비 체크리스트\n` +
      posts.map((p) => `- [${p.title}](${SITE}${글주소(p.slug)}): ${p.description}`).join('\n') + '\n';
    t = /^## 블로그[^]*?(?=^## |\s*$)/m.test(t) ? t.replace(/^## 블로그[^]*?(?=^## |\s*$)/m, 절) : t.trimEnd() + '\n\n' + 절;
    writeFileSync(ll, t, 'utf8');
  }

  /* ── rss.xml ── */
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>${esc(BRAND)} 행사 준비 블로그</title><link>${SITE}/blog/</link><description>남양주 · 의정부 · 노원 등에서 어린이 행사를 준비하는 분을 위한 글</description><language>ko</language>
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
