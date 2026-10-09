# -*- coding: utf-8 -*-
"""수집 실행 진입점

  python run.py                 # 전체 수집 → ../site/data/events.json 갱신
  python run.py --dry-run       # 파일을 쓰지 않고 수집 결과만 출력
  python run.py --only nara     # 특정 출처만 (nara | tour | rss | grant)
                                # 주의: --only 는 그 출처만 events.json 에 쓴다(나머지는 빠진다)
  python run.py --refresh grant # 공모사업만 새로 받아 events.json 의 grant 항목만 바꾼다(나머지는 그대로)
"""
import argparse
import sys

import classify
import config
import store
from collectors import grant, nara, rss, tour

SOURCES = {"nara": nara.fetch, "tour": tour.fetch, "rss": rss.fetch, "grant": grant.fetch}


def refresh(name, dry=False, path=None):
    """events.json 에서 kind 가 name 인 항목만 새로 받은 것으로 바꿔 쓴다. 나머지 항목은 그대로 둔다."""
    import json
    kind = {"grant": "grant"}[name]
    path = path or config.OUT_JSON
    try:
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
    except (OSError, ValueError) as e:
        print(f"기존 events.json 을 읽지 못해 갱신하지 않습니다: {e}", file=sys.stderr)
        return 1
    keep = [r for r in old.get("items", []) if r.get("kind") != kind]
    fresh = classify.finalize(classify.dedupe(SOURCES[name]()))
    items = classify.finalize(keep + fresh)
    print(f"{name} 갱신: 기존 {len(old.get('items', [])) - len(keep)}건 → {len(fresh)}건 (나머지 {len(keep)}건은 그대로)")
    if dry:
        print("dry-run: 파일을 쓰지 않았습니다.")
        return 0
    if not keep:
        print("다른 항목이 하나도 없어 갱신하지 않습니다(전체 수집을 먼저 하세요).", file=sys.stderr)
        return 1
    store.export_json(items, path=path, mock=bool(old.get("mock")))
    print(f"저장 완료: {path} ({len(items)}건)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="행사 공고 수집기")
    ap.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않고 결과만 출력")
    ap.add_argument("--only", choices=sorted(SOURCES), help="특정 출처만 수집")
    ap.add_argument("--refresh", choices=["grant"],
                    help="기존 events.json 은 두고 이 출처 항목만 새로 받아 바꾼다(주간 공모 갱신용)")
    args = ap.parse_args(argv)

    if args.refresh:
        return refresh(args.refresh, dry=args.dry_run)

    if not config.DATA_GO_KR_KEY:
        print("주의: DATA_GO_KR_KEY 환경변수가 없습니다. 나라장터·TourAPI 는 건너뜁니다.")

    items = []
    for name, fetch in SOURCES.items():
        if args.only and name != args.only:
            continue
        try:
            items += fetch()
        except Exception as e:
            # 한 출처가 죽어도 나머지는 배포한다
            print(f"{name} 수집 중 오류(건너뜀): {e}")

    items = classify.dedupe(items)
    items = classify.finalize(items)

    print(f"중복 제거 후 {len(items)}건")
    for r in items[:20]:
        print(f"  [{r['kind']:^8}] {r['region']:>2} | {r['title']}")
    if len(items) > 20:
        print(f"  … 외 {len(items) - 20}건")

    if args.dry_run:
        print("dry-run: 파일을 쓰지 않았습니다.")
        return 0
    if not items:
        print("수집 결과가 0건이라 events.json 을 갱신하지 않습니다.", file=sys.stderr)
        return 1

    con = store.open_db()
    store.upsert(con, items)
    path = store.export_json(items)
    print(f"저장 완료: {path} ({len(items)}건)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
