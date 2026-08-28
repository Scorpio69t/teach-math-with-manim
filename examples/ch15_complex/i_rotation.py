from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

U = 2.0                    # 单位 1 的屏幕长度


class PowerOfI(Scene):
    """i 的幂：乘以 i 就是逆时针转 90°，转两次必然落在 -1 上。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("i 到底是什么？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("课本只有一句话：i^2 = -1。背下来，然后做题",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 复平面（极简坐标轴） =====
        ax_x = Line([-4.6, 0, 0], [4.6, 0, 0], color=GREY_B, stroke_width=2)
        ax_y = Line([0, -3.0, 0], [0, 3.0, 0], color=GREY_B, stroke_width=2)
        xlab = Text("实轴", font=FONT, font_size=22, color=C_TEXT)
        xlab.next_to(ax_x, RIGHT, buff=0.15)
        ylab = Text("虚轴", font=FONT, font_size=22, color=C_TEXT)
        ylab.next_to(ax_y, UP, buff=0.15)
        self.play(Create(ax_x), Create(ax_y), FadeIn(xlab), FadeIn(ylab),
                  run_time=1.0)

        # 关键点标签（1 先出场，其余随转随落）
        lab_1 = Text("1", font=FONT, font_size=26, color=C_TEXT)
        lab_1.move_to([U, -0.45, 0])
        self.add(lab_1)

        # ===== 金色箭头：从 1 出发 =====
        arrow = Arrow(ORIGIN, [U, 0, 0], buff=0,
                      color=GOLD, stroke_width=6,
                      max_tip_length_to_length_ratio=0.12)
        self.play(GrowArrow(arrow), run_time=0.9)
        self.set_note("把「乘以 i」想成一个动作：逆时针转 90°")
        self.wait(1.6)

        stops = [
            (PI / 2,  [0, U, 0],   [0.45, U, 0],   "i",  TEAL,
             "转 90°：1 × i = i"),
            (PI / 2,  [-U, 0, 0],  [-U, -0.45, 0], "-1", ORANGE,
             "再转 90°：i × i，落在了 -1 上！"),
            (PI / 2,  [0, -U, 0],  [0.45, -U, 0],  "-i", "#C77DFF",
             "第三次：i × i × i = -i"),
            (PI / 2,  [U, 0, 0],   None,           None, GOLD,
             "第四次：回到起点——i^4 = 1"),
        ]

        dots = []
        for ang, tip, lab_pos, lab_txt, col, msg in stops:
            self.play(Rotate(arrow, angle=ang, about_point=ORIGIN),
                      run_time=1.4)
            d = Dot(tip, radius=0.09, color=col)
            dots.append(d)
            if lab_txt is not None:
                lab = Text(lab_txt, font=FONT, font_size=26, color=col)
                lab.move_to(lab_pos)
                self.play(FadeIn(d), FadeIn(lab), run_time=0.5)
            else:
                self.play(FadeIn(d), run_time=0.5)
            self.set_note(msg)
            self.wait(1.4)

        # ===== 结案：i^2 = -1 是几何必然 =====
        self.set_note("看第二次落点：转两个 90° = 转 180° = 乘以 -1")
        self.play(Indicate(dots[1], color=ORANGE, scale_factor=1.8),
                  run_time=1.2)
        self.wait(1.6)

        verdict = Text("i^2 = -1：不是规定，是几何必然",
                       font=FONT, font_size=30, weight=BOLD, color=GOLD)
        verdict.move_to([0, 2.6, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("虚数不虚——它就是「转个身」的名字")
        self.wait(2.8)
