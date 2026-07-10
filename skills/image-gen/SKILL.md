---
name: image-gen
description: 通用 AI 图像生成 skill,支持 OpenAI / NewAPI 兼容协议的任意中转站和服务商(GPT Image 系列、DALL·E、Doubao Seedream、Gemini Image 等)。内置 Geeknow 实现,默认模型 gpt-image-2,同步 + 异步两种模式,带连接池/重试/限流感知/并行批量的执行栈优化。触发场景:(1) 用户想生成、编辑或变换图片,(2) 用户提到 AI 生图、AI 绘图、生图模型名(dall-e / gpt-image / seedream / gemini-image),(3) 用户提供中转站 API key + URL 想接入自定义服务商,(4) 用户需要批量并行出图。不用于纯文本对话、PPT 排版、文档格式转换。
---

# image-gen · 通用 AI 图像生成

把"提示词 → 一张或多张图片"这件事用 CLI 串起来。默认走 Geeknow + `gpt-image-2`,但协议层是 OpenAI/NewAPI 兼容的,任何相同协议的"中转站"或"服务商"都能接进来。

## 何时使用

- 用户要"生图 / AI 绘图 / 出图 / 给我画一张"
- 用户给了具体的模型名(例如 `gpt-image-2`、`doubao-seedream-4-0-250828`、`gemini-3-pro-image-preview`)
- 用户提供了中转站 URL + API key,想换服务商
- 需要批量并行出图(同一主题多张 / 多主题同时)
- 需要异步提交,先拿 task ID 后续再回来取结果

## 不适用

- 普通 HTML / 网页设计 → 用前端类 skill
- 排版 / 演示文稿 → 用 dashiai-ppt
- 公众号文章排版 → 用 gzh-design
- 文案生成 / 对话 → 不需要生图 skill

## 工作流

1. **确认输入**:从用户那里得到 `prompt`、可选的 `size` / `n` / `model` / `quality` / `response_format`、参考图(可选)。
2. **选服务商**:默认 `geeknow`。如果用户给了别的中转站 URL/API key,选对应 preset,或者临时 inline 指定。
3. **选模式**:
   - **同步(`submit --sync`)**:服务端直接返回 base64 或 URL,适合小图 / 快速迭代。**会阻塞主线程等响应**,超时通常 30-60s。
   - **异步(`submit --async`)**:返回 task ID,服务端在后台跑。**不阻塞主线程**,agent 可以拿 task ID 去干别的活,稍后 `poll` 拿结果。
4. **轮询 / 下载**:异步模式提交后,`poll <task_id>` 检查状态;`pending` / `in_progress` 等,`success` / `completed` 后 `download <url> --out <file>` 落盘。
5. **批量**:多张图并行,`batch --prompts prompts.txt --parallel 4`。内部用 `concurrent.futures` 或 asyncio,**主线程只负责派发,不卡网络 IO**。
6. **交付**:把图返回给用户(贴路径 / 显示 / 嵌入到下游 skill)。

## 关键脚本

| 脚本 | 用途 |
|---|---|
| `submit.py` | 提交任务(sync/async 二选一) |
| `poll.py` | 轮询异步任务状态 |
| `download.py` | 下载 URL 形式的图片结果 |
| `batch.py` | 并行批量提交 |
| `client.py` | 底层 HTTP 客户端:Session 连接池 / 指数退避 / 429 限流感知 / 5xx 重试 / 流式下载 |
| `providers/geeknow.py` | Geeknow 适配器(默认) |

全部脚本都在 `scripts/` 下,执行时用 `python3 <skill-root>/scripts/<name>.py`。

## 环境与配置

**API key 安全原则**:绝不写进 skill 文件,绝不进 git。

读取顺序(高优先级覆盖低优先级):
1. 命令行 `--api-key`
2. 环境变量:`IMAGE_GEN_API_KEY` / `GEEKKNOW_API_KEY` / `OPENAI_API_KEY`(按服务商)
3. `~/.claude/skills/image-gen/config.json`(`{"providers": {"geeknow": {"api_key": "..."}}}`)

**base URL 同样三段**:`IMAGE_GEN_BASE_URL` 环境变量优先,否则走 preset 默认(Geeknow = `https://www.geeknow.top/v1`)。

**如果用户刚把 API key 直接贴在聊天里**(常见情况),立即:
1. 不要把它写进任何 skill 文件或 config
2. 用 Read/Write 工具也不要拼到上下文历史里(尽量短命)
3. 引导用户用 `export IMAGE_GEN_API_KEY=...` 或写进 config(后者建议加 `chmod 600`)
4. 如果用户已发到聊天,提醒他 rotate 一次(因为 LLM 上下文可能被记录)

## 执行栈优化要点

`client.py` 里有,这里写设计意图:
- **连接池**:`requests.Session()` 默认 + HTTPAdapter 调大 `pool_connections` / `pool_maxsize`,避免每次请求重连。
- **指数退避**:网络错误 / 5xx 重试 3 次,backoff 1s → 2s → 4s。
- **限流感知**:429 读 `Retry-After` 头(秒),老老实实等,不暴力重试。
- **流式下载**:结果是大图时 `stream=True` + 写 chunk,避免大文件塞内存。
- **缓存去重**:同一 URL 30 分钟内不重复下载(基于文件 mtime + size 简单判断,不强一致)。
- **并行批量**:`batch.py` 用 ThreadPoolExecutor,把 IO 密集型提交并行起来;**主线程不阻塞**因为 `submit()` 立刻返回 task ID。

## 触发模式(agent 自动识别)

- 出现"画一张 / 生成图片 / AI 出图 / 给我张图"→ 默认走 Geeknow + gpt-image-2 + 1:1
- 出现具体模型名 → 用指定模型
- 出现"批量 / 多来几张 / 一组"→ 走 batch
- 出现"后台跑 / 异步 / 不急"→ 走 async + 之后 poll
- 用户给了 URL + key 配对 → 临时切到该服务商

## 错误处理

- 401/403:API key 错或没权限,提示检查 `IMAGE_GEN_API_KEY`
- 429:限流,读 Retry-After 等
- 5xx:服务端问题,指数退避重试
- 网络超时:30s 默认,可在命令里调
- task 失败:读 `error.message` / `error.code` 给用户

## 验收

跑通后用 `python3 <skill-root>/scripts/submit.py --help` 应该打印出完整参数列表;`--dry-run` 模式不打真实请求,只验证参数和 endpoint 可达性。