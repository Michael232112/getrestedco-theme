# PT 2 Image Pipeline — Rested

Generated 7 PDP images via KieAI Nano Banana PRO (Gemini 3 Flash Image, 2K).
Executed 2026-04-24/25 by @Michael232112 + Claude.

## Workflow
1. Pricing reconciled: variants $115 / compareAt $229 (from Mukul's copy anchor).
2. Shot 1 = avatar + device DNA lock (panda colorway CINCOM ref).
3. Shots 2–7 inherited Shot 1 as character reference via multi-reference input.
4. All shots: 2K, iPhone-quality guardrails, no burned-in text.

## Live on Shopify product media (5 hero carousel shots)
- Shot 1 — avatar relief @ kitchen counter (1:1)
- Shot 2 — hands-on-product close-up (1:1)
- Shot 3 — 2 AM pain anchor, no device (1:1)
- Shot 4 — authority desk (1:1)
- Shot 5 — dusk released, sage sweater (4:5)

## Staged in this repo (awaiting theme section wiring)
- assets/rested-recovery-ritual-hero.jpg (16:9) — for "Recovery Ritual" section
- assets/rested-timeline-grounding.jpg (16:9) — for 4-phase timeline section

These two need `shopify theme push --only assets/` + section JSON references in
templates/product.json or templates/index.json once Mukul's copy lands and we
know which section blocks to wire them into. They're version-controlled here
so anyone picking up section work has the assets ready.

## Avatar spec (for future shots / this series continuity)
Woman, age 52, light-olive Mediterranean skin with natural pores, shoulder-length
hair with silver streaks at temples (not dyed). Domestic settings only. Warm flat
natural light. Expressions span quiet relief → soft knowing → honest weariness —
never hyped, never toothy.

## Reusable prompt frame
```
iPhone 15 Pro photo quality. Natural skin pores, visible hand texture, flat
diffused window light, no ring light, no studio bokeh, no beauty retouching,
photojournalistic, authentic domestic scene.

Using reference image 1 as the exact character reference — same woman [...] —
and reference image 2 as the exact product reference (white top with black side
leather-textured panel, panda two-tone; no pink, no magenta, no burgundy).

[SCENE DESCRIPTION]

Composition: [ASPECT, FRAME]. Absolutely no text, logos, watermarks,
branding, or typography anywhere in the image or on the device.
```

## Credit usage
- Shot 1 v1 (discarded): 12
- Shot 1 v2 (locked): 12
- Shots 2–7: 72
- Total: 96 credits ≈ $1.54 at 2K pricing
