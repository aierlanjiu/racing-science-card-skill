---
name: racing-science-card
description: 赛车科普卡片生成技能。输入赛车主题/赛事/技术概念，输出三种不同视觉风格（工业蓝图/赛道纪实/极净实验室）的Codex提示词并批量出图。触发词：赛车科普卡、赛车卡片、racing card、赛事科普、F1科普卡、拉力赛科普、勒芒科普。
---

# Racing Science Card · 赛车科普卡片生成

## 这个 Skill 做什么

将赛车主题（赛事、技术、人物）转化为三套差异化视觉风格的科普卡片提示词，并通过 Codex OAuth 批量生成 PNG 图像。

**三套视觉风格：**

| # | 风格 | 气质 | 适合主题 |
|---|------|------|---------|
| A | 工业蓝图 | 深蓝晒图纸 + 白墨工程手写体 + 透写台冷光 | 技术原理、工程解析、机械构造 |
| B | 赛道纪实 | 米黄便签纸 + 马克笔手写 + 钨丝灯暖光 | 赛事故事、人物叙事、历史时刻 |
| C | 极净实验室 | 纯白无菌空间 + 激光蚀刻 + 亚克力展柜 | 尖端科技、材料科学、未来概念 |

**双输出**：Codex 提示词（文本）+ PNG 图像（1024×1536 竖版）

## 何时使用 vs 不何时使用

**适合**：赛车科普内容创作 / 公众号配图 / 社交媒体赛车知识卡片 / 赛事回顾可视化 / 工程教育素材

**不适合**：实时赛事报道（需要新闻图片）/ 纯数据图表 / 非赛车主题

## 工作流

### Step 1 · 主题输入
用户提供赛车主题（赛事名、技术术语、车型、人物等），可附带关键参数。

### Step 2 · 风格匹配
根据主题性质推荐最佳风格：
- 技术/机械/原理 → 工业蓝图 (A)
- 赛事/人物/故事 → 赛道纪实 (B)
- 科技/材料/未来 → 极净实验室 (C)

### Step 3 · 提示词推理
基于所选风格，按元提示词模板填充：
- 卡片标题（中+英）
- 视觉锚点（核心3D零件）
- 4个核心机制
- 工程公式+标准
- 4段深度解说
- 验证图表

详见 `references/meta-prompts.md`。

### Step 4 · 图像生成
将提示词输入 Codex（gpt-image-2）生成 1024×1536 PNG。生成脚本见 `scripts/gen_cards.py`。

**Codex OAuth 认证配置**见下方「Codex 认证获取」章节。

### Step 5 · 验收
- 文件 > 10KB
- 中文文字清晰可读
- 无畸变/乱码/幽灵字

## Codex 认证获取

Codex 图像生成使用 OpenAI ChatGPT 后端的 `gpt-image-2` 模型，通过 Codex OAuth token 免 API Key 调用。

### 获取 Codex Access Token（macOS）

```bash
# Codex 将 token 存储在 Keychain 中，Hermes 的辅助函数可读取：
python3 -c "
import sys
sys.path.insert(0, '/path/to/hermes-agent')
from agent.auxiliary_client import _read_codex_access_token
print(_read_codex_access_token()[:20] + '...')
"
```

**前置条件**：
1. 安装 [Hermes Agent](https://github.com/user/hermes-agent)
2. 在 Codex.app 中登录你的 OpenAI 账号（Team Plan 或 Pro Plan）
3. Codex 安装 `openai-codex` plugin

### Token 有效期
- Codex OAuth token 有效期通常为 1 小时
- 过期后 Hermes 会自动从 Keychain 刷新
- Team Plan 有日配额限制（约 50-100 张/天）

### 支持的平台（均可使用本 Skill 的提示词）

| 平台 | 方式 | 说明 |
|------|------|------|
| **Codex.app** (macOS) | OAuth 自动 | 通过 Hermes agent 的 `_read_codex_access_token()` 免 Key 调用 |
| **ChatGPT Plus/Pro** | 网页端粘贴提示词 | 在 chatgpt.com 输入框直接提交，DALL·E/gpt-image 渲染 |
| **OpenAI API** | API Key | 使用 `openai` Python SDK，model=`gpt-image-2` |
| **Claude Code** | 通过此 Skill | 安装后 `/racing-science-card` 调用 |

## 三种风格元提示词

完整模板和示例见 `references/meta-prompts.md`。

## 资源文件

```
racing-science-card-skill/
├── SKILL.md                    ← 你正在读
├── README.md                   ← GitHub README + 认证说明
├── references/
│   ├── meta-prompts.md         ← 3 套风格元提示词模板
│   └── racing-examples.md      ← 3 场赛车史赛事完整示例
├── scripts/
│   └── gen_cards.py            ← Codex 批量出图脚本
└── assets/
    └── (placeholder)
```
