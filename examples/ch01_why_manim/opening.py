"""代码清单1-1：三角形内角和——角纸片刚性搬运与平行线说明。

运行：manim -pqh opening.py OpeningScene
正文58秒：提问、辨角、作平行线、依次搬运两个底角、拼出平角、改变形状。
本文件独立运行，不需要LaTeX、外部图片、配音文件或辅助Python模块。
"""

from types import SimpleNamespace

import numpy as np
from manim import *

A = np.array([-2.9,-1.25,0.])
B = np.array([2.5,-1.25,0.])
C = np.array([.35,1.55,0.])
PAPER_LENGTH = 1.12


def triangle_corners(top):
    verts = [A,B,np.asarray(top,dtype=float)]
    if np.cross(B-A,verts[2]-A)[2] <= 1e-8:
        raise ValueError('Triangle must have its third vertex above the base.')
    result = []
    for i,v in enumerate(verts):
        u = verts[(i+1)%3]-v
        w = verts[(i-1)%3]-v
        u,w = u/np.linalg.norm(u),w/np.linalg.norm(w)
        start = np.arctan2(u[1],u[0])
        angle = np.mod(np.arctan2(w[1],w[0])-start,2*np.pi)
        if not 0 < angle < np.pi:
            raise ValueError('Invalid interior angle.')
        result.append({'vertex':v.copy(),'u':u,'w':w,'start':start,'angle':angle,
                       'points':np.array([v,v+PAPER_LENGTH*u,v+PAPER_LENGTH*w])})
    return result


FONT = 'Microsoft YaHei'  # macOS可改为PingFang SC；Linux可改为Noto Sans CJK SC
CORAL = ManimColor('#EE8177')
ICE = ManimColor('#66C8E3')
AMBER = ManimColor('#EFC375')
INK = ManimColor('#ECF1F5')
OUTLINE = ManimColor('#79B8CA')
COLORS = [CORAL,ICE,AMBER]
GLYPHS = ['α','β','γ']
NOTE_POS = np.array([0.,-3.28,0.])

CUES = [
    (0.55, '三角形的三个内角，合起来有多大？'),
    (5.3, '每个角都带着两条边。金色角留在原位。'),
    (11.3, '过上面的顶点，画一条与底边平行的直线。'),
    (16.3, '盯住红色角。整块转半圈，再移到上面的顶点。'),
    (22.6, '平行线之间，这两个内错角相等。'),
    (27.3, '蓝色角也一样。转半圈，再移到顶点右侧。'),
    (33.4, '它与原来的角，也是内错角相等。'),
    (38.3, '三个角的外侧两条边，正好连成一条直线。'),
    (43.7, '这是一个平角，一百八十度。'),
    (48.5, '改变三角形的形状，各个角变了，拼成的平角没有变。'),
]


def label_anchor(points):
    v,p,q = points
    u,w = p-v,q-v
    direction = u/np.linalg.norm(u)+w/np.linalg.norm(w)
    return v+.68*direction/np.linalg.norm(direction)


def geometry(data,color):
    v,p,q = data['points']
    shadow = Polygon(v,p,q,fill_color=BLACK,fill_opacity=.6,stroke_opacity=0).shift(RIGHT*.045+DOWN*.045)
    face = Polygon(v,p,q,fill_color=interpolate_color(ManimColor('#0E1721'),color,.22),
                   fill_opacity=1,stroke_opacity=0)
    edge1 = Line(v,p,color=color,stroke_width=4)
    edge2 = Line(v,q,color=color,stroke_width=4)
    cut = DashedLine(p,q,dash_length=.06,color=color,stroke_width=1.7,stroke_opacity=.8)
    arc = Arc(radius=.35,start_angle=data['start'],angle=data['angle'],arc_center=v,
              color=color,stroke_width=4.5)
    vertex = Dot(v,radius=.038,color=INK)
    return VGroup(shadow,face,edge1,edge2,cut,arc,vertex)


def piece(data,index):
    geom = geometry(data,COLORS[index])
    tag = Text(GLYPHS[index],font='Cambria Math',color=COLORS[index],font_size=31)
    tag.move_to(label_anchor(data['points']))
    return SimpleNamespace(geom=geom,tag=tag,face=geom[1],arc=geom[5],cut=geom[4])


def parallel_marks(y):
    marks = VGroup()
    for x in [-1.6,-1.40]:
        marks.add(VMobject(stroke_color=INK,stroke_width=2.2).set_points_as_corners(
            [[x-.09,y-.08,0],[x,y,0],[x-.09,y+.08,0]]))
    return marks


class OpeningScene(Scene):
    def at(self,t):
        delta=t-self.time
        if delta < -max(.04,1/config.frame_rate+.015):
            raise ValueError(f'Timeline overrun: {self.time:.3f} > {t:.3f}')
        if delta>.001:
            self.wait(delta)

    def caption(self,index):
        start, text = CUES[index]
        self.at(start)
        new=Text(text,font=FONT,font_size=26,color=INK)
        if new.width>12.6:
            new.scale_to_fit_width(12.6)
        new.move_to(NOTE_POS)
        self.play(Transform(self.note,new),run_time=.30)

    def follow(self,p):
        p.tag.add_updater(lambda mob:mob.move_to(label_anchor(p.geom[1].get_vertices())))

    def stop_follow(self,p):
        p.tag.update()
        p.tag.clear_updaters()

    def construct(self):
        self.camera.background_color='#070C13'
        data=triangle_corners(C)
        title=Text('三角形的三个角，合起来有多大？',font=FONT,font_size=33,color=INK)
        title.move_to([0,3.23,0])
        bar=RoundedRectangle(width=13.15,height=.76,corner_radius=.13,
                             fill_color='#111C29',fill_opacity=.94,
                             stroke_color='#203043',stroke_width=1).move_to(NOTE_POS)
        self.note=Text('先看三角形里的三个角。',font=FONT,font_size=26,color=INK).move_to(NOTE_POS)
        self.add(title,bar,self.note)

        triangle=Polygon(A,B,C,fill_color='#152638',fill_opacity=.62,
                         stroke_color=OUTLINE,stroke_width=3.6)
        vertex_names=VGroup(
            Text('A',font='Times New Roman',font_size=31,color=INK).move_to(A+DOWN*.40),
            Text('B',font='Times New Roman',font_size=31,color=INK).move_to(B+DOWN*.40),
            Text('C',font='Times New Roman',font_size=31,color=INK).move_to(C+UP*.43),
        )
        pieces=[piece(d,i) for i,d in enumerate(data)]
        for p in pieces:
            p.cut.set_stroke(opacity=0)
        self.play(Create(triangle),run_time=.55)
        self.caption(0)
        self.play(FadeIn(vertex_names),
                  FadeIn(VGroup(*[p.geom for p in pieces])),
                  FadeIn(VGroup(*[p.tag for p in pieces])),run_time=1.15)
        self.at(5.3)

        self.caption(1)
        for p in pieces:
            self.play(Indicate(p.arc,color=p.tag.get_color(),scale_factor=1.0),run_time=.9)
        self.play(*[p.cut.animate.set_stroke(opacity=.85) for p in pieces[:2]],run_time=.7)
        self.at(11.3)

        self.caption(2)
        top_line=Line([-5.65,C[1],0],[5.65,C[1],0],color='#8094A8',stroke_width=2.4)
        marks=VGroup(parallel_marks(C[1]),parallel_marks(A[1]))
        line_name=Text('ℓ ∥ AB',font='Cambria Math',font_size=27,color='#A7B8C8').move_to([4.55,2.01,0])
        self.play(Create(top_line),run_time=1.35)
        self.play(FadeIn(marks),FadeIn(line_name),run_time=.55)
        self.play(Indicate(marks,color=INK,scale_factor=1.0),run_time=1.1)
        self.at(16.3)

        # 红角纸片先作刚性半周旋转，再整体平移到C。
        self.caption(3)
        invariant=Text('转动、平移：角的大小不变',font=FONT,font_size=23,color='#A9BDCC').move_to([0,2.53,0])
        ghost_a=piece(data[0],0)
        self.play(FadeIn(VGroup(ghost_a.geom,ghost_a.tag).set_opacity(.27)),FadeIn(invariant),run_time=.35)
        self.follow(pieces[0])
        self.play(pieces[0].geom.animate.shift(LEFT*.10+DOWN*.08),run_time=.65)
        pivot=pieces[0].geom[1].get_vertices()[0].copy()
        self.play(Rotate(pieces[0].geom,angle=PI,about_point=pivot),run_time=2.2,rate_func=smooth)
        shift=C-pieces[0].geom[1].get_vertices()[0]
        self.play(pieces[0].geom.animate.shift(shift),run_time=2.2,rate_func=smooth)
        self.stop_follow(pieces[0])
        self.caption(4)
        self.play(Indicate(ghost_a.arc,color=CORAL,scale_factor=1.0),
                  Indicate(pieces[0].arc,color=CORAL,scale_factor=1.0),run_time=1.4)
        self.play(Indicate(marks,color=INK,scale_factor=1.0),run_time=.9)
        self.at(27.3)

        self.caption(5)
        ghost_b=piece(data[1],1)
        self.play(FadeIn(VGroup(ghost_b.geom,ghost_b.tag).set_opacity(.27)),run_time=.35)
        self.follow(pieces[1])
        self.play(pieces[1].geom.animate.shift(RIGHT*.10+DOWN*.08),run_time=.65)
        pivot=pieces[1].geom[1].get_vertices()[0].copy()
        self.play(Rotate(pieces[1].geom,angle=PI,about_point=pivot),run_time=2.2,rate_func=smooth)
        shift=C-pieces[1].geom[1].get_vertices()[0]
        self.play(pieces[1].geom.animate.shift(shift),run_time=2.2,rate_func=smooth)
        self.stop_follow(pieces[1])
        self.caption(6)
        self.play(Indicate(ghost_b.arc,color=ICE,scale_factor=1.0),
                  Indicate(pieces[1].arc,color=ICE,scale_factor=1.0),run_time=1.4)
        self.play(Indicate(marks,color=INK,scale_factor=1.0),run_time=.9)
        self.at(38.3)

        self.caption(7)
        outer_left=Line(C,[-5.65,C[1],0],color=AMBER,stroke_width=3.2)
        outer_right=Line(C,[5.65,C[1],0],color=AMBER,stroke_width=3.2)
        sweep=Arc(radius=1.36,start_angle=PI,angle=sum(d['angle'] for d in data),
                  arc_center=C,color=AMBER,stroke_width=2.4)
        self.play(Create(outer_left),Create(outer_right),FadeOut(invariant),run_time=1.4)
        self.play(Create(sweep),run_time=1.7)
        self.caption(8)
        formula=VGroup(*[Text(s,font='Cambria Math',font_size=40,color=INK)
                         for s in ['α','+','β','+','γ','= 180°']]).arrange(RIGHT,buff=.13)
        formula[0].set_color(CORAL)
        formula[2].set_color(ICE)
        formula[4].set_color(AMBER)
        formula[-1].set_color(AMBER)
        formula.move_to([0,-2.32,0])
        self.play(Write(formula),run_time=1.4)
        self.at(48.5)

        self.caption(9)
        shape_tag=Text('锐角三角形',font=FONT,font_size=23,color='#A9BDCC').move_to([-4.5,2.45,0])
        self.play(FadeIn(shape_tag),run_time=.35)
        # 将强调过的子对象重新归入完整场景，避免改变形状时留下旧轮廓。
        self.clear()
        self.add(triangle,top_line,marks,line_name,
                 ghost_a.geom,ghost_a.tag,ghost_b.geom,ghost_b.tag,
                 *[p.geom for p in pieces],*[p.tag for p in pieces],vertex_names,
                 outer_left,outer_right,sweep,formula,shape_tag,title,bar,self.note)
        top_x=ValueTracker(C[0])

        def update_shape(_mob,dt=0):
            top=np.array([top_x.get_value(),C[1],0.])
            current=triangle_corners(top)
            triangle.set_points_as_corners([A,B,top,A])
            vertex_names[2].move_to(top+UP*.43)
            for i,p in enumerate(pieces):
                new=geometry(current[i],COLORS[i])
                if i<2:
                    new.rotate(PI,about_point=current[i]['vertex']).shift(top-current[i]['vertex'])
                p.geom.become(new)
                p.tag.move_to(label_anchor(p.geom[1].get_vertices()))
            for i,ghost in enumerate([ghost_a,ghost_b]):
                ghost.geom.become(geometry(current[i],COLORS[i]).set_opacity(.27))
                ghost.tag.move_to(label_anchor(current[i]['points'])).set_opacity(.27)
            outer_left.put_start_and_end_on(top,[-5.65,C[1],0])
            outer_right.put_start_and_end_on(top,[5.65,C[1],0])
            sweep.become(Arc(radius=1.36,start_angle=PI,angle=sum(d['angle'] for d in current),
                             arc_center=top,color=AMBER,stroke_width=2.4))

        driver=VMobject()
        driver.add_updater(update_shape)
        self.add(driver)
        self.play(top_x.animate.set_value(B[0]),run_time=1.9,rate_func=smooth)
        driver.clear_updaters()
        update_shape(driver)
        shape_tag.become(Text('直角三角形',font=FONT,font_size=23,color='#A9BDCC').move_to([-4.5,2.45,0]))
        self.at(52)
        driver.add_updater(update_shape)
        self.play(top_x.animate.set_value(3.6),run_time=1.9,rate_func=smooth)
        driver.clear_updaters()
        update_shape(driver)
        shape_tag.become(Text('钝角三角形',font=FONT,font_size=23,color='#A9BDCC').move_to([-4.5,2.45,0]))
        self.at(57.5)
        self.play(FadeOut(Group(*self.mobjects)),run_time=.5)
