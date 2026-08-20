"""第 3 章案例：rate_func 节奏函数对比（代码清单 3-2）

渲染：manim -pqh rate_func_demo.py RateFuncDemo
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"


class RateFuncDemo(Scene):
    """三个小球走同样的路，唯一区别是节奏函数——一眼看懂 rate_func。"""

    def construct(self):
        # 起点与终点的参考线
        start_line = DashedLine(UP * 2.2, DOWN * 2.2, color=GREY).shift(LEFT * 4.5)
        end_line = DashedLine(UP * 2.2, DOWN * 2.2, color=GREY).shift(RIGHT * 4.5)
        self.add(start_line, end_line)

        rows = [
            ("smooth（默认：先快后慢）", smooth, BLUE, UP * 1.4),
            ("linear（匀速：机械感）", linear, GOLD, ORIGIN),
            ("there_and_back（去而复返）", there_and_back, RED, DOWN * 1.4),
        ]

        balls, labels = VGroup(), VGroup()
        for name, _, color, offset in rows:
            ball = Dot(radius=0.18, color=color).shift(LEFT * 4.5 + offset)
            label = Text(name, font=FONT, font_size=22,
                         color=color).next_to(ball, LEFT, buff=0.3)
            balls.add(ball)
            labels.add(label)
        self.play(FadeIn(labels), FadeIn(balls), run_time=0.8)

        # 同一个动作，三种节奏
        self.play(
            balls[0].animate(rate_func=smooth).shift(RIGHT * 9),
            balls[1].animate(rate_func=linear).shift(RIGHT * 9),
            balls[2].animate(rate_func=there_and_back).shift(RIGHT * 9),
            run_time=3,
        )
        self.wait(1)
