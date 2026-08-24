"""第 5 章 5.2 配套：公式组按等号对齐 + 零件编号演示。

渲染：
  manim -pqh aligned_group.py AlignedEquations   # 图 5-5
  manim -pqh aligned_group.py IndexLabelsDemo    # 图 5-4
"""

from manim import *


class AlignedEquations(Scene):
    """推导类画面的基础阵型：多行公式、等号对齐。"""

    def construct(self):
        # 三个方程的等号都是第 1 号零件——这是刻意设计的
        eq1 = MathTex(r"ax^2 + bx + c", r"=", r"0")
        eq2 = MathTex(r"x^2 + \dfrac{b}{a}x + \dfrac{c}{a}", r"=", r"0")
        eq3 = MathTex(r"x^2 + \dfrac{b}{a}x", r"=", r"-\dfrac{c}{a}")

        rows = VGroup(eq1, eq2, eq3)
        rows.arrange(DOWN, buff=0.7)          # 先纵向排开
        for row in rows[1:]:                   # 再把每行的等号
            row[1].align_to(rows[0][1], LEFT)  # 对齐到首行等号

        rows.move_to(ORIGIN)
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.play(Write(eq3))
        self.wait()


class IndexLabelsDemo(Scene):
    """调试演示：index_labels 给每个零件贴上编号（一个参数=一个零件）。"""

    def construct(self):
        eq = MathTex(r"ax^2", r"+", r"bx", r"+", r"c", r"=", r"0")
        eq.scale(1.6)
        labels = index_labels(eq, label_height=0.25)
        self.add(eq, labels)
        self.wait()
