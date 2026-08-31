"""冒泡排序教学动画（精修演示版，ManimCE v0.18+）

渲染：manim -pqh bubble_sort.py BubbleSortScene
可运行的 ManimCE 冒泡排序教学案例。

设计要点：
- 颜色语义：金=正在比较，红=发生交换，绿=已就位，暗蓝灰=未参与；
- 指针系统：j / j+1 金色箭头全程在场，移动本身就是叙事；
- 节奏控制：每个节拍都等得起一句讲解；底部字幕同步给出讲解词。

节奏调节：改下面这个数即可（所有关键节拍和字幕停留时间都会按比例缩放）
    PACE = 1.0  标准节奏（约 45 秒）
    PACE = 1.3  舒缓节奏，适合首次观看的读者/评审（约 60 秒）
"""

from manim import *

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"


class BubbleSortScene(Scene):
    """冒泡排序完整教学动画：片头 → 建数组 → 逐轮比较交换 → 收尾点题。"""

    # ---- 节奏系数：字幕看不完就调大它（推荐先试 1.3） ----
    PACE = 1.3

    # ---- 颜色语义表：每种状态使用固定颜色 ----
    C_DEFAULT = "#1C2541"   # 未参与（暗蓝灰）
    C_COMPARE = GOLD        # 正在比较
    C_SWAP = "#FF5A5A"      # 发生交换
    C_SORTED = "#5EE8A0"    # 已就位
    C_EDGE = "#8A93B8"      # 单元格边框
    C_TEXT = "#EDEDED"      # 字幕主色
    C_MUTED = "#9AA3C0"     # 次要文字

    def construct(self):
        pace = self.PACE
        values = [5, 7, 3, 8, 2]
        n = len(values)

        # ========== 片头：标题卡 ==========
        title = Text("冒泡排序", font=FONT, font_size=64, weight=BOLD)
        subtitle = Text("Bubble Sort · 每一轮，让最大的元素冒到它该在的位置",
                        font=FONT, font_size=26, color=self.C_MUTED)
        subtitle.next_to(title, DOWN, buff=0.4)
        title_card = VGroup(title, subtitle)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5 * pace)
        self.play(title_card.animate.scale(0.55).to_edge(UP, buff=0.35),
                  run_time=0.8)

        # ========== 建立数组单元格 ==========
        cells = VGroup()
        for v in values:
            square = Square(side_length=1.0, stroke_color=self.C_EDGE,
                            stroke_width=2, fill_color=self.C_DEFAULT,
                            fill_opacity=1)
            number = Text(str(v), font=FONT, font_size=36, weight=BOLD,
                          color=WHITE)
            cells.add(VGroup(square, number))
        cells.arrange(RIGHT, buff=0.15).shift(UP * 0.5)
        self.play(LaggedStart(
            *[FadeIn(c, shift=UP * 0.4) for c in cells], lag_ratio=0.15),
            run_time=1.2)
        self.wait(0.4)

        # ========== 常驻 UI：轮次牌、计数器、字幕 ==========
        round_banner = Text("第 1 轮", font=FONT, font_size=28,
                            color=self.C_COMPARE)
        round_banner.to_corner(UL, buff=0.6).shift(DOWN * 0.7)
        cmp_counter = Text("比较 0 次", font=FONT, font_size=24,
                           color=self.C_MUTED)
        swap_counter = Text("交换 0 次", font=FONT, font_size=24,
                            color=self.C_MUTED)
        counters = VGroup(cmp_counter, swap_counter).arrange(RIGHT, buff=0.5)
        counters.to_corner(UR, buff=0.6).shift(DOWN * 0.7)
        self.play(FadeIn(round_banner), FadeIn(counters), run_time=0.6)

        CAPTION_POS = DOWN * 3.2   # 字幕固定锚点：画面底部，远离方块与指针
        caption = Text("相邻的两个元素比较大小，大的往后沉",
                       font=FONT, font_size=30, color=self.C_TEXT)
        caption.move_to(CAPTION_POS)

        def set_caption(msg, color=None):
            """生成字幕变换动画（Transform 原地变形，不闪烁）。"""
            new = Text(msg, font=FONT, font_size=30,
                       color=color or self.C_TEXT).move_to(CAPTION_POS)
            return Transform(caption, new, run_time=0.3 * pace)

        # ========== 指针：j 与 j+1 ==========
        ptr_j = self.make_pointer("j")
        ptr_j1 = self.make_pointer("j+1")
        ptr_j.next_to(cells[0], DOWN, buff=0.15)
        ptr_j1.next_to(cells[1], DOWN, buff=0.15)
        self.play(FadeIn(caption), FadeIn(ptr_j), FadeIn(ptr_j1),
                  run_time=0.8)
        self.wait(1.0 * pace)   # 开场字幕阅读时间

        # ========== 冒泡主过程 ==========
        cmp_cnt, swap_cnt = 0, 0
        for i in range(n - 1):
            # 轮次牌更新
            new_banner = Text(f"第 {i + 1} 轮", font=FONT, font_size=28,
                              color=self.C_COMPARE).move_to(round_banner)
            if i > 0:
                self.play(Transform(round_banner, new_banner), run_time=0.3)

            for j in range(n - 1 - i):
                a, b = values[j], values[j + 1]

                # 1. 指针就位 + 字幕预告（之后留阅读时间）
                self.play(
                    ptr_j.animate.next_to(cells[j], DOWN, buff=0.15),
                    ptr_j1.animate.next_to(cells[j + 1], DOWN, buff=0.15),
                    set_caption(f"比较 {a} 和 {b}"),
                    run_time=0.4 * pace,
                )
                self.wait(0.4 * pace)   # 读字幕
                # 2. 比较高亮（金色）
                self.play(
                    cells[j][0].animate.set_fill(self.C_COMPARE, 0.7),
                    cells[j + 1][0].animate.set_fill(self.C_COMPARE, 0.7),
                    run_time=0.5 * pace,
                )
                cmp_cnt += 1
                cmp_counter.become(
                    Text(f"比较 {cmp_cnt} 次", font=FONT, font_size=24,
                         color=self.C_MUTED).move_to(cmp_counter))

                # 3. 判断：交换 or 保持
                if a > b:
                    values[j], values[j + 1] = b, a
                    self.play(
                        set_caption(f"{a} > {b}，交换！", self.C_SWAP),
                        cells[j][0].animate.set_fill(self.C_SWAP, 0.8),
                        cells[j + 1][0].animate.set_fill(self.C_SWAP, 0.8),
                        run_time=0.3 * pace,
                    )
                    self.wait(0.4 * pace)   # 读字幕：判断结论
                    # CyclicReplace：沿弧线互换，轨迹本身就在说"交换"
                    self.play(CyclicReplace(cells[j], cells[j + 1]),
                              run_time=0.8 * pace)
                    cells[j], cells[j + 1] = cells[j + 1], cells[j]
                    swap_cnt += 1
                    swap_counter.become(
                        Text(f"交换 {swap_cnt} 次", font=FONT, font_size=24,
                             color=self.C_MUTED).move_to(swap_counter))
                else:
                    self.play(set_caption(f"{a} ≤ {b}，保持不动",
                                          self.C_MUTED),
                              run_time=0.3 * pace)
                    self.wait(0.5 * pace)   # 读字幕：不交换的结论

                # 4. 恢复默认色
                self.play(
                    cells[j][0].animate.set_fill(self.C_DEFAULT, 1),
                    cells[j + 1][0].animate.set_fill(self.C_DEFAULT, 1),
                    run_time=0.25,
                )

            # 5. 本轮最大元素就位：染绿 + 脉冲 + 停顿讲解
            settled = cells[n - 1 - i]
            self.play(
                settled[0].animate.set_fill(self.C_SORTED, 0.6),
                set_caption(f"第 {i + 1} 轮结束：{values[n - 1 - i]} 就位",
                            self.C_SORTED),
                run_time=0.4 * pace,
            )
            self.play(Indicate(settled, color=self.C_SORTED,
                               scale_factor=1.15), run_time=0.5 * pace)
            self.wait(0.8 * pace)   # 读字幕：本轮小结

        # ========== 收尾点题 ==========
        self.play(cells[0][0].animate.set_fill(self.C_SORTED, 0.6),
                  run_time=0.3)
        self.play(FadeOut(ptr_j), FadeOut(ptr_j1), run_time=0.4)
        self.play(LaggedStart(
            *[Indicate(c, color=self.C_SORTED, scale_factor=1.12)
              for c in cells], lag_ratio=0.12), run_time=1.2 * pace)
        self.play(set_caption("排序完成：每一轮，最大的泡泡都冒到了它该在的位置",
                              self.C_SORTED), run_time=0.5)
        self.wait(3.0 * pace)   # 金句停留，留出完整阅读时间

    @staticmethod
    def make_pointer(label):
        """生成金色指针：向上的箭头 + 斜体标签（用 Text 渲染，无需 LaTeX 环境）。"""
        arrow = Arrow(ORIGIN, UP * 0.45, buff=0,
                      color=GOLD, stroke_width=4,
                      max_tip_length_to_length_ratio=0.35)
        text = Text(label, font=FONT, font_size=30, color=GOLD, slant=ITALIC)
        text.next_to(arrow, DOWN, buff=0.08)
        return VGroup(arrow, text)
