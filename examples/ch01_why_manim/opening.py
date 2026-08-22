"""第 1 章案例：课堂开场动画（代码清单 1-1）

渲染：manim -pqh opening.py OpeningScene

叙事：复平面上的单位圆 → 半径向量从 1 逆时针旋转 π → 落在 -1 →
e^{iπ} = -1 移项得到 e^{iπ} + 1 = 0。
几何直觉参考：e^{iπ} 即"沿单位圆走半个圆弧"，落点正是 (-1, 0)。
"""

from manim import *


class OpeningScene(Scene):
    """课堂开场：让欧拉公式"看得见"，节奏舒缓。"""

    def construct(self):
        # 1. 复平面登场：坐标轴退作背景，单位圆才是主角
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": BLUE_E, "stroke_width": 2},
            tips=False,
        )
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(axes), run_time=1.0)
        self.play(Create(circle), run_time=1.5)

        # 2. 半径向量站在 1 上，准备出发
        vector = Arrow(ORIGIN, RIGHT * 2, buff=0, color=WHITE)
        one_label = MathTex("1").next_to(RIGHT * 2, DR, buff=0.15)
        self.play(GrowArrow(vector), FadeIn(one_label), run_time=1.0)

        # 3. 逆时针旋转 π：金色圆弧与向量同步生长，"走过的角度"看得见
        arc = Arc(radius=0.9, start_angle=0, angle=PI, color=GOLD, stroke_width=6)
        self.play(
            Rotate(vector, PI, about_point=ORIGIN, rate_func=linear),
            Create(arc, rate_func=linear),  # 与旋转同步，弧长=角度
            run_time=3,
        )
        pi_label = MathTex(r"\pi", color=GOLD).move_to(UP * 1.25 + LEFT * 0.35)
        self.play(FadeIn(pi_label), run_time=0.8)

        # 4. 落点正是 -1：这就是 e^{iπ} = -1 的几何含义
        landing = Dot(LEFT * 2, color=GOLD, radius=0.1)
        minus_one_label = MathTex("-1").next_to(LEFT * 2, DL, buff=0.15)
        self.play(FadeIn(landing, scale=1.5), FadeIn(minus_one_label), run_time=0.8)

        # 5. 公式现身：先给 e^{iπ} = -1，再移项成欧拉恒等式
        step1 = MathTex(r"e^{i\pi}", "=", "-1").scale(1.2)
        step1.to_edge(DOWN, buff=1.0)
        self.play(Write(step1), run_time=1.2)
        step2 = MathTex(r"e^{i\pi}", "+", "1", "=", "0").scale(1.2)
        step2.move_to(step1)
        self.play(TransformMatchingTex(step1, step2), run_time=1.2)  # 第 5 章详解

        self.wait(2)  # 停顿留给讲解："这就是最美的公式"
