"""模板：格阵计数（方格阵 + 逐圈 L 形增量 + 读数翻牌）

用法：改增量规则与读数算式；「新圈红入 → 读数确认 → 染金并入」的归纳演法不要动。
演示内容：1+3+5+…+(2n-1) = n²——每圈 L 形恰好 2k+1 格，k 跑到 4。

渲染：manim -pqh grid_counting.py GridCounting
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55
R1_POS = [3.4, 2.5, 0]
VERDICT_POS = [0, -2.75, 0]

CELL = 0.46                # 方格边长
GRID0 = [-0.6, -1.3, 0]    # 方格阵左下角
K_MAX = 3                  # 圈数上限：1×1 → (K_MAX+1)×(K_MAX+1)


def cell(i, j, color):
    """第 i 列第 j 行的一格（左下角原点）。"""
    s = Square(side_length=CELL, color=color, fill_opacity=0.85,
               stroke_width=1.5)
    s.move_to([GRID0[0] + (i + 0.5) * CELL,
               GRID0[1] + (j + 0.5) * CELL, 0])
    return s


class GridCounting(Scene):
    """节奏分镜：
    | 段落 | 时长 | 画面动作 | 讲解要点 |
    | 奠基 | 4 s  | 一粒金格，1 = 1² | 起点成立 |
    | 递推 | 12 s | 三圈 L 形：红入→读数→染金 | 每圈恰 2k+1 格 |
    | 结案 | 4 s  | verdict 定格 | 奇数和是平方数 |
    """

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("连续奇数相加，为什么总是平方数？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一粒格子就是 1——往外套圈看", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        gread = Text("", font=FONT, font_size=26, color=C_TEXT)
        gread.move_to(R1_POS, aligned_edge=RIGHT)
        self.add(gread)

        base = VGroup(cell(0, 0, GOLD))
        gread.become(Text("1 = 1²", font=FONT, font_size=26, color=GOLD)
                     .move_to(R1_POS, aligned_edge=RIGHT))
        self.play(FadeIn(base), run_time=0.6)
        self.set_note("奠基：1 就是 1²")
        self.wait(1.4)

        squares = VGroup(base)
        total = 1
        for k in range(1, K_MAX + 1):
            # k×k → (k+1)×(k+1)：下边 k+1 格 + 右边 k 格，角格不重复
            new_cells = VGroup(
                *[cell(i, k, RED) for i in range(k + 1)],
                *[cell(k, j, RED) for j in range(k)])
            total += 2 * k + 1   # 读数与画面同源：增量公式现算
            self.play(FadeIn(new_cells, lag_ratio=0.15), run_time=0.9)
            gread.become(Text(
                f"{total} = {k + 1}²（+{2 * k + 1} 格）", font=FONT,
                font_size=26, color=C_TEXT).move_to(R1_POS,
                                                    aligned_edge=RIGHT))
            self.set_note(f"第 {k + 1} 圈 L 形恰好 {2 * k + 1} 格："
                          f"{k}² 补成 {k + 1}²")
            self.wait(1.3)
            self.play(new_cells.animate.set_color(GOLD), run_time=0.5)
            squares.add(new_cells)

        self.set_note("每圈都是奇数格——传递步在方格上数得出")
        self.wait(2.0)

        verdict = Text("1+3+5+…+(2n−1) = n²：每圈 L 都是下一个奇数",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("数格子就是归纳法：奠基一粒，传递一圈")
        self.wait(2.8)
