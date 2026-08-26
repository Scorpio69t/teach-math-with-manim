from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2


class TrackerPanel(Scene):
    """ValueTracker 是遥控器：它只管变，谁读它谁动。"""

    def set_note(self, msg):
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.play(Transform(self.note, new, run_time=0.4))

    def construct(self):
        title = Text("ValueTracker：一个会变的数", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("遥控器上没有像素", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        tracker = ValueTracker(1.0)   # 遥控器：初始值 1

        # 仪表一：数字面板，每帧读 tracker（updater 预习 7.3）
        number = DecimalNumber(1.0, num_decimal_places=2,
                               font_size=64, color=GOLD)
        number.move_to(UP * 1.6)
        number.add_updater(lambda d: d.set_value(tracker.get_value()))

        # 仪表二：进度条，宽度跟着数值走
        bar = Rectangle(width=tracker.get_value() * 2, height=0.6,
                        color=BLUE, fill_opacity=0.8)
        bar.move_to(DOWN * 0.2, aligned_edge=LEFT)
        bar.add_updater(
            lambda b: b.stretch_to_fit_width(tracker.get_value() * 2)
        )

        self.add(number, bar)
        self.set_note("tracker 从 1 渐变到 3.5——两块仪表同步跟随")
        self.play(tracker.animate.set_value(3.5), run_time=3)
        self.wait(1)

        self.set_note("再收回到 0.5——同一个遥控器，全程只需一句话")
        self.play(tracker.animate.set_value(0.5), run_time=2.5)
        self.wait(1.5)
