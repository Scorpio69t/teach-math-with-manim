from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

C0 = LEFT * 3.6 + UP * 0.1        # 单位圆圆心
R = 1.8                           # 单位圆半径（场景单位）
OX, OY = -0.6, 0.1                # 波形图原点
XSCALE = 0.72                     # 1 弧度对应的波形横坐标长度（右侧留给面板）
T_END = 2 * np.pi                 # 转一整圈


class CircleToWave(Scene):
    """单位圆转一圈，正弦波画一条：角的高度，就是波的纵坐标。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def pinned_row(self, label, getter, row_anchor, color=GOLD,
                   fmt="{:.2f}"):
        """面板一行：标签钉右缘、数值钉左缘。"""
        lab = Text(label, font=FONT, font_size=26, color=C_TEXT)
        lab.move_to(row_anchor, aligned_edge=RIGHT)
        num_anchor = row_anchor + RIGHT * 0.25
        num = Text(fmt.format(getter()), font=FONT, font_size=26,
                   color=color)
        num.move_to(num_anchor, aligned_edge=LEFT)
        num.add_updater(lambda d: d.become(
            Text(fmt.format(getter()), font=FONT, font_size=26,
                 color=color).move_to(num_anchor, aligned_edge=LEFT)))
        return VGroup(lab, num)

    def construct(self):
        th = ValueTracker(0.0)      # 转角（弧度）

        def p_pos():
            a = th.get_value()
            return C0 + R * np.array([np.cos(a), np.sin(a), 0])

        def wave_x(a):
            return OX + a * XSCALE

        title = Text("单位圆与正弦波：圆周运动的身高曲线", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("点 P 从 (1, 0) 出发，沿单位圆逆时针旋转",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 左侧：单位圆 =====
        circle = Circle(radius=R, color=GREY_B, stroke_width=3)
        circle.move_to(C0)
        axes_c = VGroup(
            Line(C0 + LEFT * (R + 0.4), C0 + RIGHT * (R + 0.4),
                 color=GREY, stroke_width=1.5),
            Line(C0 + DOWN * (R + 0.4), C0 + UP * (R + 0.4),
                 color=GREY, stroke_width=1.5))
        lab_1 = Text("1", font=FONT, font_size=22, color=GREY_B)
        lab_1.next_to(C0 + RIGHT * R, DOWN, buff=0.08)
        self.play(Create(circle), Create(axes_c), FadeIn(lab_1),
                  run_time=1.2)

        # ===== 右侧：波形坐标系 =====
        axes_w = VGroup(
            Line([OX - 0.3, OY, 0], [wave_x(T_END) + 0.5, OY, 0],
                 color=GREY, stroke_width=1.5),
            Line([OX, OY - R - 0.4, 0], [OX, OY + R + 0.4, 0],
                 color=GREY, stroke_width=1.5))
        # 横轴刻度：π/2、π、3π/2、2π（横轴就是弧长）
        ticks = VGroup()
        for a, name in [(PI / 2, "π/2"), (PI, "π"),
                        (3 * PI / 2, "3π/2"), (2 * PI, "2π")]:
            tick = Line([wave_x(a), OY - 0.08, 0],
                        [wave_x(a), OY + 0.08, 0],
                        color=GREY_B, stroke_width=2)
            tlab = Text(name, font=FONT, font_size=20, color=GREY_B)
            tlab.next_to(tick, DOWN, buff=0.06)
            ticks.add(tick, tlab)
        lab_axis = Text("横轴 = 转过的弧长（弧度）", font=FONT,
                        font_size=20, color=GREY_B)
        lab_axis.move_to([wave_x(PI) + 1.2, OY - R - 0.55, 0])
        self.play(Create(axes_w), FadeIn(ticks), FadeIn(lab_axis),
                  run_time=1.0)
        self.set_note("横轴不用角度而用弧长：弧度制让角变成实数")
        self.wait(1.6)

        # ===== 主角：点 P、正弦线、走过的弧 =====
        dot_p = always_redraw(lambda: Dot(p_pos(), color=GOLD,
                                          radius=0.08))
        sine_line = always_redraw(lambda: Line(
            [p_pos()[0], C0[1], 0], p_pos(),
            color=GOLD, stroke_width=5))
        radius_line = always_redraw(lambda: Line(
            C0, p_pos(), color=TEAL, stroke_width=2.5))
        arc_done = always_redraw(lambda: Arc(
            radius=R, start_angle=0,
            angle=th.get_value() % (2 * PI),
            arc_center=C0, color=TEAL, stroke_width=5)
            if th.get_value() % (2 * PI) > 0.02
            else VMobject())

        self.play(FadeIn(dot_p), Create(radius_line),
                  Create(sine_line), run_time=0.8)
        self.add(arc_done)

        # 连接器：P 的高度引到波形图
        connector = always_redraw(lambda: DashedLine(
            p_pos(), [wave_x(th.get_value()), p_pos()[1], 0],
            color=GREY_B, stroke_width=1.5, dash_length=0.12))
        wave_dot = always_redraw(lambda: Dot(
            [wave_x(th.get_value()), p_pos()[1], 0],
            color=RED, radius=0.07))

        # ===== 数值面板（右上角，波形右侧留空带） =====
        px = 4.5
        p_title = Text("实时读数", font=FONT, font_size=24,
                       weight=BOLD, color=C_TEXT)
        p_title.move_to([4.75, 3.0, 0], aligned_edge=LEFT)

        def sin_clean():
            v = np.sin(th.get_value())
            return 0.0 if abs(v) < 0.005 else v

        row_deg = self.pinned_row(
            "角度 θ =", lambda: np.degrees(th.get_value()) % 360,
            np.array([px, 2.5, 0]), fmt="{:.0f}°")
        row_rad = self.pinned_row(
            "弧度 =", lambda: th.get_value() % (2 * PI),
            np.array([px, 2.0, 0]), color=C_TEXT)
        row_sin = self.pinned_row(
            "sin θ =", sin_clean,
            np.array([px, 1.5, 0]), color=GOLD)
        self.play(FadeIn(p_title), FadeIn(row_deg), FadeIn(row_rad),
                  FadeIn(row_sin), run_time=0.8)
        self.wait(0.6)

        # ===== 转圈画波 =====
        self.set_note("金色线段是 P 的高度——它就叫 sin θ")
        traced = TracedPath(
            lambda: np.array([wave_x(th.get_value()), p_pos()[1], 0]),
            stroke_color=GOLD, stroke_width=4)
        self.add(traced, connector, wave_dot)

        marks = [(PI / 2, "到达最高点：sin θ = 1", 1.2),
                 (PI, "回到水平线：sin θ = 0", 1.2),
                 (PI + 0.24, "进入第三象限：sin θ < 0", 0.8),
                 (3 * PI / 2, "沉入谷底：sin θ = −1", 1.2),
                 (2 * PI - 0.001, "走完一整圈：波也画完一整条", 0.8)]
        for target, msg, hold in marks:
            self.play(th.animate.set_value(target), run_time=2.6,
                      rate_func=linear)
            self.set_note(msg)
            self.wait(hold)
        self.remove(connector)

        # ===== 结案 =====
        self.set_note("点 P 的高度随角起伏——这就是 y = sin x 的来历")
        self.play(Indicate(traced, color=GOLD), run_time=1.2)
        self.wait(1.0)
        self.set_note("圆管旋转，波管形状——一对形影不离的双胞胎")
        self.wait(2.2)
