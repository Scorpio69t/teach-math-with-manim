"""第 2 章案例：环境验证场景（代码清单 2-1）

渲染：manim -pqh first_scene.py FirstScene
"""

from manim import *


class FirstScene(Scene):
    """环境验证场景：画一个蓝色的圆。"""

    def construct(self):
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle), run_time=2)
        self.wait(1)
