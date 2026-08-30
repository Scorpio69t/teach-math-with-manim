from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2     # 注释条固定锚点（换内容时保持位置稳定）


class TransformFamily(Scene):
    """同一个"变身"，三种语义：留引用、换件、留档。"""

    def set_note(self, msg):
        """注释条原地换内容：Transform 更新，锚点不动。"""
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.play(Transform(self.note, new, run_time=0.4))

    def construct(self):
        title = Text("Transform 三兄弟", font=FONT, font_size=32,
                     weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("同一个变字，三种语义", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # ── 第一幕：Transform —— 原地变身，引用不变 ──
        sq = Square(side_length=2, color=BLUE, fill_opacity=0.5)
        sq.shift(UP * 0.5)
        self.play(Create(sq))
        self.set_note("Transform：正方形变成圆——但它还是它")
        self.play(Transform(sq, Circle(radius=1.2, color=GOLD,
                                       fill_opacity=0.5).move_to(sq)),
                  run_time=1.5)
        self.play(sq.animate.shift(RIGHT * 2), run_time=1)   # 引用还活着！
        self.wait(1)

        # ── 第二幕：ReplacementTransform —— 旧件退役，新件接管 ──
        tri = Triangle(color=BLUE, fill_opacity=0.5).scale(1.2)
        tri.move_to(LEFT * 2 + UP * 0.5)
        self.play(Create(tri))
        self.set_note("ReplacementTransform：三角形退役，五角星接管")
        star = Star(color=GOLD, fill_opacity=0.5).scale(1.2)
        star.move_to(tri)
        self.play(ReplacementTransform(tri, star), run_time=1.5)
        self.play(star.animate.shift(RIGHT * 2), run_time=1)  # 请用新变量 star
        self.wait(1)
        # 清场不退场：前两幕演员缩小置顶，三种语义留在台上对照
        self.play(sq.animate.scale(0.5).move_to(RIGHT * 3 + UP * 2.2),
                  star.animate.scale(0.5).move_to(LEFT * 3 + UP * 2.2))

        # ── 第三幕：TransformFromCopy —— 复制变身，原件留档 ──
        card = RoundedRectangle(width=3, height=1.2, corner_radius=0.15,
                                color=BLUE, fill_opacity=0.5)
        card.move_to(LEFT * 2 + UP * 0.5)
        word = Text("原式", font=FONT, font_size=30, color=C_TEXT)
        word.move_to(card)
        self.play(FadeIn(card), FadeIn(word))
        self.set_note("TransformFromCopy：复制一份去变身，原件留在原地")
        result = Text("化简结果", font=FONT, font_size=30, color=GOLD)
        result.move_to(RIGHT * 2.5 + UP * 0.5)
        self.play(TransformFromCopy(word, result), run_time=1.5)
        self.wait(1.5)   # 原件 word 还在左区，证明"留档"
