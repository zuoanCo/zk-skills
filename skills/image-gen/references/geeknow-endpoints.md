# Geeknow AI 接口 cheat sheet

来源:[docs.geeknow.top](https://docs.geeknow.top/)。完整文档以官网为准,这里只摘 image-gen skill 实际用到的部分。

## Base URL

```
https://www.geeknow.top/v1
```

## 鉴权

```http
Authorization: Bearer <api_key>
Content-Type: application/json
```

## 1. 同步生图

```http
POST /images/generations
```

请求体:

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | ✓ | 模型名,如 `gpt-image-2`、`gpt-image-2-pro`、`gpt-image-2-vip` |
| `prompt` | string | ✓ | 提示词,1–4000 字符 |
| `n` | int |  | 生成数量,默认 1,范围 1–10 |
| `size` | string |  | 输出尺寸,见下表 |
| `response_format` | string |  | `url` 或 `b64_json`,默认 `url` |
| `quality` | string |  | `auto` / `low` / `medium` / `high`,是否生效取决于渠道 |
| `image` | string \| array |  | 参考图(base64 字符串 / 字符串数组),同步模式支持 |
| `style` / `background` / `watermark` |  |  | 透传给支持的上游 |

尺寸预设:

| 预设 | 实际尺寸 |
|---|---|
| `1:1` | `1024x1024` |
| `4:3` | `1536x1152` |
| `3:2` | `1536x1024` |
| `2:3` | `1024x1536` |
| `16:9` | `1920x1080` |
| `9:16` | `1080x1920` |

响应:

```json
{
  "created": 1735689600,
  "data": [
    {"url": "https://...", "revised_prompt": "..."}
  ]
}
```

或 `b64_json` 形式。

## 2. 异步提交

```http
POST /images/generations/async
```

请求体跟同步一样,**但 `image` 字段必须是公网 http(s) URL**,不支持 base64 / `data:` URI。

提交响应:

```json
{
  "id": "task_img_abc123",
  "task_id": "task_img_abc123"
}
```

读取 `id` / `task_id` / `taskId` 任意一个作为后续查询 ID。

## 3. 异步查询

```http
GET /images/generations/async/{task_id}
```

处理中:

```json
{
  "id": "task_img_abc123",
  "task_id": "task_img_abc123",
  "object": "image.generation.task",
  "model": "gpt-image-2-vip",
  "status": "in_progress",
  "progress": "10%",
  "created_at": 1735689600
}
```

完成:

```json
{
  "data": [
    {"url": "https://geekm.oss-cn-shanghai.aliyuncs.com/image-gen-xxx.png"}
  ],
  "size": "1024x1024",
  "usage": {
    "input_tokens": 15,
    "total_tokens": 211,
    "output_tokens": 196
  }
}
```

失败:

```json
{
  "status": "failed",
  "error": {
    "code": "rate_limit_exceeded",
    "message": "..."
  }
}
```

## 已验证可异步的模型

- `gpt-image-2`
- `gpt-image-2-pro`(高分辨率,如 3840x2160)
- `gpt-image-2-vip`(超宽画幅,如 3808x1632)
- Doubao Seedream 系列(`doubao-seedream-4-0-250828` 等)
- Gemini 图像系列(`gemini-3-pro-image-preview`、`gemini-2.5-flash-image-preview`、`gemini-3.1-flash-image-preview`、`gemini-3.1-flash-lite-image`)

## Midjourney 单独走另一套

Midjourney 提交/查询不在 `/v1/images/generations/*` 这套路径下,需要单独的 `/mj/*` 接口和适配器。当前 skill 不内置 MJ,如需支持,在 `providers/` 下加一个 `midjourney.py`。

## 图像编辑(edit)

```http
POST /images/edits
```

参考图走 multipart/form-data 或 base64。本 skill 当前不内置 edit 工作流——如果你主要用 edit,告诉我加一个 `edit.py`。

## 上传本地图片(用于参考图)

```http
POST /api/upload/presign
```

返回对象存储预签名地址,客户端 PUT 上传后拿 `public_url`,再传给接受 URL 的接口。本 skill 不内置,需要时再补。