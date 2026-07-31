# zk-skills

ZK 个人维护的 Claude Code / OpenClaw skill 集合。

按 Claude Code 标准组织：每个 skill 是仓库根下 `skills/<skill-name>/` 下的独立目录，含 `SKILL.md` 入口与 `references/` 等引用文件。

## 已收录的 skills

| Skill | 描述 | 来源 |
|---|---|---|
| [elegant-ancient-narrative-style](./skills/elegant-ancient-narrative-style) | 古雅叙事风格引擎：将现代文本转化为具有古雅气韵的现代表达，强调东方含蓄叙事而非古词替换 | 原创 |
| [super-creazy-html-ppt-in-work](./skills/super-creazy-html-ppt-in-work) | 高端 HTML 幻灯片生成器：智能主题匹配、SVG 图标系统、玻璃态/新拟态/极简多风格、8 种布局 × 12 主题 × 30 动画、16:9 演示优化 | upstream |
| [manga-studio](./skills/manga-studio) | AI 漫画工作流：从剧情/角色素材出发,自动产出世界观、角色参考表、分镜脚本、布局草图、成稿画面。覆盖单页与多页连续剧情,8 种画风预设。与 image-gen 配合使用。 | 原创(参考 morsoli/aimangastudio) |

## 安装

### Claude Code

```bash
git clone https://github.com/zuoanCo/zk-skills ~/.claude/skills/zk-skills
# 或单独软链一个
ln -s "$(pwd)/skills/super-creazy-html-ppt-in-work" ~/.claude/skills/super-creazy-html-ppt-in-work
```

### OpenClaw

```bash
cp -r skills/super-creazy-html-ppt-in-work ~/.openclaw/workspace/skills/
```

## 维护约定

- 新增 skill：放在 `skills/<skill-name>/`，自包含
- 引用文件统一放 `references/`
- frontmatter 至少含 `name` + `description`
- 大文件不进入 git
