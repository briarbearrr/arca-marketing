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
Read `../_arca-marketing-assets/brand.md` for the brand's colors and persona. The brand-splash end card
uses `../_arca-marketing-assets/assets/final-cta.png`. **NEVER composite the brand logo onto the footage — no corner watermark, no overlay logo, anywhere.** A pasted-on logo reads as a fake watermark and kills the native feel; the brand mark only ever appears DIEGETICALLY (filmed as a real in-world prop) in the generated footage upstream (`video-prompt`), never added here. The ONLY brand graphic the editor places is the end splash card (`final-cta.png`). `silence_cut.py` and `composition.template.html` are co-located in this skill folder.
This skill is the final edit stage after `video-prompt` (or runs standalone on any raw footage).

## Overview
Turn a finished-but-flat talking clip into a punchy 9:16 short. Engagement is layers stacked on clean footage: a **tight silence-cut** (raw footage AND assembled AI clips — Kling pads dead air into every generated clip), **word-by-word pop-on captions** (Anton, gold keywords, no pill backing), **native treatments** (zoom punch-ins, speed ramps, hard cuts, SFX hits — NOT glass-pill chips), and a **SFX + brand-splash** finish. The composition is HyperFrames HTML; ffmpeg cuts and masters; faster-whisper supplies timing.

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
3. **Silence-cut** with `./silence_cut.py` → `edit/tight.mp4` (the non-obvious core, see below). **Run this on AI-generated footage too** (clips from `video-prompt` / Wyren), not just raw recordings. Kling and similar models pad EVERY generated clip with ~1–2s of dead air — a slow lead-in plus a tail after the last word — so stacked clips drag badly. The old "AI clips are already tight, skip it" assumption is the opposite of reality. **Assemble the clips first, then silence-cut the assembled video.** For AI footage tune the cutter sensitive: `--cut-min 0.35` and a lower noise floor (`-36 dB`) to catch the quiet, breath-filled padding, leaving ~0.1s pads so only natural beats survive. Real raw recordings (interview, vox-pop, vlog, podcast) use the default settings.

   **Mind the tail / SFX.** AI clips often land the FINAL WORD right at the out-point, so the ~0.1s pad after the last word matters, and **never land a transition SFX on a cut where a word ends** (it steps on the last word — see the SFX layer).
4. **Re-transcribe the ASSEMBLED cut** (`edit/tight.mp4` — for raw footage OR an assembled AI-clip video), regroup into caption phrases (sentence-aware, 3-5 words). The silence-cut shifts every timestamp, so always re-transcribe and recompute **caption, zoom, SFX, and splash** timing from the NEW boundaries; never remap old times.
5. **Scan faces, then build the composition.** FIRST sample frames across the cut (`ffmpeg -i edit/tight.mp4 -vf fps=2 edit/faces/f_%03d.png`) and READ them to note which vertical band each scene's face(s) occupy (see FACE-SAFE PLACEMENT) — faces move between shots, so map them per scene. THEN build `edit/composition/` from `./composition.template.html` (muted plate + dialogue audio + word-pop captions + zooms + splash + SFX, no chips and NO logo watermark by default), placing captions and EVERY graphic in a band that clears the detected faces. Lint clean.
6. **Draft render + FACE-SAFE & SAFE-AREA CHECK** (`--quality draft`) → `edit/frames/`: extract a frame at EVERY caption / chip / splash beat, READ each one, and confirm NO caption, figure, or graphic (a) overlaps a face OR (b) crosses the platform safe margins — nothing under the right action rail (~120–150px), the bottom UI (~300–340px), or the top (~120px); the widest punch caption is the usual offender. If any does, move/shrink that element (or nudge the plate up via the cover-fit transform) and re-render — do NOT proceed to the high render until every overlay clears every face AND sits inside the safe area. Then **`--quality high`** and **master** into `out/`:
   `ffmpeg -i edit/raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5,alimiter=limit=0.95" -c:a aac -b:a 192k out/<slug>-final.mp4`
   Master in a SINGLE video encode and `-c:v copy` on the mux — re-encoding the video across multiple passes stacks compression artifacts. To trim a span out of a FINISHED master, **ripple-cut** (cut video + audio + baked captions together so they stay in sync) — valid only if NO caption is mid-display across the cut window.

## The silence-cut (the part that is easy to get wrong)
**Run on BOTH raw recordings and assembled AI-clip videos** (see Pipeline step 3). Kling pads every generated clip with ~1–2s of dead air, so AI assemblies need this just as much as raw footage — for AI clips tune sensitive (`--cut-min 0.35`, noise floor `-36 dB`).
Neither signal alone works:
- **silencedetect** misses pauses filled with ambient/breath above the noise floor.
- **whisper word timestamps** are imprecise around pauses and will report contiguous words across a real ~1s gap (e.g. it claimed "So, cheating" was continuous when 0.8s of silence sat between them).

**Cut where EITHER is true:** acoustic silence (`silencedetect=noise=-33dB:d=0.35`) OR a transcript word-gap > 0.45s. Only remove the dead middle when it exceeds ~0.5s, leave ~0.1s of speech pad each side, and KEEP sub-0.5s gaps (natural rhythm — cutting every micro-gap machine-guns the edit and looks glitchy). Add a 10ms `afade` at each join to kill clicks. **Verify with silencedetect on the OUTPUT** — it should show only short breath gaps. `./silence_cut.py` implements all of this; tune `--cut-min`. **For AI-clip assemblies** (Kling et al.), the padding is quiet near-silent breath that `-33 dB` can miss — drop the noise floor to `-36 dB` and `--cut-min 0.35` to catch it.

**Don't word-gap-cut a foley/VO/music format** (e.g. a trailer with no continuous dialogue). Word-gap detection assumes speech, so on speechless foley beats it reads the whole clip as a "gap" and guts it. For those formats, SKIP the word-gap cut: trim each Kling clip's head pad MANUALLY and time captions analytically (see Caption standard) instead.

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
- **In-world / screen graphics are NOT an editor job — generate them upstream.** Anything that belongs ON a
  surface in the scene (a laptop/phone screen's content, an in-scene poster, a product label, a "now loading"
  promo) must be generated DIEGETICALLY inside the video clip by `video-prompt`, never composited here.
  Pasted in the edit it floats in mid-air, covers faces, and looks fake — e.g. a "SYNERGIZE YOUR VIBES" card
  meant for the laptop screen ends up hovering over the whole team. The editor only adds captions, the brand
  splash / end card, and (rarely, if asked) a minimal face-safe chip — nothing that's supposed to live in the scene.
- **Zoom punch-ins:** scale the plate wrapper (base ~1.04) to ~1.10-1.14 on emphasis lines, ease back. Never scale below 1.0 (reveals letterbox edges). Cover-fit the plate.
- **SFX:** a curated set ships in `./sfx/` — use these first (no download needed). Keep dialogue front — **default SFX volume 0.12–0.22** (quieter than feels right; SFX should punctuate, not blare). Harsh / sharp sounds (buzzers, booms, risers) sit at the BOTTOM of that range or lower; only the brand-splash signature hit may go a touch louder. Every `<audio>` needs an `id`. **Never land a transition/whoosh SFX on a cut where a word ends** — it steps on the last word; put the hit on a silent beat or at the head of the next clip (this is why the silence-cut leaves ~0.1s pad after the last word, see Pipeline step 3). Mapping:
  | Role | File |
  | --- | --- |
  | Opening riser (first frame) | `./sfx/riser-high.mp3` |
  | Hard cut / speaker change | `./sfx/swoosh-high.mp3`, `./sfx/swoosh-low.mp3` |
  | Chip entrance / key reveal (pop) | `./sfx/ding.mp3` |
  | Caption word / keyword pop | `./sfx/pop.mp3` |
  | Subtle UI tick / select | `./sfx/click-soft.mp3` |
  | Photo snapshot / freeze-frame beat | `./sfx/camera-shutter.mp3` |
  | Light transition / scene change | `./sfx/transition-sweep.mp3` |
  | Correct / affirm / success beat | `./sfx/correct.mp3` |
  | Positive notification / reveal | `./sfx/notification.mp3` |
  | Achievement / reward sparkle | `./sfx/bling.mp3` |
  | Typing / on-screen text beat | `./sfx/keyboard.mp3` |
  | Brand-splash signature hit (reserve for splash only) | `./sfx/tiktok-boom-bling.mp3` |
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
- Never cover the face — DETECT where the face actually sits per scene and place captions/graphics in a band that clears it (see FACE-SAFE PLACEMENT). The lower-third default only holds when the face is high in frame; if the face sits low, raise the captions or push the plate up.
- Derive timing from **word-level transcription of the FINAL cut** (re-transcribe after any cut, including
  the AI-clip silence-cut). The same re-transcription drives caption, zoom, SFX, and splash timing — recompute
  them all from the new boundaries. Never hand-guess or remap old times.
- **Noisy mixed audio (music + foley + VO): don't transcribe the MIX** — source timing per layer. Narrator
  captions from the `voiceAI` word-alignment (plus the clip's offset); character / native lines by transcribing
  the **native-audio-only cut** (a separate export with just the dialogue track), not the final mix.

**Font / size / layout:** Anton (or a heavy grotesk like Archivo Black for premium brands), UPPERCASE by
default (sentence case only for a strictly soft/premium voice), one caption font for the whole video,
embedded (`fonts/` woff2 — source `https://cdn.jsdelivr.net/npm/@fontsource/<font>/files/<font>-latin-400-normal.woff2`).
Body ~62–72px on 1080×1920 (~3.3–3.8% of height; default 66px — readable, NOT oversized); punch/punchline
group ~115–130px (`.cap.big`, default 120px). Keep these sizes restrained — captions that fill the frame
read amateur and overflow the safe area. Centered, baseline ~340px from bottom, **max width ~840px with
≥90px side padding**, `overflow-wrap:break-word`, max 2 lines / 3–5 words per group (wrap past 2 lines →
split into another group).

**SAFE AREA (TikTok / IG Reels / Shorts) — captions must stay inside it.** The platform UI eats the edges:
bottom ~300–340px (caption, username, nav), the RIGHT action rail ~120–150px (like/comment/share), and the
top ~120px. Keep every caption (and the punch group, which is widest) within the **central ~840px column**
and **above ~330px from the bottom** so nothing slides under the rail or the bottom chrome. A single long
word at `.cap.big` size is the usual offender — it can't wrap, so it spills off-frame; if a punch word is
very long, drop that group out of `.big` or shorten it. Verify in the FACE-SAFE draft-frame check (Phase 6):
confirm no caption crosses the side/bottom safe margins, not just that it clears faces.

**Color / contrast (from brand profile):** base words white (`--ink`); keyword highlight = the brand
HIGHLIGHT color (`--hl`; Arca Sun Yellow `#FED21A`); reserve a second brand color for special emphasis
only. Legibility (replaces any pill): `-webkit-text-stroke: ~2–2.5px rgba(3,8,14,.6)` (scale with font size — lighter on the smaller body) + `text-shadow: 0 5px
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

## FACE-SAFE PLACEMENT (captions + every graphic must clear faces)
The #1 overlay failure is text or a figure landing ON someone's face. "Captions live in the lower third" only holds when the face sits HIGH in frame — but talking-head / UGC framing varies wildly (desk-level POV, low or off-center framing, two people, a face near the bottom, or a subject reframed by a zoom punch-in). A blind lower-third caption then covers the face. So DETECT, don't assume:

- **Find the face before placing anything.** Sample frames across each scene (`ffmpeg -i edit/tight.mp4 -vf fps=2 edit/faces/f_%03d.png`) and READ them to note which vertical band each scene's face(s) occupy. Faces MOVE between shots — map them per scene/segment, never once for the whole video.
- **Place overlays in a band that clears the face**, keeping a margin of ≥8–10% of frame height around the face:
  - Face high / centered (common case) → captions in the lower third (default baseline ~300px from bottom).
  - Face LOW (in the lower third) → RAISE the captions to an upper band / top strip, OR push the plate up via the cover-fit / zoom transform so the face leaves the caption band. Never drop text onto a low face.
  - Two faces, or a face off to one side → use the genuinely clear band (top strip, or the empty side); never straddle a face.
- **Every inserted element obeys this — not just captions:** word-pop captions, any chip / label, engagement figures / graphics, and the splash. Each keeps the same face margin AND stays out of the platform UI safe zone (bottom ~10%). (There is no logo watermark — the editor never composites the brand mark.)
- **If no band is safe** at a given moment (a face fills the frame), shrink or move the element, delay it to a face-clear beat, or drop it — covering the face is never acceptable.
- **Verify on real frames, not by assumption** (Pipeline step 6): extract the frame at every overlay beat, look, and move anything touching a face before the high render. When the face moves into the caption band mid-segment, re-place the captions (or the plate) for that segment and re-derive timing.

## Gotchas
| Symptom | Fix |
| --- | --- |
| `hyperframes transcribe` fails (whisper-cpp not found) | use faster-whisper directly |
| A pause survives the cut | use silencedetect ∪ word-gap union, not either alone |
| AI clips drag / dead air between clips | run the silence-cut on the assembled AI video (`--cut-min 0.35`, noise `-36 dB`, ~0.1s pads) — don't skip it for AI footage |
| Last word clipped at a cut / SFX steps on speech (AI clips) | keep the ~0.1s pad after the last word; never land a transition SFX where a word ends |
| Two captions on screen at once | clamp hard-hide to `min(end+0.12, next.start-0.06)`, floor `inAt+0.2` (see Caption standard) |
| Font silently falls back | Anton/Archivo etc. are NOT auto-embedded; download `.woff2` to `fonts/` + `@font-face` |
| SFX silent in the render | every `<audio>` needs an `id` |
| Captions or graphics land on a face | don't assume lower-third is safe — sample frames, find the face per scene, place overlays in a band that clears it (raise captions or push the plate up when the face sits low), verify on extracted frames before the high render (see FACE-SAFE PLACEMENT) |
| A brand logo / watermark shows up over the footage | the editor must NOT composite the logo anywhere — delete any `#logo` element; the brand mark belongs in the footage diegetically (upstream) and on the end splash only |
| Peaks clip (max 0.0 dBFS) | master the final with `loudnorm + alimiter` |
| HyperFrames duration looks off | its CLI duration summary misreports — trust `ffprobe` for true duration; the render also expects `index.html` in a project dir |
| Is the dialogue audible over music? | you can't audition audio — checkpoint the mix / levels with the user before finalizing |
| Can't preview alpha/cutout in ffmpeg | ffmpeg 4.x can't decode VP9-alpha; verify in Chrome (canvas getImageData) |

## Files
- `./silence_cut.py` — silence ∪ word-gap cutter: `--src --audio --transcript --out [--cut-min 0.5]`.
- `./composition.template.html` — HyperFrames composition skeleton (plate, word-pop captions, zooms, splash, SFX; chips removed from default) with the load-bearing GSAP logic already wired.
- `./sfx/` — bundled, ready-to-use SFX (riser, swooshes, ding, tiktok-boom-bling, wrong, sad-violin, pop, click-soft, camera-shutter, transition-sweep, correct, notification, bling, keyboard). See the SFX mapping above.
