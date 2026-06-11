---
name: shorts-editor
description: Use when turning existing talking-head, interview, vox-pop, vlog, podcast, or UGC footage into a high-retention vertical short for TikTok, Instagram Reels, or YouTube Shorts — cut tighter, dead air / awkward pauses removed, captions added, graphics / zooms / SFX layered in, or a brand splash / end card. Built on HyperFrames + ffmpeg + faster-whisper. Part of the arca-marketing-video kit.
---

# Shorts Editor — Editing Engaging Vertical Shorts

Turn existing talking-head, interview, vox-pop, vlog, podcast, or UGC footage into a
high-retention vertical short for TikTok, Instagram Reels, or YouTube Shorts. Triggers when you
have a raw clip and want it cut tighter, dead air / awkward pauses removed, captions added,
on-screen graphics / zooms / SFX layered in, or a brand splash / end card.
Built on HyperFrames + ffmpeg + faster-whisper.

## Brand profile (read first)
Read `../_arca-marketing-assets/brand.md` for the brand's colors, logo rules, and persona. The brand-splash end card
uses `../_arca-marketing-assets/assets/final-cta.png`; the logo (`../_arca-marketing-assets/assets/logo.png`) may appear as a subtle
in-world mark. `silence_cut.py` and `composition.template.html` are co-located in this skill folder.
This skill is the final edit stage after `video-prompt` (or runs standalone on any raw footage).

## Overview
Turn a finished-but-flat talking clip into a punchy 9:16 short. Engagement is layers stacked on clean footage: a **tight silence-cut** (raw footage only — skip for AI clips), **word-by-word pop-on captions** (Anton, gold keywords, no pill backing), **native treatments** (zoom punch-ins, speed ramps, hard cuts, SFX hits — NOT glass-pill chips), and a **SFX + brand-splash** finish. The composition is HyperFrames HTML; ffmpeg cuts and masters; faster-whisper supplies timing.

**Core principle:** retention is manufactured by deleting dead time and giving the eye a new beat every 2-4s. Cut the pauses first; every other layer just decorates the tightened result.

## When to use
- You have raw footage (interview, vox-pop, vlog, podcast clip, UGC) and want a platform-native vertical edit.
- Requests like: "remove the awkward pauses/silences", "add captions", "make it engaging for Reels/TikTok", "add zooms / SFX / graphics", "add an end card/splash".

Not for: generating footage from scratch, or pure motion-graphics pieces (use the `hyperframes` skill directly).

## Project directory (shared with `video-prompt`)
All artifacts for one video live under a SINGLE project folder so the generate → edit handoff is clean. Same layout `video-prompt` writes:

```
<project-slug>/
  board/         # production board + handoff.txt (from storyboard-prompt), if any
  startframes/   # per-shot start frames (from video-prompt)
  clips/         # generated/raw clips  ← THIS skill's INPUT (from video-prompt, or drop a raw recording here)
  edit/          # this skill's working files: audio_clean.m4a, transcript.json, tight.mp4, composition/, frames/
  out/           # final masters — the deliverable (<slug>-final.mp4)
```

Rules: read source footage from `clips/`, do ALL working files in `edit/`, write only finished masters to `out/`. Never write outside the project folder and never overwrite a source (derived files get new names). If running standalone (no `video-prompt` upstream), create `<project-slug>/` and drop the raw clip into `clips/`.

## Prerequisites
- `npx hyperframes@latest doctor` green (ffmpeg + Chrome).
- `faster-whisper` (pip) for word timestamps. `hyperframes transcribe` needs whisper-cpp, which is often missing; faster-whisper is the reliable fallback.
- Source clip(s) in `<project-slug>/clips/`; all working files go in `<project-slug>/edit/`. Never overwrite the source.

## Pipeline
All paths below are inside the project dir: source from `clips/`, working files in `edit/`, master to `out/`.
1. **Denoise** → `edit/audio_clean.m4a`:
   `ffmpeg -i clips/src.mp4 -af "highpass=85,afftdn,lowpass=12000,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -ac 2 edit/audio_clean.m4a`
2. **Transcribe** word timestamps with faster-whisper → `edit/transcript.json` (`[{text,start,end}]`). `small.en` only if the audio is English.
3. **Silence-cut** with `./silence_cut.py` → `edit/tight.mp4` (the non-obvious core, see below). **SKIP this
   step for AI-generated footage** (clips from `video-prompt` / Wyren): it is already tight and its
   pauses are intentional comedic beats — the cutter is built for RAW talking-head dead air, not for
   generated clips. For AI footage, go straight to assembly and keep the clips' timing. Only run the
   silence-cut on real raw recordings (interview, vox-pop, vlog, podcast) with genuine dead air.
4. **Re-transcribe `edit/tight.mp4`**, regroup into caption phrases (sentence-aware, 3-5 words). Cutting shifts every timestamp, so always re-transcribe the cut; never remap old times.
5. **Build the composition** in `edit/composition/` from `./composition.template.html`: muted plate + separate dialogue audio + word-pop captions + zooms + logo + splash + SFX (no chips by default). Lint clean.
6. **Draft render** (`--quality draft`) → `edit/frames/`, extract frames at every caption/splash beat, eyeball, fix. Then **`--quality high`** and **master** into `out/`:
   `ffmpeg -i edit/raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5,alimiter=limit=0.95" -c:a aac -b:a 192k out/<slug>-final.mp4`

## The silence-cut (the part that is easy to get wrong)
**Only for RAW recordings — skip entirely for AI-generated clips** (see Pipeline step 3).
Neither signal alone works:
- **silencedetect** misses pauses filled with ambient/breath above the noise floor.
- **whisper word timestamps** are imprecise around pauses and will report contiguous words across a real ~1s gap (e.g. it claimed "So, cheating" was continuous when 0.8s of silence sat between them).

**Cut where EITHER is true:** acoustic silence (`silencedetect=noise=-33dB:d=0.35`) OR a transcript word-gap > 0.45s. Only remove the dead middle when it exceeds ~0.5s, leave ~0.1s of speech pad each side, and KEEP sub-0.5s gaps (natural rhythm — cutting every micro-gap machine-guns the edit and looks glitchy). Add a 10ms `afade` at each join to kill clicks. **Verify with silencedetect on the OUTPUT** — it should show only short breath gaps. `./silence_cut.py` implements all of this; tune `--cut-min`.

## Layers (all face/caption-safe)
- **Captions — word-by-word pop-on (the default):** each WORD pops in as it's spoken (Anton, UPPERCASE,
  brand-gold keywords, NO pill backing — stroke + shadow for legibility). This is the canonical standard;
  the flat phrase-fade is the weak default, don't ship it. Full spec + data shape + the GSAP loop are in
  **Caption standard** below; `./composition.template.html` already implements it.
- **Native treatments over graphic "chips" (chips are OFF by default):** do NOT add the glass-pill /
  badge "chip" by default — it reads as AI / vibe-coded. Manufacture beats with NATIVE editing instead:
  zoom punch-ins, speed ramps / hold-frames, the word-pop captions themselves (gold keyword emphasis),
  hard cuts on the beat, and SFX hits. Only add a chip if the user explicitly asks for an on-screen
  label, and keep it minimal. The chip CSS/JS is removed from the default template.
- **Zoom punch-ins:** scale the plate wrapper (base ~1.04) to ~1.10-1.14 on emphasis lines, ease back. Never scale below 1.0 (reveals letterbox edges). Cover-fit the plate.
- **SFX:** a curated set ships in `./sfx/` — use these first (no download needed). Keep dialogue front (SFX vol 0.25-0.35); every `<audio>` needs an `id`. Mapping:
  | Role | File |
  | --- | --- |
  | Opening riser (first frame) | `./sfx/riser-high.mp3` |
  | Hard cut / speaker change | `./sfx/swoosh-high.mp3`, `./sfx/swoosh-low.mp3` |
  | Chip entrance / key reveal (pop) | `./sfx/ding.mp3` |
  | Brand-splash signature hit (reserve for splash only) | `./sfx/tiktok-boom-bling.mp3` |
  | Glitch / error beat | `./sfx/glitch.mp3` |
  | "Wrong"/mistake beat | `./sfx/wrong.mp3` |
  | Comedic deflation | `./sfx/sad-violin.mp3` |
  Need something not here? Mixkit free SFX (`mixkit.co/free-sound-effects/<cat>/` → `assets.mixkit.co/.../<id>-preview.mp3`) is a reliable no-key source.
- **Brand splash:** 3s end card (a still image — use `../_arca-marketing-assets/assets/final-cta.png`), brought in by a quick white flash + the signature SFX (`./sfx/tiktok-boom-bling.mp3`), with a subtle ken-burns zoom. Reserve that SFX for the splash only.

## Caption standard (the canonical caption layer)
Captions exist to (a) make the video legible sound-off, (b) hold retention with a beat every word, and
(c) feel native/hand-made, not AI-templated. If a caption reads like a generic SaaS overlay, it's wrong.
`./composition.template.html` implements all of this — keep it as the default.

**Hard rules (never break):**
- ONE caption group visible at a time — hard-hide the current before the next appears.
- NO pill/lozenge backings, NO badge-icon chips. Legibility comes from **stroke + shadow**, not a box
  (floating glass pills are the #1 "AI-looking" tell).
- Captions are the **wording source of truth** — they carry the exact script even if native/synth audio
  drops a word.
- Never cover the face — captions live in the lower third; any other graphic stays lower-mid or a top strip.
- Derive timing from **word-level transcription of the FINAL cut** (re-transcribe after any trim). Never
  hand-guess or remap old times.

**Font / size / layout:** Anton (or a heavy grotesk like Archivo Black for premium brands), UPPERCASE by
default (sentence case only for a strictly soft/premium voice), one caption font for the whole video,
embedded (`fonts/` woff2 — source `https://cdn.jsdelivr.net/npm/@fontsource/<font>/files/<font>-latin-400-normal.woff2`).
Body ~84–96px on 1080×1920 (~4.5–5% of height); punch/punchline group ~160–190px (`.cap.big`). Centered,
baseline ~300px from bottom (clear of the platform UI safe zone), max width ~960px, ≥60px side margins,
max 2 lines / 3–5 words per group (wrap past 2 lines → split into another group).

**Color / contrast (from brand profile):** base words white (`--ink`); keyword highlight = the brand
HIGHLIGHT color (`--hl`; Arca Sun Yellow `#FED21A`); reserve a second brand color for special emphasis
only. Legibility (replaces any pill): `-webkit-text-stroke: 2.5–3px rgba(3,8,14,.6)` + `text-shadow: 0 5px
20px rgba(0,0,0,.7), 0 2px 4px rgba(0,0,0,.9)`. Soften the keyword stroke (dark-amber) so the gold doesn't muddy.

**Grouping / data shape:** 3–5 words per group, sentence-aware (don't split mid-clause). Each group =
`{ start, end, big?, words:[{w, s, e}] }` from the word-level transcript; group `start` ≈ first word
`start − 0.06`.

**Animation — word-by-word pop-on (dynamic default):** words snap in as spoken, accumulating across the
group (not all at once, not a flat fade). Per word at `word.s − 0.04`:
`fromTo({opacity:0,scale:0.5,y:16},{opacity:1,scale:1,y:0,duration:0.20,ease:"back.out(2.8)"})`. Punch
group (`big`) uses `ease:"back.out(4)"` + the big size. Group exit: fade/slide out ~0.16s then
`set({opacity:0,visibility:"hidden"})`. Always `overwrite:"auto"` on word/group tweens. Sparingly: a
yellow marker-swipe behind a keyword or a slight whole-group rise — no spin/bounce gimmicks.

**Keyword highlighting:** gold only the 1–2 load-bearing words per line (product term, punch word, CTA
verb) — never every word (kills emphasis), never none. Match by normalizing punctuation:
`word.toLowerCase().replace(/[^a-z0-9-]/g,"")` so `"PANIC."`→`panic`, `"AI-first,"`→`ai-first`.

**Timing (no overlap, ever):** `inAt = max(0, group.start − 0.06)`;
`hardOut = min(group.end + 0.12, nextGroup.start − 0.06)`; floor `if (hardOut ≤ inAt + 0.2) hardOut = inAt + 0.2`.
Keep sub-0.5s natural speech rhythm — don't machine-gun a separate caption onto every tiny word.

**Don'ts:** ❌ glass pills / gradient badges / floating chips · ❌ two captions at once · ❌ slow
cross-dissolves / cinematic fades · ❌ tiny text, thin weights, or a generic system font · ❌ everything
(or nothing) highlighted · ❌ captions over the face or in the platform UI zone.

## Gotchas
| Symptom | Fix |
| --- | --- |
| `hyperframes transcribe` fails (whisper-cpp not found) | use faster-whisper directly |
| A pause survives the cut | use silencedetect ∪ word-gap union, not either alone |
| Two captions on screen at once | clamp hard-hide to `min(end+0.12, next.start-0.06)`, floor `inAt+0.2` (see Caption standard) |
| Font silently falls back | Anton/Archivo etc. are NOT auto-embedded; download `.woff2` to `fonts/` + `@font-face` |
| SFX silent in the render | every `<audio>` needs an `id` |
| Graphics cover the face | keep overlays in the lower-mid band (or a top strip), never the center |
| Peaks clip (max 0.0 dBFS) | master the final with `loudnorm + alimiter` |
| Can't preview alpha/cutout in ffmpeg | ffmpeg 4.x can't decode VP9-alpha; verify in Chrome (canvas getImageData) |

## Files
- `./silence_cut.py` — silence ∪ word-gap cutter: `--src --audio --transcript --out [--cut-min 0.5]`.
- `./composition.template.html` — HyperFrames composition skeleton (plate, word-pop captions, zooms, splash, SFX; chips removed from default) with the load-bearing GSAP logic already wired.
- `./sfx/` — bundled, ready-to-use SFX (riser, swooshes, ding, tiktok-boom-bling, glitch, wrong, sad-violin). See the SFX mapping above.
