"""第 5 章 5.3 配套：TransformMatchingTex 移项变形。

渲染：
  manim -pqh matching_transform.py MoveTermTransform   # 图 5-6
"""

from manim import *

FONT = "Microsoft YaHei"   # macOS 改 "PingFang SC"，Linux 改 "Noto Sans CJK SC"


class MoveTermTransform(Scene):
    """等式两边同时减去 c/a：相同零件滑动，消掉的淡出，新增的淡入。"""

    def construct(self):
        before = MathTex(r"ax^2", r"+", r"bx", r"+", r"\dfrac{c}{a}",
                         r"=", r"0")
        after = MathTex(r"ax^2", r"+", r"bx", r"=", r"-", r"\dfrac{c}{a}")

        caption = Text("两边同时减去 c/a", font=FONT, font_size=28,
                       color=GOLD)
        caption.to_edge(DOWN, buff=0.9)

        self.play(Write(before))
        self.wait(0.8)
        self.play(Write(caption))
        self.play(TransformMatchingTex(before, after), run_time=2)
        self.wait()
