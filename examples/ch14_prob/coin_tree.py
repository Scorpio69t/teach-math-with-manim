from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（换内容时保持位置稳定）


def coin(label, color, radius=0.26):
    """一枚硬币：圆 + 面字。"""
    c = Circle(radius=radius, fill_color=color, fill_opacity=0.9,
               stroke_color=WHITE, stroke_width=2)
    t = Text(label, font=FONT, font_size=22, color=BLACK)
    t.move_to(c.get_center())
    return VGroup(c, t)


class CoinTree(Scene):
    """抛两枚硬币的树状图：四种等可能结果，"一正一反"占两条路径。"""

    def set_note(self, msg):
        """注释条铁律：真实首句初始化 + 固定锚点 + become 换词。"""
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        title = Text("抛两枚硬币：一正一反的概率是 1/3 吗", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("抛两枚硬币，正好一正一反的概率是多少？",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.6)

        # ===== 错误直觉先亮相 =====
        self.set_note("不少同学抢答：两正、一正一反、两反——3 种，所以 1/3")
        self.wait(2.4)
        self.set_note("别急。把过程画成树：一层一枚硬币，一条枝一个结果")
        self.wait(2.0)

        # ===== 树状图（横向，左根右叶） =====
        root_pos = np.array([-5.2, 0.6, 0])
        l1 = {"正": np.array([-2.9, 1.9, 0]),
              "反": np.array([-2.9, -0.7, 0])}
        leaf_pos = {
            ("正", "正"): np.array([-0.4, 2.5, 0]),
            ("正", "反"): np.array([-0.4, 1.3, 0]),
            ("反", "正"): np.array([-0.4, -0.1, 0]),
            ("反", "反"): np.array([-0.4, -1.3, 0]),
        }

        root = Dot(root_pos, color=GOLD, radius=0.09)
        self.play(FadeIn(root, scale=0.5), run_time=0.5)

        self.set_note("第一层：第一枚硬币，正或反")
        edges1, coins1 = {}, {}
        for face, pos in l1.items():
            e = Line(root_pos, pos, color=GREY_B, stroke_width=2.5)
            c = coin(face, GOLD if face == "正" else TEAL).move_to(pos)
            edges1[face], coins1[face] = e, c
            self.play(Create(e), FadeIn(c, scale=0.5), run_time=0.9)
        self.wait(1.2)

        self.set_note("第二层：每种结果再分两支——不管第一枚是什么")
        edges2, coins2 = {}, {}
        for (f1, f2), pos in leaf_pos.items():
            e = Line(l1[f1], pos, color=GREY_B, stroke_width=2.5)
            c = coin(f2, GOLD if f2 == "正" else TEAL,
                     radius=0.22).move_to(pos)
            edges2[(f1, f2)], coins2[(f1, f2)] = e, c
        self.play(*[Create(e) for e in edges2.values()],
                  *[FadeIn(c, scale=0.5) for c in coins2.values()],
                  run_time=2.2)
        self.wait(1.6)

        # ===== 数结果 =====
        self.set_note("数叶子：4 个终点，4 种等可能的结果")
        panel = Text("4 种结果，每种概率 1/4", font=FONT, font_size=26,
                     color=C_TEXT)
        panel.move_to([3.6, 0.6, 0])
        self.play(FadeIn(panel, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(2.0)

        # ===== 高亮"一正一反"两条路径 =====
        self.set_note("一正一反藏在哪里？金色两条路：正反、反正")
        paths = VGroup()
        for key in (("正", "反"), ("反", "正")):
            seg = VGroup(edges1[key[0]].copy().set_color(GOLD)
                         .set_stroke(width=6),
                         edges2[key].copy().set_color(GOLD)
                         .set_stroke(width=6))
            paths.add(seg)
        self.play(FadeIn(paths), run_time=1.0)
        self.wait(1.2)
        self.play(Indicate(coins2[("正", "反")], color=GOLD),
                  Indicate(coins2[("反", "正")], color=GOLD),
                  run_time=1.2)
        panel2 = Text("一正一反 = 2/4 = 1/2", font=FONT, font_size=28,
                      weight=BOLD, color=GOLD)
        panel2.move_to([3.6, -0.1, 0])
        self.play(FadeIn(panel2, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(2.2)

        # ===== 结案 =====
        self.set_note("「一正一反」是一种结果吗？不——它是两种结果打包")
        self.wait(2.4)
        self.set_note("树状图的价值：不重不漏，每条路径等可能")
        self.wait(2.4)
        self.set_note("先问「有哪些结果」，再问「各占几条路」")
        self.wait(2.6)
