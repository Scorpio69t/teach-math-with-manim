# pitfalls.md — Manim 教学动画避坑清单

> 本文件是 AI Skill 的"事故档案"，每条都来自一次真实翻车。
> 生成或审查 Manim 代码时逐条对照；新事故随时补充（格式：错误写法 → 正确写法 → 原因）。
> 对应图书《Manim，让数学看得见》第 19 章。

## A. 版本与 API（GL/CE 混用类）

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| A1 | `from manimlib import *` | `from manim import *` | manimlib 是 3b1b 原版（GL），与社区版（CE）互不兼容 |
| A2 | `self.play(ShowCreation(m))` | `self.play(Create(m))` | ShowCreation 是 GL 旧接口，CE 已废弃 |
| A3 | `TextMobject("标题")` / `TexMobject` | `Text("标题")` / `MathTex` | 前者是 GL 名称，CE 已改名 |
| A4 | `manim file.py Scene` 无参数直接渲 | 显式指定画质：`-ql` 验证 / `-qh` 出片 | 无参数默认行为随版本变化，且容易渲出不需要的高清长视频 |
| A5 | 2D 运镜场景里 `self.camera.add_fixed_in_frame_mobjects(m)` | 用 updater 钉屏：`pin_to_screen(self.camera, m, "UL")`（每帧按取景框中心与缩放重算位置和尺寸，见 ch06_camera/hud_demo.py） | 该方法只存在于 `ThreeDCamera`（0.21 源码核实），`MovingCamera` 调用报 AttributeError（2026-08-26 第 6 章初稿真机渲染抓获，凭记忆写 API 的代价） |
| A6 | `TracedPath(tip_dot)` 传 mobject | `TracedPath(tip.get_center)` 传 callable，mobject 另用 updater 驱动 | 当前 CE 版本首参是 traced_point_func，传对象报 `'Dot' object is not callable`（2026-08-28 第15章 FourierStar 事故） |
| A7 | `DashedVMobject(circle, dash_length=0.06)` | `DashedVMobject(circle, num_dashes=30)` | 当前版本无 dash_length 参数，报 `unexpected keyword argument`（2026-08-28 同场景事故） |

## B. 动画设计类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| B1 | 交换用两个 `animate.move_to` 直线对穿 | `CyclicReplace(a, b)` 弧线互换 | 直线对穿互相遮挡；弧线轨迹本身在解释"交换" |
| B2 | 一个 `play` 里塞 5 个以上动画 | 按教学节拍拆成多个 `play` | 动画的每个节拍要等得起一句讲解 |
| B3 | `VGroup` 元素交换后仍用旧下标引用 | 交换后立即同步 VGroup 内的引用顺序 | 视图与数据不同步，后续比较结果全错 |
| B4 | 同位置公式替换用交叉淡入淡出：`old.animate.set_opacity(0)` 与 `new.animate.set_opacity(1)` 同帧播放 | 顺序替换：`play(old.animate.set_opacity(0))` 完成后再 `play(new.animate.set_opacity(1))`（或用 `TransformMatchingTex`） | 过渡期两个半透明公式堆叠，糊成一团无法阅读（2026-08-26 复刻 3B1B 导数几何系列抽帧抓获） |
| B5 | 描边框用 `box.animate.set_opacity(1)` 显现 | `box.set_fill(opacity=0)` 锁死填充，只动 `set_stroke(opacity=...)`，或直接用 `Create(box)` | `set_opacity` 把填充一起拉满，实心色块盖住框内公式（同日同批抓获，SurroundingRectangle 重灾区） |
| B6 | 密集区标签手写偏移坐标（如 `Ppos + UP*0.48 + LEFT*0.14`） | 用几何关系定位：角平分线方向 `normalize(u1+u2)`、`next_to(参照物, 方向, buff≥0.2)` | 手写偏移换一个参数就撞车；几何定位随图形自适应（同日正弦场景 P 点三标签相撞事故） |
| B7 | 多幕场景前一幕演员留在原地不退场 | 转场时处理旧演员：`FadeOut` 退场，或 `scale(0.5).move_to(顶部)` 缩小置顶留作对照 | 新幕道具直接叠在旧演员身上，画面撞车（2026-08-27 第7章 TransformFamily 第三幕星圆卡片三叠事故） |
| B8 | 会动/会转的元素按静止时占地划位置（如自转文字放右下角） | 按其活动范围划地盘：旋转体会扫过比静止 footprint 大一圈的区域，避开注释条锚点（DOWN*3.2） | 旋转中文字扫进注释条区域，两段文字重叠不可读（同日 UpdaterDemo 抽帧抓获） |
| B9 | 三维场景里对钉屏文字（fixed_in_frame）用 Transform 更新 | 钉屏文字更新用“新建 → 卸钉 → `remove` → 再钉”瞬切：先创建新对象，再 `remove_fixed_in_frame_mobjects(old)`、`self.remove(old)`（卸钉只是解绑，对象还躺在三维舞台上），最后 `add_fixed_in_frame_mobjects(new)` | Transform 会把钉屏对象拖进三维空间躺平；只卸钉不 remove，旧注释以三维身份留在舞台上越积越多（2026-08-27 第8章三维四场景集体事故） |
| B10 | 三维钉屏数值面板用 `DecimalNumber.set_value`、`Text.become()`，或从 updater 内执行四步换对象 | 数值用 `Text` 组成完整面板；把连续行程拆成短的线性 `play`，只在相邻 `play` 之间按 B9 的四步整体替换面板 | `set_value`/`become` 会让新字模脱离钉屏；即使执行四步，若发生在 updater 内，Cairo 已为当前 `play` 缓存的运动对象仍可能渲染被卸钉的旧字，形成斜挂残影（2026-08-28 ParaboloidSlices 全程抽帧确认） |
| B11 | 滑参动画让参数连续路过退化值（如 a 从 1 滑到 −0.5 必经 a≈0），绘图区间按当前参数自适应（如 `√(5/|a|)`） | 对参与定义域计算的参数钳位：`a_safe = max(abs(a), 0.25)`，区间按钳位后的值算 | a→0 时 `√(5/|a|)` 爆炸，plot 区间撑到天文数字，点阵内存爆掉直接 MemoryError（申请 25.8 GiB），渲染崩在半路（2026-08-27 第9章 TransformStudio 事故） |
| B12 | 数值面板"标签 next_to 锚点 + 数字右对齐同一锚点" | 两列钉缘：标签右缘钉死（`move_to((x1,y), aligned_edge=RIGHT)`）、数字左缘钉死（`move_to((x2,y), aligned_edge=LEFT)`），数字位数变化只向右生长 | 两个对象钉同一锚点必叠字；标签 next_to 数字则数字变宽时把标签顶飞（2026-08-27 第10章 CircleTheorems/VectorProof 面板叠字事故） |
| B13 | "指针已就位"循环写 `range(2, N+2)` | 先数清楚剩余次数：指针已在 z1 上，到 z1^N 只需 `range(2, N+1)`（N−1 次） | 多转一次越过目标落点，计数牌翻出 z1^6，扫圈论证当场穿帮（2026-08-28 第15章 UnitRoots 抽帧抓获） |
| B14 | 坐标网/坐标轴背景上的实体图形用半透明填充（`fill_opacity<1`） | 网格背景上的"演员"一律不透明填充 `fill_opacity=1.0`；要轻盈感去降描边透明度，别动填充 | 轴线透过填充穿身而过，像被坐标轴戳穿，印刷图上尤其刺眼（2026-08-31 第4章 PositioningDemo 图4-2 作者目检抓获）；同场附 B7 又一例：只服务第一幕的坐标标签悬在二三幕，转幕时 `FadeOut` 谢幕 |
| B15 | 把 `TransformMatchingTex` 的中途帧直接用作静态插图 | 动画保留连续变形，书中静态图改用变形前、变形后两张独立帧对照 | 淡出、淡入和匹配移动的零件会在中途同时出现，单帧容易重叠成乱码；第 5 章图 5-7 真机抽帧复现（2026-09-05） |
| B16 | 多站世界块按两个屏幕宽排开，直接抽取平移中途帧 | 按中途取景框计算站间距，让相邻文字在静态帧中完整同框 | 站间距过大时中途帧两端文字各被裁掉一半；第 6 章图 6-3 真机抽帧复现（2026-09-05） |
| B17 | 第一站字幕已写好，却让镜头从默认中心位置动画移向第一站 | 先把 `camera.frame` 直接布到第一站并停留，再从第二站开始巡游 | 开场字幕与画面对象错位，镜头先倒退再前进；第 6 章 `HudDemo` 真机抽帧复现（2026-09-05） |
| B18 | 多幕对照场景只保留最终图形，不标明各图形所属操作 | 在最终定格帧为保留对象补上简短操作标签 | 视频里靠时间顺序能分辨，印成单幅静态图后语义丢失；第 7 章图 7-2 抽帧复现（2026-09-05） |
| B19 | 进度条直接调用 `stretch_to_fit_width`，使用默认中心作为伸缩基准 | 用 `about_edge=LEFT` 固定起点，并增加不动的满量程轨道 | 默认行为会让色块同时向两侧膨胀，读者难以把它识别为从零端增长的进度；第 7 章图 7-3 抽帧复现（2026-09-05） |
| B20 | 三维主体按画面中心构图，却没有给左上钉屏长标题预留安全区 | 用最拥挤的关键状态检查屏幕投影；必要时缩短标题或收敛字号，确保标题边界与主体留有清晰间隔 | 三维对象的屏幕投影可能侵入固定界面层；第 8 章图 8-5 在 `h=3.20` 静帧中复现碗沿逼近 32 号长标题（2026-09-05） |
| B21 | 误以为 `Axes.plot` 会自动裁剪到坐标轴框 | 按当前函数的纵向安全边界反算 `x_range`，并为标题、注释条额外留净空 | 第 9 章图 9-2、9-4、9-5 复核时发现曲线或割线越过坐标轴，侵入标题/注释区；`Axes.plot` 本身不做视窗裁剪（2026-09-05） |

## C. 文字与动态文本类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| C1 | 中文直接 `Text("你好")` 不指定字体 | `Text("你好", font="Microsoft YaHei")`（macOS: PingFang SC / Linux: Noto Sans CJK SC） | 默认字体不含中文，渲染成方块 |
| C2 | **动态字幕用空文本初始化再定位**：`Text(" ")` → `to_edge(DOWN)` | 用真实首句初始化 + 固定锚点：`CAPTION_POS = DOWN * 3.2`，更新时 `new.move_to(CAPTION_POS)` | 纯空格被渲染成零宽高对象，定位静默失效，文字停在画面中心与图形重叠（2026-08-20 冒泡演示视频实车事故） |
| C3 | 更新文字：`remove(t); t2 = Text(...); add(t2)` | `t.become(Text(...))` 原地变形 | 先删后加造成闪烁；become 保持引用不变 |
| C4 | 字幕/标签用 `MathTex` 渲染纯文字 | 纯文字一律用 `Text`（斜体用 `slant=ITALIC`） | MathTex 依赖 LaTeX 环境，无端增加安装门槛 |
| C5 | 上屏特殊符号想当然（如 `⟹`、`⟺`） | 非常用符号先小样试屏；安全符号表：→、×、÷、²、½、°、✓；表达"推出"优先用汉字"即" | 字体缺字形时 Manim 静默渲染成豆腐块，不报错不警告（2026-08-27 第10章 PythagorasProof 横幅 ⟹ 豆腐块事故） |
| C6 | **三维钉屏文字用 become() 换词** | ThreeDScene 里 become 的子对象会脱落钉屏；必须四步：建新对象 → `remove_fixed_in_frame_mobjects(旧)` → `remove(旧)` → `add_fixed_in_frame_mobjects(新)` | become 替换的子对象不在相机 fixed 名单里，文字躺到 3D 地面成透视残影（2026-08-28 第13章四脚本集体事故）；C3 的 become 铁律仅限二维 |
| C7 | 只 `remove_fixed_in_frame_mobjects` 不 `remove` | 摘钉后必须再 `remove()` 摘除场景 | remove_fixed 只摘钉不摘场景，旧文字作为普通 3D 物体残留在地面（2026-08-28 同事故第二层残影） |
| C8 | 三维曲面用默认分辨率批量造（如 12 个 Cylinder） | 显式降采样：`Cylinder(resolution=(2,16))` 等；提示词里永远写明 resolution | 默认网格极密，12 枚硬币默认 11 分钟 vs 降采样 23 秒（2026-08-28 第13章 ZugengPrinciple） |
| C9 | 把 become 包进 play：`self.play(note.become(Text(...)))` | become 不进 play——封装成 `set_note` 助手直接瞬时换词（二维场景惯例）；要过渡动画才用 `note.animate.become(...)` | `become` 返回 mobject 本身而非 Animation，传进 play 报 `Unexpected argument VMobjectFromSVGPath passed to Scene.play()`（2026-08-31 附录 B 三场景初稿事故，render_check 抓获） |
| C10 | `MathTex(r"\text{勾股定理}")` 里塞中文 | 中文一律用 `Text`（字体见 C1），公式里的中文标注用 `MathTex` 与 `Text` 分列组装，或 LaTeX 模板换 ctex | 默认 LaTeX 模板不含中文字形，报 Unicode error 或渲出豆腐块；纯文字本来就该用 Text（C4 的推论） |
| C11 | 直接把 `index_labels(mobject)` 的默认结果当正式插图 | 用 `color=RED` 指定编号颜色，再以整个公式为纵向参照、对应零件中心为横向参照，把编号排到公式下方 | 默认编号是白色并位于各子对象中心，会与公式笔画重叠；第 5 章图 5-5 真机渲染复现（2026-09-05） |
| C12 | 为了让多行公式等号对齐，只移动每行的等号子对象 | 比较锚点等号与当前等号的横坐标差，再用 `row.shift(shift_x * RIGHT)` 平移整行 | 单独移动等号会破坏 `MathTex` 内部间距，使等号与左右公式重叠；第 5 章图 5-6 真机渲染复现（2026-09-05） |

## D. 工程习惯类

| # | 错误写法 | 正确写法 | 原因 |
|---|---|---|---|
| D1 | 一次性改多处再渲染 | 每次只改一处，`-ql` 快速验证 | 改三处出错时无法定位是哪一处 |
| D2 | 长场景整段渲染调试 | `-n 0,3` 分段渲染 / 先 `-s` 看末帧 | 重复等待与问题无关的片段；节省幅度取决于场景 |
| D3 | 变量名 `c1`、`x2`、`arr` | 教学语义命名：`compare_color`、`sorted_bar` | 代码即教材，命名即讲解 |
| D4 | 验证/预检脚本把临时渲染目录建到系统 temp（`tempfile.TemporaryDirectory()` 默认系统盘） | 临时目录建在工作区内：`tempfile.TemporaryDirectory(prefix=".manim_check_", dir=".")`，用完即删 | 一次本机事故中，工作区在 E 盘、系统 temp 在 C 盘时，MiKTeX 的 dvisvgm 静默返回 −4，manim 层只报 DVI 转 SVG 失败；这是该环境的复现记录，不外推为所有 Windows 机器的规律（2026-09-02 render_check 自身翻车抓获） |
| D5 | 用简单过滤删除所有以连字符开头的参数，再把剩余项全当作位置参数 | 显式识别 `-o`，连同其后一个值从位置参数中移除，再解析视频路径与秒数 | 输出目录会混进秒数列表并触发 `float(path)` 的 `ValueError`；第 7 章正式抽帧按文档调用 `extract_frames.py -o` 时复现（2026-09-05） |

---

**新增事故记录格式**（追加到对应分类，编号顺延）：

```
| Xn | 错误写法（一句话） | 正确写法（一句话） | 原因（一句话 + 事故日期） |
```
