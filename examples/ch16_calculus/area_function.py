"""第 16 章案例：微积分基本定理——面积函数的导数是原函数（代码清单 16-4）

渲染：manim -pqh area_function.py AreaFunction
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [5.3, 2.5, 0]       # x 读数
R2_POS = [5.3, 1.9, 0]       # 面积读数
R3_POS = [5.3, 0.9, 0]       # 长条节拍：ΔA 行
R4_POS = [5.3, 0.3, 0]       # 长条节拍：比值行

X_STOP = 2.0                 # 长条放大节拍的停靠点
DX = 0.2                     # 长条宽度


def f(t):
    """被积函数 1 + t/2——梯形面积能手算验证（第 9 章的验收纪律）。"""
    return 1 + t / 2


def A(x):
    """面积函数 ∫₀ˣ f = x + x²/4——它是 f 的一个原函数。"""
    return x + x**2 / 4


class AreaFunction(Scene):
    """上板阴影随 x 生长，下板描出面积函数 A(x)；
    停靠点放大一条新增的『面积长条』：ΔA/Δx 几乎就是 f(x)。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("面积越攒越多——攒的速度由谁决定？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("把阴影面积看成一个函数 A(x)，它是谁？长什么样？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 双板：上 f，下 A =====
        self.top = Axes(x_range=[0, 3.2, 1], y_range=[0, 3, 1],
                        x_length=7.2, y_length=2.6,
                        axis_config={"color": GREY_B, "stroke_width": 2},
                        tips=False)
        self.top.move_to([-0.9, 1.55, 0])
        self.bot = Axes(x_range=[0, 3.2, 1], y_range=[0, 6, 2],
                        x_length=7.2, y_length=1.8,
                        axis_config={"color": GREY_B, "stroke_width": 2},
                        tips=False)
        self.bot.move_to([-0.9, -1.65, 0])
        curve = self.top.plot(f, x_range=[0, 3.05], color=TEAL,
                              stroke_width=4)
        f_lab = Text("f(t) = 1 + t/2", font=FONT, font_size=24, color=TEAL)
        f_lab.move_to([-3.8, 2.6, 0])
        self.play(Create(self.top), Create(self.bot), run_time=1.2)
        self.play(Create(curve), FadeIn(f_lab), run_time=1.3)
        self.set_note("上面的曲线是 f；下面这块板，专门记录阴影面积")
        self.wait(1.6)

        # ===== 扫动：阴影生长，A(x) 被描出来 =====
        x_track = ValueTracker(0.02)
        area = always_redraw(lambda: self.top.get_area(
            curve, x_range=[0, x_track.get_value()],
            color=GOLD, opacity=0.5))
        a_dot = always_redraw(lambda: Dot(
            self.bot.c2p(x_track.get_value(), A(x_track.get_value())),
            radius=0.08, color=GOLD))
        trace = TracedPath(a_dot.get_center, stroke_color=GOLD,
                           stroke_width=4)
        readout1 = always_redraw(lambda: Text(
            f"x = {x_track.get_value():.2f}", font=FONT, font_size=26,
            color=C_TEXT).move_to(R1_POS))
        readout2 = always_redraw(lambda: Text(
            f"阴影面积 A = {A(x_track.get_value()):.2f}",
            font=FONT, font_size=26, color=C_TEXT).move_to(R2_POS))
        self.add(area, a_dot, trace, readout1, readout2)
        self.set_note("x 走到哪，阴影攒到哪；下面的金点把面积值逐点记下")
        self.play(x_track.animate.set_value(X_STOP), run_time=3.2,
                  rate_func=linear)
        self.wait(0.8)

        # ===== 长条节拍：ΔA ≈ f(x)·Δx =====
        x0 = X_STOP
        strip = Polygon(self.top.c2p(x0, 0), self.top.c2p(x0 + DX, 0),
                        self.top.c2p(x0 + DX, f(x0 + DX)),
                        self.top.c2p(x0, f(x0)),
                        color=RED, fill_opacity=0.7, stroke_width=0)
        box = Polygon(self.top.c2p(x0, 0), self.top.c2p(x0 + DX, 0),
                      self.top.c2p(x0 + DX, f(x0)), self.top.c2p(x0, f(x0)),
                      color=RED, fill_opacity=0.0, stroke_width=3)
        link = DashedLine(self.top.c2p(x0, f(x0)), self.bot.c2p(x0, A(x0)),
                          color=GREY_B, stroke_width=2)
        dA = A(x0 + DX) - A(x0)
        row3 = Text(f"ΔA = {dA:.3f}（红色长条）", font=FONT, font_size=22,
                    color=RED).move_to(R3_POS)
        row4 = Text(f"ΔA÷Δx = {dA / DX:.2f} ≈ f(2)", font=FONT,
                    font_size=22, color=GREEN).move_to(R4_POS)
        self.play(x_track.animate.set_value(x0 + DX), FadeIn(strip),
                  run_time=1.0, rate_func=linear)
        self.play(Create(box), FadeIn(row3), run_time=0.8)
        self.set_note("新增的这条面积：宽度 0.2，高度几乎不变——约等于 高 × 宽")
        self.wait(1.8)
        self.play(FadeIn(row4), Create(link), run_time=0.9)
        self.set_note("比值 2.05 已经咬住 f(2) = 2——Δx 再小就严丝合缝")
        self.wait(2.0)

        # ===== 继续扫完，结案 =====
        self.play(FadeOut(box), FadeOut(strip), FadeOut(link),
                  FadeOut(row3), FadeOut(row4), run_time=0.6)
        self.play(x_track.animate.set_value(3.0), run_time=1.6,
                  rate_func=linear)
        a_lab = Text("A(x) = x + x²/4", font=FONT, font_size=24,
                     color=GOLD)
        a_lab.move_to([2.35, -0.75, 0])
        self.play(FadeIn(a_lab), run_time=0.8)
        self.set_note("A(x) 攒面积的速度（导数），恰好是 f 的高度")
        self.wait(1.8)

        verdict = Text("连续函数下：面积函数的导数 = 被积函数",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to([0, -3.0, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("这就是微积分基本定理：两大主角本是同一件事的两面")
        self.wait(2.8)
