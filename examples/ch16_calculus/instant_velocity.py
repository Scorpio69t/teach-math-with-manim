"""第 16 章案例：从平均速度到瞬时速度（代码清单 16-1）

渲染：manim -pqh instant_velocity.py InstantVelocity
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.5      # 注释条固定锚点（换词位置不动）
R1_POS = [5.3, 2.5, 0]     # 读数面板第一行锚点
R2_POS = [5.3, 1.9, 0]     # 读数面板第二行锚点

T0 = 1.0                   # 考察时刻：t = 1 秒


def displacement(t):
    """位移记录 s(t) = 2t^2（米）。选它是因为平均速度算出来全是整数。"""
    return 2 * t**2


class InstantVelocity(Scene):
    """让 dt 一步步缩小：平均速度的读数自己走向瞬时速度。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def set_readout(self, dt_text, v_text, v_color=C_TEXT):
        self.row1.become(Text(dt_text, font=FONT, font_size=26,
                              color=C_TEXT).move_to(R1_POS))
        self.row2.become(Text(v_text, font=FONT, font_size=26,
                              color=v_color).move_to(R2_POS))

    def secant_through(self, dt, color=RED):
        """过 P、斜率等于平均速度的定长割线。

        割线展示的是方向而不是两点距离（第 9 章的教训），
        所以用定长线段绕 P、Q 中点旋转，dt 再小也不会缩没。
        """
        P = self.axes.c2p(T0, displacement(T0))
        Q = self.axes.c2p(T0 + dt, displacement(T0 + dt))
        center = (P + Q) / 2
        direction = (Q - P) / np.linalg.norm(Q - P)
        half = 2.0
        return Line(center - direction * half, center + direction * half,
                    color=color, stroke_width=4)

    def construct(self):
        title = Text("这辆车在 t = 1 秒时，到底开多快？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("问的是瞬时速度——可手里只有一张位移记录",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.6)

        # ===== 坐标系与位移曲线 =====
        self.axes = Axes(x_range=[0, 3, 1], y_range=[0, 14, 2],
                         x_length=8.4, y_length=4.6,
                         axis_config={"color": GREY_B, "stroke_width": 2},
                         tips=False)
        self.axes.move_to([0.2, 0.35, 0])
        t_lab = Text("t / s", font=FONT, font_size=22, color=C_TEXT)
        t_lab.next_to(self.axes.x_axis, RIGHT, buff=0.15)
        s_lab = Text("s / m", font=FONT, font_size=22, color=C_TEXT)
        s_lab.next_to(self.axes.y_axis, UP, buff=0.15)
        curve = self.axes.plot(displacement, x_range=[0, 2.4],
                               color=TEAL, stroke_width=4)
        self.play(Create(self.axes), FadeIn(t_lab), FadeIn(s_lab),
                  run_time=1.2)
        self.play(Create(curve), run_time=1.6)
        self.set_note("位移曲线 s = 2t²：每个时刻的位置都躺在上面")
        self.wait(1.4)

        # ===== 第一个区间：1 到 2 秒 =====
        self.row1 = Text("Δt = 1.0 s", font=FONT, font_size=26,
                         color=C_TEXT).move_to(R1_POS)
        self.row2 = Text("平均速度 = 6.0 m/s", font=FONT, font_size=26,
                         color=C_TEXT).move_to(R2_POS)
        P = Dot(self.axes.c2p(T0, displacement(T0)), radius=0.09, color=GOLD)
        Q = Dot(self.axes.c2p(T0 + 1, displacement(T0 + 1)),
                radius=0.09, color=RED)
        p_lab = Text("P", font=FONT, font_size=24, color=GOLD)
        p_lab.next_to(P, LEFT, buff=0.15)
        q_lab = Text("Q", font=FONT, font_size=24, color=RED)
        q_lab.next_to(Q, RIGHT, buff=0.15)
        self.play(FadeIn(P), FadeIn(p_lab), FadeIn(Q), FadeIn(q_lab),
                  FadeIn(self.row1), FadeIn(self.row2), run_time=0.9)
        secant = self.secant_through(1.0)
        self.play(Create(secant), run_time=0.9)
        self.set_note("1 到 2 秒：平均速度 = Δs ÷ Δt = 6 m/s——但这不是 t = 1 的速度")
        self.wait(1.8)

        # ===== Δt 缩小三连 =====
        steps = [
            (0.5, "5.0", "Δt 砍半：平均速度 5.0——更接近了"),
            (0.2, "4.4", "再缩小：4.4。Q 越贴近 P，割线越趴在曲线上"),
            (0.1, "4.2", "4.2……读数变化越来越慢，像被什么拽住了"),
        ]
        for dt, vtxt, msg in steps:
            new_secant = self.secant_through(dt)
            new_Q = Dot(self.axes.c2p(T0 + dt, displacement(T0 + dt)),
                        radius=0.09, color=RED)
            self.play(Transform(secant, new_secant), Transform(Q, new_Q),
                      FadeOut(q_lab), run_time=1.2)
            self.set_readout(f"Δt = {dt} s", f"平均速度 = {vtxt} m/s")
            self.set_note(msg)
            self.wait(1.6)

        # ===== 定格：割线旋成切线 =====
        tangent = self.secant_through(0.001, color=GREEN)
        self.play(FadeOut(Q), Transform(secant, tangent), run_time=1.4)
        self.set_readout("Δt → 0", "瞬时速度 = 4 m/s", v_color=GREEN)
        self.set_note("Δs 和 Δt 都奔向 0——但它们的比值稳稳走向 4")
        self.wait(2.0)

        verdict = Text("瞬时速度不是 0/0，是平均速度一步步走到的归宿",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to([0, 2.55, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("这个「一步步逼近」的动作就是本章的主角：极限")
        self.wait(2.6)
