"""模板：几何证明（构造 + 标注 + Indicate 关键件）

用法：替换图形构造与读数命题；「构造 → 标注 → 关键件强调 → 结案」的骨架不要动。
演示内容：对顶角相等——两条直线相交，一对对顶角同步 Indicate，读数同源报角度。

渲染：manim -pqh geometry_proof.py GeometryProof
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.55
R1_POS = [4.4, 2.4, 0]
VERDICT_POS = [0, -2.75, 0]

ANGLE_DEG = 38.0           # 两线夹角（基础参数，一切由此派生）
HALF_LEN = 2.6


class GeometryProof(Scene):
    """节奏分镜：
    | 段落 | 时长 | 画面动作 | 讲解要点 |
    | 构造 | 4 s  | 两线相交于 O | 一个交点，两对对顶角 |
    | 标注 | 5 s  | 角标 + 读数同源现算 | 对顶角读数始终相等 |
    | 强调 | 3 s  | Indicate 一対对顶角 | 相等不是巧合 |
    | 结案 | 4 s  | verdict 定格 | 对顶角相等 |
    """

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("对顶的两个角，为什么一定相等？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("先看图：两条直线交于一点", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        # ===== 构造：基础参数 ANGLE_DEG，全部点位由此派生 =====
        O = [-1.2, 0.2, 0]
        theta = np.radians(ANGLE_DEG)
        l1 = Line(O + LEFT * HALF_LEN, O + RIGHT * HALF_LEN,
                  color=TEAL, stroke_width=3.5)
        d = np.array([np.cos(theta), np.sin(theta), 0]) * HALF_LEN
        l2 = Line(O - d, O + d, color=TEAL, stroke_width=3.5)
        self.play(Create(l1), Create(l2), run_time=1.4)
        self.set_note("两条直线一交，相对的两个角叫对顶角")
        self.wait(1.8)

        # ===== 标注：角弧与读数都从 theta 现算 =====
        a1 = Arc(radius=0.7, start_angle=0, angle=theta,
                 arc_center=O, color=GOLD, stroke_width=4)
        a2 = Arc(radius=0.7, start_angle=PI, angle=theta,
                 arc_center=O, color=GOLD, stroke_width=4)
        r1 = Text(f"两个金色角都是 {ANGLE_DEG:.0f}°", font=FONT,
                  font_size=26, color=GOLD)
        r1.move_to(R1_POS, aligned_edge=RIGHT)
        self.play(Create(a1), run_time=0.8)
        self.set_note("第一个角：从水平线量起")
        self.wait(1.2)
        self.play(Create(a2), FadeIn(r1), run_time=0.8)
        self.set_note("对面的角：同样的张开程度——因为边还是那两条线")
        self.wait(2.0)

        # ===== 强调：关键件 Indicate =====
        self.play(Indicate(a1, color=GOLD), Indicate(a2, color=GOLD),
                  run_time=1.0)
        self.set_note("各补一个邻角都是 180°——去掉同一个邻角，剩下的必等")
        self.wait(2.2)

        # ===== 结案 =====
        verdict = Text("对顶角相等：同减去邻角，剩下的必然一样",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to(VERDICT_POS)
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("证明的结构：等量减等量，差相等")
        self.wait(2.8)
