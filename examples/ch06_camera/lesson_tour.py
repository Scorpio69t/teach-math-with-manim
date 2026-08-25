# -*- coding: utf-8 -*-
"""第 6 章 代码清单 6-3：一节课的运镜脚本（lesson_tour.py）

三角形内角和微课：一区对象、一区证明、一区结论，镜头巡游，HUD 钉屏。
渲染：manim -pql examples/ch06_camera/lesson_tour.py LessonTour
"""
from manim import *

FONT = "Microsoft YaHei"
C_TEXT = "#EDEDED"

TRI_CENTER = LEFT * 9          # 左区：三角形与三个角
PASTE_CENTER = RIGHT * 9       # 右区：撕角拼合现场
RESULT_POS = DOWN * 8          # 下方：结论区


def pin_to_screen(camera, mob, place, buff=0.5):
    """钉屏：让 mob 钉在屏幕固定位置，镜头推拉平移都不动（机制见 6.2）。

    place: "UL"（左上角）或 "BOTTOM"（底部居中）。
    原理：updater 每帧按取景框当前位置与缩放，重算 HUD 的世界坐标与尺寸。
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


def build_triangle_zone():
    """左区：任意三角形 + 三角标记（红 A、金 B、绿 C）。"""
    A = TRI_CENTER + LEFT * 2.4 + DOWN * 1.2
    B = TRI_CENTER + RIGHT * 2.4 + DOWN * 1.2
    C = TRI_CENTER + RIGHT * 0.6 + UP * 1.8
    tri = Polygon(A, B, C, color=BLUE, stroke_width=5)
    marks, labels = [], []
    verts = [A, B, C]
    for i, (v, name, c) in enumerate(zip(verts, "ABC", [RED, GOLD, GREEN])):
        side1 = Line(v, verts[(i + 1) % 3])
        side2 = Line(v, verts[(i - 1) % 3])
        marks.append(Angle(side1, side2, radius=0.55, color=c,
                           stroke_width=6))
        labels.append(Text(name, font=FONT, font_size=30, color=c).move_to(
            v + normalize(v - tri.get_center()) * 0.7))
    return tri, marks, labels


class LessonTour(MovingCameraScene):
    """三角形内角和：一区对象、一区证明、一区结论，镜头巡游。"""

    def set_note(self, msg):
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        self.play(Transform(self.note, new, run_time=0.3))

    def construct(self):
        frame = self.camera.frame

        # HUD 钉屏：标题 + 注释条（6.2 的 pin_to_screen 机制）
        title = Text("三角形内角和", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("任意三角形，内角和为什么是 180°？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(DOWN * 3.3)
        pin_to_screen(self.camera, title, "UL")
        pin_to_screen(self.camera, self.note, "BOTTOM", buff=0.4)
        self.add(title, self.note)

        # 幕后布机位：镜头直接落在左区（不演给观众看）
        frame.move_to(TRI_CENTER).set(width=12)

        # ── 镜 1：左区，对象登场 ──
        tri, marks, labels = build_triangle_zone()
        self.play(Create(tri), run_time=1.5)
        self.play(*[FadeIn(m) for m in marks],
                  *[FadeIn(l) for l in labels], run_time=1.2)
        self.set_note("三个内角：红的、金的、绿的")
        self.wait(1.5)

        # ── 镜 2：平移到右区，撕角启程 ──
        self.set_note("把三个角搬到同一个顶点上")
        self.play(frame.animate.move_to(PASTE_CENTER).set(width=12),
                  run_time=2)
        center = PASTE_CENTER + DOWN * 0.3
        start = 0.0
        moves = []
        for m, c in zip(marks, [RED, GOLD, GREEN]):
            target = Arc(radius=1.4, start_angle=start,
                         angle=m.get_value(), arc_center=center,
                         color=c, stroke_width=6)
            moves.append(Transform(m.copy(), target))
            start += m.get_value()
        self.play(LaggedStart(*moves, lag_ratio=0.3), run_time=2.5)
        self.wait(0.8)

        # ── 镜 3：半圆显现 ──
        half = Arc(radius=1.9, start_angle=0, angle=PI,
                   arc_center=center, color=WHITE, stroke_width=3)
        self.play(Create(half), run_time=1.2)
        self.set_note("弧弧相接，严丝合缝——这是一个半圆")
        self.wait(1.5)

        # ── 镜 4：拉远全景，结论浮现 ──
        formula = Text("∠A + ∠B + ∠C = 180°", font=FONT,
                       font_size=48, weight=BOLD, color=GOLD)
        formula.move_to(RESULT_POS)
        self.play(frame.animate.move_to(DOWN * 3).set(width=26),
                  run_time=2)
        self.play(Write(formula), run_time=1.5)
        self.set_note("半圆就是平角——所以，内角和是 180°")
        self.wait(2.5)
