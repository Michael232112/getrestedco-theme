#!/usr/bin/env python3
"""Phase 1 of the PT 2 PDP restructure to match Mukul's 14-section landing page copy.

This script ONLY touches structure: section reorder, block-count adjustments,
section deletion, new section instantiation. NO copy population (Phase 2).
NO image wiring (Phase 3).

Operations:
  1. Backup templates/product.json to .bak
  2. Delete `product_comparison_pw7jpT` (key + from order)
  3. Trim testimonials_44W6N3 from 9 -> 4 blocks (keep first 4)
  4. Trim as_seen_in_logos_byrbEG from 10 -> 3 blocks
  5. Add 1 block to store_features_QmUYDi (timeline phase 4)
  6. Add 1 block to roadmap_MP3fN8 (hobby grid item 4)
  7. Add 1 block to product_benefits_trbtD8 (icon benefit 4)
  8. Add 2 blocks to store_faq_pV3P8w (offer accordion items 4 + 5)
  9. Add 3 blocks to store_faq_9hjxMb (FAQ items 6, 7, 8)
 10. Instantiate new section image_with_text_USECASE_NEW (3 blocks: heading + paragraph + bullet_list)
 11. Instantiate new section facebook_comments_NEW (6 review blocks)
 12. Reorder `order` array per Plan B mapping

Idempotent: safe to re-run. Each mutation checks current state before acting.
"""
from __future__ import annotations
import json
import shutil
import sys
import secrets
import string
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
PRODUCT_JSON = THEME / "templates/product.json"


def gen_id(length: int = 6) -> str:
    """Generate a Shopify-style alphanumeric block/section ID suffix."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def load_compact(path: Path):
    return json.loads(path.read_text())


def save_compact(path: Path, data) -> None:
    """Preserve Shopify export's compact single-line JSON."""
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))


def backup(path: Path) -> Path:
    bk = path.with_suffix(path.suffix + ".phase1.bak")
    if not bk.exists():
        shutil.copy2(path, bk)
        print(f"[backup] {bk.name}")
    else:
        print(f"[backup] already exists, skipping: {bk.name}")
    return bk


def trim_blocks(section: dict, keep: int, label: str) -> list[str]:
    """Trim section's blocks dict + block_order list down to `keep` count.
    Keeps the first `keep` block IDs from block_order (they remain in document order).
    """
    changes = []
    block_order = section.get("block_order", [])
    blocks = section.get("blocks", {})
    if len(block_order) <= keep:
        return changes
    kept = block_order[:keep]
    removed = block_order[keep:]
    section["block_order"] = kept
    for bid in removed:
        if bid in blocks:
            del blocks[bid]
    changes.append(f"{label}: trimmed {len(removed)} blocks ({len(block_order)} -> {keep})")
    return changes


def add_block(section: dict, block_type: str, block_id: str, settings: dict | None = None) -> str | None:
    """Append a new block to section.blocks + section.block_order.
    Returns the new block id (or None if it already existed)."""
    blocks = section.setdefault("blocks", {})
    block_order = section.setdefault("block_order", [])
    if block_id in blocks:
        return None
    blocks[block_id] = {
        "type": block_type,
        "settings": settings or {},
    }
    block_order.append(block_id)
    return block_id


def main() -> None:
    backup(PRODUCT_JSON)
    p = load_compact(PRODUCT_JSON)
    sections = p.setdefault("sections", {})
    order = p.setdefault("order", [])
    changes: list[str] = []

    # ----------------------------------------------------------------------
    # 1. DELETE product_comparison_pw7jpT (Mukul did not include Us-vs-Them)
    # ----------------------------------------------------------------------
    if "product_comparison_pw7jpT" in sections:
        del sections["product_comparison_pw7jpT"]
        changes.append("deleted section: product_comparison_pw7jpT")
    if "product_comparison_pw7jpT" in order:
        order.remove("product_comparison_pw7jpT")
        changes.append("removed product_comparison_pw7jpT from order")

    # ----------------------------------------------------------------------
    # 2. TRIM testimonials_44W6N3 from 9 -> 4 (Mukul's 4 verified reviews)
    # ----------------------------------------------------------------------
    if "testimonials_44W6N3" in sections:
        changes.extend(trim_blocks(sections["testimonials_44W6N3"], 4, "testimonials_44W6N3"))

    # ----------------------------------------------------------------------
    # 3. TRIM as_seen_in_logos_byrbEG from 10 -> 3 (will be repurposed for §7
    #    Authority: 3 clinical citation cards)
    # ----------------------------------------------------------------------
    if "as_seen_in_logos_byrbEG" in sections:
        changes.extend(trim_blocks(sections["as_seen_in_logos_byrbEG"], 3, "as_seen_in_logos_byrbEG"))

    # ----------------------------------------------------------------------
    # 4. ADD 1 block to store_features_QmUYDi (3 -> 4) for §12 Timeline phases
    # ----------------------------------------------------------------------
    if "store_features_QmUYDi" in sections:
        sec = sections["store_features_QmUYDi"]
        if len(sec.get("block_order", [])) < 4:
            new_id = f"feature_{gen_id()}"
            add_block(sec, "feature", new_id, {"title": "", "description": ""})
            changes.append(f"store_features_QmUYDi: added block {new_id} (3 -> 4 for §12 phase 4)")

    # ----------------------------------------------------------------------
    # 5. ADD 1 block to roadmap_MP3fN8 (3 -> 4) for §9b Hobby Grid item 4
    # ----------------------------------------------------------------------
    if "roadmap_MP3fN8" in sections:
        sec = sections["roadmap_MP3fN8"]
        if len(sec.get("block_order", [])) < 4:
            new_id = f"roadmap_step_{gen_id()}"
            add_block(sec, "roadmap_step", new_id, {"badge_text": "", "title": "", "description": ""})
            changes.append(f"roadmap_MP3fN8: added block {new_id} (3 -> 4 for §9b hobby item 4)")

    # ----------------------------------------------------------------------
    # 6. ADD 1 block to product_benefits_trbtD8 (3 -> 4) for §9a Icon Benefit 4
    # ----------------------------------------------------------------------
    if "product_benefits_trbtD8" in sections:
        sec = sections["product_benefits_trbtD8"]
        if len(sec.get("block_order", [])) < 4:
            new_id = f"benefit_{gen_id()}"
            add_block(sec, "benefit", new_id, {"title": "", "description": ""})
            changes.append(f"product_benefits_trbtD8: added block {new_id} (3 -> 4 for §9a icon benefit 4)")

    # ----------------------------------------------------------------------
    # 7. ADD 2 blocks to store_faq_pV3P8w (3 -> 5) for §6 Offer accordion
    #    (Description, Why, Benefits, How, Guarantee)
    # ----------------------------------------------------------------------
    if "store_faq_pV3P8w" in sections:
        sec = sections["store_faq_pV3P8w"]
        while len(sec.get("block_order", [])) < 5:
            new_id = f"faq_item_{gen_id()}"
            add_block(sec, "faq_item", new_id, {"question": "", "answer": ""})
            changes.append(f"store_faq_pV3P8w: added block {new_id}")

    # ----------------------------------------------------------------------
    # 8. ADD 3 blocks to store_faq_9hjxMb (5 -> 8) for §14 FAQ
    # ----------------------------------------------------------------------
    if "store_faq_9hjxMb" in sections:
        sec = sections["store_faq_9hjxMb"]
        while len(sec.get("block_order", [])) < 8:
            new_id = f"faq_item_{gen_id()}"
            add_block(sec, "faq_item", new_id, {"question": "", "answer": ""})
            changes.append(f"store_faq_9hjxMb: added block {new_id}")

    # ----------------------------------------------------------------------
    # 9. INSTANTIATE image_with_text_USECASE_NEW for §10 Use Case
    #    Clone the settings shape from image_with_text_yU6dxk
    # ----------------------------------------------------------------------
    USECASE_KEY = "image_with_text_USECASE_NEW"
    if USECASE_KEY not in sections:
        # Clone settings from existing image-with-text instance for consistent visual style
        template_section = sections.get("image_with_text_yU6dxk", {})
        cloned_settings = dict(template_section.get("settings", {}))
        # Reset image-specific overrides; will be wired in Phase 3
        cloned_settings.pop("image", None)

        h_id = f"heading_{gen_id()}"
        p_id = f"paragraph_{gen_id()}"
        bl_id = f"bullet_list_{gen_id()}"

        sections[USECASE_KEY] = {
            "type": "image-with-text",
            "settings": cloned_settings,
            "blocks": {
                h_id: {"type": "heading", "settings": {"heading_text": "", "heading_accent": ""}},
                p_id: {"type": "paragraph", "settings": {"paragraph_text": ""}},
                bl_id: {"type": "bullet_list", "settings": {
                    "list_item_1": "",
                    "list_item_2": "",
                    "list_item_3": "",
                }},
            },
            "block_order": [h_id, p_id, bl_id],
        }
        changes.append(f"instantiated {USECASE_KEY} (image-with-text, 3 blocks: heading/paragraph/bullet_list)")

    # ----------------------------------------------------------------------
    # 10. INSTANTIATE facebook_comments_NEW for §13 FB Comments (6 review blocks)
    # ----------------------------------------------------------------------
    FB_KEY = "facebook_comments_NEW"
    if FB_KEY not in sections:
        review_ids = [f"review_{gen_id()}" for _ in range(6)]
        review_blocks = {
            rid: {"type": "review", "settings": {"name": "", "comment": "", "date": ""}}
            for rid in review_ids
        }
        sections[FB_KEY] = {
            "type": "facebook-comments",
            "settings": {
                "title": "",
                "section_padding_vertical": 60,
                "section_padding_horizontal": 20,
            },
            "blocks": review_blocks,
            "block_order": review_ids,
        }
        changes.append(f"instantiated {FB_KEY} (facebook-comments, 6 review blocks)")

    # ----------------------------------------------------------------------
    # 11. REORDER `order` per Plan B mapping (final 14-section flow + sticky)
    # ----------------------------------------------------------------------
    DESIRED_ORDER = [
        "shop_product_details_YnRKdn",       # §2 Hero + §6 inline price/CTA
        "sticky_add_to_cart_NJqgUd",         # sticky bar (passive)
        "image_with_text_WPzJcE",            # §3 Agitation A
        "rich_text_YkP6Md",                  # §4 Agitation B
        "image_with_text_yU6dxk",            # §5 Solution Reveal
        "store_faq_pV3P8w",                  # §6 Offer accordion (5 items)
        "as_seen_in_logos_byrbEG",           # §7 Authority (3 citations)
        "testimonials_44W6N3",               # §8 Testimonials (4)
        "product_benefits_trbtD8",           # §9a 4 icon benefits
        "roadmap_MP3fN8",                    # §9b hobby grid
        "image_with_text_USECASE_NEW",       # §10 Use Case
        "statistics_column_y9eLJy",          # §11 Stats
        "store_features_QmUYDi",             # §12 Timeline (4 phases)
        "facebook_comments_NEW",             # §13 FB Comments
        "store_faq_9hjxMb",                  # §14 FAQ (8)
    ]
    # Sanity: only reorder ones that exist in sections
    new_order = [s for s in DESIRED_ORDER if s in sections]
    # Append any sections we might have missed that exist but aren't in our desired order
    for sid in sections:
        if sid not in new_order:
            print(f"[warn] section {sid} not in DESIRED_ORDER; appending to end")
            new_order.append(sid)
    if new_order != order:
        p["order"] = new_order
        changes.append(f"reordered `order` array: {len(order)} -> {len(new_order)} entries")

    # ----------------------------------------------------------------------
    # WRITE OUT
    # ----------------------------------------------------------------------
    save_compact(PRODUCT_JSON, p)

    # Re-parse to verify valid JSON
    load_compact(PRODUCT_JSON)

    print()
    print(f"=== Phase 1 changes ({len(changes)}) ===")
    for c in changes:
        print(f"  • {c}")
    print()
    print(f"Final order ({len(p['order'])}):")
    for i, sid in enumerate(p["order"]):
        sec = sections.get(sid, {})
        n_blocks = len(sec.get("block_order", []))
        print(f"  [{i:2}] {sid} ({sec.get('type')}) — {n_blocks} blocks")


if __name__ == "__main__":
    main()
