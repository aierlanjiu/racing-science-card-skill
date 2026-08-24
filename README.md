# Racing Science Card · 赛车科普卡片生成技能

将赛车工程、赛事历史或人物故事转化成三套差异化竖版科普卡片提示词。默认不绑定图片模型，不读取任何账号凭据。

## 三种风格预览

| 工业蓝图 | 赛道纪实 | 极净实验室 |
|---------|---------|-----------|
| 深蓝晒图纸 + 白墨工程手写 | 米黄便签 + 马克笔 + 钨丝暖光 | 纯白无菌 + 激光蚀刻 + 亚克力展柜 |
| 适合技术/机械/原理 | 适合赛事/人物/故事 | 适合科技/材料/未来 |

## 快速开始

### 1. 安装到 Codex

```bash
# 克隆仓库
git clone https://github.com/aierlanjiu/racing-science-card-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R racing-science-card-skill "${CODEX_HOME:-$HOME/.codex}/skills/racing-science-card"

# 或直接复制
cp -r racing-science-card-skill ~/.codex/skills/racing-science-card
```

### 2. 使用

直接说出技能名和目标：
```
使用 racing-science-card，把“尾流分离点”做成 3:4 工业蓝图科普卡。不要写未经核对的风阻数值。
```

### 3. 手动生成提示词

```bash
# 查看三套元提示词模板
cat ~/.codex/skills/racing-science-card/references/meta-prompts.md

# 查看完整赛事示例
cat ~/.codex/skills/racing-science-card/references/racing-examples.md
```

## 离线批量整理

准备一个 JSON 对象，键为文件名，值为完整提示词：

```json
{
  "wake-separation": "完整提示词文本",
  "brake-fade": "完整提示词文本"
}
```

运行：

```bash
python3 scripts/gen_cards.py prompts.json output-prompts
```

脚本会输出独立 `.txt` 文件和 `manifest.json`。它不会联网、不会直接出图，也不会读取 Keychain、Cookie、API Key、OAuth token 或浏览器 profile。

## Agent 配置

可在项目 `AGENTS.md` 中加入：

```md
## Skill routing

- 赛车工程、赛事历史或赛车人物科普使用 `racing-science-card`。
- 默认只输出提示词。只有当前环境明确提供图像生成工具时才渲染。
- 具体标准号、参数和历史结论必须先核对可靠来源。
```

## 事实边界

`references/racing-examples.md` 保存的是历史生成案例，其中的速度、马力、公式结果和标准号没有完整来源登记。它们只能用来理解提示词结构，不能直接当作实测或官方材料复用。

## 文件结构

```
racing-science-card-skill/
├── SKILL.md                    # Codex Skill 入口
├── README.md                   # 本文件
├── LICENSE                     # MIT 代码与文档许可
├── SECURITY.md                # 凭据与渲染器安全边界
├── references/
│   ├── meta-prompts.md         # 3 套风格元提示词（含占位变量）
│   └── racing-examples.md      # 3 场赛车史赛事完整提示词示例
└── scripts/
    └── gen_cards.py            # 离线提示词导出脚本
```

## 会员案例边界

配套会员案例包含三张历史生成卡片：

- `lemans_1966.png`：工业蓝图风格，1966 勒芒主题
- `fuji_1976.png`：赛道纪实风格，1976 富士主题
- `sanremo_1985.png`：极净实验室风格，1985 圣雷莫主题

这些成图不随本仓库分发。仓库提供提示词结构，图片中的历史与工程结论仍需二次核对。

## 依赖

- Codex Skill：无额外 Python 依赖
- 离线整理脚本：Python 3.10 或更新版本，仅使用标准库

## License

代码和文档使用 MIT License。赛事名称、车手、车型和品牌标识仍归各自权利人所有。

## 致谢

- 雪沐江南视觉实验室（Xuemu Lab）：视觉系统与教程整理
