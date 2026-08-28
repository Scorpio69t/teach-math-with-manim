from manim import *

FONT = "Microsoft YaHei"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2


class ParaboloidSlices(ThreeDScene):
    """旋转抛物面：水平切片一路升高，圆从点长成整个碗。"""

    def set_note(self, msg):
        """三维钉屏铁律：fixed_in_frame 文字不能走 Transform（会被
        拖进三维空间躺平）。新建 -> 卸钉 -> remove -> 再钉，瞬切更新。"""
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.remove_fixed_in_frame_mobjects(self.note)
        self.remove(self.note)   # 卸钉只是解绑，它还躺在三维舞台上
        self.note = new
        self.add_fixed_in_frame_mobjects(self.note)

    def make_height_panel(self, value):
        """每次返回一块完整的新面板，避免替换已钉屏对象的子对象。"""
        label = MathTex("h=", font_size=44)
        number = Text(f"{value:.2f}", font=FONT,
                      font_size=40, color=GOLD)
        return VGroup(label, number).arrange(RIGHT, buff=0.12).to_corner(
            UR, buff=0.6)

    def set_height_panel(self, value):
        """三维钉屏数字更新：新建 -> 卸钉 -> remove -> 再钉。"""
        new_panel = self.make_height_panel(value)
        self.remove_fixed_in_frame_mobjects(self.height_panel)
        self.remove(self.height_panel)
        self.add_fixed_in_frame_mobjects(new_panel)
        self.height_panel = new_panel

    def animate_height_to(self, tracker, target, run_time, steps=21):
        """分段播放；只在相邻 play 之间安全替换钉屏面板。"""
        start = tracker.get_value()
        for value in np.linspace(start, target, steps + 1)[1:]:
            self.play(
                tracker.animate.set_value(value),
                run_time=run_time / steps,
                rate_func=linear,
            )
            self.set_height_panel(value)

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

        # 数值面板自身不挂 updater。高度动画分成短段，每段 play 结束后
        # 整块新建面板，再走“卸钉 -> remove -> 再钉”四步。
        self.height_panel = self.make_height_panel(h.get_value())
        self.add_fixed_in_frame_mobjects(
            title, self.note, self.height_panel)

        self.play(Create(axes), run_time=1.2)
        self.add(bowl, plane, ring)
        self.wait(1)

        self.set_note("切片升高——交线始终是个圆")
        self.animate_height_to(h, 3.2, run_time=5)
        self.wait(1.5)

        self.set_note("圆越大，半径 = √h——这就是碗的横截面")
        self.animate_height_to(h, 0.05, run_time=3)
        self.wait(1.5)
