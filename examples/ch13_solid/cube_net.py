from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（三维场景用 fixed-frame 钉屏）

A = 2.0                   # 正方体棱长


class CubeNet(ThreeDScene):
    """正方体拆成十字展开图，再折回去：6 个面、11 种展开法的入门体验。"""

    def set_note(self, msg):
        """注释条铁律（三维版）：fixed-frame 下 become 换词会脱落钉屏，
        必须换成新对象后重新钉。"""
        new_note = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new_note.move_to(NOTE_POS)
        self.remove_fixed_in_frame_mobjects(self.note)
        self.remove(self.note)  # remove_fixed 只摘钉不摘场景，必须再 remove 否则留残影
        self.add_fixed_in_frame_mobjects(new_note)
        self.note = new_note

    def face(self, shift, color, rot_axis=None):
        f = Square(side_length=A, fill_color=color, fill_opacity=0.85,
                   stroke_color=WHITE, stroke_width=2)
        if rot_axis is not None:
            f.rotate(PI / 2, axis=rot_axis)
        f.shift(shift)
        return f

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-60 * DEGREES)
        title = Text("拆盒子：正方体与它的展开图", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一个正方体，6 个面", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        # ===== 六个面（底面不动，四个侧面铰接，顶面挂在后面上） =====
        bottom = self.face([0, 0, -A / 2], GREY)
        front = self.face([0, -A / 2, 0], GOLD, RIGHT)
        back = self.face([0, A / 2, 0], ORANGE, RIGHT)
        left = self.face([-A / 2, 0, 0], BLUE, UP)
        right = self.face([A / 2, 0, 0], TEAL, UP)
        top = self.face([0, 0, A / 2], PURPLE)
        cube = VGroup(bottom, front, back, left, right, top)
        self.play(LaggedStart(*[FadeIn(f, scale=0.6) for f in cube],
                              lag_ratio=0.12), run_time=1.8)
        self.wait(1.0)

        # 转一圈看看全貌
        self.set_note("先转一圈：记住每个面的颜色和位置")
        self.move_camera(theta=-60 * DEGREES + PI / 2, run_time=2.6)
        self.wait(0.8)

        # ===== 拆盒子 =====
        h = A / 2   # 半棱长，铰链都在 z = -h 的底边一圈
        self.set_note("沿底面的四条棱，把四个侧面放倒")
        back_top = VGroup(back, top)
        self.play(Rotate(front, PI / 2, axis=RIGHT,
                         about_point=[0, -h, -h]),
                  Rotate(right, PI / 2, axis=UP,
                         about_point=[h, 0, -h]),
                  Rotate(left, -PI / 2, axis=UP,
                         about_point=[-h, 0, -h]),
                  Rotate(back_top, -PI / 2, axis=RIGHT,
                         about_point=[0, h, -h]),
                  run_time=3.0)
        self.wait(1.2)
        self.set_note("顶面还挂在后面上——再折一次，彻底摊平")
        self.play(Rotate(top, -PI / 2, axis=RIGHT,
                         about_point=[0, 3 * h, -h]),
                  run_time=2.0)
        self.wait(1.4)

        # ===== 展开图特写 =====
        self.set_note("摊平了：这就是展开图——一条四连面，左右各一臂")
        self.move_camera(phi=8 * DEGREES, theta=-90 * DEGREES,
                         run_time=2.4)   # 转到正上方俯视
        self.wait(1.6)
        self.set_note("正方体的展开图共有 11 种，这是最常见的十字形")
        self.wait(2.4)
        self.set_note("考考你：折回去之后，金色的对面是什么颜色？")
        self.wait(2.6)

        # ===== 叠盒子 =====
        self.move_camera(phi=68 * DEGREES, theta=-60 * DEGREES,
                         run_time=2.2)
        self.set_note("原路折回去：先立顶面")
        self.play(Rotate(top, PI / 2, axis=RIGHT,
                         about_point=[0, 3 * h, -h]),
                  run_time=1.6)
        self.set_note("再立四个侧面——答案揭晓：金色对面是橙色")
        self.play(Rotate(front, -PI / 2, axis=RIGHT,
                         about_point=[0, -h, -h]),
                  Rotate(right, -PI / 2, axis=UP,
                         about_point=[h, 0, -h]),
                  Rotate(left, PI / 2, axis=UP,
                         about_point=[-h, 0, -h]),
                  Rotate(back_top, PI / 2, axis=RIGHT,
                         about_point=[0, h, -h]),
                  run_time=3.0)
        self.wait(1.0)
        self.set_note("展开与折叠互为逆操作——面与面的邻居关系不变")
        self.move_camera(theta=-60 * DEGREES - PI / 2, run_time=2.6)
        self.wait(2.0)
