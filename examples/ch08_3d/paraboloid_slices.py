from manim import *

FONT = "Microsoft YaHei"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2


class ParaboloidSlices(ThreeDScene):
    """旋转抛物面：水平切片一路升高，圆从点长成整个碗。"""

    def set_note(self, msg):
        """三维钉屏铁律：fixed_in_frame 文字不能走 Transform（会被
        拖进三维空间躺平）。卸钉 -> 换件 -> 再钉，瞬切更新。"""
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.remove_fixed_in_frame_mobjects(self.note)
        self.remove(self.note)   # 卸钉只是解绑，它还躺在三维舞台上
        self.note = new
        self.add_fixed_in_frame_mobjects(self.note)

    def construct(self):
        title = Text("切片升起来，碗就长出来了", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("旋转抛物面 z = x² + y²", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-75 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                          z_range=[0, 4.5, 1],
                          x_length=5, y_length=5, z_length=4,
                          axis_config={"color": GREY_B, "stroke_width": 2},
                          tips=False)

        # 旋转抛物面：极坐标参数化，r 走半径、θ 走一圈
        bowl = Surface(
            lambda r, th: axes.c2p(r * np.cos(th), r * np.sin(th), r**2),
            u_range=[0, 1.9], v_range=[0, TAU],
            resolution=(14, 28),
            fill_opacity=0.25, fill_color=BLUE,
            stroke_color=BLUE_A, stroke_width=0.5,
        )

        # 遥控器：切片高度 h（第 7 章骨架三维复用）
        h = ValueTracker(0.05)

        # 切平面：半透明方片，每帧钉在 z=h
        plane = always_redraw(lambda: Square(
            side_length=4.6, fill_color=TEAL, fill_opacity=0.22,
            stroke_width=0).move_to(axes.c2p(0, 0, h.get_value())))

        # 交线圆：半径 = √h，每帧按当前 h 重画
        def make_circle():
            r = np.sqrt(max(h.get_value(), 1e-6))
            r_world = axes.c2p(r, 0, 0)[0] - axes.c2p(0, 0, 0)[0]
            return Circle(radius=r_world, color=GOLD,
                          stroke_width=5).move_to(axes.c2p(0, 0, h.get_value()))

        ring = always_redraw(make_circle)

        # 数值面板：h = 当前值（钉屏 2D，不跟三维转）
        # 三维钉屏面板的数字不能用 DecimalNumber.set_value（重建字模会
        # 脱离钉屏状态），改用 Text + updater 里 become 原地换内容；
        # 数字钉右缘、标签挂左边，防止位数变长时冲出画面右边
        num = Text("0.05", font=FONT, font_size=40, color=GOLD)
        num.to_corner(UR, buff=0.6)
        lab = MathTex("h=", font_size=44)
        lab.next_to(num, LEFT, buff=0.12)

        def refresh(d):
            d.become(Text(f"{h.get_value():.2f}", font=FONT,
                          font_size=40, color=GOLD)
                     .to_corner(UR, buff=0.6))

        num.add_updater(refresh)
        self.add_fixed_in_frame_mobjects(title, self.note, lab, num)

        self.play(Create(axes), run_time=1.2)
        self.add(bowl, plane, ring)
        self.wait(1)

        self.set_note("切片升高——交线始终是个圆")
        self.play(h.animate.set_value(3.2), run_time=5,
                  rate_func=linear)
        self.wait(1.5)

        self.set_note("圆越大，半径 = √h——这就是碗的横截面")
        self.play(h.animate.set_value(0.05), run_time=3,
                  rate_func=linear)
        self.wait(1.5)
