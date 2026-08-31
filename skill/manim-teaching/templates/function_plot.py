"""模板：函数图像（Axes + ValueTracker 滑参 + 活读数）

用法：改 f(x)、参数含义与读数文案即得新场景；斜率滑杆结构不要动。
演示内容：y = kx 的斜率滑杆——k 从 0.5 到 3 再穿过 0 到 -1，读数同源报 k。

渲染：manim -pqh function_plot.py FunctionPlot
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55
R1_POS = [4.6, 2.4, 0]
VERDICT_POS = [0, -2.75, 0]

K_MIN, K_MAX = -2.0, 3.0   # 滑参行程；参与绘图的参数要远离退化值


def f(x, k):
    """被画函数：参数显式传入，与滑杆同源。"""
    return k * x


class FunctionPlot(Scene):
    """节奏分镜：
    | 段落 | 时长 | 画面动作 | 讲解要点 |
    | 建系 | 4 s  | 坐标系 + k=1 基准线 | 斜率是倾斜的程度 |
    | 滑参 | 10 s | k: 1→3→-1，活读数 | k 大陡、k 负右下 |
    | 结案 | 4 s  | verdict 定格 | k 的符号定方向 |
    """

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("k 变了，直线怎么动？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("捏住斜率滑杆，看直线绕原点转", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        axes = Axes(x_range=[-4, 4, 1], y_range=[-4, 4, 1],
                    x_length=6.4, y_length=4.8,
                    axis_config={"color": GREY_B, "stroke_width": 2},
                    tips=False)
        axes.move_to([-1.2, 0.2, 0])
        k = ValueTracker(1.0)
        graph = always_redraw(lambda: axes.plot(
            lambda x: f(x, k.get_value()), x_range=[-4, 4],
            color=GOLD, stroke_width=4))
        r1 = always_redraw(lambda: Text(
            f"k = {k.get_value():+.1f}", font=FONT, font_size=28,
            color=C_TEXT).move_to(R1_POS, aligned_edge=RIGHT))
        self.play(Create(axes), run_time=1.1)
        self.play(FadeIn(graph), FadeIn(r1), run_time=0.9)
        self.set_note("基准：k = 1，45° 向右上")
        self.wait(1.8)

        self.play(k.animate.set_value(K_MAX), run_time=2.0,
                  rate_func=linear)
        self.set_note("k 变大——直线变陡，绕着原点“拧紧”")
        self.wait(1.6)
        self.play(k.animate.set_value(-1.0), run_time=2.6,
                  rate_func=linear)
        self.set_note("k 穿过 0 变负——方向整个翻成右下")
        self.wait(2.0)

        verdict = Text("k 的大小管陡缓，k 的符号管方向",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("滑参的铁律：图像与读数吃同一个 k")
        self.wait(2.8)
