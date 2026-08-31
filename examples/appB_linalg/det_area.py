# 附录 B 案例三：行列式即面积——符号是方向在说话
# 渲染：manim -pqh det_area.py DetAreaScene
from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55
READOUT_POS = [4.2, 2.2, 0]


class DetAreaScene(Scene):
    """平行四边形的面积就是行列式的绝对值；
    滑一个矩阵元素让 det 穿过 0，看图形在 det = 0 处压扁、
    过零后翻转方向——det 的符号是方向在说话。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=24,
                              color=C_TEXT).move_to(NOTE_POS))

    def construct(self):
        plane = NumberPlane(
            x_range=[-2, 5, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": "#3A3A3A",
                                   "stroke_width": 1},
        )
        title = Text("行列式：面积与方向", font=FONT,
                     font_size=30, color=C_TEXT).to_edge(UP)
        self.note = Text("u 和 v 张成一个平行四边形",
                         font=FONT, font_size=24,
                         color=C_TEXT).move_to(NOTE_POS)
        self.play(Create(plane), Write(title), run_time=1.5)
        self.play(FadeIn(self.note))

        # u = (2, 0.5) 固定；v = (0.5, d)，d 用滑参从 1.5 滑到 -1
        d_track = ValueTracker(1.5)
        origin = plane.c2p(0, 0)
        u_end = plane.c2p(2, 0.5)
        v_end = lambda: plane.c2p(0.5, d_track.get_value())

        vec_u = Arrow(origin, u_end, buff=0, color=GOLD,
                      stroke_width=6)
        lab_u = Text("u = (2, 0.5)", font=FONT, font_size=26,
                     color=GOLD).next_to(u_end, DOWN, buff=0.15)

        # 派生对象全部公式化：v 的落点、平行四边形、读数都由 d 现算
        vec_v = always_redraw(lambda: Arrow(
            origin, v_end(), buff=0, color=TEAL, stroke_width=6))
        quad = always_redraw(lambda: Polygon(
            origin, u_end, u_end + (v_end() - origin), v_end(),
            stroke_color=GREEN, stroke_width=3,
            fill_color=GREEN, fill_opacity=0.25))
        readout = always_redraw(lambda: Text(
            f"v = (0.5, {d_track.get_value():+.1f})\n"
            f"det = 2×({d_track.get_value():+.1f}) − 0.5×0.5 "
            f"= {2 * d_track.get_value() - 0.25:+.2f}\n"
            f"面积 = {abs(2 * d_track.get_value() - 0.25):.2f}",
            font=FONT, font_size=22, color=C_TEXT,
            line_spacing=1.15).move_to(READOUT_POS))
        lab_v = always_redraw(lambda: Text(
            "v", font=FONT, font_size=26, color=TEAL
        ).next_to(v_end(), UP, buff=0.15))

        self.play(GrowArrow(vec_u), Write(lab_u), run_time=1.2)
        self.add(vec_v, quad, readout, lab_v)
        self.wait(1)

        # ===== d 下滑：det 奔向 0，四边形越来越扁 =====
        self.set_note("v 的纵坐标往下走——盯住面积读数")
        self.play(d_track.animate.set_value(0.125), run_time=3,
                  rate_func=linear)
        self.set_note("det ≈ 0：两个向量几乎共线，面积快被压没了")
        self.wait(1.5)

        # ===== 穿过 0：方向翻转，det 变负 =====
        self.play(d_track.animate.set_value(-1.0), run_time=3,
                  rate_func=linear)
        self.set_note("det 变负了——v 跑到了 u 的另一侧，方向翻了")
        self.play(Indicate(readout, color=RED), run_time=1.2)
        self.wait(3)
