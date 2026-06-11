# Arca Marketing Skills

A brand-driven short-form marketing kit: **seven agent skills** (a "start here" guide + six workers) that share one editable brand profile and asset set. Built for any agent that uses the `SKILL.md` format — Claude Code, Cursor, Codex — and usable from ChatGPT too. Use any skill on its own, or chain them.

## Install — no coding needed

The simplest path (great for non-technical users): just ask your AI agent to fetch the files. See **[INSTALL.md](INSTALL.md)** for a copy-paste prompt — paste it to ChatGPT / Claude / Cursor and it downloads the skills into the right folder for you.

> The skills are plain files in this public repo, so any file-capable agent can install them — no `npx`, no terminal.

### Other ways to install
- **Skills CLI:** `npx skills add aobalitaan/arca-marketing`
- **In-chat:** install the `/learn` command, then `/learn @aobalitaan/arca-marketing`
- **npm (Claude Code):** `npx arca-marketing-video` (copies the skills into `.claude/skills/`; add `--global` for `~/.claude/skills/`)
- **Manual:** copy the **contents** of `skills/` into your agent's skills folder (`.claude/skills/`, `.cursor/skills/`, or `.agents/skills/`) so each skill folder sits exactly one level deep, and keep `_arca-marketing-assets/` beside them.

> Skills must be exactly one level deep — `.claude/skills/<name>/SKILL.md`. Don't nest them inside an extra folder, or the agent won't discover them. If your skills folder didn't exist before, restart your agent once so it starts watching it.

## The skills

| Skill | Use when you want to… |
| --- | --- |
| `arca-marketing` | **Start here** — orients you and routes to the right skill |
| `brand-builder` | Run a guided Q&A to create/rewrite your `brand.md` (retargets the kit to your brand) |
| `design-guide` | Generate a one-page brand identity board from your `brand.md` |
| `carousel-generator` | Make a 3–5 slide Instagram/LinkedIn carousel (4:5) |
| `storyboard-prompt` | Pressure-test a video idea → a full production board + text breakdown |
| `video-prompt` | Turn a production board into a vertical AI video (drives the Wyren MCP) |
| `shorts-editor` | Cut / caption / add graphics to existing footage → a high-retention short |

After installing, say **"use arca-marketing"** (or just describe what you want).

## Shared brand profile + assets

All skills read brand specifics from one place, so the kit is reusable for any brand:

- `_arca-marketing-assets/brand.md` — the brand profile (run `brand-builder` to generate your own)
- `_arca-marketing-assets/assets/` — `logo.png`, `characters.png`, `design-guide.png`, `final-cta.png`

This `_arca-marketing-assets/` folder has no `SKILL.md`, so it's ignored as a skill; the skills reference it via `../_arca-marketing-assets/…`. **Keep it beside the skill folders when installing.** To retarget to another brand: run `brand-builder` (rewrites `brand.md`), swap in your `logo.png`, and run `design-guide` to regenerate the board.

## Natural chain

```
arca-marketing                                     (start here)
brand-builder  →  design-guide                     (one-time brand setup)
storyboard-prompt  →  video-prompt  →  shorts-editor   (original video; shared project folder)
carousel-generator                                 (independent image posts)
```

## Publishing this to skills.sh (maintainers)

skills.sh indexes public GitHub repos that contain valid `SKILL.md` files. To list this kit:
1. Push this repo public to GitHub.
2. (Optional) Submit the repo URL at **agentskill.sh/submit** to index it.
3. Share the install command `npx skills add aobalitaan/arca-marketing` — it also auto-indexes as people install it.

## License

MIT
