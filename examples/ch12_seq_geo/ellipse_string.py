from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

C_F = 1.8                 # 半焦距 c
A0 = 3.0                  # 初始半长轴 a（绳长一半）


class EllipseString(Scene):
    """两枚钉子一根绳：|PF1|+|PF2| 恒定的点画出的曲线就是椭圆。
    随后收紧绳长演示退化：2a = 2c 成线段，2a < 2c 画不出来。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def b_now(self):
        """当前短半轴，退化值守卫：a < c 时钳到 0。"""
        a = self.trk_a.get_value()
        return np.sqrt(max(a * a - C_F * C_F, 1e-6))

    def p_pos(self):
        t = self.trk_t.get_value()
        a = self.trk_a.get_value()
        return np.array([a * np.cos(t), self.b_now() * np.sin(t), 0])

    def construct(self):
        self.trk_t = ValueTracker(0.0)
        self.trk_a = ValueTracker(A0)
        f1 = np.array([-C_F, 0, 0])
        f2 = np.array([C_F, 0, 0])

        title = Text("拉绳法：一根绳子画出椭圆", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("桌面上钉两枚钉子，就是两个焦点 F1、F2",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 钉子与绳子 =====
        axis_x = Line(LEFT * 4.2, RIGHT * 4.2, color=GREY,
                      stroke_width=1.5)
        axis_y = Line(DOWN * 3.0, UP * 3.0, color=GREY,
                      stroke_width=1.5)
        pin1 = Dot(f1, color=RED, radius=0.09)
        pin2 = Dot(f2, color=RED, radius=0.09)
        lf1 = Text("F1", font=FONT, font_size=24, color=RED)
        lf1.next_to(pin1, DOWN, buff=0.12)
        lf2 = Text("F2", font=FONT, font_size=24, color=RED)
        lf2.next_to(pin2, DOWN, buff=0.12)
        self.play(Create(axis_x), Create(axis_y), run_time=0.9)
        self.play(FadeIn(pin1, scale=0.4), FadeIn(pin2, scale=0.4),
                  FadeIn(lf1), FadeIn(lf2), run_time=0.9)
        self.wait(1.4)

        # 绳子两段 + 铅笔
        seg1 = always_redraw(lambda: Line(
            f1, self.p_pos(), color=GOLD, stroke_width=4))
        seg2 = always_redraw(lambda: Line(
            f2, self.p_pos(), color=GOLD, stroke_width=4))
        pencil = always_redraw(lambda: Dot(self.p_pos(), color=TEAL,
                                           radius=0.1))
        self.set_note("绳长固定为 2a = 6，铅笔把绳绷紧，走到哪画到哪")
        self.play(Create(seg1), Create(seg2), FadeIn(pencil),
                  run_time=1.0)
        self.wait(1.8)

        # ===== 数值面板（右上角） =====
        def d1():
            return float(np.linalg.norm(self.p_pos() - f1))

        def d2():
            return float(np.linalg.norm(self.p_pos() - f2))

        p_title = Text("绳子账本", font=FONT, font_size=24,
                       weight=BOLD, color=C_TEXT)
        p_title.move_to([3.6, 2.9, 0], aligned_edge=LEFT)
        row1 = self._pinned("|PF1| =", d1, np.array([3.2, 2.3, 0]))
        row2 = self._pinned("|PF2| =", d2, np.array([3.2, 1.8, 0]))
        row3 = self._pinned("两段之和 =", lambda: d1() + d2(),
                            np.array([3.2, 1.3, 0]), color=GOLD)
        self.play(FadeIn(p_title), FadeIn(row1), FadeIn(row2),
                  FadeIn(row3), run_time=0.8)
        self.wait(1.0)

        # ===== 画一整圈 =====
        self.set_note("盯住账本：两段各自在变，加起来却纹丝不动")
        trace = TracedPath(self.p_pos, stroke_color=TEAL,
                           stroke_width=4)
        self.add(trace)
        self.play(self.trk_t.animate.set_value(2 * PI),
                  run_time=7.0, rate_func=linear)
        self.wait(1.0)
        self.set_note("到两焦点距离之和恒为 2a——这就是椭圆的定义")
        self.wait(2.4)

        # 轨迹换成随 a 联动的轮廓线，才能看见"瘪下去"的过程
        outline = always_redraw(lambda: Ellipse(
            width=2 * self.trk_a.get_value(),
            height=2 * max(self.b_now(), 0.02),
            color=TEAL, stroke_width=4))
        self.remove(trace)
        self.add(outline)

        # ===== 退化一：2a → 2c，椭圆瘪成线段 =====
        self.set_note("现在把绳子收短：2a 逼近焦距 2c = 3.6")
        self.play(self.trk_a.animate.set_value(C_F),
                  self.trk_t.animate.set_value(3 * PI),
                  run_time=3.5)
        self.wait(1.0)
        self.set_note("2a = 2c 时：铅笔只能在线段 F1F2 上来回蹭")
        seg_degen = Line(f1, f2, color=RED, stroke_width=5)
        self.play(Create(seg_degen), run_time=1.0)
        self.play(self.trk_t.animate.set_value(4 * PI),
                  run_time=2.2, rate_func=linear)
        self.wait(1.2)

        # ===== 退化二：2a < 2c，画不出来 =====
        self.set_note("再短一点试试：2a < 2c——绳子不够长！")
        short1 = Line(f1, f1 + RIGHT * 0.7, color=RED, stroke_width=4)
        short2 = Line(f2, f2 + LEFT * 0.7, color=RED, stroke_width=4)
        mark = Text("✗ 够不着", font=FONT, font_size=28, color=RED,
                    weight=BOLD)
        mark.move_to(UP * 1.2)
        self.play(FadeOut(seg1), FadeOut(seg2), FadeOut(pencil),
                  FadeIn(short1), FadeIn(short2), run_time=0.9)
        self.play(FadeIn(mark, scale=0.5), run_time=0.7)
        self.wait(2.4)

        # ===== 结案 =====
        self.set_note("定义里「大于焦距」不是废话：是椭圆存在的门槛")
        self.wait(2.6)

    def _pinned(self, label, getter, row_anchor, color=C_TEXT,
                fmt="{:.2f}"):
        """面板一行：标签钉右缘、数值钉左缘。"""
        lab = Text(label, font=FONT, font_size=26, color=C_TEXT)
        lab.move_to(row_anchor, aligned_edge=RIGHT)
        num_anchor = row_anchor + RIGHT * 0.25
        num = Text(fmt.format(getter()), font=FONT, font_size=26,
                   color=color)
        num.move_to(num_anchor, aligned_edge=LEFT)
        num.add_updater(lambda d: d.become(
            Text(fmt.format(getter()), font=FONT, font_size=26,
                 color=color).move_to(num_anchor, aligned_edge=LEFT)))
        return VGroup(lab, num)
