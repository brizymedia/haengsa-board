/*
 * 행사ON — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
  { group:'축제 (초 · 중 · 고)', items:[
    { id:'p1', name:'학교축제 음향 · 조명',     spec:'스피커 · 무선마이크 · 디지털 믹서 · 무대 조명 · 오퍼레이터', unit:'식', price:null },
    { id:'p2', name:'학예발표회 · 예술제',      spec:'음향 · 핀마이크(다채널) · 무대 조명 · 무대막 · 풍선장식',    unit:'식', price:null },
    { id:'a5', name:'밴드 공연 추가 구성',      spec:'악기 마이크 · 모니터 스피커 · 밴드 믹싱',                  unit:'식', price:null },
  ]},
  { group:'체육대회 (초 · 중 · 고 · 기업)', items:[
    { id:'p3', name:'체육대회 기본 구성',       spec:'행사 음향 · MC · 게임장비 · 천막',                         unit:'식', price:null },
    { id:'f1', name:'MC · 운영 스태프',         spec:'진행 MC, 경기 운영 스태프 (인원은 규모에 따라)',            unit:'식', price:null },
    { id:'h3', name:'게임 프로그램 · 게임장비', spec:'학년 · 인원에 맞춘 단체 게임 구성',                        unit:'식', price:null },
    { id:'p4', name:'기업 체육대회 (여러 날 진행)', spec:'조별 · 일자별 운영, 천막 · 음향 · 테이블 · 의자 · MC · 스태프', unit:'식', price:null },
  ]},
  { group:'토탈행사', items:[
    { id:'d1', name:'무대 · 무대 덱',           spec:'행사장 크기에 맞춘 무대 구성',                             unit:'식', price:null },
    { id:'b4', name:'트러스',                   spec:'외줄트러스 · 백월 트러스 · 포토존 트러스 · 대형 현수막 구조물', unit:'식', price:null },
    { id:'c1', name:'LED 전광판',               spec:'무대 배경 · 영상 송출',                                    unit:'식', price:null },
    { id:'p5', name:'토탈 시스템 패키지',       spec:'무대 + 트러스 + LED + 조명 + 음향 통합 설계 · 운영',        unit:'식', price:null },
  ]},
  { group:'렌탈', items:[
    { id:'d3',  name:'캐노피 천막',             spec:'규격 · 색상 · 수량 상담, 설치 · 철거 포함 여부 선택',      unit:'동', price:null, qty:true },
    { id:'d12', name:'행사용 테이블',           spec:'접수 · 진열 · 운영본부용',                                 unit:'개', price:null, qty:true },
    { id:'d9',  name:'행사용 의자',             spec:'관람석 · 참가자석',                                        unit:'개', price:null, qty:true },
    { id:'d14', name:'천막 + 테이블 + 의자 묶음', spec:'체육대회 · 운동회 · 주민행사용 한 번에',                  unit:'식', price:null },
  ]},
  { group:'시스템', items:[
    { id:'a1', name:'음향 시스템',              spec:'라인어레이 · 스피커 · 디지털 콘솔 · 무선 · 핀마이크',       unit:'식', price:null },
    { id:'b1', name:'조명',                     spec:'무대 조명 · 무빙 조명',                                    unit:'식', price:null },
    { id:'c2', name:'LED',                      spec:'LED 전광판',                                               unit:'식', price:null },
    { id:'f5', name:'현장 오퍼레이터',          spec:'행사 시간 동안 음향 · 조명 운영',                          unit:'명', price:null },
    { id:'g4', name:'송년회 노래방 기계',       spec:'연말 기업행사용',                                          unit:'식', price:null },
  ]},
  { group:'에어바운스', items:[
    { id:'h1', name:'놀이바운스',               spec:'어린이날 · 가족행사 · 축제용',                             unit:'동', price:null, qty:true },
    { id:'h2', name:'물놀이바운스 · 워터슬라이드', spec:'크기별 보유 — 단지 · 운동장 규모에 맞춰',               unit:'동', price:null, qty:true },
    { id:'h4', name:'에어풀장',                 spec:'대형 · 어린이용',                                          unit:'동', price:null, qty:true },
    { id:'h5', name:'물놀이행사 운영',          spec:'행사 전날 설치 · 저학년 / 고학년 구역 나눠 운영',          unit:'식', price:null },
  ]},
  { group:'아파트', items:[
    { id:'p6', name:'플리마켓 · 야시장',        spec:'셀러 부스 천막 · 테이블 · 의자 · 조명',                    unit:'식', price:null },
    { id:'p7', name:'입주민축제',               spec:'무대 · 음향 · 체험부스 · 어린이 놀이존 · 포토존',          unit:'식', price:null },
    { id:'p8', name:'아파트 물놀이행사',        spec:'에어풀장 · 워터슬라이드 · 물놀이바운스 · 먹거리 부스',      unit:'식', price:null },
    { id:'p9', name:'계절 행사',                spec:'어린이날 · 여름 물놀이 · 가을 야시장 · 크리스마스 · 송년',  unit:'식', price:null },
  ]},
  { group:'행사기획', items:[
    { id:'p10', name:'행사 기획 · 프로그램 구성', spec:'사전 미팅 · 기획안 · 진행표',                            unit:'식', price:null },
    { id:'p11', name:'기업행사 · 송년회 진행',  spec:'MC · 음향 · 조명 · 트러스',                                unit:'식', price:null },
    { id:'p12', name:'개소식 · 개관식 · 준공식', spec:'음향 · 레드카펫 · 테이프커팅식',                          unit:'식', price:null },
    { id:'b5',  name:'졸업식 · 입학식 포토존',  spec:'트러스 포토존 · 레드카펫',                                 unit:'식', price:null },
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
