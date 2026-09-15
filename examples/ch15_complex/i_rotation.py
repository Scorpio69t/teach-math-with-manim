from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）

U = 2.0                    # 单位 1 的屏幕长度


def zh(s, size=26, color=C_TEXT, bold=False):
    """中文文本（公式一律用 MathTex，不进这里）。"""
    return Text(s, font=FONT, font_size=size,
                weight=BOLD if bold else NORMAL, color=color)


def mix(parts, size=26, color=C_TEXT, math_scale=0.9):
    """中文 + 公式混排：parts 交错给出文本串与 LaTeX 串，返回一个 VGroup。

    纪律：中文走 Text，公式走 MathTex——不把 ^ π θ 之类的符号塞进 Text。
    """
    group = VGroup()
    for kind, s in parts:
        if kind == "t":
            group.add(zh(s, size, color))
        else:
            group.add(MathTex(s, color=color).scale(math_scale))
    return group.arrange(RIGHT, buff=0.10)


class PowerOfI(Scene):
    """i 的幂：乘以 i 就是逆时针转 90°，转两次必然落在 -1 上。"""

    def set_note(self, msg):
        """msg 为 mix() 可接受的 parts 列表。"""
        self.note.become(mix(msg).move_to(NOTE_POS))

    def construct(self):
        title = zh("i 到底是什么？", 32, bold=True)
        title.to_corner(UL, buff=0.5)
        self.note = mix([
            ("t", "课本只有一句话："),
            ("m", "i^2 = -1"),
            ("t", "。背下来，然后做题"),
        ]).move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 复平面（极简坐标轴） =====
        ax_x = Line([-4.6, 0, 0], [4.6, 0, 0], color=GREY_B, stroke_width=2)
        ax_y = Line([0, -3.0, 0], [0, 3.0, 0], color=GREY_B, stroke_width=2)
        xlab = zh("实轴", 22)
        xlab.next_to(ax_x, RIGHT, buff=0.15)
        ylab = zh("虚轴", 22)
        ylab.next_to(ax_y, UP, buff=0.15)
        self.play(Create(ax_x), Create(ax_y), FadeIn(xlab), FadeIn(ylab),
                  run_time=1.0)

        # 关键点标签（1 先出场，其余随转随落）
        lab_1 = zh("1", 26)
        lab_1.move_to([U, -0.45, 0])
        self.add(lab_1)

        # ===== 金色箭头：从 1 出发 =====
        arrow = Arrow(ORIGIN, [U, 0, 0], buff=0,
                      color=GOLD, stroke_width=6,
                      max_tip_length_to_length_ratio=0.12)
        self.play(GrowArrow(arrow), run_time=0.9)
        self.set_note([("t", "把「乘以 i」想成一个动作：逆时针转 90°")])
        self.wait(1.6)

        stops = [
            (PI / 2,  [0, U, 0],   [0.45, U, 0],   "i",  TEAL,
             [("t", "转 90°："), ("m", "1 \\times i = i")]),
            (PI / 2,  [-U, 0, 0],  [-U, -0.45, 0], "-1", ORANGE,
             [("t", "再转 90°："), ("m", "i \\times i"), ("t", "，落在了 −1 上！")]),
            (PI / 2,  [0, -U, 0],  [0.45, -U, 0],  "-i", "#C77DFF",
             [("t", "第三次："), ("m", "i \\times i \\times i = -i")]),
            (PI / 2,  [U, 0, 0],   None,           None, GOLD,
             [("t", "第四次：回到起点——"), ("m", "i^4 = 1")]),
        ]

        dots = []
        for ang, tip, lab_pos, lab_txt, col, msg in stops:
            self.play(Rotate(arrow, angle=ang, about_point=ORIGIN),
                      run_time=1.4)
            d = Dot(tip, radius=0.09, color=col)
            dots.append(d)
            if lab_txt is not None:
                lab = zh(lab_txt, 26, col)
                lab.move_to(lab_pos)
                self.play(FadeIn(d), FadeIn(lab), run_time=0.5)
            else:
                self.play(FadeIn(d), run_time=0.5)
            self.set_note(msg)
            self.wait(1.4)

        # ===== 结案：i^2 = -1 是几何必然 =====
        self.set_note([("t", "看第二次落点：转两个 90° = 转 180° = 乘以 −1")])
        self.play(Indicate(dots[1], color=ORANGE, scale_factor=1.8),
                  run_time=1.2)
        self.wait(1.6)

        verdict = mix([
            ("m", "i^2 = -1"),
            ("t", "：不是规定，是几何必然"),
        ], size=30, color=GOLD, math_scale=1.0)
        verdict.move_to([0, 2.6, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note([("t", "虚数不虚——它就是「转个身」的名字")])
        self.wait(2.8)
