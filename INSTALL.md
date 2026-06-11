# Install the Arca marketing skills (no coding needed)

You don't need to know any commands. You just ask your AI agent (ChatGPT, Claude, Cursor, Codex…) to fetch the files for you.

---

## The easy way — paste this to your AI agent

Copy everything between the lines and send it to your agent:

```
Please install the Arca marketing skills into this environment.

1. Download every folder inside the "skills/" directory of this public GitHub repo:
   https://github.com/aobalitaan/arca-marketing/tree/main/skills

2. Place each of those folders so it sits DIRECTLY inside my agent's skills folder
   (exactly one level deep — folder name, then SKILL.md inside it). Use the folder for my tool:
     • Claude / Claude Code  ->  .claude/skills/
     • Cursor                ->  .cursor/skills/
     • Codex                 ->  .agents/skills/
   If you are ChatGPT in a sandbox without a skills folder, just keep the files in the
   working directory and follow each SKILL.md as instructions when I ask.

3. IMPORTANT: also copy the "_arca-marketing-assets" folder into the same skills folder,
   right next to the skill folders. Every skill reads the brand profile and assets from it.

4. When done, list the skills you installed and tell me to start with "arca-marketing".
```

That's it. Then say **"use the arca-marketing skill"** (or "where do I start?") and it walks you through the rest.

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

## Set up the video tools (only if you'll edit videos)

The image skills (`brand-builder`, `design-guide`, `carousel-generator`, `storyboard-prompt`) need nothing extra. The **video editing** skill (`shorts-editor`) renders with **HyperFrames**, which needs a few free tools: Node.js, ffmpeg, Google Chrome, and faster-whisper (for captions).

Easiest: ask your agent to set it up. Paste this:

```
Set up the video tools for the shorts-editor skill in this environment:
1. Make sure Node.js is installed, then run:  npx hyperframes@latest doctor
2. Install anything it reports missing — usually ffmpeg and Google Chrome.
3. Install the captions tool:  pip install faster-whisper
4. Run "npx hyperframes@latest doctor" again and confirm everything is green.
Tell me if something can't be installed in this environment.
```

Manual equivalent:
- `npx hyperframes@latest doctor` — checks ffmpeg + Chrome and lists what's missing
- **ffmpeg** — `brew install ffmpeg` (Mac), `sudo apt install ffmpeg` (Linux), or a build from ffmpeg.org (Windows)
- **Google Chrome** — HyperFrames renders frames with it
- **faster-whisper** — `pip install faster-whisper` (word-level captions)

> Heads-up: this is the one part that needs a real machine/sandbox that can install ffmpeg + Chrome. If your environment can't, you can still do everything up through generating the clips, then do the final edit on a computer that can.

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
