# Manim，让数学看得见 · 配套代码仓库

> Teach Math with Manim — 图书《Manim，让数学看得见》官方配套开源仓库

本仓库是图书《Manim，让数学看得见：AI 时代的教学动画设计与实战》的配套资源，包含书中全部 **60+ 教学动画案例的完整源码**、**自研 Manim 教学动画 AI Skill**，以及可直接复用的模板与工具脚本。全部内容以 MIT 协议开源，欢迎教师、学生和科普创作者自由取用。

## 这本书讲什么

Manim 是 3Blue1Brown 使用的数学动画引擎。本书是国内首部系统讲解 Manim（社区版 ManimCE）的实战图书，以"工具 + 教学法 + AI 工作流"为主线：

- **入门与进阶**：核心概念、公式渲染、镜头语言、3D 场景；
- **数学篇**：函数图像、平面几何、三角函数、数列与解析几何、立体几何、概率统计——每个案例贯通初中、高中到大学衔接学段，对标课标知识点；
- **数学之美·拓展篇**：复数与欧拉公式、微积分直观、不等式与最值、数学归纳法与证明之美——站在中学终点向高等数学门口的远眺；
- **AI 实战篇**："AI 生成 + 人工精修"的微课生产线，以及本仓库内置的教学动画 AI Skill。

## 快速开始

```bash
# 1. 克隆本仓库
git clone https://github.com/Scorpio69t/teach-math-with-manim.git
cd teach-math-with-manim

# 2. 安装依赖（需要 Python 3.11+，锁定 ManimCE 0.21）
pip install -r requirements.txt

# 3. 渲染第一个案例（冒泡排序——番外示例，免 LaTeX，低画质快速预览）
#    注：算法内容已不属本书正篇，将单独成书；此案例保留为入门练手与 Skill 演示用
manim -pql examples/bonus_sorting/bubble_sort.py BubbleSortScene
```

渲染参数速查：`-pql` 快速预览 / `-pqm` 中等画质 / `-pqh` 高清出片 / `-pqk` 4K。
环境提示：全仓 65 个案例中 38 个免 LaTeX 即可渲染，其余 27 个含 `MathTex` 公式的案例需安装 TeX 发行版（TeX Live / MiKTeX / MacTeX），详见 [examples/README.md](examples/README.md)。

## 仓库结构

```
teach-math-with-manim/
├── examples/          # 书中各章案例源码（65 个文件，按章节组织，均可直接渲染）
│   ├── ch09_functions/
│   ├── bonus_sorting/
│   └── ...
├── skill/             # 自研 Manim 教学动画 AI Skill（含 6 个教学模板、校验脚本、dsh 插件与安装脚本）
├── templates/         # 教学设计模板（微课分镜表等）
├── tools/             # 辅助工具说明（渲染校验与抽帧脚本位于 skill/manim-teaching/scripts/）
├── videos/            # 精选成片预览
├── requirements.txt   # Python 依赖与 ManimCE 0.21 版本范围
└── README.md
```

## AI Skill：一句话生成教学动画

`skill/` 目录是本书第 19 章完整讲解的开源 Skill。安装到支持的 AI 编程助手后，用一句自然语言即可生成规范、可渲染的 Manim 教学动画脚本：

> "帮我做一个冒泡排序的教学动画，比较时金色高亮，交换时红色，已就位的元素变绿。"
>
> （番外示例：排序动画是检验颜色语义与节奏控制的最佳试金石，故保留为 Skill 演示案例。）

Skill 内置版本锁定（ManimCE 0.21 白名单）、64 条避坑档案、教学风格规范（颜色语义 / 五件套版式 / 节奏纪律）、数学严谨性军规、交付前验收清单，以及六个经真实渲染验证的教学模板。

三种安装方式（详见 [skill/README.md](skill/README.md)）：

```bash
# ① DeepSeek Harness 插件（本仓库即 dsh 插件包）
dsh plugin --profile web add github:Scorpio69t/teach-math-with-manim

# ② 一键脚本：自动探测本机已装的 10 种 AI Agent 并安装
bash skill/install.sh            # macOS / Linux / Git Bash
powershell -ExecutionPolicy Bypass -File skill\install.ps1   # Windows

# ③ 纯对话工具：直接粘贴 skill/dist/manim-teaching-prompt.md 单文件版
```

## 许可与引用

- 本仓库全部代码与文档以 [MIT 协议](LICENSE) 开源，可自由用于课堂、课程与二次创作；
- 书中案例对应的渲染视频将陆续发布在作者的自媒体账号（链接待补充）；
- 如果本仓库对你的教学有帮助，欢迎 Star，也欢迎在课堂中使用后反馈建议（Issues）。

## 关于作者

资深全栈工程师，软考高级系统架构设计师，专注 AI 应用与数学可视化创作，运营数学可视化科普自媒体。

---

*This repository contains all source code, templates and an open-source AI Skill for the book "Teach Math with Manim". All examples are written for Manim Community Edition (ManimCE) and released under the MIT License.*
