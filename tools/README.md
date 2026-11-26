# tools/ — 辅助脚本

跨平台验证与辅助脚本已整合至 Skill 内置目录 `skill/manim-teaching/scripts/`，可直接独立运行（详见书中第 19 章）：

- `skill/manim-teaching/scripts/render_check.py` — 低画质（`-ql`）渲染验证脚本，自动检测报错与字体回退告警；
- `skill/manim-teaching/scripts/extract_frames.py` — 从渲染成片按时间点抽帧，供目检重叠、出画与缺字形；
- `skill/manim-teaching/scripts/api_probe.py` — 探测当前 ManimCE 环境中某个 API 是否真实存在及其签名。

后续批量导出、章节截图整理等仓库级脚本将放于本目录。
