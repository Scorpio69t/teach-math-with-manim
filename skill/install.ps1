# install.ps1 — 把 manim-teaching 技能安装到本机检测到的 AI Agent skills 目录
# 用法：powershell -ExecutionPolicy Bypass -File install.ps1            # 自动探测并安装
#       powershell -ExecutionPolicy Bypass -File install.ps1 <目录>     # 安装到指定目录
param([string]$Target)

$ErrorActionPreference = "Stop"
$Src = Join-Path $PSScriptRoot "manim-teaching"

function Install-To($dir) {
    $dst = Join-Path $dir "manim-teaching"
    if (-not (Test-Path -LiteralPath $dst)) {
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
    }
    $srcReal = (Resolve-Path -LiteralPath $Src).Path.TrimEnd('\', '/')
    $dstReal = (Resolve-Path -LiteralPath $dst).Path.TrimEnd('\', '/')
    if ($dstReal -ieq $srcReal) {
        throw "目标目录与源目录相同，跳过：$dstReal"
    }
    Get-ChildItem -LiteralPath $Src -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $dst -Recurse -Force
    }
    Get-ChildItem -LiteralPath $dst -Directory -Recurse -Filter "__pycache__" | ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
    }
    Get-ChildItem -LiteralPath $dst -File -Recurse -Filter "*.pyc" | ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Force
    }
    Write-Host "[OK] 已安装到 $dst"
}

if ($Target) {
    Install-To $Target
    exit 0
}

# 常见 Agent 的 skills 目录（截至 2026-08；路径随各产品版本变动，
# 失效时以各产品官方文档为准，或用 -Target 手动指定）
$Candidates = @(
    "$env:USERPROFILE\.claude\skills",           # Claude Code
    "$env:USERPROFILE\.agents\skills",           # DeepSeek Harness / Zed 等共享目录
    "$env:USERPROFILE\.config\agents\skills",    # Kimi Code
    "$env:USERPROFILE\.codex\skills",            # Codex CLI
    "$env:USERPROFILE\.copilot\skills",          # GitHub Copilot CLI
    "$env:USERPROFILE\.gemini\skills",           # Gemini CLI
    "$env:USERPROFILE\.trae\skills",             # Trae
    "$env:USERPROFILE\.codebuddy\skills",        # CodeBuddy
    "$env:USERPROFILE\.comate\skills",           # 文心快码 Comate
    "$env:USERPROFILE\.qoderwork\skills"         # 通义灵码 Qoder
)

$installed = 0
foreach ($dir in $Candidates) {
    # 只装进"该产品已存在"的目录（父目录存在说明装过这个 Agent）
    if (Test-Path (Split-Path $dir -Parent)) {
        Install-To $dir
        $installed++
    }
}

if ($installed -eq 0) {
    Write-Host "未检测到任何已安装的 Agent 目录。"
    Write-Host "请手动指定你的 Agent skills 目录：install.ps1 <目录>"
    exit 1
}
Write-Host "完成：共安装到 $installed 个 Agent。重启对应工具后生效。"
