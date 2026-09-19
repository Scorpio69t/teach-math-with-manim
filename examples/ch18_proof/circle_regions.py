"""第 18 章案例：圆分割陷阱——猜想被第六项击碎（代码清单 18-1）

渲染：manim -pqh circle_regions.py CircleRegions
"""

from manim import *
from math import comb
import math

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [4.8, 2.3, 0]       # n 读数
R2_POS = [4.8, 1.7, 0]       # 区域数读数
R3_POS = [4.8, 1.1, 0]       # 猜想读数
VERDICT_POS = [0, -2.75, 0]
CNT_POS = [-2.3, -2.6, 0]    # 区域计数牌（圆心正下方）


def region_count(n):
    """一般位置下 n 点分圆的区域数：C(n,4) + C(n,2) + 1（真公式现算）。"""
    return comb(n, 4) + comb(n, 2) + 1


def mix(parts, size=26, color=C_TEXT, math_scale=0.9):
    """中文 + 公式混排：parts 交错给出文本串与 LaTeX 串，返回一个 VGroup。"""
    group = VGroup()
    for kind, s in parts:
        if kind == "t":
            group.add(Text(s, font=FONT, font_size=size, color=color))
        else:
            group.add(MathTex(s, color=color).scale(math_scale))
    return group.arrange(RIGHT, buff=0.10)


def _half(poly, nx, ny, c, keep_pos):
    """凸多边形按直线 nx·x + ny·y = c 切出的单侧（Sutherland–Hodgman）。"""
    out = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        sa = nx * a[0] + ny * a[1] - c
        sb = nx * b[0] + ny * b[1] - c
        if (sa >= -1e-9) == keep_pos:
            out.append(a)
        if (sa > 1e-9 and sb < -1e-9) or (sa < -1e-9 and sb > 1e-9):
            t = sa / (sa - sb)
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), 0))
    return out


def circle_regions(center, radius, pts):
    """当前点位的全部区域多边形。

    圆盘近似为 144 边形，被每条弦的直线依次切割；弦在圆内横贯全盘，
    所以切出的凸块恰好就是弦布置的区域。弦两端点绕中点微扰 1e-6 弧度，
    避免切割线恰好穿过细分顶点的退化。
    """
    disk = [[center[0] + radius * np.cos(2 * np.pi * s / 144),
             center[1] + radius * np.sin(2 * np.pi * s / 144), 0]
            for s in range(144)]
    chords = [(pts[i], pts[j]) for i in range(len(pts))
              for j in range(i + 1, len(pts))]
    polys = [disk]
    for A, B in chords:
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        ca, sa = math.cos(1e-6), math.sin(1e-6)
        a = (mx + (A[0] - mx) * ca - (A[1] - my) * sa,
             my + (A[0] - mx) * sa + (A[1] - my) * ca, 0)
        b = (mx + (B[0] - mx) * ca - (B[1] - my) * sa,
             my + (B[0] - mx) * sa + (B[1] - my) * ca, 0)
        nx, ny = a[1] - b[1], b[0] - a[0]
        c = nx * a[0] + ny * a[1]
        nxt = []
        for poly in polys:
            pos = _half(poly, nx, ny, c, True)
            neg = _half(poly, nx, ny, c, False)
            if len(pos) >= 3:
                nxt.append(pos)
            if len(neg) >= 3:
                nxt.append(neg)
        polys = nxt
    return polys


class CircleRegions(Scene):
    """n 个点两两相连：区域逐块点亮、计数牌同步累加——
    1, 2, 4, 8, 16 印证猜想 2^(n-1)，第六项 31 当场击碎猜想。"""

    def set_note(self, msg):
        if isinstance(msg, str):
            self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                             .move_to(NOTE_POS))
        else:
            self.note.become(mix(msg).move_to(NOTE_POS))

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

        r1 = Text("n = 1", font=FONT, font_size=26, color=C_TEXT).move_to(R1_POS)
        r2 = Text("区域数 = 1", font=FONT, font_size=26, color=C_TEXT).move_to(R2_POS)
        r3 = Text("先观察前几项", font=FONT, font_size=26, color=C_TEXT).move_to(R3_POS)
        self.add(r1, r2, r3)

        notes = {
            1: "一个点，圆还是完整的一块",
            2: "两个点一条弦，圆成两块",
            3: "三个点三条弦，四块",
            4: "四个点：八块——倍数规律呼之欲出",
            5: [("t", "五个点：十六块！"), ("m", "2^{n-1}"), ("t", "，就是它了吧？")],
            6: "六个点——慢着，跟我一块块数清楚：不是 32",
        }
        prev = None
        for n in range(1, 7):
            # 这组固定点位已核验到 n=6；固定扰动本身不等于一般位置证明
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
            self.set_note(notes[n])

            # ===== 逐块点亮数区域：每块闪一下，计数牌同步 +1 =====
            regions = circle_regions(center, RAD, pts)
            polys = VGroup(*[Polygon(*r, stroke_width=0, fill_color=GREY_E,
                                     fill_opacity=0)
                             for r in regions])
            polys.sort(lambda p: (p[0], p[1]))
            counter = Text("0", font=FONT, font_size=30, color=YELLOW
                           ).move_to(CNT_POS)
            self.add(counter)
            for k, poly in enumerate(polys, 1):
                counter.become(Text(str(k), font=FONT, font_size=30,
                                    color=YELLOW).move_to(CNT_POS))
                r2.become(Text(f"区域数 = {k}", font=FONT, font_size=26,
                               color=C_TEXT).move_to(R2_POS))
                self.play(poly.animate.set_fill(YELLOW, 0.40), run_time=0.14)
                self.play(poly.animate.set_fill(GREY_E, 0.15), run_time=0.10)

            ok = (cnt == len(polys) == guess)
            r2.become(Text(f"区域数 = {cnt}", font=FONT, font_size=26,
                           color=GREEN if ok else RED).move_to(R2_POS))
            if n >= 4:
                r3.become(mix([("t", "猜想 "), ("m", "2^{n-1}"),
                               ("t", f" = {guess}")],
                              size=26, color=C_TEXT if ok else RED
                              ).move_to(R3_POS))
            self.wait(2.0 if n < 5 else 2.4)
            prev = VGroup(dots, chords, polys, counter)

        # ===== 结案：猜想翻车 =====
        r3.become(mix([("t", "猜想 "), ("m", "2^{n-1}"), ("t", " 翻车！")],
                      size=26, color=RED).move_to(R3_POS))
        self.set_note("31 不是 32——增长的秘密，藏在弦与弦的交点里")
        self.wait(2.6)

        verdict = Text("归纳只生产猜想，证明才生产真理",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("找到规律是好事——但交卷之前，它需要一纸证明")
        self.wait(2.8)
