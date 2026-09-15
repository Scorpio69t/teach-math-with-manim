from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）


def zh(s, size=26, color=C_TEXT, bold=False):
    """中文文本（公式一律用 MathTex，不进这里）。"""
    return Text(s, font=FONT, font_size=size,
                weight=BOLD if bold else NORMAL, color=color)


def mix(parts, size=26, color=C_TEXT, math_scale=0.9):
    """中文 + 公式混排：parts 交错给出 ("t", 文本) / ("m", LaTeX)。"""
    group = VGroup()
    for kind, s in parts:
        if kind == "t":
            group.add(zh(s, size, color))
        else:
            group.add(MathTex(s, color=color).scale(math_scale))
    return group.arrange(RIGHT, buff=0.10)


U = 0.7                    # 单位 1 的屏幕长度
CENTER = np.array([-0.3, 0.7, 0])   # 复平面原点（给螺线留生长空间）
STEPS = 12
DEG = 25                   # 每步转角
RATIO = 1.15               # 每步模长倍数


class ComplexSpiral(Scene):
    """复数乘法 = 旋转 + 缩放：连乘 w 十二次，等角螺线浮现。"""

    def set_note(self, msg):
        if isinstance(msg, str):          # 纯中文注释条
            self.note.become(zh(msg).move_to(NOTE_POS))
        else:                             # 中文 + 公式混排
            self.note.become(mix(msg).move_to(NOTE_POS))

    def screen(self, z):
        """复数 → 屏幕坐标。"""
        return CENTER + U * np.array([z.real, z.imag, 0])

    def construct(self):
        title = zh("复数乘法在干什么？", 32, bold=True)
        title.to_corner(UL, buff=0.5)
        self.note = mix([("m", "z = 1"),
                         ("t", " 出发，每次乘同一个 "),
                         ("m", "w = 1.15 \times e^{i\cdot 25^\circ}")])
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 极简坐标轴 =====
        ax_x = Line(CENTER + [-3.4, 0, 0], CENTER + [3.6, 0, 0],
                    color=GREY_B, stroke_width=1.5)
        ax_y = Line(CENTER + [0, -3.0, 0], CENTER + [0, 2.6, 0],
                    color=GREY_B, stroke_width=1.5)
        self.play(Create(ax_x), Create(ax_y), run_time=0.8)

        # ===== 面板 =====
        panel = VGroup(
            Text("每次：转 25°", font=FONT, font_size=24, color=TEAL),
            Text("长度 ×1.15", font=FONT, font_size=24, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel.move_to([4.6, 2.4, 0], aligned_edge=RIGHT)
        self.play(FadeIn(panel), run_time=0.7)

        # ===== 起点 z0 = 1 =====
        z = 1 + 0j
        w = RATIO * np.exp(1j * np.deg2rad(DEG))
        arrow = Arrow(CENTER, self.screen(z), buff=0,
                      color=GOLD, stroke_width=5,
                      max_tip_length_to_length_ratio=0.15)
        d0 = Dot(self.screen(z), radius=0.07, color=GOLD)
        lab0 = MathTex("z_0 = 1", color=GOLD).scale(0.8)
        lab0.next_to(d0, DOWN, buff=0.18)
        self.play(GrowArrow(arrow), FadeIn(d0), FadeIn(lab0), run_time=0.9)
        self.set_note("盯住箭头：下一步会发生什么？")
        self.wait(1.4)

        # ===== 连乘 12 次 =====
        prev = z
        for k in range(1, STEPS + 1):
            z = z * w
            seg = DashedLine(self.screen(prev), self.screen(z),
                             color=GREY_B, dash_length=0.08,
                             stroke_width=2)
            d = Dot(self.screen(z), radius=0.055,
                    color=TEAL if k % 2 else "#C77DFF")
            self.play(
                arrow.animate.put_start_and_end_on(CENTER, self.screen(z)),
                Create(seg), FadeIn(d),
                run_time=0.75 if k < 4 else 0.55)
            prev = z
            if k == 1:
                self.set_note("转了 25°，同时变长了一点点")
            elif k == 3:
                self.set_note("每一步都是同一个动作：转 25°，×1.15")
            elif k == 7:
                self.set_note("角度在相加，模长在相乘")
            elif k == 11:
                self.set_note("十二个复制粘贴的动作，画出了什么？")

        self.wait(1.2)

        # ===== 点破 =====
        rule = VGroup(
            Text("复数相乘：", font=FONT, font_size=26, color=C_TEXT),
            Text("角度相加，模长相乘", font=FONT, font_size=28,
                 weight=BOLD, color=GOLD),
        ).arrange(DOWN, buff=0.3)
        rule.move_to([3.4, -1.6, 0])
        self.play(FadeIn(rule, shift=UP * 0.3), run_time=0.9)
        self.set_note("这条曲线叫等角螺线——乘法自己会画画")
        self.wait(2.8)
