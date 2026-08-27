from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2     # 注释条固定锚点（AGENTS.md §6.1 铁律）


class ThreeDBasics(ThreeDScene):
    """三维世界第一课：三根轴、一个点、会动的机位。"""

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
        # 钉在屏幕上的 2D 文字：不参与三维旋转，永远正对读者
        title = Text("三维世界第一课", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("三根轴，两两垂直", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        # 初始机位：phi 俯仰角（压多低），theta 水平角（绕多远）
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                          z_range=[-1, 4, 1],
                          x_length=6, y_length=6, z_length=4,
                          axis_config={"color": GREY_B, "stroke_width": 2},
                          tips=False)
        self.play(Create(axes), run_time=1.5)

        # 读出点 P(2, 1, 3)：先沿底面走，再竖直爬升
        c2p = axes.coords_to_point
        P = Dot3D(point=c2p(2, 1, 3), color=GOLD, radius=0.09)
        foot = Dot3D(point=c2p(2, 1, 0), color=GREY_B, radius=0.06)
        guide_xy = DashedLine(c2p(0, 0, 0), c2p(2, 1, 0), color=GREY_B)
        guide_z = DashedLine(c2p(2, 1, 0), c2p(2, 1, 3), color=GOLD)
        self.set_note("读点 P(2,1,3)：底面投影，再竖起高度")
        self.play(Create(guide_xy), FadeIn(foot), run_time=1.2)
        self.play(Create(guide_z), FadeIn(P), run_time=1.2)
        self.wait(1)

        # 换机位：同一个点，换个角度看——三维读图的核心训练
        self.set_note("同一个点，换个机位再看一眼")
        self.move_camera(phi=40 * DEGREES, theta=-10 * DEGREES,
                         run_time=2.5)
        self.wait(1.5)
