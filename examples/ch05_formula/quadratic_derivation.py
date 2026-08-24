"""第 5 章 5.6 案例：配方法推导一元二次方程求根公式（七步链式变形）。

渲染：
  manim -pqh quadratic_derivation.py QuadraticDerivation   # 图 5-8
"""

from manim import *

FONT = "Microsoft YaHei"   # macOS 改 "PingFang SC"，Linux 改 "Noto Sans CJK SC"
CAPTION_POS = DOWN * 3.2

STEPS = [
    (r"ax^2", r"+", r"bx", r"+", r"c", r"=", r"0"),
    (r"x^2", r"+", r"\dfrac{b}{a}x", r"+", r"\dfrac{c}{a}", r"=", r"0"),
    (r"x^2", r"+", r"\dfrac{b}{a}x", r"=", r"-", r"\dfrac{c}{a}"),
    (r"x^2", r"+", r"\dfrac{b}{a}x", r"+", r"\left(\dfrac{b}{2a}\right)^2",
     r"=", r"-", r"\dfrac{c}{a}", r"+", r"\left(\dfrac{b}{2a}\right)^2"),
    (r"\left(x+\dfrac{b}{2a}\right)^2", r"=", r"\dfrac{b^2-4ac}{4a^2}"),
    (r"x+\dfrac{b}{2a}", r"=", r"\pm", r"\dfrac{\sqrt{b^2-4ac}}{2a}"),
    (r"x", r"=", r"\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}"),
]
NARRATION = ["一般形式", "两边同时除以 a", "移项：两边同减 c/a",
             "配方：两边同加 (b/2a)²", "左边完全平方，右边通分",
             "两边开平方", "移项，公式成形"]


class QuadraticDerivation(Scene):
    """配方法七步推导：一屏一式，相同零件滑动衔接。"""

    def construct(self):
        eq = MathTex(*STEPS[0])
        caption = Text(NARRATION[0], font=FONT, font_size=30)
        caption.move_to(CAPTION_POS)
        self.play(Write(eq), Write(caption))
        self.wait(0.8)

        for i in range(1, len(STEPS)):
            nxt = MathTex(*STEPS[i])
            new_caption = Text(NARRATION[i], font=FONT, font_size=30)
            new_caption.move_to(CAPTION_POS)
            self.play(Transform(caption, new_caption),
                      TransformMatchingTex(eq, nxt), run_time=2)
            eq = nxt
            if i == 3:   # 配方步：补上的那一项是"钥匙"，染绿
                eq.set_color_by_tex(r"\left(\dfrac{b}{2a}\right)^2", GREEN)
            self.wait(0.8)

        self.play(eq.animate.set_color(GOLD).scale(1.25))  # 结论就位
        self.play(Transform(caption,
                            Text("求根公式", font=FONT, font_size=34,
                                 color=GOLD).move_to(CAPTION_POS)))
        self.wait(2)
