from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

# 3-4-5 相似族：坡角 arctan(0.75) ≈ 36.87°
A0 = np.array([-3.2, -1.6, 0])   # 角 A 的顶点（缩放不动点）
L0, H0 = 5.0, 3.75               # 基准水平距离 / 铅直高度，比值 0.75


class SlopeToRatio(Scene):
    """锐角三角比的引入：坡面可大可小，坡度纹丝不动——比值由角决定。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def pinned_pair(self, label, getter, row_anchor, color=GOLD,
                    fmt="{:.2f}"):
        """面板一行：标签钉右缘、数值钉左缘（数值变长不挤压标签）。"""
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

    def construct(self):
        k = ValueTracker(1.0)     # 相似缩放比例

        def verts():
            s = k.get_value()
            return (A0,
                    A0 + RIGHT * L0 * s,
                    A0 + RIGHT * L0 * s + UP * H0 * s)

        title = Text("从坡度到角度：比值是谁决定的？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一段斜坡：水平前进 5.00 米，升高 3.75 米",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 搭台：直角三角形（坡面） =====
        tri = always_redraw(lambda: Polygon(
            *verts(), color=TEAL, stroke_width=4,
            fill_color=TEAL, fill_opacity=0.12))
        base = always_redraw(lambda: Line(
            verts()[0], verts()[1], color=C_TEXT, stroke_width=3))
        height = always_redraw(lambda: DashedLine(
            verts()[1], verts()[2], color=GOLD, stroke_width=3))

        def angle_arc():
            s = k.get_value()
            r = min(0.9, 0.9 * s)
            return Arc(radius=r, start_angle=0,
                       angle=np.arctan2(H0, L0),
                       arc_center=A0, color=GOLD, stroke_width=3)

        arc = always_redraw(angle_arc)
        lab_a = always_redraw(lambda: Text(
            "A", font=FONT, font_size=28, color=GOLD
        ).move_to(A0 + RIGHT * (1.25 * k.get_value()) + UP * 0.35
                  * k.get_value()))
        right_mark = always_redraw(lambda: Square(
            side_length=0.28, color=C_TEXT, stroke_width=2
        ).move_to(verts()[1] + LEFT * 0.14 + UP * 0.14))

        self.play(Create(tri), run_time=1.5)
        self.play(Create(base), Create(height), Create(right_mark),
                  Create(arc), FadeIn(lab_a), run_time=1.2)

        # 边长标签（随缩放漂移）
        lab_l = always_redraw(lambda: Text(
            "水平 l = {:.2f}".format(L0 * k.get_value()),
            font=FONT, font_size=24, color=C_TEXT
        ).move_to((verts()[0] + verts()[1]) / 2 + DOWN * 0.42))
        lab_h = always_redraw(lambda: Text(
            "高 h = {:.2f}".format(H0 * k.get_value()),
            font=FONT, font_size=24, color=GOLD
        ).move_to(verts()[1] + UP * (H0 * k.get_value() * 0.22)
                  + RIGHT * 1.15))
        self.play(FadeIn(lab_l), FadeIn(lab_h), run_time=0.8)
        self.wait(0.6)

        # ===== 数值面板（右侧，两列钉缘） =====
        px = 4.6
        p_title = Text("坡度 = 高 ÷ 水平", font=FONT, font_size=26,
                       weight=BOLD, color=C_TEXT)
        p_title.move_to(np.array([3.1, 2.7, 0]), aligned_edge=LEFT)
        row1 = self.pinned_pair("h =", lambda: H0 * k.get_value(),
                                np.array([px, 2.05, 0]))
        row2 = self.pinned_pair("l =", lambda: L0 * k.get_value(),
                                np.array([px, 1.45, 0]))
        ratio = self.pinned_pair("h ÷ l =", lambda: H0 / L0,
                                 np.array([px, 0.65, 0]), color=GOLD)
        self.play(FadeIn(p_title), FadeIn(row1), FadeIn(row2),
                  FadeIn(ratio), run_time=0.8)
        self.wait(0.8)

        # ===== 第一幕：放大——坡变陡了吗？ =====
        self.set_note("把斜坡放大到 1.4 倍：更高、更长，也更陡吗？")
        self.play(k.animate.set_value(1.4), run_time=2.5,
                  rate_func=smooth)
        self.wait(1.0)
        self.set_note("高度和水平距离都在涨，但坡度的读数——钉死了")
        self.play(Indicate(ratio, color=GOLD, scale_factor=1.15),
                  run_time=1.0)
        self.wait(1.0)

        # ===== 第二幕：缩小 =====
        self.set_note("再缩小到 0.7 倍：坡变平缓了吗？看读数")
        self.play(k.animate.set_value(0.7), run_time=2.5,
                  rate_func=smooth)
        self.wait(1.0)
        self.play(Indicate(ratio, color=GOLD, scale_factor=1.15),
                  run_time=0.8)

        # ===== 第三幕：点破——相似三角形 =====
        self.play(k.animate.set_value(1.0), run_time=1.5,
                  rate_func=smooth)
        self.set_note("三个三角形大小不同，但彼此相似——角 A 没有变")
        self.play(Indicate(arc, color=GOLD), Indicate(lab_a, color=GOLD),
                  run_time=1.2)
        self.wait(1.2)

        # ===== 结案：比值有了名字 =====
        self.set_note("比值只跟着角走——它配拥有一个名字")
        box = VGroup(
            Text("tan A = 对边 ÷ 邻边", font=FONT, font_size=26,
                 color=GOLD),
            Text("sin A = 对边 ÷ 斜边", font=FONT, font_size=25,
                 color=C_TEXT),
            Text("cos A = 邻边 ÷ 斜边", font=FONT, font_size=25,
                 color=C_TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        box.move_to(np.array([1.95, -2.1, 0]), aligned_edge=LEFT)
        frame_box = SurroundingRectangle(box, color=GOLD, buff=0.25,
                                         stroke_width=2)
        self.play(FadeIn(box), run_time=1.2)
        self.set_note("正切、正弦、余弦：三个比值，都是角 A 的指纹")
        self.play(Create(frame_box), run_time=0.8)
        self.wait(2.5)
