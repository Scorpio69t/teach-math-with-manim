# -*- coding: utf-8 -*-
"""第 6 章 代码清单 6-2：钉屏 HUD 演示（hud_demo.py）

渲染：manim -pqh examples/ch06_camera/hud_demo.py HudDemo
"""
from manim import *

FONT = "Microsoft YaHei"
C_TEXT = "#EDEDED"
WORLD_SPACING = 10


def pin_to_screen(camera, mob, place, buff=0.5):
    """钉屏：让 mob 钉在屏幕固定位置，镜头推拉平移都不动。

    place: "UL"（左上角）或 "BOTTOM"（底部居中）。
    原理：updater 每帧按取景框当前位置与缩放，重算 HUD 的世界坐标与尺寸
    ——钉屏不是一个状态，是每帧一次的重计算。
    """
    frame = camera.frame
    h0, fh0 = mob.height, frame.height   # 钉屏瞬间的尺寸基准

    def update(m):
        m.set_height(h0 * frame.height / fh0)   # 框缩一半，HUD 世界尺寸跟缩一半
        cx, cy = frame.get_center()[0], frame.get_center()[1]
        if place == "UL":
            m.move_to([cx - frame.width / 2 + buff + m.width / 2,
                       cy + frame.height / 2 - buff - m.height / 2, 0])
        elif place == "BOTTOM":
            m.move_to([cx, cy - frame.height / 2 + buff + m.height / 2, 0])

    mob.add_updater(update)
    return mob


class HudDemo(MovingCameraScene):
    """标题与注释条钉屏：镜头巡游三块内容，HUD 全程不动。"""

    def set_note(self, msg):
        """更新钉屏注释条：Transform 原地换内容，位置由 updater 接管。"""
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        self.play(Transform(self.note, new, run_time=0.3))

    def construct(self):
        frame = self.camera.frame

        # HUD：标题钉左上，注释条钉底部
        title = Text("勾股定理三讲", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("第一讲：它说了什么", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(DOWN * 3.3)
        pin_to_screen(self.camera, title, "UL")
        pin_to_screen(self.camera, self.note, "BOTTOM", buff=0.4)
        self.add(title, self.note)

        # 世界：三块内容一字排开；相邻两块在平移中途仍能完整同框
        world_positions = [
            RIGHT * (i * WORLD_SPACING - WORLD_SPACING) for i in range(3)
        ]
        for i, (txt, color) in enumerate([("是什么", BLUE),
                                          ("怎么证", GOLD),
                                          ("有什么用", GREEN)]):
            block = Text(txt, font=FONT, font_size=60, color=color)
            block.move_to(world_positions[i])
            self.add(block)

        # 幕后布机位：第一帧就让“第一讲”的字幕与“是什么”对应
        frame.move_to(world_positions[0])
        self.wait(1.5)

        # 镜头巡游：从第二站起，先运镜、再换注释、后停留
        nums = "一二三"
        topics = ["它说了什么", "怎么证明", "能干什么"]
        for i in range(1, 3):
            self.play(frame.animate.move_to(world_positions[i]), run_time=1.8)
            self.set_note(f"第{nums[i]}讲：{topics[i]}")
            self.wait(1.5)
