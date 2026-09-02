"""api_probe.py — 动笔前探测 API 是否真实存在（对抗 API 幻觉，跨平台）

用法：
    python api_probe.py Circle Square.set_fill NumberPlane DashedVMobject ...

支持点号链路（从 manim 顶层命名空间逐级取属性）。
每个名字输出：存在与否、类型、签名（能取到时）。
退出码：全部存在 0；任一缺失 1——AI 自修复流程据此决定是否回表白名单。
"""

import inspect
import sys


def probe(name):
    import manim

    obj = manim
    for part in name.split("."):
        if not hasattr(obj, part):
            return None
        obj = getattr(obj, part)
    return obj


def describe(obj):
    kind = type(obj).__name__
    if inspect.isclass(obj):
        kind = f"class（模块 {obj.__module__}）"
    elif callable(obj):
        kind = "callable"
    try:
        sig = str(inspect.signature(obj))
        if len(sig) > 160:
            sig = sig[:157] + "..."
    except (TypeError, ValueError):
        sig = "(签名不可内省，查官方文档)"
    return kind, sig


def main():
    if len(sys.argv) < 2:
        print("用法：python api_probe.py <名字> [<名字> ...]  例：python api_probe.py CyclicReplace Text.become")
        return 2
    missing = 0
    for name in sys.argv[1:]:
        obj = probe(name)
        if obj is None:
            print(f"MISSING  {name}  —— 当前版本不存在，回 rules/version-lock.md 白名单找替代")
            missing += 1
        else:
            kind, sig = describe(obj)
            print(f"OK       {name}  [{kind}]  {sig}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
