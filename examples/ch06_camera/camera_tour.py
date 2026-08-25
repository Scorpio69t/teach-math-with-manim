# -*- coding: utf-8 -*-
"""第 6 章 代码清单 6-1：运镜三式巡游（camera_tour.py）

渲染：manim -pql examples/ch06_camera/camera_tour.py CameraTour
"""
from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"


class CameraTour(MovingCameraScene):
    """一块大四倍的世界，镜头三式巡游：推近、平移、拉远回家。"""

    def make_block(self, title, subtitle, color, center):
        """一个内容块：色卡标题 + 说明，散布在世界各处。"""
        card = RoundedRectangle(width=6, height=3, corner_radius=0.2,
                                color=color, stroke_width=4)
        title_text = Text(title, font=FONT, font_size=34,
                          weight=BOLD, color=color)
        title_text.move_to(card.get_center() + UP * 0.6)
        sub = Text(subtitle, font=FONT, font_size=22, color="#9AA3C0")
        sub.next_to(title_text, DOWN, buff=0.4)
        block = VGroup(card, title_text, sub).move_to(center)
        return block

    def construct(self):
        frame = self.camera.frame

        # 世界布局：四块内容散布在 ±7、±4 的四个方位
        b1 = self.make_block("第一块：定义", "先把概念摆在这里", BLUE,
                             LEFT * 7 + UP * 4)
        b2 = self.make_block("第二块：推导", "过程写在旁边", GOLD,
                             RIGHT * 7 + UP * 4)
        b3 = self.make_block("第三块：例题", "练一道", GREEN,
                             LEFT * 7 + DOWN * 4)
        b4 = self.make_block("第四块：结论", "收尾点题", RED,
                             RIGHT * 7 + DOWN * 4)
        self.add(b1, b2, b3, b4)    # 世界就位——此刻镜头装不下它们，没关系

        # 全景开场：框放大到装下整个世界（直接调用 = 瞬间完成，观众第一帧即全景）
        frame.scale(1.9)
        frame.save_state()          # 把全景记成"家"，巡游结束好回来
        self.wait(1.2)

        # 第一式：推近——"现在只看第一块"
        self.play(frame.animate.scale(0.4).move_to(b1), run_time=2)
        self.wait(1.5)

        # 第二式：平移——"跟我来，目光移到第二块"
        self.play(frame.animate.move_to(b2), run_time=1.8)
        self.wait(1.5)

        # 第三式：拉远回家——Restore 回到 save_state 的全景
        self.play(Restore(frame), run_time=2)
        self.wait(1.5)
