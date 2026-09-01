from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

S = 3.6                   # 单位正方形边长（场景单位）
SQ = LEFT * 3.4 + DOWN * 0.9   # 正方形左下角
N_TERMS = 6               # 填充 6 项


class SeriesFill(Scene):
    """1/2 + 1/4 + 1/8 + … 依次填进单位正方形：
    每个有限部分和都小于 1；无穷级数的和等于 1。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        new_note = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        if new_note.width > 12.4:
            new_note.scale_to_fit_width(12.4)
        self.note.become(new_note)
        self.note.move_to(NOTE_POS)

    def regions(self):
        """螺旋对半分割：返回 6 个填充矩形及其分数标签。"""
        rects, labels = [], []
        x0, y0, w, h = 0.0, 0.0, 1.0, 1.0   # 剩余区域（归一化）
        fracs = ["1/2", "1/4", "1/8", "1/16", "1/32", "1/64"]
        vertical = True
        for i in range(N_TERMS):
            if vertical:
                rects.append((x0, y0, w / 2, h))
                lx, ly = x0 + w / 4, y0 + h / 2
                x0 += w / 2
                w /= 2
            else:
                rects.append((x0, y0, w, h / 2))
                lx, ly = x0 + w / 2, y0 + h / 4
                y0 += h / 2
                h /= 2
            labels.append((fracs[i], lx, ly))
            vertical = not vertical
        return rects, labels

    def construct(self):
        title = Text("一半的一半：无限加下去会爆吗？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一个面积为 1 的正方形，先填一半",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        square = Square(side_length=S, color=GREY_B, stroke_width=3)
        square.move_to(SQ + np.array([S / 2, S / 2, 0]))
        lab_1 = Text("面积 = 1", font=FONT, font_size=22, color=GREY_B)
        lab_1.next_to(square, DOWN, buff=0.15)
        self.play(Create(square), FadeIn(lab_1), run_time=1.0)
        self.wait(1.2)

        # ===== 右侧：总量水位计 =====
        gx = 3.6                 # 水位计 x
        gy0, gy1 = -2.2, 2.2     # 0 到 1 的纵坐标范围
        gauge = Line([gx, gy0, 0], [gx, gy1, 0], color=GREY,
                     stroke_width=6)
        target = DashedLine([gx - 0.45, gy1, 0], [gx + 0.45, gy1, 0],
                            color=RED, stroke_width=3,
                            dash_length=0.12)
        lab_t = Text("1", font=FONT, font_size=26, color=RED)
        lab_t.next_to(target, RIGHT, buff=0.12)
        lab_g = Text("已填总面积", font=FONT, font_size=22,
                     color=C_TEXT)
        lab_g.move_to([gx, gy1 + 0.55, 0])
        self.play(Create(gauge), Create(target), FadeIn(lab_t),
                  FadeIn(lab_g), run_time=0.9)
        self.wait(0.8)

        def sum_now():
            return self.trk_s.get_value()

        self.trk_s = ValueTracker(0.0)
        water = always_redraw(lambda: Polygon(
            [gx - 0.28, gy0, 0], [gx + 0.28, gy0, 0],
            [gx + 0.28, gy0 + (gy1 - gy0) * sum_now(), 0],
            [gx - 0.28, gy0 + (gy1 - gy0) * sum_now(), 0],
            color=GOLD, fill_color=GOLD, fill_opacity=0.75,
            stroke_width=0))
        num_anchor = np.array([gx + 0.75, gy0 - 0.55, 0])
        sum_lab = Text("S =", font=FONT, font_size=26, color=C_TEXT)
        sum_lab.move_to(num_anchor, aligned_edge=RIGHT)
        sum_num = Text("0.000", font=FONT, font_size=26, color=GOLD)
        sum_num.move_to(num_anchor + RIGHT * 0.2, aligned_edge=LEFT)
        sum_num.add_updater(lambda d: d.become(
            Text("{:.3f}".format(sum_now()), font=FONT, font_size=26,
                 color=GOLD).move_to(num_anchor + RIGHT * 0.2,
                                     aligned_edge=LEFT)))
        self.add(water, sum_lab, sum_num)

        # ===== 逐项填充 =====
        rects, labels = self.regions()
        colors = [GOLD, TEAL, GOLD, TEAL, GOLD, TEAL]
        notes = [
            "填 1/2：水位涨到 0.5",
            "再填剩下的一半：1/4，水位 0.75",
            "再填剩下的一半：1/8，水位 0.875",
            "1/16：每次都只填剩余的一半",
            "1/32：当前有限部分和仍小于 1",
            "1/64：六项已到 0.984，离红线还差一截",
        ]
        partial = 0.0
        for i, ((x0, y0, w, h), (frac, lx, ly)) in enumerate(
                zip(rects, labels)):
            rect = Rectangle(
                width=w * S, height=h * S,
                color=colors[i], fill_color=colors[i],
                fill_opacity=0.7, stroke_width=1.5)
            rect.move_to(SQ + np.array(
                [(x0 + w / 2) * S, (y0 + h / 2) * S, 0]))
            fs = 30 if i < 2 else (24 if i < 4 else 18)
            center = SQ + np.array([lx * S, ly * S, 0])
            if i < 4:
                lab = Text(frac, font=FONT, font_size=fs,
                           color=BLACK, weight=BOLD)
                lab.move_to(center)
                lab_extra = lab
            else:
                # 太小的区域：标签放到正方形右侧，加指引线
                lab = Text(frac, font=FONT, font_size=fs,
                           color=colors[i], weight=BOLD)
                lab.move_to(center + RIGHT * 0.85)
                leader = Line(center, lab.get_left() + LEFT * 0.06,
                              color=colors[i], stroke_width=1.5)
                lab_extra = VGroup(leader, lab)
            partial += 0.5 ** (i + 1)
            self.set_note(notes[i])
            self.play(FadeIn(rect), FadeIn(lab_extra),
                      self.trk_s.animate.set_value(partial),
                      run_time=1.3)
            self.wait(1.2)

        # ===== 结案 =====
        self.set_note("每个有限部分和都小于 1；无穷级数的和等于 1")
        self.wait(2.0)
        self.play(Indicate(target, color=RED), run_time=1.2)
        self.wait(2.0)
        self.set_note("1/2 + 1/4 + 1/8 + … = 1——无限项，有限和，这叫收敛")
        self.wait(2.6)
        self.set_note("换成 1 + 1/2 + 1/3 + … 就填不满任何框：那叫发散")
        self.wait(2.8)
