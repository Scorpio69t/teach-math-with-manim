from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

X_MIN, X_MAX = -0.4, 4 * PI + 0.4
TERMS = [1, 3, 5, 7]              # 方波的前四项：sin(kx)/k


def square_wave(x):
    """目标方波：±1，周期 2π。"""
    return 1.0 if np.sin(x) >= 0 else -1.0


def partial_sum(n_terms):
    def f(x):
        return sum(np.sin(k * x) / k for k in TERMS[:n_terms])
    return f


class FourierStack(Scene):
    """波形叠加：一个个正弦"音符"叠上去，方波浮现——傅里叶直觉。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("波形叠加：用圆滚的正弦，叠出带棱角的方波",
                     font=FONT, font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("目标：那条灰色虚线——一段方波",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        ax = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.8, 1.8, 1],
                  x_length=12.2, y_length=3.6,
                  axis_config={"color": GREY, "stroke_width": 1.5},
                  tips=False)
        ax.move_to(DOWN * 0.15)
        tick_labels = VGroup()
        for k, name in [(1, "π"), (2, "2π"), (3, "3π"), (4, "4π")]:
            lab = Text(name, font=FONT, font_size=20, color=GREY_B)
            lab.next_to(ax.c2p(k * PI, 0), DOWN, buff=0.1)
            tick_labels.add(lab)
        self.play(Create(ax), FadeIn(tick_labels), run_time=1.2)

        # 目标方波（虚线）
        target = VGroup()
        xs = np.linspace(0, 4 * PI, 400)
        seg = []
        prev = None
        for x in xs:
            y = square_wave(x)
            if prev is not None and y != prev:
                target.add(DashedLine(ax.c2p(x, prev), ax.c2p(x, y),
                                      color=GREY_B, dash_length=0.08))
                if seg:
                    target.add(DashedLine(
                        ax.c2p(seg[0], prev), ax.c2p(seg[-1], prev),
                        color=GREY_B, dash_length=0.08))
                seg = []
            seg.append(x)
            prev = y
        if seg:
            target.add(DashedLine(ax.c2p(seg[0], prev),
                                  ax.c2p(seg[-1], prev),
                                  color=GREY_B, dash_length=0.08))
        self.play(FadeIn(target), run_time=1.0)
        self.wait(0.8)

        # 面板：项数与当前叠加式
        p_title = Text("正在叠加的项", font=FONT, font_size=24,
                       weight=BOLD, color=C_TEXT)
        p_title.to_corner(UR, buff=0.6).shift(UP * 0.15)
        self.play(FadeIn(p_title), run_time=0.5)

        term_texts = ["sin x",
                      "sin x + (1/3)·sin 3x",
                      "… + (1/5)·sin 5x",
                      "… + (1/7)·sin 7x"]
        cur_formula = Text("项数 n = 0", font=FONT, font_size=26,
                           color=GOLD)
        cur_formula.to_corner(UR, buff=0.6).shift(DOWN * 0.35)
        self.add(cur_formula)

        def set_formula(msg):
            nonlocal cur_formula
            new = Text(msg, font=FONT, font_size=26, color=GOLD)
            new.to_corner(UR, buff=0.6).shift(DOWN * 0.35)
            cur_formula.become(new)

        # ===== 逐项叠加 =====
        sum_curve = None
        notes = ["第一个音：y = sin x——圆滑，离方波还很远",
                 "加入三倍频：波峰开始被'顶'平",
                 "再加五倍频：平台更平，边缘更陡",
                 "七倍频到位：方波的轮廓已经肉眼可辨"]
        for i, k in enumerate(TERMS):
            n = i + 1
            # 先单独亮出这一项（虚线），再叠进总和
            comp = ax.plot(lambda x: np.sin(k * x) / k,
                           x_range=[0, 4 * PI], color=TEAL,
                           stroke_width=2.5)
            comp.set_stroke(opacity=0.9)
            self.set_note(notes[i])
            self.play(Create(comp), run_time=1.6)
            self.wait(0.5)
            new_sum = ax.plot(partial_sum(n), x_range=[0, 4 * PI],
                              color=GOLD, stroke_width=4.5)
            if sum_curve is None:
                self.play(FadeOut(comp), Create(new_sum), run_time=1.4)
                sum_curve = new_sum
            else:
                self.play(FadeOut(comp), Transform(sum_curve, new_sum),
                          run_time=1.4)
            set_formula("n = {}：{}".format(n, term_texts[i]))
            self.wait(1.2)

        # ===== 结案 =====
        self.set_note("棱角的代价：跳变处总有一撮压不下去的'小耳朵'")
        # 标出 Gibbs 过冲位置（x=0 附近）
        ear = Circle(radius=0.35, color=RED, stroke_width=3)
        ear.move_to(ax.c2p(0.0, 1.15))
        self.play(Create(ear), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(ear), run_time=0.5)

        self.set_note("项数趋向无穷，和就是方波——这就是傅里叶级数")
        self.play(Indicate(sum_curve, color=GOLD), run_time=1.2)
        final = Text("任何周期波，都是一堆正弦波的合唱",
                     font=FONT, font_size=28, weight=BOLD, color=GOLD)
        final.move_to(UP * 2.9 + LEFT * 1.6)
        self.play(FadeIn(final), run_time=1.0)
        self.wait(2.6)
