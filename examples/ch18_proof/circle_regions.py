"""第 18 章案例：圆分割陷阱——猜想被第六项击碎（代码清单 18-1）

渲染：manim -pqh circle_regions.py CircleRegions
"""

from manim import *
from math import comb

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [4.8, 2.3, 0]       # n 读数
R2_POS = [4.8, 1.7, 0]       # 区域数读数
R3_POS = [4.8, 1.1, 0]       # 猜想读数
VERDICT_POS = [0, -2.75, 0]


def region_count(n):
    """一般位置下 n 点分圆的区域数：C(n,4) + C(n,2) + 1（真公式现算）。"""
    return comb(n, 4) + comb(n, 2) + 1


class CircleRegions(Scene):
    """n 个点两两相连：区域数 1, 2, 4, 8, 16——猜想 2^(n-1)，
    第六项 31 当场击碎猜想。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("1, 2, 4, 8, 16——下一个是什么？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("圆上取 n 个点，两两连线，圆被分成几块？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        center = [-2.3, 0.2, 0]
        RAD = 2.35
        circle = Circle(radius=RAD, color=C_TEXT, stroke_width=3)
        circle.move_to(center)
        self.play(Create(circle), run_time=1.1)

        r1 = Text("", font=FONT, font_size=26, color=C_TEXT).move_to(R1_POS)
        r2 = Text("", font=FONT, font_size=26, color=C_TEXT).move_to(R2_POS)
        r3 = Text("", font=FONT, font_size=26, color=C_TEXT).move_to(R3_POS)
        self.add(r1, r2, r3)

        notes = {
            1: "一个点，圆还是完整的一块",
            2: "两个点一条弦，圆成两块",
            3: "三个点三条弦，四块",
            4: "四个点：八块——倍数规律呼之欲出",
            5: "五个点：十六块！2^(n-1)，就是它了吧？",
            6: "六个点——慢着，数清楚：不是 32",
        }
        prev = None
        for n in range(1, 7):
            # 角度加扰动：避免三线共点（保持"一般位置"）
            angs = [np.radians(i * 360 / n + i * 7) for i in range(n)]
            pts = [[center[0] + RAD * np.cos(a), center[1] + RAD * np.sin(a),
                    0] for a in angs]
            dots = VGroup(*[Dot(p, radius=0.07, color=GOLD) for p in pts])
            chords = VGroup(*[Line(pts[i], pts[j], color=TEAL,
                                   stroke_width=1.8)
                              for i in range(n) for j in range(i + 1, n)])
            cnt = region_count(n)
            guess = 2 ** (n - 1)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            self.play(FadeIn(dots), run_time=0.5)
            if chords:
                self.play(Create(chords), lag_ratio=0.12, run_time=1.1)
            r1.become(Text(f"n = {n}", font=FONT, font_size=26,
                           color=C_TEXT).move_to(R1_POS))
            ok = (cnt == guess)
            r2.become(Text(f"区域数 = {cnt}", font=FONT, font_size=26,
                           color=GREEN if ok else RED).move_to(R2_POS))
            if n >= 4:
                r3.become(Text(f"猜想 2^(n-1) = {guess}", font=FONT,
                               font_size=26,
                               color=C_TEXT if ok else RED)
                          .move_to(R3_POS))
            self.set_note(notes[n])
            self.wait(2.0 if n < 5 else 2.4)
            prev = VGroup(dots, chords)

        # ===== 结案：猜想翻车 =====
        r3.become(Text("猜想 2^(n-1) 翻车！", font=FONT,
                       font_size=26, weight=BOLD, color=RED)
                  .move_to(R3_POS))
        self.set_note("31 不是 32——增长的秘密，藏在弦与弦的交点里")
        self.wait(2.6)

        verdict = Text("归纳只生产猜想，证明才生产真理",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("找到规律是好事——但交卷之前，它需要一纸证明")
        self.wait(2.8)
