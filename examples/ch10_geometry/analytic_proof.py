from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（AGENTS.md §6.1 铁律）

B_LEN, Q_LEN = 4.0, 2.2   # B(b,0)、D(p,q) 的 b 与 q


class AnalyticProof(Scene):
    """坐标化证明：平行四边形对角线互相平分——把"永远成立"算成恒等式。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("坐标化证明：对角线互相平分", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("命题：平行四边形的两条对角线互相平分",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        axes = Axes(x_range=[-1, 7, 1], y_range=[-1, 4, 1],
                    x_length=6.6, y_length=4.4,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to(LEFT * 3.3 + DOWN * 0.4)
        self.add(title, self.note)
        self.play(Create(axes), run_time=1.2)

        p = ValueTracker(1.0)

        def pt_a():
            return axes.c2p(0, 0)

        def pt_b():
            return axes.c2p(B_LEN, 0)

        def pt_d():
            return axes.c2p(p.get_value(), Q_LEN)

        def pt_c():
            return axes.c2p(B_LEN + p.get_value(), Q_LEN)

        def mid_ac():
            return axes.c2p((B_LEN + p.get_value()) / 2, Q_LEN / 2)

        def mid_bd():
            return axes.c2p((B_LEN + p.get_value()) / 2, Q_LEN / 2)

        para = always_redraw(lambda: Polygon(
            pt_a(), pt_b(), pt_c(), pt_d(),
            color=TEAL, stroke_width=4,
            fill_color=TEAL, fill_opacity=0.15))
        lab_pa = always_redraw(lambda: Text(
            "A(0,0)", font=FONT, font_size=20, color=C_TEXT)
            .next_to(pt_a(), DL, buff=0.08))
        lab_pb = always_redraw(lambda: Text(
            "B(b,0)", font=FONT, font_size=20, color=C_TEXT)
            .next_to(pt_b(), DR, buff=0.08))
        lab_pc = always_redraw(lambda: Text(
            "C(b+p,q)", font=FONT, font_size=20, color=C_TEXT)
            .next_to(pt_c(), UR, buff=0.08))
        lab_pd = always_redraw(lambda: Text(
            "D(p,q)", font=FONT, font_size=20, color=C_TEXT)
            .next_to(pt_d(), UL, buff=0.08))
        self.play(FadeIn(para), run_time=1)
        self.add(lab_pa, lab_pb, lab_pc, lab_pd)
        self.wait(0.8)

        # 右侧推演台：四步出现，与左侧画面一一对应
        steps_x = 3.9
        s1 = Text("① 建系设点：A 压原点，AB 贴 x 轴",
                  font=FONT, font_size=23, color=C_TEXT)
        s1.move_to(np.array([steps_x, 2.5, 0]))
        s2 = MathTex(r"A(0,0),\ B(b,0),\ D(p,q),\ C(b+p,q)",
                     font_size=30)
        s2.move_to(np.array([steps_x, 1.8, 0]))
        s3 = MathTex(
            r"M_{AC}=\left(\tfrac{0+(b+p)}{2},\tfrac{0+q}{2}\right)"
            r"=\left(\tfrac{b+p}{2},\tfrac{q}{2}\right)",
            font_size=30)
        s3.move_to(np.array([steps_x, 1.0, 0]))
        s4 = MathTex(
            r"M_{BD}=\left(\tfrac{b+p}{2},\tfrac{0+q}{2}\right)"
            r"=\left(\tfrac{b+p}{2},\tfrac{q}{2}\right)",
            font_size=30)
        s4.move_to(np.array([steps_x, 0.2, 0]))
        s5 = Text("两式一字不差：中点重合，互相平分，证毕",
                  font=FONT, font_size=23, weight=BOLD, color=GOLD)
        s5.move_to(np.array([steps_x, -0.6, 0]))

        self.set_note("第一步：建系设点——只剩三个自由字母 b、p、q")
        self.play(Write(s1), Write(s2), run_time=1.6)
        self.wait(1)

        # 对角线 AC 与它的中点
        self.set_note("第二步：翻译——对角线 AC 的中点坐标")
        diag_ac = always_redraw(lambda: DashedLine(
            pt_a(), pt_c(), color=GOLD))
        dot_m1 = always_redraw(lambda: Dot(mid_ac(), color=GOLD,
                                           radius=0.09))
        self.play(FadeIn(diag_ac), run_time=0.8)
        self.play(FadeIn(dot_m1), Write(s3), run_time=1.6)
        self.wait(1)

        # 对角线 BD 与它的中点
        self.set_note("第三步：再算 BD 的中点坐标")
        diag_bd = always_redraw(lambda: DashedLine(
            pt_b(), pt_d(), color=RED))
        ring_m2 = always_redraw(lambda: Circle(
            radius=0.16, color=RED, stroke_width=3)
            .move_to(mid_bd()))
        self.play(FadeIn(diag_bd), run_time=0.8)
        self.play(FadeIn(ring_m2), Write(s4), run_time=1.6)
        self.wait(1)

        self.set_note("两个式子一字不差：同一个点——互相平分")
        self.play(Write(s5), Flash(mid_ac(), color=GOLD), run_time=1.4)
        self.wait(1.5)

        # 推歪试验：恒等式级别的相等，不认 p 的具体值
        self.set_note("把 D 往右推：平行四边形歪了，中点咬死不松口")
        self.play(p.animate.set_value(2.6), run_time=3,
                  rate_func=linear)
        self.set_note("坐标化的底气：算出来的相等，是恒等式级别的相等")
        self.play(p.animate.set_value(0.6), run_time=3,
                  rate_func=linear)
        self.wait(2)
