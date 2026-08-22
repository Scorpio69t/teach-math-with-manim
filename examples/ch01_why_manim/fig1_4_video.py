"""图 1-4 取帧用视频：与 opening.py 完全同节奏、同布局。

唯一差别：本机无 LaTeX，MathTex 全部换成 matplotlib mathtext
预渲染的透明 PNG（png/ 目录，Computer Modern 字形与 LaTeX 一致）。
装有 LaTeX 的机器可直接渲染 opening.py 抽取同样的帧。

渲染（在 code/ 目录下）：
    ../.venv-manim/Scripts/python.exe -m manim -qh examples/ch01_why_manim/fig1_4_video.py Fig14Video

时间轴（供抽帧参考）：
    0.0–1.0   Create 坐标轴
    1.0–2.5   Create 单位圆
    2.5–3.5   GrowArrow 向量 + 标签 1
    3.5–6.5   Rotate π + 圆弧同步生长
    6.5–7.3   π 标签
    7.3–8.1   落点 -1
    8.1–9.3   Write e^{iπ} = -1
    9.3–10.5  变形为 e^{iπ} + 1 = 0
    10.5–12.5 wait
抽帧建议：3.4s（单位圆与向量就位）/ 5.0s（旋转中途，向量指向上方）/ 11.5s（终帧）
"""

from pathlib import Path

from manim import *

PNG = Path(__file__).with_name("png")


def math_img(name: str, height: float) -> ImageMobject:
    """加载 mathtext 预渲染 PNG，等价替换书中的 MathTex。"""
    img = ImageMobject(str(PNG / name))
    img.height = height
    return img


class Fig14Video(Scene):
    """与 OpeningScene 同节奏：单位圆 → 旋转 π → 欧拉公式。"""

    def construct(self):
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

        vector = Arrow(ORIGIN, RIGHT * 2, buff=0, color=WHITE)
        one_label = math_img("one.png", 0.4).next_to(RIGHT * 2, DR, buff=0.15)
        self.play(GrowArrow(vector), FadeIn(one_label), run_time=1.0)

        arc = Arc(radius=0.9, start_angle=0, angle=PI, color=GOLD, stroke_width=6)
        self.play(
            Rotate(vector, PI, about_point=ORIGIN, rate_func=linear),
            Create(arc, rate_func=linear),
            run_time=3,
        )
        pi_label = math_img("pi_gold.png", 0.45).move_to(UP * 1.25 + LEFT * 0.35)
        self.play(FadeIn(pi_label), run_time=0.8)

        landing = Dot(LEFT * 2, color=GOLD, radius=0.1)
        minus_one_label = math_img("minus_one.png", 0.4).next_to(LEFT * 2, DL, buff=0.15)
        self.play(FadeIn(landing, scale=1.5), FadeIn(minus_one_label), run_time=0.8)

        step1 = math_img("eq_neg1.png", 0.6)
        step1.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(step1, shift=UP * 0.2), run_time=1.2)  # 书中为 Write(MathTex)
        step2 = math_img("identity.png", 0.6)
        step2.move_to(step1)
        # 书中为 TransformMatchingTex；图片无法插值，用交叉淡入淡出模拟
        self.play(FadeOut(step1, shift=UP * 0.1), FadeIn(step2, shift=UP * 0.1), run_time=1.2)

        self.wait(2)
