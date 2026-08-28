from manim import *

FONT = "Microsoft YaHei"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2


class SurfaceDemo(ThreeDScene):
    """Surface：给参数方程一片定义域，长出一张曲面。"""

    def set_note(self, msg):
        """三维钉屏铁律：fixed_in_frame 文字不能走 Transform（会被
        拖进三维空间躺平）。新建 -> 卸钉 -> remove -> 再钉，瞬切更新。"""
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.remove_fixed_in_frame_mobjects(self.note)
        self.remove(self.note)   # 卸钉只是解绑，它还躺在三维舞台上
        self.note = new
        self.add_fixed_in_frame_mobjects(self.note)

    def construct(self):
        title = Text("马鞍面：z = x² − y²", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("曲面是一张参数网格", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                          z_range=[-3, 3, 1],
                          x_length=5, y_length=5, z_length=4,
                          axis_config={"color": GREY_B, "stroke_width": 2},
                          tips=False)
        self.play(Create(axes), run_time=1.2)

        # 马鞍面：u、v 两个参数各走一遍定义域，每个 (u,v) 算出空间点
        saddle = Surface(
            lambda u, v: axes.c2p(u, v, (u**2 - v**2) / 2.5),
            u_range=[-2.4, 2.4], v_range=[-2.4, 2.4],
            resolution=(20, 20),            # 网格密度：越大越细腻越慢
            fill_opacity=0.65, fill_color=TEAL,
            stroke_color=TEAL_A, stroke_width=0.6,
        )
        self.set_note("一个方向向上弯，另一个方向向下弯")
        self.play(Create(saddle), run_time=2)
        self.wait(1)

        # 环绕半周：从另一侧看"又凸又凹"——马鞍的灵魂
        self.set_note("换个方向看：它同时是凸的和凹的")
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()
        self.wait(1)
