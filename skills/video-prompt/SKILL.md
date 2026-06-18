---
name: video-prompt
description: Use when turning a storyboard or production board into a finished vertical short-form video of any type (UGC, cinematic / movie-trailer, animation, product film, etc.). Handles photographic storyboards (clean and use as start frames), schematic / annotated plans (do NOT upscale 1:1 — rebuild with Wyren clips, on-screen UI generated diegetically, never composited), and comprehensive PRODUCTION BOARDS (character-reference turnaround + environment + floor plan + per-cut storyboard strip) — which it uses as the reference image: for zero-reference video models (Kling V3) the board feeds the IMAGE stage to design each start frame; for reference-capable models (Seedance, Veo, Kling O1) the board / its storyboard frames feed the video model directly as reference images. Drives the Wyren MCP — picks image/video models and resolutions, forces phone-camera realism on the start frames (so they don't look like stock/AI photos), generates multi-angle coverage so the edit can cut fast like real UGC, optimizes the TikTok first 5 seconds, and keeps character faces consistent across shots. Triggers on "make the video from this storyboard", "generate the short", "render the clips". Part of the arca-marketing-video kit.
---

# Video Prompt

Turn a 3×3 storyboard into a finished vertical short-form video. This skill drives the **Wyren MCP** — load the `wyren` skill before any `mcp__wyren__*` call. Pairs with `storyboard-prompt` (upstream) and `shorts-editor` (downstream edit).

## Brand profile (read first)
Read `../_arca-marketing-assets/brand.md` first and apply its name-usage, persona, logo rules, and colors. Brand assets live in `../_arca-marketing-assets/assets/` — feed `characters.png` (persona) and `logo.png` to the image/video models for consistency; use the supplied logo only, never invent or distort it. Swap `brand.md` + `assets/` to retarget to another brand.

## INTAKE — ASK FIRST
Before generating, ask for any of these not already provided, then wait for answers:
1. **STORYBOARD REFERENCE** — the image (+ shot notes). Note which of three forms: PHOTOGRAPHIC frames, a SCHEMATIC / annotated plan (panel numbers, notes boxes, mock UI), or a comprehensive PRODUCTION BOARD (character-reference turnaround + environment + floor plan + per-cut storyboard strip, from `storyboard-prompt`). See STORYBOARD INTERPRETATION + USING THE PRODUCTION BOARD AS A REFERENCE; the form changes how the video is built.
2. **VIDEO TYPE / STYLE** — UGC / phone-shot (default), cinematic / movie-trailer, animation, motion-graphics, product film, skit, etc. Match the storyboard's declared type. Drives the LOOK and the cold open. UGC → phone-shot styling applies; else → that type's craft.
3. **BRAND PROFILE** — attached/pasted `brand.md`.
4. **TARGET MARKET / AUDIENCE.**
5. **VIDEO SEGMENT** — FULL VIDEO / PART 1 / PART 2.
6. **TARGET DURATION** — default 15–20s; only exceed 20s if the user explicitly asks.
7. **IMAGE MODEL + RESOLUTION** — which model cleans/upscales storyboard frames into start frames, at what size. Default: Nanobanana Pro at 2K.
8. **VIDEO MODEL + RESOLUTION** — which model generates clips, at what resolution, which mode (std/pro). Default: Kling V3 at 720p.
9. **ASPECT RATIO** — default 9:16 vertical.
10. **NATIVE AUDIO** — whether the video model synthesizes dialogue/sound (some models only). Default: on if the model supports `sound`.

Only make smart, briefly-stated assumptions for what's still missing. If the user names a budget or "cheapest/fastest", pick the model tier accordingly and say which.

## SCRIPT & ORDER PRE-FLIGHT — vet the script BEFORE any generation (non-negotiable)
Generated clips are slow and expensive to redo, and you **cannot fix broken dialogue logic by re-cutting** — native audio bakes the words and delivery into each clip. So vet the script BEFORE building any Wyren graph. Take the dialogue + beats you received (the `storyboard-prompt` handoff, FLOW table, or the user's notes) and run this pass; if anything fails, rewrite the lines or reorder the beats NOW, then proceed.

- **Dialogue-only read (coherence).** Read just the spoken lines top-to-bottom, ignoring visuals. They must read as ONE coherent conversation: one through-line, each line *answers or escalates* the one before it, no non-sequiturs (a question gets answered), no contradictions (a claim isn't undercut by the next line). This mirrors `storyboard-prompt`'s dialogue-only pass — run it again here, because the handoff can still arrive incoherent and you are the LAST gate before spend.
- **Order check.** Confirm the beat order actually builds: hook first (the first clip carries the first-5s cold open), tension/escalation in the middle, payoff/punchline last. If a beat is out of place, reorder the SHOT LIST now (cheap) — never plan to "fix it in the edit" (impossible once clips are generated with baked-in audio).
- **Say it out loud (natural-dialogue test).** Read each line the way a real person would speak it. Rewrite anything stiff, written, robotic, on-the-nose, or over-explained. Real talk uses contractions, fragments, interruptions, filler ("I mean", "honestly", "wait"), and reactions; people don't narrate the obvious or recite exposition. Keep each speaker's voice consistent and distinct from the others.
- **Length vs duration budget.** Each line must fit its clip's seconds (~2–3 words/second; a 3s Kling shot ≈ 6–9 words). Trim lines that can't be said naturally in the beat's duration — rushed, crammed delivery reads as fake. If a beat truly needs more words, give it a longer clip or split it; never speed-talk to fit.
- **Lock the cast.** Before writing any shot prompt, list EVERY speaking character by NAME with their one-line bible (from the handoff). You'll paste each into the shots where they appear so the model always knows who is who and who is speaking.

Only after the script reads clean AND the order is right do you move to the model decision and graph build. If you changed any lines or the order, show the user the corrected shot list before spending.

## MODEL CAPABILITY MATRIX — decide in the FIRST intake round
The question that always surfaces late — "shouldn't the storyboard be a reference image for the video model?" — must be answered up front, because the answer changes the whole graph. Reconfirm live with `list_models` + `get_model_capabilities`, but the load-bearing facts:

| Model | Ref images | Native audio | Multishot | Start frame | Duration |
| --- | --- | --- | --- | --- | --- |
| **Kling V3** (default) | **0** (none) | yes (`sound`) | yes (≤6) | yes | 3–15s |
| Kling O1 | yes (≤7) | **no** | **no** | yes | — |
| Kling V2.6 | 0 | yes (+voice clone) | no | yes | 5/10s |
| Veo 3.1 Fast/Std | ≤3 | yes | no | yes | 4/6/8s |
| Seedance 2.0 / Fast | ≤4 | no | yes | yes | 4–15s (480/720p) |

- **Kling V3 takes ZERO reference images** (`maxReferenceImages: 0`). The storyboard does NOT feed the video model — it drives the IMAGE stage only (becomes/designs the start frame). Identity on V3 = per-shot **startFrame + the verbatim character bible** in each shot prompt, never a reference image.
- **Only Kling O1 accepts reference images** — but it LOSES native audio AND multishot. Choosing O1 for face-locking means giving up scripted dialogue + in-generation angle changes; usually not worth it. Prefer V3 (audio + multishot) with startFrame-driven identity.
- **Kling V3 Omni is disabled** — do not route to it.
- Net: dialogue UGC skit → default **Kling V3**, identity via startFrame + bible, audio native. Reach for a ref-image model (O1/Veo/Seedance) only when face-lock genuinely beats audio+multishot.

### DECISION RULE — multishot vs separate clips
- **Many quick dialogue beats + native audio → ONE Kling V3 multishot per part** (not many tiny separate clips). Multishot keeps face/voice continuous and gives angle changes in one generation.
- Watch the math: **Kling's minimum clip is 3s**, multishot maxes at 15s, so one multishot merge caps at **~5 beats** (5 × 3s = 15s). If a part has >5 dialogue beats, split into a second multishot/part rather than crushing beats below 3s.
- **Native audio nails the exact scripted lines** — for a dialogue skit you do NOT need a separate TTS pass. Write the real lines into each shot's prompt (the storyboard FLOW table's Dialogue column) and let the model speak them. Fall back to TTS/editor-added VO only when the model has no `sound`.

## STORYBOARD INTERPRETATION — PHOTOGRAPHIC vs SCHEMATIC
Use the storyboard as the PLAN, not as footage to copy. Detect which form you have before touching Wyren. If unsure, ask the user.

**A) PHOTOGRAPHIC frames** — each cell is a real/clean image of the actual scene (people, environment), like `storyboard-prompt`'s clean frame grid.
→ Crop each frame to 9:16 and clean/upscale it into a start frame (Step A), keeping the face, then use as the videoAI startFrame. The 1:1-friendly path.

**B) SCHEMATIC / ANNOTATED** — each panel is a rough PLAN: drawn phone bezel, webcam tiles, mock UI cards, labels, sticky notes, captions, and a notes box (SCENE / TIME / SHOT / ANGLE / MOVE / ACTION / DIALOGUE / AUDIO / TRANSITION / RETENTION / PHONE REALISM). The "AI Operator Interview" sheet is exactly this.
→ Treat strictly as a SHOT PLAN, never pixels. Do NOT upscale, reproduce panels 1:1, or render panel numbers, "Panel N" labels, notes boxes, drawn bezels, or rough mock graphics into the video. Instead REBUILD each beat:
  - Read the panel's SCENE / ACTION / SHOT / ANGLE / MOVE / DIALOGUE / AUDIO / TRANSITION / RETENTION as that shot's brief.
  - Generate LIVE FOOTAGE with Wyren (people, faces, desk, reactions, real environment, camera move) using the recurring character profile for face consistency and a fresh start frame DESIGNED for that shot via image AI — not the schematic panel.
  - Realize any on-screen UI / data / screens the panel shows (deck, dashboard, sticky notes, checklist, route map, "REC" indicator) as DIEGETIC parts of the scene — generated INSIDE the Wyren clip as the real laptop/phone screen, real paper, or real props, framed so the text is small/partial/blurred and need not render perfectly. Do NOT composite them as floating graphics.
  - Match each panel's layout and intent (what's on screen, what the person is doing), realized as real in-scene footage in the chosen VIDEO TYPE's look.

**WHO MAKES WHAT (schematic path):**
- Wyren videoAI → everything in-frame: people, faces, reactions, hands, environment, props, camera move, AND any on-screen UI / data / screens (diegetic in the clip).
- Wyren imageAI → designed start frames and any photographic plates feeding the clips.
- HyperFrames → reserved for the EDIT stage (`shorts-editor`): spoken-word captions, brand splash/end card, timing of zooms/SFX. Nothing else.

## USING THE PRODUCTION BOARD AS A REFERENCE
When the storyboard arrives as a comprehensive PRODUCTION BOARD (from `storyboard-prompt` — SHARED CHOICES header, CHARACTER REFERENCE turnaround + close-ups + wardrobe, ENVIRONMENT/SET + floor plan, STORYBOARD strip of per-cut frames, LIGHTING/MOOD notes), it is your master reference. It is a richer SCHEMATIC plan: read it as the brief, never reproduce its scaffolding (section headers, labels, swatches, floor plan, annotation strips) into the footage. Mine it as follows:
- **CHARACTER REFERENCE panel = the identity lock.** Crop the turnaround (front/side/back) + facial/side close-ups + wardrobe detail and use them as the character profile reference — you may SKIP generating a fresh profile (RECURRING CHARACTER CONSISTENCY Step 0) because the board already provides it. Still copy the character bible text from the breakdown into every shot prompt.
- **ENVIRONMENT + FLOOR PLAN = set + camera.** Use for set consistency and each cut's framing/movement (the numbered cut positions and arrows).
- **STORYBOARD strip cell = that beat's composition.** Use the cell as the target for that shot's start frame (lens/shot-size/move come from the cell's annotation / the breakdown's Shot-spec column).
- **SHARED CHOICES + LIGHTING/MOOD = the global look lock.** Repeat the palette + environment fingerprint + mood in every shot prompt so panels stay coherent.

### MODEL ROUTING — where the board is fed (driven by the capability matrix)
The board is a REFERENCE IMAGE, but WHERE it connects depends on whether the chosen video model accepts reference images:
- **Zero-reference video models (Kling V3 / V3 multishot / V2.6, `maxReferenceImages: 0`):** the board CANNOT go to the video model. Feed it to the **IMAGE stage** — pass the board (or the cropped CHARACTER REFERENCE panel + the relevant STORYBOARD cell) into `imageAI` as the reference to DESIGN each shot's start frame, then drive the clip with that `startFrame` + the verbatim bible. (This is the default Kling V3 path.)
- **Reference-capable video models (Seedance 2.0 ≤4, Veo 3.1 ≤3, Kling O1 ≤7):** feed the board / its STORYBOARD frames + CHARACTER REFERENCE **directly into the `videoAI` node as `referenceImages`** — the video model uses the storyboard as a direct visual reference. Still set a start frame when the model+mode supports one. (Mind each model's max ref count; if the board plus character refs exceed it, send the most load-bearing crops — character close-up + the target storyboard cell.)
- Either way, the board NEVER gets reproduced as on-screen graphics; it only conditions generation.

### DO NOT COMPOSITE TEXT/UI GRAPHICS (hard rule)
This (the video-generation) stage composites NO overlay onto the footage. Never recreate the storyboard's mock UI / data as floating overlays — no data/deck cards, dashboards, labels, callouts, checklists, route-map text, fake screens, or "REC"-style HUD text laid over the video. It looks fake and instantly kills the UGC feel. Any text or screen the viewer sees must be DIEGETIC (filmed/generated as a real screen or prop inside the Wyren clip) or simply dropped — if a panel's mock UI can't be made diegetic, simplify or omit it. All overlays are decided later by `shorts-editor` (spoken-word captions, brand splash, engagement chips/graphics) on the editor's terms — not generated or composited here.

### KLING FRAGILITY — morph guard + where dialogue lands
- **Kling warps fragile on-screen content and morphs objects.** It garbles readable UI/text (e.g. "Option A / B" labels turn to mush) and deforms objects mid-shot (a laptop literally rotating from its back, the lid becoming the screen). So don't give it readable UI or shape-critical objects to animate: keep screens **dim / out-of-focus / glare-washed**, snap the camera to faces, and **lock each object's shape + orientation explicitly** in the prompt. Add anti-morph negatives: *morphing screen, warping text, laptop flipping, lid becoming screen, deforming/melting object, unstable geometry.*
- **Native dialogue lands at the END of a generated clip**, and Kling pads the HEAD with filler / ad-libs. Plan the real line for the clip's back half, and tell `shorts-editor` to **transcribe before trimming** — a blind fixed-duration trim chops the actual line (see shorts-editor's AI-clip edge handling).

## VIDEO TYPE SCOPE
This skill makes ANY video type. The LOOK follows the chosen VIDEO TYPE; the TikTok retention rules (FIRST 5 SECONDS cold open, sound-off clarity, a fresh beat every 2–4s, continuity locks, brand rules) apply to EVERY type.
- **UGC / phone-shot (default):** final video must feel like "someone grabbed their phone and filmed this in the moment" — NOT a cinematic commercial, glossy AI video, polished brand film, stock footage, DSLR shoot, studio production, or high-end ad. The PHONE-SHOT VISUAL STYLE / CAMERA / FRAMING / LIGHTING / DEPTH OF FIELD / CHARACTER REALISM / ENVIRONMENT / MOTION / QUALITY-CONTROL sections below are in force; "choose realism / reinterpret as phone footage" applies.
- **Non-UGC (cinematic / movie-trailer, animation, product film, motion-graphics):** IGNORE the phone-shot styling sections and the "reinterpret as casual phone footage" instruction — render in that type's craft (e.g. trailer: cinematic lighting, fast cutting, scale). Still keep retention rules, continuity locks, brand/logo rules, and the first-5s cold open.

## CORE OUTPUT
Generate a finished vertical short-form video with:
- Aspect ratio: [default 9:16 vertical portrait]
- Resolution: [from chosen model; default 720p]
- Platform feel: TikTok / Instagram Reels / YouTube Shorts
- Visual style: realistic phone-shot UGC (or chosen type's craft)
- Camera style: handheld smartphone footage (UGC)
- Production level: low-cost, casual, creator-shot (UGC)
- Audio: native dialogue, voice, room tone, foley, SFX, risers, music — only if supported by the model
- Duration: [TARGET DURATION — default 15–20s unless the user asked for longer]
- Max per generation: model-dependent (typically 15s)

If the full video exceeds the model's max single-clip duration, split into multiple generated clips.

## PROJECT DIRECTORY (shared with `shorts-editor`)
All artifacts for one video live under a SINGLE project folder so the generate → edit handoff is clean and nothing scatters. Pick a kebab-case slug for the video and create it under the working dir:

```
<project-slug>/
  board/         # production board image + handoff.txt (from storyboard-prompt), if any
  startframes/   # per-shot start frames designed/cleaned by imageAI (frame-01.png …)
  clips/         # generated video clips (Wyren videoAI outputs): clip-01.mp4, part1.mp4 …  ← shorts-editor's input
  edit/          # shorts-editor working files (audio_clean.m4a, transcript.json, tight.mp4, composition/, frames/)
  out/           # final masters — the deliverables (<slug>-final.mp4)
```

Rules: confirm/announce the slug once, then keep everything inside that folder; never write outside it and never overwrite a source (derived files get new names); **`startframes/` + `clips/` are THIS skill's outputs and `shorts-editor`'s inputs**; `out/` holds only finished masters. This skill writes `startframes/` and `clips/`; it hands the `clips/` folder to `shorts-editor`.

## GENERATION SETTINGS (image + video models, resolutions)
This template runs alongside the Wyren MCP. Confirm settings with the user during intake, then drive Wyren. Always reconfirm live options with `list_models` + `get_model_capabilities` before building — the lists below are a current snapshot, not a contract (per-model resolution/duration/startFrame support changes).

### Step A — produce a start frame per shot (image model, `imageAI` node)
- **PHOTOGRAPHIC (path A):** crop each panel to 9:16, then upscale/clean into a usable first frame.
- **SCHEMATIC (path B):** do NOT upscale the panel. Use image AI to DESIGN a new start frame from the character profile + the panel's brief (scene, action, framing), so the frame is real-looking footage, not a redraw of the mockup. Any on-screen UI is realized diegetically inside the clip (real screen/prop), never composited.

**PHONE-CAMERA REALISM FOR START FRAMES (UGC types — non-negotiable).** The #1 failure mode is a start frame that looks like a polished STOCK PHOTO or AI render (soft studio light, model-perfect symmetric faces, plastic skin, centered staged composition, sterile clean room). The video model inherits the start frame's look, so a stock-looking frame produces a stock-looking clip. Fix it at the frame:
- Apply the SAME realism rules this skill specifies for footage — PHONE-SHOT VISUAL STYLE, CHARACTER REALISM, FRAMING, LIGHTING, DEPTH OF FIELD (below) — to the START FRAME. It's a paused still from that same casual phone video, NOT a separate photo shoot. Reuse: natural skin texture/pores/asymmetry, non-model casting, candid mid-action expression; mixed practical light, uneven exposure, blown-out window, mild noise; off-center imperfect handheld framing; normal phone depth of field, no creamy bokeh; real lived-in clutter.
- Add explicit phone-camera tokens to the image prompt: **"shot on an iPhone, candid vertical phone snapshot, amateur, mild phone HDR, slight grain, imperfect framing."**
- Always include a negative prompt: **stock photo, AI render, 3D render, glossy, airbrushed, retouched, model, supermodel, perfect skin, symmetrical, studio lighting, softbox, beauty lighting, creamy bokeh, shallow depth of field, hyperdetailed, 8k, cinematic, magazine, advertisement, clean, sterile, staged.**
- Applies whether upscaling a photo (A) or designing a fresh frame (B). If the source/look is already stock-ish (the common failure), explicitly **degrade it toward phone realism — grain, uneven light, candid expression, off-center framing — BEFORE generating the clip.** (NON-UGC: follow that type's craft; this phone-realism bar is for UGC.)
- **Keep the face.** When upscaling/cleaning, instruct the model to PRESERVE the existing person's identity — same face, hair, age, build, wardrobe — and only improve quality (sharpen, denoise, fix artifacts). Don't let it redraw or beautify into a different face. Use an image-edit-capable model (Nanobanana / Nanobanana Pro accept image input), pass the panel + character profile (+ `characters.png`) as references, with a prompt like "enhance and clean this frame, keep the exact same face and person, do not change identity." This face-preserving upscale is what makes per-shot start frames consistent across a multishot/multi-clip video.

**Image models (category "image"):** Nanobanana (Gemini 2.5 Flash Image, 1K, image input, default), Nanobanana Pro (Gemini 3 Pro Image, up to 4K, up to 14 reference images — best for keeping persona/logo consistent), Imagen 4 Fast/Standard/Ultra (text-only, 1K–2K, no image input). Sizes: 1K/2K/4K. Aspect ratios: 1:1, 4:3, 9:16, 16:9.
**Default:** Nanobanana Pro at 2K (image input + multi-reference locks character + logo). Pass `characters.png` and `logo.png` as reference images — the `logo.png` file is REQUIRED whenever the mark is visible, never a text description (the model fabricates a wrong logo otherwise; see BRAND & LOGO RULES).

### Step B — generate the clips (video model, `videoAI` node)
Video models (category "video") and key knobs:
- **Kling V3** (default) — 3–15s, 720p/1080p, std/pro, native audio (`sound`), multishot ≤6, startFrame. Good all-rounder; only model with a true 15s clip.
- **Kling V2.6** — 5s/10s, 720p/1080p, std/pro, native audio + voice cloning, startFrame.
- **Kling V2.5 Turbo** — 5s/10s, 720p/1080p; start/end frames only in PRO mode (1080p).
- **Veo 3.1 Fast/Standard** (Google) — 4/6/8s, 720p/1080p/4K, built-in audio, up to 3 reference images.
- **Seedance 2.0 / 2.0 Fast** (ByteDance) — 4–15s, 480p/720p only; Fast is ~3× faster, ~5× cheaper. Pick Seedance when the user wants the grainier low-res 480p phone look or the cheapest path.

Resolutions: 480p (Seedance only), 720p, 1080p, 4K (Veo only). Default 720p for UGC. Mode: use `pro` when relying on start/end frames; `std` is cheaper. Native audio: enable on `sound`-capable models (Kling V3, V2.6, Veo); else leave dialogue/SFX for `shorts-editor`. startFrame: confirm via `get_model_capabilities` that the chosen model+mode+resolution actually accepts a start frame before wiring `imageAI → videoAI`; if not, pick another model/mode or go text-only.

### Wyren execution flow (load the wyren skill first)
1. `list_models` + `get_model_capabilities` to lock the exact image/video model, resolution, mode, duration.
2. `build_graph`: `imageInput` (start-frame source, characters.png, logo.png, AND the production board / its cropped character-reference + storyboard cell if you have one) → `imageAI` (A: clean/upscale photo panel; B: design fresh start frame from the board reference) → `videoAI` (chosen model/resolution/mode/duration). **Route the board per MODEL ROUTING:** zero-ref models (Kling V3) → board into `imageAI` only; reference-capable models (Seedance/Veo/O1) → also wire the board / storyboard frames into `videoAI` as `referenceImages`. Use multishot or per-clip nodes per the split rule.
3. `validate_workflow` — resolve warnings with the user.
4. Estimate cost: `get_pricing` (chain mode) / `estimate_product_cost`; get the user's OK to spend.
5. `run_workflow` (`userConfirmed: true`), then poll for completion. **`get_workflow_run_status` lags badly** — it can still show `pending` ~10 min after a job already succeeded, so treat **`get_node_outputs` as the source of truth** for whether a node is done, not the run status. There is a single video worker, so `run_node` jobs queue and run ~sequentially; `cancel_job` is wedge-risky, so let redundant jobs finish rather than cancel.
6. Pull clips with `get_node_outputs` and SAVE into the project dir: clips → `<project-slug>/clips/` (`clip-01.mp4`, `part1.mp4` …), and any designed/cleaned start frames → `<project-slug>/startframes/`. On-screen UI/data/screens were generated DIEGETICALLY inside the clips — no text-overlay pass here.
7. EDIT & FINISH — hand the `<project-slug>/clips/` folder to `shorts-editor`: fast-cut assembly, spoken-word CAPTIONS, brand splash/end card, zoom/SFX timing, master into `<project-slug>/out/`. That is the ONLY place HyperFrames is used, and only for captions + splash + timing — never to composite text/UI graphics onto the footage.

### WYREN BUILD GOTCHAS (these cost failed validate/run calls)
- **`multiPrompt` must be a JSON STRING, not an array.** For multishot, pass per-shot prompts as a stringified JSON value (e.g. `"[{...},{...}]"`), not a raw array. A raw array fails validation.
- **`imageAI` / `videoAI` need a CONNECTED TEXT EDGE — `customPrompt` alone fails.** Wire a text/prompt node into the AI node's prompt input; a `customPrompt` field set without an incoming text edge does not satisfy validation. Build the graph so every imageAI/videoAI has its prompt edge connected, then set the prompt content. (`imageInput` data shape is `{imageUrls:[url]}`; `videoAI.text` needs a connected `textInput` edge.)
- **`run_workflow` re-runs ALL nodes.** To regenerate just a few nodes (a reshot clip, a fixed frame) WITHOUT clobbering already-approved outputs, call **`run_node` per node** instead of re-running the whole workflow.

## RECURRING CHARACTER CONSISTENCY (multishot / multi-clip)
Any time the video is more than one shot — a multi-clip split (Part 1/Part 2) or video-model multishot (Kling V3 ≤6 shots) — the same person must look identical in every shot. Faces, hair, build, age, wardrobe drift badly across independent generations. Lock identity FIRST, for each recurring character (e.g. the Arca Navigator).

**Step 0 — secure a character profile BEFORE any shot:**
1. **If the storyboard is a PRODUCTION BOARD, you already have the profile** — crop its CHARACTER REFERENCE panel (front/side/back turnaround + facial/side close-ups + wardrobe detail) and use that as the reference; skip regenerating. Otherwise generate a character profile / face reference with **Nanobanana Pro** (≤14 reference images, up to 4K) seeded with `characters.png` + the persona description from `brand.md`. Produce a clean reference: front face + 3/4 face (+ head-to-waist) of the SAME person — consistent face, hair, skin, age, build, wardrobe — in the casual phone-UGC look (natural skin texture, real lighting), NOT glamour/studio. One profile image per recurring character.
2. Write a short **character bible** in words: face shape, skin tone, hair (color/length/style), age, build, wardrobe, 1–2 distinguishing features. Keep it tight. Paste it **verbatim into every shot's prompt** so the text description never drifts.

**Then for EACH shot / clip:**
- Use the profile image as the shot's **startFrame** whenever the action allows — the first frame anchors identity for the whole clip. For mid-action shots, first generate that shot's start frame from the profile via image AI (Nanobanana Pro with the profile as reference), then feed it as the startFrame so the face is locked before any motion.
- If the model accepts **referenceImages**, pass the profile as a reference too: Veo 3.1 (≤3), Kling O1 (≤7), Seedance 2.0 (≤4). Note: **Kling V3 / V3 multishot does NOT accept reference images** (`maxReferenceImages: 0`) — there, identity = per-shot startFrame + the verbatim character bible in each shot's prompt.
- Repeat the exact character bible text in every shot prompt; never paraphrase between shots.
- Keep the CONTINUITY LOCKS (same face, hair, wardrobe, props, setting, lighting) in force.

If two characters recur, build a separate profile + bible for each, and keep both references wired into every shot where they appear.

**SECONDARY & BACKGROUND characters drift worst.** Per-shot generation only locks the START-FRAME subject; everyone else — the second person in a two-hander, recurring side characters, background extras — gets reinvented (face AND wardrobe) every shot. Don't rely on the bible text alone for them:
- **Pin each recurring secondary character's wardrobe explicitly** in every shot prompt, not just the lead's (e.g. "the man in the grey zip hoodie and black cap"). Vague secondary descriptions are where the model improvises a new person.
- **Chain that character's best generated frame back in as a reference** into their later shots: once a shot renders them well, feed that frame to `imageAI` as a reference when designing their next start frame. The image input carries multiple reference URLs, so wire BOTH characters' references in for any shot where both appear.
- **Push extras out of focus.** Keep background people incidental, turned away, blurred, or cropped — never ask the model to hold a face it doesn't need to. An extra the viewer can't study can't visibly drift.

## DEFAULT SPLIT RULE
**The default 15–20s video is usually ONE part** — a single Kling V3 multishot (up to 15s) plus a short final clip if needed. Only SPLIT into two parts when the user explicitly asked for a LONGER video (>~20s). When you do split: **Part 1 = Panels 1–5; Part 2 = Panels 6–9.** Each part feels like one continuous video. Part 2 continues the same character, wardrobe, props, lighting, setting, camera quality, and emotional energy — do not restart the story, do not recap. Never show the storyboard grid, panel numbers, production notes, borders, arrows, labels, or annotations. Convert panels into real-feeling vertical footage.

## INPUTS
- Storyboard reference: [ATTACH 3×3 STORYBOARD IMAGE]
- Storyboard breakdown / shot notes: [PASTE BREAKDOWN]
- Brand: [BRAND NAME — see `brand.md`]
- Brand profile: [ATTACH/PASTE `brand.md` — name, logo rules, persona, colors]
- Logo asset: use the supplied brand logo only if available
- Video segment: [FULL VIDEO / PART 1 / PART 2]
- Target duration: [DURATION]
- Primary audience: [TARGET AUDIENCE — the market/niche implied by the storyboard; see brand profile]

## PRIORITY ORDER
1. Preserve the 9 storyboard beats in order.
2. Preserve story logic and emotional progression.
3. Preserve same characters, wardrobe, props, setting, lighting.
4. Preserve the strongest visual intent from each panel.
5. Make every shot feel like real phone footage.
6. Keep the video fast, clear, human, retention-focused.
7. Keep the brand subtle and natural if the logo appears.
8. Avoid cinematic, commercial, glossy, or AI-polished visuals.

If storyboard vs realism conflict → choose realism. If the storyboard looks too polished/cinematic, reinterpret as casual phone-shot footage while keeping the same story beat.

## SHOT ORDER (9 panels, left→right, top→bottom)
1. Scroll-stopping hook · 2. Immediate context · 3. Subject/problem intro · 4. First key action/escalation · 5. Tension, contradiction, or reveal · 6. Transformation/solution/emotional shift · 7. Strongest visual payoff/climax · 8. Resolution/result · 9. CTA, loop, final punchline, or memorable closing shot.

Don't add unrelated shots, reorder beats, skip the payoff, or make the first shot slow. The first shot must immediately show something visually interesting, awkward, funny, tense, surprising, emotionally specific, or easy to understand.

## TIKTOK FIRST 5 SECONDS — COLD OPEN (every video type)
TikTok decides in ~5s whether to keep serving, so the opening clip is the single highest-leverage generation. Front-load it regardless of style — most formats (trailers, vlogs, ads) traditionally open slow; override that here. Panel 1 (into 2) carries this; if the storyboard opens slow, recut so the strongest beat is first.

**5-second micro-arc (any format):**
- **0.0–1.0s — pattern interrupt:** most arresting shot/motion/sound you can generate. No logos, no slow establishing shot, no greeting, no black-screen build-up.
- **1.0–3.0s — the promise:** clear sound-off who it's for and why to keep watching (stakes, question, teased payoff).
- **3.0–5.0s — escalate:** a second distinct beat (cut, reveal, line, raise) so the open isn't one held shot; land a mini-hit right before 5s.

**Adapt to VIDEO TYPE (same goal, different execution):**
- Cinematic/trailer → most action-packed, highest-stakes shot (cold-open set-piece or climax tease), fast cuts, hard hook line / on-screen stakes; no slow atmospheric/logo build, save the title card for later.
- UGC/talking-head → open mid-thought on a bold spoken HOOK STATEMENT (claim, contrarian take, callout, question), face in frame; no greeting.
- Vlog → in medias res at the peak moment, not "good morning."
- Tutorial/how-to → show the finished RESULT/payoff first, then promise the steps.
- Product/brand ad → lead with the visceral problem or the transformation, never the logo first.
- Story/skit → open inside the conflict, mid-scene.
- Listicle → number + payoff promise first line, then jump to #1.
- Reaction/commentary → lead with the most outrageous clip/claim.
- Meme/comedy → hit the funniest visual or high-tension setup immediately.

When you split (Part 1/Part 2 or multishot), the very first clip MUST deliver this cold open; spend extra prompt detail and the better model/resolution on it. First 5s must read sound-off and promise a payoff the video delivers. If the style's normal opening is slow, the cold open wins.

## RETENTION & PACING
- First 1s: visual interruption · First 3s: clear reason to keep watching · Every 2–4s: new visual/emotional beat · Middle: escalation, reveal, action, reaction, or transformation · Final: payoff, punchline, result, or loop · End quickly after the payoff.
- **Avoid:** slow setup, greetings, logo-first openings, long pauses, over-explaining, generic establishing shots, slow cinematic movement, dead air, endings that drag.
- Every shot must answer: "Why would someone keep watching right now?"

## FAST CUTS & MULTI-ANGLE COVERAGE (the UGC editing engine)
A single continuous clip per beat reads as a slow AI ad. Real engaging UGC is CUT FAST and constantly SWITCHES ANGLE and shot size. This operationalizes "new beat every 2–4s" for GENERATION and **overrides the one-shot-per-panel default**: a storyboard panel is a BEAT — usually several shots, not one clip. You cannot cut between angles you never generated.
- Cut roughly every 1–2.5s. No talking shot holds longer than ~3s without a cut, angle change, or reframe. The whole video should feel like many short shots, not a few long ones.
- Cover each beat from MULTIPLE angles/shot sizes, then cut between them. Generate 2–3 variations per beat from the FRAMING + CAMERA set: wide/establishing → medium close-up → tight close-up → over-the-shoulder → desk-level POV → reaction insert. Vary framing on EVERY cut (never two same-size shots back to back).
- Use the model's multishot where available (Kling V3 ≤6 shots) to get angle changes inside one generation; otherwise generate several short clips per beat with different framings and assemble.
- Intercut B-roll / insert shots between talking shots — hands on keyboard, the screen, paper packet, a face reaction, an object. Inserts let you cut on every sentence and hide jumps.
- Punctuate with the TRANSITIONS vocabulary (jump cuts, reaction cuts, quick whip-pans, match cuts, camera repositioning) and snap zooms / handheld punch-ins — never slow dissolves or cinematic moves.
- Keep continuity locked across angle changes (same person/face, wardrobe, set, lighting) via the character profile — fast cuts must not become a different person.
- Actual cutting/assembly is finished in `shorts-editor`: generate enough angle coverage here so that stage can cut fast. Hand it one long clip per beat and it cannot.

---

## UGC CRAFT (skip for non-UGC types — render in that type's craft, but keep cold open, retention, continuity, brand rules)

**PHONE-SHOT VISUAL STYLE** — casual iPhone/smartphone video (could be non-iPhone if the concept demands, e.g. cartoons). Use: vertical handheld framing, slight camera shake, micro-wobbles, imperfect/slightly off-center framing, casual creator blocking, practical real-world lighting, visible background detail, mild phone-camera softness, mild compression, mild autofocus imperfections (occasional tiny focus hunting only if natural), mild exposure imperfections, slight motion blur during movement, natural skin texture, visible pores/imperfections, imperfect hair, wrinkled casual clothing, slightly awkward posture, candid expressions, believable body language, real-world clutter (coffee cups, papers, cables, bags, laptops, notebooks, fingerprints, sticky notes, scuffed desks, messy surfaces, imperfect rooms). Clear enough to understand, not polished. Native to TikTok/Reels/Shorts, not an ad.

**CAMERA RULES** — simple creator phone behavior. Preferred: handheld push-in, quick casual pan, slight handheld zoom, desk-level POV, over-the-shoulder phone angle, quick whip pan, jump cut, reaction cut, awkward close-up, quick repositioning, natural handheld walking/leaning if needed. Avoid: gimbal, dolly, slider, crane, drone, Steadicam, smooth commercial tracking, cinematic push-ins, rack focus, telephoto compression, perfect stabilization, choreographed blocking. Feel like a real person holding a phone.

**FRAMING RULES** — native short-form framing. Prefer: close-ups, medium close-ups, POV, over-the-shoulder, desk-level, awkward-but-readable, visible background context, fast reaction shots, simple action per shot, UI-safe composition. Keep important faces/actions away from extreme edges. Avoid: cinematic wide establishing shots, perfect hero framing, symmetrical luxury-ad composition, perfectly centered commercial shots, beauty-shot framing, shots that feel crew-staged.

**LIGHTING RULES** — available practical lighting: office fluorescents, overhead lights, window/desk-lamp/home/hallway/cafe/street light, natural daylight, mixed real-world light. Allow: uneven shadows, mild under/overexposure, imperfect white balance, mixed color temperatures, slightly harsh overhead light, normal real-world flaws. Avoid: studio/beauty/cinematic key light, strong rim light, dramatic shadow patterns, perfect softbox, moody commercial, glossy ad lighting.

**DEPTH OF FIELD** — don't make background too blurry; use normal smartphone DoF; the viewer should still understand where the scene is. Avoid: creamy bokeh, DSLR/cinema-lens blur, extreme subject separation, rack focus, artificial background blur, perfect focus pulls.

**CHARACTER REALISM** — real people captured casually on a phone. Use: natural skin texture, normal facial asymmetry, small imperfections, realistic hands, imperfect hair, casual/wrinkled clothes, natural fatigue/surprise/stress/confusion/relief/awkwardness/excitement, candid expressions, imperfect posture, human hesitation, believable timing. Avoid: model-perfect/airbrushed/plastic faces, AI-smooth or warped hands, perfect smiles every shot, mannequin acting, glamor lighting, stock-photo casting, changing faces/body shape/hair/clothes/age between shots. Caught in the moment, not cast for a commercial.

**ENVIRONMENT** — real, lived-in, imperfect: visible background detail, real props, slightly messy desks, clutter, coffee cups, bags, cables, papers, laptops, notebooks, sticky notes, scuffed surfaces, imperfect furniture, casual spaces. Avoid: spotless studio sets, showroom offices, empty perfect rooms, fake AI environments, luxury commercial spaces, production-designed backgrounds, randomly changing backgrounds, unrealistic cleanliness. Setting stays consistent across the full video.

**MOTION REALISM** — all motion physically believable: natural body movement, realistic hand gestures, believable object interaction, casual walking/leaning/sitting/turning/picking up/putting down, real and imperfect reaction timing, realistic motion blur. Avoid: floating objects, rubbery faces, warped hands, flickering props, unstable object shapes, impossible hand positions, unnatural facial animation, mannequin movement, overly smooth AI motion, teleporting props, changing screen layouts. Keep actions simple enough for reliable generation.

**LOW-COST GENERATION** — easy to generate and film. Prefer: one main location, 1–2 main characters, simple props, clear actions, close-ups, reaction shots, natural cuts, minimal screen text, simple body movement, practical lighting. Avoid: crowds, complex choreography, detailed handwriting, fast hand manipulation, small unreadable screens, multiple changing locations, complex props, complex branded objects, reflections that must be perfect, long continuous action sequences, anything requiring exact text rendering. Goal: believable short-form clarity, not complexity.

**TRANSITIONS** — simple creator-style. Preferred: hard cuts, jump cuts, reaction cuts, quick phone pans, casual whip pans, match cuts, camera repositioning, movement cuts. Avoid: slow dissolves, glossy wipes, cinematic transitions, flashy motion graphics, music-video transitions, commercial edit effects.

## CONTINUITY LOCKS (all types)
Keep consistent across all shots: same character identity, face, hairstyle, wardrobe, props, setting, background layout, time of day, lighting direction, camera quality, visual mood, brand/logo placement if applicable. Avoid: characters changing appearance, clothes changing between shots, props appearing/disappearing randomly, background rearranging, lighting changing dramatically, faces morphing, hands deforming, screens flickering unnaturally, objects warping, impossible physical movement. If a prop is important in one shot, preserve it later unless the action removes it.

## TEXT RULES
Do not add generated overlay captions unless explicitly requested. Avoid: subtitles, floating captions, big title cards, CTA banners, meme text, fake UI graphics, labels, arrows, watermark-style branding, copied storyboard annotations, complicated handwriting, detailed small text. Text may appear only if physically part of the scene: phone/laptop screen, whiteboard, paper, notebook, shirt, tote bag, mug, sticker, packaging, real sign, printed document. Keep physical text simple, large, minimal. If text is likely to render poorly, make it blurred/partial or avoid it. Captions and subtitles are added later in editing.

## BRAND & LOGO RULES
If a brand is included: use the supplied logo only if available, as a natural physical prop. Good placements: laptop sticker, tote bag, mug, notebook, badge, desk object, small office poster. Keep it subtle but recognizable, only where it naturally belongs. Do not: make it the focus, use it as an overlay/watermark, make it giant, force it into every shot, or invent a fake/distorted logo. If exact reproduction isn't possible, use a plain prop and avoid fake logo distortion. The video should feel like native content that happens to include the brand, not a brand ad.

**NEVER trust the image model to draw the mark.** From a text description alone, image models fabricate the logo — wrong wordmark, invented icon — every time. **Attach the actual `../_arca-marketing-assets/assets/logo.png` file to every `imageAI` node that should show the mark** (the start-frame stage is where the logo gets baked in). If the model still can't reproduce it cleanly, leave a plain unbranded prop and add the real logo later in the edit (`shorts-editor`) — never let the model invent one.

## AUDIO DIRECTION
Generate native audio if supported; it should feel like real creator-shot social video. Use: natural room tone, phone-mic ambience, casual dialogue, natural VO if the storyboard calls for it, imperfect human delivery, tiny pauses, keyboard taps, chair squeaks, paper sounds, phone buzzes, footsteps, desk sounds, bag rustles, small reaction sounds, subtle whoosh/riser only when helpful, light music only if it supports pacing. Native to TikTok/Reels, not cinematic. Avoid: trailer/orchestral music, dramatic swells, glossy commercial music, overproduced sound design, fake epic SFX, booming risers, ad-like or perfect-studio VO. Dialogue casual, slightly imperfect, human. If the model can't generate clean dialogue, prioritize realistic visual storytelling and leave dialogue/captions for editing.

**Audio mix (esp. narrated / trailer formats):** use **native Kling dialogue for character lines**, a **separate, consistent narrator VO** track when there's narration (don't let Kling re-voice the narrator per clip — it drifts), and **native foley everywhere**. Keep **dialogue clearly audible over music** — the editor will balance levels, but write/generate so speech sits on top. For trailer/hype energy (non-UGC), pace it punchy: fast whip-pans and snap-zooms, ~3s shots, high intensity — not slow cinematic drift.

## SHOT-BY-SHOT EXECUTION
Each panel is a BEAT — realize it as several short shots from different angles, not one held clip (see FAST CUTS). Per panel: preserve the main action, emotional beat, character placement when possible, important props, and environment; make it feel like real phone footage; make the action understandable without text; keep it short and purposeful; move the story forward quickly. Panel 1 = strongest scroll-stopping moment. Panel 7 = strongest visual payoff/climax. Panel 9 = punchline, loop, CTA, or memorable final image. Don't let the ending drag. Speak the EXACT lines from the vetted script (SCRIPT & ORDER PRE-FLIGHT) — any dialogue improvement happens THERE and gets re-vetted, not silently per shot, so the same words and order ship every time. You may still refine timing, micro-actions, transitions, and audio as long as the script, story order, and visual anchor stay intact.

### PER-SHOT PROMPT ANATOMY (write every shot this explicitly)
Vague shot prompts are why faces drift and dialogue lands flat. Every shot prompt — each entry in a multishot `multiPrompt`, AND each single clip — must spell out, in order:
1. **WHO is in frame + WHO speaks.** Name the character ("Maya, the Navigator") and paste their verbatim bible (face / hair / age / build / wardrobe) so identity never drifts. If two people are in frame, name BOTH and say who is speaking vs listening.
2. **The LINE, verbatim, in quotes** — the exact words from the vetted script: `says: "…"`. Silent beat → write `(no dialogue)`. Native audio speaks exactly what you write, so write the final words, never a paraphrase or a "talks about X" summary.
3. **DELIVERY / EMOTION** — how it's said: tone + emotion + pace + any non-verbal (e.g. "deadpan, then a small smirk"; "rushed and anxious, glancing off-camera"; "warm, almost a whisper"; "laughs mid-sentence"). This is what makes the read sound human — NEVER omit it.
4. **WHO they speak TO + blocking** — to camera, to the other character, or to themselves; where each person stands and faces.
5. **ACTION** — the one clear physical action in the beat (typing, sliding a phone across the desk, leaning back).
6. **FRAMING + CAMERA** — shot size, angle, movement (from the storyboard shot spec; vary it on every cut per FAST CUTS).
7. **CONTINUITY LOCKS** — same setting / wardrobe / props / lighting as the surrounding shots; plus the UGC phone-realism tokens.

**Template for one shot:**
> [CHARACTER NAME + verbatim bible]. [Framing / angle / movement]. [Setting + continuity locks]. [Action]. Speaking [to whom], they say: "[exact line]" — delivery: [emotion / tone / pace + any non-verbal]. [Phone-realism tokens for UGC.]

For a **multishot**, build the `multiPrompt` as one such block per shot, in order, each naming its speaker, exact line, and delivery — so the model keeps the right person saying the right line with the right emotion across every shot in the generation. (`multiPrompt` is a JSON STRING, not an array — see WYREN BUILD GOTCHAS.)

## SEGMENT-SPECIFIC INSTRUCTIONS
- **FULL VIDEO:** all 9 panels in order; total at or below 15s if the model limit requires; compress beats but never remove the hook or payoff.
- **PART 1:** Panels 1–5 only; end on tension, contradiction, reveal, or open loop; no final payoff; maintain momentum for Part 2.
- **PART 2:** Panels 6–9 only; continue directly from Part 1 with the same characters, props, wardrobe, setting, lighting, camera feel; don't restart or recap; deliver the transformation, payoff, resolution, and final beat.

## QUALITY CONTROL BEFORE FINAL OUTPUT (UGC)
Check every shot. Reject and revise any shot that feels too cinematic, glossy, polished, symmetrical, perfectly lit, heavily blurred, too sharp, too high-resolution, airbrushed, or too much like stock footage / a commercial / corporate video / AI-generated video / movie scene / DSLR-or-cinema shoot / luxury campaign. Every shot must pass: **Could a real creator plausibly film this on an iPhone in one or two takes without a crew?** If no, make it simpler, messier, closer, flatter, more awkward, more handheld, more naturally lit, less composed, less perfect, less cinematic, more human, more phone-native.

## FINAL RESULT
A finished creator-shot version of the storyboard. Preserve: same story beats, shot order, characters, wardrobe, setting, props, mood, emotional progression, visual intent. Should look/feel like: real vertical iPhone footage, casual UGC, native TikTok/Reels/Shorts content, believable creator-shot footage — imperfect but clear, human and specific, fast and engaging, filmable tomorrow on a phone. Should NOT look like: a cinematic commercial, AI-generated stock footage, glossy brand film, polished corporate ad, DSLR shoot, studio production, music video, movie scene, or luxury campaign. The goal is not "cinematic" — the goal is **believable, native, human, fast, slightly messy, low-cost, and filmed on a phone.**
