/**
 * 바로기획 블로그 — _blog/posts/*.json 을 홈페이지 글로 만든다
 * ──────────────────────────────────────────────────────
 *   /blog/               글 목록 (최신순, 24개씩 → /blog/page/2/)
 *   /blog/<지역>/        지역별 모음 (예: /blog/ansan/)
 *   /blog/<글주소>/      글 하나
 *   /rss.xml             블로그 RSS
 *   sitemap.xml · llms.txt 의 블로그 부분도 같이 갱신한다
 *
 * 원본은 _blog/ 에 둔다. 밑줄로 시작하는 폴더는 GitHub Pages(Jekyll)가 공개하지 않는다.
 * blog/ 는 매번 지우고 새로 만든다 — 결과 HTML 을 손으로 고치지 말고 원본 JSON 이나 이 템플릿을 고친다.
 * (HD기획 scripts/build-blog.mjs 를 바로기획에 맞게 옮긴 것 — 사진은 이 저장소 /assets/img/p/ , 목록 카드는 /assets/img/t/)
 * 사이트 주소는 연결된 도메인 www.바로기획.com(퓨니코드) 기준. 사이트 루트에 바로 올라가 있어 / 로 시작하는 주소를 쓴다.
 *
 * 실행:  node scripts/build-blog.mjs      글 형식 · 규칙: _blog/GUIDE.md   ·   검사: node scripts/blog-check.mjs
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SITE = 'https://www.xn--ok0bx6qu3cus0b.com';
export const BRAND = '바로기획';
const TEL = '010-2758-0655';
const 쪽당 = 24;

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 글 안에서는 **굵게** 와 [글자](주소) 만 쓴다. 주소는 / 로 시작하거나 https:// 여야 한다. */
export function 인라인(글) {
  return esc(글)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(((?:\/|https:\/\/)[^)\s]*)\)/g, (m, t, u) =>
      u.startsWith('/') ? `<a href="${u}">${t}</a>` : `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
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

const CSS = `
:root{--acc:#C9A24B;--acc-ink:#8F6E22;--acc2:#E3C57E;--ink:#131A2A;--navy:#0E1F3F;--txt:#394254;--muted:#6B7385;--dim:#7D8496;--line:#E3E6ED;--bg:#fff;--bg2:#F4F6FA;--en:"Montserrat","Pretendard Variable",Pretendard,sans-serif}
*{box-sizing:border-box;font-family:"Pretendard Variable",Pretendard,"Noto Sans KR",system-ui,sans-serif;word-break:keep-all}
html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--txt);-webkit-font-smoothing:antialiased}
a{color:inherit}img{display:block;max-width:100%}
.topbar{position:sticky;top:0;z-index:40;background:var(--navy);color:#fff;box-shadow:0 8px 24px -16px rgba(0,0,0,.6)}
.topbar-in{max-width:1180px;margin:0 auto;padding:0 20px;height:56px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{text-decoration:none;display:flex;align-items:center;gap:10px;font-weight:800;font-size:16px;white-space:nowrap}
.brand img{height:34px;width:auto}
.topnav{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.topnav a{color:rgba(255,255,255,.78);text-decoration:none;font-size:14px;font-weight:700;padding:8px 12px;white-space:nowrap;border-radius:6px}
.topnav a:hover,.topnav a[aria-current]{color:#fff;background:rgba(255,255,255,.08)}
.topnav a.tel{background:var(--acc);color:var(--navy);font-family:var(--en)}
@media (max-width:640px){.topnav a{font-size:13px;padding:7px 9px}.topnav .hide-sm{display:none}.brand img{height:28px}}
@media (max-width:400px){.topnav a.tel{display:none}}
.crumb{max-width:760px;margin:0 auto;padding:18px 20px 0;font-size:12.5px;color:var(--dim)}.crumb.wide{max-width:1180px}
.crumb a{text-decoration:none}.crumb a:hover{color:var(--acc-ink)}
.art{max-width:760px;margin:0 auto;padding:16px 20px 48px}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-family:var(--en);font-size:11px;font-weight:700;letter-spacing:.28em;color:var(--acc-ink);margin:0 0 12px;text-transform:uppercase}
.eyebrow::before{content:"";width:9px;height:9px;border-radius:50%;border:2px solid var(--acc)}
h1{font-size:clamp(26px,4.2vw,40px);line-height:1.25;letter-spacing:-.035em;margin:0 0 16px;font-weight:800;color:var(--ink);text-wrap:balance}
.meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 24px}
.meta a,.meta span{font-size:12.5px;font-weight:700;text-decoration:none;padding:5px 12px;border-radius:9999px;background:var(--bg2);color:var(--muted)}
.meta a{background:rgba(201,162,75,.14);color:var(--acc-ink)}.meta a:hover{background:rgba(201,162,75,.26)}
.lead{font-size:17px;line-height:1.85;color:var(--ink);margin:0 0 24px}.lead a{color:var(--acc-ink);font-weight:700}
figure{margin:0 0 28px}figure img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:14px;background:var(--bg2)}
figure.cover img{aspect-ratio:16/9}
figcaption{font-size:13px;color:var(--dim);margin-top:8px;line-height:1.6}
.points{background:var(--bg2);border-radius:14px;padding:18px 22px;margin:0 0 28px}
.points b{display:block;font-family:var(--en);font-size:11px;letter-spacing:.24em;color:var(--acc-ink);margin-bottom:8px}
.points ul{margin:0;padding-left:18px}.points li{line-height:1.75;margin:4px 0;color:var(--ink)}
.toc{border-left:3px solid var(--acc);padding:2px 0 2px 16px;margin:0 0 36px}
.toc b{font-size:12.5px;color:var(--dim)}.toc ol{margin:6px 0 0;padding-left:18px}.toc li{line-height:1.9}.toc a{text-decoration:none}.toc a:hover{color:var(--acc-ink)}
.body h2,.faq h2{font-size:22px;line-height:1.4;letter-spacing:-.025em;margin:40px 0 14px;font-weight:800;color:var(--ink);scroll-margin-top:72px;text-wrap:balance}
.body p,.faq p{font-size:16px;line-height:1.95;color:var(--txt);margin:0 0 18px}
.body ul,.body ol{margin:0 0 20px;padding-left:20px;color:var(--txt)}.body li{line-height:1.85;margin:5px 0}
.body b{color:var(--ink)}.body a,.faq a{color:var(--acc-ink);font-weight:700;text-underline-offset:3px}
.tbl{overflow-x:auto;margin:0 0 22px;border:1px solid var(--line);border-radius:12px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:520px}
th,td{padding:10px 13px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);line-height:1.6}
th{background:var(--bg2);font-weight:800;white-space:nowrap;color:var(--ink)}tbody tr:last-child td{border-bottom:0}
.tip{background:rgba(201,162,75,.12);border-radius:12px;padding:14px 18px;margin:0 0 22px;font-size:15.5px;line-height:1.8;color:var(--ink)}
.tip::before{content:'현장 메모';display:block;font-family:var(--en);font-size:10px;font-weight:800;letter-spacing:.22em;color:var(--acc-ink);margin-bottom:3px}
.faq details{background:#fff;border:1px solid var(--line);border-radius:12px;margin:0 0 8px;padding:0 16px}
.faq summary{cursor:pointer;font-weight:700;padding:13px 0;line-height:1.6;color:var(--ink)}.faq details p{margin:0 0 14px}
.src{margin-top:32px;font-size:13.5px;color:var(--dim);line-height:1.7}.src ul{padding-left:18px;margin:6px 0 0}.src a{color:var(--muted)}
.cta{background:var(--navy);color:#fff;border-radius:16px;padding:26px;margin-top:40px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between}
.cta h3{margin:0 0 5px;font-size:19px;letter-spacing:-.02em}.cta p{margin:0;color:rgba(255,255,255,.7);font-size:14px;line-height:1.7}
.cta .num{font-family:var(--en);font-weight:800;font-size:22px;color:#fff;text-decoration:none;display:block;margin-bottom:8px}
.btn{display:inline-flex;align-items:center;padding:12px 20px;border-radius:8px;font-weight:700;font-size:14.5px;text-decoration:none;background:var(--acc);color:var(--navy);white-space:nowrap}
.btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.3)}
.more{max-width:1180px;margin:0 auto;padding:8px 20px 64px}.more h2{font-size:20px;margin:0 0 16px;letter-spacing:-.02em;color:var(--ink)}
.wrap{max-width:1180px;margin:0 auto;padding:18px 20px 64px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.card{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:transform .35s,box-shadow .35s}
.card:hover{transform:translateY(-4px);box-shadow:0 20px 50px -24px rgba(17,19,24,.3)}
.card img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;background:var(--bg2)}
.card .in{padding:14px 16px 17px}.card .r{font-family:var(--en);font-size:10px;font-weight:800;letter-spacing:.2em;color:var(--acc-ink);margin-bottom:6px}
.card .t{font-size:16px;font-weight:800;line-height:1.45;letter-spacing:-.02em;color:var(--ink)}
.card .s{font-size:13px;color:var(--muted);line-height:1.6;margin-top:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 28px}
.chips a{font-size:13.5px;font-weight:700;text-decoration:none;padding:8px 14px;border-radius:9999px;background:#fff;border:1px solid var(--line);color:var(--txt)}
.chips a[aria-current]{background:var(--ink);color:#fff;border-color:var(--ink)}.chips small{font-weight:600;margin-left:4px;opacity:.6}
.pager{display:flex;gap:7px;justify-content:center;margin-top:32px}
.pager a,.pager span{padding:8px 14px;border-radius:8px;border:1px solid var(--line);text-decoration:none;font-weight:700;font-size:14px;background:#fff}.pager span{background:var(--ink);color:#fff}
.empty{background:#fff;border:1px dashed var(--line);border-radius:14px;padding:22px;color:var(--muted);line-height:1.8;margin-bottom:24px}
.foot{background:#081427;color:rgba(255,255,255,.55);font-size:12.5px;padding:32px 20px;text-align:center;line-height:1.9}.foot a{color:rgba(255,255,255,.75);text-decoration:none}
a:focus-visible,summary:focus-visible{outline:2px solid var(--acc);outline-offset:3px;border-radius:4px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.card{transition:none}.card:hover{transform:none}}
`.trim();

export function buildBlog(옵션 = {}) {
  const ROOT = 옵션.ROOT;
  const 사진주소 = (path) => SITE + String(path).split('/').map(encodeURIComponent).join('/');   // 절대 주소(og · JSON-LD 용)
  const 지역 = 지역표(ROOT);
  const posts = 글읽기(ROOT);
  const 발행처 = { '@type': 'Organization', name: BRAND, url: SITE + '/', logo: SITE + '/assets/img/logo-mark.svg', telephone: '+82-10-2758-0655' };
  const 제이슨 = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;

  rmSync(resolve(ROOT, 'blog'), { recursive: true, force: true });
  const 쓰기 = (폴더, html) => {
    const d = resolve(ROOT, 폴더);
    mkdirSync(d, { recursive: true });
    writeFileSync(resolve(d, 'index.html'), html, 'utf8');
  };

  const 머리 = ({ 제목, 설명, 경로, 이미지, 종류 = 'website', 더넣기 = '', 색인 = true }) => `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0E1F3F">
<title>${esc(제목)}</title>
<meta name="description" content="${esc(설명)}">
<meta name="robots" content="${색인 ? 'index,follow,max-image-preview:large' : 'noindex,follow'}">
<link rel="canonical" href="${SITE}${경로}">
<link rel="alternate" type="application/rss+xml" title="${BRAND} 행사 준비 블로그" href="/rss.xml">
<meta property="og:type" content="${종류}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="${BRAND}">
<meta property="og:title" content="${esc(제목)}">
<meta property="og:description" content="${esc(설명)}">
<meta property="og:url" content="${SITE}${경로}">
<meta property="og:image" content="${esc(이미지)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
${더넣기}
<style>${CSS}</style>
<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="baro"></script>
</head>
<body>
<div class="topbar"><div class="topbar-in">
  <a class="brand" href="/" aria-label="${BRAND} 홈"><img src="/assets/img/logo-h-white.svg" alt="${BRAND} BARO PLANNING" width="113" height="34"></a>
  <nav class="topnav" aria-label="주 메뉴">
    <a href="/service.html" class="hide-sm">하는 일</a>
    <a href="/blog/" aria-current="page">블로그</a>
    <a href="/stories/index.html" class="hide-sm">행사 이야기</a>
    <a href="/areas/index.html" class="hide-sm">운영 지역</a>
    <a href="/quote.html">자동 견적</a>
    <a class="tel" href="tel:${TEL}">${TEL}</a>
  </nav>
</div></div>`;

  const 꼬리 = `<footer class="foot">
  <div>${BRAND} · 대표 김선호 · 경기도 안산시 상록구 장화1길 56, 103호 (사동) · <a href="tel:${TEL}">${TEL}</a> · mot2256@naver.com · 상담 오전 8시 ~ 저녁 8시</div>
  <div style="margin-top:8px;"><a href="/">홈</a> · <a href="/blog/">블로그</a> · <a href="/stories/index.html">행사 이야기</a> · <a href="/areas/index.html">운영 지역</a> · <a href="/portfolio.html">현장 사진</a> · <a href="/quote.html">자동 견적서</a> · <a href="/contact.html">견적 문의</a></div>
  <div style="margin-top:8px;">COPYRIGHT © ${new Date().getFullYear()} ${BRAND}. ALL RIGHTS RESERVED.</div>
</footer>
</body>
</html>
`;

  const 상담 = `<div class="cta">
    <div><h3>행사 날짜가 잡히셨나요?</h3><p>규모가 작아도 괜찮습니다. 날짜 · 장소 · 대략의 인원만 알려 주세요. (상담 오전 8시 ~ 저녁 8시)</p></div>
    <div><a class="num" href="tel:${TEL}">${TEL}</a><div style="display:flex;gap:8px;flex-wrap:wrap;"><a class="btn" href="/quote.html">자동 견적서</a><a class="btn ghost" href="/contact.html">견적 문의 폼</a></div></div>
  </div>`;

  const 카드 = (p) => {
    const r = 지역.get(p.region);
    return `<a class="card" href="${글주소(p.slug)}">
      <img src="${esc(String(p.cover.path).replace('/assets/img/p/', '/assets/img/t/'))}" alt="${esc(p.cover.alt)}" loading="lazy" decoding="async" width="800" height="500">
      <div class="in"><div class="r">${esc(r ? r.이름 : '')} · ${esc(날짜글(p.date))}</div><div class="t">${esc(p.title)}</div><div class="s">${esc(p.description)}</div></div>
    </a>`;
  };

  const 개수 = new Map();
  posts.forEach((p) => 개수.set(p.region, (개수.get(p.region) || 0) + 1));
  const 칩 = (현재) => `<nav class="chips" aria-label="지역별 글">
    <a href="/blog/"${현재 === '' ? ' aria-current="page"' : ''}>전체<small>${posts.length}</small></a>
    ${[...지역.values()].filter((r) => 개수.get(r.slug)).map((r) =>
      `<a href="/blog/${r.slug}/"${현재 === r.slug ? ' aria-current="page"' : ''}>${esc(r.이름)}<small>${개수.get(r.slug)}</small></a>`).join('\n    ')}
  </nav>`;

  /* ── 글 페이지 ── */
  const 이미지html = (im, 표지) => `<figure${표지 ? ' class="cover"' : ''}>
    <img src="${esc(im.path)}" alt="${esc(im.alt)}" ${표지 ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" width="${표지 ? 1600 : 1200}" height="900">
    <figcaption>${인라인(im.caption)}</figcaption>
  </figure>`;
  const 블록 = (b) => {
    if (b.p) return `<p>${인라인(b.p)}</p>`;
    if (b.tip) return `<div class="tip">${인라인(b.tip)}</div>`;
    if (b.ul) return `<ul>${b.ul.map((x) => `<li>${인라인(x)}</li>`).join('')}</ul>`;
    if (b.ol) return `<ol>${b.ol.map((x) => `<li>${인라인(x)}</li>`).join('')}</ol>`;
    if (b.table) return `<div class="tbl"><table><thead><tr>${b.table.head.map((h) => `<th scope="col">${인라인(h)}</th>`).join('')}</tr></thead><tbody>${
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
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic === p.topic)].slice(0, 3);

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
        ...(지역글 ? { spatialCoverage: { '@type': 'Place', name: `${r.도} ${r.시군}` } } : {}) },
      ...((p.faq || []).length ? [{ '@type': 'FAQPage', '@id': SITE + 경로 + '#faq',
        mainEntity: p.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: 글자만(f.a) } })) }] : []),
    ] };

    const html = 머리({ 제목: `${p.title} | ${BRAND}`, 설명: p.description, 경로, 이미지: 사진주소(p.cover.path), 종류: 'article',
      더넣기: `<meta property="article:published_time" content="${p.date}">\n${제이슨(ld)}` }) + `
<div class="crumb"><a href="/">홈</a> › <a href="/blog/">블로그</a>${지역글 ? ` › <a href="/blog/${p.region}/">${esc(r.이름)}</a>` : ''}</div>
<article class="art">
  <p class="eyebrow">${esc(지역글 ? r.이름 + ' 행사 준비' : '행사 준비')} · ${esc(날짜글(p.date))}</p>
  <h1>${esc(p.title)}</h1>
  <div class="meta">
    ${지역글 ? `<a href="/blog/${p.region}/">${esc(r.이름)} 글 모음</a>` : ''}
    ${r.서비스페이지 ? `<a href="${r.서비스페이지}">${esc(r.이름)} 행사 안내</a>` : ''}
    <span>읽는 시간 약 ${분}분</span>
  </div>
  <p class="lead">${인라인(p.lead)}</p>
  ${이미지html(p.cover, true)}
  <div class="points"><b>이 글의 요점</b><ul>${p.points.map((x) => `<li>${인라인(x)}</li>`).join('')}</ul></div>
  <nav class="toc" aria-label="목차"><b>목차</b><ol>${p.sections.map((s, i) => `<li><a href="#s${i + 1}">${esc(s.h2)}</a></li>`).join('')}</ol></nav>
  <div class="body">
${p.sections.map((s, i) => `<h2 id="s${i + 1}">${esc(s.h2)}</h2>\n${s.blocks.map(블록).join('\n')}`).join('\n')}
  </div>
  ${(p.faq || []).length ? `<section class="faq" id="faq"><h2>자주 묻는 질문</h2>${p.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${인라인(f.a)}</p></details>`).join('')}</section>` : ''}
  ${(p.sources || []).length ? `<div class="src"><b>확인한 자료</b> (${esc(날짜글(p.updated || p.date))} 기준)<ul>${p.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>`).join('')}</ul></div>` : ''}
  ${상담}
</article>
${관련.length ? `<section class="more"><h2>같이 보면 좋은 글</h2><div class="cards">${관련.map(카드).join('\n')}</div></section>` : ''}
` + 꼬리;
    쓰기(`blog/${p.slug}`, html);
  }

  /* ── 목록 (/blog/, /blog/page/N/) ── */
  const 대표이미지 = posts[0] ? 사진주소(posts[0].cover.path) : `${SITE}/assets/img/og.jpg`;
  const 쪽수 = Math.max(1, Math.ceil(posts.length / 쪽당));
  for (let n = 1; n <= 쪽수; n++) {
    const 조각 = posts.slice((n - 1) * 쪽당, n * 쪽당);
    const 경로 = n === 1 ? '/blog/' : `/blog/page/${n}/`;
    const 쪽나눔 = 쪽수 > 1 ? `<nav class="pager" aria-label="쪽 이동">${Array.from({ length: 쪽수 }, (_, i) => i + 1).map((k) =>
      k === n ? `<span aria-current="page">${k}</span>` : `<a href="${k === 1 ? '/blog/' : `/blog/page/${k}/`}">${k}</a>`).join('')}</nav>` : '';
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' } ] },
      { '@type': 'Blog', '@id': SITE + '/blog/', name: `${BRAND} 행사 준비 블로그`, inLanguage: 'ko', publisher: 발행처,
        blogPost: 조각.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug), datePublished: p.date, image: 사진주소(p.cover.path) })) } ] };
    const html = 머리({
      제목: n === 1 ? `행사 준비 블로그 — 안산 · 화성 · 수원 등 경기 지역별 행사 준비 정보 | ${BRAND}` : `행사 준비 블로그 ${n}쪽 | ${BRAND}`,
      설명: '안산 · 화성 · 수원 · 시흥 · 안양 · 광명 · 동탄 · 용인 · 평택에서 행사를 준비하는 담당자를 위한 글. 체육대회 · 지역축제 · 커팅식 · 송년회 · 물놀이 · 점등식, 음향 · 천막 · MC 섭외까지 현장 기준으로 정리합니다.',
      경로, 이미지: 대표이미지, 더넣기: 제이슨(ld) }) + `
<div class="crumb wide"><a href="/">홈</a> › 블로그${n > 1 ? ` › ${n}쪽` : ''}</div>
<main class="wrap">
  <p class="eyebrow">Blog · Event Guide</p>
  <h1>행사 준비 블로그</h1>
  <p class="lead" style="max-width:760px">행사를 맡은 담당자가 먼저 확인할 것들을 경기 지역별로 정리합니다. 종목과 순서, 장비와 섭외, 날씨와 안전, 견적까지 현장 기준으로 씁니다.</p>
  ${칩('')}
  ${posts.length ? `<div class="cards">${조각.map(카드).join('\n')}</div>` : '<div class="empty">첫 글을 준비하고 있습니다.</div>'}
  ${쪽나눔}
  ${상담}
</main>
` + 꼬리;
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
      : `${esc(r.이름)}에서 행사를 준비하는 담당자를 위한 글입니다. ${esc(r.이동)}.${r.서비스페이지 ? ` 서비스 안내는 <a href="${r.서비스페이지}">${esc(r.이름)} 행사 안내 페이지</a>에 있습니다.` : ''}`;
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: 허브제목, item: SITE + 경로 } ] },
      { '@type': 'CollectionPage', '@id': SITE + 경로, name: 허브제목, inLanguage: 'ko',
        hasPart: 목록.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug) })) } ] };
    const html = 머리({
      제목: `${허브제목} — 체육대회 · 지역축제 · 커팅식 · 송년회 · 음향 | ${BRAND}`,
      설명: r.slug === 'common' ? '지역과 상관없이 행사 준비에 두루 필요한 내용. 준비 순서 · 안전 · 견적 항목을 현장 기준으로 정리한 글 모음입니다.' : `${r.이름}에서 행사를 준비할 때 확인할 것들. 체육대회 · 지역축제 · 커팅식 · 송년회 같은 행사와 음향 · 천막 · MC 섭외, 날씨와 안전, 견적까지 현장 기준으로 정리한 글 모음입니다.`,
      경로, 이미지: 목록[0] ? 사진주소(목록[0].cover.path) : 대표이미지, 색인: 목록.length > 0, 더넣기: 제이슨(ld) }) + `
<div class="crumb wide"><a href="/">홈</a> › <a href="/blog/">블로그</a> › ${esc(r.이름)}</div>
<main class="wrap">
  <p class="eyebrow">${r.slug === 'common' ? 'Guide' : esc(`${r.도} ${r.시군}`)}</p>
  <h1>${esc(허브제목)}</h1>
  <p class="lead" style="max-width:760px">${소개}</p>
  ${칩(r.slug)}
  ${목록.length ? `<div class="cards">${목록.map(카드).join('\n')}</div>`
    : `<div class="empty">${esc(r.이름)} 글은 곧 올라옵니다. 그동안 다른 지역 글을 참고해 보세요.</div>${posts.length ? `<div class="cards">${posts.slice(0, 6).map(카드).join('\n')}</div>` : ''}`}
  ${상담}
</main>
` + 꼬리;
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
    xml = xml.replace(/<\/urlset>\s*$/, 추가 + '</urlset>\n');
    writeFileSync(sm, xml, 'utf8');
  }

  /* ── llms.txt — 「## 블로그」 절을 다시 쓴다 ── */
  const ll = resolve(ROOT, 'llms.txt');
  if (existsSync(ll) && posts.length) {
    let t = readFileSync(ll, 'utf8').replace(/\r\n/g, '\n');
    const 절 = `## 블로그 (행사 준비 정보, 지역별)\n- [행사 준비 블로그](${SITE}/blog/): 안산 · 화성 · 수원 등 경기 지역별 행사 준비 체크리스트\n` +
      posts.map((p) => `- [${p.title}](${SITE}${글주소(p.slug)}): ${p.description}`).join('\n') + '\n';
    /* 「## 블로그」부터 다음 「## 」 절 앞(없으면 끝)까지 바꾼다 — 옛 식은 m 플래그의 $ 가 줄 끝에 걸려 두 번째 실행부터 목록이 겹쳤다 */
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
<title>${esc(BRAND)} 행사 준비 블로그</title><link>${SITE}/blog/</link><description>안산 · 화성 · 수원 등 경기 지역에서 행사를 준비하는 담당자를 위한 글</description><language>ko</language>
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
