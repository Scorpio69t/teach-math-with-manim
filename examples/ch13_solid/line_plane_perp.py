from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（三维场景用 fixed-frame 钉屏）


class LinePlanePerp(ThreeDScene):
    """旗杆为什么立得直：垂直于平面内两条相交直线才行，一条不够。"""

    def set_note(self, msg):
        """注释条铁律（三维版）：fixed-frame 下 become 换词会脱落钉屏，
        必须换成新对象后重新钉。"""
        new_note = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new_note.move_to(NOTE_POS)
        self.remove_fixed_in_frame_mobjects(self.note)
        self.remove(self.note)  # remove_fixed 只摘钉不摘场景，必须再 remove 否则留残影
        self.add_fixed_in_frame_mobjects(new_note)
        self.note = new_note

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-75 * DEGREES)
        title = Text("旗杆为什么立得直：线面垂直的判定", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("地面是一个平面，旗杆要立得直", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        # ===== 地面与旗杆 =====
        ground = Square(side_length=6, fill_color=GREY, fill_opacity=0.25,
                        stroke_color=GREY_B, stroke_width=2)
        grid = VGroup(*[Line([-3, i, 0], [3, i, 0], color=GREY_B,
                             stroke_width=0.8) for i in (-2, -1, 1, 2)],
                      *[Line([i, -3, 0], [i, 3, 0], color=GREY_B,
                             stroke_width=0.8) for i in (-2, -1, 1, 2)])
        pole = Line([0, 0, 0], [0, 0, 3], color=GOLD, stroke_width=8)
        tip = Dot([0, 0, 3], color=GOLD, radius=0.09)
        base = Dot([0, 0, 0], color=WHITE, radius=0.07)
        self.play(FadeIn(ground), FadeIn(grid), run_time=1.2)
        self.play(Create(pole), FadeIn(tip), FadeIn(base), run_time=1.2)
        self.wait(1.0)

        # ===== 地面上两条相交直线 =====
        l1 = Line([-2.6, 0, 0], [2.6, 0, 0], color=RED, stroke_width=5)
        l2 = Line([0, -2.6, 0], [0, 2.6, 0], color=TEAL, stroke_width=5)
        self.set_note("检验：旗杆和地面上的红线垂直吗？")
        self.play(Create(l1), run_time=1.0)
        # 直角标记：杆脚与 l1 之间的小拐角
        sq1 = VGroup(Line([0.28, 0, 0], [0.28, 0, 0.28],
                          color=WHITE, stroke_width=2.5),
                     Line([0.28, 0, 0.28], [0, 0, 0.28],
                          color=WHITE, stroke_width=2.5))
        self.play(FadeIn(sq1), run_time=0.6)
        self.wait(1.4)
        self.set_note("再检验：和青线也垂直吗？")
        self.play(Create(l2), run_time=1.0)
        sq2 = VGroup(Line([0, 0.28, 0], [0, 0.28, 0.28],
                          color=WHITE, stroke_width=2.5),
                     Line([0, 0.28, 0.28], [0, 0, 0.28],
                          color=WHITE, stroke_width=2.5))
        self.play(FadeIn(sq2), run_time=0.6)
        self.wait(1.4)
        self.set_note("两条都垂直，而且两线相交——旗杆钉死了")
        self.play(Indicate(l1, color=RED), Indicate(l2, color=TEAL),
                  run_time=1.4)
        self.wait(1.8)

        # ===== 反例：只垂直一条线 =====
        self.set_note("把青线撤掉：只垂直红线，旗杆还能立住吗？")
        self.play(FadeOut(l2), FadeOut(sq2), run_time=0.8)
        self.wait(0.8)
        self.set_note("看——它可以绕着红线前后倒，依然⊥红线")
        self.play(Rotate(pole, 35 * DEGREES, axis=RIGHT,
                         about_point=ORIGIN),
                  Rotate(tip, 35 * DEGREES, axis=RIGHT,
                         about_point=ORIGIN),
                  run_time=1.8)
        self.play(Rotate(pole, -70 * DEGREES, axis=RIGHT,
                         about_point=ORIGIN),
                  Rotate(tip, -70 * DEGREES, axis=RIGHT,
                         about_point=ORIGIN),
                  run_time=2.2)
        self.play(Rotate(pole, 35 * DEGREES, axis=RIGHT,
                         about_point=ORIGIN),
                  Rotate(tip, 35 * DEGREES, axis=RIGHT,
                         about_point=ORIGIN),
                  run_time=1.8)
        self.wait(1.2)
        self.set_note("一条直线管不住它——判定定理要「两条相交直线」")
        self.wait(2.6)

        # ===== 结案 =====
        self.set_note("相交两个字也关键：两条平行线同样管不住")
        self.play(FadeIn(l2), FadeIn(sq2), run_time=0.8)
        self.wait(1.2)
        self.set_note("线面垂直 = 垂直于平面内两条相交直线")
        self.wait(2.6)
