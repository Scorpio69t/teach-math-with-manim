"""第 4 章案例：三种定位思维对比（代码清单 4-1）

渲染：manim -pqh position_demo.py PositioningDemo
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"


class PositioningDemo(Scene):
    """同一个小方块，三种找位置的方式：绝对坐标、相对位移、相对元素。"""

    C_TEXT = "#EDEDED"

    def construct(self):
        CAPTION_POS = DOWN * 3.2   # 字幕固定锚点（见 AGENTS.md §6.1）

        # 淡色坐标网当"黑板坐标纸"：让坐标数字可见，是定位直觉的第一步
        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": GREY, "stroke_width": 1,
                                   "stroke_opacity": 0.35},
        )
        self.add(grid)

        caption = Text("第一幕：move_to——报到坐标原点", font=FONT,
                       font_size=28, color=self.C_TEXT).move_to(CAPTION_POS)
        self.play(FadeIn(caption), run_time=0.5)

        # 第一幕：绝对坐标。方块被"指派"到坐标 (3, 1.5)，不管它原来在哪
        seat = Square(side_length=1.2, color=GOLD, fill_opacity=0.6)
        coord_label = Text("", font=FONT, font_size=24, color=GOLD)
        self.play(FadeIn(seat), run_time=0.6)
        self.play(seat.animate.move_to(RIGHT * 3 + UP * 1.5), run_time=1.2)
        coord_label.become(
            Text("坐标 (3.0, 1.5)", font=FONT, font_size=24, color=GOLD)
            .next_to(seat, UP, buff=0.3))
        self.play(FadeIn(coord_label), run_time=0.4)
        self.wait(1.2)

        # 第二幕：相对位移。shift 不问"在哪"，只问"往哪挪"
        caption.become(Text("第二幕：shift——向左挪 4 格，向下挪 2 格",
                            font=FONT, font_size=28,
                            color=self.C_TEXT).move_to(CAPTION_POS))
        self.play(seat.animate.shift(LEFT * 4 + DOWN * 2), run_time=1.4)
        self.wait(1.2)

        # 第三幕：相对元素。next_to 不问坐标，只问"挨着谁"
        caption.become(Text("第三幕：next_to——跟着方块走，不记坐标",
                            font=FONT, font_size=28,
                            color=self.C_TEXT).move_to(CAPTION_POS))
        tag = Text("我是标签", font=FONT, font_size=24, color=BLUE)
        tag.next_to(seat, RIGHT, buff=0.4)   # 标签的位置由方块决定
        self.play(FadeIn(tag), run_time=0.6)
        # 方块动，标签手动跟随——第 7 章 updater 会让这个跟随自动化
        self.play(seat.animate.shift(RIGHT * 2), tag.animate.shift(RIGHT * 2),
                  run_time=1.2)
        self.wait(1.5)
