from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

R = 1.3                              # 单位圆屏幕半径
C_CIRCLE = np.array([1.3, 0.2, 0])   # 圆心
TAPE_X = -3.3                        # 卷尺所在竖线
TAPE_Y0 = -1.5                       # 卷尺下端


def zh(s, size=26, color=C_TEXT, bold=False):
    """中文文本（公式一律用 MathTex，不进这里）。"""
    return Text(s, font=FONT, font_size=size,
                weight=BOLD if bold else NORMAL, color=color)


def mix(parts, size=26, color=C_TEXT, math_scale=0.9):
    """中文 + 公式混排：parts 交错给出 ("t", 文本) / ("m", LaTeX)。"""
    group = VGroup()
    for kind, s in parts:
        if kind == "t":
            group.add(zh(s, size, color))
        else:
            group.add(MathTex(s, color=color).scale(math_scale))
    return group.arrange(RIGHT, buff=0.10)


class EulerWrap(Scene):
    """卷尺缠单位圆：长度 θ 的卷尺 = 弧长 θ 的金弧 = 转角 θ。
    θ 扫到 π，动点正中 -1——e^(iπ) + 1 = 0 只是「走了半圈」。"""

    def set_note(self, msg):
        if isinstance(msg, str):          # 纯中文注释条
            self.note.become(zh(msg).move_to(NOTE_POS))
        else:                             # 中文 + 公式混排
            self.note.become(mix(msg).move_to(NOTE_POS))

    def construct(self):
        title = mix([("m", "e^{i\\pi} + 1 = 0"),
                     ("t", " 凭什么？")], size=32, math_scale=1.0)
        title[0].set_color(C_TEXT)
        for part in title[1:]:
            part.set_color(C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = zh("先别背公式。准备一根卷尺和一个单位圆")
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 单位圆 =====
        circle = Circle(radius=R, color=GREY_B, stroke_width=2.5)
        circle.move_to(C_CIRCLE)
        center_dot = Dot(C_CIRCLE, radius=0.05, color=GREY_B)
        lab_1 = zh("1", 24)
        lab_1.move_to(C_CIRCLE + [R + 0.35, 0, 0])
        self.play(Create(circle), FadeIn(center_dot), FadeIn(lab_1),
                  run_time=1.0)

        # ===== 卷尺底座刻度 =====
        tape_base = Line([TAPE_X, TAPE_Y0, 0],
                         [TAPE_X, TAPE_Y0 + PI * R + 0.2, 0],
                         color=GREY_B, stroke_width=1.5)
        self.play(Create(tape_base), run_time=0.6)
        self.set_note("规则只有一条：卷尺多长，圆上的金弧就多长")
        self.wait(1.6)

        # ===== 同步生长：θ 驱动 =====
        th = ValueTracker(0.001)

        tape = always_redraw(lambda: Line(
            [TAPE_X, TAPE_Y0, 0],
            [TAPE_X, TAPE_Y0 + th.get_value() * R, 0],
            color=GOLD, stroke_width=8))
        tape_tip = always_redraw(lambda: Dot(
            [TAPE_X, TAPE_Y0 + th.get_value() * R, 0],
            radius=0.08, color=GOLD))

        arc = always_redraw(lambda: Arc(
            radius=R, start_angle=0, angle=th.get_value(),
            arc_center=C_CIRCLE, color=GOLD, stroke_width=6))
        mover = always_redraw(lambda: Dot(
            C_CIRCLE + R * np.array([np.cos(th.get_value()),
                                     np.sin(th.get_value()), 0]),
            radius=0.09, color=GOLD))
        spoke = always_redraw(lambda: Line(
            C_CIRCLE,
            C_CIRCLE + R * np.array([np.cos(th.get_value()),
                                     np.sin(th.get_value()), 0]),
            color=GREY_B, stroke_width=1.5))

        # θ 读数：MathTex 符号 + DecimalNumber 数字（逐帧只重排数字，不编译 LaTeX）
        th_num = DecimalNumber(0.00, num_decimal_places=2, color=GOLD)
        th_num.scale(0.85)
        th_sym = MathTex(r"\theta =", color=GOLD).scale(0.85)
        th_lab = VGroup(th_sym, th_num).arrange(RIGHT, buff=0.10)
        th_lab.add_updater(lambda m: (
            th_num.set_value(th.get_value()),
            m.move_to([TAPE_X + 1.05,
                       TAPE_Y0 + th.get_value() * R + 0.1, 0])))

        # 挂 updater 的对象一律 add 入场，不进 FadeIn
        self.add(tape, tape_tip, arc, mover, spoke, th_lab)

        # ===== 走到 π/2 =====
        self.set_note("卷尺往上长，圆弧同步爬——弧长就是转角")
        self.play(th.animate.set_value(PI / 2), run_time=3.5,
                  rate_func=linear)
        lab_i = zh("i", 24, TEAL)
        lab_i.move_to(C_CIRCLE + [0, R + 0.38, 0])
        self.play(FadeIn(lab_i), run_time=0.5)
        self.set_note([("m", "\\theta = \\pi/2"),
                       ("t", "：四分之一圈，这里是 i")])
        self.wait(1.8)

        # ===== 走到 π：高潮 =====
        self.set_note("继续。卷尺长度 π——圆上正好半圈")
        self.play(th.animate.set_value(PI - 0.02), run_time=3.5,
                  rate_func=linear)
        self.play(th.animate.set_value(PI), run_time=0.3)

        lab_m1 = zh("-1", 26, ORANGE, bold=True)
        lab_m1.move_to(C_CIRCLE + [-R - 0.45, 0, 0])
        self.play(FadeIn(lab_m1),
                  Flash(C_CIRCLE + [-R, 0, 0], color=ORANGE,
                        flash_radius=0.5),
                  run_time=1.0)
        self.set_note("正中 -1！「e 的 iπ 次方」说的只是：转半圈")
        self.wait(2.0)

        # ===== 公式亮相 =====
        f1 = MathTex(r"e^{i\pi} = -1", color=GOLD).scale(1.15)
        f1.move_to([1.3, 2.7, 0])
        self.play(FadeIn(f1, shift=UP * 0.3), run_time=0.9)
        self.wait(1.6)
        f2 = MathTex(r"e^{i\pi} + 1 = 0", color=GOLD).scale(1.15)
        f2.move_to([1.3, 2.7, 0])
        self.play(Transform(f1, f2), run_time=0.9)
        self.set_note("最美的公式，只是「走半圈」的另一写法")
        self.wait(2.6)

        # ===== 一般形式收尾 =====
        f3 = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta",
                     color=C_TEXT).scale(0.95)
        f3.move_to([1.3, 2.0, 0])
        self.play(FadeIn(f3, shift=UP * 0.2), run_time=0.9)
        self.set_note("θ 角对应的坐标，就是欧拉公式的全部内容")
        self.wait(3.0)
