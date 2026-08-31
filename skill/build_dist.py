"""build_dist.py — 生成单文件版协作手册（纯对话 AI 工具用）

把 SKILL.md 正文 + rules/*.md 合并为 dist/manim-teaching-prompt.md，
供无法安装技能目录的工具（ChatGPT / Claude.ai / Kimi 网页版 / DeepSeek /
豆包等）粘贴进自定义指令、项目知识或常用语。

用法：python build_dist.py   （在 skill/ 目录下运行）
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "manim-teaching"
OUT = Path(__file__).resolve().parent / "dist" / "manim-teaching-prompt.md"

RULE_ORDER = ["version-lock.md", "teaching-style.md",
              "math-accuracy.md", "pitfalls.md"]

skill_raw = (ROOT / "SKILL.md").read_text(encoding="utf-8")
body = re.sub(r"^---\r?\n.*?\r?\n---\r?\n?", "", skill_raw, flags=re.S)

parts = [
    "# Manim 教学动画协作手册（单文件版）",
    "",
    "> 本文件由 build_dist.py 自动生成：SKILL.md + rules/ 四份规则的合并版。",
    "> 粘贴进你的 AI 工具的自定义指令 / 项目知识 / 常用语即可生效。",
    "> 内容更新时重新运行 build_dist.py，不要手改本文件。",
    "",
    body.strip(),
]
for name in RULE_ORDER:
    parts.append("\n---\n")
    parts.append((ROOT / "rules" / name).read_text(encoding="utf-8").strip())

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"已生成 {OUT}（{OUT.stat().st_size} 字节）")
