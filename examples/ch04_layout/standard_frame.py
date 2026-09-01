"""第 4 章综合案例：标准讲解帧——标题 + 曲线 + 参数面板 + 注释（代码清单 4-2）

把"标题 + 公式 + 注释"的标准版式扩展为"标题 + 坐标系 + 抛物线 + 参数面板 + 注释"。
a/b/c 三个参数在面板上各占一行；讲解哪个参数，对应行变金色、抛物线同步变形——
注释文字讲的"a 管开口方向"就不再是空话。

节奏按"留足加讲解空间"原则设计：每个变形段后留 2—3 秒 wait，
讲解者可以在这段时间里把"为什么这么变"讲清楚。

渲染：manim -pqh standard_frame.py StandardFrameScene
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"


class StandardFrameScene(Scene):
    """本书讲解画面的标准版式：左上标题、中央坐标系与曲线、右侧参数面板、底部注释。

    四个分区的位置全部用相对定位钉死——这套版式会在数学篇反复复用。
    """

    C_TEXT = "#EDEDED"        # 默认文字色：浅灰
    C_MUTED = "#9AA3C0"       # 蓝灰：默认背景元素（全书颜色语义）

    NOTE_POS = DOWN * 3.2          # 注释条固定锚点
    TITLE_BUFF = 0.5              # 标题到画布边的距离
    AXES_CENTER = LEFT * 1.5 + DOWN * 0.2   # 坐标系中心位置
    PANEL_CENTER = RIGHT * 4.2 + UP * 0.8    # 参数面板中心位置
    FORMULA_POS = UP * 2.4                  # 公式区锚点

    # ---------- 主流程 ----------
    def construct(self):
        title, title_rule = self._make_title()
        panel = self._make_panel(1.0, 0.0, 0.0)
        axes = self._make_axes()
        parabola = self._make_parabola(axes, 1.0, 0.0, 0.0)
        formula = self._make_formula(None)  # 默认三参数皆灰
        note = Text("a 管开口方向与宽窄", font=FONT, font_size=26,
                    t2c={"a": GOLD}, color=self.C_TEXT).move_to(self.NOTE_POS)

        def set_note(msg, key):
            """换注释不换位置；关键词 t2c 标金，告诉学生眼睛看哪"""
            new = Text(msg, font=FONT, font_size=26, t2c={key: GOLD},
                       color=self.C_TEXT).move_to(self.NOTE_POS)
            return Transform(note, new, run_time=0.5)

        def highlight_param(idx, value):
            """参数面板第 idx 行变金色（当前关注）；其它行保持中性"""
            names = ["a", "b", "c"]
            row = Text(f"{names[idx]} = {value:+.1f}", font=FONT,
 font_size=28, color=GOLD)
            row.move_to(panel[idx].get_center())
            return Transform(panel[idx], row, run_time=0.6)

        def new_curve(a, b, c):
            """生成新抛物线"""
            return axes.plot(lambda x: a * x ** 2 + b * x + c,
                            color=WHITE, stroke_width=4)

        # ---------- 开场：版式骨架全部登场 ----------
        # MathTex 第一次登场稍慢，让读者看清"这是公式"；
        # MathTex 的更多用法（公式变形、子对象拆分、TransformMatchingTex）见第 5 章。
        self.play(FadeIn(title), Create(title_rule), run_time=1.0)
        self.play(Write(formula), run_time=1.8)
        self.play(Create(axes), FadeIn(parabola), run_time=1.4)
        self.play(FadeIn(panel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.5)

        # ---------- 阶段 A：a 从 1.0 变 2.0，开口变窄 ----------
        a1 = 2.0
        new_a = new_curve(a1, 0.0, 0.0)
        self.play(highlight_param(0, a1),
                  Transform(formula, self._make_formula("a")), run_time=1.0)
        self.play(FadeOut(parabola), FadeIn(new_a), run_time=1.2)
        parabola = new_a
        self.wait(2.5)

        # ---------- 阶段 B：b 从 0.0 变 -2.0，对称轴登场 ----------
        b1 = -2.0
        new_b = new_curve(a1, b1, 0.0)
        # 对称轴 x = -b/(2a)，落在坐标系内
        axis_x = -b1 / (2 * a1)
        symmetry = DashedLine(
            axes.c2p(axis_x, -1), axes.c2p(axis_x, 5),
            color=GREEN, stroke_width=2,
        )
        self.play(set_note("b 与 a 一起决定对称轴 x = -b/2a", "b"),
                  highlight_param(1, b1),
                  Transform(formula, self._make_formula("b")), run_time=1.0)
        self.play(FadeOut(parabola), FadeIn(new_b), run_time=1.2)
        self.play(Create(symmetry), run_time=0.8)
        parabola = new_b
        self.wait(2.8)

        # ---------- 阶段 C：c 从 0.0 变 2.0，曲线整体上移 ----------
        c1 = 2.0
        new_c = new_curve(a1, b1, c1)
        self.play(set_note("c 是抛物线与 y 轴的交点高度", "c"),
                  highlight_param(2, c1),
                  Transform(formula, self._make_formula("c")), run_time=1.0)
        self.play(FadeOut(parabola), FadeIn(new_c), run_time=1.2)
        parabola = new_c
        self.wait(2.8)

        # ---------- 收尾：三参数同时微调，呼应"改一个曲线动一处" ----------
        a2, b2, c2 = 0.5, 1.0, -1.0
        final_curve = new_curve(a2, b2, c2).set_color(GOLD)
        self.play(set_note("三个参数，三种职责——改一个，曲线动一处", "改"),
                  run_time=0.6)
        # 三个参数面板行同时变换（最终态：a 当前关注，金色；b/c 中性）
        final_rows = VGroup(*[
            Text(f"{n} = {v:+.1f}", font=FONT, font_size=28,
                 color=GOLD if i == 0 else self.C_TEXT)
            for i, (n, v) in enumerate([("a", a2), ("b", b2), ("c", c2)])
        ]).arrange(DOWN, buff=0.45).move_to(self.PANEL_CENTER)
        self.play(
            Transform(parabola, final_curve),
            *[Transform(panel[i], final_rows[i], run_time=1.2)
              for i in range(3)],
        )
        self.play(FadeOut(symmetry), run_time=0.5)
        note.set_color(self.C_MUTED)
        self.wait(4.0)

    # ---------- 辅助方法 ----------
    def _make_title(self):
        """标题区：左上贴角 + 金色短尺"""
        title = Text("二次函数的一般式", font=FONT, font_size=34,
                     weight=BOLD, color=self.C_TEXT)
        title.to_corner(UL, buff=self.TITLE_BUFF)
        rule = Line(LEFT * 1.8, RIGHT * 1.8, color=GOLD,
                    stroke_width=3).next_to(title, DOWN, buff=0.15)
        rule.align_to(title, LEFT)
        return title, rule

    def _make_axes(self):
        """坐标系，钉在左侧演示区"""
        return Axes(
            x_range=[-3, 3, 1], y_range=[-1, 5, 1],
            x_length=5.5, y_length=4.5,
            axis_config={"stroke_color": self.C_MUTED, "stroke_width": 2,
                         "include_tip": False},
        ).move_to(self.AXES_CENTER)

    def _make_parabola(self, axes, a, b, c):
        """生成初始抛物线：白色，与轴线蓝灰形成对比"""
        return axes.plot(lambda x: a * x ** 2 + b * x + c,
                         color=WHITE, stroke_width=4)

    def _make_formula(self, highlight):
        """生成公式区：当前讲解的字母（"a"/"b"/"c"/None）用子对象索引标金

        用多参数 MathTex 传入，每个 token 单独成子对象：
            f[0]="y" f[1]="=" f[2]="a" f[3]="x^2" f[4]="+" f[5]="b" f[6]="x"
            f[7]="+" f[8]="c"
        不在 LaTeX 里写 \\color{GOLD}{a}——ManimCE 默认 MathTex 模板不加载
        xcolor 包，会触发 Undefined control sequence；改在 Python 端用
        f[2].set_color(GOLD) 精确染色单个字母，每次生成结构完全一致便于 Transform。

        注意：MathTex 是第 5 章的核心 API，本章先用先感受；公式变形
        （TransformMatchingTex）、子对象拆分等高级用法见第 5 章。
        """
        f = MathTex("y", "=", "a", "x^2", "+", "b", "x", "+", "c",
 font_size=60)
        f.set_color(self.C_TEXT)  # 默认色（浅灰）
        idx_map = {"a": 2, "b": 5, "c": 8}
        if highlight in idx_map:
            f[idx_map[highlight]].set_color(GOLD)
        f.move_to(self.FORMULA_POS)
        return f

    def _make_panel(self, a, b, c):
        """三行参数面板，钉在右侧；每行字号一致，可单独 Transform 替换"""
        rows = VGroup(*[
            Text(f"{name} = {val:+.1f}", font=FONT, font_size=28,
                 color=self.C_TEXT)
            for name, val in [("a", a), ("b", b), ("c", c)]
        ]).arrange(DOWN, buff=0.45)
        rows.move_to(self.PANEL_CENTER)
        return rows