"""第 17 章案例：柯西不等式的向量看法——点积的天花板（代码清单 17-4）

渲染：manim -pqh cauchy_vectors.py CauchyVectors
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [5.0, 2.5, 0]       # 模长积（天花板）
R2_POS = [5.0, 1.9, 0]       # 点积读数
R3_POS = [5.0, 1.3, 0]       # 夹角读数
VERDICT_POS = [0, -2.75, 0]

U = np.array([3.0, 1.0])     # 固定向量
U_LEN = np.linalg.norm(U)    # √10 ≈ 3.162
V_LEN = np.sqrt(5.0)         # v 的模长恒为 √5 ≈ 2.236
U_ANG = np.arctan2(U[1], U[0])          # ≈ 18.4°
THETA0 = np.arctan2(2.0, 1.0)           # v 初始角 ≈ 63.4°（v = (1, 2)）


class CauchyVectors(Scene):
    """u 固定，v 保持模长旋转；点积 = |u| × 投影，随 cosθ 呼吸；
    共线一刻点积顶到天花板 |u||v|——柯西不等式取等。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("两个向量的点积，最大能多大？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("固定 u，捏住 v 的长度让它转——盯住点积的变化",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 建系 =====
        axes = Axes(x_range=[-1, 4, 1], y_range=[-1, 3, 1],
                    x_length=7.6, y_length=4.2,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to([-1.6, -0.2, 0])
        origin = axes.c2p(0, 0)
        self.play(Create(axes), run_time=1.1)

        # u 与其延长线
        u_tip = axes.c2p(*U)
        u_ext = DashedLine(origin, origin + (u_tip - origin) * 1.55,
                           color=GREY_B, stroke_width=2)
        u_arr = Arrow(origin, u_tip, buff=0, color=GOLD, stroke_width=5,
                      max_tip_length_to_length_ratio=0.12)
        u_lab = Text("u = (3, 1)", font=FONT, font_size=24, color=GOLD)
        u_lab.move_to(u_tip + RIGHT * 0.75 + DOWN * 0.38)
        self.play(Create(u_ext), run_time=0.6)
        self.play(FadeIn(u_arr), FadeIn(u_lab), run_time=0.9)
        self.set_note("金色箭头 u 不动；灰色虚线是它的延长线")
        self.wait(1.6)

        # ===== v 登场（可旋转） =====
        theta = ValueTracker(THETA0)

        def v_tip():
            t = theta.get_value()
            return axes.c2p(V_LEN * np.cos(t), V_LEN * np.sin(t))

        v_arr = always_redraw(lambda: Arrow(
            origin, v_tip(), buff=0, color=TEAL, stroke_width=5,
            max_tip_length_to_length_ratio=0.12))
        v_lab = always_redraw(lambda: Text(
            "v", font=FONT, font_size=24, color=TEAL)
            .move_to(v_tip() + UP * 0.35))

        def foot():
            """v 在 u 方向上的投影垂足（数据坐标）。"""
            t = theta.get_value()
            v = np.array([V_LEN * np.cos(t), V_LEN * np.sin(t)])
            return np.dot(v, U) / np.dot(U, U) * U

        proj = always_redraw(lambda: DashedLine(
            v_tip(), axes.c2p(*foot()), color=RED, stroke_width=2.5))
        proj_seg = always_redraw(lambda: Line(
            origin, axes.c2p(*foot()), color=RED, stroke_width=6,
            stroke_opacity=0.8))

        self.play(FadeIn(v_arr), FadeIn(v_lab), run_time=0.9)
        self.play(FadeIn(proj_seg), FadeIn(proj), run_time=0.9)
        self.set_note("红色是 v 投在 u 方向上的影子——点积 = |u| × 影长")
        self.wait(2.2)

        # ===== 读数面板 =====
        r1 = Text(f"|u|·|v| = {U_LEN * V_LEN:.2f}（天花板）", font=FONT,
                  font_size=24, color=GREEN)
        r1.move_to(R1_POS)
        r2 = always_redraw(lambda: Text(
            f"u·v = {U_LEN * V_LEN * np.cos(theta.get_value() - U_ANG):.2f}",
            font=FONT, font_size=26, color=C_TEXT).move_to(R2_POS))
        r3 = always_redraw(lambda: Text(
            f"夹角 θ = {np.degrees(abs(theta.get_value() - U_ANG)):.0f}°",
            font=FONT, font_size=24, color=C_TEXT).move_to(R3_POS))
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.8)
        self.set_note("此刻 u·v = 5，离天花板 7.07 还差一截——差的就是夹角")
        self.wait(2.4)

        # ===== 旋转节拍：点积呼吸 =====
        self.play(theta.animate.set_value(U_ANG + np.radians(80)),
                  run_time=1.8, rate_func=linear)
        self.set_note("v 转远：影子缩短，点积一路缩水")
        self.wait(1.6)
        self.play(theta.animate.set_value(U_ANG), run_time=1.8,
                  rate_func=linear)
        self.play(Indicate(u_arr, color=GREEN), run_time=0.8)
        r2_still = Text(f"u·v = {U_LEN * V_LEN:.2f} = |u|·|v|，取等！",
                        font=FONT, font_size=26, weight=BOLD, color=GREEN)
        r2_still.move_to([4.6, 1.9, 0])
        self.remove(r2)  # 静态取等读数交棒，防叠影
        self.add(r2_still)
        self.set_note("共线！影子 = v 的全长——点积顶到天花板")
        self.wait(2.4)
        self.remove(r2_still)
        self.add(r2)
        self.play(theta.animate.set_value(U_ANG - np.radians(35)),
                  run_time=1.6, rate_func=linear)
        self.set_note("再转开，点积又落回去——天花板只有共线才摸得到")
        self.wait(1.6)

        # ===== 结案 =====
        self.play(theta.animate.set_value(THETA0), run_time=1.2,
                  rate_func=linear)
        verdict = Text("柯西不等式：|u·v| ≤ |u|·|v|——真身就是 |cosθ| ≤ 1",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("(a₁²+a₂²)(b₁²+b₂²) ≥ (a₁b₁+a₂b₂)² 只是这句话的坐标翻译")
        self.wait(2.8)
