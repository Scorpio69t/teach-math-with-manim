"""第 16 章案例：割线旋成切线，切线斜率汇成导函数（代码清单 16-2）

渲染：manim -pqh derivative_sweep.py DerivativeSweep
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.5        # 注释条固定锚点
READOUT_POS = [3.3, 2.65, 0]  # 读数行锚点（右板上方）
X0 = 1.6                     # 复盘割线逼近的考察点


def f(x):
    """主曲线 y = x²/4。选它：斜率 x/2 全是干净的一位小数。"""
    return x**2 / 4


class DerivativeSweep(Scene):
    """左板切线随切点扫动，右板把斜率逐点收集——导函数曲线自己长出来。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def secant_at(self, h, color=RED):
        """过 (X0, f(X0)) 与 (X0+h, f(X0+h)) 的定长割线（展示方向，不是距离）。"""
        lax = self.lax
        P = lax.c2p(X0, f(X0))
        Q = lax.c2p(X0 + h, f(X0 + h))
        center = (P + Q) / 2
        direction = (Q - P) / np.linalg.norm(Q - P)
        return Line(center - direction * 1.4, center + direction * 1.4,
                    color=color, stroke_width=4)

    def tangent_line(self, x, color=GOLD):
        """x 处的切线：方向由数据斜率 x/2 换算成屏幕方向，定长。"""
        lax = self.lax
        P = lax.c2p(x, f(x))
        sx = lax.x_length / (lax.x_range[1] - lax.x_range[0])
        sy = lax.y_length / (lax.y_range[1] - lax.y_range[0])
        d = np.array([sx, (x / 2) * sy, 0])
        d = d / np.linalg.norm(d)
        return Line(P - d * 1.3, P + d * 1.3, color=color, stroke_width=4)

    def construct(self):
        title = Text("每一点的切线斜率，收集起来是什么？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("第 9 章逼近过一个点——今天让所有点一起出场",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.6)

        # ===== 左板：主曲线 =====
        self.lax = Axes(x_range=[-3.5, 3.5, 1], y_range=[-1, 3, 1],
                        x_length=5.4, y_length=3.6,
                        axis_config={"color": GREY_B, "stroke_width": 2},
                        tips=False)
        self.lax.move_to([-3.6, 1.3, 0])
        curve = self.lax.plot(f, x_range=[-3.2, 3.2], color=TEAL,
                              stroke_width=4)
        f_lab = Text("y = x²/4", font=FONT, font_size=24, color=TEAL)
        f_lab.move_to([-5.5, 2.85, 0])
        self.play(Create(self.lax), run_time=1.0)
        self.play(Create(curve), FadeIn(f_lab), run_time=1.4)
        self.set_note("老规矩：先在一个点上把割线逼成切线")
        self.wait(1.2)

        # ===== 复盘：割线两步逼近（h: 0.8 → 0.2 → 切线） =====
        recap = Text("x = 1.6 处：h = 0.8，斜率 1.00", font=FONT,
                     font_size=24, color=C_TEXT).move_to(READOUT_POS)
        self.add(recap)
        secant = self.secant_at(0.8)
        self.play(Create(secant), run_time=0.9)
        self.wait(1.0)
        self.play(Transform(secant, self.secant_at(0.2)), run_time=1.0)
        recap.become(Text("x = 1.6 处：h = 0.2，斜率 0.85", font=FONT,
                          font_size=24, color=C_TEXT).move_to(READOUT_POS))
        self.wait(1.0)
        self.play(Transform(secant, self.tangent_line(X0, color=GREEN)),
                  run_time=1.0)
        recap.become(Text("x = 1.6 处：切线斜率 = 0.80", font=FONT,
                          font_size=24, color=GREEN).move_to(READOUT_POS))
        self.set_note("h 越小斜率越稳——这一点的答案：0.80")
        self.wait(1.6)

        # ===== 右板：斜率收集器 =====
        self.rax = Axes(x_range=[-3.5, 3.5, 1], y_range=[-2, 2, 1],
                        x_length=5.4, y_length=2.8,
                        axis_config={"color": GREY_B, "stroke_width": 2},
                        tips=False)
        self.rax.move_to([3.3, 0.9, 0])
        start_readout = Text("x = -3.00　切线斜率 = -1.50", font=FONT,
                             font_size=24, color=C_TEXT).move_to(READOUT_POS)
        self.play(FadeOut(secant), ReplacementTransform(recap, start_readout),
                  run_time=0.8)
        self.play(Create(self.rax), run_time=1.0)
        self.set_note("右边的点只做一件事：高度 = 左边切线此刻的斜率")
        self.wait(1.6)

        # ===== 扫动：切线走到哪里，斜率描到哪里 =====
        x_track = ValueTracker(-3.0)
        tangent = always_redraw(
            lambda: self.tangent_line(x_track.get_value()))
        move_dot = always_redraw(lambda: Dot(
            self.lax.c2p(x_track.get_value(), f(x_track.get_value())),
            radius=0.08, color=GOLD))
        slope_dot = always_redraw(lambda: Dot(
            self.rax.c2p(x_track.get_value(), x_track.get_value() / 2),
            radius=0.08, color=GOLD))
        trace = TracedPath(slope_dot.get_center,
                           stroke_color=GOLD, stroke_width=4)
        readout = always_redraw(lambda: Text(
            f"x = {x_track.get_value():+.2f}　切线斜率 = "
            f"{x_track.get_value() / 2:+.2f}",
            font=FONT, font_size=24, color=C_TEXT).move_to(READOUT_POS))
        self.remove(start_readout)  # 静态起始读数交棒给 always_redraw，防叠影
        self.add(tangent, move_dot, slope_dot, trace, readout)
        self.set_note("从左端出发：盯住左边切线的倾斜，看右边点的高度")
        self.play(x_track.animate.set_value(0.0), run_time=3.2,
                  rate_func=linear)
        self.set_note("顶点处切线水平——右边的高度恰好压到 0")
        self.wait(1.6)
        self.play(x_track.animate.set_value(3.0), run_time=3.4,
                  rate_func=linear)
        self.wait(0.8)

        # ===== 结案：描出来的是一条直线 =====
        d_lab = Text("f′(x) = x/2", font=FONT, font_size=26,
                     weight=BOLD, color=GREEN)
        d_lab.move_to([4.7, 2.25, 0])
        self.play(FadeIn(d_lab), run_time=0.8)
        self.set_note("右边的轨迹是一条直线——它就是 f 的导函数")
        self.wait(1.8)

        verdict = Text("在可导区间内：输入 x，导数输出该点切线斜率",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to([0, -2.6, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("曲线 f 与它的导函数 f′：一个管位置，一个管变化")
        self.wait(2.6)
