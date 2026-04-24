#!/usr/bin/env python3
"""Apply Rested audit + color-font-pass fixes to pulled MAIN theme files.

Scope: audit findings + Michael's color/font pass intent.
NOT fixed here (Mukul's PT 2 job): vacuum-template custom_text block copy.
"""
import json, re, shutil, os
from pathlib import Path

THEME = Path("/tmp/rested-theme-main")
BRAND_GREEN = "#1f5e3b"
SCHEME_PINK = "#ef4a65"  # Elixir default to unify out

def load_theme_json(path):
    text = path.read_text()
    stripped = re.sub(r'^\s*/\*.*?\*/\s*', '', text, count=1, flags=re.DOTALL)
    return json.loads(stripped), text.startswith('/*')

def save_theme_json(path, data, had_comment):
    path.with_suffix(path.suffix + '.bak').write_text(path.read_text()) if not path.with_suffix(path.suffix + '.bak').exists() else None
    # Write compact JSON (matches Shopify export style)
    body = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    path.write_text(body)

changes = []

# ============ 1. config/settings_data.json ============
p = THEME / "config/settings_data.json"
sd, had = load_theme_json(p)
cur = sd["current"]

# Font pass — serif title
before = cur.get("type_header_font")
cur["type_header_font"] = "lora_n7"
changes.append(f"settings.type_header_font: {before!r} -> 'lora_n7'")

# Letter spacing fix (negative -> positive)
before = cur.get("body_letter_spacing")
cur["body_letter_spacing"] = 0.3
changes.append(f"settings.body_letter_spacing: {before} -> 0.3")

# Accent unification
for field in ("global_section_accent_2_color", "global_section_button_color"):
    before = cur.get(field)
    if before and before != BRAND_GREEN:
        cur[field] = BRAND_GREEN
        changes.append(f"settings.{field}: {before!r} -> {BRAND_GREEN!r}")

# Color schemes — sweep accent_1 from pink to brand green
for scheme_id, scheme in cur.get("color_schemes", {}).items():
    s = scheme.get("settings", {})
    if s.get("accent_1") == SCHEME_PINK or (s.get("accent_1", "").lower() == SCHEME_PINK.lower()):
        s["accent_1"] = BRAND_GREEN
        changes.append(f"  color_scheme.{scheme_id}.accent_1: {SCHEME_PINK} -> {BRAND_GREEN}")

save_theme_json(p, sd, had)

# ============ 2. templates/product.json ============
p = THEME / "templates/product.json"
prod, had = load_theme_json(p)

sec = prod["sections"]["shop_product_details_YnRKdn"]
blocks = sec["blocks"]

# Aero Vacuum -> disable custom title (pull from product record)
title_b = blocks["title_jJAKcC"]["settings"]
before = (title_b.get("use_custom_title"), title_b.get("custom_title"))
title_b["use_custom_title"] = False
title_b["custom_title"] = ""
changes.append(f"product.title_jJAKcC: use_custom_title/custom_title {before} -> (False, '')")

# Main add-to-cart — CTA text + font size
atc_b = blocks["add_to_cart_hnegaC"]["settings"]
before = (atc_b.get("button_text_override"), atc_b.get("custom_button_font_size"))
atc_b["button_text_override"] = "Get Yours Now"
atc_b["custom_button_font_size"] = 16
changes.append(f"product.add_to_cart_hnegaC: button_text_override/font_size {before} -> ('Get Yours Now', 16)")

# CINCOM-y $49 promo — neutralize (Mukul replaces)
promo = blocks["custom_text_teazbd"]["settings"]
before = promo.get("text", "")[:60]
promo["text"] = ""
changes.append(f"product.custom_text_teazbd.text: {before!r}... -> ''")

# Sticky CTA
sticky_s = prod["sections"]["sticky_add_to_cart_NJqgUd"]["settings"]
before = sticky_s.get("button_text")
sticky_s["button_text"] = "Get Yours Now"
changes.append(f"product.sticky.button_text: {before!r} -> 'Get Yours Now'")

save_theme_json(p, prod, had)

# ============ 3. templates/index.json ============
p = THEME / "templates/index.json"
idx, had = load_theme_json(p)

hero = idx["sections"]["new_hero_tq9qtW"]
hs = hero["settings"]

for field, target in [
    ("button_bg", BRAND_GREEN),
    ("button_text_color", "#ffffff"),
    ("button_font_size_mobile", 16),
]:
    before = hs.get(field)
    hs[field] = target
    changes.append(f"index.hero.{field}: {before!r} -> {target!r}")

# Hero button text
hbtn = hero.get("blocks", {}).get("button_pgbiCn")
if hbtn:
    bs = hbtn["settings"]
    before = bs.get("button_text")
    bs["button_text"] = "Get Yours Now"
    changes.append(f"index.hero.button_pgbiCn.button_text: {before!r} -> 'Get Yours Now'")

# Image with text button label (if present)
iwt = idx["sections"].get("image_with_text_36pMmF")
if iwt:
    b2 = iwt.get("blocks", {}).get("button_xAXpyj")
    if b2 and "button_label" in b2.get("settings", {}):
        before = b2["settings"]["button_label"]
        b2["settings"]["button_label"] = "Get Yours Now"
        changes.append(f"index.iwt.button_xAXpyj.button_label: {before!r} -> 'Get Yours Now'")

save_theme_json(p, idx, had)

# ============ Summary ============
print(f"\nApplied {len(changes)} edits:\n")
for c in changes:
    print(f"  • {c}")

# Verify files re-parse cleanly
for path in (
    THEME / "config/settings_data.json",
    THEME / "templates/product.json",
    THEME / "templates/index.json",
):
    load_theme_json(path)
print("\nAll 3 files re-parse cleanly ✓")
