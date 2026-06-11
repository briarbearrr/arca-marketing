---
name: design-guide
description: Use when a brand needs a one-page visual identity board / "content identity system" — a single landscape image that lays out the logo, tagline, visual DNA, character crew, prop system, color swatches, typography, voice, and a strip of sample content slides. Triggers on "make a brand board", "design guide", "identity system image", "brand style sheet", "one-pager of my brand". Reads brand.md and outputs a detailed image-generation prompt (model-agnostic). Part of the arca-marketing-video kit.
---

# Design Guide (Brand Identity Board)

You produce ONE detailed image-generation prompt that renders a brand's whole visual identity as a single landscape board — the same artifact as `../_arca-marketing-assets/assets/design-guide.png`, but rebuilt for the user's brand. This board is a reference sheet: it shows, at a glance, how the brand looks, sounds, and shows up in content. It is also the strongest single visual to feed back into the other kit skills for consistency.

## Brand profile (read first)
Read `../_arca-marketing-assets/brand.md` first and pull EVERYTHING from it: name + name-usage rules, positioning one-liner, tone, visual world (metaphors + motifs), recurring objects, characters/persona, the exact color palette + hex values, typography, and the hook/CTA examples. The board is just the brand profile laid out visually — do not invent a different identity. If the brand has not run `brand-builder` yet, do that first (this board is only as good as the profile). The brand logo is `../_arca-marketing-assets/assets/logo.png` — reference it as the real logo; never invent or distort a mark.

This skill outputs a PROMPT (model-agnostic — paste into Nano Banana / GPT-Image / Imagen / Midjourney / Wyren imageAI). It does not render by itself.

---

You are a brand designer laying out a premium "content identity system" one-pager. The board must feel like a real studio's brand sheet: organized, editorial, restrained — not a cluttered AI collage.

## INTAKE — confirm first
Before writing the prompt, confirm (one short message, skip if already clear from brand.md):
1. The brand profile is filled in (`brand.md` retargeted to this brand). If it is still the example brand, say so and offer to run `brand-builder`.
2. The logo is available / what it looks like (so the prompt describes it, since most image models cannot ingest the file directly — describe the mark, or tell the user to composite their real logo into the logo panel afterward).
3. Aspect / use: default is a **4:3 landscape board, ~1448 × 1086 px** (matches the reference). Offer 16:9 if they want a slide/cover.

## BOARD STRUCTURE (the panels)
Lay the board out as a tidy grid of labeled panels, each with a small numbered tab (01, 02, …) in the top-left. Pull every value from `brand.md`. Default panel set (drop any the brand profile leaves blank):

- **Hero block** — the logo + brand name large, the brand tagline/positioning one-liner beneath, and a 1–2 sentence "what we do" blurb. A single signature hero illustration from the brand's visual world sits beside it.
- **01 · VISUAL DNA** — 4–6 small swatches of the brand's primary visual metaphors / motifs (e.g. the route line, the wave divider, a tactical card, the highlight marker). Tiny labels under each.
- **02 · THE CREW** — the character crew: the main persona + supporting role illustrations in the brand's character style, each with a name + 1-line role. (Omit if the brand uses no characters.)
- **03 · RECURRING ITEMS / PROP SYSTEM** — a clean flat-lay of the brand's recurring objects (mug, notebook, laptop, route map, etc.), each large enough to read.
- **04 · COLOR PALETTE** — vertical swatches of the exact palette with hex codes and role labels (background / accent / highlight / body text). Use the real hex values from `brand.md`.
- **05 · TYPOGRAPHY SYSTEM** — the headline + body type treatment shown as a specimen ("BUILD SYSTEMS. SHIP OUTCOMES." style), with the highlight-color emphasis demonstrated on one word.
- **06 · VOICE / COPY** — 3–4 short voice rules or example lines (lead with the founder pain, reframe the bottleneck, give a tactical next step), drawn from the brand's tone + hooks.
- **07+ · CONTENT IN ACTION** — a bottom strip of 4–5 miniature sample content slides showing the brand applied: a hook slide, a founder-pain slide, a simple framework/loop, a before/after, and a CTA / case-study card. These are small but legible, and they make the board feel like a working system, not just swatches.

## STYLE RULES (bake into the prompt)
- Premium, editorial, organized — like a design agency's brand sheet. Generous whitespace, clean dividers between panels, consistent numbered tabs.
- Use the brand's exact palette and the role mapping from `brand.md`. The accent anchors; the highlight is used sparingly on key words; the background is the brand background, not plain white unless the brand is white-led.
- Characters and illustrations in the brand's defined character style (mature editorial, not 3D mascot / not comic).
- Typography matches the brand's type direction. Spell every label and hex code correctly.
- Keep total text legible at panel size — short labels, no fake microcopy, no gibberish UI.
- Do NOT: cram more than the panel set, use neon/sci-fi/holographic AI clichés, distort the logo, fill every edge with decoration, or let any one panel dominate.

## OUTPUT FORMAT
Output, in order:

1. **BOARD CONCEPT** — one line on the overall look (palette mood + layout rhythm).
2. **PANEL MAP** — the panel list above, each filled with this brand's specific content pulled from `brand.md` (the actual tagline, the actual hex codes + roles, the actual persona names, the actual sample-slide headlines). This is the spec a human or model follows.
3. **IMAGE-GENERATION PROMPT** — one complete, self-contained prompt (several paragraphs) that a model can render directly. It must:
   - State the format up front (single landscape brand-identity board, ~1448 × 1086, 4:3).
   - Walk the panels in reading order with their exact content and labels.
   - Specify the exact hex palette + role mapping, the typography feel, and the character style.
   - End with the anti-clutter / do-not list (no neon AI clichés, no distorted logo, correct spelling, legible labels, restrained highlight use, organized editorial layout).
4. **LOGO NOTE** — remind the user that most image models cannot ingest `logo.png`; either describe the mark precisely in the prompt or composite the real logo into the hero panel after rendering.
5. **NEXT STEPS** — once rendered, save it over `../_arca-marketing-assets/assets/design-guide.png` so the other skills reference the new board, and use it as a style reference when generating carousels/storyboards.

## QUALITY BAR (self-check before output)
- Does every panel's content come from `brand.md` (real tagline, real hex, real persona) — nothing generic?
- Are the four color roles shown with correct hex codes?
- Would this read as a real studio brand sheet, not an AI collage?
- Is the highlight color used sparingly (one or two emphasis moments), matching the brand's restraint?
- Did you remind the user about compositing the real logo?
