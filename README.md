# Racing Science Card · 赛车科普卡片生成技能

将赛车主题转化为三种差异化视觉风格的科普卡片，通过 Codex `gpt-image-2` 批量出图。

## 三种风格预览

| 工业蓝图 | 赛道纪实 | 极净实验室 |
|---------|---------|-----------|
| 深蓝晒图纸 + 白墨工程手写 | 米黄便签 + 马克笔 + 钨丝暖光 | 纯白无菌 + 激光蚀刻 + 亚克力展柜 |
| 适合技术/机械/原理 | 适合赛事/人物/故事 | 适合科技/材料/未来 |

## 快速开始

### 1. 安装到 Claude Code

```bash
# 克隆仓库
git clone https://github.com/your-org/racing-science-card-skill.git ~/.codex/skills/racing-science-card

# 或直接复制
cp -r racing-science-card-skill ~/.codex/skills/racing-science-card
```

### 2. 使用

在 Claude Code 中输入触发词即可：
```
赛车科普卡：涡轮增压原理
racing card: 1985 San Remo Rally
```

### 3. 手动生成提示词

```bash
# 查看三套元提示词模板
cat ~/.codex/skills/racing-science-card/references/meta-prompts.md

# 查看完整赛事示例
cat ~/.codex/skills/racing-science-card/references/racing-examples.md
```

## Codex 认证获取

本技能使用 Codex OAuth 机制调用 `gpt-image-2` 模型，**无需 OpenAI API Key**。

### 前置条件

1. **安装 Hermes Agent**
   ```bash
   git clone https://github.com/your-org/hermes-agent.git ~/.hermes/hermes-agent
   cd ~/.hermes/hermes-agent
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **安装 Codex.app**（macOS）
   - 下载：[codex.app](https://codex.app)
   - 安装 `openai-codex` plugin
   - 登录你的 OpenAI 账号（ChatGPT Plus / Team Plan / Pro Plan）

3. **验证 token 可读**
   ```bash
   python3 -c "
   import sys
   sys.path.insert(0, '$HOME/.hermes/hermes-agent')
   from agent.auxiliary_client import _read_codex_access_token
   token = _read_codex_access_token()
   if token:
       print('Token OK:', token[:20] + '...')
   else:
       print('Token NOT found - check Codex login')
   "
   ```

### 如何获取 Codex OAuth Token（原理说明）

Codex.app 将 OAuth token 存储在 macOS Keychain 中：

```
Keychain: "Codex" / "chatgpt-access-token"
```

Hermes 的 `_read_codex_access_token()` 函数通过 `security` CLI 读取：

```python
import subprocess, json

def _read_codex_access_token():
    result = subprocess.run(
        ['security', 'find-generic-password',
         '-s', 'Codex',
         '-a', 'chatgpt-access-token',
         '-w'],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None
```

### Token 生命周期

- **有效期**：1 小时（OAuth access token）
- **刷新**：Codex.app 在后台自动续期，Hermes 每次调用时从 Keychain 读取最新值
- **日配额**：Team Plan 约 50-100 张/天，Pro Plan 约 200 张/天
- **429 限流**：遇到 `usage_limit_reached` 错误时，响应中 `resets_in_seconds` 字段告知重置倒计时

## 支持的平台

### Codex.app（macOS，推荐）
通过 Hermes agent 的 OAuth 机制免 Key 调用，内部走 ChatGPT 后端 `gpt-image-2` 管线。

### ChatGPT 网页端（任何平台）
将本技能生成的提示词直接粘贴到 [chatgpt.com](https://chatgpt.com) 的输入框。ChatGPT Plus/Pro 订阅用户可直接生成图片。

**操作步骤**：
1. 打开 `references/meta-prompts.md` 复制对应风格的提示词
2. 替换 `{卡片标题}` 等占位变量
3. 粘贴到 ChatGPT 输入框并发送
4. ChatGPT 会自动调用 `gpt-image-2` 生成图片

### OpenAI API（开发者）
```python
import openai

client = openai.OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    tools=[{"type": "image_generation", "model": "gpt-image-2", "size": "1024x1536"}]
)
```

### Claude Code（通过此 Skill）
安装后自动注册为 Claude Code skill，`/racing-science-card` 或触发词调用。

## 配额与成本

| 方案 | 日配额（估算）| 适合场景 |
|------|-------------|---------|
| ChatGPT Plus | ~20 张/天 | 个人偶尔使用 |
| ChatGPT Pro | ~200 张/天 | 内容创作者日常使用 |
| Team Plan | ~50-100 张/天 | 团队协作 |

## 文件结构

```
racing-science-card-skill/
├── SKILL.md                    # Skill 定义（Claude Code 加载入口）
├── README.md                   # 本文件
├── references/
│   ├── meta-prompts.md         # 3 套风格元提示词（含占位变量）
│   └── racing-examples.md      # 3 场赛车史赛事完整提示词示例
├── scripts/
│   └── gen_cards.py            # Codex 批量出图脚本（需 Hermes 环境）
└── assets/
    └── (示例输出图)
```

## 示例输出

三张赛车史赛事卡片（1024×1536 PNG）：

- `lemans_1966.png` — 工业蓝图风格 · 1966 勒芒 GT40 复仇工程
- `fuji_1976.png` — 赛道纪实风格 · 1976 富士 Hunt vs Lauda 雨战
- `sanremo_1985.png` — 极净实验室风格 · 1985 圣雷莫 Delta S4 双增压

## 依赖

- **Codex 图像生成**：Hermes Agent + Codex.app + OpenAI 订阅
- **Python**：≥ 3.10 + `openai` SDK
- **Claude Code 集成**：本 Skill 的 SKILL.md + references

## License

MIT

## 致谢

- 雪沐江南视觉实验室（Xuemu Lab）— 视觉风格 DNA 来源
- Hermes Agent — Codex OAuth 集成
- OpenAI — gpt-image-2 模型
