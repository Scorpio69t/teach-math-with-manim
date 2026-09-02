"""derivation_chain.py — 推导链模板：一屏一式的公式推导动画骨架

适用：解方程、公式推导、化简链、证明步骤链（提炼自《Manim，让数学看得见》第 5 章
求根公式案例）。把推导链数据化（STEPS）、解说话语数据化（NARRATION），播放循环化。

骨架必须保留：
  1. STEPS / NARRATION 数据列表与类分离——改推导只动列表，循环体不碰；
  2. 每个状态一个多参数 MathTex——按"教学上需独立操纵的最小单位"拆零件，
     相邻两步的零件写法保持一致，TransformMatchingTex 才能平滑配对；
  3. 字幕真实首句初始化 + CAPTION_POS 固定锚点 + become 换词（动态文本铁律）；
  4. 链内引用交接 `eq = nxt`——少了这行，第二步开始所有配对错乱；
  5. 每步变形 run_time ≥ 2 秒，步间 wait ≥ 0.8 秒——每个节拍等得起一句讲解。

渲染：manim -pqh derivation_chain.py DerivationChain
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
CAPTION_POS = DOWN * 3.2  # 注释条固定锚点

# ===== 改写区：只动这两张表 =====
# 示例推导链：解一元一次方程 2x + 3 = 9
STEPS = [
    (r"2x", r"+", r"3", r"=", r"9"),
    (r"2x", r"=", r"9", r"-", r"3"),
    (r"2x", r"=", r"6"),
    (r"x", r"=", r"3"),
]
NARRATION = ["原方程", "两边同时减去 3", "右边算出 6", "两边同时除以 2"]
HIGHLIGHT_STEP = None  # 需要染色的步骤号（如 3），None 表示不染
HIGHLIGHT_TEX = None   # 要染色的零件写法，如 r"3"
# ===== 改写区结束 =====


class DerivationChain(Scene):
    """推导链通用骨架：一屏一式，相同零件滑动衔接，字幕钉死底部锚点。"""

    def construct(self):
        eq = MathTex(*STEPS[0])
        caption = Text(NARRATION[0], font=FONT, font_size=30)
        caption.move_to(CAPTION_POS)
        self.play(Write(eq), run_time=1.8)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(0.8)

        for i in range(1, len(STEPS)):
            nxt = MathTex(*STEPS[i])
            # 字幕换词：先锚定位置再 become，位置纹丝不动
            caption.become(
                Text(NARRATION[i], font=FONT, font_size=30).move_to(CAPTION_POS))
            self.play(TransformMatchingTex(eq, nxt), run_time=2)
            eq = nxt  # 链内引用交接：下一轮以新公式为源
            if HIGHLIGHT_STEP is not None and i == HIGHLIGHT_STEP:
                eq.set_color_by_tex(HIGHLIGHT_TEX, GREEN)  # 绿 = 就位/关键补项
            self.wait(0.8)

        # 终帧：结论染金放大，"就位"的仪式感
        self.play(eq.animate.set_color(GOLD).scale(1.25), run_time=1.2)
        self.wait(2)
