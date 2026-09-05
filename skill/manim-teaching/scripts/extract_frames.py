"""extract_frames.py — 从渲染成片抽帧供目检（重叠 / 出画 / 字形缺失）

用法：python extract_frames.py <video.mp4> <秒1> [秒2 ...] [-o 输出目录]
输出：输出目录（默认视频同目录 frames/）下 frame_<秒>s.png。
依赖：pip install av（PyAV）；按时间顺序解码取帧，兼容一切编码。

AI 用法：渲染完成后抽关键节拍帧（读数翻牌点、结案定格点），
逐张目检：文字是否出画、对象是否重叠、特殊符号是否豆腐块。
"""

import sys
from pathlib import Path


def grab(video, times, outdir):
    import av
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    times = sorted(times)
    idx = 0
    container = av.open(str(video))
    for frame in container.decode(video=0):
        while idx < len(times) and frame.time >= times[idx]:
            out = outdir / f"frame_{times[idx]:g}s.png"
            frame.to_image().save(out)
            print(f"saved {out}")
            idx += 1
        if idx >= len(times):
            break
    container.close()
    if idx < len(times):
        print(f"警告：{len(times) - idx} 个时间点超出视频时长，未抽取")
        return 1
    return 0


def parse_args(argv):
    """拆分位置参数与 -o，避免把输出目录误当成抽帧秒数。"""
    args = list(argv)
    outdir = None
    if "-o" in args:
        i = args.index("-o")
        if i + 1 >= len(args):
            raise ValueError("-o 后必须提供输出目录")
        outdir = Path(args[i + 1])
        del args[i:i + 2]
    if len(args) < 2:
        raise ValueError("至少需要视频路径和一个抽帧秒数")
    video = Path(args[0])
    times = [float(a) for a in args[1:]]
    if outdir is None:
        outdir = video.parent / "frames"
    return video, times, outdir


def main():
    try:
        video, times, outdir = parse_args(sys.argv[1:])
    except (ValueError, IndexError) as exc:
        print("用法：python extract_frames.py <video.mp4> <秒1> [秒2 ...] [-o 目录]")
        print(f"参数错误：{exc}")
        return 2
    return grab(video, times, outdir)


if __name__ == "__main__":
    sys.exit(main())
