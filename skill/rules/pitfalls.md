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

## B. 动画设计类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| B1 | 交换用两个 `animate.move_to` 直线对穿 | `CyclicReplace(a, b)` 弧线互换 | 直线对穿互相遮挡；弧线轨迹本身在解释"交换" |
| B2 | 一个 `play` 里塞 5 个以上动画 | 按教学节拍拆成多个 `play` | 动画的每个节拍要等得起一句讲解 |
| B3 | `VGroup` 元素交换后仍用旧下标引用 | 交换后立即同步 VGroup 内的引用顺序 | 视图与数据不同步，后续比较结果全错 |
| B4 | 同位置公式替换用交叉淡入淡出：`old.animate.set_opacity(0)` 与 `new.animate.set_opacity(1)` 同帧播放 | 顺序替换：`play(old.animate.set_opacity(0))` 完成后再 `play(new.animate.set_opacity(1))`（或用 `TransformMatchingTex`） | 过渡期两个半透明公式堆叠，糊成一团无法阅读（2026-08-26 复刻 3B1B 导数几何系列抽帧抓获） |
| B5 | 描边框用 `box.animate.set_opacity(1)` 显现 | `box.set_fill(opacity=0)` 锁死填充，只动 `set_stroke(opacity=...)`，或直接用 `Create(box)` | `set_opacity` 把填充一起拉满，实心色块盖住框内公式（同日同批抓获，SurroundingRectangle 重灾区） |
| B6 | 密集区标签手写偏移坐标（如 `Ppos + UP*0.48 + LEFT*0.14`） | 用几何关系定位：角平分线方向 `normalize(u1+u2)`、`next_to(参照物, 方向, buff≥0.2)` | 手写偏移换一个参数就撞车；几何定位随图形自适应（同日正弦场景 P 点三标签相撞事故） |

## C. 文字与动态文本类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| C1 | 中文直接 `Text("你好")` 不指定字体 | `Text("你好", font="Microsoft YaHei")`（macOS: PingFang SC / Linux: Noto Sans CJK SC） | 默认字体不含中文，渲染成方块 |
| C2 | **动态字幕用空文本初始化再定位**：`Text(" ")` → `to_edge(DOWN)` | 用真实首句初始化 + 固定锚点：`CAPTION_POS = DOWN * 3.2`，更新时 `new.move_to(CAPTION_POS)` | 纯空格被渲染成零宽高对象，定位静默失效，文字停在画面中心与图形重叠（2026-08-20 冒泡演示视频实车事故） |
| C3 | 更新文字：`remove(t); t2 = Text(...); add(t2)` | `t.become(Text(...))` 原地变形 | 先删后加造成闪烁；become 保持引用不变 |
| C4 | 字幕/标签用 `MathTex` 渲染纯文字 | 纯文字一律用 `Text`（斜体用 `slant=ITALIC`） | MathTex 依赖 LaTeX 环境，无端增加安装门槛 |

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
