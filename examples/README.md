# examples/ — 书中案例源码

按章节组织，每章一个子目录，命名 `chNN_主题/`（附录为 `appB_linalg/`，番外演示为 `bonus_sorting/`）。所有场景类均可直接渲染：

```bash
manim -pql examples/bonus_sorting/bubble_sort.py BubbleSortScene
```

代码对应《Manim，让数学看得见》书中各章“完整代码”小节，全部脚本已内置跨平台中文字体选择（Windows `Microsoft YaHei` / macOS `PingFang SC` / Linux `Noto Sans CJK SC`），无需手动改字体即可直接渲染。

> **收录纪律**：本目录只收正文“完整代码”小节的教学案例。图书生产工具（拼图脚本、取帧专用渲染版、mathtext 预渲染素材等）不进本仓。

## 案例总索引（共 65 个文件）

标注“需 LaTeX = 是”的案例使用了 `MathTex`，渲染前需安装 TeX Live / MiKTeX / MacTeX；其余案例仅用 `Text`，免 LaTeX 即可渲染。

| 章节 | 脚本路径 | 场景类 | 需 LaTeX |
|---|---|---|---|
| 第 1 章 · 为什么用 Manim | `ch01_why_manim/opening.py` | `OpeningScene` | 否 |
| 第 3 章 · 核心概念 | `ch03_core_concepts/rate_func_demo.py` | `RateFuncDemo` | 否 |
| 第 3 章 · 核心概念 | `ch03_core_concepts/transform_story.py` | `TransformStoryScene` | 否 |
| 第 4 章 · 画面布局 | `ch04_layout/position_demo.py` | `PositioningDemo` | 否 |
| 第 4 章 · 画面布局 | `ch04_layout/standard_frame.py` | `StandardFrameScene` | 是 |
| 第 5 章 · 公式渲染 | `ch05_formula/aligned_group.py` | `AlignedEquations`, `IndexLabelsDemo` | 是 |
| 第 5 章 · 公式渲染 | `ch05_formula/color_reading.py` | `GuidedReading` | 是 |
| 第 5 章 · 公式渲染 | `ch05_formula/matching_transform.py` | `MoveTermTransform` | 是 |
| 第 5 章 · 公式渲染 | `ch05_formula/quadratic_derivation.py` | `QuadraticDerivation` | 是 |
| 第 6 章 · 镜头语言 | `ch06_camera/camera_tour.py` | `CameraTour` | 否 |
| 第 6 章 · 镜头语言 | `ch06_camera/hud_demo.py` | `HudDemo` | 否 |
| 第 6 章 · 镜头语言 | `ch06_camera/lesson_tour.py` | `LessonTour` | 否 |
| 第 7 章 · 变换与数值驱动 | `ch07_transform/parabola_slider.py` | `ParabolaSlider` | 是 |
| 第 7 章 · 变换与数值驱动 | `ch07_transform/tracker_panel.py` | `TrackerPanel` | 否 |
| 第 7 章 · 变换与数值驱动 | `ch07_transform/transform_family.py` | `TransformFamily` | 否 |
| 第 7 章 · 变换与数值驱动 | `ch07_transform/updater_demo.py` | `UpdaterDemo` | 否 |
| 第 8 章 · 3D 场景 | `ch08_3d/camera_orbit.py` | `CameraOrbit` | 否 |
| 第 8 章 · 3D 场景 | `ch08_3d/paraboloid_slices.py` | `ParaboloidSlices` | 是 |
| 第 8 章 · 3D 场景 | `ch08_3d/surface_demo.py` | `SurfaceDemo` | 是 |
| 第 8 章 · 3D 场景 | `ch08_3d/three_d_basics.py` | `ThreeDBasics` | 否 |
| 第 9 章 · 函数图像 | `ch09_functions/growth_race.py` | `GrowthRace` | 否 |
| 第 9 章 · 函数图像 | `ch09_functions/secant_tangent.py` | `SecantToTangent` | 是 |
| 第 9 章 · 函数图像 | `ch09_functions/slope_opening.py` | `SlopeAndOpening` | 是 |
| 第 9 章 · 函数图像 | `ch09_functions/transform_studio.py` | `TransformStudio` | 是 |
| 第 10 章 · 平面几何 | `ch10_geometry/analytic_proof.py` | `AnalyticProof` | 是 |
| 第 10 章 · 平面几何 | `ch10_geometry/circle_theorems.py` | `CircleTheorems` | 是 |
| 第 10 章 · 平面几何 | `ch10_geometry/pythagoras_proof.py` | `PythagorasProof` | 是 |
| 第 10 章 · 平面几何 | `ch10_geometry/vector_proof.py` | `VectorProof` | 是 |
| 第 11 章 · 三角函数 | `ch11_trig/circle_to_wave.py` | `CircleToWave` | 否 |
| 第 11 章 · 三角函数 | `ch11_trig/fourier_stack.py` | `FourierStack` | 否 |
| 第 11 章 · 三角函数 | `ch11_trig/slope_to_ratio.py` | `SlopeToRatio` | 否 |
| 第 11 章 · 三角函数 | `ch11_trig/two_path_transform.py` | `TwoPathTransform` | 是 |
| 第 12 章 · 数列与解析几何 | `ch12_seq_geo/arith_vs_geom.py` | `ArithVsGeom` | 是 |
| 第 12 章 · 数列与解析几何 | `ch12_seq_geo/ellipse_string.py` | `EllipseString` | 否 |
| 第 12 章 · 数列与解析几何 | `ch12_seq_geo/figurate_numbers.py` | `FigurateNumbers` | 否 |
| 第 12 章 · 数列与解析几何 | `ch12_seq_geo/series_fill.py` | `SeriesFill` | 否 |
| 第 13 章 · 立体几何 | `ch13_solid/cube_net.py` | `CubeNet` | 否 |
| 第 13 章 · 立体几何 | `ch13_solid/line_plane_perp.py` | `LinePlanePerp` | 否 |
| 第 13 章 · 立体几何 | `ch13_solid/space_vector.py` | `SpaceVector` | 否 |
| 第 13 章 · 立体几何 | `ch13_solid/zugeng_principle.py` | `ZugengPrinciple` | 否 |
| 第 14 章 · 概率统计 | `ch14_prob/coin_tree.py` | `CoinTree` | 否 |
| 第 14 章 · 概率统计 | `ch14_prob/galton_board.py` | `GaltonBoard` | 否 |
| 第 14 章 · 概率统计 | `ch14_prob/law_large_numbers.py` | `LawOfLargeNumbers` | 否 |
| 第 14 章 · 概率统计 | `ch14_prob/least_squares.py` | `LeastSquares` | 否 |
| 第 15 章 · 复数与欧拉公式 | `ch15_complex/euler_wrap.py` | `EulerWrap` | 否 |
| 第 15 章 · 复数与欧拉公式 | `ch15_complex/fourier_star.py` | `FourierStar` | 是 |
| 第 15 章 · 复数与欧拉公式 | `ch15_complex/i_rotation.py` | `PowerOfI` | 是 |
| 第 15 章 · 复数与欧拉公式 | `ch15_complex/spiral_multiply.py` | `ComplexSpiral` | 否 |
| 第 15 章 · 复数与欧拉公式 | `ch15_complex/unit_roots.py` | `UnitRoots` | 否 |
| 第 16 章 · 微积分直观 | `ch16_calculus/area_function.py` | `AreaFunction` | 是 |
| 第 16 章 · 微积分直观 | `ch16_calculus/derivative_sweep.py` | `DerivativeSweep` | 是 |
| 第 16 章 · 微积分直观 | `ch16_calculus/instant_velocity.py` | `InstantVelocity` | 否 |
| 第 16 章 · 微积分直观 | `ch16_calculus/riemann_refine.py` | `RiemannRefine` | 是 |
| 第 17 章 · 不等式与最值 | `ch17_inequality/amgm_semicircle.py` | `AmGmSemicircle` | 是 |
| 第 17 章 · 不等式与最值 | `ch17_inequality/cauchy_vectors.py` | `CauchyVectors` | 否 |
| 第 17 章 · 不等式与最值 | `ch17_inequality/linear_programming.py` | `LinearProgramming` | 否 |
| 第 17 章 · 不等式与最值 | `ch17_inequality/number_line_ops.py` | `NumberLineOps` | 否 |
| 第 18 章 · 数学归纳法与证明之美 | `ch18_proof/circle_regions.py` | `CircleRegions` | 是 |
| 第 18 章 · 数学归纳法与证明之美 | `ch18_proof/domino_induction.py` | `DominoInduction` | 是 |
| 第 18 章 · 数学归纳法与证明之美 | `ch18_proof/pigeonhole.py` | `Pigeonhole` | 是 |
| 第 18 章 · 数学归纳法与证明之美 | `ch18_proof/sqrt2_descent.py` | `Sqrt2Descent` | 是 |
| 附录 B · 线性代数 | `appB_linalg/det_area.py` | `DetAreaScene` | 否 |
| 附录 B · 线性代数 | `appB_linalg/matrix_transform.py` | `MatrixTransformScene` | 否 |
| 附录 B · 线性代数 | `appB_linalg/vector_add.py` | `VectorAddScene` | 否 |
| 番外示例 · 冒泡排序（Skill 演示） | `bonus_sorting/bubble_sort.py` | `BubbleSortScene` | 否 |
