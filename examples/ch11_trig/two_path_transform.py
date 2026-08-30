from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

X_MIN, X_MAX = -1.2, 7.2          # 自变量范围
PHI = PI / 3                      # 初相 φ
C_PATH_A = TEAL                   # 路线一：先平移后伸缩
C_PATH_B = ORANGE                 # 路线二：先伸缩后平移


class TwoPathTransform(Scene):
    """y=sin(2x+π/3) 的两条变换路线：平移量 π/3 与 π/6，谁对谁错？"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def make_axes(self):
        ax = Axes(x_range=[X_MIN, X_MAX, 1], y_range=[-1.6, 1.6, 1],
                  x_length=10.5, y_length=3.4,
                  axis_config={"color": GREY, "stroke_width": 1.5},
                  tips=False)
        ax.move_to(DOWN * 0.1)
        # 横轴只标 π 的整数倍，保持干净
        labels = VGroup()
        for k in range(0, 3):
            lab = Text("π" if k == 1 else ("2π" if k == 2 else "0"),
                       font=FONT, font_size=20, color=GREY_B)
            lab.next_to(ax.c2p(k * PI, 0), DOWN, buff=0.1)
            labels.add(lab)
        return ax, labels

    def plot(self, ax, f, color):
        return ax.plot(f, x_range=[X_MIN, X_MAX], color=color,
                       stroke_width=4)

    def construct(self):
        title = Text("两条路线，一个终点：平移量为何不一样？",
                     font=FONT, font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("目标：把 y = sin x 变成 y = sin(2x + π/3)",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        ax, ax_labels = self.make_axes()
        self.play(Create(ax), FadeIn(ax_labels), run_time=1.2)

        # ===== 出发：y = sin x =====
        c_sin = self.plot(ax, np.sin, GREY_B)
        formula = Text("y = sin x", font=FONT, font_size=30,
                       weight=BOLD, color=C_TEXT)
        formula.to_corner(UR, buff=0.6).shift(DOWN * 0.35)
        self.play(Create(c_sin), FadeIn(formula), run_time=1.4)
        self.wait(0.8)

        f_final = lambda x: np.sin(2 * x + PHI)

        # ===== 路线一：先平移，后伸缩 =====
        path_tag = Text("路线一：先平移，后伸缩", font=FONT, font_size=28,
                        weight=BOLD, color=C_PATH_A)
        path_tag.to_corner(UR, buff=0.6).shift(UP * 0.15)
        self.play(Transform(formula, Text(
            "y = sin x", font=FONT, font_size=30, weight=BOLD,
            color=C_PATH_A).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            FadeIn(path_tag), run_time=0.8)
        self.wait(0.6)

        self.set_note("第一步：向左平移 π/3 个单位——整个波形搬家")
        c_a1 = self.plot(ax, lambda x: np.sin(x + PHI), C_PATH_A)
        self.play(Transform(c_sin, c_a1), Transform(
            formula, Text("y = sin(x + π/3)", font=FONT, font_size=30,
                          weight=BOLD, color=C_PATH_A
                          ).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            run_time=2.2)
        self.play(Indicate(formula, color=C_PATH_A), run_time=0.8)
        self.wait(1.4)

        self.set_note("第二步：横坐标压缩到 1/2——周期从 2π 变成 π")
        c_a2 = self.plot(ax, f_final, C_PATH_A)
        self.play(Transform(c_sin, c_a2), Transform(
            formula, Text("y = sin(2x + π/3)", font=FONT, font_size=30,
                          weight=BOLD, color=C_PATH_A
                          ).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            run_time=2.2)
        self.set_note("路线一完成：平移量就是 φ = π/3，一步到位")
        self.wait(1.8)

        # ===== 回到起点 =====
        self.set_note("回到 y = sin x，换一条路线再走一遍")
        c_back = self.plot(ax, np.sin, GREY_B)
        self.play(Transform(c_sin, c_back), FadeOut(path_tag),
                  Transform(formula, Text(
                      "y = sin x", font=FONT, font_size=30, weight=BOLD,
                      color=C_TEXT).to_corner(UR, buff=0.6)
                      .shift(DOWN * 0.35)),
                  run_time=1.6)
        self.wait(0.8)

        # ===== 路线二：先伸缩，后平移 =====
        path_tag2 = Text("路线二：先伸缩，后平移", font=FONT,
                         font_size=28, weight=BOLD, color=C_PATH_B)
        path_tag2.to_corner(UR, buff=0.6).shift(UP * 0.15)
        self.play(Transform(formula, Text(
            "y = sin x", font=FONT, font_size=30, weight=BOLD,
            color=C_PATH_B).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            FadeIn(path_tag2), run_time=0.8)

        self.set_note("第一步：先把横坐标压缩到 1/2，得到 y = sin 2x")
        c_b1 = self.plot(ax, lambda x: np.sin(2 * x), C_PATH_B)
        self.play(Transform(c_sin, c_b1), Transform(
            formula, Text("y = sin 2x", font=FONT, font_size=30,
                          weight=BOLD, color=C_PATH_B
                          ).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            run_time=2.2)
        self.wait(1.2)

        self.set_note("关键一步：此时再平移，只移 π/6——不是 π/3！")
        c_b2 = self.plot(ax, f_final, C_PATH_B)
        self.play(Transform(c_sin, c_b2), Transform(
            formula, Text("y = sin 2(x + π/6)", font=FONT, font_size=30,
                          weight=BOLD, color=C_PATH_B
                          ).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            run_time=2.2)
        self.play(Indicate(formula, color=C_PATH_B), run_time=1.0)
        self.wait(1.6)

        # ===== 结案：殊途同归 =====
        self.set_note("sin 2(x + π/6) 展开就是 sin(2x + π/3)——同一条曲线")
        self.play(FadeOut(path_tag2), Transform(
            formula, Text("y = sin(2x + π/3)  ✓", font=FONT,
                          font_size=30, weight=BOLD, color=GOLD
                          ).to_corner(UR, buff=0.6).shift(DOWN * 0.35)),
            run_time=1.0)
        self.play(c_sin.animate.set_color(GOLD), run_time=0.8)

        rule = VGroup(
            Text("先平移后伸缩：平移 φ", font=FONT, font_size=26,
                 color=C_PATH_A),
            Text("先伸缩后平移：平移 φ ÷ ω", font=FONT, font_size=26,
                 color=C_PATH_B),
            Text("平移永远对着 x 说话，不对着 ωx + φ 说话", font=FONT,
                 font_size=26, color=C_TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rule.move_to(np.array([-3.4, -2.35, 0]), aligned_edge=LEFT)
        self.set_note("两条路都对——但平移量不一样，这就是考试埋雷点")
        self.play(FadeIn(rule), run_time=1.2)
        self.wait(2.8)
