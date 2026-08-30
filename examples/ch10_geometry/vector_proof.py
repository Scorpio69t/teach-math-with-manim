from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）
C0 = LEFT * 3.2 + UP * 0.05
R = 2.05                  # 圆半径（场景单位）
C_BLUE = "#6EC6FF"


class VectorProof(Scene):
    """向量语言看几何：直径所对圆周角为直角，一行数量积证完。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def pinned(self, getter, anchor, color=GOLD, fmt="{:.2f}", size=30):
        """钉屏数值行：数字钉右缘，become 原地刷新。"""
        num = Text(fmt.format(getter()), font=FONT, font_size=size,
                   color=color)
        num.move_to(anchor, aligned_edge=LEFT)
        num.add_updater(lambda d: d.become(
            Text(fmt.format(getter()), font=FONT, font_size=size,
                 color=color).move_to(anchor, aligned_edge=LEFT)))
        return num

    def construct(self):
        title = Text("向量证明：直径所对的圆周角", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("10.2 的定理：直径所对的圆周角是直角",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        p_ang = ValueTracker(70)

        def pt_p():
            a = np.deg2rad(p_ang.get_value())
            return C0 + R * np.array([np.cos(a), np.sin(a), 0])

        pt_a = C0 + LEFT * R
        pt_b = C0 + RIGHT * R

        circle = Circle(radius=R, color=GREY_B, stroke_width=3)
        circle.move_to(C0)
        diam = DashedLine(pt_a, pt_b, color=GREY_B)
        dot_o = Dot(C0, color=C_TEXT)
        lab_o = Text("O（原点）", font=FONT, font_size=20,
                     color=C_TEXT)
        lab_o.next_to(dot_o, DOWN, buff=0.1)
        lab_a = Text("A", font=FONT, font_size=24, color=TEAL)
        lab_a.next_to(pt_a, LEFT, buff=0.12)
        lab_b = Text("B", font=FONT, font_size=24, color=TEAL)
        lab_b.next_to(pt_b, RIGHT, buff=0.12)
        self.add(title, self.note)
        self.play(Create(circle), Create(diam), FadeIn(dot_o),
                  FadeIn(lab_o), FadeIn(lab_a), FadeIn(lab_b),
                  run_time=1.4)

        # 向量登场：位置向量 p、a、−a，弦向量 PA、PB
        arr_p = always_redraw(lambda: Arrow(
            C0, pt_p(), buff=0, color=GOLD, stroke_width=4,
            max_tip_length_to_length_ratio=0.12))
        lab_p = always_redraw(lambda: Text(
            "p", font=FONT, font_size=26, color=GOLD).move_to(
            (C0 + pt_p()) / 2 + 0.3 * normalize(pt_p() - C0)))
        arr_a = Arrow(C0, pt_b, buff=0, color=TEAL, stroke_width=4,
                      max_tip_length_to_length_ratio=0.12)
        lab_va = Text("a", font=FONT, font_size=26, color=TEAL)
        lab_va.move_to((C0 + pt_b) / 2 + UP * 0.3)
        arr_ma = Arrow(C0, pt_a, buff=0, color=TEAL, stroke_width=4,
                       max_tip_length_to_length_ratio=0.12)
        lab_vma = Text("−a", font=FONT, font_size=26, color=TEAL)
        lab_vma.move_to((C0 + pt_a) / 2 + UP * 0.3)
        arr_pa = always_redraw(lambda: Arrow(
            pt_p(), pt_a, buff=0, color=RED, stroke_width=4,
            max_tip_length_to_length_ratio=0.08))
        arr_pb = always_redraw(lambda: Arrow(
            pt_p(), pt_b, buff=0, color=C_BLUE, stroke_width=4,
            max_tip_length_to_length_ratio=0.08))
        dot_p = always_redraw(lambda: Dot(pt_p(), color=GOLD))
        lab_pp = always_redraw(lambda: Text(
            "P", font=FONT, font_size=24, color=GOLD).move_to(
            pt_p() + 0.38 * normalize(pt_p() - C0)))
        rmark = always_redraw(lambda: RightAngle(
            Line(pt_p(), pt_a), Line(pt_p(), pt_b),
            length=0.26, color=GOLD, stroke_width=3))
        self.play(FadeIn(arr_a), FadeIn(arr_ma), FadeIn(lab_va),
                  FadeIn(lab_vma), run_time=1)
        self.add(arr_p, lab_p, arr_pa, arr_pb, dot_p, lab_pp, rmark)
        self.wait(1)

        # 右侧推演台：一行展开到底
        steps_x = 3.8
        s1 = Text("设 A = −a，B = a，P = p，|p| = |a| = r",
                  font=FONT, font_size=23, color=C_TEXT)
        s1.move_to(np.array([steps_x, 2.5, 0]))
        s2 = MathTex(
            r"\vec{PA}\cdot\vec{PB}"
            r"=(-\vec{a}-\vec{p})\cdot(\vec{a}-\vec{p})",
            font_size=32)
        s2.move_to(np.array([steps_x, 1.7, 0]))
        s3 = MathTex(
            r"=\vec{p}\cdot\vec{p}-\vec{a}\cdot\vec{a}"
            r"=|\vec{p}|^2-|\vec{a}|^2",
            font_size=32)
        s3.move_to(np.array([steps_x, 0.9, 0]))
        s4 = MathTex(r"=r^2-r^2=0", font_size=32, color=GOLD)
        s4.move_to(np.array([steps_x, 0.1, 0]))
        s5 = Text("数量积为 0 即垂直：∠APB = 90°，证毕",
                  font=FONT, font_size=23, weight=BOLD, color=GOLD)
        s5.move_to(np.array([steps_x, -0.7, 0]))

        self.set_note("这次不用圆周角定理——只许用向量")
        self.play(Write(s1), run_time=1.2)
        self.wait(0.8)
        self.set_note("PA = −a − p，PB = a − p：数量积摆出来")
        self.play(Write(s2), run_time=1.4)
        self.wait(0.8)
        self.set_note("展开：交叉项 −a·p + p·a 自动抵消")
        self.play(Write(s3), run_time=1.4)
        self.wait(0.8)
        self.set_note("P 在圆上：|p| = r，于是 r² − r² = 0")
        self.play(Write(s4), run_time=1.2)
        self.play(Write(s5), Flash(pt_p(), color=GOLD), run_time=1.4)
        self.wait(1.2)

        # 数值验尸：P 跑起来，两个读数钉死
        def dot_now():
            u, v = pt_a - pt_p(), pt_b - pt_p()
            return float(np.dot(u, v))

        def angle_now():
            u, v = pt_a - pt_p(), pt_b - pt_p()
            cos_t = np.dot(u, v) / (np.linalg.norm(u)
                                    * np.linalg.norm(v))
            return float(np.degrees(np.arccos(
                np.clip(cos_t, -1, 1))))

        num_dot = self.pinned(dot_now, np.array([4.55, -1.6, 0]),
                              RED, "{:.2f}")
        num_ang = self.pinned(angle_now, np.array([4.55, -2.2, 0]),
                              GOLD, "{:.1f}°")
        lab_dot = Text("PA·PB =", font=FONT, font_size=24,
                       color=C_TEXT)
        lab_dot.move_to(np.array([4.25, -1.6, 0]), aligned_edge=RIGHT)
        lab_ang = Text("∠APB =", font=FONT, font_size=24,
                       color=C_TEXT)
        lab_ang.move_to(np.array([4.25, -2.2, 0]), aligned_edge=RIGHT)
        self.add(num_dot, num_ang, lab_dot, lab_ang)

        self.set_note("P 在圆上随便跑：两个读数钉死在 0.00 与 90.0°")
        self.play(p_ang.animate.set_value(150), run_time=3.5,
                  rate_func=linear)
        self.play(p_ang.animate.set_value(255), run_time=3.5,
                  rate_func=linear)
        self.set_note("同一个定理：几何语言、坐标语言、向量语言，一次看齐")
        self.wait(2.5)
