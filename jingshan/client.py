"""RunningHub HTTP 客户端，只封装我们用到的几个接口。"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import httpx

from .config import Settings


class RHError(RuntimeError):
    pass


class RunningHubClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._client = httpx.Client(
            base_url=settings.base_url,
            headers={"Authorization": f"Bearer {settings.api_key}"},
            timeout=httpx.Timeout(60.0, connect=15.0),
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    # ---------- 任务发起 ----------

    def run_quick_ai_app(
        self,
        *,
        webapp_id: str,
        quick_create_code: str,
        node_info_list: list[dict[str, Any]],
    ) -> str:
        """发起快捷创作任务，返回 taskId。"""
        body = {
            "apiKey": self.settings.api_key,
            "webappId": webapp_id,
            "quickCreateCode": quick_create_code,
            "nodeInfoList": node_info_list,
        }
        r = self._post("/task/openapi/quick-ai-app/run", body)
        return str(r["data"]["taskId"])

    def run_ai_app(
        self,
        *,
        webapp_id: str,
        node_info_list: list[dict[str, Any]],
        instance_type: str | None = None,
    ) -> str:
        body: dict[str, Any] = {
            "apiKey": self.settings.api_key,
            "webappId": webapp_id,
            "nodeInfoList": node_info_list,
        }
        if instance_type:
            body["instanceType"] = instance_type
        r = self._post("/task/openapi/ai-app/run", body)
        return str(r["data"]["taskId"])

    def run_standard_model(self, path: str, body: dict[str, Any]) -> str:
        """发起标准模型 API（扁平 JSON，直接返回 taskId/status）。"""
        resp = self._client.post(path, json=body)
        resp.raise_for_status()
        data = resp.json()
        # 有些标准模型返回包装 {code, data:{taskId}}；有些直接扁平
        if "code" in data and data.get("code") not in (0, None):
            raise RHError(f"{path} 返回错误: code={data.get('code')} msg={data.get('msg') or data.get('errorMessage')}")
        task_id = data.get("taskId") or (data.get("data") or {}).get("taskId")
        if not task_id:
            raise RHError(f"{path} 响应缺少 taskId: {data}")
        return str(task_id)

    # ---------- 上传 ----------

    def upload_file(self, path: Path) -> dict[str, Any]:
        """上传参考图 / 首尾帧等。返回 {type, download_url, fileName, size}。"""
        with open(path, "rb") as f:
            files = {"file": (path.name, f)}
            resp = self._client.post(
                "/openapi/v2/media/upload/binary",
                files=files,
            )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RHError(f"上传失败: {data}")
        return data["data"]

    # ---------- 查询 / 轮询 ----------

    def query_v2(self, task_id: str) -> dict[str, Any]:
        """v2 查询。返回解包后的 payload（若响应是 {code, data} 则返回 data）。"""
        resp = self._client.post("/openapi/v2/query", json={"taskId": task_id})
        resp.raise_for_status()
        data = resp.json()
        if "code" in data and "data" in data and data.get("code") in (0, None):
            return data["data"] or {}
        return data

    def wait(self, task_id: str, on_tick=None) -> dict[str, Any]:
        """轮询直至 SUCCESS / FAILED，返回最终 payload（含 status / results）。"""
        deadline = time.monotonic() + self.settings.poll_timeout
        last_status = None
        while time.monotonic() < deadline:
            data = self.query_v2(task_id)
            status = data.get("status") or data.get("taskStatus")
            if status != last_status and on_tick:
                on_tick(status, data)
                last_status = status
            if status == "SUCCESS":
                return data
            if status == "FAILED":
                msg = data.get("errorMessage") or data.get("promptTips") or "unknown"
                raise RHError(f"任务失败: {msg}")
            time.sleep(self.settings.poll_interval)
        raise RHError(f"轮询超时（{self.settings.poll_timeout}s）: taskId={task_id}")

    # ---------- 下载 ----------

    def download(self, url: str, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with self._client.stream("GET", url) as resp:
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_bytes(chunk_size=1 << 16):
                    f.write(chunk)

    # ---------- 内部 ----------

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        resp = self._client.post(path, json=body)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") not in (0, None):
            raise RHError(f"{path} 返回错误: code={data.get('code')} msg={data.get('msg')}")
        return data
