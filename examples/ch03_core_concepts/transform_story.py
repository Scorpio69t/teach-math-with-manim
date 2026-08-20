"""第 3 章综合案例：圆 → 方 → 三角的变形故事（代码清单 3-3）

渲染：manim -pqh transform_story.py TransformStoryScene
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"


class TransformStoryScene(Scene):
    """用一个五拍小故事串起本章三概念：Scene 搭台，Mobject 登场，Animation 叙事。"""

    C_TEXT = "#EDEDED"
    C_MUTED = "#9AA3C0"

    def construct(self):
        CAPTION_POS = DOWN * 3.2   # 字幕固定锚点（见 AGENTS.md §6.1）
        caption = Text("第一幕：一个圆的诞生", font=FONT, font_size=30,
                       color=self.C_TEXT)
        caption.move_to(CAPTION_POS)

        def set_caption(msg, color=None):
            new = Text(msg, font=FONT, font_size=30,
                       color=color or self.C_TEXT).move_to(CAPTION_POS)
            return Transform(caption, new, run_time=0.3)

        # 第一幕：出现（Create 的语义是"无中生有"）
        circle = Circle(radius=1.6, color=BLUE, stroke_width=6)
        self.play(FadeIn(caption), run_time=0.6)
        self.play(Create(circle), run_time=1.5)
        self.wait(0.8)

        # 第二幕：变形（Transform 的语义是"同一个东西在变化"）
        square = Square(side_length=2.8, color=GOLD, stroke_width=6)
        self.play(set_caption("第二幕：圆变成了正方形"), run_time=0.3)
        self.wait(0.5)
        self.play(Transform(circle, square), run_time=1.5)
        self.wait(0.8)

        # 第三幕：再变形
        triangle = Triangle(color=GREEN, stroke_width=6).scale(1.4)
        self.play(set_caption("第三幕：正方形又变成了三角形"), run_time=0.3)
        self.wait(0.5)
        self.play(Transform(circle, triangle), run_time=1.5)
        self.wait(0.8)

        # 第四幕：强调（Indicate 的语义是"看这里"）
        self.play(set_caption("第四幕：就是它——记住这个三角形"), run_time=0.3)
        self.wait(0.5)
        self.play(Indicate(circle, color=YELLOW, scale_factor=1.3),
                  run_time=0.8)
        self.wait(0.6)

        # 第五幕：谢幕与点题
        self.play(FadeOut(circle), run_time=1.0)
        self.play(set_caption("出现、变化、强调、退场——这就是动画的四种基本语义",
                              self.C_MUTED), run_time=0.4)
        self.wait(2.5)
