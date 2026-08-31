"""第 18 章案例：多米诺骨牌与数学归纳法（代码清单 18-2）

渲染：manim -pqh domino_induction.py DominoInduction
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
GREAD_POS = [3.4, 2.5, 0]    # 方格读数
VERDICT_POS = [0, -2.75, 0]

CELL = 0.46                  # 方格边长
GRID0 = [1.7, -1.3, 0]       # 方格阵左下角


class DominoInduction(Scene):
    """骨牌链条演示奠基与递推；右侧 L 形格块证明
    1+3+5+...+(2n-1) = n²——传递步就是那一圈 L。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("命题有无穷多个，怎么一次证完？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("先玩一排骨牌：推倒第一块，其余交给链条",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 骨牌 =====
        doms = []
        for i in range(6):
            d = Rectangle(width=0.32, height=1.3,
                          color=GOLD if i == 0 else TEAL,
                          fill_opacity=0.85, stroke_width=2)
            d.move_to([-5.3 + i * 1.05, 0.05, 0])
            doms.append(d)
        n_lab = Text("第 1 块", font=FONT, font_size=20, color=GOLD)
        n_lab.move_to([-5.3, 1.0, 0])
        self.play(FadeIn(VGroup(*doms), lag_ratio=0.1), FadeIn(n_lab),
                  run_time=1.0)
        self.set_note("骨牌站成一排：间距小于牌高——倒下的牌必砸中下一张")
        self.wait(1.8)

        # ===== 推倒：奠基 + 链条 =====
        self.play(Rotate(doms[0], angle=-82 * DEGREES,
                         about_point=doms[0].get_corner(DR)),
                  run_time=0.6)
        self.set_note("奠基：第 1 块确实倒下——命题对 n = 1 成立")
        self.wait(1.2)
        for i in range(1, 6):
            self.play(Rotate(doms[i], angle=-82 * DEGREES,
                             about_point=doms[i].get_corner(DR)),
                      run_time=0.34)
        self.set_note("递推：每块倒下必砸倒下一块——n 成立则 n + 1 成立")
        self.wait(1.8)

        # ===== 翻译成式子：L 形格块 =====
        self.set_note("翻译成式子：1+3+5+...+(2n-1) = n²，看右边方格")
        self.wait(1.2)

        def cell(i, j, color, opacity=0.85):
            s = Square(side_length=CELL, color=color, fill_opacity=opacity,
                       stroke_width=1.5)
            s.move_to([GRID0[0] + (i + 0.5) * CELL,
                       GRID0[1] + (j + 0.5) * CELL, 0])
            return s

        gread = Text("", font=FONT, font_size=26, color=C_TEXT)
        gread.move_to(GREAD_POS)
        self.add(gread)

        base = VGroup(cell(0, 0, GOLD))
        gread.become(Text("1 = 1²", font=FONT, font_size=26, color=GOLD)
                     .move_to(GREAD_POS))
        self.play(FadeIn(base), run_time=0.6)
        self.set_note("奠基：1 就是 1²")
        self.wait(1.4)

        squares = VGroup(base)
        total = 1
        for k in range(1, 4):  # k×k → (k+1)×(k+1)，新增 2k+1 格
            new_cells = VGroup(
                *[cell(i, k, RED) for i in range(k + 1)],
                *[cell(k, j, RED) for j in range(k)])
            total += 2 * k + 1
            self.play(FadeIn(new_cells, lag_ratio=0.15), run_time=0.9)
            gread.become(Text(
                f"{total} = {k + 1}²（+{2 * k + 1} 格）", font=FONT,
                font_size=26, color=C_TEXT).move_to(GREAD_POS))
            self.set_note(f"第 {k + 1} 圈 L 形恰好 {2 * k + 1} 格："
                          f"{k}² 补成 {k + 1}²")
            self.wait(1.3)
            self.play(new_cells.animate.set_color(GOLD), run_time=0.5)
            squares.add(new_cells)
        self.set_note("每一圈 L 形都是奇数格——传递步在方格上肉眼可见")
        self.wait(2.0)

        # ===== 结案 =====
        verdict = Text("奠基 + 传递：第 1 块倒下，且每块必砸中下一块——全部倒下",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("这就是数学归纳法：两次确认，换掉无穷次验证")
        self.wait(2.8)
