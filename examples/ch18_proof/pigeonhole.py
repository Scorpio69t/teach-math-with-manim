"""第 18 章案例：鸽巢原理——从显然到不显然（代码清单 18-4）

渲染：manim -pqh pigeonhole.py Pigeonhole
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [4.6, 2.4, 0]       # 计数读数
R2_POS = [4.6, 1.8, 0]       # 结论读数
VERDICT_POS = [0, -2.75, 0]

# 第二幕的 5 个点（数据坐标，正方形边长 2，半格边长 1）
PTS = [(-0.75, -0.60), (-0.45, -0.85), (0.80, -0.65),
       (-0.65, 0.75), (0.70, 0.65)]
PAIR = (0, 1)                # 同格的一对：距离现算


class Pigeonhole(Scene):
    """第一幕：10 球 9 格，必有一格两球；
    第二幕：边长 2 的正方形任取 5 点，必有两点距离 ≤ √2。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("多出来的那一个，去了哪里？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("10 个球，9 个格子——一个一个往里放",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 第一幕：10 球 9 格 =====
        CS = 0.92  # 格子边长
        grid_c = [-2.5, 0.2, 0]
        cells = VGroup()
        for i in range(3):
            for j in range(3):
                sq = Square(side_length=CS, color=TEAL, stroke_width=2.5)
                sq.move_to([grid_c[0] + (i - 1) * CS,
                            grid_c[1] + (j - 1) * CS, 0])
                cells.add(sq)
        r1 = Text("", font=FONT, font_size=26, color=C_TEXT).move_to(R1_POS)
        self.add(r1)
        self.play(FadeIn(cells, lag_ratio=0.08), run_time=1.0)
        self.set_note("9 个格子是巢——球一个个落下")
        self.wait(1.2)

        import itertools
        jitter = list(itertools.product([-0.14, 0.14], repeat=2))
        balls = VGroup()
        for k in range(9):
            jx, jy = jitter[k % 4]
            pos = cells[k].get_center() + [jx, jy, 0]
            ball = Dot(pos + UP * 1.6, radius=0.09, color=GOLD)
            self.add(ball)
            self.play(ball.animate.move_to(pos), run_time=0.35,
                      rate_func=rush_into)
            balls.add(ball)
            r1.become(Text(f"已放 {k + 1} 球 / 9 格", font=FONT,
                           font_size=26, color=C_TEXT).move_to(R1_POS))
        self.set_note("前 9 球各占一格——第 10 球来了")
        self.wait(1.2)

        pos10 = cells[4].get_center() + [0.2, 0.16, 0]
        ball10 = Dot(pos10 + UP * 1.6, radius=0.09, color=RED)
        self.add(ball10)
        self.play(ball10.animate.move_to(pos10), run_time=0.4,
                  rate_func=rush_into)
        r1.become(Text("已放 10 球 / 9 格", font=FONT, font_size=26,
                       color=C_TEXT).move_to(R1_POS))
        self.play(Indicate(cells[4], color=RED, scale_factor=1.12),
                  run_time=0.8)
        r2 = Text("这一格有两只！", font=FONT, font_size=26, weight=BOLD,
                  color=RED)
        r2.move_to(R2_POS)
        self.play(FadeIn(r2, scale=0.9), run_time=0.6)
        self.set_note("球比巢多，必有一巢撞车——显然得不能再显然")
        self.wait(2.4)

        # ===== 换场 =====
        self.play(FadeOut(cells), FadeOut(balls), FadeOut(ball10),
                  FadeOut(r1), FadeOut(r2), run_time=0.8)

        # ===== 第二幕：正方形里的 5 个点 =====
        self.set_note("换成数学题：边长 2 的正方形里任取 5 个点")
        SC = 1.5  # 数据 1 单位 = 1.5 屏幕单位
        sq_c = [-0.4, 0.2, 0]
        big = Square(side_length=2 * SC, color=GOLD, stroke_width=3.5)
        big.move_to(sq_c)
        cross = VGroup(
            DashedLine(sq_c + LEFT * SC, sq_c + RIGHT * SC,
                       color=GREY_B, stroke_width=2),
            DashedLine(sq_c + DOWN * SC, sq_c + UP * SC,
                       color=GREY_B, stroke_width=2))
        self.play(FadeIn(big), Create(cross), run_time=1.0)
        self.set_note("十字虚线分成 4 个小格——抽屉造好了")
        self.wait(1.8)

        def sc(pt):
            return [sq_c[0] + pt[0] * SC, sq_c[1] + pt[1] * SC, 0]

        dots = VGroup(*[Dot(sc(p), radius=0.09, color=RED) for p in PTS])
        self.play(FadeIn(dots, lag_ratio=0.2), run_time=1.0)
        self.set_note("5 个红点落进 4 个格子——鸽巢原理说：必有一格装了两个")
        self.wait(2.0)

        p0, p1 = PTS[PAIR[0]], PTS[PAIR[1]]
        dist = float(np.hypot(p0[0] - p1[0], p0[1] - p1[1]))
        link = Line(sc(p0), sc(p1), color=RED, stroke_width=4)
        rr1 = Text("同格两点的距离：", font=FONT, font_size=24,
                   color=C_TEXT).move_to(R1_POS)
        rr2 = Text(f"{dist:.2f} ≤ √2 ≈ {np.sqrt(2):.2f}", font=FONT,
                   font_size=26, weight=BOLD, color=RED).move_to(R2_POS)
        self.play(Create(link), run_time=0.7)
        self.play(FadeIn(rr1), FadeIn(rr2), run_time=0.7)
        self.set_note("同格必撞线：小格对角线才 √2，同格距离超不过它")
        self.wait(2.6)

        verdict = Text("鸽巢原理：球多于巢必撞车——高明之处在于造抽屉",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("原理三岁能懂；看出哪儿有抽屉，是数学家的手艺")
        self.wait(2.8)
