# 附录 B 案例二：矩阵即变换——看基向量去哪里
# 渲染：manim -pqh matrix_transform.py MatrixTransformScene
from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55
READOUT_POS = [5.0, 2.6, 0]

MATRIX = [[2, 1], [-1, 1]]  # 本案例的变换矩阵


class MatrixTransformScene(Scene):
    """2x2 矩阵作用在整个坐标平面上：
    盯住金色 i 与青色 j 两个基向量落在哪里，
    矩阵的两列就是它们在标准基下的像坐标。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=24,
                              color=C_TEXT).move_to(NOTE_POS))

    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": "#3A3A3A",
                                   "stroke_width": 1},
        )
        title = Text("矩阵即变换：基向量去哪里", font=FONT,
                     font_size=30, color=C_TEXT).to_edge(UP)
        self.note = Text("单位正方形就位：i 指向右，j 指向上",
                         font=FONT, font_size=24,
                         color=C_TEXT).move_to(NOTE_POS)
        readout = Text("变换矩阵\n[ 2   1 ]\n[ -1  1 ]",
                       font=FONT, font_size=24, color=C_TEXT,
                       line_spacing=1.1).move_to(READOUT_POS)

        # 单位正方形与两个基向量：变换前的"标准配置"
        square = Polygon(plane.c2p(0, 0), plane.c2p(1, 0),
                         plane.c2p(1, 1), plane.c2p(0, 1),
                         stroke_color=C_TEXT, stroke_width=3)
        vec_i = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0,
                      color=GOLD, stroke_width=6)
        vec_j = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), buff=0,
                      color=TEAL, stroke_width=6)
        lab_i = Text("i", font=FONT, font_size=28, color=GOLD
                     ).next_to(plane.c2p(1, 0), DOWN, buff=0.15)
        lab_j = Text("j", font=FONT, font_size=28, color=TEAL
                     ).next_to(plane.c2p(0, 1), LEFT, buff=0.15)

        self.play(Create(plane), Write(title), run_time=1.5)
        self.play(Create(square), GrowArrow(vec_i), GrowArrow(vec_j),
                  Write(lab_i), Write(lab_j), run_time=1.5)
        self.play(FadeIn(self.note), FadeIn(readout))
        self.wait(1)

        # ===== 整个平面被矩阵"揉"一遍 =====
        self.set_note("盯住 i 和 j——它们要搬家了")
        moving = VGroup(plane, square, vec_i, vec_j)
        self.play(FadeOut(lab_i), FadeOut(lab_j),
                  ApplyMatrix(MATRIX, moving), run_time=3)
        lab_i.next_to(vec_i.get_end(), DOWN, buff=0.15)
        lab_j.next_to(vec_j.get_end(), LEFT, buff=0.15)
        self.play(FadeIn(lab_i), FadeIn(lab_j), run_time=0.5)
        self.wait(1)

        # ===== 结案：矩阵的列是在标准基下的像坐标 =====
        self.set_note("i 落在 (2, -1)，j 落在 (1, 1)——正好是矩阵的两列")
        self.play(Indicate(vec_i, color=GOLD), Indicate(vec_j, color=TEAL),
                  run_time=1.5)
        self.wait(3)
