from manim import *

FONT = "Microsoft YaHei"  # macOS: "PingFang SC" / Linux: "Noto Sans CJK SC"
C_TEXT = "#EDEDED"
NOTE_POS = DOWN * 3.2


class UpdaterDemo(Scene):
    """updater 两种签名：状态型追随别人，时间型跟着时钟走。"""

    def set_note(self, msg):
        new = Text(msg, font=FONT, font_size=26, color=C_TEXT)
        new.move_to(NOTE_POS)
        self.play(Transform(self.note, new, run_time=0.4))

    def construct(self):
        title = Text("updater：每帧渲染前先看一眼", font=FONT,
                     font_size=32, weight=BOLD, color=C_TEXT)
        title.to_corner(UL, buff=0.5)
        self.note = Text("状态型：跟别的对象走", font=FONT,
                         font_size=26, color=C_TEXT)
        self.note.move_to(NOTE_POS)
        self.add(title, self.note)

        # 状态型：箭头每帧重算指向，始终对准目标点
        target = Dot(LEFT * 3 + UP * 0.5, color=RED, radius=0.1)
        base = Dot(RIGHT * 1.5 + DOWN * 1.2, color=BLUE, radius=0.08)
        arrow = Arrow(base.get_center(), target.get_center(),
                      color=GOLD, buff=0.15, stroke_width=6)
        follow = lambda a: a.put_start_and_end_on(
            base.get_center(), target.get_center())
        arrow.add_updater(follow)
        self.add(target, base, arrow)

        # 时间型：角落的秒针文字，每帧累积 dt 自转
        # 放右上：避开底部注释条锚点（DOWN*3.2 附近会被旋转扫到）
        spinner = Text("时间型 updater 在自转", font=FONT,
                       font_size=20, color=GREY_B)
        spinner.to_corner(UR, buff=0.6)
        spinner.add_updater(lambda m, dt: m.rotate(0.25 * dt))
        self.add(spinner)

        self.set_note("目标点游走，箭头每帧重新瞄准")
        self.play(target.animate.move_to(RIGHT * 2.5 + UP * 1.5),
                  run_time=2)
        self.play(target.animate.move_to(LEFT * 1 + DOWN * 0.8),
                  run_time=2)
        self.wait(0.8)

        # 放手：卸下 updater，追踪结束
        arrow.remove_updater(follow)
        self.set_note("remove_updater 之后：目标再走，箭头不跟了")
        self.play(target.animate.move_to(UP * 2), run_time=2)
        self.wait(1.5)
