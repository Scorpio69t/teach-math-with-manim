from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（三维场景用 fixed-frame 钉屏）

PX, PY, PZ = 2.0, 1.2, 2.0   # 点 P 的坐标


class SpaceVector(ThreeDScene):
    """空间向量两件套：位置向量 = 三次位移的合成；法向量是平面的方向盘。"""

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
        self.set_camera_orientation(phi=65 * DEGREES, theta=-65 * DEGREES)
        title = Text("空间向量：把几何翻译成坐标", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("空间里点 P 的位置，怎么描述？", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        # ===== 坐标轴 =====
        axes = ThreeDAxes(x_range=[0, 4, 1], y_range=[0, 3, 1],
                          z_range=[0, 3, 1],
                          x_length=4, y_length=3, z_length=3,
                          axis_config={"color": GREY_B,
                                       "stroke_width": 2})
        self.play(Create(axes), run_time=1.4)
        self.wait(0.6)

        # ===== 三次位移合成 =====
        p = np.array([PX, PY, PZ])
        axes_c = axes.get_origin() if hasattr(axes, "get_origin") \
            else axes.coords_to_point(0, 0, 0)
        o = axes.coords_to_point(0, 0, 0)
        p3 = axes.coords_to_point(PX, PY, PZ)
        pxy = axes.coords_to_point(PX, PY, 0)

        self.set_note("先沿 x 轴走 2 步（红）")
        step_x = Arrow3D(o, axes.coords_to_point(PX, 0, 0),
                         color=RED, thickness=0.02)
        self.play(FadeIn(step_x), run_time=1.0)
        self.set_note("再沿 y 方向走 1.2 步（青）")
        step_y = Arrow3D(axes.coords_to_point(PX, 0, 0), pxy,
                         color=TEAL, thickness=0.02)
        self.play(FadeIn(step_y), run_time=1.0)
        self.set_note("最后竖直爬 2 步（蓝）——到达 P")
        step_z = Arrow3D(pxy, p3, color=BLUE, thickness=0.02)
        self.play(FadeIn(step_z), run_time=1.0)
        dot_p = Dot(p3, color=GOLD, radius=0.09)
        self.play(FadeIn(dot_p, scale=0.4), run_time=0.6)
        self.wait(1.2)

        self.set_note("三支位移首尾相接，合成一支：位置向量 OP")
        vec = Arrow3D(o, p3, color=GOLD, thickness=0.035)
        self.play(FadeIn(vec, scale=0.6), run_time=1.0)
        self.wait(1.0)
        self.set_note("OP = (2, 1.2, 2)——坐标就是三次位移的账单")
        self.wait(2.4)
        # 垂足虚线：P 到 xOy 面
        drop = DashedLine(p3, pxy, color=GREY_B, dash_length=0.12)
        self.play(Create(drop), run_time=0.8)
        self.set_note("P 到底面的投影，就是「先走两步再走一步」的终点")
        self.wait(2.2)

        # ===== 法向量是平面的方向盘 =====
        for m in (step_x, step_y, step_z, vec, dot_p, drop):
            self.play(FadeOut(m), run_time=0.5)
        self.set_note("换个主角：平面的方向，谁来描述？")
        tilt = ValueTracker(0.0)

        def plane_now():
            sq = Square(side_length=3.2, fill_color=TEAL,
                        fill_opacity=0.35, stroke_color=TEAL,
                        stroke_width=2)
            sq.rotate(tilt.get_value(), axis=RIGHT)
            sq.shift([1.2, 0.6, 1.2])
            return sq

        def normal_now():
            n = np.array([0, -np.sin(tilt.get_value()),
                          np.cos(tilt.get_value())])
            base = np.array([1.2, 0.6, 1.2])
            return Arrow3D(base, base + 1.6 * n, color=GOLD,
                           thickness=0.03)

        plane_m = always_redraw(plane_now)
        normal_m = always_redraw(normal_now)
        self.play(FadeIn(plane_m), FadeIn(normal_m), run_time=1.0)
        self.wait(1.0)
        self.set_note("金色箭头是法向量：垂直于平面，管它的朝向")
        self.play(tilt.animate.set_value(40 * DEGREES), run_time=2.4)
        self.set_note("法向量往哪边倒，平面就往哪边躺")
        self.play(tilt.animate.set_value(-25 * DEGREES), run_time=2.4)
        self.play(tilt.animate.set_value(15 * DEGREES), run_time=1.6)
        self.wait(1.2)
        self.set_note("证垂直、算夹角、求距离——都翻译成向量的运算")
        self.wait(2.4)
        self.set_note("这就是解析几何的立体版：几何不动手，坐标来算账")
        self.wait(2.6)
