"""图 1-4 取帧用视频：与 opening.py 完全同节奏、同布局。

唯一差别：本机无 LaTeX，MathTex 全部换成 matplotlib mathtext
预渲染的透明 PNG（png/ 目录，Computer Modern 字形与 LaTeX 一致）。
装有 LaTeX 的机器可直接渲染 opening.py 抽取同样的帧。

渲染（在 code/ 目录下）：
    ../.venv-manim/Scripts/python.exe -m manim -qh examples/ch01_why_manim/fig1_4_video.py Fig14Video

时间轴（供抽帧参考）：
    0.0–1.5  Create 三角形
    1.5–2.5  三个内角标记 + 顶点字母
    2.5–5.0  三个角搬到下方顶点（LaggedStart）
    5.0–6.5  半圆 + 公式
    6.5–8.5  wait
抽帧建议：2.4s（三角标记就位）/ 3.8s（拼合中途）/ 7.5s（终帧）
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
    """与 OpeningScene 同节奏：撕角拼平角 → 内角和 180°。"""

    def construct(self):
        A, B, C = LEFT * 2.4 + DOWN * 0.4, RIGHT * 2.4 + DOWN * 0.4, RIGHT * 0.6 + UP * 2.4
        tri = Polygon(A, B, C, color=BLUE, stroke_width=4)
        self.play(Create(tri), run_time=1.5)

        verts = [A, B, C]
        label_files = ["label_a.png", "label_b.png", "label_c.png"]
        colors = [RED, GOLD, GREEN]
        marks, labels = [], []
        for i, (v, f, c) in enumerate(zip(verts, label_files, colors)):
            side1 = Line(v, verts[(i + 1) % 3])
            side2 = Line(v, verts[(i - 1) % 3])
            marks.append(Angle(side1, side2, radius=0.55, color=c, stroke_width=6))
            labels.append(math_img(f, 0.42).move_to(
                v + normalize(v - tri.get_center()) * 0.45))
        self.play(
            *[FadeIn(m) for m in marks],
            *[FadeIn(l) for l in labels],
            run_time=1.0,
        )

        center = DOWN * 2.4
        start = 0.0
        moves = []
        for m, c in zip(marks, colors):
            target = Arc(radius=1.1, start_angle=start, angle=m.get_value(),
                         arc_center=center, color=c, stroke_width=6)
            moves.append(Transform(m.copy(), target))
            start += m.get_value()
        self.play(LaggedStart(*moves, lag_ratio=0.3), run_time=2.5)

        half = Arc(radius=1.5, start_angle=0, angle=PI,
                   arc_center=center, color=WHITE, stroke_width=3)
        formula = math_img("angle_sum.png", 0.62)
        formula.next_to(center, DOWN, buff=0.5)
        # 书中为 Create(half) + Write(MathTex)；图片用 FadeIn 模拟 Write
        self.play(Create(half), FadeIn(formula, shift=UP * 0.2), run_time=1.5)

        self.wait(2)
