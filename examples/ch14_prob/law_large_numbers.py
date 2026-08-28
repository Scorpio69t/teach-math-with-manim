from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

N_FLIPS = 10000
N_PLOT = 400    # 描点总数（前期密、后期疏，√刻度下均匀）


def freq_series(seed):
    """一条抛硬币序列的累计频率折线（采样点按 i² 加密前期）。"""
    rng = np.random.default_rng(seed)
    flips = rng.integers(0, 2, N_FLIPS)
    cum = np.cumsum(flips)
    ns = np.unique(np.concatenate([
        np.arange(1, 101),
        np.unique((np.sqrt(100) + (np.sqrt(N_FLIPS) - np.sqrt(100))
                   * np.linspace(0, 1, N_PLOT - 100)) ** 2
                  ).astype(int)]))
    ns = ns[ns <= N_FLIPS]
    return ns, cum[ns - 1] / ns


class LawOfLargeNumbers(Scene):
    """大数定律：三条平行宇宙的频率折线，震荡收窄，贴向 1/2。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("大数定律：抛一万次硬币之后", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("抛 10 次 7 次正面——这枚硬币有问题吗？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 坐标（x 轴用 √n 刻度：前期拉开，后期压缩） =====
        X0, X1 = -5.6, 5.6          # 屏幕 x 范围
        Y0 = -2.3                   # 频率 0 的屏幕高度
        YS = 5.0                    # 频率 1 = 5 单位高 → 1/2 在 0.2

        def sx(n):
            return X0 + (X1 - X0) * np.sqrt(n / N_FLIPS)

        def sy(p):
            return Y0 + p * YS

        axis_x = Line([X0, sy(0), 0], [X1, sy(0), 0],
                      color=GREY_B, stroke_width=2)
        axis_y = Line([X0, sy(0), 0], [X0, sy(1) + 0.15, 0],
                      color=GREY_B, stroke_width=2)
        ref = DashedLine([X0, sy(0.5), 0], [X1, sy(0.5), 0],
                         color=GOLD, dash_length=0.15, stroke_width=2.5)
        ref_lab = Text("1/2", font=FONT, font_size=24, color=GOLD)
        ref_lab.next_to(ref, LEFT, buff=0.15)
        xlab = Text("试验次数 n（√刻度）", font=FONT, font_size=22,
                    color=C_TEXT)
        xlab.move_to([1.5, sy(0) - 0.42, 0])
        ylab = Text("正面频率", font=FONT, font_size=22, color=C_TEXT)
        ylab.move_to([X0 + 1.1, sy(0.97), 0])
        self.play(Create(axis_x), Create(axis_y), run_time=1.0)
        self.play(Create(ref), FadeIn(ref_lab), FadeIn(xlab),
                  FadeIn(ylab), run_time=0.9)
        # 刻度标签
        for n in (10, 100, 1000, 10000):
            tick = Line([sx(n), sy(0) - 0.08, 0],
                        [sx(n), sy(0) + 0.08, 0],
                        color=GREY_B, stroke_width=2)
            lab = Text(str(n), font=FONT, font_size=20, color=C_TEXT)
            lab.move_to([sx(n), sy(0) - 0.4, 0])
            self.add(tick, lab)
        self.wait(0.8)

        # ===== 三条平行宇宙 =====
        series = [freq_series(s) for s in (2026, 828, 314)]
        colors = [TEAL, ORANGE, "#C77DFF"]
        t = ValueTracker(0)   # 采样点下标
        ns0 = series[0][0]

        traces = []
        for (ns, fq), col in zip(series, colors):
            def make(ns=ns, fq=fq, col=col):   # col 也要快照，否则三条同色
                idx = max(int(t.get_value()), 2)   # 至少两个点才能成折线
                pts = [np.array([sx(ns[i]), sy(fq[i]), 0])
                       for i in range(idx)]
                m = VMobject(color=col, stroke_width=2.5)
                m.set_points_as_corners(pts)
                return m
            traces.append(always_redraw(make))
        self.play(*[FadeIn(tr) for tr in traces], run_time=0.6)

        # ===== 面板：n 与频率 =====
        n_lab = Text("n =", font=FONT, font_size=26, color=C_TEXT)
        n_lab.move_to([3.6, 3.0, 0], aligned_edge=RIGHT)
        n_num = Text("1", font=FONT, font_size=26, color=GOLD)
        n_num.move_to([3.85, 3.0, 0], aligned_edge=LEFT)
        f_lab = Text("频率 =", font=FONT, font_size=26, color=C_TEXT)
        f_lab.move_to([3.6, 2.5, 0], aligned_edge=RIGHT)
        f_num = Text("1.000", font=FONT, font_size=26, color=TEAL)
        f_num.move_to([3.85, 2.5, 0], aligned_edge=LEFT)

        def n_upd(m):
            i = min(max(int(t.get_value()), 1) - 1, len(ns0) - 1)
            m.become(Text(str(int(ns0[i])), font=FONT, font_size=26,
                          color=GOLD).move_to([3.85, 3.0, 0],
                                              aligned_edge=LEFT))

        def f_upd(m):
            i = min(max(int(t.get_value()), 1) - 1, len(ns0) - 1)
            m.become(Text(f"{series[0][1][i]:.3f}", font=FONT,
                          font_size=26, color=TEAL)
                     .move_to([3.85, 2.5, 0], aligned_edge=LEFT))
        n_num.add_updater(n_upd)
        f_num.add_updater(f_upd)
        self.add(n_lab, n_num, f_lab, f_num)

        # ===== 摇起来 =====
        n_pts = len(ns0)
        self.set_note("三条轨迹，三个平行宇宙——前几十次上天入地")
        self.play(t.animate.set_value(60), run_time=3.0,
                  rate_func=linear)
        self.set_note("10 次里 7 次正面太正常了：小样本什么都敢发生")
        self.play(t.animate.set_value(120), run_time=2.6,
                  rate_func=linear)
        self.set_note("1000 次以后：震荡明显收窄")
        self.play(t.animate.set_value(int(n_pts * 0.75)),
                  run_time=3.0, rate_func=linear)
        self.set_note("10000 次：三条轨迹都贴上了 1/2")
        self.play(t.animate.set_value(n_pts - 1), run_time=3.0,
                  rate_func=linear)
        self.wait(1.6)

        # ===== 结案 =====
        self.set_note("不是「纠偏」——下一次抛出正面的机会永远是 1/2")
        self.wait(2.4)
        self.set_note("频率会稳定于概率：这就是大数定律")
        self.wait(2.4)
        self.set_note("随机的反面不是混乱，是另一种秩序")
        self.wait(2.6)
