# -*- coding: utf-8 -*-
"""수집 실행 진입점

  python run.py                 # 전체 수집 → ../site/data/events.json 갱신
  python run.py --dry-run       # 파일을 쓰지 않고 수집 결과만 출력
  python run.py --only nara     # 특정 출처만 (nara | tour | rss)
"""
import argparse
import sys

import classify
import config
import store
from collectors import nara, rss, tour

SOURCES = {"nara": nara.fetch, "tour": tour.fetch, "rss": rss.fetch}


def main(argv=None):
    ap = argparse.ArgumentParser(description="행사 공고 수집기")
    ap.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않고 결과만 출력")
    ap.add_argument("--only", choices=sorted(SOURCES), help="특정 출처만 수집")
    args = ap.parse_args(argv)

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
