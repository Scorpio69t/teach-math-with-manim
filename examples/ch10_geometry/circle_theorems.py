from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）
C0 = LEFT * 3.3 + UP * 0.1
R = 2.0                   # 圆半径（场景单位）


def on_circle(ang_deg, r=R):
    """圆上角度（度）→ 屏幕坐标。"""
    a = np.deg2rad(ang_deg)
    return C0 + r * np.array([np.cos(a), np.sin(a), 0])


def inscribed_deg(a_pos, b_pos, p_pos):
    """圆周角 ∠APB 的度数，用向量点积老老实实算。"""
    u, v = a_pos - p_pos, b_pos - p_pos
    cos_t = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return np.degrees(np.arccos(np.clip(cos_t, -1, 1)))


class CircleTheorems(Scene):
    """垂径定理与圆周角定理：弦会滑，角会转，不变量钉在屏幕上。"""

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
        title = Text("垂径定理与圆周角定理", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("垂直于弦的直径，平分这条弦——垂径定理",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)

        circle = Circle(radius=R, color=GREY_B, stroke_width=3)
        circle.move_to(C0)
        dot_o = Dot(C0, color=C_TEXT)
        lab_o = Text("O", font=FONT, font_size=24, color=C_TEXT)
        lab_o.next_to(dot_o, DL, buff=0.08)
        self.add(title, self.note)
        self.play(Create(circle), FadeIn(dot_o), FadeIn(lab_o),
                  run_time=1.2)

        # ===== 第一幕：垂径定理 =====
        h = ValueTracker(1.4)

        def half_chord():
            return np.sqrt(max(R ** 2 - h.get_value() ** 2, 1e-9))

        chord = always_redraw(lambda: Line(
            C0 + np.array([-half_chord(), h.get_value(), 0]),
            C0 + np.array([half_chord(), h.get_value(), 0]),
            color=TEAL, stroke_width=4))
        diam = DashedLine(C0 + DOWN * R, C0 + UP * R, color=GREY_B)
        foot = always_redraw(lambda: Dot(
            C0 + np.array([0, h.get_value(), 0]), color=GOLD))
        # 直角三角形三边：弦心距 OM、半弦 MA、半径 OA
        tri_legs = always_redraw(lambda: VGroup(
            DashedLine(C0, C0 + np.array([0, h.get_value(), 0]),
                       color=GOLD),
            DashedLine(C0 + np.array([0, h.get_value(), 0]),
                       C0 + np.array([half_chord(), h.get_value(), 0]),
                       color=GOLD),
            Line(C0, C0 + np.array([half_chord(), h.get_value(), 0]),
                 color=RED, stroke_width=3),
        ) if abs(h.get_value()) > 0.03 else VGroup(
            Line(C0, C0 + np.array([half_chord(), h.get_value(), 0]),
                 color=RED, stroke_width=3)))
        rmark = always_redraw(lambda: RightAngle(
            Line(C0 + np.array([0, h.get_value(), 0]), C0),
            Line(C0 + np.array([0, h.get_value(), 0]),
                 C0 + np.array([half_chord(), h.get_value(), 0])),
            length=0.2, color=GOLD, stroke_width=2)
            if abs(h.get_value()) > 0.03 else VGroup())
        num_d = self.pinned(lambda: abs(h.get_value()),
                            np.array([4.55, 2.3, 0]), GOLD, "{:.2f}")
        num_h = self.pinned(half_chord, np.array([4.55, 1.7, 0]),
                            GOLD, "{:.2f}")
        num_chk = self.pinned(
            lambda: h.get_value() ** 2 + half_chord() ** 2,
            np.array([4.55, 1.1, 0]), TEAL, "{:.2f}")
        lab_d = Text("弦心距 d =", font=FONT, font_size=24, color=C_TEXT)
        lab_d.move_to(np.array([4.25, 2.3, 0]), aligned_edge=RIGHT)
        lab_h = Text("半弦 =", font=FONT, font_size=24, color=C_TEXT)
        lab_h.move_to(np.array([4.25, 1.7, 0]), aligned_edge=RIGHT)
        lab_chk = Text("d²+半弦² =", font=FONT, font_size=24,
                       color=C_TEXT)
        lab_chk.move_to(np.array([4.25, 1.1, 0]), aligned_edge=RIGHT)
        lab_r = Text("r = 2，平方和恒等于 r² = 4", font=FONT,
                     font_size=20, color=TEAL)
        lab_r.move_to(np.array([4.9, 0.55, 0]))
        self.play(Create(diam), run_time=0.8)
        self.add(chord, foot, tri_legs, rmark,
                 num_d, num_h, num_chk, lab_d, lab_h, lab_chk, lab_r)
        self.wait(1)

        self.set_note("弦上下滑：d 与半弦此消彼长，平方和钉死在 r²")
        self.play(h.animate.set_value(-1.4), run_time=4,
                  rate_func=linear)
        self.set_note("弦心距、半弦、半径围成直角三角形——勾股定理回岗")
        self.play(h.animate.set_value(0), run_time=2, rate_func=linear)
        self.wait(1)

        # 特例一拍：弦滑成直径，"平分"推不出"垂直"
        slant = DashedLine(C0 + 2 * np.array([np.cos(np.deg2rad(40)),
                                              np.sin(np.deg2rad(40)), 0]),
                           C0 - 2 * np.array([np.cos(np.deg2rad(40)),
                                              np.sin(np.deg2rad(40)), 0]),
                           color=RED)
        self.set_note("弦滑成直径：任意斜直径都平分它，却不垂直")
        self.play(Create(slant), run_time=1)
        self.set_note("所以推论必须写明：平分弦（不是直径）的直径垂直于弦")
        self.wait(2.2)
        self.play(FadeOut(slant), run_time=0.6)

        # ===== 第二幕：圆周角定理 =====
        for mob in (chord, foot, tri_legs, rmark,
                    num_d, num_h, num_chk):
            mob.clear_updaters()
        self.play(FadeOut(chord), FadeOut(foot), FadeOut(tri_legs),
                  FadeOut(rmark), FadeOut(diam),
                  FadeOut(num_d), FadeOut(num_h), FadeOut(num_chk),
                  FadeOut(lab_d), FadeOut(lab_h), FadeOut(lab_chk),
                  FadeOut(lab_r), run_time=0.9)

        a_ang = ValueTracker(210)
        b_ang = ValueTracker(330)
        p_ang = ValueTracker(15)

        def central_deg():
            d = abs(a_ang.get_value() - b_ang.get_value()) % 360
            return min(d, 360 - d)

        def inscr_deg():
            return inscribed_deg(on_circle(a_ang.get_value()),
                                 on_circle(b_ang.get_value()),
                                 on_circle(p_ang.get_value()))

        sides_ab = always_redraw(lambda: VGroup(
            Line(C0, on_circle(a_ang.get_value()), color=TEAL,
                 stroke_width=3),
            Line(C0, on_circle(b_ang.get_value()), color=TEAL,
                 stroke_width=3)))
        central_arc = always_redraw(lambda: Angle(
            Line(C0, on_circle(a_ang.get_value())),
            Line(C0, on_circle(b_ang.get_value())),
            radius=0.6, color=TEAL))
        dot_p = always_redraw(lambda: Dot(
            on_circle(p_ang.get_value()), color=GOLD))
        lab_p = always_redraw(lambda: Text(
            "P", font=FONT, font_size=22, color=GOLD).move_to(
            on_circle(p_ang.get_value()) + 0.35 * normalize(
                on_circle(p_ang.get_value()) - C0)))
        dot_a = always_redraw(lambda: Dot(
            on_circle(a_ang.get_value()), color=TEAL))
        dot_b = always_redraw(lambda: Dot(
            on_circle(b_ang.get_value()), color=TEAL))
        lab_a = always_redraw(lambda: Text(
            "A", font=FONT, font_size=22, color=TEAL).move_to(
            on_circle(a_ang.get_value()) + 0.35 * normalize(
                on_circle(a_ang.get_value()) - C0)))
        lab_b = always_redraw(lambda: Text(
            "B", font=FONT, font_size=22, color=TEAL).move_to(
            on_circle(b_ang.get_value()) + 0.35 * normalize(
                on_circle(b_ang.get_value()) - C0)))
        sides_p = always_redraw(lambda: VGroup(
            Line(on_circle(p_ang.get_value()),
                 on_circle(a_ang.get_value()), color=GOLD,
                 stroke_width=3),
            Line(on_circle(p_ang.get_value()),
                 on_circle(b_ang.get_value()), color=GOLD,
                 stroke_width=3)))
        arc_p = always_redraw(lambda: RightAngle(
            Line(on_circle(p_ang.get_value()),
                 on_circle(a_ang.get_value())),
            Line(on_circle(p_ang.get_value()),
                 on_circle(b_ang.get_value())),
            length=0.28, color=GOLD, stroke_width=3)
            if abs(inscr_deg() - 90) < 0.3 else Angle(
            Line(on_circle(p_ang.get_value()),
                 on_circle(a_ang.get_value())),
            Line(on_circle(p_ang.get_value()),
                 on_circle(b_ang.get_value())),
            radius=0.5, color=GOLD))
        num_c = self.pinned(central_deg, np.array([4.55, 2.3, 0]),
                            TEAL, "{:.0f}°")
        num_i = self.pinned(inscr_deg, np.array([4.55, 1.7, 0]),
                            GOLD, "{:.1f}°")
        lab_c = Text("圆心角 =", font=FONT, font_size=24, color=C_TEXT)
        lab_c.move_to(np.array([4.25, 2.3, 0]), aligned_edge=RIGHT)
        lab_i = Text("圆周角 =", font=FONT, font_size=24, color=C_TEXT)
        lab_i.move_to(np.array([4.25, 1.7, 0]), aligned_edge=RIGHT)
        rel = Text("同弧：圆周角 = ½ × 圆心角", font=FONT,
                   font_size=22, color=C_TEXT)
        rel.move_to(np.array([3.85, 1.0, 0]))

        self.set_note("圆周角 ∠APB：P 在优弧上随便站")
        self.play(FadeIn(sides_ab), FadeIn(central_arc), FadeIn(dot_a),
                  FadeIn(dot_b), FadeIn(lab_a), FadeIn(lab_b),
                  run_time=1)
        self.add(dot_p, lab_p, sides_p, arc_p, num_c, num_i,
                 lab_c, lab_i, rel)
        self.wait(1)

        self.set_note("P 在优弧上滑个遍：读数钉在 60°，圆心角的一半")
        self.play(p_ang.animate.set_value(195), run_time=5,
                  rate_func=linear)
        self.wait(1)

        # 换侧一跳：劣弧上的圆周角
        self.set_note("把 P 请到劣弧上——读数变成 120°，与刚才互补！")
        p_ang.set_value(240)
        self.play(Flash(on_circle(240), color=RED, run_time=0.8))
        rel.become(Text("劣弧站法：½ × (360° − 120°) = 120°",
                        font=FONT, font_size=22, color=RED)
                   .move_to(np.array([3.85, 1.0, 0])))
        self.wait(2.5)

        # 第三幕：AB 拉成直径，圆周角定格 90°
        self.set_note("把 AB 拉成直径：圆心角 180°，圆周角呢？")
        self.play(a_ang.animate.set_value(180),
                  b_ang.animate.set_value(360), run_time=2.5,
                  rate_func=linear)
        self.set_note("90°——直径所对的圆周角是直角，见直径想直角")
        rel.become(Text("直径：圆心角 180° ÷ 2 = 90°",
                        font=FONT, font_size=22, color=GOLD)
                   .move_to(np.array([3.85, 1.0, 0])))
        self.wait(2.5)
