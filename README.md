# 京城山海经·新编

AIGC 作品项目：把北京"文脉 × 科创"的六神兽新编为《山海经》卷一，配 90 秒短片。
本仓库包含策划案、实施计划、prompt 日志，以及调用 RunningHub API 的 CLI 工具。

## 仓库策略

- **入库**：`src/`、`.md` 策划文档、`models.toml`、`assets/<slot>/prompt-log.md`、`runs.db`
- **不入库**（见 `.gitignore`）：`.env`、`outputs/`、`.venv/`
- `generate` / `poll` 完成后会**自动下载**结果到 `outputs/<slot>/run####/`，`runs.db` 的 `run_results.local_path` 同时保存该路径（相对仓库根）
- ⚠️ RunningHub 返回的 URL **24h 过期**，所以不要依赖 URL —— 本地文件才是真资产。重要的作品记得再备份一份到网盘 / 硬盘
- 在别的电脑 clone 后看不到 `outputs/`。想把某个 slot 的成片带过去，可以手动把对应 `outputs/<slot>/` 打包同步，或者基于 `runs.db` 里的 prompt 用 `./rh regen` 重出

## 环境搭建

推荐 uv（纯 CLI，不需要 gui，uv 一步到位）：

```bash
# 在仓库根目录
uv venv --python 3.11
uv sync            # 安装 pyproject.toml 中的依赖
# 或 `uv pip install -e .`

# 激活 (bash / git-bash)
source .venv/Scripts/activate   # Windows
# source .venv/bin/activate      # macOS/Linux
```

配置密钥：

```bash
cp .env.example .env
# 编辑 .env 填入 RUNNINGHUB_API_KEY
```

验证：

```bash
./rh --help           # bash / git-bash / macOS / Linux
rh.cmd --help         # Windows cmd
./rh models           # 看有哪些模型注册好了
```

> **Windows 小坑**：项目路径含中文（"沿着总书记指引的方向"），所以**没有**用 uv 生成的 `rh.exe` entry-point —— 那会因 CP936/UTF-8 冲突失败。而是提供根目录的 `rh` / `rh.cmd` 包装脚本直接跑 `python -m jingshan.cli`。两种形式都能正常工作。

## 工作流

### 1. 已注册的模型

`./rh models` 查看。当前 6 个（全部走标准模型 API，扁平 JSON）：

| key | 类型 | 对应平台名 |
|---|---|---|
| `youchuan-v7` | 文生图 | 悠船文生图-v7 |
| `omni-v2` | 文生图 | 全能图片V2-文生图-官方稳定版 |
| `seedream-v5-lite` | 文生图 | seedream-v5-lite-文生图 |
| `vidu-i2v-q3` | 图生视频 | Vidu-图生视频-q3-pro |
| `wan-i2v-2_7` | 图生视频（支持首尾帧） | 万相2.7-图生视频 |
| `seedance-2_0-i2v` | 图生视频（支持首尾帧） | seedance2.0-global/图生视频 |

要加新模型：把文档里对应模型的 path / 字段抄到 [models.toml](models.toml) 即可，不需要跑去 RunningHub 网页端抓 webappId。

### 2. 发起生成

```bash
# 文生图
./rh generate seedream-v5-lite \
  --slot 01_智枢 \
  --prompt "千目千臂的神兽，坐镇中关村星图……" \
  --set resolution=3k

# 图生视频：先 upload 首帧，拿到 URL，再 generate
./rh upload outputs/01_智枢/run0003/result_1.png
# => 复制输出里的 download_url
./rh generate wan-i2v-2_7 \
  --slot 01_智枢 \
  --prompt "神兽缓缓展翼，星图在身后旋转" \
  --set firstImageUrl=https://rh-xxx.cos.../xxx.png \
  --set duration=8 --set resolution=1080P
```

`--set key=value` 覆盖 `defaults` 里的任意字段。`true/false` 自动识别为布尔，纯数字为整数。

发起后会：
1. 在 `runs.db` 插入一行 run，状态 `QUEUED`
2. 轮询 `/openapi/v2/query` 直到 `SUCCESS`/`FAILED`
3. 结果 URL 存进 `run_results` 表
4. **立即下载**到 `outputs/01_智枢/run0012/`，`local_path` 写回 DB
5. 同步一条记录（含本地路径）追加到 `assets/01_智枢/prompt-log.md`

### 3. 看结果

```bash
./rh list --slot 01_智枢        # 列表
./rh show 12                   # 详情：prompt / params / 本地文件 / URL
./rh download 12               # 兜底重下（一般不用）；URL 过期会失败
./rh download 12 --force       # 覆盖重下
```

### 4. 反馈 → 再生（核心迭代循环）

你看了结果后给改进方向：

```bash
./rh feedback 12 "眼睛太写实，换成工笔重彩勾线 + 石青石绿晕染"
```

然后让我（AI）根据反馈改 prompt，再调：

```bash
# 沿用原 prompt + 人工调整
./rh regen 12 --prompt "<新 prompt>"
# 或不指定 prompt，沿用旧 prompt（用于换模型 / 调参数）
./rh regen 12 --model omni-v2 --set aspectRatio=2:3 --set resolution=4k
```

`regen` 会把新的 run 的 `parent_run_id` 设成 12，形成迭代链。

### 5. 上传参考图（图生图 / 图生视频需要）

```bash
./rh upload references/style-anchor.png
# 输出里的 download_url 就是公网可访问的 URL，直接作为 --set imageUrl=... 的值传给 generate
# 上传返回的 fileName 主要给老式 nodeInfoList 调用用，标准模型 API 用 URL 更方便
```

## 另一台电脑上 clone 后

```bash
git clone ...
cp .env.example .env  # 填 key
uv sync
# 查历史（runs.db 入库，能看到每个 run 的 prompt / 参数 / 曾经的 URL）
./rh list
./rh show 5
# outputs/ 不入库，所以这台机器上还没有结果文件
# 想看原成片：手动同步 outputs/<slot>/；或基于原 prompt 重出一次
./rh regen 5
```

## 目录

```
.
├── 京城山海经·新编-策划案.md
├── 京城山海经·新编-实施计划.md
├── README.md
├── pyproject.toml
├── models.toml              # 模型注册表（必须配）
├── .env.example             # 密钥模板
├── rh / rh.cmd              # 两个包装脚本（bash / cmd）
├── runs.db                  # SQLite；run 元数据 + 结果 URL（入库）
├── jingshan/                # CLI 实现
│   ├── cli.py
│   ├── client.py            # RunningHub HTTP 封装
│   ├── db.py                # SQLite schema + CRUD
│   ├── models.py            # models.toml 加载
│   ├── promptlog.py         # 同步 assets/<slot>/prompt-log.md
│   └── config.py
├── assets/<slot>/           # 每个神兽 / 总览 / 视频的 prompt-log.md（入库）
├── outputs/<slot>/run####/  # 下载回来的图/视频（不入库）
└── references/              # 风格参考素材
```

## 常见坑

- `code=0` 是成功；非零看 `msg` 和 `errorMessage`
- 下载链接有效期 24h。重要的作品下载完立刻备份到你自己的云盘或本地盘
- `nodeInfoList` 里的 `fieldValue` 必须是字符串（即使是 INT 也传字符串）
- RunningHub 官方把个人账户的并发限制在 1 个任务；建议串行而不是并行发
