#!/usr/bin/env node
'use strict';

// Installs the four Arca marketing skills into a Claude Code skills directory.
//   npx arca-marketing-video            -> ./.claude/skills (this project)
//   npx arca-marketing-video --global   -> ~/.claude/skills (all projects)

const fs = require('fs');
const path = require('path');
const os = require('os');

const args = process.argv.slice(2);

if (args.includes('-h') || args.includes('--help')) {
  process.stdout.write(`
arca-marketing-video — install the marketing skills into Claude Code

Usage:
  npx arca-marketing-video            Install into ./.claude/skills (this project)
  npx arca-marketing-video --global   Install into ~/.claude/skills (all projects)
  npx arca-marketing-video --help     Show this help

Installs: carousel-generator, storyboard-prompt, video-prompt, shorts-editor
(plus a shared brand profile + assets the skills read).
`);
  process.exit(0);
}

const isGlobal = args.includes('--global') || args.includes('-g');
const baseDir = isGlobal ? os.homedir() : process.cwd();
const skillsRoot = path.join(baseDir, '.claude', 'skills');
const srcSkills = path.join(__dirname, '..', 'skills');

if (typeof fs.cpSync !== 'function') {
  process.stderr.write('Error: Node 16.7+ is required (fs.cpSync). Please upgrade Node.\n');
  process.exit(1);
}

const skillsRootExisted = fs.existsSync(skillsRoot);
fs.mkdirSync(skillsRoot, { recursive: true });

const entries = fs
  .readdirSync(srcSkills, { withFileTypes: true })
  .filter((d) => d.isDirectory());

const installedSkills = [];
for (const dir of entries) {
  const from = path.join(srcSkills, dir.name);
  const to = path.join(skillsRoot, dir.name);
  fs.rmSync(to, { recursive: true, force: true });
  fs.cpSync(from, to, { recursive: true });
  if (!dir.name.startsWith('_')) installedSkills.push(dir.name);
}

process.stdout.write(`\n✓ Installed ${installedSkills.length} Arca marketing skills into ${skillsRoot}\n`);
for (const name of installedSkills.sort()) process.stdout.write(`  • ${name}\n`);
process.stdout.write(`  (+ shared brand profile & assets in _arca-marketing-assets)\n`);

if (!skillsRootExisted) {
  process.stdout.write(
    `\nNote: .claude/skills was just created — restart Claude Code once so it starts watching the folder.\n\n`
  );
} else {
  process.stdout.write(
    `\nThe skills are available now — Claude Code detects skill changes live.\n\n`
  );
}
