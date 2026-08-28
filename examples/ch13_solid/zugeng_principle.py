from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（三维场景用 fixed-frame 钉屏）

N_DISCS = 12              # 硬币片数
R_DISC = 1.0              # 硬币半径
H_DISC = 0.16             # 硬币厚度
STACK_X = -3.4            # 硬币堆的 x 位置


class ZugengPrinciple(ThreeDScene):
    """祖暅原理：一摞硬币推斜了体积不变——「幂势既同，则积不容异」。
    右侧推导：半球与「圆柱挖圆锥」截面面积相等 → 球体积 4/3 πR³。"""

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
        self.set_camera_orientation(phi=72 * DEGREES, theta=-80 * DEGREES)
        title = Text("祖暅原理：摞起来的硬币", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一摞硬币，整整齐齐", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add_fixed_in_frame_mobjects(title, self.note)

        # ===== 硬币堆 =====
        k = ValueTracker(0.0)   # 0 = 直摞，1 = 推斜
        discs = VGroup()
        for i in range(N_DISCS):
            d = Cylinder(radius=R_DISC, height=H_DISC,
                         resolution=(2, 16),
                         fill_color=GOLD if i % 2 == 0 else TEAL,
                         fill_opacity=0.95, stroke_color=WHITE,
                         stroke_width=1)
            idx = i

            def place(m, idx=idx):
                m.move_to([STACK_X + k.get_value() * idx * 0.16,
                           0, idx * H_DISC])
            d.add_updater(place)
            discs.add(d)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6)
                                for d in discs], lag_ratio=0.08),
                  run_time=2.2)
        self.wait(1.2)

        # ===== 推斜 =====
        self.set_note("用手一推：每片平移一点，摞子斜了")
        self.play(k.animate.set_value(1.0), run_time=2.8)
        self.wait(1.4)
        self.set_note("变了吗？每片的面积没变，每片的高度没变")
        self.wait(2.0)
        self.set_note("所以体积没变——幂势既同，则积不容异")
        self.play(k.animate.set_value(0.35), run_time=1.6)
        self.wait(1.0)

        # ===== 右侧：祖暅原理推球体积（钉屏 2D 推导板） =====
        self.set_note("同一招，推出球的体积：半球 vs 圆柱挖圆锥")
        panel = VGroup()
        p_title = Text("祖暅原理推球体积", font=FONT, font_size=24,
                       weight=BOLD, color=C_TEXT)
        p_title.move_to([3.45, 3.0, 0], aligned_edge=LEFT)
        steps = [
            "高度 d 处水平截一刀：",
            "半球截面：π(R²−d²)",
            "圆柱挖圆锥：πR²−πd²",
            "截面积相等——幂势既同！",
            "V半球 = πR³−⅓πR³",
            "= ⅔πR³",
            "V球 = 4/3 πR³",
        ]
        for i, s in enumerate(steps):
            line = Text(s, font=FONT, font_size=19,
                        color=GOLD if i in (4, 5, 6) else C_TEXT)
            line.move_to([3.45, 2.35 - i * 0.5, 0], aligned_edge=LEFT)
            panel.add(line)
        self.add_fixed_in_frame_mobjects(p_title)
        self.play(FadeIn(p_title), run_time=0.6)
        for line in panel:
            self.add_fixed_in_frame_mobjects(line)  # 推导板也要钉屏，否则透视躺地上
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.9)
        self.wait(1.2)

        # ===== 结案 =====
        self.set_note("一千五百年前的积分思想：截面积定，体积就定")
        self.wait(2.4)
        self.set_note("刘徽没能解决的球体积，祖暅用「幂势既同」拿下了")
        self.wait(2.6)
