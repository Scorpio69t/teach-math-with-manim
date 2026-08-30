from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

N_TERMS = 6               # 两边都演示 6 项


class ArithVsGeom(Scene):
    """左：等差数列散点落在直线上；右：等比数列散点落在指数曲线上。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("等差与等比：一条直线，一条起飞曲线", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("同一个问题两种增长：每次加 3，还是每次乘 2？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 双坐标系 =====
        ax_l = Axes(x_range=[0, 7, 1], y_range=[0, 20, 5],
                    x_length=4.6, y_length=3.4,
                    axis_config={"color": GREY, "stroke_width": 1.5},
                    tips=False)
        ax_l.move_to(LEFT * 3.8 + DOWN * 0.15)
        ax_r = Axes(x_range=[0, 7, 1], y_range=[0, 36, 6],
                    x_length=4.6, y_length=3.4,
                    axis_config={"color": GREY, "stroke_width": 1.5},
                    tips=False)
        ax_r.move_to(RIGHT * 3.0 + DOWN * 0.15)
        lab_l = Text("等差：a = 2 + (n−1) × 3", font=FONT, font_size=22,
                     color=GOLD)
        lab_l.next_to(ax_l, UP, buff=0.15)
        lab_r = Text("等比：b = 1 × 2ⁿ⁻¹", font=FONT, font_size=22,
                     color=TEAL)
        lab_r.next_to(ax_r, UP, buff=0.15)
        xlab_l = Text("n", font=FONT, font_size=20, color=GREY_B)
        xlab_l.next_to(ax_l.x_axis, RIGHT, buff=0.1)
        xlab_r = Text("n", font=FONT, font_size=20, color=GREY_B)
        xlab_r.next_to(ax_r.x_axis, RIGHT, buff=0.1)
        self.play(Create(ax_l), Create(ax_r), FadeIn(lab_l),
                  FadeIn(lab_r), FadeIn(xlab_l), FadeIn(xlab_r),
                  run_time=1.4)
        self.wait(0.8)

        # ===== 散点逐项规定 =====
        a_terms = [2 + 3 * (n - 1) for n in range(1, N_TERMS + 1)]
        b_terms = [2 ** (n - 1) for n in range(1, N_TERMS + 1)]
        dots_l = VGroup()
        dots_r = VGroup()
        for i, (a, b) in enumerate(zip(a_terms, b_terms)):
            n = i + 1
            d1 = Dot(ax_l.c2p(n, a), color=GOLD, radius=0.09)
            d2 = Dot(ax_r.c2p(n, b), color=TEAL, radius=0.09)
            t1 = Text(str(a), font=FONT, font_size=18, color=GOLD)
            t1.next_to(d1, UP, buff=0.06)
            t2 = Text(str(b), font=FONT, font_size=18, color=TEAL)
            t2.next_to(d2, UP, buff=0.06)
            self.set_note(
                "第 {} 项：等差 {}（+3），等比 {}（×2）".format(n, a, b))
            self.play(FadeIn(d1, scale=0.4), FadeIn(t1),
                      FadeIn(d2, scale=0.4), FadeIn(t2), run_time=0.9)
            dots_l.add(d1, t1)
            dots_r.add(d2, t2)
            self.wait(0.35)
        self.wait(0.8)

        # ===== 等差：散点连成直线 =====
        self.set_note("等差的点，全踩在一条直线上")
        line_l = DashedLine(ax_l.c2p(0.4, 2 + 3 * (0.4 - 1)),
                            ax_l.c2p(6.8, 2 + 3 * (6.8 - 1)),
                            color=GOLD, stroke_width=3, dash_length=0.15)
        self.play(Create(line_l), run_time=1.6)
        self.wait(1.0)
        lab_lin = Text("一次函数 y = 3x − 1 的整数点", font=FONT,
                       font_size=20, color=GOLD)
        lab_lin.move_to(ax_l.c2p(4.9, 4.0))
        self.play(FadeIn(lab_lin), run_time=0.7)
        self.set_note("均匀增长 = 直线——等差数列是「掰碎了的一次函数」")
        self.wait(2.2)

        # ===== 等比：散点连成指数曲线 =====
        self.set_note("等比的点，全踩在一条指数曲线上")
        curve_r = ax_r.plot(lambda x: 2 ** (x - 1),
                            x_range=[0.4, 6.6], color=TEAL,
                            stroke_width=3)
        curve_r.set_stroke(opacity=0.85)
        dash_r = DashedVMobject(curve_r, num_dashes=60)
        self.play(Create(dash_r), run_time=1.8)
        self.wait(1.0)
        lab_exp = Text("指数函数 y = 2ˣ⁻¹ 的整数点", font=FONT,
                       font_size=20, color=TEAL)
        lab_exp.move_to(ax_r.c2p(2.4, 28))
        self.play(FadeIn(lab_exp), run_time=0.7)
        self.set_note("翻倍增长 = 指数曲线——第 6 项已经窜到 32")
        self.wait(2.2)

        # ===== 结案对照 =====
        self.set_note("同样 6 项：等差爬到 17，等比冲到 32")
        box_l = SurroundingRectangle(dots_l, color=GOLD, buff=0.2,
                                     stroke_width=2)
        box_r = SurroundingRectangle(dots_r, color=TEAL, buff=0.2,
                                     stroke_width=2)
        self.play(Create(box_l), run_time=0.8)
        self.play(ReplacementTransform(box_l, box_r), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(box_r), run_time=0.5)
        self.set_note("数列是定义在正整数上的函数——散点背后都有一条曲线")
        self.wait(2.4)
        self.set_note("棋盘上放麦粒：第 64 格的等比，是天文数字")
        self.wait(2.6)
