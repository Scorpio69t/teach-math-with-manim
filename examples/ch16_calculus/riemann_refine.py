"""第 16 章案例：矩形分割逼近曲边梯形面积（代码清单 16-3）

渲染：manim -pqh riemann_refine.py RiemannRefine
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.5        # 注释条固定锚点
R1_POS = [5.2, 2.4, 0]       # 读数面板第一行
R2_POS = [5.2, 1.8, 0]       # 读数面板第二行
R3_POS = [5.2, 1.2, 0]       # 精确值行（结案时出场）

X_END = 2.0                  # 区间 [0, 2]


def f(x):
    """被积函数 x²——选它因为精确面积 8/3 能口算验证。"""
    return x**2


class RiemannRefine(Scene):
    """右端点矩形从 4 个加密到 64 个：面积和读数自己走向 8/3。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def right_sum(self, n):
        """n 个右端点矩形的面积和——读数一律现算，不手抄。"""
        dx = X_END / n
        return sum(f(k * dx) * dx for k in range(1, n + 1))

    def excess_regions(self, n):
        """每个矩形高出曲线的部分（误差）涂红：它缩水就是逼近在发生。"""
        dx = X_END / n
        regions = VGroup()
        for k in range(1, n + 1):
            a, b = (k - 1) * dx, k * dx
            xs = np.linspace(a, b, 8)
            pts = [self.axes.c2p(x, f(x)) for x in xs]
            pts += [self.axes.c2p(b, f(b)), self.axes.c2p(a, f(b))]
            regions.add(Polygon(*pts, color=RED, fill_opacity=0.75,
                                stroke_width=0))
        return regions

    def construct(self):
        title = Text("曲边梯形的面积，怎么算？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("没有现成公式——但我们会算矩形",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.6)

        # ===== 坐标系与曲线 =====
        self.axes = Axes(x_range=[0, 2.2, 1], y_range=[0, 4.5, 1],
                         x_length=7.6, y_length=4.2,
                         axis_config={"color": GREY_B, "stroke_width": 2},
                         tips=False)
        self.axes.move_to([-0.6, 0.45, 0])
        curve = self.axes.plot(f, x_range=[0, 2.05], color=TEAL,
                               stroke_width=4)
        f_lab = Text("y = x²", font=FONT, font_size=24, color=TEAL)
        f_lab.move_to([2.4, 2.75, 0])
        self.play(Create(self.axes), run_time=1.0)
        self.play(Create(curve), FadeIn(f_lab), run_time=1.4)
        self.set_note("目标：曲线下方、0 到 2 之间这块面积")
        self.wait(1.4)

        # ===== 读数面板 =====
        self.row1 = Text("n = 4", font=FONT, font_size=26,
                         color=C_TEXT).move_to(R1_POS)
        self.row2 = Text(f"面积和 S = {self.right_sum(4):.3f}",
                         font=FONT, font_size=26, color=C_TEXT).move_to(R2_POS)

        # ===== n = 4 起步 =====
        rects = self.axes.get_riemann_rectangles(
            curve, x_range=[0, X_END], dx=X_END / 4,
            input_sample_type="right",
            color=GOLD, stroke_width=2, fill_opacity=0.5)
        excess = self.excess_regions(4)
        self.play(Create(rects), FadeIn(self.row1), FadeIn(self.row2),
                  run_time=1.4)
        self.set_note("四个矩形封顶，每个取右端点高度")
        self.wait(1.4)
        self.play(FadeIn(excess), run_time=0.8)
        self.set_note("红色是多算的部分——误差全在这里")
        self.wait(1.8)

        # ===== 加密三连 =====
        steps = [
            (8,  "加密一倍：红色瘦了一圈"),
            (16, "再加密：红色快看不见了"),
            (32, "读数还在降，但降得越来越慢"),
        ]
        for n, msg in steps:
            new_rects = self.axes.get_riemann_rectangles(
                curve, x_range=[0, X_END], dx=X_END / n,
                input_sample_type="right",
                color=GOLD, stroke_width=2, fill_opacity=0.5)
            new_excess = self.excess_regions(n)
            self.play(ReplacementTransform(rects, new_rects),
                      ReplacementTransform(excess, new_excess),
                      run_time=1.2)
            rects, excess = new_rects, new_excess
            self.row1.become(Text(f"n = {n}", font=FONT, font_size=26,
                                  color=C_TEXT).move_to(R1_POS))
            self.row2.become(Text(f"面积和 S = {self.right_sum(n):.3f}",
                                  font=FONT, font_size=26,
                                  color=C_TEXT).move_to(R2_POS))
            self.set_note(msg)
            self.wait(1.7)

        # ===== n = 64 快闪 =====
        new_rects = self.axes.get_riemann_rectangles(
            curve, x_range=[0, X_END], dx=X_END / 64,
            input_sample_type="right",
            color=GOLD, stroke_width=1, fill_opacity=0.5)
        self.play(ReplacementTransform(rects, new_rects), FadeOut(excess),
                  run_time=1.0)
        rects = new_rects
        self.row1.become(Text("n = 64", font=FONT, font_size=26,
                              color=C_TEXT).move_to(R1_POS))
        self.row2.become(Text(f"面积和 S = {self.right_sum(64):.3f}",
                              font=FONT, font_size=26,
                              color=C_TEXT).move_to(R2_POS))
        self.set_note("64 个矩形：肉眼已经分不清矩形和曲线了")
        self.wait(1.8)

        # ===== 结案：极限值就是定积分 =====
        exact = Text("精确值 8/3 ≈ 2.667", font=FONT, font_size=26,
                     color=GREEN).move_to(R3_POS)
        self.play(FadeIn(exact), run_time=0.8)
        self.set_note("n 无限加密的归宿：8/3——它就是定积分 ∫₀² x² dx")
        self.wait(2.0)

        verdict = Text("定积分不是新算法，是矩形面积和的极限",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to([0, -2.6, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("逼近的每一步都是近似，极限那一步是精确")
        self.wait(2.6)
