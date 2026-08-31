# skill/ — manim-teaching：Manim 教学动画 AI Skill

本书第 19 章完整讲解的自研开源 Skill。安装到支持的 AI 编程助手后，用一句自然语言即可生成**规范、可渲染、有教学设计**的 Manim 教学动画脚本。

> "帮我做一个二次函数顶点式的教学动画：描点时金色高亮，配方过程逐步变换，结论用绿色定格。"
> —— 装好 Skill 后，这句话就是全部输入。

## 这个 Skill 强在哪里

- **版本锁定（rules/version-lock.md）**：只生成 ManimCE 0.21 的 API 白名单代码，附 GL 版禁用对照表，从源头杜绝 GL/CE 混用和幻觉 API；
- **避坑档案（rules/pitfalls.md）**：28+ 条真实渲染事故记录（已废弃接口、参数顺序、字体缺字形、文字重叠等），每条含错误现象与修法；
- **教学风格（rules/teaching-style.md）**：颜色语义系统（金=当前关注、红=变化与矛盾、绿=结论成立、青=假设链条）、五件套版式、节奏纪律、三平台字体方案；
- **数学严谨（rules/math-accuracy.md）**：六条军规——公式真算、点位可复现、派生点公式化、读数同源、递推驻留、颜色绑角色；
- **可运行模板（templates/）**：五个覆盖高频场景的教学场景骨架（函数图像、几何证明、数轴、网格计数、通用五段式），全部经过真实渲染验证；
- **验证脚本（scripts/）**：`render_check.py` 跨平台一键验证脚本可渲染，`extract_frames.py` 抽帧自查画面。

## 目录结构

```
skill/
├── manim-teaching/        # Skill 本体（安装的就是这个目录）
│   ├── SKILL.md           # 入口：触发词、三条铁律、五步工作流、版本速查
│   ├── rules/             # 四条规则库：版本锁定 / 避坑档案 / 教学风格 / 数学严谨
│   ├── templates/         # 五个可渲染教学模板
│   └── scripts/           # render_check.py / extract_frames.py
├── dsh-plugin/            # DeepSeek Harness 插件入口（index.js）
├── install.sh             # Unix 一键安装脚本（自动探测 10 种 Agent 目录）
├── install.ps1            # Windows 一键安装脚本
├── build_dist.py          # 生成单文件粘贴版
└── dist/
    └── manim-teaching-prompt.md   # 纯对话工具用的合并版提示词
```

## 三种安装方式

### ① DeepSeek Harness（dsh）插件——一行安装

本仓库本身就是一个 dsh 插件包（`package.json` + `cordis.patch.yml`）：

```bash
dsh plugin --profile web add github:Scorpio69t/teach-math-with-manim
```

插件启动时自动解析 `manim-teaching/SKILL.md` 并注册进 dsh 的技能系统，规则与模板通过 `resourceBase` 挂载。重启 dsh 后，在 web UI 中模型即可自动触发本技能。

> dsh 安装：`npm install -g @deepseek-ai/dsh`（需要 Node.js 18+ 与 `DEEPSEEK_API_KEY`）。dsh 目前处于开发者预览阶段，命令行细节以其官方文档为准。

### ② 安装脚本——装进本机已有的 AI Agent

脚本会自动探测本机已安装的 Agent（Claude Code、DeepSeek Harness 共享目录、Kimi Code、Codex CLI、GitHub Copilot CLI、Gemini CLI、Trae、CodeBuddy、文心快码、通义灵码等 10 种），把技能目录复制进去：

```bash
# macOS / Linux / Git Bash
bash skill/install.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File skill\install.ps1

# 手动指定目录（两种脚本都支持）
bash skill/install.sh ~/.myagent/skills
```

装完重启对应工具即生效。

### ③ 单文件粘贴——任何纯对话工具

`dist/manim-teaching-prompt.md` 是把 SKILL.md 正文与四份规则库合并后的单文件版本，直接粘贴到 ChatGPT、DeepSeek 网页版、Kimi 等任何对话窗口的系统提示词或首条消息里即可使用（模板与脚本请从本仓库单独下载）。

该文件由 `build_dist.py` 生成，修改规则库后重跑一次即可同步。

## 给 Skill 的提问技巧

- 说清楚**知识点 + 学段**，Skill 会按教学节奏组织画面；
- 指定**颜色语义**（"错误操作红色、正确结论绿色"），动画会更有教学表达力；
- 生成后让 AI 用 `scripts/render_check.py` 自验渲染，不通过就自动修——这是 Skill 工作流的最后一步。

---

*Skill 的设计思路、每条规则的由来与实战翻车实录，见本书第 19 章。*
