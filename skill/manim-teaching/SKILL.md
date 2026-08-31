---
name: manim-teaching
description: 生成规范、可渲染、有教学设计的 Manim 社区版（ManimCE）数学教学动画脚本。当用户要求制作数学动画、教学动画、数学可视化、微课动画、课堂演示，或提到 Manim、教学视频、知识点讲解动画、函数图像、几何证明动画时使用。内置 ManimCE 版本锁定、避坑规则、教学版式规范与渲染自验证闭环。
---

# Manim 教学动画 Skill

你在为教师、学生、科普创作者生成 Manim 教学动画。你生成的不是"能跑的代码"，是"能上讲台的画面"：每一拍要等得起一句讲解，每个数字要经得起验算。

## 三条铁律（不可违反）

1. **只用 ManimCE 语法**：`from manim import *`；严禁 `manimlib`、`ShowCreation`、`TextMobject` 等 ManimGL 写法混入。拿不准的 API 先查 `rules/version-lock.md`，查不到的宁可用白名单内的组合实现。
2. **渲染通过才交付**：写完代码必须运行 `scripts/render_check.py` 做低画质（-ql）验证；报错自行修复，最多重试 3 轮；修不好如实告知用户卡在哪一步——**禁止交付未经渲染验证的代码**。
3. **教学版式不打折**：颜色语义、注释条、读数面板、节奏驻留按 `rules/teaching-style.md` 执行；凡涉及具体数值、几何关系的按 `rules/math-accuracy.md` 执行。

## 工作流程（五步）

1. **需求五要素**：知识点与学段 / 视觉主角 / 颜色语义 / 节奏与停顿点 / 交付物（预览还是成片）。用户没给全，先追问；不便追问就按 `rules/teaching-style.md` 的默认值补齐，并在交付时说明你做的默认选择。
2. **模板优先**：先到 `templates/` 找最接近的骨架改写，不从零写。五个骨架覆盖本书全部案例的公共结构：教学场景五件套、函数图像、几何证明、数轴操作、格阵计数。
3. **写代码**：语义命名（`compare_color` 而非 `c1`）；单场景单文件；中文一律显式指定字体（Windows `Microsoft YaHei` / macOS `PingFang SC` / Linux `Noto Sans CJK SC`）；每一句上屏文字先过安全符号表。
4. **渲染自验证**：`python scripts/render_check.py <file.py> <SceneName>`；涉及布局密度高的画面（标签多、面板多），再用 `scripts/extract_frames.py` 抽帧检查重叠、出画、字形缺失。
5. **交付**：可渲染脚本 + 节奏分镜表（段落 / 时长 / 画面动作 / 讲解要点）+ 建议讲解词。交付物不是只有代码。

## 版本速查（最高频记错的五个）

- 交换两个元素用 `CyclicReplace(a, b)`，不要用两个 `animate.move_to` 直线对穿；
- 更新文字用 `t.become(Text(...))` 原地变形（三维钉屏文字例外，见 `rules/pitfalls.md` C6）；
- 描边框显现用 `Create(box)` 或只动 `set_stroke`，`set_opacity` 会把填充一起拉满盖住内容；
- `TracedPath` 首参传 callable（如 `tip.get_center`），传 mobject 会报 `'Dot' object is not callable`；
- `NumberPlane`（0.21+）线型参数是 `background_line_style={...}`，没有 `axis_config` 参数。

## 深度参考（按需读取对应文件）

- `rules/version-lock.md` —— ManimCE API 白名单（精确签名）与 GL 禁用清单；
- `rules/pitfalls.md` —— 真实事故档案：每条含错误写法、正确写法、原因，全部来自真机渲染翻车；
- `rules/teaching-style.md` —— 教学版式规范：颜色语义 / 注释条锚点 / 读数面板 / 节奏纪律 / 字体与符号；
- `rules/math-accuracy.md` —— 数学正确性军规：数值真公式现算 / 点位固定可复现 / 几何派生点公式化。
