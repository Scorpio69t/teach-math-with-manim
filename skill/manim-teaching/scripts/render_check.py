"""render_check.py — AI 生成 Manim 代码后的强制渲染验证（跨平台）

用法：python render_check.py <file.py> <SceneName>
退出码 0 = RENDER_OK；非 0 = RENDER_FAILED（AI 自修复闭环据此判断）。
验证用最低画质 -ql（480p），速度是 1080p 的 4~6 倍；通过后再用 -pqh 出片。
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("用法：python render_check.py <file.py> <SceneName>")
        return 2
    file, scene = sys.argv[1], sys.argv[2]
    if not Path(file).is_file():
        print(f"RENDER_FAILED: 文件不存在 {file}")
        return 2

    with tempfile.TemporaryDirectory(prefix="manim_check_") as media:
        cmd = [sys.executable, "-m", "manim", "-ql", "--disable_caching",
               "--media_dir", media, file, scene]
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace",
                              timeout=600)
        log = (proc.stdout or "") + "\n" + (proc.stderr or "")

    # manim 的报错走 stderr；渲染成功标志是 "Rendered" 或文件产物
    failed = (proc.returncode != 0
              or re.search(r"Traceback \(most recent call last\)", log))
    if failed:
        tail = "\n".join(log.strip().splitlines()[-25:])
        print("RENDER_FAILED\n---- 报错尾部 ----\n" + tail)
        return 1
    print("RENDER_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
