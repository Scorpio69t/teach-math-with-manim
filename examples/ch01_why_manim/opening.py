"""第 1 章案例：课堂开场动画（代码清单 1-1）

渲染：manim -pqh opening.py OpeningScene

叙事：任意三角形 → 三个内角上色标记 → 把三个角"撕下来"搬到
同一个顶点上 → 正好拼成一个平角 → ∠A + ∠B + ∠C = 180°。
公式成立的理由就是画面本身：三块角拼起来恰好是半圆。
"""

from manim import *


class OpeningScene(Scene):
    """课堂开场：三角形内角和，"撕角拼平角"，节奏舒缓。"""

    def construct(self):
        # 1. 一个任意三角形登场（不画坐标轴，主角只有它）
        A, B, C = LEFT * 2.4 + DOWN * 0.4, RIGHT * 2.4 + DOWN * 0.4, RIGHT * 0.6 + UP * 2.4
        tri = Polygon(A, B, C, color=BLUE, stroke_width=4)
        self.play(Create(tri), run_time=1.5)

        # 2. 给三个内角上色标记：红 A、金 B、绿 C，顶点字母同色
        verts = [A, B, C]
        names = ["A", "B", "C"]
        colors = [RED, GOLD, GREEN]
        marks, labels = [], []
        for i, (v, name, c) in enumerate(zip(verts, names, colors)):
            side1 = Line(v, verts[(i + 1) % 3])
            side2 = Line(v, verts[(i - 1) % 3])
            marks.append(Angle(side1, side2, radius=0.55, color=c, stroke_width=6))
            labels.append(MathTex(name, color=c).move_to(
                v + normalize(v - tri.get_center()) * 0.45))
        self.play(
            *[FadeIn(m) for m in marks],
            *[FadeIn(l) for l in labels],
            run_time=1.0,
        )

        # 3. 把三个角"搬"到下方同一个顶点上：弧弧相接，正好拼成半圆
        center = DOWN * 2.4
        start = 0.0
        moves = []
        for m, c in zip(marks, colors):
            target = Arc(radius=1.1, start_angle=start, angle=m.get_value(),
                         arc_center=center, color=c, stroke_width=6)
            moves.append(Transform(m.copy(), target))  # 复制一份搬走，原角留在三角形上
            start += m.get_value()
        self.play(LaggedStart(*moves, lag_ratio=0.3), run_time=2.5)

        # 4. 三块拼满半圆——半圆就是平角，就是 180°
        half = Arc(radius=1.5, start_angle=0, angle=PI,
                   arc_center=center, color=WHITE, stroke_width=3)
        formula = MathTex(r"\angle A + \angle B + \angle C = 180^\circ").scale(1.1)
        formula.next_to(center, DOWN, buff=0.5)
        self.play(Create(half), Write(formula), run_time=1.5)

        self.wait(2)  # 停顿留给讲解："所以，内角和是 180°"
