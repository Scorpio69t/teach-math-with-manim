"""第 1 章案例：课堂开场动画（代码清单 1-1）

渲染：manim -pqh opening.py OpeningScene
"""

from manim import *


class OpeningScene(Scene):
    """课堂开场：圆 → 正方形 → 欧拉公式，节奏舒缓。"""

    def construct(self):
        # 1. 画圆：Create 描边动画，适合"无中生有"的开场
        circle = Circle(radius=1.5, color=BLUE)
        self.play(Create(circle), run_time=1.5)

        # 2. 圆变正方形：Transform 保持"同一个东西在变化"的直觉
        square = Square(side_length=3, color=GOLD)
        self.play(Transform(circle, square), run_time=1.5)

        # 3. 欧拉公式淡入：数学之美的点睛，位置下移给图形留位
        formula = MathTex(r"e^{i\pi} + 1 = 0").scale(1.2)
        formula.next_to(circle, DOWN, buff=0.8)
        self.play(FadeIn(formula), run_time=1.5)

        self.wait(2)  # 停顿留给讲解："这就是最美的公式"
