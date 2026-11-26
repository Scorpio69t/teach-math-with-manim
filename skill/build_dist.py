"""build_dist.py — 生成单文件版协作手册（纯对话 AI 工具用）

把 SKILL.md 正文 + rules/*.md 合并为 dist/manim-teaching-prompt.md，
供无法安装技能目录的工具（ChatGPT / Claude.ai / Kimi 网页版 / DeepSeek /
豆包等）粘贴进自定义指令、项目知识或常用语。

用法：python build_dist.py           （生成 dist/manim-teaching-prompt.md）
      python build_dist.py --check   （检查 dist/ 是否与源码同步，CI 用）
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "manim-teaching"
OUT = Path(__file__).resolve().parent / "dist" / "manim-teaching-prompt.md"

RULE_ORDER = [
    "version-lock.md",
    "teaching-style.md",
    "math-accuracy.md",
    "pitfalls.md",
    "qa-checklist.md",
]


def build_content() -> str:
    skill_raw = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    body = re.sub(r"^---\r?\n.*?\r?\n---\r?\n?", "", skill_raw, flags=re.S)

    parts = [
        "# Manim 教学动画协作手册（单文件版）",
        "",
        "> 本文件由 build_dist.py 自动生成：SKILL.md + rules/ 五份规则的合并版。",
        "> 粘贴进你的 AI 工具的自定义指令 / 项目知识 / 常用语即可生效。",
        "> 内容更新时重新运行 build_dist.py，不要手改本文件。",
        "",
        body.strip(),
    ]
    for name in RULE_ORDER:
        parts.append("\n---\n")
        parts.append((ROOT / "rules" / name).read_text(encoding="utf-8").strip())
    return "\n".join(parts) + "\n"


def main() -> int:
    expected = build_content()
    if "--check" in sys.argv[1:]:
        if not OUT.is_file():
            print(f"OUT_OF_SYNC: 缺少 {OUT}")
            return 1
        actual = OUT.read_text(encoding="utf-8")
        if actual != expected:
            print(f"OUT_OF_SYNC: {OUT} 与源码不一致，请运行 python skill/build_dist.py")
            return 1
        print(f"IN_SYNC: {OUT}")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(expected, encoding="utf-8")
    print(f"已生成 {OUT}（{OUT.stat().st_size} 字节）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
