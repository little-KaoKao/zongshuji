from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id        TEXT    UNIQUE,
    model_key      TEXT    NOT NULL,
    asset_slot     TEXT    NOT NULL,
    kind           TEXT    NOT NULL,          -- image | video | audio | other
    prompt         TEXT    NOT NULL,
    params_json    TEXT    NOT NULL,          -- 发起时的 nodeInfoList / 其它参数
    status         TEXT    NOT NULL,          -- QUEUED|RUNNING|SUCCESS|FAILED|CREATED
    error_message  TEXT,
    parent_run_id  INTEGER,                   -- 上一轮，用于迭代链
    feedback       TEXT,                      -- 你对此条的改进方向，留给下一轮参考
    created_at     TEXT    NOT NULL,
    updated_at     TEXT    NOT NULL,
    FOREIGN KEY (parent_run_id) REFERENCES runs(id)
);

CREATE TABLE IF NOT EXISTS run_results (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id         INTEGER NOT NULL,
    file_url       TEXT    NOT NULL,
    file_type      TEXT,
    output_type    TEXT,
    local_path     TEXT,                      -- 下载后的相对路径，未下载则 NULL
    created_at     TEXT    NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_runs_slot ON runs(asset_slot);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
CREATE INDEX IF NOT EXISTS idx_results_run ON run_results(run_id);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    with _connect(db_path) as conn:
        conn.executescript(SCHEMA)


@contextmanager
def session() -> Iterator[sqlite3.Connection]:
    init_db()
    conn = _connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_run(
    *,
    model_key: str,
    asset_slot: str,
    kind: str,
    prompt: str,
    params: dict[str, Any],
    parent_run_id: int | None = None,
) -> int:
    now = _now()
    with session() as conn:
        cur = conn.execute(
            """INSERT INTO runs(model_key, asset_slot, kind, prompt, params_json,
                                status, parent_run_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, 'CREATED', ?, ?, ?)""",
            (model_key, asset_slot, kind, prompt, json.dumps(params, ensure_ascii=False),
             parent_run_id, now, now),
        )
        return int(cur.lastrowid)


def set_task_id(run_id: int, task_id: str) -> None:
    with session() as conn:
        conn.execute(
            "UPDATE runs SET task_id=?, status='QUEUED', updated_at=? WHERE id=?",
            (task_id, _now(), run_id),
        )


def update_status(run_id: int, status: str, error_message: str | None = None) -> None:
    with session() as conn:
        conn.execute(
            "UPDATE runs SET status=?, error_message=?, updated_at=? WHERE id=?",
            (status, error_message, _now(), run_id),
        )


def add_results(run_id: int, items: list[dict[str, Any]]) -> None:
    now = _now()
    with session() as conn:
        for it in items:
            conn.execute(
                """INSERT INTO run_results(run_id, file_url, file_type, output_type, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (run_id, it.get("fileUrl") or it.get("url"),
                 it.get("fileType"), it.get("outputType"), now),
            )


def set_local_path(result_id: int, local_path: str) -> None:
    with session() as conn:
        conn.execute("UPDATE run_results SET local_path=? WHERE id=?", (local_path, result_id))


def set_feedback(run_id: int, feedback: str) -> None:
    with session() as conn:
        conn.execute(
            "UPDATE runs SET feedback=?, updated_at=? WHERE id=?",
            (feedback, _now(), run_id),
        )


def get_run(run_id: int) -> sqlite3.Row | None:
    with session() as conn:
        return conn.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()


def get_run_results(run_id: int) -> list[sqlite3.Row]:
    with session() as conn:
        return conn.execute(
            "SELECT * FROM run_results WHERE run_id=? ORDER BY id", (run_id,)
        ).fetchall()


def list_runs(asset_slot: str | None = None, limit: int = 50) -> list[sqlite3.Row]:
    q = "SELECT * FROM runs"
    args: tuple[Any, ...] = ()
    if asset_slot:
        q += " WHERE asset_slot=?"
        args = (asset_slot,)
    q += " ORDER BY id DESC LIMIT ?"
    args = args + (limit,)
    with session() as conn:
        return conn.execute(q, args).fetchall()
