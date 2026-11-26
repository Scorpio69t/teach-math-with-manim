#!/usr/bin/env bash
# install.sh — 把 manim-teaching 技能安装到本机检测到的 AI Agent skills 目录
# 用法：bash install.sh            # 自动探测常见 Agent 的 skills 目录并安装
#       bash install.sh <目录>     # 安装到指定目录
set -e

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/manim-teaching" && pwd)"

install_to() {
  local dst="$1/manim-teaching"
  mkdir -p "$dst"
  local dst_real
  dst_real="$(cd "$dst" && pwd)"
  if [ "$dst_real" = "$SRC" ]; then
    echo "目标目录与源目录相同，跳过：$dst_real" >&2
    return 1
  fi
  (cd "$SRC" && tar cf - --exclude='__pycache__' --exclude='*.pyc' .) | tar xf - -C "$dst"
}

if [ -n "${1:-}" ]; then
  install_to "$1"
  echo "已安装到 $1/manim-teaching"
  exit 0
fi

# 常见 Agent 的 skills 目录（截至 2026-08；路径随各产品版本变动，
# 失效时以各产品官方文档为准，或用「bash install.sh <目录>」手动指定）
CANDIDATES=(
  "$HOME/.claude/skills"          # Claude Code
  "$HOME/.agents/skills"          # DeepSeek Harness / Zed 等共享目录
  "$HOME/.config/agents/skills"   # Kimi Code
  "$HOME/.codex/skills"           # Codex CLI
  "$HOME/.copilot/skills"         # GitHub Copilot CLI
  "$HOME/.gemini/skills"          # Gemini CLI
  "$HOME/.trae/skills"            # Trae
  "$HOME/.codebuddy/skills"       # CodeBuddy
  "$HOME/.comate/skills"          # 文心快码 Comate
  "$HOME/.qoderwork/skills"       # 通义灵码 Qoder
)

installed=0
for dir in "${CANDIDATES[@]}"; do
  # 只装进"该产品已存在"的目录（父目录存在说明装过这个 Agent）
  if [ -d "$(dirname "$dir")" ]; then
    install_to "$dir"
    echo "✓ 已安装到 $dir/manim-teaching"
    installed=$((installed + 1))
  fi
done

if [ "$installed" -eq 0 ]; then
  echo "未检测到任何已安装的 Agent 目录。"
  echo "请手动指定你的 Agent skills 目录：bash install.sh <目录>"
  exit 1
fi
echo "完成：共安装到 $installed 个 Agent。重启对应工具后生效。"
