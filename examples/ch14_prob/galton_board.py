from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

ROWS = 6          # 钉板层数
N_BALLS = 40      # 落球总数
DX, DY = 0.92, 0.62
TOP = 1.9         # 顶层钉高度
BIN_Y = TOP - ROWS * DY - 0.68   # 槽底高度（球堆可长高，漫到钉区属正常）
BAR_H = 0.13      # 每个球贡献的柱高


class GaltonBoard(Scene):
    """高尔顿钉板：小球随机左右落，槽里堆出二项分布，逼近正态曲线。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("高尔顿钉板：随机的尽头是钟形", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("一颗小球掉下来，碰到钉子往左还是往右？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ===== 钉板 =====
        pins = VGroup()
        for r in range(ROWS):
            for j in range(r + 1):
                p = Dot([(j - r / 2) * DX, TOP - r * DY, 0],
                        color=C_TEXT, radius=0.045)
                pins.add(p)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pins],
                              lag_ratio=0.03), run_time=1.6)
        # 槽位隔板
        for k in range(ROWS + 2):
            x = (k - (ROWS + 1) / 2) * DX
            wall = Line([x, BIN_Y, 0], [x, BIN_Y + 0.35, 0],
                        color=GREY_B, stroke_width=2)
            self.add(wall)
        self.wait(0.8)

        # ===== 球数面板 =====
        cnt_lab = Text("球数 n =", font=FONT, font_size=26, color=C_TEXT)
        cnt_lab.move_to([4.6, 3.0, 0], aligned_edge=RIGHT)
        cnt_anchor = np.array([4.85, 3.0, 0])
        cnt_num = Text("0", font=FONT, font_size=26, color=GOLD)
        cnt_num.move_to(cnt_anchor, aligned_edge=LEFT)
        self.add(cnt_lab, cnt_num)

        # ===== 落球（路径预生成，种子固定可复现） =====
        rng = np.random.default_rng(20260828)
        counts = np.zeros(ROWS + 1, dtype=int)
        bars = []
        for k in range(ROWS + 1):
            b = Rectangle(width=DX * 0.82, height=0.001,
                          fill_color=TEAL, fill_opacity=0.85,
                          stroke_width=0)
            b.move_to([(k - ROWS / 2) * DX, BIN_Y, 0], aligned_edge=DOWN)
            bars.append(b)
            self.add(b)

        self.set_note("一颗球的去向完全没法预测——看它左碰右撞")
        for i in range(N_BALLS):
            x, y = 0.0, TOP + 0.55
            path = [np.array([x, y, 0])]
            rights = 0
            for r in range(ROWS):
                step = rng.choice([-1, 1])
                rights += (step + 1) // 2
                x += step * DX / 2
                y -= DY
                path.append(np.array([x, y, 0]))
            k = rights
            counts[k] += 1
            land = np.array([(k - ROWS / 2) * DX, BIN_Y + 0.15, 0])
            path.append(land)
            ball = Dot(path[0], color=GOLD, radius=0.075)
            rail = VMobject()
            rail.set_points_as_corners(path)   # 隐形轨道供 MoveAlongPath 使用
            self.add(ball)
            rt = 0.5 if i < 6 else (0.3 if i < 20 else 0.16)
            self.play(MoveAlongPath(ball, rail),
                      run_time=rt, rate_func=linear)
            self.remove(ball)
            h = counts[k] * BAR_H
            bars[k].become(Rectangle(width=DX * 0.82, height=h,
                                     fill_color=TEAL, fill_opacity=0.85,
                                     stroke_width=0)
                           .move_to([(k - ROWS / 2) * DX, BIN_Y, 0],
                                    aligned_edge=DOWN))
            cnt_num.become(Text(str(i + 1), font=FONT, font_size=26,
                                color=GOLD)
                           .move_to(cnt_anchor, aligned_edge=LEFT))
        self.wait(1.0)

        # ===== 数槽：二项系数现身 =====
        self.set_note("数每个槽：1、6、15、20、15、6、1 的影子")
        coefs = [1, 6, 15, 20, 15, 6, 1]
        pred = VGroup()
        for k, c in enumerate(coefs):
            h = c / 64 * N_BALLS * BAR_H
            marker = Rectangle(width=DX * 0.82, height=h,
                               fill_color=GOLD, fill_opacity=0.28,
                               stroke_color=GOLD, stroke_width=1.5)
            marker.move_to([(k - ROWS / 2) * DX, BIN_Y, 0],
                           aligned_edge=DOWN)
            pred.add(marker)
        self.play(FadeIn(pred), run_time=1.0)
        self.wait(2.2)

        # ===== 正态曲线覆盖 =====
        self.set_note("这就是二项分布：C(6,k)/64；层数越多，越像一条光滑曲线")
        self.wait(2.0)
        mu = ROWS / 2
        sigma = np.sqrt(ROWS * 0.25)
        # 每个槽概率 px ≈ φ(x)/(σ√2π)（槽宽 Δk=1），柱高 = 概率 × 总球高
        xs = np.linspace(0, ROWS, 120)
        pts = []
        for x in xs:
            px = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) \
                / (sigma * np.sqrt(2 * np.pi))
            pts.append(np.array([(x - ROWS / 2) * DX,
                                 BIN_Y + px * N_BALLS * BAR_H, 0]))
        curve = VMobject(color=GOLD, stroke_width=4)
        curve.set_points_smoothly(pts)
        self.play(Create(curve), run_time=2.0)
        self.wait(1.2)
        self.set_note("层数继续增加，柱子就磨成这条曲线——正态分布")
        self.wait(2.4)
        self.set_note("单个不可预测，整体无比稳定——这就是统计的世界观")
        self.wait(2.6)
