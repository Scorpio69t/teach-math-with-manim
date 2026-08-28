from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

DATA = [(1, 1.4), (2, 2.2), (3, 1.8), (4, 3.4),
        (5, 3.0), (6, 4.2), (7, 4.0), (8, 5.2)]


class LeastSquares(Scene):
    """最小二乘的几何意义：残差画成方块，回归直线让方块总面积最小。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("最小二乘：哪条直线最配这堆点", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("八个散点，哪条直线和它们最般配？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 坐标系与散点 =====
        axes = Axes(x_range=[0, 9, 1], y_range=[0, 6, 1],
                    x_length=8.4, y_length=4.9,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to(LEFT * 1.4 + UP * 0.15)
        self.play(Create(axes), run_time=1.2)
        pts = [axes.coords_to_point(x, y) for x, y in DATA]
        dots = VGroup(*[Dot(p, color=TEAL, radius=0.08) for p in pts])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              lag_ratio=0.1), run_time=1.6)
        self.wait(0.8)

        # ===== 候选直线 + 残差方块 =====
        xs = np.array([d[0] for d in DATA])
        ys = np.array([d[1] for d in DATA])
        k_star, b_star = np.polyfit(xs, ys, 1)   # 最小二乘最优解
        k = ValueTracker(1.05)
        b = ValueTracker(-0.2)

        def f(x):
            return k.get_value() * x + b.get_value()

        line = always_redraw(lambda: Line(
            axes.coords_to_point(0.2, f(0.2)),
            axes.coords_to_point(8.8, f(8.8)),
            color=GOLD, stroke_width=4))
        residuals = VGroup(*[
            always_redraw(lambda x=x, y=y: DashedLine(
                axes.coords_to_point(x, y),
                axes.coords_to_point(x, f(x)),
                color=GREY_B, dash_length=0.08, stroke_width=2))
            for x, y in DATA])
        squares = VGroup(*[
            always_redraw(lambda x=x, y=y: self._res_square(axes, x, y, f))
            for x, y in DATA])
        self.add(line)   # always_redraw 对象不进 FadeIn：updater 改家族成员数会让插值错位
        self.wait(0.8)
        self.set_note("每个点的竖直偏离画成一个方块——方块面积 = 偏离²")
        self.add(residuals, squares)
        self.wait(1.6)

        # ===== Q 面板 =====
        q_lab = Text("方块总面积 Q =", font=FONT, font_size=26,
                     color=C_TEXT)
        q_lab.move_to([4.35, 3.0, 0], aligned_edge=RIGHT)
        q_anchor = np.array([4.6, 3.0, 0])
        q_num = Text("0.00", font=FONT, font_size=26, color=GOLD)
        q_num.move_to(q_anchor, aligned_edge=LEFT)

        def q_upd(m):
            q = float(np.sum((ys - k.get_value() * xs
                              - b.get_value()) ** 2))
            m.become(Text(f"{q:.2f}", font=FONT, font_size=26,
                          color=GOLD).move_to(q_anchor, aligned_edge=LEFT))
        q_num.add_updater(q_upd)
        self.add(q_lab, q_num)   # 挂 updater 的对象同样不走 FadeIn
        self.wait(1.2)

        # ===== 试来试去 =====
        self.set_note("斜率调小试试——方块胖了，Q 变大")
        self.play(k.animate.set_value(0.25), b.animate.set_value(1.8),
                  run_time=2.2)
        self.wait(1.2)
        self.set_note("调大再试——还是胖")
        self.play(k.animate.set_value(1.25), b.animate.set_value(-0.9),
                  run_time=2.2)
        self.wait(1.2)
        self.set_note("总有一个角度让 Q 最小——那就是答案")
        self.play(k.animate.set_value(k_star),
                  b.animate.set_value(b_star), run_time=2.6)
        self.wait(1.6)

        # ===== 样本中心点 =====
        self.set_note("盯住一点：回归直线一定穿过样本中心 (x̄, ȳ)")
        cx, cy = xs.mean(), ys.mean()
        center = Dot(axes.coords_to_point(cx, cy), color=RED,
                     radius=0.11)
        halo = Circle(radius=0.22, color=RED, stroke_width=2.5)
        halo.move_to(center.get_center())
        self.play(FadeIn(center, scale=0.5), Create(halo), run_time=0.9)
        self.wait(2.0)
        self.set_note("x̄ ≈ 4.5，ȳ ≈ 3.2——代进直线方程，严丝合缝")
        self.wait(2.4)

        # ===== 结案 =====
        self.set_note("为什么用平方不用绝对值？大偏差会被罚得更狠")
        self.wait(2.4)
        self.set_note("让面积和最小——所以叫「最小二乘」")
        self.wait(2.6)

    def _res_square(self, axes, x, y, f):
        """以残差线段为边长的半透明方块（面积=残差²）。"""
        p_dot = axes.coords_to_point(x, y)
        p_line = axes.coords_to_point(x, f(x))
        side = abs(p_dot[1] - p_line[1])
        side = max(side, 0.001)   # 退化值守卫：残差为 0 时不建零尺寸方块
        sq = Square(side_length=side, fill_color=GOLD,
                    fill_opacity=0.3, stroke_color=GOLD,
                    stroke_width=1.2)
        mid = (p_dot + p_line) / 2
        direction = RIGHT if f(x) >= y else LEFT
        sq.move_to(mid + direction * side / 2)
        return sq
