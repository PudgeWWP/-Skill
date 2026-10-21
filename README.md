# -Skill

专为游戏服务的 Skill。

## 玩法立项 / game-project-planning

把一个游戏想法逐步整理成可审阅、可沟通的立项方案。适合独立开发者、游戏策划和前期项目讨论，也支持继续完善已有立项。默认中文交流与交付，可按用户要求切换语言。

### 能做什么

- **理清玩法**：确认游戏类型、核心操作、玩法循环、阶段节奏，以及混合玩法之间的进入、退出和资源传递。
- **研究参考产品**：实际联网查证参考游戏，明确整体参考或局部借鉴，区分调研事实、分析判断和待确认设计。
- **确定产品方向**：逐步确认目标用户、题材背景和美术风格，支持多选、自由补充、参考图和脑暴。
- **可选效果图**：生成主要玩法 1、主要玩法 2 和养成界面三张独立模拟实机图；这些是设计效果图，不代表游戏已开发完成。
- **输出 Word 立项案**：方案确认后生成排版美化的 `.docx`，涵盖核心玩法、立项逻辑、市场分析、参考拆解、差异化、落地结合与风险，并逐页检查。

每轮聚焦一至两个关键问题；已有答案直接承接，建议需经用户确认后才成为设计决定。具体配方、完整数值和技能树等留给后续详细设计。

### 一句话安装

将下面这一句话直接发给 **Codex**（这是对话指令，不是终端命令）：

```text
请使用 $skill-installer 安装 https://github.com/PudgeWWP/-Skill/tree/main/skills/game-project-planning 这个 Skill。
```

安装后可在下一轮对话中使用；如果没有出现，重启 Codex。已有同名 Skill 时，请先让 Codex 检查现有版本并由你决定是否替换。安装方式参考 [OpenAI 官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use)。

### 如何使用

安装后，发送例如：

```text
使用 $game-project-planning 帮我做一个游戏立项。我想做一款融合模拟经营和探索刷宝的游戏，请从玩法循环开始逐步讨论。
```

也可以说“帮我做游戏立项”或“继续完善这个游戏立项”，并提供已有想法、参考游戏或美术参考图。暂时没有方向时，可以选择“帮我脑暴”。

### 使用环境

- **Codex + Skill Installer**：用于安装和调用此 Skill；仓库中包含完整指令、参考规范和字体辅助脚本。
- **联网能力**：用于参考产品与市场调研。
- **documents 文档能力**：生成及渲染检查 Word 交付物时需要；字体辅助脚本使用 Python 和 `lxml`。
- **imagegen 图像能力（可选）**：需要模拟实机效果图时使用；可跳过生图。指定图像模型是否可用取决于实际环境。

本仓库不会自动安装上述配套能力，不能保证任意环境都能生成图片或 Word。

### 仓库结构

```text
skills/game-project-planning/
├── SKILL.md                       # 入口与立项流程
├── agents/openai.yaml             # 展示信息与自动调用策略
├── references/
│   ├── interview.md               # 逐步访谈与脑暴
│   ├── visuals.md                 # 三张模拟实机图规范
│   └── document.md                # 立项案内容与排版规范
└── scripts/normalize_docx_fonts.py # Word 字体一致性辅助工具
```

[查看完整 Skill](skills/game-project-planning/SKILL.md)
