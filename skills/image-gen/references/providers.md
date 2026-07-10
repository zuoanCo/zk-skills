# 中转站 / 服务商接入指南

image-gen skill 的协议层是 OpenAI / NewAPI 兼容接口。任何提供该协议的"中转站"或"上游服务商"都能接进来——只要它支持 `POST /v1/images/generations` 风格即可。

## 已内置

| 名称 | 默认 base_url | 默认模型 | 备注 |
|---|---|---|---|
| `geeknow` | `https://www.geeknow.top/v1` | `gpt-image-2` | Geeknow AI 中转,完整实现 sync + async + poll |

## 协议兼容矩阵

判断一个中转站能否直接用 `geeknow` preset 的简单方法:

1. 文档里有没有 `POST /v1/images/generations`?
2. 请求体是不是 `{ "model": ..., "prompt": ..., "size": ..., "n": ... }` 这种 OpenAI 形状?
3. 鉴权是不是 `Authorization: Bearer <key>`?

三个都是 → 直接复用 Geeknow preset,只需在 env 里改 `IMAGE_GEN_BASE_URL` 和 `IMAGE_GEN_API_KEY`。

如果只有前两条(协议兼容但鉴权不同,例如用 `x-api-key` 头),照样能复用——只要改 base_url,key 还是走同一个 header,大多数情况下能跑通,只是偶尔返回 401 时要把 header 名字换掉。

## 临时切换服务商(不改代码)

```bash
# 切到任意 NewAPI 兼容中转站(以 one-api 自建为例)
export IMAGE_GEN_BASE_URL="https://your-oneapi.example.com/v1"
export IMAGE_GEN_API_KEY="sk-your-key"
python3 submit.py --prompt "..." --model doubao-seedream-4-0-250828
```

provider 名仍写 `geeknow`,只是 base_url 和 key 临时指向别处。这个 trick 在跑 Geeknow 临时不可用,或想用同一 key 试多家时很有用。

## 长期配置:写进 config.json

```json
{
  "providers": {
    "geeknow": {
      "api_key": "sk-xxxxxx",
      "base_url": "https://www.geeknow.top/v1"
    },
    "my_custom_proxy": {
      "api_key": "sk-yyyyy",
      "base_url": "https://my-proxy.example.com/v1"
    }
  }
}
```

存到 `~/.claude/skills/image-gen/config.json`,权限建议 `chmod 600`。然后:

```bash
python3 submit.py --provider my_custom_proxy --prompt "..."
```

前提:`my_custom_proxy` 已经在 `providers/` 里实现了对应的 adapter。如果只是协议兼容,**不需要写 adapter**,只要在 `load_provider()` 里加一个分支:

```python
# _common.py 的 load_provider()
if name == "my_custom_proxy":
    from providers.geeknow import GeeknowProvider  # 直接复用
    return GeeknowProvider(
        api_key=resolve_api_key(name, api_key) or "",
        base_url=resolve_base_url(name, base_url),
    )
```

## 协议不兼容时:写新 adapter

少数服务商的请求/响应结构跟 OpenAI 不一样(例如 Gemini native、Doubao native、Claude native)。这时需要新写 adapter:

1. 在 `scripts/providers/` 下加一个文件,例如 `my_provider.py`
2. 继承 `ImageProvider`,实现三个方法:`submit_sync` / `submit_async` / `poll_async`
3. 在 `_common.py` 的 `load_provider()` 里加分支
4. 在 SKILL.md 的"已内置"表格里登记

`providers/base.py` 里有几个 helper(`extract_items` / `normalize_status` / `_first`)能省事。

## 安全注意

- API key 一律不进 git
- 配置文件的权限建议 600
- 如果用户刚把 key 直接贴在对话里,提醒 rotate 一次,因为 LLM 上下文可能被记录
- `chmod 600 ~/.claude/skills/image-gen/config.json` 后,其它用户就读不到

## 性能调优

`IMAGE_GEN_*` 环境变量可调:

| 变量 | 默认 | 含义 |
|---|---|---|
| `IMAGE_GEN_CONNECT_TIMEOUT` | 10 | TCP 连接超时(秒) |
| `IMAGE_GEN_READ_TIMEOUT` | 60 | 响应读取超时(秒) |
| `IMAGE_GEN_MAX_RETRIES` | 3 | 5xx / 网络错误重试次数 |
| `IMAGE_GEN_POOL_SIZE` | 16 | 连接池大小(并发请求多就调大) |

`batch.py` 的 `--parallel` 决定 ThreadPoolExecutor 大小,不是连接池大小,两者独立可调。