"""第 17 章案例：均值不等式的半圆模型——半径压弦高（代码清单 17-2）

渲染：manim -pqh amgm_semicircle.py AmGmSemicircle
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [4.8, 2.2, 0]       # a / b 读数
R2_POS = [4.8, 1.6, 0]       # 半径读数
R3_POS = [4.8, 1.0, 0]       # 弦高读数
VERDICT_POS = [0, -2.75, 0]

SCALE = 0.62                 # 1 个数据单位 = 0.62 屏幕单位
TOTAL = 10                   # a + b 恒为 10
BASE_Y = -0.4                # 直径所在高度


def cx(a):
    """分点 C 的屏幕 x 坐标：圆心在原点正上方 BASE_Y 处。"""
    return (a - TOTAL / 2) * SCALE


class AmGmSemicircle(Scene):
    """直径 a+b 的半圆：半径 (a+b)/2 是斜边，弦高 √ab 是直角边；
    分点滑动，弦高追着半径长，a = b 时恰好贴上——等号成立。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("(a+b)/2 和 √ab，谁大？——一个圆讲完", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("把 a 和 b 首尾接成一条直径，看半圆里藏着什么",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        center = [0, BASE_Y, 0]
        R = TOTAL / 2 * SCALE  # 半圆半径（屏幕单位）

        # ===== 直径与分点 =====
        seg = Line(center + LEFT * R, center + RIGHT * R,
                   color=C_TEXT, stroke_width=3)
        a_val = ValueTracker(6.0)  # 初始 a = 6，b = 4

        c_dot = always_redraw(lambda: Dot(
            [cx(a_val.get_value()), BASE_Y, 0], radius=0.08, color=GOLD))
        a_lab = always_redraw(lambda: Text(
            f"a = {a_val.get_value():.1f}", font=FONT, font_size=22,
            color=GOLD).move_to(
                [(cx(a_val.get_value()) - R) / 2, BASE_Y - 0.42, 0]))
        b_lab = always_redraw(lambda: Text(
            f"b = {TOTAL - a_val.get_value():.1f}", font=FONT,
            font_size=22, color=GOLD).move_to(
                [(cx(a_val.get_value()) + R) / 2, BASE_Y - 0.42, 0]))
        self.play(Create(seg), run_time=1.0)
        self.play(FadeIn(c_dot), FadeIn(a_lab), FadeIn(b_lab),
                  run_time=0.8)
        self.set_note("左段是 a，右段是 b——两数之和被钉死成直径")
        self.wait(1.8)

        # ===== 半圆与半径 =====
        arc = Arc(radius=R, start_angle=0, angle=PI,
                  arc_center=center, color=TEAL, stroke_width=4)
        o_dot = Dot(center, radius=0.06, color=C_TEXT)
        o_lab = Text("O", font=FONT, font_size=22, color=C_TEXT)
        o_lab.move_to(center + LEFT * 0.35 + DOWN * 0.3)
        radius = Line(center, center + UP * R, color=GOLD, stroke_width=4)
        t_dot = Dot(center + UP * R, radius=0.07, color=GOLD)
        self.play(Create(arc), FadeIn(o_dot), FadeIn(o_lab), run_time=1.2)
        self.play(Create(radius), FadeIn(t_dot), run_time=0.9)
        self.set_note("半径 OT 长 (a+b)/2——它就是 a 和 b 的算术平均")
        self.wait(2.0)

        # ===== 弦高：垂线交半圆 =====
        def chord_top():
            a = a_val.get_value()
            h = np.sqrt(a * (TOTAL - a)) * SCALE
            return [cx(a), BASE_Y + h, 0]

        chord = always_redraw(lambda: Line(
            [cx(a_val.get_value()), BASE_Y, 0], chord_top(),
            color=RED, stroke_width=4))
        d_dot = always_redraw(lambda: Dot(chord_top(), radius=0.07,
                                          color=RED))
        hyp = always_redraw(lambda: DashedLine(
            center, chord_top(), color=GREY_B, stroke_width=2))
        self.play(FadeIn(chord), FadeIn(d_dot), run_time=0.9)
        self.play(Create(hyp), run_time=0.7)
        self.set_note("过 C 作垂线交半圆于 D——射影定理：CD = √ab")
        self.wait(2.2)

        # ===== 读数面板 =====
        r1 = always_redraw(lambda: Text(
            f"a = {a_val.get_value():.1f}　b = "
            f"{TOTAL - a_val.get_value():.1f}",
            font=FONT, font_size=24, color=C_TEXT).move_to(R1_POS))
        r2 = Text(f"(a+b)/2 = {TOTAL / 2:.3f}（半径）",
                  font=FONT, font_size=24, color=GOLD)
        r2.move_to(R2_POS)
        r3 = always_redraw(lambda: Text(
            f"√ab = {np.sqrt(a_val.get_value() * (TOTAL - a_val.get_value())):.3f}（弦高）",
            font=FONT, font_size=24, color=RED).move_to(R3_POS))
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.8)
        self.set_note("OD 也是半径——直角三角形 OCD 里，斜边永远压得住直角边")
        self.wait(2.4)

        # ===== 滑动节拍：弦高追半径 =====
        self.play(a_val.animate.set_value(8.5), run_time=1.4,
                  rate_func=linear)
        self.set_note("a 拉大差距：弦高立刻矮下去")
        self.wait(1.4)
        self.play(a_val.animate.set_value(5.0), run_time=1.8,
                  rate_func=linear)
        eq = Text("a = b：弦高 = 半径，取等！", font=FONT,
                  font_size=24, weight=BOLD, color=GREEN)
        eq.move_to([4.5, 0.3, 0])
        self.play(FadeIn(eq, scale=0.9), run_time=0.7)
        self.play(Indicate(chord, color=GREEN), Indicate(radius, color=GREEN),
                  run_time=0.9)
        self.set_note("C 滑到圆心：弦高恰好贴上半径——两数相等时取等")
        self.wait(2.2)
        self.play(FadeOut(eq), run_time=0.4)
        self.play(a_val.animate.set_value(2.0), run_time=1.6,
                  rate_func=linear)
        self.set_note("滑向另一头，弦高又矮回去——5 是它的天花板")
        self.wait(1.6)

        # ===== 结案 =====
        self.play(a_val.animate.set_value(6.0), run_time=1.0,
                  rate_func=linear)
        verdict = Text("(a+b)/2 ≥ √ab——半径压弦高，a = b 时恰好贴上",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("代数里的配方 (a−b)² ≥ 0，几何里就是一个直角三角形")
        self.wait(2.8)
