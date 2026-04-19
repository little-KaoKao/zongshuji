"""模型注册表：把 models.toml 里的条目映射成调用参数。

支持两种 endpoint：
- standard：标准模型 API，扁平 JSON，POST 到 models.<key>.path
- quick_ai_app / ai_app：ComfyUI 工作流封装，需要 webappId + nodeInfoList
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from .config import MODELS_TOML


@dataclass
class ModelSpec:
    key: str
    kind: str                                    # image | video | audio
    endpoint: str                                # standard | quick_ai_app | ai_app

    # --- standard 专用 ---
    path: str = ""                               # POST 路径，如 /openapi/v2/vidu/image-to-video-q3-pro
    prompt_field: str = "prompt"                 # prompt 在 body 里的字段名
    defaults: dict[str, Any] = field(default_factory=dict)  # 请求体其余默认字段
    image_fields: list[str] = field(default_factory=list)   # 哪些字段需要走 upload → URL

    # --- quick_ai_app / ai_app 专用 ---
    webapp_id: str = ""
    quick_create_code: str | None = None
    prompt_node: dict[str, str] = field(default_factory=dict)
    extra_nodes: list[dict[str, Any]] = field(default_factory=list)


def load_registry() -> dict[str, ModelSpec]:
    if not MODELS_TOML.exists():
        return {}
    data = tomllib.loads(MODELS_TOML.read_text(encoding="utf-8"))
    out: dict[str, ModelSpec] = {}
    for key, cfg in data.get("models", {}).items():
        endpoint = cfg.get("endpoint", "standard")
        out[key] = ModelSpec(
            key=key,
            kind=cfg["kind"],
            endpoint=endpoint,
            path=cfg.get("path", ""),
            prompt_field=cfg.get("prompt_field", "prompt"),
            defaults=dict(cfg.get("defaults", {})),
            image_fields=list(cfg.get("image_fields", [])),
            webapp_id=str(cfg.get("webapp_id", "")),
            quick_create_code=cfg.get("quick_create_code"),
            prompt_node=cfg.get("prompt_node", {}),
            extra_nodes=list(cfg.get("extra_nodes", [])),
        )
    return out


def build_node_info(
    spec: ModelSpec,
    prompt: str,
    overrides: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """quick_ai_app / ai_app 用：组装 nodeInfoList。"""
    overrides = overrides or {}
    nodes: list[dict[str, Any]] = [{**spec.prompt_node, "fieldValue": prompt}]
    for n in spec.extra_nodes:
        n2 = dict(n)
        if n2["fieldName"] in overrides:
            n2["fieldValue"] = overrides[n2["fieldName"]]
        nodes.append(n2)
    return nodes


def build_standard_body(
    spec: ModelSpec,
    prompt: str,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """standard 用：组装扁平 body。overrides 直接按 fieldName 覆盖 defaults。"""
    body: dict[str, Any] = dict(spec.defaults)
    body[spec.prompt_field] = prompt
    for k, v in (overrides or {}).items():
        body[k] = v
    return body
