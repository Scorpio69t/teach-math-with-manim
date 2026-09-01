from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

D = 0.62                  # 点阵间距
ORIGIN = LEFT * 3.2 + UP * 2.0   # 点阵左上角


def dot_at(row, col, color=C_TEXT):
    """第 row 层第 col 个点（row、col 从 0 计），层向下堆。"""
    return Dot(ORIGIN + RIGHT * col * D + DOWN * row * D,
               radius=0.11, color=color)


class FigurateNumbers(Scene):
    """三角形数逐层生长，两个三角形数拼成矩形：T_n = n(n+1)/2。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("三角形数：会生长的点阵", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("第一层只有 1 个点", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 数值面板（右上角） =====
        p_title = Text("点阵账本", font=FONT, font_size=24,
                       weight=BOLD, color=C_TEXT)
        p_title.move_to([3.4, 2.9, 0], aligned_edge=LEFT)
        row_layer = self._pinned("层数 n =", np.array([3.0, 2.3, 0]),
                                 fmt="{:.0f}", getter=lambda: 0)
        row_new = self._pinned("本层新增 =", np.array([3.0, 1.8, 0]),
                               fmt="{:.0f}", getter=lambda: 0)
        row_total = self._pinned("总数 T =", np.array([3.0, 1.3, 0]),
                                 color=GOLD, fmt="{:.0f}",
                                 getter=lambda: 0)
        self.play(FadeIn(p_title), FadeIn(row_layer[1]),
                  FadeIn(row_new[1]), FadeIn(row_total[1]),
                  run_time=0.8)

        def set_rows(n_layer, n_new, n_total):
            row_layer[1][1].become(Text("{:.0f}".format(n_layer),
                font=FONT, font_size=26, color=C_TEXT)
                .move_to(row_layer[0], aligned_edge=LEFT))
            row_new[1][1].become(Text("{:.0f}".format(n_new),
                font=FONT, font_size=26, color=C_TEXT)
                .move_to(row_new[0], aligned_edge=LEFT))
            row_total[1][1].become(Text("{:.0f}".format(n_total),
                font=FONT, font_size=26, color=GOLD)
                .move_to(row_total[0], aligned_edge=LEFT))

        # ===== 逐层生长 =====
        tri = VGroup()
        rows_notes = ["第二层 2 个点：每层比上一层多一个",
                      "第三层 3 个点：总数 1+2+3 = 6",
                      "第四层 4 个点：总数 1+2+3+4 = 10"]
        total = 1
        first = dot_at(0, 0, GOLD)
        tri.add(first)
        set_rows(1, 1, 1)
        self.play(FadeIn(first, scale=0.4), run_time=0.7)
        self.wait(1.0)
        for r in range(1, 4):
            new_dots = VGroup(*[dot_at(r, c, GOLD) for c in range(r + 1)])
            total += r + 1
            self.set_note(rows_notes[r - 1])
            self.play(LaggedStart(*[FadeIn(d, scale=0.4)
                                    for d in new_dots], lag_ratio=0.15),
                      run_time=1.2)
            tri.add(*new_dots)
            set_rows(r + 1, r + 1, total)
            self.wait(1.4)

        self.set_note("1、3、6、10……这些数能堆成三角形，叫三角形数")
        self.wait(2.2)

        # ===== 复制一份，倒过来拼 =====
        self.set_note("关键一步：复制一份，旋转 180°")
        twin = tri.copy().set_color(TEAL)
        twin.shift(RIGHT * 1.6)
        self.play(FadeIn(twin), run_time=0.9)
        self.wait(1.2)
        # 旋转 180°：顶点 dot[0] 转到副本右下，各层点变成"右对齐"
        self.play(Rotate(twin, PI, about_point=twin.get_center()),
                  run_time=1.4)
        self.wait(0.8)
        # 顶点最终应落在第 4 层（r=3）第 5 列（c=4），凑成每行 5 个
        goal = (ORIGIN + RIGHT * 4 * D + DOWN * 3 * D) \
            - twin[0].get_center()
        self.set_note("拼上去：每一层都补齐成 5 个点")
        self.play(twin.animate.shift(goal), run_time=1.5)
        self.wait(1.6)

        # ===== 矩形账本 =====
        self.set_note("4 层 × 每层 5 个 = 20 个 = 两份三角形数")
        brace_l = Text("4 层", font=FONT, font_size=24, color=C_TEXT)
        brace_l.next_to(ORIGIN + DOWN * 1.5 * D, LEFT, buff=0.35)
        brace_b = Text("每层 5 个", font=FONT, font_size=24, color=C_TEXT)
        brace_b.next_to(ORIGIN + DOWN * 3 * D + RIGHT * 2 * D, DOWN,
                        buff=0.3)
        self.play(FadeIn(brace_l), FadeIn(brace_b), run_time=0.8)
        self.wait(2.0)

        # ===== 结案：公式 =====
        self.set_note("两份拼成 n×(n+1)，一份就是一半")
        formula = Text("T = n × (n+1) ÷ 2", font=FONT, font_size=30,
                       weight=BOLD, color=GOLD)
        formula.move_to([4.6, 0.5, 0])
        self.play(Write(formula), run_time=1.2)
        self.wait(1.6)
        self.set_note("n = 4 时：4 × 5 ÷ 2 = 10，和一层一层数的一样")
        self.wait(2.0)
        self.set_note("这就是首尾配对求 1 加到 100 的几何底牌")
        self.wait(2.6)

    def _pinned(self, label, row_anchor, getter, color=C_TEXT,
                fmt="{:.2f}"):
        """面板一行：标签钉右缘、数值钉左缘。返回 (lab_anchor, (lab, num))。"""
        lab = Text(label, font=FONT, font_size=26, color=C_TEXT)
        lab.move_to(row_anchor, aligned_edge=RIGHT)
        num_anchor = row_anchor + RIGHT * 0.25
        num = Text(fmt.format(getter()), font=FONT, font_size=26,
                   color=color)
        num.move_to(num_anchor, aligned_edge=LEFT)
        return (num_anchor, VGroup(lab, num))
