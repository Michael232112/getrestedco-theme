# Phase 3 — Image Wiring Guide

After `shopify theme push` deploys the assets in `assets/`, Shopify's theme editor needs the image fields wired to these files. The image_picker JSON setting type stores `shopify://shop_images/...` URLs, which require uploading to **Settings → Files** first (separate from theme assets).

## Assets shipped in this commit

| File in `assets/` | Section | Mukul § | Aspect |
|---|---|---|---|
| `rested-agitation-a-drawer.jpg` | `image_with_text_WPzJcE` | §3 Agitation A | 16:9 |
| `rested-agitation-b-hands.jpg` | `rich_text_YkP6Md` (background) OR new section image | §4 Agitation B | 4:5 |
| `rested-recovery-ritual-hero.jpg` (Plan A) | `image_with_text_yU6dxk` | §5 Solution Reveal | 16:9 |
| `rested-citation-archives-phys-med.jpg` | `as_seen_in_logos_byrbEG` block 1 | §7 Authority | 1:1 |
| `rested-citation-int-archives-health.jpg` | `as_seen_in_logos_byrbEG` block 2 | §7 Authority | 1:1 |
| `rested-citation-journal-hand-therapy.jpg` | `as_seen_in_logos_byrbEG` block 3 | §7 Authority | 1:1 |
| `rested-usecase-shoelace.jpg` | `image_with_text_USECASE_NEW` | §10 Use Case | 4:5 |
| `rested-stats-backdrop.jpg` | `statistics_column_y9eLJy` (background) | §11 Stats | 16:9 |
| `rested-timeline-grounding.jpg` (Plan A) | `store_features_QmUYDi` (background) | §12 Timeline | 16:9 |

## Manual wiring steps (in admin theme editor)

### 1. Upload the assets into **Shopify Files** library
- Shopify admin → **Content** → **Files** → drag all 9 `rested-*.jpg` files in (the 7 new + 2 from Plan A).
- Shopify will give each a `shopify://shop_images/<filename>` URL accessible from any image_picker.

### 2. Open the **theme editor** for the live MAIN theme
- Shopify admin → **Online Store** → **Themes** → `elixir-ky-01-2604` → **Customize**.
- Switch to **Product page** template (top-bar dropdown — type "Rested Hand Massager" in the search if needed).

### 3. Wire each section's image picker
For each of the sections below, click into the section in the left sidebar, find the **Image** field, click **Select image**, pick from **Library**, and choose the matching file:

| Section in sidebar | Pick this file |
|---|---|
| **Image with Text** (§3 Agitation A — first one in sidebar) | `rested-agitation-a-drawer.jpg` |
| **Image with Text** (§5 Solution Reveal — third in sidebar) | `rested-recovery-ritual-hero.jpg` |
| **As Seen In Logos** (§7 Authority) — open each of 3 logo blocks | citations 1, 2, 3 in order |
| **Image with Text** (§10 Use Case — newly added "instance NEW") | `rested-usecase-shoelace.jpg` |
| **Statistics Column** (§11 Stats — has a background_image setting at section level) | `rested-stats-backdrop.jpg` |
| **Store Features** (§12 Timeline — has a background_image setting) | `rested-timeline-grounding.jpg` |

§4 (`rich-text` Agitation B) doesn't have a background image setting in this theme. The hands image (`rested-agitation-b-hands.jpg`) can either:
- Be added by switching §4 to an `image-with-text` section type instead (more invasive)
- Stay unused for now (text-only §4 is a clean editorial moment in Mukul's flow)

§13 (Facebook Comments) and §9b (Hobby Grid) don't need new images — they're emoji-driven.

### 4. Save + preview mobile
After all picks, click **Save** in top-right. Preview at `https://getrestedco.com/products/rested-hand-massager` (mobile viewport).

## Tempfile backup URLs (in case Files re-upload is needed)

The Nano Banana CDN tempfile URLs from the generation run on 2026-04-25 — usable for ~24 hours, then expire:

- §3 Drawer: https://tempfile.aiquickdraw.com/image-format-converter/1777116032287-vhgk15shxai.jpg
- §4 Hands: https://tempfile.aiquickdraw.com/na2/25f4898b1be7c2212faf9cbc99eab0ea1141871.jpeg
- §7-1 Archives Phys Med: https://tempfile.aiquickdraw.com/na2/e43c4bbcf8a894eb8853346e0563de011346621.jpeg
- §7-2 Int Archives Health: https://tempfile.aiquickdraw.com/image-format-converter/1777116048349-mnlflfpennp.jpg
- §7-3 J Hand Therapy: https://tempfile.aiquickdraw.com/na2/dc5986ca52cf5032aca6125b25fb96fb1814912.jpeg
- §10 Use Case: https://tempfile.aiquickdraw.com/na2/8fb364fb149020ef2d2b194a55d747451325556.jpeg
- §11 Stats backdrop: https://tempfile.aiquickdraw.com/image-format-converter/1777116078712-4pparcp0bww.jpg

The local repo files in `assets/` are the durable source of truth.

## Credits used (Phase 3)

- §3 Drawer 16:9 2K: 12cr
- §4 Hands 4:5 2K (with avatar ref): 12cr
- §7-1, §7-2, §7-3 Citations 1:1 1K: 8 + 8 + 8 = 24cr
- §10 Shoelace 4:5 2K (with avatar ref): 12cr
- §11 Stats backdrop 16:9 1K: 8cr

**Total: 68 credits ≈ $1.10**, well under the 80cr budget. Headroom remains: ~1830 credits in the KieAI account.
