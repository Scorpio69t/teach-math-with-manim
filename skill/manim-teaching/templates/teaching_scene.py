"""模板：教学场景五件套骨架（标题 + 注释条 + 读数面板 + verdict + 节奏分镜）

用法：复制本文件，替换 construct 里的演示内容；五件套的锚点与版式不要动。
演示内容（可删）：正方形边长 a 从 1 长到 3，读数报面积 a²——展示读数与几何同源。

渲染：manim -pqh teaching_scene.py TeachingScene
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55       # 注释条固定锚点
R1_POS = [4.6, 2.4, 0]       # 读数第一行（标签右缘钉死）
R2_POS = [4.6, 1.8, 0]       # 读数第二行
VERDICT_POS = [0, -2.75, 0]  # verdict 结案语锚点


class TeachingScene(Scene):
    """节奏分镜：
    | 段落 | 时长 | 画面动作 | 讲解要点 |
    | 提问 | 3 s  | 标题注释登场 | 面积随边长怎么变 |
    | 演示 | 8 s  | 边长滑杆 1→3，读数同源现算 | a² 不是 2a |
    | 结案 | 4 s  | verdict 定格 | 面积是平方关系 |
    """

    def set_note(self, msg):
        """注释条换词：become 原地变形 + 固定锚点，防闪烁防漂移。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        # ===== 五件套之一：标题（问题式，不用定义式） =====
        title = Text("边长翻倍，面积翻几倍？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        # ===== 五件套之二：注释条（真实首句初始化，禁空文本） =====
        self.note = Text("拖动边长，盯住面积读数", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 演示区：几何与读数同源（同一个 a 驱动） =====
        a = ValueTracker(1.0)
        square = always_redraw(lambda: Square(
            side_length=a.get_value(), color=TEAL, stroke_width=4,
            fill_opacity=0.3).move_to([-1.5, 0.3, 0]))
        r1 = always_redraw(lambda: Text(
            f"边长 a = {a.get_value():.1f}", font=FONT, font_size=26,
            color=C_TEXT).move_to(R1_POS, aligned_edge=RIGHT))
        r2 = always_redraw(lambda: Text(
            f"面积 = {a.get_value() ** 2:.1f}", font=FONT, font_size=26,
            color=GREEN).move_to(R2_POS, aligned_edge=RIGHT))
        self.play(FadeIn(square), FadeIn(r1), FadeIn(r2), run_time=0.9)
        self.wait(1.2)
        self.play(a.animate.set_value(2.0), run_time=1.6,
                  rate_func=linear)
        self.set_note("边长 ×2——面积 ×4，不是 ×2")
        self.wait(2.0)
        self.play(a.animate.set_value(3.0), run_time=1.6,
                  rate_func=linear)
        self.set_note("边长 ×3——面积 ×9：倍数自己被平方了")
        self.wait(2.0)

        # ===== 五件套之四：verdict 结案语 =====
        verdict = Text("面积随边长平方增长：倍数进，平方出",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("读数与几何同源：同一个 a，画面与数字永不打架")
        self.wait(2.8)
