"""第 18 章案例：√2 无理数的无限递降——网格上的等腰直角三角形（代码清单 18-3）

渲染：manim -pqh sqrt2_descent.py Sqrt2Descent
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
VERDICT_POS = [0, -2.75, 0]

Q = 7                        # 直角边的数据长度
S = 0.52                     # 1 数据单位 = 0.52 屏幕单位
ORIGIN_PT = [-3.4, -1.7, 0]  # 直角顶点 A 的屏幕位置


def P(x, y):
    """数据坐标 → 屏幕坐标。"""
    return [ORIGIN_PT[0] + x * S, ORIGIN_PT[1] + y * S, 0]


class Sqrt2Descent(Scene):
    """假设 √2 = p/q 最小整数解；折边构造出更小的整数边
    等腰直角三角形——最小性自我击败，假设崩塌。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("√2 能写成一个分数吗？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.3)
        self.note = Text("假设能：√2 = p/q——看看这个假设把自己逼到哪",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 网格与大三角形 =====
        grid = NumberPlane(x_range=[-1, 9, 1], y_range=[-1, 9, 1],
                           background_line_style={
                               "stroke_color": GREY, "stroke_width": 1,
                               "stroke_opacity": 0.25},
                           faded_line_ratio=0)
        grid.scale(S)
        grid.shift(ORIGIN_PT - grid.c2p(0, 0))  # 让 (0,0) 格点落在 A

        A, B, C = P(0, 0), P(Q, 0), P(0, Q)
        tri = Polygon(A, B, C, color=TEAL, stroke_width=4)
        ra = Square(side_length=0.22, color=C_TEXT, stroke_width=2)
        ra.move_to([A[0] + 0.11, A[1] + 0.11, 0])
        q_lab1 = Text("q（整数）", font=FONT, font_size=22, color=TEAL)
        q_lab1.move_to([(A[0] + B[0]) / 2, A[1] - 0.32, 0])
        q_lab2 = Text("q（整数）", font=FONT, font_size=22, color=TEAL)
        q_lab2.move_to([A[0] - 0.75, (A[1] + C[1]) / 2, 0])
        p_lab = Text("p（整数）", font=FONT, font_size=22, color=TEAL)
        p_lab.move_to([(B[0] + C[0]) / 2 + 0.75, (B[1] + C[1]) / 2 + 0.15, 0])
        self.play(FadeIn(grid), run_time=0.9)
        self.play(Create(tri), FadeIn(ra), run_time=1.1)
        self.play(FadeIn(q_lab1), FadeIn(q_lab2), FadeIn(p_lab),
                  run_time=0.8)
        self.set_note("直角边 q、q，斜边 p——假设三边全是整数，且 q 最小")
        self.wait(2.2)

        # ===== 折边：在斜边上截出 q =====
        arc = Arc(radius=Q * S, start_angle=PI, angle=-PI / 4,
                  arc_center=B, color=GOLD, stroke_width=3)
        D = P(Q - Q / np.sqrt(2), Q / np.sqrt(2))
        d_dot = Dot(D, radius=0.07, color=GOLD)
        bd_lab = Text("BD = q", font=FONT, font_size=22, color=GOLD)
        bd_lab.move_to([(B[0] + D[0]) / 2 + 0.55, (B[1] + D[1]) / 2 - 0.3, 0])
        self.play(Create(arc), run_time=0.9)
        self.play(FadeIn(d_dot), FadeIn(bd_lab), run_time=0.7)
        self.set_note("以 B 为圆心、q 为半径截斜边：BD = q，剩下 DC = p − q")
        self.wait(2.2)

        # ===== 小三角形登场 =====
        E = P(0, Q * (np.sqrt(2) - 1))
        de = DashedLine(D, E, color=RED, stroke_width=2.5)
        small = Polygon(C, D, E, color=RED, fill_opacity=0.5,
                        stroke_width=3)
        dc_lab = Text("p − q", font=FONT, font_size=20, color=RED)
        dc_lab.move_to([(D[0] + C[0]) / 2 + 0.5, (D[1] + C[1]) / 2, 0])
        ce_lab = Text("2q − p", font=FONT, font_size=20, color=RED)
        ce_lab.move_to([(C[0] + E[0]) / 2 - 0.6, (C[1] + E[1]) / 2, 0])
        self.play(Create(de), run_time=0.8)
        self.play(FadeIn(small), FadeIn(dc_lab), FadeIn(ce_lab),
                  run_time=0.9)
        self.set_note("红色三角形还是等腰直角：边长 p−q、2q−p——全是整数！")
        self.wait(2.4)

        # ===== 递降矛盾 =====
        self.play(Indicate(small, color=RED, scale_factor=1.15),
                  run_time=0.9)
        loop = CurvedArrow([C[0] + 0.55, C[1] + 0.4, 0],
                           [C[0] - 0.1, C[1] + 0.75, 0],
                           angle=TAU / 3, color=RED, stroke_width=3,
                           tip_length=0.18)
        self.play(Create(loop), run_time=0.7)
        self.set_note("同样的构造还能再来一遍——更小的整数解永远造得出来")
        self.wait(2.2)

        verdict = Text("假设自我复制出更小的解——无限递降不可能，√2 不是分数",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("反证法：不直接证明它对，而是证明它的反面活不下去")
        self.wait(2.8)
