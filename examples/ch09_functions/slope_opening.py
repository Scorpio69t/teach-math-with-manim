from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）


class SlopeAndOpening(Scene):
    """斜率与开口：拖一拖 k 和 a，函数的性格全在脸上。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def make_panel(self, attr, tracker):
        """钉屏数值面板：标签在左、数字钉右缘，become 原地刷新。"""
        num = Text(f"{tracker.get_value():.2f}", font=FONT,
                   font_size=36, color=GOLD)
        num.to_corner(UR, buff=0.6)
        lab = MathTex(f"{attr}=", font_size=40)
        lab.next_to(num, LEFT, buff=0.12)
        num.add_updater(lambda d: d.become(
            Text(f"{tracker.get_value():.2f}", font=FONT,
                 font_size=36, color=GOLD).to_corner(UR, buff=0.6)))
        return lab, num

    def construct(self):
        title = Text("斜率与开口：参数的性格", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("y = kx：k 管方向和陡峭", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        axes = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1],
                    x_length=9, y_length=6.2,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        self.add(title, self.note)
        self.play(Create(axes), run_time=1.2)

        # 第一幕：直线 y = kx，k 是遥控器
        k = ValueTracker(1)
        line = always_redraw(lambda: axes.plot(
            lambda x: k.get_value() * x, x_range=[-5, 5],
            color=TEAL, stroke_width=4))
        # 斜率三角：横走 1 竖走 k——"斜率"两个字的几何身份证
        tri = always_redraw(lambda: VGroup(
            DashedLine(axes.c2p(1, k.get_value()), axes.c2p(2, k.get_value()),
                       color=GOLD),
            DashedLine(axes.c2p(2, k.get_value()),
                       axes.c2p(2, 2 * k.get_value()), color=GOLD)))
        lab_k, num_k = self.make_panel("k", k)
        self.add(line, tri, lab_k, num_k)
        self.wait(1)

        self.set_note("k 变大：同样的横走 1，竖得更高——更陡")
        self.play(k.animate.set_value(2.5), run_time=3, rate_func=linear)
        self.wait(1)
        self.set_note("k 变负：从左到右，一路上下坡反过来了")
        self.play(k.animate.set_value(-1.2), run_time=3, rate_func=linear)
        self.wait(1.2)

        # 第二幕：抛物线 y = ax²，a 是遥控器；y=x² 留作灰色参照
        self.set_note("换主角：y = ax²，a 管开口")
        num_k.clear_updaters()
        self.play(FadeOut(line), FadeOut(tri), FadeOut(lab_k),
                  FadeOut(num_k), run_time=1)
        ghost = axes.plot(lambda x: x**2, x_range=[-2.2, 2.2],
                          color=GREY_B, stroke_width=2)
        a = ValueTracker(1)
        # a 过 0 附近时 |a| 趋零，显示窗口必须钳住，避免采样区间过宽
        para = always_redraw(lambda: axes.plot(
            lambda x: a.get_value() * x**2,
            x_range=[-min(np.sqrt(5 / max(abs(a.get_value()), 0.25)), 2.4),
                     min(np.sqrt(5 / max(abs(a.get_value()), 0.25)), 2.4)],
            color=GOLD, stroke_width=4))
        lab_a, num_a = self.make_panel("a", a)
        self.play(FadeIn(ghost), run_time=0.8)
        self.add(para, lab_a, num_a)
        self.wait(1)

        self.set_note("a 变大：开口收窄——|a| 是胖瘦开关")
        self.play(a.animate.set_value(3), run_time=3, rate_func=linear)
        self.wait(1)
        self.set_note("a 变负：抛物线整个翻过来，顶点成了最高点")
        self.play(a.animate.set_value(-0.5), run_time=3.5,
                  rate_func=linear)
        self.wait(1.5)
