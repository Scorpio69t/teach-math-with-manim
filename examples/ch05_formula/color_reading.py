"""第 5 章 5.4 配套：教鞭式带读——指示器逐项高亮。

渲染：
  manim -pqh color_reading.py GuidedReading   # 图 5-7
"""

from manim import *


class GuidedReading(Scene):
    """教鞭式带读：下划线滑到某项下方，该项亮起，读完保留痕迹。"""

    TERMS = [r"x^2", r"-", r"5x", r"+", r"6", r"=", r"0"]

    def construct(self):
        eq = MathTex(*self.TERMS)
        eq.scale(1.4)
        pointer = Line(LEFT * 0.5, RIGHT * 0.5, color=GOLD, stroke_width=5)

        self.play(Write(eq))
        for part in eq:
            pointer.next_to(part, DOWN, buff=0.25)  # 教鞭先到位
            self.add(pointer)
            self.play(Indicate(part, color=GOLD, scale_factor=1.15),
                      run_time=0.7)
            part.set_color(GOLD)                    # 讲过的留一点痕迹
            self.remove(pointer)
        self.wait()
