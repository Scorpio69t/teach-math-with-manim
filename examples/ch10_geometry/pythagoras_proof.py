from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

A_LEN, B_LEN = 3.0, 4.0   # 3-4-5 直角三角形
L = A_LEN + B_LEN         # 大正方形边长 a+b = 7
S = 0.58                  # 屏幕缩放
CENTER = LEFT * 3.1 + DOWN * 0.15


def P(x, y):
    """局部坐标 (x,y) → 屏幕坐标。"""
    return CENTER + S * np.array([x - L / 2, y - L / 2, 0])


class PythagorasProof(Scene):
    """勾股定理割补法无字证明：四个三角形，两种摆法，面积自己说话。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def ledger(self, lines):
        """右侧面积账：逐行 Text，返回 VGroup。"""
        group = VGroup()
        for i, (txt, color) in enumerate(lines):
            t = Text(txt, font=FONT, font_size=24, color=color)
            t.move_to(np.array([4.0, 1.9 - i * 0.62, 0]))
            group.add(t)
        return group

    def construct(self):
        title = Text("勾股定理：无字证明", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一个 3-4-5 直角三角形：面积 = 3×4÷2 = 6",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # 第一幕：一个 3-4-5 三角形，三边点名
        tri = Polygon(P(0, 0), P(A_LEN, 0), P(0, B_LEN),
                      color=TEAL, stroke_width=4,
                      fill_color=TEAL, fill_opacity=0.35)
        lab_a = Text("a = 3", font=FONT, font_size=24, color=C_TEXT)
        lab_a.move_to(P(1.5, 0) + DOWN * 0.32)
        lab_b = Text("b = 4", font=FONT, font_size=24, color=C_TEXT)
        lab_b.move_to(P(0, 2) + LEFT * 0.55)
        lab_c = Text("c = 5", font=FONT, font_size=24, color=GOLD)
        lab_c.move_to(P(1.5, 2) + UP * 0.28 + RIGHT * 0.42)
        self.play(Create(tri), run_time=1.2)
        self.play(FadeIn(lab_a), FadeIn(lab_b), FadeIn(lab_c),
                  run_time=0.8)
        self.wait(1.2)

        # 第二幕：复制四份，围成边长 (a+b) 的大正方形
        self.set_note("复制 4 份，围成边长 (a+b) 的大正方形")
        big = Polygon(P(0, 0), P(L, 0), P(L, L), P(0, L),
                      color=GREY_B, stroke_width=3)
        tri_b = Polygon(P(7, 0), P(7, 3), P(3, 0),
                        color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.35)
        tri_c = Polygon(P(7, 7), P(4, 7), P(7, 3),
                        color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.35)
        tri_d = Polygon(P(0, 7), P(0, 4), P(4, 7),
                        color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.35)
        self.play(Create(big), run_time=1)
        self.play(*[FadeIn(t) for t in (tri_b, tri_c, tri_d)],
                  run_time=1.2)
        self.wait(0.8)

        # 中间空出的倾斜正方形：边长 c
        self.set_note("中间空出的四边形：四边都是 c，四角都是直角——是正方形")
        inner = Polygon(P(3, 0), P(7, 3), P(4, 7), P(0, 4),
                        color=GOLD, stroke_width=4,
                        fill_color=GOLD, fill_opacity=0.12)
        lab_inner = Text("c²", font=FONT, font_size=30,
                         weight=BOLD, color=GOLD)
        lab_inner.move_to(P(3.5, 3.5))
        self.play(Create(inner), FadeIn(lab_inner), FadeOut(lab_a),
                  FadeOut(lab_b), FadeOut(lab_c), run_time=1.2)
        self.wait(1)

        # 第一笔面积账
        self.set_note("第一笔面积账：c² = 49 − 24 = 25")
        ledger1 = self.ledger([
            ("面积账 · 第一种摆法", C_TEXT),
            ("大正方形：(3+4)² = 49", C_TEXT),
            ("4 个三角形：4 × 6 = 24", C_TEXT),
            ("中间空白 = 49 − 24 = 25", GOLD),
            ("而空白正好是 c²", GOLD),
        ])
        self.play(Write(ledger1), run_time=1.6)
        self.wait(1.5)

        # 第三幕：同样四个三角形，换一种摆法
        self.set_note("同样 4 个三角形，换一种摆法——面积没动过")
        tgt_b = Polygon(P(7, 7), P(3, 7), P(7, 4),
                        color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.35)
        tgt_c = Polygon(P(3, 4), P(0, 4), P(3, 0),
                        color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.35)
        tgt_d = Polygon(P(3, 4), P(7, 4), P(3, 7),
                        color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.35)
        self.play(FadeOut(inner), FadeOut(lab_inner), run_time=0.8)
        self.play(Transform(tri_b, tgt_b), Transform(tri_c, tgt_c),
                  Transform(tri_d, tgt_d), run_time=2.5)
        self.wait(0.8)

        # 空白变成两个小正方形：a² 和 b²
        self.set_note("空白变成两个小正方形：a² = 9，b² = 16")
        sq_a = Polygon(P(0, 4), P(3, 4), P(3, 7), P(0, 7),
                       color=GOLD, stroke_width=4,
                       fill_color=GOLD, fill_opacity=0.12)
        sq_b = Polygon(P(3, 0), P(7, 0), P(7, 4), P(3, 4),
                       color=GOLD, stroke_width=4,
                       fill_color=GOLD, fill_opacity=0.12)
        lab_a2 = Text("a²", font=FONT, font_size=26, weight=BOLD,
                      color=GOLD).move_to(P(1.5, 5.5))
        lab_b2 = Text("b²", font=FONT, font_size=26, weight=BOLD,
                      color=GOLD).move_to(P(5, 2))
        self.play(Create(sq_a), Create(sq_b), FadeIn(lab_a2),
                  FadeIn(lab_b2), run_time=1.4)
        self.wait(1)

        # 第二笔面积账 + 收束
        self.set_note("空白必然相等：c² = a² + b²。证毕")
        ledger2 = self.ledger([
            ("面积账 · 第二种摆法", C_TEXT),
            ("大正方形：还是 49", C_TEXT),
            ("4 个三角形：还是 24", C_TEXT),
            ("空白 = a² + b² = 9 + 16 = 25", GOLD),
            ("两次空白必相等", GOLD),
        ])
        self.play(FadeOut(ledger1), Write(ledger2), run_time=1.4)
        banner = Text("c² = a² + b²，即 25 = 9 + 16 ✓",
                      font=FONT, font_size=30, weight=BOLD, color=GOLD)
        banner.move_to(UP * 2.9)
        box = SurroundingRectangle(banner, color=GOLD, buff=0.25)
        self.play(FadeIn(banner), Create(box), run_time=1.2)
        self.wait(2)
