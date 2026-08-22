"""图 1-4 用三帧静帧：复刻 OpeningScene 的三个关键画面（代码清单 1-1 的成片帧）

渲染（静止帧，1080p）：
  manim -sqh fig1_4_stills.py Fig14Frame1Circle
  manim -sqh fig1_4_stills.py Fig14Frame2Square
  manim -sqh fig1_4_stills.py Fig14Frame3Final

说明：本机无 LaTeX，欧拉公式用 matplotlib mathtext 预渲染的透明 PNG
（euler_formula.png，cm 字体集，外观与 LaTeX 一致）；装有 LaTeX 的机器
上可将 ImageMobject 换成 MathTex(r"e^{i\\pi} + 1 = 0").scale(1.2)。
"""

from manim import *
from pathlib import Path

EULER_PNG = str(Path(__file__).parent / "euler_formula.png")


class Fig14Frame1Circle(Scene):
    """第一帧：Create 完成后的蓝色圆（半径 1.5，居中）。"""

    def construct(self):
        self.add(Circle(radius=1.5, color=BLUE, stroke_width=6))
        self.wait(0.1)


class Fig14Frame2Square(Scene):
    """第二帧：Transform 完成后的金色正方形（边长 3，居中）。"""

    def construct(self):
        self.add(Square(side_length=3, color=GOLD, stroke_width=6))
        self.wait(0.1)


class Fig14Frame3Final(Scene):
    """终帧：正方形 + 下方欧拉公式（next_to, DOWN, buff=0.8）。"""

    def construct(self):
        square = Square(side_length=3, color=GOLD, stroke_width=6)
        formula = ImageMobject(EULER_PNG)
        formula.height = 0.66   # 对齐 MathTex(...).scale(1.2) 的视觉体量
        formula.next_to(square, DOWN, buff=0.8)
        self.add(square, formula)
        self.wait(0.1)
