from manim import *
import numpy as np

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.4     # 注释条固定锚点（本书动态文本规范：换内容不换对象）

R_OUT, R_IN = 2.3, 2.3 * 0.382   # 五角星外/内半径
CENTER = np.array([0, 0.2, 0])
PTS_PER_EDGE = 20                 # 每条边采样 20 点，共 200 个采样点
N_COMP = 9                        # 参与叠加的旋转分量个数
TRACE_TIME = 14.0                 # 描完一整圈的时长


def star_contour():
    """五角星轮廓：外内交替的 10 个顶点，均匀采样成复数序列。"""
    vs = []
    for k in range(10):
        ang = np.deg2rad(90 + k * 36)
        r = R_OUT if k % 2 == 0 else R_IN
        vs.append(np.array([r * np.cos(ang), r * np.sin(ang)]))
    pts = []
    for k in range(10):
        a, b = vs[k], vs[(k + 1) % 10]
        for j in range(PTS_PER_EDGE):
            pts.append(a + (b - a) * j / PTS_PER_EDGE)
    return np.array([p[0] + 1j * p[1] for p in pts]), vs


class FourierStar(Scene):
    """欧拉公式的华丽应用：9 支各按自身频率旋转的箭头首尾相接，
    末端描出一颗五角星——这就是离散傅里叶级数。"""

    def set_note(self, msg):
        self.note.become(Text(msg, font=FONT, font_size=26, color=C_TEXT)
                         .move_to(NOTE_POS))

    def construct(self):
        # ===== 信号与分解（离散傅里叶变换） =====
        signal, verts = star_contour()
        NPTS = len(signal)
        coeffs = np.fft.fft(signal) / NPTS
        freqs = np.array([j if j <= NPTS // 2 else j - NPTS
                          for j in range(NPTS)])
        top = np.argsort(np.abs(coeffs))[::-1][:N_COMP]
        comps = sorted([(int(freqs[j]), float(np.abs(coeffs[j])),
                         float(np.angle(coeffs[j]))) for j in top],
                       key=lambda c: -c[1])   # 大的在外圈

        title = Text("几个圆，能画一颗星？", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("欧拉公式说：e^(iθ) 是一支会旋转的箭头",
                         font=FONT, font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)
        self.wait(1.8)

        panel = Text(f"{N_COMP} 支旋转的箭头，首尾相接",
                     font=FONT, font_size=24, color=C_TEXT)
        panel.move_to([4.7, 2.6, 0], aligned_edge=RIGHT)
        self.play(FadeIn(panel), run_time=0.7)
        self.set_note("让它们各转各的——盯住最末端")
        self.wait(1.6)

        # ===== 旋转向量链 =====
        th = ValueTracker(0.0)

        def chain_points():
            """当前时刻各关节位置（屏幕坐标）。"""
            pos = np.array([0.0, 0.0])
            pts = [pos.copy()]
            for f, amp, ph in comps:
                pos = pos + amp * np.array(
                    [np.cos(f * th.get_value() + ph),
                     np.sin(f * th.get_value() + ph)])
                pts.append(pos.copy())
            return [CENTER + np.array([p[0], p[1], 0]) for p in pts]

        def build_chain():
            pts = chain_points()
            g = VGroup()
            for k in range(N_COMP):
                g.add(DashedVMobject(
                    Circle(radius=max(np.linalg.norm(
                        pts[k + 1] - pts[k]), 0.001),
                        color=GREY_B, stroke_width=1, stroke_opacity=0.4)
                    .move_to(pts[k]), num_dashes=30))
                g.add(Arrow(pts[k], pts[k + 1], buff=0,
                            color=TEAL if k < N_COMP - 1 else GOLD,
                            stroke_width=3 if k < N_COMP - 1 else 5,
                            max_tip_length_to_length_ratio=0.3))
            return g

        chain = always_redraw(build_chain)   # 挂 redraw 的对象只能 add
        tip = Dot(color=GOLD, radius=0.07)
        tip.add_updater(lambda m: m.move_to(chain_points()[-1]))
        trace = TracedPath(tip.get_center, stroke_color=GOLD,
                           stroke_width=3.5)
        self.add(chain, tip, trace)

        # ===== 开转：一整圈 =====
        self.set_note("大圈慢转，小圈疯转——末端开始画画")
        self.play(th.animate.set_value(2 * PI * 0.45),
                  run_time=TRACE_TIME * 0.45, rate_func=linear)
        self.set_note("棱角出来了：五个尖，一个不少")
        self.play(th.animate.set_value(2 * PI * 0.8),
                  run_time=TRACE_TIME * 0.35, rate_func=linear)
        self.set_note("最后一段，封口……")
        self.play(th.animate.set_value(2 * PI),
                  run_time=TRACE_TIME * 0.2, rate_func=linear)
        self.set_note("一颗五角星——从 9 个圆里长出来的")
        self.wait(2.0)

        # ===== 对照：淡色原轮廓 =====
        ghost = Polygon(*[CENTER + np.array([v[0], v[1], 0])
                          for v in verts],
                        color=C_TEXT, stroke_width=1.5,
                        stroke_opacity=0.5)
        self.play(FadeIn(ghost), run_time=1.0)
        self.set_note("和真实轮廓几乎重合——9 个圆已经够用")
        self.play(th.animate.set_value(2 * PI * 1.15),
                  run_time=2.2, rate_func=linear)   # 让链条再活一会儿
        self.wait(1.0)

        # ===== 点题 =====
        self.remove(chain, tip)     # 箭头退场，轨迹与轮廓留下
        verdict = Text("任何轮廓 = 一圈圈旋转的叠加（傅里叶级数）",
                       font=FONT, font_size=28, weight=BOLD, color=GOLD)
        verdict.move_to([0, -2.9, 0])
        self.play(FadeIn(verdict, shift=UP * 0.3), run_time=0.9)
        self.set_note("从 i 到 e^(iθ) 再到傅里叶——复数的故事才刚开始")
        self.wait(3.0)
