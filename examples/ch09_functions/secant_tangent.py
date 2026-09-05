from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）
PLOT_Y_MIN = -1.0
H_START = 1.0             # 保证初始动点 Q(2, 4) 位于坐标轴视窗内


class SecantToTangent(Scene):
    """割线逼近切线：极限不是代入，是无限靠近的过程。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("割线逼近切线：极限的眼睛", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("y = x²，盯住点 P(1, 1)", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        axes = Axes(x_range=[-1, 3, 1], y_range=[PLOT_Y_MIN, 5, 1],
                    x_length=8.5, y_length=5.8,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to(ORIGIN + UP * 0.1)
        curve = axes.plot(lambda x: x**2, x_range=[-1, 2.2],
                          color=TEAL, stroke_width=4)
        self.add(title, self.note)
        self.play(Create(axes), Create(curve), run_time=1.8)

        P = Dot(axes.c2p(1, 1), color=GOLD, radius=0.09)
        h = ValueTracker(H_START)   # 遥控器：Q 与 P 的横距

        def secant():
            m = 2 + h.get_value()          # 割线斜率 = ((1+h)²−1)/h = 2+h
            x0 = max(0.2, 1 + (PLOT_Y_MIN - 1) / m)
            x1 = 1.9                       # 过 P、斜率 m 的可见线段
            return Line(axes.c2p(x0, 1 + m * (x0 - 1)),
                        axes.c2p(x1, 1 + m * (x1 - 1)),
                        color=RED, stroke_width=3)

        Q = always_redraw(lambda: Dot(
            axes.c2p(1 + h.get_value(), (1 + h.get_value())**2),
            color=RED, radius=0.08))
        sec = always_redraw(secant)
        # 斜率面板：割线斜率读数，随 h 逼近 2
        slope_num = always_redraw(lambda: Text(
            f"{2 + h.get_value():.2f}", font=FONT, font_size=36,
            color=GOLD).to_corner(UR, buff=0.6))
        slope_lab = Text("割线斜率 =", font=FONT, font_size=30,
                         color=C_TEXT)
        slope_lab.next_to(slope_num, LEFT, buff=0.12)

        self.set_note("Q 在远处：割线斜率 = 2 + h = 3.00")
        self.play(FadeIn(P), FadeIn(Q), Create(sec),
                  FadeIn(slope_lab), FadeIn(slope_num), run_time=1.5)
        self.wait(1)

        self.set_note("Q 滑向 P：割线转起来，斜率读数逼近 2")
        self.play(h.animate.set_value(0.15), run_time=6,
                  rate_func=linear)
        self.wait(1.2)

        # 切线登场：斜率恰好是 2——极限值，不是近似值
        tangent = Line(axes.c2p(0.2, 1 + 2 * (0.2 - 1)),
                       axes.c2p(1.9, 1 + 2 * (1.9 - 1)),
                       color=GREEN, stroke_width=4)
        tan_lab = Text("切线：斜率恰好 = 2", font=FONT, font_size=26,
                       color=GREEN)
        tan_lab.next_to(axes.c2p(2.2, 2.4), RIGHT, buff=0.1)
        self.set_note("h → 0 的极限：切线斜率恰好是 2")
        self.play(FadeOut(Q), FadeOut(sec), run_time=0.8)
        self.play(Create(tangent), Write(tan_lab), run_time=1.5)
        self.wait(1.5)
