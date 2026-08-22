"""图 1-3 拼图用四张成品关键帧（静态合成场景）

渲染（静止帧，1080p）：
  manim -sqh fig1_3_stills.py QuadraticSlideStill
  manim -sqh fig1_3_stills.py SineWaveFromCircleStill
  manim -sqh fig1_3_stills.py BubbleSortStill
  manim -sqh fig1_3_stills.py GaltonBoardStill

版式遵循第 4 章标准帧：左上标题 + 金色短尺、底部固定注释条。
颜色语义：金=当前关注，红=变化/运动，绿=就位/结论，蓝灰=背景。
"""

from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS 改为 "PingFang SC"，Linux 改为 "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
C_MUTED = "#9AA3C0"
NOTE_Y = -3.35


def add_frame_chrome(scene, title_text, note_text):
    """标准帧三件套：左上标题、金色短尺、底部注释条。"""
    title = Text(title_text, font=FONT, font_size=32, weight=BOLD,
                 color=C_TEXT).to_corner(UL, buff=0.45)
    rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=3)
    rule.next_to(title, DOWN, buff=0.12).align_to(title, LEFT)
    note = Text(note_text, font=FONT, font_size=24, color=C_MUTED)
    note.move_to(DOWN * abs(NOTE_Y))
    scene.add(title, rule, note)


class QuadraticSlideStill(Scene):
    """第 9 章：二次函数开口随 a 变化（三条抛物线对比，金色为当前值）。"""

    def construct(self):
        add_frame_chrome(self, "第 9 章｜二次函数：a 管开口的方向与宽窄",
                         "a 越大，开口越窄——拖动滑杆，曲线跟着变")

        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 6, 2],
                    x_length=8.6, y_length=4.6,
                    axis_config={"color": C_MUTED, "stroke_width": 2},
                    tips=False).shift(DOWN * 0.45 + LEFT * 0.3)

        def parabola(a, color, width):
            xmax = min(3.9, np.sqrt(5.9 / a))   # 让曲线停在画面内
            return axes.plot(lambda x: a * x**2, x_range=[-xmax, xmax],
                             color=color, stroke_width=width)

        p_thin = parabola(0.4, C_MUTED, 3)
        p_gold = parabola(1.0, GOLD, 6)
        p_steep = parabola(2.2, C_MUTED, 3)

        # 三条曲线在顶部挤在一起，直接标注必撞车——改用右上角图例：
        # 色块 + 文字纵向排列，左侧对齐（先内部排版、再整体定位）
        legend = VGroup()
        for a, color, bold in [(0.4, C_MUTED, False), (1.0, GOLD, True),
                               (2.2, C_MUTED, False)]:
            swatch = Line(LEFT * 0.35, RIGHT * 0.35, color=color,
                          stroke_width=6 if bold else 3)
            txt = Text(f"a = {a:g}", font=FONT, font_size=24, color=color,
                       weight=BOLD if bold else NORMAL)
            txt.next_to(swatch, RIGHT, buff=0.15)
            legend.add(VGroup(swatch, txt))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend.to_corner(UR, buff=0.55).shift(DOWN * 0.8)

        self.add(axes, p_thin, p_gold, p_steep, legend)
        self.wait(0.1)


class SineWaveFromCircleStill(Scene):
    """第 11 章：单位圆上的点转动，纵坐标投影出正弦波（关键中间帧）。"""

    def construct(self):
        add_frame_chrome(self, "第 11 章｜单位圆：转出来的正弦波",
                         "圆上那一点的高度，展开成直线——就是正弦曲线")

        theta = 2.3   # 当前转角：曲线正好描到一半，最有"进行中"的张力

        axes = Axes(x_range=[0, 6.6, PI / 2], y_range=[-1.5, 1.5, 1],
                    x_length=7.6, y_length=3.4,
                    axis_config={"color": C_MUTED, "stroke_width": 2},
                    tips=False).shift(RIGHT * 2.7 + UP * 0.55)
        origin_y = axes.c2p(0, 0)[1]
        unit = axes.c2p(0, 1)[1] - origin_y   # 圆半径与坐标轴单位对齐

        circle_center = np.array([-4.1, origin_y, 0])
        circle = Circle(radius=unit, color=C_MUTED, stroke_width=3)
        circle.move_to(circle_center)

        point_on_circle = circle_center + unit * np.array(
            [np.cos(theta), np.sin(theta), 0])
        radius_line = Line(circle_center, point_on_circle, color=GOLD,
                           stroke_width=4)
        dot_on_circle = Dot(point_on_circle, radius=0.09, color=GOLD)
        angle_arc = Arc(radius=0.55, start_angle=0, angle=theta,
                        arc_center=circle_center, color=GOLD, stroke_width=3)
        theta_label = Text("θ", font=FONT, font_size=26, color=GOLD)
        # 收在角度弧与投影虚线之间的空隙：离开弧线 0.2，低于虚线 0.2
        theta_label.move_to(circle_center + np.array(
            [0.95 * np.cos(theta / 2), 0.95 * np.sin(theta / 2) * 0.75, 0]))

        # 已描出的正弦曲线（绿=结论），终点与圆上的点同高
        traced = axes.plot(np.sin, x_range=[0, theta], color=GREEN,
                           stroke_width=5)
        trace_end = axes.c2p(theta, np.sin(theta))
        dot_on_curve = Dot(trace_end, radius=0.09, color=GOLD)
        projection = DashedLine(point_on_circle, trace_end, color=GOLD,
                                stroke_width=2, dash_length=0.08)

        self.add(axes, circle, radius_line, angle_arc, theta_label,
                 dot_on_circle, traced, dot_on_curve, projection)
        self.wait(0.1)


class BubbleSortStill(Scene):
    """第 15 章：冒泡排序中间帧——金色比较中，绿色已就位。"""

    VALUES = [3, 1, 5, 2, 4, 6, 7, 8]
    COMPARING = (1, 2)   # 正在比较的下标
    SORTED_FROM = 5      # 从此下标起已就位

    def construct(self):
        add_frame_chrome(self, "第 15 章｜冒泡排序：相邻比较，大数沉底",
                         "每一轮两两比较，最大的元素向右「沉底」就位")

        n = len(self.VALUES)
        base_y, unit_h, bar_w, gap = -2.1, 0.42, 0.72, 0.28
        total_w = n * bar_w + (n - 1) * gap
        x0 = -total_w / 2 + bar_w / 2

        bars = VGroup()
        for i, v in enumerate(self.VALUES):
            if i >= self.SORTED_FROM:
                color = GREEN        # 就位
            elif i in self.COMPARING:
                color = GOLD         # 正在比较
            else:
                color = C_MUTED      # 待处理
            bar = Rectangle(width=bar_w, height=v * unit_h,
                            fill_color=color, fill_opacity=0.85,
                            stroke_color=color, stroke_width=2)
            bar.move_to([x0 + i * (bar_w + gap), base_y + v * unit_h / 2, 0])
            label = Text(str(v), font=FONT, font_size=22, color=color)
            label.next_to(bar, UP, buff=0.12)
            bars.add(VGroup(bar, label))

        # 比较对上方的弧线箭头：交换意图的视觉预告
        # 两端对齐到同一高度，弧线对称，读者一眼看出"这是一对"
        top_y = max(bars[self.COMPARING[0]][0].get_top()[1],
                    bars[self.COMPARING[1]][0].get_top()[1]) + 0.6
        p_left = [bars[self.COMPARING[0]][0].get_center()[0], top_y, 0]
        p_right = [bars[self.COMPARING[1]][0].get_center()[0], top_y, 0]
        swap_arc = CurvedArrow(p_left, p_right, angle=TAU / 6,
                               color=GOLD, stroke_width=3,
                               tip_length=0.22)

        self.add(bars, swap_arc)
        self.wait(0.1)


class GaltonBoardStill(Scene):
    """第 14 章：Galton 钉板——下落路径（红）、堆积（绿）、正态轮廓（金）。"""

    ROWS = 7
    BIN_HEIGHTS = [1, 3, 6, 9, 6, 3, 1]   # 已堆出钟形的各槽球数

    def construct(self):
        add_frame_chrome(self, "第 14 章｜Galton 钉板：一万次随机之后",
                         "每个小球向左向右各一半概率——堆起来，就是钟形曲线")

        dx, dy, top_y = 0.62, 0.52, 1.9
        pegs = VGroup()
        for r in range(self.ROWS):
            for c in range(r + 1):
                pegs.add(Dot([ (c - r / 2) * dx, top_y - r * dy, 0],
                             radius=0.045, color=C_MUTED))

        # 底部球槽：绿色小球堆出钟形
        ball_r, bin_y0 = 0.075, -2.35
        balls = VGroup()
        for b, h in enumerate(self.BIN_HEIGHTS):
            for k in range(h):
                balls.add(Dot([ (b - 3) * dx, bin_y0 + k * ball_r * 2, 0],
                              radius=ball_r, color=GREEN,
                              fill_opacity=0.9))

        # 正态轮廓线（金）：手算钟形点，贴合堆高
        xs = np.linspace(-3 * dx, 3 * dx, 120)
        peak = 9 * ball_r * 2
        ys = bin_y0 + peak * np.exp(-(xs / (1.35 * dx)) ** 2)
        curve = VMobject(color=GOLD, stroke_width=4)
        curve.set_points_smoothly(
            [np.array([x, y + 0.12, 0]) for x, y in zip(xs, ys)])

        # 一颗还在下落的小球（红=变化）与它的折线路径
        path_pts = [[-0.3, 2.45, 0], [-0.62 + 0.31, 1.6, 0],
                    [0.31, 0.85, 0], [-0.31, 0.1, 0], [0.0, -0.7, 0]]
        fall_path = VMobject(color=RED, stroke_width=2.5)
        fall_path.set_points_as_corners([np.array(p) for p in path_pts])
        fall_path.set_stroke(opacity=0.6)
        falling = Dot(path_pts[-1], radius=ball_r, color=RED)

        self.add(pegs, balls, curve, fall_path, falling)
        self.wait(0.1)
