# -*- coding: utf-8 -*-
"""SQLite 저장 · JSON 내보내기

DB는 수집 이력(최초 확인일)을 이어가기 위한 것이고, 사이트가 읽는 건 JSON 하나다.
"""
import json
import os
import sqlite3
from datetime import datetime

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  uid        TEXT PRIMARY KEY,
  first_seen TEXT NOT NULL,
  last_seen  TEXT NOT NULL,
  payload    TEXT NOT NULL
)
"""


def open_db(path=None):
    con = sqlite3.connect(path or config.DB_PATH)
    con.execute(SCHEMA)
    return con


def upsert(con, items, now=None):
    """있으면 payload·last_seen 갱신, 없으면 새로 넣는다. first_seen 은 보존."""
    now = now or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for r in items:
        con.execute(
            """INSERT INTO events(uid, first_seen, last_seen, payload)
               VALUES(?,?,?,?)
               ON CONFLICT(uid) DO UPDATE SET
                 last_seen=excluded.last_seen, payload=excluded.payload""",
            (r["uid"], now, now, json.dumps(r, ensure_ascii=False)),
        )
    con.commit()


def first_seen(con, uid):
    row = con.execute("SELECT first_seen FROM events WHERE uid=?", (uid,)).fetchone()
    return row[0] if row else None


def export_json(items, path=None, mock=False, generated_at=None):
    """사이트가 읽는 events.json 을 쓴다."""
    path = path or config.OUT_JSON
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "generated_at": generated_at or datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "mock": bool(mock),
        "count": len(items),
        "items": items,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return path
