"""模板：数轴操作（NumberLine + 残影 + 弧形箭头跳点 + 读数翻牌）

用法：改操作序列（同加/同乘）与读数文案；「残影 → 跳点 → 读数」三步演法不要动。
演示内容：a = 2 经历「+3」「×2」两次操作，读数逐次报出新位置。

渲染：manim -pqh number_line.py NumberLineOps
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55
R1_POS = [4.7, 2.4, 0]
VERDICT_POS = [0, -2.75, 0]

A0 = 2                     # 初始数（基础参数）


class NumberLineOps(Scene):
    """节奏分镜：
    | 段落 | 时长 | 画面动作 | 讲解要点 |
    | 建轴 | 4 s  | 数轴 + 金点 a=2 | 数是数轴上的位置 |
    | 操作1 | 5 s  | 残影 + 平移 +3 | 位置整体右移 |
    | 操作2 | 5 s  | 残影 + 跳点 ×2 | 离原点远了 |
    | 结案 | 4 s  | verdict 定格 | 运算 = 位置操作 |
    """

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("加法和乘法，在数轴上各是什么动作？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("把数看成数轴上的一个点", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        line = NumberLine(x_range=[-6, 12, 1], length=11,
                          color=GREY_B, stroke_width=2,
                          include_ticks=True)
        line.move_to([0, 0.2, 0])
        dot = Dot(line.n2p(A0), radius=0.09, color=GOLD)
        r1 = Text(f"a = {A0}", font=FONT, font_size=26, color=C_TEXT)
        r1.move_to(R1_POS, aligned_edge=RIGHT)
        self.play(Create(line), run_time=1.2)
        self.play(FadeIn(dot), FadeIn(r1), run_time=0.8)
        self.set_note("a = 2：站在 2 这个位置")
        self.wait(1.8)

        def hop(target_num, note, value_text, color=C_TEXT):
            """三步演法：留残影 → 弧箭跳点 → 读数翻牌。"""
            ghost = Dot(dot.get_center(), radius=0.07, color=GREY)
            arr = CurvedArrow(dot.get_center(), line.n2p(target_num),
                              angle=-TAU / 5, color=RED, stroke_width=3,
                              tip_length=0.2)
            self.play(FadeIn(ghost), Create(arr), run_time=0.5)
            self.play(dot.animate.move_to(line.n2p(target_num)),
                      run_time=0.8)
            self.play(FadeOut(arr), run_time=0.3)
            r1.become(Text(value_text, font=FONT, font_size=26,
                           color=color).move_to(R1_POS,
                                                aligned_edge=RIGHT))
            self.set_note(note)

        hop(A0 + 3, "同加 3：整个点向右平移 3 格",
            f"a + 3 = {A0 + 3}")
        self.wait(2.0)
        hop((A0 + 3) * 2, "再乘 2：离原点的距离翻倍",
            f"(a + 3) × 2 = {(A0 + 3) * 2}")
        self.wait(2.0)

        verdict = Text("运算是位置的操作：加是平移，乘是拉伸",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("残影标出来路——每个新位置都有据可查")
        self.wait(2.8)
