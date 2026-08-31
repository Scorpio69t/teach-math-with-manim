// dsh-manim-teaching — DeepSeek Harness 插件：把 manim-teaching 技能注册进 dsh
//
// 安装：dsh plugin --profile web add github:Scorpio69t/teach-math-with-manim
// （仓库根的 package.json 声明了 dsh.bundle，本行会随安装自动插入 web profile）
//
// 机制：读取同仓 skill/manim-teaching/SKILL.md（Agent Skills 标准格式），
// 解析 frontmatter 后通过 ctx.skills.register() 注册；
// resourceBase 指向技能目录，技能内 rules/、templates/、scripts/ 相对引用可用。

import { readFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const SKILL_DIR = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)), '..', 'manim-teaching')
const SKILL_FILE = path.join(SKILL_DIR, 'SKILL.md')

/** 解析 SKILL.md 的 YAML frontmatter（只需 name / description / whenToUse 三个单行字段）。 */
function parseFrontmatter(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  if (!m) return { meta: {}, body: raw }
  const meta = {}
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^(name|description|whenToUse)\s*:\s*(.*)$/)
    if (kv) meta[kv[1]] = kv[2].trim()
  }
  return { meta, body: raw.slice(m[0].length) }
}

export const name = 'dsh-manim-teaching'
export const inject = ['skills']

export function apply(ctx) {
  const { meta, body } = parseFrontmatter(readFileSync(SKILL_FILE, 'utf8'))
  ctx.skills.register({
    name: meta.name ?? 'manim-teaching',
    description: meta.description
      ?? 'Manim 教学动画生成（ManimCE 版本锁定 + 避坑规则 + 渲染自验证）',
    ...(meta.whenToUse ? { whenToUse: meta.whenToUse } : {}),
    source: 'custom',
    provider: 'dsh-manim-teaching',
    path: SKILL_FILE,
    resourceBase: { kind: 'directory', path: SKILL_DIR },
    content: body,
  })
  ctx.logger?.info?.('[dsh-manim-teaching] skill registered: manim-teaching')
}
