from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（AGENTS.md §6.1 铁律）


class GrowthRace(Scene):
    """指数 vs 线性：一场起跑悬殊、结局反转的赛跑。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("指数爆炸：起跑落后，结局碾压", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("线性 100x（青） vs 指数 2^x（金）", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        axes = Axes(x_range=[0, 12, 1], y_range=[0, 4200, 1000],
                    x_length=10, y_length=5.6,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to(ORIGIN + UP * 0.2)
        self.add(title, self.note)
        self.play(Create(axes), run_time=1.2)

        f_lin = lambda x: 100 * x
        f_exp = lambda x: 2**x
        x = ValueTracker(0.5)   # 遥控器：赛跑到第 x 秒

        # 两条曲线只画到当前 x——跑道随赛程生长
        lin_curve = always_redraw(lambda: axes.plot(
            f_lin, x_range=[0.01, x.get_value()], color=TEAL,
            stroke_width=4))
        exp_curve = always_redraw(lambda: axes.plot(
            f_exp, x_range=[0.01, x.get_value()], color=GOLD,
            stroke_width=4))
        lin_dot = always_redraw(lambda: Dot(
            axes.c2p(x.get_value(), f_lin(x.get_value())), color=TEAL,
            radius=0.09))
        exp_dot = always_redraw(lambda: Dot(
            axes.c2p(x.get_value(), f_exp(x.get_value())), color=GOLD,
            radius=0.09))
        # 数值面板：线性在左、指数在右，become 原地刷新
        lin_num = always_redraw(lambda: Text(
            f"{f_lin(x.get_value()):.0f}", font=FONT, font_size=30,
            color=TEAL).next_to(axes.c2p(10.5, 3400), UP))
        exp_num = always_redraw(lambda: Text(
            f"{f_exp(x.get_value()):.0f}", font=FONT, font_size=30,
            color=GOLD).next_to(axes.c2p(10.5, 3400), DOWN))
        self.add(lin_curve, exp_curve, lin_dot, exp_dot, lin_num, exp_num)
        self.wait(1)

        self.set_note("发令枪响：线性一上来就冲在前面")
        self.play(x.animate.set_value(5), run_time=3, rate_func=linear)
        self.set_note("x=5：线性 500，指数才 32——别急")
        self.wait(1.2)

        self.set_note("继续跑：注意指数的脚印在翻倍")
        self.play(x.animate.set_value(10), run_time=3, rate_func=linear)
        self.set_note("x=10：追平了！指数每过 1 步就翻一倍")
        cross = Dot(axes.c2p(10, 1024), color=RED, radius=0.11)
        self.play(Flash(cross, color=RED), FadeIn(cross), run_time=1)
        self.wait(1)

        self.set_note("再跑两步，结局没有悬念了")
        self.play(x.animate.set_value(12), run_time=2.5, rate_func=linear)
        self.set_note("x=12：4096 对 1200——指数的胜利才刚开始")
        self.wait(1.5)
