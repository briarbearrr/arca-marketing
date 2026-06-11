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
2. Place each folder so it sits DIRECTLY inside my agent's skills folder (exactly one level
   deep — folder name, then SKILL.md inside it). Use the folder for my tool:
     • Claude / Claude Code  ->  .claude/skills/
     • Cursor                ->  .cursor/skills/
     • Codex                 ->  .agents/skills/
   If you are ChatGPT in a sandbox without a skills folder, just keep the files in the
   working directory and follow each SKILL.md as instructions when I ask.
3. Also copy the "_arca-marketing-assets" folder into that same skills folder, right next
   to the skill folders. Every skill reads the brand profile and assets from it.

PART B — set up the video tools (only needed for the shorts-editor skill; skip if you can't):
4. If Node.js is available, run:  npx hyperframes@latest doctor
5. Install anything it reports missing — usually ffmpeg and Google Chrome.
6. Install the captions tool:  pip install faster-whisper
7. Run "npx hyperframes@latest doctor" again to confirm it's green.

When done: list the skills you installed, say whether the video tools are ready, and tell me
to start with "arca-marketing".
```

That's it — one paste does everything. Then say **"use the arca-marketing skill"** (or "where do I start?") and it walks you through the rest.

---

## What you just installed

Seven folders land in your skills folder:

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
- **Manual:** clone the repo and copy the contents of `skills/` into your `.claude/skills/` folder.

## First steps after installing
1. Say **"use arca-marketing"** — it explains the kit.
2. Run **`brand-builder`** to set up your brand.
3. Then make content: `carousel-generator`, or `storyboard-prompt → video-prompt → shorts-editor`.
