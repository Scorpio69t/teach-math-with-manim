from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

R = 1.3                              # 单位圆屏幕半径
C_CIRCLE = np.array([1.3, 0.2, 0])   # 圆心
TAPE_X = -3.3                        # 卷尺所在竖线
TAPE_Y0 = -1.5                       # 卷尺下端


class EulerWrap(Scene):
    """卷尺缠单位圆：长度 θ 的卷尺 = 弧长 θ 的金弧 = 转角 θ。
    θ 扫到 π，动点正中 -1——e^(iπ) + 1 = 0 只是「走了半圈」。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("e^(iπ) + 1 = 0 凭什么？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("先别背公式。准备一根卷尺和一个单位圆",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 单位圆 =====
        circle = Circle(radius=R, color=GREY_B, stroke_width=2.5)
        circle.move_to(C_CIRCLE)
        center_dot = Dot(C_CIRCLE, radius=0.05, color=GREY_B)
        lab_1 = Text("1", font=FONT, font_size=24, color=C_TEXT)
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

        th_lab = always_redraw(lambda: Text(
            f"θ = {th.get_value():.2f}", font=FONT, font_size=24,
            color=GOLD).move_to(
                [TAPE_X + 1.05, TAPE_Y0 + th.get_value() * R + 0.1, 0]))

        # 挂 updater 的对象一律 add 入场，不进 FadeIn
        self.add(tape, tape_tip, arc, mover, spoke, th_lab)

        # ===== 走到 π/2 =====
        self.set_note("卷尺往上长，圆弧同步爬——弧长就是转角")
        self.play(th.animate.set_value(PI / 2), run_time=3.5,
                  rate_func=linear)
        lab_i = Text("i", font=FONT, font_size=24, color=TEAL)
        lab_i.move_to(C_CIRCLE + [0, R + 0.38, 0])
        self.play(FadeIn(lab_i), run_time=0.5)
        self.set_note("θ = π/2：四分之一圈，这里是 i")
        self.wait(1.8)

        # ===== 走到 π：高潮 =====
        self.set_note("继续。卷尺长度 π——圆上正好半圈")
        self.play(th.animate.set_value(PI - 0.02), run_time=3.5,
                  rate_func=linear)
        self.play(th.animate.set_value(PI), run_time=0.3)

        lab_m1 = Text("-1", font=FONT, font_size=26, weight=BOLD,
                      color=ORANGE)
        lab_m1.move_to(C_CIRCLE + [-R - 0.45, 0, 0])
        self.play(FadeIn(lab_m1),
                  Flash(C_CIRCLE + [-R, 0, 0], color=ORANGE,
                        flash_radius=0.5),
                  run_time=1.0)
        self.set_note("正中 -1！「e 的 iπ 次方」说的只是：转半圈")
        self.wait(2.0)

        # ===== 公式亮相 =====
        f1 = Text("e^(iπ) = -1", font=FONT, font_size=34,
                  weight=BOLD, color=GOLD)
        f1.move_to([1.3, 2.7, 0])
        self.play(FadeIn(f1, shift=UP * 0.3), run_time=0.9)
        self.wait(1.6)
        f2 = Text("e^(iπ) + 1 = 0", font=FONT, font_size=36,
                  weight=BOLD, color=GOLD)
        f2.move_to([1.3, 2.7, 0])
        self.play(Transform(f1, f2), run_time=0.9)
        self.set_note("最美的公式，只是「走半圈」的另一写法")
        self.wait(2.6)

        # ===== 一般形式收尾 =====
        f3 = Text("e^(iθ) = cos θ + i sin θ",
                  font=FONT, font_size=26, color=C_TEXT)
        f3.move_to([1.3, 2.0, 0])
        self.play(FadeIn(f3, shift=UP * 0.2), run_time=0.9)
        self.set_note("θ 角对应的坐标，就是欧拉公式的全部内容")
        self.wait(3.0)
