from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.3


class ParabolaSlider(Scene):
    """y = a·x²：a 连续变化，开口、数值、注释全部实时跟随。"""

    def set_note(self, msg):
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.play(Transform(self.note, new, run_time=0.4))

    def construct(self):
        title = Text("a 越大，开口越窄？", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("盯着抛物线，a 要动了", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        axes = Axes(x_range=[-4, 4, 1], y_range=[-1, 8, 1],
                    x_length=7, y_length=4.5,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to(UP * 0.3)

        a = ValueTracker(0.25)   # 遥控器：参数 a

        # 抛物线：每帧按当前 a 重画（always_redraw）
        curve = always_redraw(
            lambda: axes.plot(lambda x: a.get_value() * x**2,
                              x_range=[-4, 4, 0.2], color=GOLD,
                              stroke_width=5)
        )

        # 数值面板：a = 当前值（updater 每帧读数）
        panel = VGroup(
            MathTex("a=", font_size=44),
            DecimalNumber(a.get_value(), num_decimal_places=2,
                          font_size=44, color=GOLD),
        ).arrange(RIGHT, buff=0.12)
        panel.to_corner(UR, buff=0.6)
        panel[1].add_updater(lambda d: d.set_value(a.get_value()))

        self.play(Create(axes), run_time=1.2)
        self.add(curve, panel)
        self.wait(1)

        # 行程一：a 从 0.25 到 2.5——开口连续收窄
        self.set_note("a 连续变大——看开口怎么收窄")
        self.play(a.animate.set_value(2.5), run_time=4)
        self.wait(1.5)

        # 行程二：收回来——开口张开复位
        self.set_note("a 收回去——开口重新张开")
        self.play(a.animate.set_value(0.25), run_time=3)
        self.wait(1.5)

        self.set_note("PPT 给你三张图，这里给你整个变化过程")
        self.wait(2)
