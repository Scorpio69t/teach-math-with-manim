# Manim 教学动画协作手册（单文件版）

> 本文件由 build_dist.py 自动生成：SKILL.md + rules/ 四份规则的合并版。
> 粘贴进你的 AI 工具的自定义指令 / 项目知识 / 常用语即可生效。
> 内容更新时重新运行 build_dist.py，不要手改本文件。

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
- `CyclicReplace(a, b, ...)` —— 弧线互换位置，交换语义的标准演法
- `mobject.animate.move_to(p) / .set_value(v) / .set_color(c)` —— 属性动画
- `MoveToTarget(mobject)` —— 先设 `m.target` 再播放

### 文字与公式

- `Text("内容", font=字体, font_size=26, color=..., weight=BOLD)` —— 纯文字一律用它
- `MathTex(r"...")` —— 真公式才用，依赖 LaTeX 环境
- `t.become(Text(...).move_to(原锚点))` —— 二维文字原地更新
- `DecimalNumber(x, num_decimal_places=2)` —— 纯数字读数

### 数值驱动

- `ValueTracker(v)` + `tracker.animate.set_value(v2)` —— 参数滑杆
- `always_redraw(lambda: ...)` —— 每帧重建的活对象（**不能对它 become**，见 pitfalls）
- `m.add_updater(lambda m, dt: ...)` / `m.clear_updaters()` —— 每帧更新
- `rate_func=linear / rush_into / smooth / there_and_back` —— 节奏曲线

### 坐标与图形

- `NumberLine(x_range=[a, b, step], length=..., include_ticks=True)`；`line.n2p(x)` 数值转坐标
- `Axes(x_range=..., y_range=..., x_length=..., y_length=..., tips=False)`；`axes.c2p(x, y)`、`axes.plot(f, x_range=[...])`
- `NumberPlane(x_range=..., y_range=..., background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.25}, faded_line_ratio=0)` —— **0.21 起用 background_line_style，无 axis_config**
- `Dot(p, radius=0.07, color=...)`、`Line(a, b)`、`DashedLine(a, b)`、`Arrow(start, end, buff=0, max_tip_length_to_length_ratio=0.12)`
- `CurvedArrow(a, b, angle=TAU/3, tip_length=0.18)` —— 弧形箭头/循环示意
- `Polygon(p1, p2, ..., fill_opacity=0.5)`、`Square(side_length=...)`、`Rectangle(width=..., height=...)`
- `Circle(radius=...)`、`Arc(radius=..., start_angle=..., angle=..., arc_center=...)`
- `VGroup(*items)`、`v.arrange(RIGHT, buff=...)`、`v.add(...)`
- `SurroundingRectangle(mobject, buff=0.2)` —— 描边框（填充必须锁 0）

### 布局定位

- `m.move_to([x, y, 0])`、`m.move_to(p, aligned_edge=RIGHT)` —— 钉缘对齐
- `m.next_to(参照物, UP, buff=0.25)` —— 相对定位优先于手写偏移
- `m.to_edge(UP, buff=...)`、`m.to_corner(UL, buff=...)` —— 贴边/贴角

### 强调与镜头

- `Indicate(m, color=..., scale_factor=1.15)` —— 关键件闪烁放大
- `Circumscribe(m)`、`Flash(p)`、`Wiggle(m)` —— 圈注 / 闪光 / 抖动
- `ThreeDScene`：`self.set_camera_orientation(phi=..., theta=...)`；钉屏 `self.add_fixed_in_frame_mobjects(m)`
- `MovingCameraScene`：`self.camera.frame`（无 add_fixed_in_frame_mobjects！）

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

## D. 工程习惯类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| D1 | 一次性改多处再渲染 | 每次只改一处，`-ql` 快速验证 | 改三处出错时无法定位是哪一处 |
| D2 | 长场景整段渲染调试 | `-n 0,3` 分段渲染 / 先 `-s` 看末帧 | 调试效率差 5 倍以上 |
| D3 | 变量名 `c1`、`x2`、`arr` | 教学语义命名：`compare_color`、`sorted_bar` | 代码即教材，命名即讲解 |

---

**新增事故记录格式**（追加到对应分类，编号顺延）：

```
| Xn | 错误写法（一句话） | 正确写法（一句话） | 原因（一句话 + 事故日期） |
```
