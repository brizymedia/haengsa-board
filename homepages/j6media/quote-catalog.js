/*
 * 제이식스미디어 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
  { group:'행사 음향 · 조명 운영', items:[
    { id:'p1', name:'교회행사 음향 · 조명',     spec:'예배 · 세미나 · 수련회 · 찬양 집회',      unit:'식', price:null },
    { id:'p2', name:'기업행사 음향 · 조명',     spec:'포럼 · 고객초청 음악회 · 송년 콘서트',    unit:'식', price:null },
    { id:'p3', name:'지자체 · 컨퍼런스 음향',   spec:'영화제 · 제막식 · 컨퍼런스 · 마켓',      unit:'식', price:null },
    { id:'p4', name:'학교행사 음향',            spec:'체육대회 · 축제 · 공연',                  unit:'식', price:null },
    { id:'p5', name:'전시 · 공연 입체음향',     spec:'이머시브 사운드 · 콘서트 · 패션쇼',      unit:'식', price:null },
  ]},
  { group:'음향 렌탈', items:[
    { id:'a1', name:'음향 (소형)',            spec:'세미나 · 강연 · 소규모 예배',              unit:'식', price:null },
    { id:'a2', name:'음향 (중형)',            spec:'수련회 · 실내 공연 · 풀밴드 찬양',          unit:'식', price:null },
    { id:'a3', name:'음향 (대형)',            spec:'NEXO 라인어레이 · 야외 공연 · 축제',        unit:'식', price:null },
    { id:'a4', name:'무선 마이크 추가',       spec:'핸드 / 핀 마이크',                          unit:'개', price:null, qty:true },
    { id:'a5', name:'무선 인이어 · 퍼스널 모니터', spec:'연주자 · 찬양팀 모니터',               unit:'채널', price:null, qty:true },
    { id:'a6', name:'모니터 스피커',          spec:'무대 모니터 (웨지)',                        unit:'대', price:null, qty:true },
    { id:'a7', name:'디지털 믹서',            spec:'YAMAHA · MIDAS 등',                         unit:'대', price:null },
  ]},
  { group:'조명 렌탈', items:[
    { id:'b1', name:'무빙 · 빔 라이트',       spec:'무대 크기 · 분위기 협의',                   unit:'식', price:null },
    { id:'b2', name:'레이저',                 spec:'공연 · 축제 연출',                          unit:'식', price:null },
    { id:'b3', name:'LED 바 · 스트로보',      spec:'무대 바닥 · 배경 조명',                     unit:'식', price:null },
  ]},
  { group:'영상', items:[
    { id:'b4', name:'프로젝터 · 스크린',      spec:'행사 영상 · 자막 송출',                     unit:'식', price:null },
  ]},
  { group:'운영 인력', items:[
    { id:'f1', name:'음향 엔지니어',          spec:'현장 믹싱 · 운영',                          unit:'명', price:null, qty:true },
    { id:'f2', name:'조명 오퍼레이터',        spec:'조명 운영',                                 unit:'명', price:null, qty:true },
    { id:'f5', name:'설치 · 철수 스탭',       spec:'현장 인력',                                 unit:'명', price:null, qty:true },
  ]},
  { group:'음향 · 영상 · 방송장비 설치', items:[
    { id:'i1', name:'교회 음향 · 영상 시스템',  spec:'본당 · 교육관 · 예배실 · 리모델링',       unit:'식', price:null },
    { id:'i2', name:'카페 · 매장 BGM 음향',     spec:'실내 · 야외 방수 스피커',                 unit:'식', price:null },
    { id:'i3', name:'강당 · 홀 · 공간대여 음향 영상', spec:'컬럼 스피커 · 레이저 프로젝터',     unit:'식', price:null },
    { id:'i4', name:'입체음향 · 스튜디오',     spec:'이머시브 · 7.1채널',                       unit:'식', price:null },
    { id:'i5', name:'방송 · 영상 장비',        spec:'전광판 · TV · 영상 송출',                  unit:'식', price:null },
    { id:'i6', name:'점검 · 튜닝 · 유지보수',  spec:'기존 장비 점검 · 사용법 안내',             unit:'식', price:null },
  ]},
  { group:'기타', items:[
    { id:'g2', name:'운반 · 설치 인건비',     spec:'상하차 · 설치 · 철수',                      unit:'식', price:null },
    { id:'g3', name:'출장비',                 spec:'수도권 외 지역',                            unit:'식', price:null },
  ]},
];
const BY_ID = {};
CATALOG.forEach(g => g.items.forEach(it => { BY_ID[it.id] = it; }));

const 견적정보칸 = ['org','name','tel','email','title','date','place','people','memo'];
const 견적정보짧게 = { org:'o', name:'n', tel:'t', email:'e', title:'m', date:'d', place:'p', people:'c', memo:'x' };

const 견적b64u   = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const 견적unb64u = (s) => {
  let t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (t.length % 4) t += '=';
  return decodeURIComponent(escape(atob(t)));
};

/**
 * 견적 코드를 사람이 읽을 수 있는 모양으로 푼다.
 *   { 정보:{org,name,tel,…}, 줄:[{id,name,spec,qty,unit,days,price}], 할인 }
 * 못 읽으면 null.
 */
function 견적풀기(코드) {
  try {
    const s = JSON.parse(견적unb64u(코드));
    const 정보 = {};
    견적정보칸.forEach((k, idx) => {
      const i = s.i;
      if (!i) { 정보[k] = ''; return; }
      const v = Array.isArray(i) ? i[idx]
              : (i[견적정보짧게[k]] != null ? i[견적정보짧게[k]] : i[k]);
      정보[k] = v == null ? '' : String(v);
    });

    const 책 = (id) => BY_ID[id] || { name: '', spec: '', unit: '식' };
    const 줄 = (s.r || []).map((a) => {
      if (typeof a === 'string') {
        const c = 책(a);
        return { id: a, name: c.name, spec: c.spec, qty: 1, unit: c.unit, days: 1, price: null };
      }
      if (a.length <= 4) {
        const c = 책(a[0]);
        return { id: a[0], name: c.name, spec: c.spec,
                 qty: a[1] != null ? a[1] : 1, unit: c.unit,
                 days: a[2] != null ? a[2] : 1,
                 price: a[3] != null ? a[3] : null };
      }
      return { id: a[0], name: a[1], spec: a[2], qty: a[3], unit: a[4], days: a[5], price: a[6] };
    });

    return { 정보: 정보, 줄: 줄, 할인: +s.d || 0 };
  } catch (e) { return null; }
}

/* 견적 한 줄을 「300명 내외 · 스피커 4통 · 2개 · 2일」 같은 한 줄 설명으로 */
function 견적줄설명(r) {
  return [r.spec, (+r.qty > 1 ? r.qty + (r.unit || '') : ''), (+r.days > 1 ? r.days + '일' : '')]
    .filter(Boolean).join(' · ');
}
