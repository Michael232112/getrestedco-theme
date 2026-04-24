#!/usr/bin/env python3
"""Replace stale non-Rested theme content with PT1-safe Rested scaffolding.

This keeps the section structure intact for PT 1 while removing obvious
AirVacuum/FlyDrop carryover copy that makes the theme untrustworthy.
"""

from __future__ import annotations

import json
from pathlib import Path


THEME = Path(__file__).resolve().parents[1]
PRODUCT_HANDLE = "rested-hand-massager"
PRODUCT_LINK = f"shopify://products/{PRODUCT_HANDLE}"
BRAND_GREEN = "#1f5e3b"


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))


def apply_text_list(blocks: dict, payloads: list[dict]) -> list[str]:
    changes = []
    for block_id, payload in zip(blocks.keys(), payloads):
        settings = blocks[block_id]["settings"]
        for key, value in payload.items():
            before = settings.get(key)
            if before != value:
                settings[key] = value
                changes.append(f"{block_id}.{key}: {before!r} -> {value!r}")
    return changes


def main() -> None:
    changes: list[str] = []

    product_path = THEME / "templates/product.json"
    product = load_json(product_path)

    shop_details = product["sections"]["shop_product_details_YnRKdn"]
    shop_settings = shop_details["settings"]
    if shop_settings.get("current_product") != PRODUCT_HANDLE:
        changes.append(
            f"product.shop_product_details.current_product: {shop_settings.get('current_product')!r} -> {PRODUCT_HANDLE!r}"
        )
        shop_settings["current_product"] = PRODUCT_HANDLE

    product_blocks = shop_details["blocks"]
    for block_id, replacement in {
        "custom_text_pdQQkk": "<p><strong>Compression-style relief</strong></p>",
        "custom_text_Fm3qaa": "<p>Soothing warmth for tired hands</p>",
        "custom_text_BYd69L": "<p>Air compression + warmth</p>",
        "custom_text_XLBwJd": "<p>For hands worn out by typing, cooking, crafting, and caregiving</p>",
    }.items():
        if block_id in product_blocks:
            before = product_blocks[block_id]["settings"].get("text")
            if before != replacement:
                product_blocks[block_id]["settings"]["text"] = replacement
                changes.append(f"product.{block_id}.text: {before!r} -> {replacement!r}")

    for block_id in ("custom_text_LE8GRw", "custom_text_hJbHX8"):
        if block_id in product_blocks:
            before = product_blocks[block_id]["settings"].get("text")
            if before:
                product_blocks[block_id]["settings"]["text"] = ""
                changes.append(f"product.{block_id}.text: {before!r} -> ''")

    if "custom_text_e7xkQT" in product_blocks:
        before = product_blocks["custom_text_e7xkQT"]["settings"].get("text")
        if before:
            product_blocks["custom_text_e7xkQT"]["settings"]["text"] = ""
            changes.append(f"product.custom_text_e7xkQT.text: {before!r} -> ''")

    rating = product_blocks["image_rating_Pc9yqk"]["settings"]
    if rating.get("rating_text") != "<p>Loved by women building calmer evening routines</p>":
        changes.append("product.image_rating.rating_text -> Rested-safe copy")
        rating["rating_text"] = "<p>Loved by women building calmer evening routines</p>"

    faq_intro = product_blocks["product_faq_T6WHNi"]["settings"]
    faq_intro_updates = {
        "question_1": "What it does",
        "answer_1": "<p>Rested is a portable hand massager designed to make tired hands feel calmer after long days of typing, cooking, crafting, caregiving, or everyday chores. It combines air compression, warmth, and a soothing massage feel in a quick at-home ritual.</p>",
        "question_2": "Shipping, returns, and support",
        "answer_2": "<p>Shipping rates and delivery estimates are shown at checkout based on your location.</p><p>If Rested is not the right fit, please use the return and support details listed in the store policies and contact page for the latest guidance.</p>",
    }
    for key, value in faq_intro_updates.items():
        before = faq_intro.get(key)
        if before != value:
            faq_intro[key] = value
            changes.append(f"product.product_faq.{key}: {before!r} -> {value!r}")

    product_testimonials = product["sections"]["testimonials_44W6N3"]["blocks"]
    changes.extend(
        apply_text_list(
            product_testimonials,
            [
                {
                    "title": "Impressed from the start",
                    "content": "<p>I keep this by the couch and reach for it most evenings. It feels like a simple little ritual that helps my hands relax after a long day.</p>",
                },
                {
                    "title": "Exactly as promised",
                    "content": "<p>The device feels sturdy, easy to use, and surprisingly calming. It is the kind of wellness product that actually earns a place in your routine.</p>",
                },
                {
                    "title": "Relief I actually keep using",
                    "content": "<p>My hands get stiff after work, and this is one of the few things I remember to use because it is quick and comforting.</p>",
                },
                {
                    "title": "Exceeded my expectations",
                    "content": "<p>I bought it hoping for a little relief and ended up using it far more often than I expected. The warmth makes it feel especially soothing at night.</p>",
                },
                {
                    "title": "A thoughtful gift",
                    "content": "<p>I originally ordered one for myself and then bought another as a gift. It feels practical, calming, and easy to appreciate right away.</p>",
                },
                {
                    "title": "Simple and comforting",
                    "content": "<p>It does not take any learning curve. You slip your hand in, choose a setting, and a few minutes later you feel more relaxed.</p>",
                },
                {
                    "title": "Very satisfied with my purchase",
                    "content": "<p>This feels like a small luxury at the end of the day. It has become part of how I wind down after using my hands all afternoon.</p>",
                },
                {
                    "title": "Did exactly what I needed",
                    "content": "<p>I wanted something easy for hand tension and this delivered. It feels supportive without being fussy or complicated.</p>",
                },
                {
                    "title": "Comforting heat without fuss",
                    "content": "<p>I like that it feels giftable and useful at the same time. It is easy to keep nearby and reach for when my hands feel overworked.</p>",
                },
            ],
        )
    )

    comparison = product["sections"]["product_comparison_pw7jpT"]
    comparison_settings = comparison["settings"]
    comparison_updates = {
        "title_part_1": "Why Women Choose Rested",
        "subheading": "<p>A daily hand-relief ritual should feel easy to trust, easy to use, and easy to keep nearby.</p>",
    }
    for key, value in comparison_updates.items():
        before = comparison_settings.get(key)
        if before != value:
            comparison_settings[key] = value
            changes.append(f"product.comparison.{key}: {before!r} -> {value!r}")

    comparison_blocks = comparison["blocks"]
    product_columns = [k for k, v in comparison_blocks.items() if v["type"] == "product_column"]
    if len(product_columns) >= 2:
        pc1 = comparison_blocks[product_columns[0]]["settings"]
        pc2 = comparison_blocks[product_columns[1]]["settings"]
        for key, value in {"product_name": "Rested"}.items():
            if pc1.get(key) != value:
                changes.append(f"product.comparison.{product_columns[0]}.{key} -> {value!r}")
                pc1[key] = value
        for key, value in {"product_name": "Basic Hand Massagers"}.items():
            if pc2.get(key) != value:
                changes.append(f"product.comparison.{product_columns[1]}.{key} -> {value!r}")
                pc2[key] = value

    product_feature_rows = [k for k, v in comparison_blocks.items() if v["type"] == "feature_row"]
    product_feature_names = [
        "Air compression massage",
        "Optional soothing heat",
        "Easy daily-use routine",
        "Comfort-first giftability",
        "Portable at-home relief",
        "Designed for tired hands",
    ]
    for block_id, feature_name in zip(product_feature_rows, product_feature_names):
        settings = comparison_blocks[block_id]["settings"]
        if settings.get("feature_name") != feature_name:
            changes.append(f"product.comparison.{block_id}.feature_name -> {feature_name!r}")
            settings["feature_name"] = feature_name
        settings["value_1"] = "yes"
        settings["text_value_1"] = "Yes"
        settings["value_2"] = "no"
        settings["text_value_2"] = "No"

    stats = product["sections"]["statistics_column_y9eLJy"]
    stats_settings = stats["settings"]
    stats_updates = {
        "heading": "A simple ritual for overworked hands.",
        "disclaimer_text": "<em>Rested is positioned here as PT 1 scaffolding so the theme feels coherent before final copy is delivered. The goal is calm, readable, and trustworthy.</em>",
    }
    for key, value in stats_updates.items():
        before = stats_settings.get(key)
        if before != value:
            stats_settings[key] = value
            changes.append(f"product.statistics.{key}: {before!r} -> {value!r}")

    stat_blocks = stats["blocks"]
    changes.extend(
        apply_text_list(
            stat_blocks,
            [
                {"number": "3", "title": "Massage settings to reach for"},
                {"number": "10", "title": "Minutes that feel like a reset"},
                {"number": "1", "title": "Easy ritual to keep nearby"},
            ],
        )
    )

    image_with_text = product["sections"]["image_with_text_WPzJcE"]
    iwt_settings = image_with_text["settings"]
    for key, value in {
        "accent_color": BRAND_GREEN,
        "button_bg_color": BRAND_GREEN,
        "button_text_color": "#ffffff",
    }.items():
        if iwt_settings.get(key) != value:
            changes.append(f"product.image_with_text_WPzJcE.{key}: {iwt_settings.get(key)!r} -> {value!r}")
            iwt_settings[key] = value
    changes.extend(
        apply_text_list(
            image_with_text["blocks"],
            [
                {"heading_text": "A small ritual that makes busy hands feel cared for."},
                {
                    "paragraph_text": "<p>Rested gives the product page a believable wellness story now, before final brand copy is dropped in. The emphasis is comfort, ease, and a calmer end-of-day routine.</p>"
                },
            ],
        )
    )

    rich_text = product["sections"]["rich_text_YkP6Md"]
    for key, value in {
        "accent_color": BRAND_GREEN,
        "button_bg_color": BRAND_GREEN,
        "button_hover_bg_color": BRAND_GREEN,
    }.items():
        if rich_text["settings"].get(key) != value:
            changes.append(f"product.rich_text.{key}: {rich_text['settings'].get(key)!r} -> {value!r}")
            rich_text["settings"][key] = value
    changes.extend(
        apply_text_list(
            rich_text["blocks"],
            [
                {"subtitle": "<p>Meet Rested</p>"},
                {"title": "Daily hand relief you will actually keep using"},
                {
                    "subtitle": "<p>PT 1 does not need final sales copy yet, but it does need a coherent product story. Rested should read like a calm, giftable hand-massage ritual, not another product entirely.</p>"
                },
            ],
        )
    )

    roadmap = product["sections"]["roadmap_MP3fN8"]
    if roadmap["settings"].get("heading") != "How to use Rested":
        changes.append(f"product.roadmap.heading: {roadmap['settings'].get('heading')!r} -> 'How to use Rested'")
        roadmap["settings"]["heading"] = "How to use Rested"
    roadmap_steps = roadmap["blocks"]
    changes.extend(
        apply_text_list(
            roadmap_steps,
            [
                {"title": "Slip your hand in", "description": "<p>Place one hand comfortably inside the massager and settle into a position that feels relaxed.</p>"},
                {"title": "Choose your mode", "description": "<p>Select the compression and warmth setting that feels best for the moment.</p>"},
                {"title": "Take a few quiet minutes", "description": "<p>Let Rested do the work while you unwind, read, or sit back for a short reset.</p>"},
            ],
        )
    )

    benefits = product["sections"]["product_benefits_trbtD8"]
    if benefits["settings"].get("heading_regular") != "How to use Rested":
        changes.append(f"product.benefits.heading_regular: {benefits['settings'].get('heading_regular')!r} -> 'How to use Rested'")
        benefits["settings"]["heading_regular"] = "How to use Rested"
    benefit_blocks = benefits["blocks"]
    changes.extend(
        apply_text_list(
            benefit_blocks,
            [
                {"title": "Slip your hand in", "description": "Start with one hand and choose the position that feels most comfortable."},
                {"title": "Choose your setting", "description": "Pick the mode and warmth level that match how your hands feel that day."},
                {"title": "Let it become a ritual", "description": "Use Rested during a quiet break, after chores, or whenever your hands feel overworked."},
            ],
        )
    )

    iwt2 = product["sections"]["image_with_text_yU6dxk"]
    for key, value in {
        "accent_color": BRAND_GREEN,
        "button_bg_color": BRAND_GREEN,
        "button_text_color": "#ffffff",
    }.items():
        if iwt2["settings"].get(key) != value:
            changes.append(f"product.image_with_text_yU6dxk.{key}: {iwt2['settings'].get(key)!r} -> {value!r}")
            iwt2["settings"][key] = value
    iwt2_blocks = iwt2["blocks"]
    if "heading_dkXYwA" in iwt2_blocks:
        iwt2_blocks["heading_dkXYwA"]["settings"]["heading_text"] = "More than a device,"
        iwt2_blocks["heading_dkXYwA"]["settings"]["heading_accent"] = "it is an easier reset."
    if "paragraph_EdK7mL" in iwt2_blocks:
        iwt2_blocks["paragraph_EdK7mL"]["settings"]["paragraph_text"] = (
            "<p>Rested belongs in a calm, practical wellness routine. The message here is simple: it is easy to keep nearby, easy to use, and easy to gift.</p>"
        )
    if "bullet_list_UUcUa9" in iwt2_blocks:
        bullet = iwt2_blocks["bullet_list_UUcUa9"]["settings"]
        bullet["list_item_1"] = "Air compression + soothing warmth"
        bullet["list_item_2"] = "Designed for daily use"
        bullet["list_item_3"] = "Portable and easy to keep nearby"
        bullet["list_item_4"] = "A giftable wellness pick"
    if "button_4t7bRj" in iwt2_blocks:
        btn = iwt2_blocks["button_4t7bRj"]["settings"]
        btn["button_label"] = "Get Yours Now"
        btn["button_redirect_type"] = "product"
        btn["button_link"] = PRODUCT_LINK

    store_faq = product["sections"]["store_faq_9hjxMb"]
    faq_settings = store_faq["settings"]
    faq_settings["heading"] = "Rested Questions"
    faq_settings["question_font_size_mobile"] = 16
    faq_settings["answer_font_size_mobile"] = 16
    faq_payloads = [
        {
            "question": "Who is Rested for?",
            "answer": "<p>Rested is framed for people whose hands feel tired, overworked, or ready for a little more comfort at the end of the day. It is especially well positioned for women 40+ and gift shoppers looking for a wellness-forward present.</p>",
        },
        {
            "question": "Does it use heat?",
            "answer": "<p>Yes, the product story for Rested includes a soothing warmth setting alongside compression-style massage. Final feature claims can be tightened once the final product details are locked.</p>",
        },
        {
            "question": "How often can I use it?",
            "answer": "<p>It is positioned as a simple daily ritual you can reach for whenever your hands feel tense or overworked.</p>",
        },
        {
            "question": "Is it easy to use?",
            "answer": "<p>Yes. The intended experience is straightforward: place your hand in, choose a setting, and relax for a few quiet minutes.</p>",
        },
        {
            "question": "Is it giftable?",
            "answer": "<p>Very much so. Rested is being framed as a thoughtful wellness gift, especially for mothers, caretakers, and anyone who would appreciate practical comfort.</p>",
        },
    ]
    changes.extend(apply_text_list(store_faq["blocks"], faq_payloads))

    save_json(product_path, product)

    index_path = THEME / "templates/index.json"
    index = load_json(index_path)

    hero = index["sections"]["new_hero_tq9qtW"]
    hero_blocks = hero["blocks"]
    hero_blocks["subtitle_rXRxYH"]["settings"]["subtitle"] = "<p><strong>Portable hand relief for tired, overworked hands</strong></p>"
    hero_blocks["heading_p9CVL9"]["settings"]["heading"] = "Soothe hand tension in minutes."
    hero_blocks["subtitle_69D7t7"]["settings"]["subtitle"] = (
        "<p>Rested is a portable hand massager built around a calm daily ritual. Think air compression, warmth, and a little comfort you can reach for after typing, cooking, crafting, or long days.</p>"
    )
    hero_blocks["button_pgbiCn"]["settings"]["button_link"] = PRODUCT_LINK
    hero_blocks["button_pgbiCn"]["settings"]["button_text"] = "Get Yours Now"

    steps = index["sections"]["steps_WQ7Xib"]["blocks"]
    changes.extend(
        apply_text_list(
            steps,
            [
                {
                    "step_title": "Slip it on",
                    "step_description": "Place one hand inside Rested and settle in comfortably.",
                },
                {
                    "step_title": "Choose your mode",
                    "step_description": "Pick the setting that feels right for the amount of tension or fatigue you are carrying.",
                },
                {
                    "step_title": "Relax into relief",
                    "step_description": "Let it run for a few quiet minutes while you unwind, read, or reset between tasks.",
                },
            ],
        )
    )

    home_testimonials = index["sections"]["testimonials_Ywi4m4"]["blocks"]
    home_testimonial_copy = [
        "<p>I keep Rested nearby in the evenings and actually use it. It feels calming without asking much of you.</p>",
        "<p>My hands get tired after long computer days and this has become part of how I wind down. It feels simple and comforting.</p>",
        "<p>I bought it hoping for a little relief and it ended up becoming one of the easiest wellness habits to keep.</p>",
        "<p>The warmth is my favorite part. It makes the whole experience feel more soothing and less clinical.</p>",
        "<p>This feels giftable in the best way: practical, calming, and easy to appreciate right away.</p>",
        "<p>I like that I can reach for it without thinking too hard. A few minutes with it helps me slow down.</p>",
        "<p>It looks nice, feels sturdy, and has the kind of comfort-first design I wanted for an at-home wellness tool.</p>",
        "<p>I gave one to my mom after trying mine and she immediately understood the appeal. It feels thoughtful and useful.</p>",
        "<p>The whole experience is straightforward. It is not complicated, it just fits naturally into an evening routine.</p>",
        "<p>I wanted something that felt restorative instead of gimmicky, and this gets much closer to that than most wellness gadgets do.</p>",
    ]
    for block_id, copy in zip(home_testimonials.keys(), home_testimonial_copy):
        settings = home_testimonials[block_id]["settings"]
        if settings.get("content") != copy:
            changes.append(f"index.testimonials.{block_id}.content updated")
            settings["content"] = copy

    home_comparison = index["sections"]["product_comparison_8wRiLf"]
    home_comparison["settings"]["title_part_1"] = "Why customers choose Rested"
    home_comparison["settings"]["subheading"] = "<p>A calmer, more giftable hand-massage ritual than the generic options people usually settle for.</p>"
    home_comparison_blocks = home_comparison["blocks"]
    home_product_columns = [k for k, v in home_comparison_blocks.items() if v["type"] == "product_column"]
    if len(home_product_columns) >= 2:
        home_comparison_blocks[home_product_columns[0]]["settings"]["product_name"] = "Rested"
        home_comparison_blocks[home_product_columns[1]]["settings"]["product_name"] = "Basic Hand Massagers"
    home_feature_rows = [k for k, v in home_comparison_blocks.items() if v["type"] == "feature_row"]
    home_feature_names = [
        "Air compression massage",
        "Optional soothing heat",
        "Easy to use while resting",
        "Giftable wellness feel",
        "Portable for daily routines",
        "Designed for tired hands",
    ]
    for block_id, feature_name in zip(home_feature_rows, home_feature_names):
        settings = home_comparison_blocks[block_id]["settings"]
        settings["feature_name"] = feature_name
        settings["value_1"] = "yes"
        settings["text_value_1"] = "Yes"
        settings["value_2"] = "no"
        settings["text_value_2"] = "No"

    home_iwt = index["sections"]["image_with_text_36pMmF"]
    for key, value in {
        "accent_color": BRAND_GREEN,
        "button_bg_color": BRAND_GREEN,
        "button_text_color": "#ffffff",
    }.items():
        home_iwt["settings"][key] = value
    home_iwt_blocks = home_iwt["blocks"]
    home_iwt_blocks["heading_hr4PMP"]["settings"]["heading_text"] = "More than a hand massager,"
    home_iwt_blocks["heading_hr4PMP"]["settings"]["heading_accent"] = "it is an easier reset."
    home_iwt_blocks["paragraph_MwEtr9"]["settings"]["paragraph_text"] = (
        "<p>Rested is being positioned as a comforting, portable way to care for hands that feel overworked. The homepage only needs to feel coherent and trustworthy at PT 1.</p>"
    )
    bullet2 = home_iwt_blocks["bullet_list_zjen6G"]["settings"]
    bullet2["list_item_1"] = "Air compression + soothing warmth"
    bullet2["list_item_2"] = "Daily-use comfort"
    bullet2["list_item_3"] = "Portable for home or desk"
    bullet2["list_item_4"] = "Thoughtful gift framing"
    home_iwt_blocks["button_xAXpyj"]["settings"]["button_link"] = PRODUCT_LINK
    home_iwt_blocks["button_xAXpyj"]["settings"]["button_label"] = "Get Yours Now"

    save_json(index_path, index)

    footer_path = THEME / "sections/footer-group.json"
    footer = load_json(footer_path)
    footer_blocks = footer["sections"]["footer"]["blocks"]
    footer_blocks["text_column_zGNKtt"]["settings"]["heading"] = "Daily hand relief, right at home."
    footer_blocks["text_column_zGNKtt"]["settings"]["text"] = (
        "<p>Rested is a portable hand massager framed around calm, comfort, and an easy end-of-day ritual. This footer copy is PT 1 scaffolding until final brand copy is ready.</p>"
    )
    support = footer_blocks["custom_links_1"]["settings"]
    support["link_1_text"] = "Contact Us"
    support["link_1_url"] = "/pages/contact"
    support["link_2_text"] = "Privacy Policy"
    support["link_2_url"] = "/policies/privacy-policy"
    support["link_3_text"] = "Terms of Service"
    support["link_3_url"] = "/policies/terms-of-service"
    support["link_4_text"] = "Refund Policy"
    support["link_4_url"] = "/policies/refund-policy"
    support["link_5_text"] = "Shipping Policy"
    support["link_5_url"] = "/policies/shipping-policy"
    support["link_6_text"] = ""
    support["link_6_url"] = ""
    save_json(footer_path, footer)

    header_path = THEME / "sections/header-group.json"
    header = load_json(header_path)
    ticker = header["sections"]["scrolling_features_bar_J64Pwx"]["blocks"]["feature_item_4AhQrK"]["settings"]
    banner_text = "RESTED LAUNCH PREVIEW | PORTABLE HAND RELIEF FOR TIRED, OVERWORKED HANDS"
    if ticker.get("text") != banner_text:
        changes.append(f"header.ticker.text: {ticker.get('text')!r} -> {banner_text!r}")
        ticker["text"] = banner_text
    save_json(header_path, header)

    print(f"Applied {len(changes)} content cleanup updates.")
    for change in changes:
        print(f"- {change}")


if __name__ == "__main__":
    main()
