"""把每次调用同步一行到对应 assets/<slot>/prompt-log.md。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .config import ASSETS_DIR


def append_entry(
    asset_slot: str,
    *,
    run_id: int,
    model_key: str,
    prompt: str,
    task_id: str,
    result_urls: list[str],
    local_paths: list[str] | None = None,
    parent_run_id: int | None = None,
    feedback: str | None = None,
) -> Path:
    log_path = ASSETS_DIR / asset_slot / "prompt-log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "",
        f"### Run #{run_id} · {ts}",
        f"- **模型**: `{model_key}`",
        f"- **taskId**: `{task_id}`",
    ]
    if parent_run_id:
        lines.append(f"- **基于**: Run #{parent_run_id}")
    if feedback:
        lines.append(f"- **反馈驱动**: {feedback}")
    lines.append("- **Prompt**:")
    lines.append("")
    lines.append("```")
    lines.append(prompt)
    lines.append("```")
    if local_paths:
        lines.append("- **本地文件**:")
        for p in local_paths:
            lines.append(f"  - `{p}`")
    if result_urls:
        lines.append("- **结果 URL（24h 过期）**:")
        for u in result_urls:
            lines.append(f"  - {u}")
    lines.append("")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return log_path
