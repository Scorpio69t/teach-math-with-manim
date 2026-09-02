# 附录 B 案例一：向量加法与数乘——平行四边形法则
# 渲染：manim -pqh vector_add.py VectorAddScene
from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
READOUT_POS = [4.9, 2.8, 0]  # 读数面板固定锚点


class VectorAddScene(Scene):
    """两个向量相加：先各归各位，再把 b 平移到 a 的终点，
    绿色对角线就是 a + b——平行四边形法则。"""

    def set_note(self, msg):
        # 注释条原地换词：become 保持引用，不产生闪烁（全书统一写法）
        self.note.become(Text(msg, font=FONT, font_size=24,
                              color=C_TEXT).move_to(NOTE_POS))

    def construct(self):
        plane = NumberPlane(
            x_range=[-1, 6, 1], y_range=[-1, 4, 1],
            background_line_style={"stroke_color": "#3A3A3A",
                                   "stroke_width": 1},
        )
        title = Text("向量加法：平行四边形法则", font=FONT,
                     font_size=30, color=C_TEXT).to_edge(UP)
        self.note = Text("两个向量，从同一点出发", font=FONT,
                         font_size=24, color=C_TEXT).move_to(NOTE_POS)
        readout = Text("a = (3, 1)\nb = (1, 2)", font=FONT,
                       font_size=24, color=C_TEXT,
                       line_spacing=1.2).move_to(READOUT_POS)
        self.play(Create(plane), Write(title), run_time=1.5)
        self.play(FadeIn(self.note), FadeIn(readout))

        # ===== 两个向量登场：金 a、青 b =====
        origin = plane.c2p(0, 0)
        tip_a, tip_b = plane.c2p(3, 1), plane.c2p(1, 2)
        vec_a = Arrow(plane.c2p(0, 0), tip_a, buff=0,
                      color=GOLD, stroke_width=6)
        vec_b = Arrow(plane.c2p(0, 0), tip_b, buff=0,
                      color=TEAL, stroke_width=6)
        lab_a = Text("a", font=FONT, font_size=28, color=GOLD
                     ).next_to(tip_a, RIGHT, buff=0.15)
        lab_b = Text("b", font=FONT, font_size=28, color=TEAL
                     ).next_to(tip_b, UP, buff=0.15)
        self.play(GrowArrow(vec_a), Write(lab_a), run_time=1.2)
        self.play(GrowArrow(vec_b), Write(lab_b), run_time=1.2)
        self.wait(0.8)

        # ===== b 平移到 a 的终点：虚线副本跟随，原 b 留在原地 =====
        self.set_note("把 b 平移到 a 的终点——方向和长度都不变")
        vec_b_copy = vec_b.copy().set_stroke(opacity=0.6)
        shift_to_a = tip_a - origin
        tip_sum = plane.c2p(4, 3)
        dash_b = DashedLine(tip_a, tip_sum, color=TEAL)
        self.play(vec_b_copy.animate.shift(shift_to_a), Create(dash_b),
                  run_time=1.6)
        self.wait(0.8)

        # ===== 对角线即答案：绿色 a + b =====
        self.set_note("从起点指向终点的那条对角线，就是 a + b")
        vec_sum = Arrow(plane.c2p(0, 0), tip_sum, buff=0,
                        color=GREEN, stroke_width=6)
        lab_sum = Text("a + b = (4, 3)", font=FONT, font_size=28,
                       color=GREEN).next_to(tip_sum, RIGHT, buff=0.2)
        dash_a = DashedLine(tip_b, tip_sum, color=GOLD)
        self.play(Create(dash_a), GrowArrow(vec_sum), run_time=1.5)
        self.play(Write(lab_sum))
        self.set_note("坐标也对得上：(3+1, 1+2) = (4, 3)")
        self.wait(3)
