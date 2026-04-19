from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import typer
from rich.console import Console
from rich.table import Table

from . import db, promptlog
from .client import RHError, RunningHubClient
from .config import OUTPUTS_DIR, load_settings
from .models import ModelSpec, build_node_info, build_standard_body, load_registry

app = typer.Typer(help="京城山海经 · RunningHub AIGC 调用 / 归档工具")
console = Console()


def _client() -> RunningHubClient:
    return RunningHubClient(load_settings())


def _parse_overrides(items: list[str]) -> dict[str, Any]:
    """解析 --set key=value。value 自动识别 true/false / 整数 / 其余为字符串。"""
    out: dict[str, Any] = {}
    for it in items:
        if "=" not in it:
            raise typer.BadParameter(f"--set 需要 fieldName=value，收到: {it}")
        k, v = it.split("=", 1)
        v = v.strip()
        low = v.lower()
        if low == "true":
            out[k.strip()] = True
        elif low == "false":
            out[k.strip()] = False
        elif v.lstrip("-").isdigit():
            out[k.strip()] = int(v)
        else:
            out[k.strip()] = v
    return out


def _do_generate(
    *,
    spec: ModelSpec,
    slot: str,
    prompt: str,
    overrides: dict[str, Any],
    parent: int | None,
    feedback: str | None,
    no_wait: bool,
) -> int:
    # 根据 endpoint 类型准备 params
    if spec.endpoint == "standard":
        body = build_standard_body(spec, prompt, overrides)
        params_for_db: dict[str, Any] = {"path": spec.path, "body": body}
    else:
        node_info = build_node_info(spec, prompt, overrides)
        params_for_db = {"nodeInfoList": node_info}

    run_id = db.insert_run(
        model_key=spec.key, asset_slot=slot, kind=spec.kind,
        prompt=prompt, params=params_for_db, parent_run_id=parent,
    )
    if feedback:
        db.set_feedback(run_id, feedback)

    with _client() as cli:
        console.print(f"[cyan]发起任务[/cyan] run_id={run_id} model={spec.key}")
        if spec.endpoint == "standard":
            task_id = cli.run_standard_model(spec.path, body)
        elif spec.endpoint == "quick_ai_app":
            task_id = cli.run_quick_ai_app(
                webapp_id=spec.webapp_id,
                quick_create_code=spec.quick_create_code or "",
                node_info_list=params_for_db["nodeInfoList"],
            )
        elif spec.endpoint == "ai_app":
            task_id = cli.run_ai_app(
                webapp_id=spec.webapp_id,
                node_info_list=params_for_db["nodeInfoList"],
            )
        else:
            console.print(f"[red]未知 endpoint: {spec.endpoint}[/red]"); raise typer.Exit(2)
        db.set_task_id(run_id, task_id)
        console.print(f"[green]taskId={task_id}[/green]")

        if no_wait:
            console.print(f"--no-wait：稍后用 `rh poll {run_id}` 轮询。")
            return run_id

        try:
            data = cli.wait(task_id, on_tick=lambda s, _: console.print(f"  状态: {s}"))
        except RHError as e:
            db.update_status(run_id, "FAILED", str(e))
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)

    results = data.get("results") or []
    db.update_status(run_id, "SUCCESS")
    db.add_results(run_id, [{"url": r["url"], "outputType": r.get("outputType")} for r in results])
    urls = [r["url"] for r in results]
    local_paths = _download_results(run_id, slot)
    promptlog.append_entry(
        slot, run_id=run_id, model_key=spec.key, prompt=prompt,
        task_id=task_id, result_urls=urls, local_paths=local_paths,
        parent_run_id=parent, feedback=feedback,
    )
    console.print(f"[bold green]完成 run #{run_id}[/bold green] -- {len(urls)} 个结果:")
    for p in local_paths:
        console.print(f"  - {p}")
    return run_id


def _download_results(run_id: int, slot: str, force: bool = False) -> list[str]:
    """下载 run 的所有结果到本地并写回 local_path。返回相对仓库根的路径列表。"""
    results = db.get_run_results(run_id)
    if not results:
        return []
    dest_dir = OUTPUTS_DIR / slot / f"run{run_id:04d}"
    paths: list[str] = []
    with _client() as cli:
        for r in results:
            if r["local_path"] and not force:
                paths.append(r["local_path"])
                continue
            suffix = Path(r["file_url"].split("?")[0]).suffix or ".bin"
            dest = dest_dir / f"result_{r['id']}{suffix}"
            try:
                cli.download(r["file_url"], dest)
            except Exception as e:
                console.print(f"[red]下载失败 {r['file_url']}: {e}[/red]")
                continue
            rel = str(dest.relative_to(OUTPUTS_DIR.parent))
            db.set_local_path(r["id"], rel)
            paths.append(rel)
    return paths


@app.command()
def models() -> None:
    """列出 models.toml 中注册的模型。"""
    reg = load_registry()
    if not reg:
        console.print("[yellow]models.toml 为空或不存在。[/yellow]")
        raise typer.Exit(1)
    tbl = Table("key", "kind", "endpoint", "path / webapp_id")
    for spec in reg.values():
        ident = spec.path if spec.endpoint == "standard" else spec.webapp_id
        tbl.add_row(spec.key, spec.kind, spec.endpoint, ident)
    console.print(tbl)


@app.command()
def generate(
    model_key: str = typer.Argument(..., help="models.toml 中的 key"),
    slot: str = typer.Option(..., "--slot", "-s", help="资产分栏，例如 01_智枢"),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p"),
    prompt_file: Optional[Path] = typer.Option(None, "--prompt-file"),
    override: list[str] = typer.Option([], "--set", help="覆盖 extra_nodes: fieldName=value"),
    parent: Optional[int] = typer.Option(None, "--parent"),
    feedback: Optional[str] = typer.Option(None, "--feedback"),
    no_wait: bool = typer.Option(False, "--no-wait"),
):
    """发起一次生成。"""
    reg = load_registry()
    if model_key not in reg:
        console.print(f"[red]未找到模型 {model_key}[/red]；可用：{list(reg)}")
        raise typer.Exit(2)
    if prompt_file:
        prompt = prompt_file.read_text(encoding="utf-8").strip()
    if not prompt:
        raise typer.BadParameter("必须提供 --prompt 或 --prompt-file")
    _do_generate(
        spec=reg[model_key], slot=slot, prompt=prompt,
        overrides=_parse_overrides(override),
        parent=parent, feedback=feedback, no_wait=no_wait,
    )


@app.command()
def poll(run_id: int):
    """对已发起的 run 做轮询并写回结果。"""
    row = db.get_run(run_id)
    if not row:
        console.print(f"[red]run #{run_id} 不存在[/red]"); raise typer.Exit(2)
    if not row["task_id"]:
        console.print("[red]此 run 尚无 taskId[/red]"); raise typer.Exit(2)
    with _client() as cli:
        try:
            data = cli.wait(row["task_id"], on_tick=lambda s, _: console.print(f"  {s}"))
        except RHError as e:
            db.update_status(run_id, "FAILED", str(e))
            console.print(f"[red]{e}[/red]"); raise typer.Exit(1)
    results = data.get("results") or []
    db.update_status(run_id, "SUCCESS")
    db.add_results(run_id, [{"url": r["url"], "outputType": r.get("outputType")} for r in results])
    local_paths = _download_results(run_id, row["asset_slot"])
    promptlog.append_entry(
        row["asset_slot"], run_id=run_id, model_key=row["model_key"],
        prompt=row["prompt"], task_id=row["task_id"],
        result_urls=[r["url"] for r in results], local_paths=local_paths,
        parent_run_id=row["parent_run_id"], feedback=row["feedback"],
    )
    console.print(f"[green]完成 run #{run_id}[/green] -- {len(local_paths)} 个文件")
    for p in local_paths:
        console.print(f"  - {p}")


@app.command("list")
def list_cmd(
    slot: Optional[str] = typer.Option(None, "--slot", "-s"),
    limit: int = typer.Option(30, "--limit", "-n"),
):
    """列出最近的 run。"""
    rows = db.list_runs(slot, limit)
    tbl = Table("id", "slot", "model", "status", "task_id", "parent", "feedback", "created")
    for r in rows:
        tbl.add_row(
            str(r["id"]), r["asset_slot"], r["model_key"], r["status"],
            r["task_id"] or "-", str(r["parent_run_id"] or "-"),
            (r["feedback"] or "")[:40], r["created_at"][:16],
        )
    console.print(tbl)


@app.command()
def show(run_id: int):
    """查看 run 详情。"""
    row = db.get_run(run_id)
    if not row:
        console.print(f"[red]run #{run_id} 不存在[/red]"); raise typer.Exit(2)
    console.print(f"[bold]Run #{run_id}[/bold]  slot={row['asset_slot']}  model={row['model_key']}  status={row['status']}")
    console.print(f"taskId: {row['task_id']}")
    if row["parent_run_id"]:
        console.print(f"parent: #{row['parent_run_id']}")
    if row["feedback"]:
        console.print(f"feedback: {row['feedback']}")
    console.print("\n[bold]Prompt[/bold]:"); console.print(row["prompt"])
    console.print("\n[bold]Params[/bold]:"); console.print_json(row["params_json"])
    console.print("\n[bold]Results[/bold]:")
    for r in db.get_run_results(run_id):
        tag = "[dim](已下载)[/dim]" if r["local_path"] else "[yellow](仅链接)[/yellow]"
        console.print(f"  - {tag} {r['file_url']}")
        if r["local_path"]:
            console.print(f"      -> {r['local_path']}")


@app.command()
def download(
    run_id: int,
    force: bool = typer.Option(False, "--force", help="已下载的也覆盖重下"),
):
    """重新下载 run 的结果（一般不需要，generate / poll 会自动下载）。URL 24h 过期。"""
    row = db.get_run(run_id)
    if not row:
        console.print(f"[red]run #{run_id} 不存在[/red]"); raise typer.Exit(2)
    paths = _download_results(run_id, row["asset_slot"], force=force)
    if not paths:
        console.print("[yellow]此 run 无可用结果[/yellow]"); return
    for p in paths:
        console.print(f"  - {p}")


@app.command()
def feedback(run_id: int, text: str = typer.Argument(...)):
    """把改进方向写到 run 上，作为下一轮 regen 的参考。"""
    db.set_feedback(run_id, text)
    console.print(f"[green]run #{run_id} 反馈已保存[/green]")


@app.command()
def regen(
    run_id: int = typer.Argument(..., help="基于哪一轮再生"),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p"),
    prompt_file: Optional[Path] = typer.Option(None, "--prompt-file"),
    model_key: Optional[str] = typer.Option(None, "--model"),
    override: list[str] = typer.Option([], "--set"),
    no_wait: bool = typer.Option(False, "--no-wait"),
):
    """基于某 run 发起下一轮（parent 链接起来）。不指定 prompt 时沿用原 prompt。"""
    row = db.get_run(run_id)
    if not row:
        console.print(f"[red]run #{run_id} 不存在[/red]"); raise typer.Exit(2)
    reg = load_registry()
    key = model_key or row["model_key"]
    if key not in reg:
        console.print(f"[red]模型 {key} 未注册[/red]"); raise typer.Exit(2)
    new_prompt = prompt
    if prompt_file:
        new_prompt = prompt_file.read_text(encoding="utf-8").strip()
    if not new_prompt:
        new_prompt = row["prompt"]
    _do_generate(
        spec=reg[key], slot=row["asset_slot"], prompt=new_prompt,
        overrides=_parse_overrides(override),
        parent=run_id, feedback=row["feedback"], no_wait=no_wait,
    )


@app.command()
def upload(path: Path):
    """上传本地图片/视频到 RunningHub，返回 fileName / download_url。"""
    if not path.exists():
        console.print(f"[red]{path} 不存在[/red]"); raise typer.Exit(2)
    with _client() as cli:
        info = cli.upload_file(path)
    console.print_json(data=info)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
