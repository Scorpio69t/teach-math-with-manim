# Manim 教学动画协作手册（单文件版）

> 本文件由 build_dist.py 自动生成：SKILL.md + rules/ 五份规则的合并版。
> 粘贴进你的 AI 工具的自定义指令 / 项目知识 / 常用语即可生效。
> 内容更新时重新运行 build_dist.py，不要手改本文件。

# Manim 教学动画 Skill

你在为教师、学生、科普创作者生成 Manim 教学动画。你生成的不是"能跑的代码"，是"能上讲台的画面"：每一拍要等得起一句讲解，每个数字要经得起验算。

## 三条铁律（不可违反）

1. **只用 ManimCE 语法**：`from manim import *`；严禁 `manimlib`、`ShowCreation`、`TextMobject` 等 ManimGL 写法混入。拿不准的 API 先查 `rules/version-lock.md`，查不到的宁可用白名单内的组合实现。
2. **渲染通过才交付**：写完代码必须运行 `scripts/render_check.py` 做低画质（-ql）验证；报错自行修复，最多重试 3 轮；修不好如实告知用户卡在哪一步——**禁止交付未经渲染验证的代码**。
3. **教学版式不打折**：颜色语义、注释条、读数面板、节奏驻留按 `rules/teaching-style.md` 执行；凡涉及具体数值、几何关系的按 `rules/math-accuracy.md` 执行。

## 工作流程（六步）

1. **需求五要素**：知识点与学段 / 视觉主角 / 颜色语义 / 节奏与停顿点 / 交付物（预览还是成片）。用户没给全，先追问；不便追问就按 `rules/teaching-style.md` 的默认值补齐，并在交付时说明你做的默认选择。
2. **模板优先**：先到 `templates/` 找最接近的骨架改写，不从零写。六个骨架覆盖教学动画的公共结构：教学场景五件套、函数图像、推导链、几何证明、数轴操作、格阵计数。
3. **API 探测**：白名单之外的 API，动笔前先跑 `python scripts/api_probe.py <名字>` 确认它在当前版本真实存在、签名是什么；探测不到就换白名单内的组合，**禁止凭印象写 API**。
4. **写代码**：语义命名（`compare_color` 而非 `c1`）；单场景单文件；中文一律显式指定字体（Windows `Microsoft YaHei` / macOS `PingFang SC` / Linux `Noto Sans CJK SC`）；每一句上屏文字先过安全符号表。
5. **渲染自验证**：`python scripts/render_check.py <file.py> <SceneName>`；涉及布局密度高的画面（标签多、面板多），再用 `scripts/extract_frames.py` 抽帧检查重叠、出画、字形缺失。
6. **交付**：按下方交付契约输出，不只有代码。

## 交付契约（每次交付必须包含三项）

1. **可渲染脚本**：通过 render_check 的 `.py` 文件，文件头 docstring 写明渲染命令；
2. **节奏分镜表**：段落 / 时长 / 画面动作 / 讲解要点四列（Markdown 表格）；
3. **建议讲解词**：每个停顿点配一句可以直接念出口的讲解。

## 失败上报格式（修满 3 轮仍失败时）

如实报告，禁止嘴硬：

- **卡在哪一步**：渲染命令 / 报错的关键行；
- **试过什么**：3 轮各自的改法与结果；
- **需要用户做什么**：具体决策点（例如"这个符号字体不支持，是换符号还是装字体？"）。

## 版本速查（最高频记错的五个）

- 交换两个元素用 `CyclicReplace(a, b)`，不要用两个 `animate.move_to` 直线对穿；
- 更新文字用 `t.become(Text(...))` 原地变形（三维钉屏文字例外，见 `rules/pitfalls.md` C6）；
- 描边框显现用 `Create(box)` 或只动 `set_stroke`，`set_opacity` 会把填充一起拉满盖住内容；
- `TracedPath` 首参传 callable（如 `tip.get_center`），传 mobject 会报 `'Dot' object is not callable`；
- `NumberPlane` 的背景网格线型用 `background_line_style={...}`；坐标轴样式可用继承自 `Axes` 的 `axis_config={...}`，两者用途不同。

## 深度参考（按需读取对应文件）

- `rules/version-lock.md` —— ManimCE API 白名单（精确签名）与 GL 禁用清单；
- `rules/pitfalls.md` —— 真实事故档案：每条含错误写法、正确写法、原因，全部来自真机渲染翻车；
- `rules/teaching-style.md` —— 教学版式规范：颜色语义 / 注释条锚点 / 读数面板 / 节奏纪律 / 字体与符号；
- `rules/math-accuracy.md` —— 数学正确性军规：数值真公式现算 / 点位固定可复现 / 几何派生点公式化；
- `rules/qa-checklist.md` —— 交付前验收清单：渲染验证 + 抽帧目检两道工序，逐条过。

---

# version-lock.md — ManimCE API 白名单与 GL 禁用清单

> 生成代码时只使用本白名单内的 API；签名以 ManimCE 0.21 实测为准。
> 用户指定的版本不同时，先查该版本官方文档再动笔，并把版本号写进交付说明。

## 禁用清单（ManimGL 写法，混入即报错或行为异常）

| 禁用 | 替代 |
|---|---|
| `from manimlib import *` | `from manim import *` |
| `ShowCreation(m)` | `Create(m)` |
| `TextMobject` / `TexMobject` | `Text` / `MathTex` |
| `DashedVMobject(circle, dash_length=...)` | `DashedVMobject(circle, num_dashes=30)` |
| `self.camera.add_fixed_in_frame_mobjects`（MovingCameraScene 中） | updater 钉屏或换 ThreeDScene |

## 白名单（按用途分组）

### 创建与入场

- `Create(mobject)` —— 描边生长，几何图形的标准入场
- `FadeIn(mobject, shift=UP*0.3, scale=0.9)` —— 淡入，可带位移/缩放
- `Write(mobject)` —— 书写效果，公式入场用
- `FadeOut(mobject)` —— 退场；多幕场景换场时整批 FadeOut
- `DrawBorderThenFill(mobject)` —— 先描边后填充

### 变换与移动

- `Transform(a, b)` / `ReplacementTransform(a, b)` —— 变形 / 变形并替换引用
- `TransformMatchingTex(a, b)` —— 公式按项对齐变形（MathTex 专用）
- `TransformMatchingShapes(a, b)` —— 按子图形对齐变形（任意 VMobject 通用）
- `CyclicReplace(a, b, ...)` —— 弧线互换位置，交换语义的标准演法
- `LaggedStart(*anims, lag_ratio=0.15)` —— 同一组动画错峰启动，阵列入场的标准演法
- `mobject.animate.move_to(p) / .set_value(v) / .set_color(c)` —— 属性动画
- `MoveToTarget(mobject)` —— 先设 `m.target` 再播放

### 文字与公式

- `Text("内容", font=字体, font_size=26, color=..., weight=BOLD)` —— 纯文字一律用它
- `MathTex(r"...")` —— 真公式才用，依赖 LaTeX 环境
- `t.become(Text(...).move_to(原锚点))` —— 二维文字原地更新
- `DecimalNumber(x, num_decimal_places=2)` —— 纯数字读数

### 公式与零件化（MathTex 进阶）

- `MathTex(r"x", r"=", r"\frac{-b \pm \sqrt{b^2-4ac}}{2a}")` —— 多参数拆件，每项成为可寻址子对象 `t[0]`、`t[2]`
- `t.set_color_by_tex("x", RED)` —— 按子串染色；拆件后优先用下标 `t[0].set_color(RED)`，更稳
- `TransformMatchingTex(a, b)` —— 按相同子串对齐变形，推导链换式的标准演法
- `index_labels(t)` —— 调试专用：给每个子对象贴上序号小标签，拆件下标对不上时先用它看图（模块级函数，`self.play(Create(index_labels(t)))` 或 `self.add(index_labels(t))`，调完删掉）

### 数值驱动

- `ValueTracker(v)` + `tracker.animate.set_value(v2)` —— 参数滑杆
- `always_redraw(lambda: ...)` —— 每帧重建的活对象（**不能对它 become**，见 pitfalls）
- `m.add_updater(lambda m, dt: ...)` / `m.clear_updaters()` —— 每帧更新
- `rate_func=linear / rush_into / smooth / there_and_back` —— 节奏曲线

### 坐标与图形

- `NumberLine(x_range=[a, b, step], length=..., include_ticks=True)`；`line.n2p(x)` 数值转坐标
- `Axes(x_range=..., y_range=..., x_length=..., y_length=..., tips=False)`；`axes.c2p(x, y)`、`axes.plot(f, x_range=[...])`
- `NumberPlane(x_range=..., y_range=..., background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.25}, faded_line_ratio=0)` —— CE 0.21 中 `axis_config` 仍可配置坐标轴；网格线型使用 `background_line_style`
- `Dot(p, radius=0.07, color=...)`、`Line(a, b)`、`DashedLine(a, b)`、`Arrow(start, end, buff=0, max_tip_length_to_length_ratio=0.12)`
- `CurvedArrow(a, b, angle=TAU/3, tip_length=0.18)` —— 弧形箭头/循环示意
- `Polygon(p1, p2, ..., fill_opacity=0.5)`、`Square(side_length=...)`、`Rectangle(width=..., height=...)`
- `Circle(radius=...)`、`Arc(radius=..., start_angle=..., angle=..., arc_center=...)`
- `Angle(line1, line2, radius=0.5)` —— 角标弧线；`RightAngle(line1, line2, length=0.3)` —— 直角符号
- `VGroup(*items)`、`v.arrange(RIGHT, buff=...)`、`v.add(...)`
- `v.arrange_in_grid(rows=2, cols=3, buff=0.6)` —— 网格排布，图鉴/多面板用
- `Paragraph("第一行", "第二行", line_spacing=0.8)` —— 多行文字，自动换行对齐
- `SurroundingRectangle(mobject, buff=0.2)` —— 描边框（填充必须锁 0）

### 布局定位

- `m.move_to([x, y, 0])`、`m.move_to(p, aligned_edge=RIGHT)` —— 钉缘对齐
- `m.next_to(参照物, UP, buff=0.25)` —— 相对定位优先于手写偏移
- `m.to_edge(UP, buff=...)`、`m.to_corner(UL, buff=...)` —— 贴边/贴角

### 强调与镜头

- `Indicate(m, color=..., scale_factor=1.15)` —— 关键件闪烁放大
- `Circumscribe(m)`、`Flash(p)`、`Wiggle(m)` —— 圈注 / 闪光 / 抖动
- `ThreeDScene`：`self.set_camera_orientation(phi=..., theta=...)`；钉屏 `self.add_fixed_in_frame_mobjects(m)`
- `MovingCameraScene`：`self.camera.frame`（无 add_fixed_in_frame_mobjects！）；运镜用 `self.play(self.camera.frame.animate.set_width(6).move_to(p))` 链式属性动画

### 播放控制

- `self.play(anim1, anim2, run_time=1.2, lag_ratio=0.12)` —— lag_ratio 级联入场
- `self.wait(2.0)` —— 驻留；每个教学节拍 ≥1.2 s，关键读数 ≥2 s
- `Rotate(m, angle=-82*DEGREES, about_point=m.get_corner(DR))` —— 绕点翻转

## 渲染命令

- 验证：`manim -ql --disable_caching file.py SceneName`（480p，快）
- 出片：`manim -pqh file.py SceneName`（1080p60）
- 调试：`manim -qh -n 0,3 file.py SceneName`（分段）、`-s`（只渲末帧）

---

# teaching-style.md — 教学动画版式规范

> 教学动画与炫技动画的区别在版式纪律。本文件的每条规则都对应一次真实的课堂反馈或渲染事故。

## 颜色语义（全局固定，不得随机配色）

| 颜色 | 角色 | 用法 |
|---|---|---|
| 金（GOLD） | 关注与结论 | 主角对象、奠基件、verdict 结案语 |
| 红（RED） | 变化与矛盾 | 关键变化、错误示范、反例翻车、证明中的矛盾 |
| 绿（GREEN） | 成立与验证 | 验算通过、取等/取到最值的瞬间、结论行 |
| 青（TEAL） | 辅助与链条 | 辅助线、假设对象、传递链条中的普通成员 |
| 灰（GREY/GREY_B） | 背景与残影 | 网格、坐标轴、操作前的残影 |
| 白（#EDEDED） | 正文文字 | 注释条、一般读数 |

**纪律**：颜色是逻辑角色不是美术偏好。同一个对象变色 = 角色改变（如"待证的新增量"红色入场、证明成立后染金并入）。

## 五件套版式（教学场景的公共骨架）

1. **标题**（`to_corner(UL, buff=0.3~0.5)`，font_size=32，BOLD）：用问题不用定义——"√2 能写成一个分数吗？"而非"√2 的无理性证明"。
2. **注释条**（固定锚点 `DOWN * 3.55`，font_size=26）：每拍一句口语化讲解，用 `become` 换词；它是老师的嘴。
3. **读数面板**（画面右上区域，x 约 4.6~5.0）：标签右缘钉死、数字左缘钉死（`move_to(p, aligned_edge=RIGHT/LEFT)`），位数变化只向右生长，防止叠字。
4. **verdict 结案语**（`[0, -2.75, 0]`，金色 BOLD，font_size=28）：一句话定律，FadeIn(shift=UP*0.3) 登场后至少驻留 2.8 s。
5. **节奏分镜表**（写在模块 docstring 或交付说明里）：段落 / 时长 / 画面动作 / 讲解要点四列。

## 节奏纪律

- 每个教学节拍之间 `self.wait(1.2~2.4)`，让观众数得清、问得出；
- 奠基性的"第一次"要慢（0.6 s+），重复性的链条要快（0.34 s）——速度差本身就是叙事；
- 一个 `play` 里最多 3 个动画，每个节拍要等得起一句讲解；
- 关键读数出现后至少驻留 2 s 再推进。

## 字体与符号

- 中文显式字体三平台备选：Windows `Microsoft YaHei` / macOS `PingFang SC` / Linux `Noto Sans CJK SC`；
- **安全符号表**（微软雅黑实测有字形）：→ ← ≥ ≤ √ Δ θ ° × · ² ³ ± ≈ ≠；
- 安全表之外的符号（⟹ ⟺ ✓ ✗ ⊆ ∈ 等）先用一行最小场景试渲染，缺字形会静默渲成豆腐块，不报错；
- 纯文字用 `Text`；只有真公式用 `MathTex`（LaTeX 环境是额外安装门槛）。

## 画面布局红线

- 右侧面板行长文案：中心 x ≥ 4.6 时按字数估算宽度（CJK 字 ≈ 0.36 × font_size/26 单位/字），右缘不得越过 ±7.1；
- 会动/会转的对象按**活动范围**划地盘，不按静止占地；
- 多幕场景幕间道具零共享：整批 FadeOut，绝不复用旧对象；
- 标签定位优先几何关系（`next_to`、角平分线方向），禁止手写魔法偏移。

---

# math-accuracy.md — 数学正确性军规

> 证明与演算类动画里，画面本身就是证据——数字错一个、点位偏一分，动画就从证明变伪证。

## 军规一：数值必须由真公式现算，禁止手抄结论数字

- 画面报出的每一个数（区域数、距离、和、极限值……）都要从驱动动画的变量算出来；
- **验收方法**：全文搜索结论数字的字面量（如 `31`、`0.39`）——搜到即违规；
- 组合数用 `math.comb`，距离用 `np.hypot`，不要因为"这个数我记得"而写死；
- 反例数字尤其不许手抄：它是推翻猜想的关键证物，本身必须可重算。

## 军规二：演示点位必须固定且可复现

- 禁止 `random`：随机点位每次渲染换位置，读数、撞线对、剪辑全部失效；
- "任意取点"的教学语义用**文件头常量**表达（如 `PTS = [...]`），想换一组就改常量重渲；
- 需要"看起来不规则"时用固定扰动（`i*7°`）或固定偏移表（`itertools.product([-0.14, 0.14], repeat=2)` 轮取）；
- 点位若要求"一般位置"（无三线共点等退化），扰动后必须验算关键数量不变。

## 军规三：几何派生点必须公式化，禁止目测摆位

- 垂足用投影公式 `(v·u)/(u·u)·u`；截点用参数方程；交点用解析解；
- "差不多摆一个看着像的位置"在静态帧里看不出，一动就露馅：垂线不垂直、弦高脱弧；
- 派生量链条要可溯源：改一个基础参数（如半径 Q），所有派生点自动跟随——这是检验公式化的试金石。

## 军规四：读数与几何同源

- 读数面板显示的值与画面几何必须从**同一批变量**算出；
- 读数与画面各算各的，改一个参数两边就打架（16、17 章各抓到过一起）。

## 军规五：假设 / 递推的节奏给足驻留

- 证明动画的信息密度在"步"上：每一步推理配独立 `wait`（1.3~2.4 s）；
- 循环生成的推理步禁止一口气播完——观众要看到"步"，不是只看到"开始"和"结束"；
- 逻辑关节词（"假设""最小""矛盾""所以"）必须出现在画面文字层，不能只在配音里。

## 军规六：颜色绑定逻辑角色

- 假设与链条用冷色（青），矛盾与翻车用红，奠基与结论用金，验证通过用绿；
- 生成前先写角色表，验收时逐帧核对颜色语义与逻辑角色一致。

---

# pitfalls.md — Manim 教学动画避坑清单

> 本文件是 AI Skill 的"事故档案"，每条都来自一次真实翻车。
> 生成或审查 Manim 代码时逐条对照；新事故随时补充（格式：错误写法 → 正确写法 → 原因）。
> 对应图书《Manim，让数学看得见》第 19 章。

## A. 版本与 API（GL/CE 混用类）

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| A1 | `from manimlib import *` | `from manim import *` | manimlib 是 3b1b 原版（GL），与社区版（CE）互不兼容 |
| A2 | `self.play(ShowCreation(m))` | `self.play(Create(m))` | ShowCreation 是 GL 旧接口，CE 已废弃 |
| A3 | `TextMobject("标题")` / `TexMobject` | `Text("标题")` / `MathTex` | 前者是 GL 名称，CE 已改名 |
| A4 | `manim file.py Scene` 无参数直接渲 | 显式指定画质：`-ql` 验证 / `-qh` 出片 | 无参数默认行为随版本变化，且容易渲出不需要的高清长视频 |
| A5 | 2D 运镜场景里 `self.camera.add_fixed_in_frame_mobjects(m)` | 用 updater 钉屏：`pin_to_screen(self.camera, m, "UL")`（每帧按取景框中心与缩放重算位置和尺寸，见 ch06_camera/hud_demo.py） | 该方法只存在于 `ThreeDCamera`（0.21 源码核实），`MovingCamera` 调用报 AttributeError（2026-08-26 第 6 章初稿真机渲染抓获，凭记忆写 API 的代价） |
| A6 | `TracedPath(tip_dot)` 传 mobject | `TracedPath(tip.get_center)` 传 callable，mobject 另用 updater 驱动 | 当前 CE 版本首参是 traced_point_func，传对象报 `'Dot' object is not callable`（2026-08-28 第15章 FourierStar 事故） |
| A7 | `DashedVMobject(circle, dash_length=0.06)` | `DashedVMobject(circle, num_dashes=30)` | 当前版本无 dash_length 参数，报 `unexpected keyword argument`（2026-08-28 同场景事故） |

## B. 动画设计类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| B1 | 交换用两个 `animate.move_to` 直线对穿 | `CyclicReplace(a, b)` 弧线互换 | 直线对穿互相遮挡；弧线轨迹本身在解释"交换" |
| B2 | 一个 `play` 里塞 5 个以上动画 | 按教学节拍拆成多个 `play` | 动画的每个节拍要等得起一句讲解 |
| B3 | `VGroup` 元素交换后仍用旧下标引用 | 交换后立即同步 VGroup 内的引用顺序 | 视图与数据不同步，后续比较结果全错 |
| B4 | 同位置公式替换用交叉淡入淡出：`old.animate.set_opacity(0)` 与 `new.animate.set_opacity(1)` 同帧播放 | 顺序替换：`play(old.animate.set_opacity(0))` 完成后再 `play(new.animate.set_opacity(1))`（或用 `TransformMatchingTex`） | 过渡期两个半透明公式堆叠，糊成一团无法阅读（2026-08-26 复刻 3B1B 导数几何系列抽帧抓获） |
| B5 | 描边框用 `box.animate.set_opacity(1)` 显现 | `box.set_fill(opacity=0)` 锁死填充，只动 `set_stroke(opacity=...)`，或直接用 `Create(box)` | `set_opacity` 把填充一起拉满，实心色块盖住框内公式（同日同批抓获，SurroundingRectangle 重灾区） |
| B6 | 密集区标签手写偏移坐标（如 `Ppos + UP*0.48 + LEFT*0.14`） | 用几何关系定位：角平分线方向 `normalize(u1+u2)`、`next_to(参照物, 方向, buff≥0.2)` | 手写偏移换一个参数就撞车；几何定位随图形自适应（同日正弦场景 P 点三标签相撞事故） |
| B7 | 多幕场景前一幕演员留在原地不退场 | 转场时处理旧演员：`FadeOut` 退场，或 `scale(0.5).move_to(顶部)` 缩小置顶留作对照 | 新幕道具直接叠在旧演员身上，画面撞车（2026-08-27 第7章 TransformFamily 第三幕星圆卡片三叠事故） |
| B8 | 会动/会转的元素按静止时占地划位置（如自转文字放右下角） | 按其活动范围划地盘：旋转体会扫过比静止 footprint 大一圈的区域，避开注释条锚点（DOWN*3.2） | 旋转中文字扫进注释条区域，两段文字重叠不可读（同日 UpdaterDemo 抽帧抓获） |
| B9 | 三维场景里对钉屏文字（fixed_in_frame）用 Transform 更新 | 钉屏文字更新用“新建 → 卸钉 → `remove` → 再钉”瞬切：先创建新对象，再 `remove_fixed_in_frame_mobjects(old)`、`self.remove(old)`（卸钉只是解绑，对象还躺在三维舞台上），最后 `add_fixed_in_frame_mobjects(new)` | Transform 会把钉屏对象拖进三维空间躺平；只卸钉不 remove，旧注释以三维身份留在舞台上越积越多（2026-08-27 第8章三维四场景集体事故） |
| B10 | 三维钉屏数值面板用 `DecimalNumber.set_value`、`Text.become()`，或从 updater 内执行四步换对象 | 数值用 `Text` 组成完整面板；把连续行程拆成短的线性 `play`，只在相邻 `play` 之间按 B9 的四步整体替换面板 | `set_value`/`become` 会让新字模脱离钉屏；即使执行四步，若发生在 updater 内，Cairo 已为当前 `play` 缓存的运动对象仍可能渲染被卸钉的旧字，形成斜挂残影（2026-08-28 ParaboloidSlices 全程抽帧确认） |
| B11 | 滑参动画让参数连续路过退化值（如 a 从 1 滑到 −0.5 必经 a≈0），绘图区间按当前参数自适应（如 `√(5/|a|)`） | 对参与定义域计算的参数钳位：`a_safe = max(abs(a), 0.25)`，区间按钳位后的值算 | a→0 时 `√(5/|a|)` 爆炸，plot 区间撑到天文数字，点阵内存爆掉直接 MemoryError（申请 25.8 GiB），渲染崩在半路（2026-08-27 第9章 TransformStudio 事故） |
| B12 | 数值面板"标签 next_to 锚点 + 数字右对齐同一锚点" | 两列钉缘：标签右缘钉死（`move_to((x1,y), aligned_edge=RIGHT)`）、数字左缘钉死（`move_to((x2,y), aligned_edge=LEFT)`），数字位数变化只向右生长 | 两个对象钉同一锚点必叠字；标签 next_to 数字则数字变宽时把标签顶飞（2026-08-27 第10章 CircleTheorems/VectorProof 面板叠字事故） |
| B13 | "指针已就位"循环写 `range(2, N+2)` | 先数清楚剩余次数：指针已在 z1 上，到 z1^N 只需 `range(2, N+1)`（N−1 次） | 多转一次越过目标落点，计数牌翻出 z1^6，扫圈论证当场穿帮（2026-08-28 第15章 UnitRoots 抽帧抓获） |
| B14 | 坐标网/坐标轴背景上的实体图形用半透明填充（`fill_opacity<1`） | 网格背景上的"演员"一律不透明填充 `fill_opacity=1.0`；要轻盈感去降描边透明度，别动填充 | 轴线透过填充穿身而过，像被坐标轴戳穿，印刷图上尤其刺眼（2026-08-31 第4章 PositioningDemo 图4-2 作者目检抓获）；同场附 B7 又一例：只服务第一幕的坐标标签悬在二三幕，转幕时 `FadeOut` 谢幕 |
| B15 | 把 `TransformMatchingTex` 的中途帧直接用作静态插图 | 动画保留连续变形，书中静态图改用变形前、变形后两张独立帧对照 | 淡出、淡入和匹配移动的零件会在中途同时出现，单帧容易重叠成乱码；第 5 章图 5-7 真机抽帧复现（2026-09-05） |
| B16 | 多站世界块按两个屏幕宽排开，直接抽取平移中途帧 | 按中途取景框计算站间距，让相邻文字在静态帧中完整同框 | 站间距过大时中途帧两端文字各被裁掉一半；第 6 章图 6-3 真机抽帧复现（2026-09-05） |
| B17 | 第一站字幕已写好，却让镜头从默认中心位置动画移向第一站 | 先把 `camera.frame` 直接布到第一站并停留，再从第二站开始巡游 | 开场字幕与画面对象错位，镜头先倒退再前进；第 6 章 `HudDemo` 真机抽帧复现（2026-09-05） |
| B18 | 多幕对照场景只保留最终图形，不标明各图形所属操作 | 在最终定格帧为保留对象补上简短操作标签 | 视频里靠时间顺序能分辨，印成单幅静态图后语义丢失；第 7 章图 7-2 抽帧复现（2026-09-05） |
| B19 | 进度条直接调用 `stretch_to_fit_width`，使用默认中心作为伸缩基准 | 用 `about_edge=LEFT` 固定起点，并增加不动的满量程轨道 | 默认行为会让色块同时向两侧膨胀，读者难以把它识别为从零端增长的进度；第 7 章图 7-3 抽帧复现（2026-09-05） |
| B20 | 三维主体按画面中心构图，却没有给左上钉屏长标题预留安全区 | 用最拥挤的关键状态检查屏幕投影；必要时缩短标题或收敛字号，确保标题边界与主体留有清晰间隔 | 三维对象的屏幕投影可能侵入固定界面层；第 8 章图 8-5 在 `h=3.20` 静帧中复现碗沿逼近 32 号长标题（2026-09-05） |
| B21 | 误以为 `Axes.plot` 会自动裁剪到坐标轴框 | 按当前函数的纵向安全边界反算 `x_range`，并为标题、注释条额外留净空 | 第 9 章图 9-2、9-4、9-5 复核时发现曲线或割线越过坐标轴，侵入标题/注释区；`Axes.plot` 本身不做视窗裁剪（2026-09-05） |
| B22 | 二维钉屏仅让文字尺寸随取景框缩放，边距仍用固定世界单位 | 文字尺寸与边距都乘 `frame.height / 初始框高` | 缩放时固定世界边距对应的屏幕边距会变化，HUD向边缘漂移；第6章复核以0.5倍、2倍框高和偏移机位复现（2026-11-03） |
| B23 | 参数曲线始终按完整横坐标范围重画，误以为坐标轴会裁剪曲线 | 随当前参数反算可见自变量范围，曲线留在坐标区内；必要时关闭平滑避免端点附近越界 | 第7章ParabolaSlider在a=2.5时把y画到40，曲线冲出画面并穿过标题区；按y≤7.5限制范围并对两段参数行程检查边界（2026-11-03） |
| B24 | 圆周角换侧后仍用Angle默认逆时针分支，读数120°却画出240°角弧 | 按两边向量叉积符号选择other_angle，使角弧表示实际较小夹角；直角标记需与数值容差一致 | 第10章CircleTheorems在P=240°的原版画面与回归检查均复现；优弧/劣弧上的读数正确不代表标记也正确（2026-11-03） |
| B25 | 圆上动点从150°连续移到255°，忽略路径经过直径端点180° | 检查整段参数路径，避开使PA或PB为零的端点；需要换弧时明确跳切或换合法路径 | 第10章VectorProof的原路径经过P=A，圆周角与两非零向量夹角在该处无定义；低帧率恰好跳过也不代表路径有效（2026-11-03） |
| B26 | 用正数下限保护根号，仍把a=c的椭圆当成精确线段 | 合法域内允许b=0并单独画线段，a<c拒绝构造；无解示意移除旧轨迹与账本 | 第12章原b下限0.001、轮廓高度下限0.04，且无解幕残留等号状态；数值检查复现后按三种条件分开处理（2026-11-04） |
| B27 | 指数参照线画至x=6.6，误以为纵轴范围会自动裁剪 | 按当前项数和纵轴范围限制绘图区间，并核对末端 | 第12章2^(x−1)在6.6处约48.50，超过纵轴36；本例改画第1至6项对应区间（2026-11-04） |
| B28 | 仅给场景后部的空对象加updater，从中修改前面的曲线和读数，误以为渲染器会自动识别这些对象在运动 | 将updater挂在实际变化的曲线、读数组或其共同父组上，共享同一组参数；抽查运动中间帧 | ManimCE 0.21.0的Cairo优化可能把不含updater的前置对象作为静态背景缓存，数值计算已变但画面直到下一拍才更新；标准讲解帧制作版以中途曲线及读数停在旧值复现，改为对象自身更新后中间帧同步（2026-11-21） |
| B29 | 三维地面参照线默认不参与3D深度排序，以为降低z_index就不会盖过实体 | 核对所用相机的实际排序；当地面确在所有实体之下时，将明确标记的地面参照先绘制，再绘制实体，保持其余深度排序；用有/无参照线的实体内部像素对照验收 | 08-02高清首帧复现网格透过球及圆锥。ManimCE 0.21.0 ThreeDCamera把未启用shade_in_3d的对象排序为无穷远键，单改z_index仍排在曲面后；内部相机仅重排已标记的地面，实体不透明，重渲染后106691个内部像素仅25个因曲面片接缝抗锯齿相差最多4/255，其余一致，99.9百分位差为0，未见地面线覆盖实体（2026-11-22） |

## C. 文字与动态文本类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| C1 | 中文直接 `Text("你好")` 不指定字体 | `Text("你好", font="Microsoft YaHei")`（macOS: PingFang SC / Linux: Noto Sans CJK SC） | 默认字体不含中文，渲染成方块 |
| C2 | **动态字幕用空文本初始化再定位**：`Text(" ")` → `to_edge(DOWN)` | 用真实首句初始化 + 固定锚点：`CAPTION_POS = DOWN * 3.2`，更新时 `new.move_to(CAPTION_POS)` | 纯空格被渲染成零宽高对象，定位静默失效，文字停在画面中心与图形重叠（2026-08-20 冒泡演示视频实车事故） |
| C3 | 更新文字：`remove(t); t2 = Text(...); add(t2)` | `t.become(Text(...))` 原地变形 | 先删后加造成闪烁；become 保持引用不变 |
| C4 | 字幕/标签用 `MathTex` 渲染纯文字 | 纯文字一律用 `Text`（斜体用 `slant=ITALIC`） | MathTex 依赖 LaTeX 环境，无端增加安装门槛 |
| C5 | 上屏特殊符号想当然（如 `⟹`、`⟺`） | 非常用符号先小样试屏；安全符号表：→、×、÷、²、½、°、✓；表达"推出"优先用汉字"即" | 字体缺字形时 Manim 静默渲染成豆腐块，不报错不警告（2026-08-27 第10章 PythagorasProof 横幅 ⟹ 豆腐块事故） |
| C6 | **三维钉屏文字用 become() 换词** | ThreeDScene 里 become 的子对象会脱落钉屏；必须四步：建新对象 → `remove_fixed_in_frame_mobjects(旧)` → `remove(旧)` → `add_fixed_in_frame_mobjects(新)` | become 替换的子对象不在相机 fixed 名单里，文字躺到 3D 地面成透视残影（2026-08-28 第13章四脚本集体事故）；C3 的 become 铁律仅限二维 |
| C7 | 只 `remove_fixed_in_frame_mobjects` 不 `remove` | 摘钉后必须再 `remove()` 摘除场景 | remove_fixed 只摘钉不摘场景，旧文字作为普通 3D 物体残留在地面（2026-08-28 同事故第二层残影） |
| C8 | 三维曲面用默认分辨率批量造（如 12 个 Cylinder） | 显式降采样：`Cylinder(resolution=(2,16))` 等；提示词里永远写明 resolution | 默认网格极密，12 枚硬币默认 11 分钟 vs 降采样 23 秒（2026-08-28 第13章 ZugengPrinciple） |
| C9 | 把 become 包进 play：`self.play(note.become(Text(...)))` | become 不进 play——封装成 `set_note` 助手直接瞬时换词（二维场景惯例）；要过渡动画才用 `note.animate.become(...)` | `become` 返回 mobject 本身而非 Animation，传进 play 报 `Unexpected argument VMobjectFromSVGPath passed to Scene.play()`（2026-08-31 附录 B 三场景初稿事故，render_check 抓获） |
| C10 | `MathTex(r"\text{勾股定理}")` 里塞中文 | 中文一律用 `Text`（字体见 C1），公式里的中文标注用 `MathTex` 与 `Text` 分列组装，或 LaTeX 模板换 ctex | 默认 LaTeX 模板不含中文字形，报 Unicode error 或渲出豆腐块；纯文字本来就该用 Text（C4 的推论） |
| C11 | 直接把 `index_labels(mobject)` 的默认结果当正式插图 | 用 `color=RED` 指定编号颜色，再以整个公式为纵向参照、对应零件中心为横向参照，把编号排到公式下方 | 默认编号是白色并位于各子对象中心，会与公式笔画重叠；第 5 章图 5-5 真机渲染复现（2026-09-05） |
| C12 | 为了让多行公式等号对齐，只移动每行的等号子对象 | 比较锚点等号与当前等号的横坐标差，再用 `row.shift(shift_x * RIGHT)` 平移整行 | 单独移动等号会破坏 `MathTex` 内部间距，使等号与左右公式重叠；第 5 章图 5-6 真机渲染复现（2026-09-05） |
| C13 | 钉屏字幕 `Transform(note, Text(...))`，新文字仍在原点，且默认暂停updater | 先使目标文字匹配当前高度和位置，再用 `suspend_mobject_updating=False` 保持钉屏更新器工作 | 默认Transform暂停被变形对象的updater，字幕向世界原点移动后才跳回底部；第6章HudDemo换词中途帧与回归检查复现（2026-11-03） |
| C14 | 为适应坐标范围缩放函数值，却仍在标题显示缩放前的公式 | 标题、正文、参数方程和坐标读数使用同一个实际表达式 | 第8章SurfaceDemo画的是z=(x²−y²)/2.5，原渲染标题却显示z=x²−y²；复核原版画面后同步修正标题（2026-11-03） |
| C15 | 数量积的微小负浮点残差直接保留两位小数，显示为-0.00 | 明示小容差，仅把其内残差显示为0，保留其他实际数值并另做数学证明 | 第10章VectorProof在P=30°的修正路径片尾复现-0.00；采用1e-10容差，并用离圆点检验0.04不会被归零（2026-11-03） |
| C16 | 长字幕直接居中到右侧面板，未检查文字右缘 | 先精简字幕，并检查包围盒在画幅内；必要时换行或适度缩小 | 第10章AnalyticProof结论行在右侧被裁切，缩短为“中点相同，对角线互相平分”后核对边界并重新渲染（2026-11-03） |
| C17 | 动点开始下一段运动时，仍保留上一停靠点的精确数值结论 | 运动前改为过程提示，到达并停下后再显示该位置结论 | 第11章CircleToWave进入第三象限时，原字幕仍写sinθ=0而面板已为负；逐段运动前更新观察提示并重新渲染（2026-11-04） |
| C18 | 距离面板与椭圆右上弧共用空间，曲线穿过标签 | 以最大轮廓核对标签包围盒，将面板移到右侧净空区 | 第12章EllipseString正常椭圆穿过距离和标签，右移账本后按字框下缘对应的椭圆包络检查间隔并重渲染（2026-11-04） |
| C19 | 三维点名只加固定世界偏移，未核对整段相机路径的屏幕投影 | 图内点名保持世界锚点并固定朝向，再逐视角检查投影字框与轴线、网格、屏幕标题的间隔；必要时调整偏移或整个图的位置 | 08-01制作版高清目检发现O被负向轴线穿过、Q靠近网格，另有末端视角z轴名靠近标题；移动图形并把O/Q标注置于空白处，181个相机状态检查投影安全区及字框与线段不相交后重渲染通过（2026-11-22） |
| C20 | 模型模块也导出ORIGIN，覆盖Manim的零向量后仍用它摆放屏幕字形模板 | 世界原点使用WORLD_ORIGIN等明确名称或导入别名，屏幕字形模板以零向量排版；检查数字与标签的共同基线和运动中实际帧 | 08-03高清静帧发现u、v、z读数整体低于各自标签，根因是ORIGIN已变为构图用世界平移；别名隔离后361个读数状态行锚点及实际字形检查（2026-11-22） |
| C21 | 自定义Mobject子类把数字子对象命名为self.height，覆盖基类尺寸属性 | 使用height_digits、height_label等明确字段，不覆盖width、height、depth等已有属性 | 08-04读数初次低清在super初始化前给self.height赋对象，触发Mobject尺寸setter，报缺少submobjects；改为height_digits后标准低清通过（2026-11-22） |

## D. 工程习惯类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| D1 | 一次性改多处再渲染 | 每次只改一处，`-ql` 快速验证 | 改三处出错时无法定位是哪一处 |
| D2 | 长场景整段渲染调试 | `-n 0,3` 分段渲染 / 先 `-s` 看末帧 | 重复等待与问题无关的片段；节省幅度取决于场景 |
| D3 | 变量名 `c1`、`x2`、`arr` | 教学语义命名：`compare_color`、`sorted_bar` | 代码即教材，命名即讲解 |
| D4 | 验证/预检脚本把临时渲染目录建到系统 temp（`tempfile.TemporaryDirectory()` 默认系统盘） | 临时目录建在工作区内：`tempfile.TemporaryDirectory(prefix=".manim_check_", dir=".")`，用完即删 | 一次本机事故中，工作区在 E 盘、系统 temp 在 C 盘时，MiKTeX 的 dvisvgm 静默返回 −4，manim 层只报 DVI 转 SVG 失败；这是该环境的复现记录，不外推为所有 Windows 机器的规律（2026-09-02 render_check 自身翻车抓获） |
| D5 | 用简单过滤删除所有以连字符开头的参数，再把剩余项全当作位置参数 | 显式识别 `-o`，连同其后一个值从位置参数中移除，再解析视频路径与秒数 | 输出目录会混进秒数列表并触发 `float(path)` 的 `ValueError`；第 7 章正式抽帧按文档调用 `extract_frames.py -o` 时复现（2026-09-05） |
| D6 | 需要逐帧相同的两轮回放，直接以浮点秒差调用静态wait，并只核对相机目标 | 在没有持续更新任务的驻留段，以目标整数帧减去实际已写帧计算等待；为静态冻结的向下取整保留小于一帧的余量，核对每轮开始帧及实际中途画面 | ManimCE 0.21.0 Cairo的freeze_current_frame按int(duration/dt)写帧；06-03内部制作版的3秒驻留因浮点残差只写179帧，使第二轮平移提前1帧；按整数帧对齐并在静止段用(剩余帧+0.25)/fps冻结等待后，两轮实际起止帧一致。此做法不用于需持续运行updater的等待（2026-11-21） |
| D7 | 活动wait直接用半秒边界，并假定每种帧率下末次dt累计都等于duration减一帧 | 按目标整数帧安排活动等待，检查实际采样时刻及累计dt；arange式活动等待按包含的采样点计帧，不套用静态wait的向下取整补偿 | 07-03制作版在15fps低清中13.5秒对应202.5帧，活动wait产生203帧，末次累计时间与整帧假定不符；源码核对后以目标帧数控制开区间终点，60fps为810帧，15fps也保持全片目标帧数。持续自转段用单一活动等待，换字幕不切断dt时间轴（2026-11-22） |

---

**新增事故记录格式**（追加到对应分类，编号顺延）：

```
| Xn | 错误写法（一句话） | 正确写法（一句话） | 原因（一句话 + 事故日期） |
```

---

# qa-checklist.md — 交付前验收清单

> 渲染通过只是及格线。本清单是两道验收关卡的完整版：**机器查语法，人（或抽帧）查画面**。
> 每次交付前逐条过一遍；任何一条不过，回到对应规则文件修。

## 第一关：渲染验证（机器执行）

- [ ] `python scripts/render_check.py <file.py> <SceneName>` 输出 `RENDER_OK`；
- [ ] 渲染日志中无 `WARNING` 级别的字体回退提示（`warn_missing_font` 命中会在这里出现）；
- [ ] 临时产物在临时目录，工作区无 `media/` 残留污染；
- [ ] 最终出片用 `-pqh`，验证只用 `-ql`——预览不当母版。

## 第二关：抽帧目检（看画面）

用 `scripts/extract_frames.py` 至少抽三帧：开场帧 / 信息密度最高帧 / 结束帧。逐帧核对：

- [ ] 没有任何文字与图形重叠（字幕、标签、读数面板逐一检查）；
- [ ] 没有任何元素超出画面边界（±7.1 × ±4.0，竖屏另算）；
- [ ] 没有豆腐块（缺字形渲染成的方框）；
- [ ] 注释条位置全程固定，只有内容在变；
- [ ] 会动/会转的元素按其活动范围核对，不按静止占地；
- [ ] 幕间转场后无旧演员残留（上一幕的标签、箭头、高亮全部谢幕）。

## 第三关：教学审查（必须人来，不可外包）

- [ ] 颜色语义全程一致：金=关注、红=变化、绿=就位、蓝灰=背景，无临时换色；
- [ ] 每个节拍之间 `wait ≥ 1.2 s`，关键读数驻留 ≥ 2 s——每一拍等得起一句讲解；
- [ ] 一个 `play` 里不超过 3 个动画；
- [ ] 指针/标签有名字、有颜色、不突然消失；
- [ ] 结尾有定格画面，方便提问互动；
- [ ] 画面上的每个数字都经得起手工验算（对照 `rules/math-accuracy.md` 军规一）。

## 验收记录（建议随交付附上）

```
场景名：        渲染：RENDER_OK（第 N 轮通过）
抽帧：          开场 / 密度帧 / 结束帧 三帧已检
教学审查：      通过 / 存疑项：______
```
