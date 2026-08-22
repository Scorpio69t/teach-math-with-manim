"""第 4 章综合案例：标准讲解帧——标题 + 公式 + 注释（代码清单 4-2）

渲染：manim -pqh standard_frame.py StandardFrameScene
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"


class StandardFrameScene(Scene):
    """本书所有讲解画面的标准版式：左上标题、中央演示、底部注释条。

    三个分区的位置全部用相对定位钉死——这套版式会在数学篇反复复用。
    """

    C_TEXT = "#EDEDED"
    C_MUTED = "#9AA3C0"   # 蓝灰：默认背景元素（全书颜色语义）

    def construct(self):
        # 标题区：左上贴角，学生视线从左上角进入（与板书习惯一致）
        title = Text("二次函数的一般式", font=FONT, font_size=34,
                     weight=BOLD, color=self.C_TEXT)
        title.to_corner(UL, buff=0.5)

        # 标题下的金色短尺：标明"本帧主题"，也给标题区一个下边界
        title_rule = Line(LEFT * 1.8, RIGHT * 1.8, color=GOLD,
                          stroke_width=3).next_to(title, DOWN, buff=0.15)
        title_rule.align_to(title, LEFT)   # 尺的左边缘与标题左边缘对齐

        # 演示区：公式居中偏上，是这一帧唯一的主角
        # MathTex 依赖 LaTeX，第 5 章系统讲解，这里先用起来
        formula = MathTex(r"y = ax^2 + bx + c", font_size=60)
        formula.move_to(UP * 0.8)

        # 注释区：固定在底部的注释条，位置钉死不随内容漂移（§6.1 铁律）
        NOTE_POS = DOWN * 3.0
        note = Text("a 管开口方向与宽窄", font=FONT, font_size=26,
                    t2c={"a": GOLD}, color=self.C_TEXT).move_to(NOTE_POS)

        def set_note(msg, key):
            # 换注释不换位置；关键词 t2c 标金，告诉学生眼睛看哪
            new = Text(msg, font=FONT, font_size=26, t2c={key: GOLD},
                       color=self.C_TEXT).move_to(NOTE_POS)
            return Transform(note, new, run_time=0.3)

        self.play(FadeIn(title), Create(title_rule), run_time=0.8)
        self.play(Write(formula), run_time=1.5)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.0)

        # 注释轮换三条，每条停留足够一句讲解（节奏纪律）
        # 公式的逐字符高亮（拆解 MathTex 子对象）属于第 5 章内容，这里先整式强调
        self.play(Indicate(formula, color=GOLD, scale_factor=1.1),
                  run_time=0.6)
        self.wait(1.2)
        self.play(set_note("b 与 a 一起决定对称轴 x = -b/2a", "b"))
        self.wait(1.5)
        self.play(set_note("c 是抛物线与 y 轴的交点高度", "c"))
        self.wait(1.5)
        self.play(set_note("三个参数，三种职责——改一个，曲线动一处", "改"))
        note.set_color(self.C_MUTED)
        self.wait(2.0)
