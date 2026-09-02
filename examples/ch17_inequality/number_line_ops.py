"""第 17 章案例：数轴上的不等式——加减乘除下的顺序命运（代码清单 17-1）

渲染：manim -pqh number_line_ops.py NumberLineOps
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
READ_POS = [4.7, 2.4, 0]     # 读数锚点
VERDICT_POS = [0, -2.75, 0]

A0, B0, C0 = 2, -1, 4        # 三个演示数：a > b，c 用于传递性


class NumberLineOps(Scene):
    """a > b 就是"a 在 b 右边"。同加同乘正数，顺序不动；
    同乘负数＝照镜子，顺序翻转——不等号必须掉头。最后补传递性。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("乘一个负数，不等号为什么要掉头？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("先把 a > b 摆到数轴上，看看它到底长什么样",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 建轴：a > b 的位置含义 =====
        line = NumberLine(x_range=[-6, 6, 1], length=11,
                          color=GREY_B, stroke_width=2,
                          include_ticks=True, include_numbers=False)
        line.move_to([0, 0.2, 0])
        a_dot = Dot(line.n2p(A0), radius=0.09, color=GOLD)
        b_dot = Dot(line.n2p(B0), radius=0.09, color=GOLD)
        a_lab = Text(f"a = {A0}", font=FONT, font_size=24, color=GOLD)
        a_lab.next_to(a_dot, UP, buff=0.25)
        b_lab = Text(f"b = {B0}", font=FONT, font_size=24, color=GOLD)
        b_lab.next_to(b_dot, UP, buff=0.25)
        self.play(Create(line), run_time=1.2)
        self.play(FadeIn(a_dot), FadeIn(b_dot),
                  FadeIn(a_lab), FadeIn(b_lab), run_time=0.8)
        stmt = Text("a > b 就是：a 站在 b 的右边", font=FONT, font_size=26,
                    color=C_TEXT)
        stmt.move_to([0, 2.3, 0])
        self.play(FadeIn(stmt, shift=DOWN * 0.2), run_time=0.8)
        self.set_note("大于号不是符号游戏，是一个位置关系")
        self.wait(2.0)

        # ===== 同加 3：整体平移 =====
        def ghost(dot):
            return Dot(dot.get_center(), radius=0.07, color=GREY)

        def hop(dot, lab, target_num, name):
            """点跳到新位置：留残影 + 弧形箭头。"""
            g = ghost(dot)
            arr = CurvedArrow(dot.get_center(), line.n2p(target_num),
                              angle=-TAU / 6, color=RED, stroke_width=3,
                              tip_length=0.18)
            self.play(FadeIn(g), Create(arr), run_time=0.5)
            self.play(dot.animate.move_to(line.n2p(target_num)),
                      run_time=0.9)
            self.play(FadeOut(arr), run_time=0.3)
            lab.become(Text(f"{name} = {target_num}", font=FONT,
                            font_size=24, color=GOLD)
                       .move_to(line.n2p(target_num) + UP * 0.45))
            return g

        ghosts = []
        readout = Text("准备操作：先看同加 3", font=FONT,
                       font_size=24, color=C_TEXT)
        readout.move_to(READ_POS)
        self.add(readout)

        ghosts += [hop(a_dot, a_lab, A0 + 3, "a"),
                   hop(b_dot, b_lab, B0 + 3, "b")]
        readout.become(Text(f"同加 3：{A0 + 3} > {B0 + 3}，顺序不变",
                            font=FONT, font_size=24, color=C_TEXT)
                       .move_to(READ_POS))
        self.set_note("同加一个数 = 整列向右平移——左右关系平移不走")
        self.wait(2.2)

        # ===== 复位，同乘 2：以原点为轴拉伸 =====
        self.play(a_dot.animate.move_to(line.n2p(A0)),
                  b_dot.animate.move_to(line.n2p(B0)), run_time=0.6)
        a_lab.become(Text(f"a = {A0}", font=FONT, font_size=24, color=GOLD)
                     .move_to(line.n2p(A0) + UP * 0.45))
        b_lab.become(Text(f"b = {B0}", font=FONT, font_size=24, color=GOLD)
                     .move_to(line.n2p(B0) + UP * 0.45))
        ghosts += [hop(a_dot, a_lab, A0 * 2, "a"),
                   hop(b_dot, b_lab, B0 * 2, "b")]
        readout.become(Text(f"同乘 2：{A0 * 2} > {B0 * 2}，顺序不变",
                            font=FONT, font_size=24, color=C_TEXT)
                       .move_to(READ_POS))
        self.set_note("同乘正数 = 以原点为轴向外拉伸——左右关系拉不散")
        self.wait(2.2)

        # ===== 复位，同乘 -1：镜像翻转 =====
        self.play(a_dot.animate.move_to(line.n2p(A0)),
                  b_dot.animate.move_to(line.n2p(B0)), run_time=0.6)
        a_lab.become(Text(f"a = {A0}", font=FONT, font_size=24, color=GOLD)
                     .move_to(line.n2p(A0) + UP * 0.45))
        b_lab.become(Text(f"b = {B0}", font=FONT, font_size=24, color=GOLD)
                     .move_to(line.n2p(B0) + UP * 0.45))
        ghosts += [hop(a_dot, a_lab, -A0, "a"),
                   hop(b_dot, b_lab, -B0, "b")]
        warn = Text(f"同乘 -1：{-A0} < {-B0}，顺序翻了！",
                    font=FONT, font_size=26, weight=BOLD, color=RED)
        warn.move_to(READ_POS)
        readout.become(warn)
        self.play(Indicate(a_dot, color=RED), Indicate(b_dot, color=RED),
                  run_time=0.8)
        self.set_note("同乘负数 = 照镜子：右边翻到左边——不等号必须跟着掉头")
        self.wait(2.6)

        # ===== 传递性：排队 =====
        c_dot = Dot(line.n2p(C0), radius=0.09, color=TEAL)
        c_lab = Text(f"c = {C0}", font=FONT, font_size=24, color=TEAL)
        c_lab.next_to(c_dot, DOWN, buff=0.25)
        self.play(FadeIn(c_dot), FadeIn(c_lab), run_time=0.8)
        readout.become(Text("c 在 a 右，a 在 b 右 → c 在 b 右",
                            font=FONT, font_size=24, color=TEAL)
                       .move_to(READ_POS))
        self.set_note("传递性就是排队：右者的右者，必在更右")
        self.wait(2.2)

        # ===== 结案 =====
        self.play(FadeOut(stmt), run_time=0.5)
        verdict = Text("加减乘正，顺序不动；乘负掉头；传递性就是排队",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("三条性质，全是数轴上的位置常识——几何就是它们的证词")
        self.wait(2.8)
