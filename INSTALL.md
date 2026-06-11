# Install the Arca marketing skills (no coding needed)

You don't need to know any commands. You just ask your AI agent (ChatGPT, Claude, Cursor, Codex…) to fetch the files for you.

---

## The easy way — paste this to your AI agent

Copy everything between the lines and send it to your agent:

```
Please set up the Arca marketing kit in this environment.

PART A — install the skills (always do this):
1. Download every folder inside the "skills/" directory of this public GitHub repo:
   https://github.com/aobalitaan/arca-marketing/tree/main/skills
2. Install them into THIS PROJECT (the current working directory) — NOT globally in my home
   folder. Use the project-scoped skills folder, creating it if it doesn't exist; place each
   skill folder DIRECTLY inside it (exactly one level deep — folder name, then SKILL.md inside).
     • Claude / Claude Code  ->  ./.claude/skills/    (in this project — do NOT use ~/.claude/skills)
     • Cursor                ->  ./.cursor/skills/
     • Codex                 ->  ./.agents/skills/
   If you are ChatGPT in a sandbox without a skills folder, just keep the files in the
   current working directory and follow each SKILL.md as instructions when I ask.
3. Also copy the "_arca-marketing-assets" folder into that same project skills folder, right
   next to the skill folders. Every skill reads the brand profile and assets from it.

PART B — set up the video tools (only needed for the shorts-editor skill; skip if you can't):
4. If Node.js is available, run:  npx hyperframes@latest doctor
5. Install anything it reports missing — usually ffmpeg and Google Chrome.
6. Install the captions tool:  pip install faster-whisper
7. Run "npx hyperframes@latest doctor" again to confirm it's green.

When done: print the EXACT folder path you installed into (it should be inside this project,
e.g. ./.claude/skills/ — if it's in my home folder, move it into the project), list the skills,
say whether the video tools are ready, and tell me to start with "arca-marketing".
```

That's it — one paste does everything. Then say **"use the arca-marketing skill"** (or "where do I start?") and it walks you through the rest.

---

## What you just installed

Seven folders land in your project's skills folder (`./.claude/skills/` in the current project):

- `arca-marketing` — **start here**; orients you and points to the right skill
- `brand-builder` — Q&A that writes your brand profile
- `design-guide` — generates your brand identity board
- `carousel-generator` — Instagram/LinkedIn carousels
- `storyboard-prompt` — pressure-tests a video idea into a production board
- `video-prompt` — turns the board into an AI video
- `shorts-editor` — cuts/captions footage into a finished short

…plus `_arca-marketing-assets/` (the shared brand profile + logo/images the skills read).

---

## About the video tools (Part B above)

The image skills (`brand-builder`, `design-guide`, `carousel-generator`, `storyboard-prompt`) need nothing extra. Only the **video editing** skill (`shorts-editor`) needs **HyperFrames** + a few free tools — Node.js, ffmpeg, Google Chrome, and faster-whisper (for captions). Part B of the paste above sets these up; you don't need a second prompt.

Manual equivalent, if you'd rather do it yourself:
- `npx hyperframes@latest doctor` — checks ffmpeg + Chrome and lists what's missing
- **ffmpeg** — `brew install ffmpeg` (Mac), `sudo apt install ffmpeg` (Linux), or a build from ffmpeg.org (Windows)
- **Google Chrome** — HyperFrames renders frames with it
- **faster-whisper** — `pip install faster-whisper` (word-level captions)

> Heads-up: Part B needs a real machine/sandbox that can install ffmpeg + Chrome. If your environment can't, Part A still works — do everything up through generating the clips, then run the final edit on a computer that can.

---

## Alternative installs (if you're comfortable with a terminal)

- **Skills CLI:** `npx skills add aobalitaan/arca-marketing`
- **In-chat:** install the `/learn` command, then `/learn @aobalitaan/arca-marketing`
- **npm (Claude Code):** `npx arca-marketing-video` (copies the skills into `.claude/skills/`)
- **Manual:** clone the repo and copy the contents of `skills/` into this project's `./.claude/skills/` folder (not the global `~/.claude/skills/`).

## First steps after installing
1. Say **"use arca-marketing"** — it explains the kit.
2. Run **`brand-builder`** to set up your brand.
3. Then make content: `carousel-generator`, or `storyboard-prompt → video-prompt → shorts-editor`.
