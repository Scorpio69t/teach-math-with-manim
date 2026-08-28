from manim import *

FONT = "Microsoft YaHei"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2


class CameraOrbit(ThreeDScene):
    """运镜三招：摆机位、环绕、推近——立体感是运动给的。"""

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
        title = Text("相机环绕：让立体感自己出现", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("先摆机位", font=FONT, font_size=26,
                         color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # 三个简单几何体：前后错落，专门用来看视差
        cube = Cube(side_length=1.4, fill_color=BLUE,
                    fill_opacity=0.7, stroke_color=BLUE_A)
        cube.move_to(LEFT * 2.2 + IN * 0.5)
        ball = Sphere(radius=0.8, resolution=(16, 16))
        ball.set_fill(TEAL, opacity=0.8)
        cone = Cone(base_radius=0.8, height=1.6, fill_color=GOLD,
                    fill_opacity=0.8, stroke_color=GOLD_A)
        cone.move_to(RIGHT * 2.2 + OUT * 0.5)
        self.play(FadeIn(cube), FadeIn(ball), FadeIn(cone), run_time=1.5)
        self.wait(0.8)

        # 招式一：环境旋转——相机绕场景匀速环绕，视差自动出现
        self.set_note("环绕开始：你没动，几何体的相对位置在动")
        self.begin_ambient_camera_rotation(rate=0.3)  # 弧度/秒
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # 招式二：推近——move_camera 调 zoom，直奔细节
        self.set_note("推近看球：move_camera 调 zoom")
        self.move_camera(zoom=1.6, run_time=2)
        self.wait(1.5)
