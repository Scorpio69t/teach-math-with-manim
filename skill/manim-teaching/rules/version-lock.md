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
