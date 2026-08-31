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
