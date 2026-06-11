---
name: arca-marketing
description: Use when getting started with the Arca marketing kit, or when unsure which Arca skill to use — orients you and routes to the right one. The kit makes brand-consistent short-form marketing content (carousels, storyboards, AI videos, edited shorts) from one shared brand profile. Triggers on "make marketing content", "where do I start", "make a video/carousel/short for my brand", "set up my brand", "which arca skill". Part of the arca-marketing-video kit.
---

# Arca Marketing — Start Here

This is the front door to a kit of six skills that turn a brand into platform-native short-form content (TikTok / Reels / Shorts / Instagram). Everything reads from ONE shared brand profile, so the whole kit speaks in your brand's voice. You don't need to be technical — describe what you want in plain language and the right skill takes over.

## First time? Do the one-time brand setup
1. **`brand-builder`** — answer a short guided Q&A; it writes your `brand.md` (name, tone, audience, colors, persona, hooks). This retargets the whole kit to your brand.
2. **`design-guide`** — generates a one-page brand identity board from your `brand.md` (a visual style reference).

If `brand.md` is still the example brand, start with `brand-builder`.

## Then make content — pick by what you want
| You want… | Use this skill | Say something like |
| --- | --- | --- |
| An Instagram/LinkedIn carousel (3–5 slides) | **`carousel-generator`** | "make a carousel about X" |
| To pressure-test a video idea + a full production board | **`storyboard-prompt`** | "storyboard this idea" / "is this concept good?" |
| To turn that board into an actual AI video | **`video-prompt`** | "make the video from this storyboard" |
| To cut/caption/polish existing footage into a short | **`shorts-editor`** | "remove the dead air and add captions" |

## The natural workflow (chain them)
```
brand-builder → design-guide                       (one-time brand setup)
storyboard-prompt → video-prompt → shorts-editor   (make + edit an original video)
carousel-generator                                 (standalone image posts)
```
Video projects share one folder: `video-prompt` writes clips into `<project>/clips/`, `shorts-editor` reads them and writes the final cut to `<project>/out/`.

## How the brand stays consistent
All six skills read `_arca-marketing-assets/brand.md` (your brand profile) and `_arca-marketing-assets/assets/` (logo, characters, design board, end card). To switch the kit to a different brand, run `brand-builder` again (rewrites `brand.md`), swap in that brand's `logo.png`, and re-run `design-guide`.

## Generation + video tools
- **Wyren MCP** (`npx wyren-mcp`, project-scoped) powers AI image/video generation — needed when `storyboard-prompt` renders the board and when `video-prompt` generates clips. If those skills can't reach `mcp__wyren__*`, point the user to INSTALL.md Part B (run `npx wyren-mcp` and approve in the browser; or add the HTTP MCP `https://api.wyren.ai/mcp`).
- **HyperFrames** (Node.js + ffmpeg + Google Chrome + faster-whisper) is needed ONLY by `shorts-editor` for the final edit. If it's not set up, point to INSTALL.md Part B (`npx hyperframes@latest doctor`, install ffmpeg/Chrome, `pip install faster-whisper`).
The planning/text skills (`brand-builder`, `carousel-generator` as prompts) need neither.

## If a skill seems missing
The kit is six skill folders that live one level deep in your agent's skills folder (e.g. `.claude/skills/<name>/SKILL.md`), plus the shared `_arca-marketing-assets/` folder beside them. If a skill doesn't trigger, the folder is probably nested too deep or the assets folder is missing — see the kit's README install steps.
