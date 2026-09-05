from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）
PLOT_Y_MIN = -4.0         # 曲线安全区：给上下方标题、注释条留出净空
PLOT_Y_MAX = 5.0
PLOT_X_HALF = 2.4


def visible_half_width(a_value, k_value):
    """计算抛物线在安全纵向范围内可见的横向半宽。"""
    if abs(a_value) < 0.05:
        return PLOT_X_HALF
    vertical_room = (PLOT_Y_MAX - k_value if a_value > 0
                     else k_value - PLOT_Y_MIN)
    return min(np.sqrt(max(vertical_room / abs(a_value), 0)), PLOT_X_HALF)


class TransformStudio(Scene):
    """函数变换工作室：y = a(x−h)² + k，三个滑杆看透平移伸缩翻转。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def make_live_curve(self, axes, a, h, k):
        a_value = a.get_value()
        h_value = h.get_value()
        k_value = k.get_value()
        half_width = visible_half_width(a_value, k_value)
        return axes.plot(
            lambda x: a_value * (x - h_value)**2 + k_value,
            x_range=[h_value - half_width, h_value + half_width],
            color=GOLD, stroke_width=4)

    def construct(self):
        title = Text("y = a(x − h)² + k：三个滑杆", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("灰色是 y = x²，金色是变换后的它", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        axes = Axes(x_range=[-6, 6, 1], y_range=[-4, 6, 1],
                    x_length=10, y_length=6,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to(ORIGIN + UP * 0.1)
        self.add(title, self.note)
        self.play(Create(axes), run_time=1.2)

        # 参照系：y = x² 灰影常驻，变换前后对比全靠它
        ghost_half_width = np.sqrt(PLOT_Y_MAX)
        ghost = axes.plot(lambda x: x**2,
                          x_range=[-ghost_half_width, ghost_half_width],
                          color=GREY_B, stroke_width=2)
        a, h, k = ValueTracker(1), ValueTracker(0), ValueTracker(0)
        live = always_redraw(lambda: self.make_live_curve(axes, a, h, k))
        # 顶点：抛物线的"心脏"，坐标 (h, k) 实时可读
        vertex = always_redraw(lambda: Dot(
            axes.c2p(h.get_value(), k.get_value()), color=RED, radius=0.09))
        panel = always_redraw(lambda: Text(
            f"a={a.get_value():.1f}  h={h.get_value():.1f}  "
            f"k={k.get_value():.1f}",
            font=FONT, font_size=30, color=C_TEXT)
            .to_corner(UR, buff=0.6))
        self.play(FadeIn(ghost), run_time=0.8)
        self.add(live, vertex, panel)
        self.wait(1)

        self.set_note("k +2：整体抬升 2 格——k 管上下，最老实")
        self.play(k.animate.set_value(2), run_time=2.5, rate_func=linear)
        self.wait(1)

        self.set_note("h +3：括号里是 x−3，图却向右走——左加右减")
        self.play(h.animate.set_value(3), run_time=3, rate_func=linear)
        self.wait(1.2)

        self.set_note("a ×2：开口收窄，形状变瘦——|a| 管胖瘦")
        self.play(a.animate.set_value(2), run_time=2.5, rate_func=linear)
        self.wait(1)

        self.set_note("a 变 −0.5：翻转 + 变宽，顶点从谷底变峰顶")
        self.play(a.animate.set_value(-0.5), run_time=3.5,
                  rate_func=linear)
        self.wait(1.5)
