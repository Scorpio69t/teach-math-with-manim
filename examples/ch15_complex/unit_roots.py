from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

R = 1.8                              # 单位圆屏幕半径
C0 = np.array([0, 0.3, 0])           # 圆心
N = 5                                # 五次单位根
COLS = [GOLD, TEAL, ORANGE, "#C77DFF", "#7BD88F"]


class UnitRoots(Scene):
    """x^5 = 1 的五个根：z1 连乘五次扫过整圈砸回 1，
    五个根正是正五边形的五个顶点。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def pt(self, k):
        ang = 2 * PI * k / N
        return C0 + R * np.array([np.cos(ang), np.sin(ang), 0])

    def construct(self):
        title = Text("x^5 = 1 的根长什么样？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("实数范围只有 x = 1。复数世界里呢？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 单位圆与五个根 =====
        circle = Circle(radius=R, color=GREY_B, stroke_width=2.5)
        circle.move_to(C0)
        self.play(Create(circle), run_time=0.9)

        dots, labs = [], []
        for k in range(N):
            d = Dot(self.pt(k), radius=0.09, color=COLS[k])
            ang = 2 * PI * k / N
            out = np.array([np.cos(ang), np.sin(ang), 0])
            lab = Text(f"z{k}", font=FONT, font_size=24, color=COLS[k])
            lab.move_to(self.pt(k) + out * 0.45)
            dots.append(d)
            labs.append(lab)
        self.play(*[FadeIn(d) for d in dots],
                  *[FadeIn(l) for l in labs], run_time=1.0)
        self.set_note("五个候选：z0 = 1，其余四个等距站在圆上——间隔 72°")
        self.wait(2.0)

        # ===== z1 的五次方：扫过整圈 =====
        arrow = Arrow(C0, self.pt(1), buff=0, color=GOLD, stroke_width=5,
                      max_tip_length_to_length_ratio=0.15)
        self.play(GrowArrow(arrow), run_time=0.9)
        self.set_note("算算 z1 的五次方：每乘一次 z1，转 72°")
        self.wait(1.4)

        pow_lab = Text("z1^1", font=FONT, font_size=28, weight=BOLD,
                       color=GOLD)
        pow_lab.move_to([4.6, 2.6, 0], aligned_edge=RIGHT)
        self.add(pow_lab)

        for m in range(2, N + 1):        # 第 2..5 次乘法
            k = m % N                    # 落点编号（m=5 → z0）
            self.play(Rotate(arrow, angle=2 * PI / N, about_point=C0),
                      run_time=1.1)
            pow_lab.become(Text(
                f"z1^{m} = 1" if m == N else f"z1^{m}",
                font=FONT, font_size=28, weight=BOLD,
                color=GOLD if m < N else "#7BD88F")
                .move_to([4.6, 2.6, 0], aligned_edge=RIGHT))
            self.play(Indicate(dots[k], color=COLS[k], scale_factor=1.6),
                      run_time=0.5)
            if m == 3:
                self.set_note("72° + 72° + 72°……角度一直在累加")
            if m == N:
                self.set_note("5 × 72° = 360°——正好一整圈，砸回 1！")
                self.wait(1.8)

        self.wait(0.8)

        # ===== 其余四个也一样 =====
        self.play(FadeOut(arrow), run_time=0.6)
        self.set_note("每个顶点的五次方都是 1：五个根，一个不多一个不少")
        self.play(*[Indicate(d, color=c, scale_factor=1.5)
                    for d, c in zip(dots, COLS)], run_time=1.2)
        self.wait(1.6)

        # ===== 连线：正五边形现身 =====
        penta = Polygon(*[self.pt(k) for k in range(N)],
                        color=GOLD, stroke_width=4)
        self.play(Create(penta), run_time=1.6)
        verdict = Text("x^5 = 1 的五个根 = 正五边形的顶点",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to([0, -2.6, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("代数方程的解，原来是一幅几何图形")
        self.wait(2.2)
        self.set_note("x^n = 1：n 个根，永远是正 n 边形")
        self.wait(2.6)
