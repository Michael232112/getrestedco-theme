#!/usr/bin/env python3
"""Phase 2 of the PT 2 PDP restructure.

Populates Mukul's verbatim 14-section landing page copy into the structural
skeleton built by Phase 1. Idempotent — re-running is safe; only writes when
field values differ from the desired ones.

Sections covered (matching Mukul's Notion spec):
  §2 Hero                     → shop_product_details_YnRKdn (title + custom_text x7)
  §3 Problem Agitation A      → image_with_text_WPzJcE
  §4 Problem Agitation B      → rich_text_YkP6Md
  §5 Solution Reveal          → image_with_text_yU6dxk
  §6 Offer Accordion (5 items)→ store_faq_pV3P8w
  §7 Authority (3 citations)  → as_seen_in_logos_byrbEG  [text-as-image lands in Phase 3]
  §8 Testimonials (4)         → testimonials_44W6N3
  §9a Icon Benefits (4)       → product_benefits_trbtD8
  §9b Hobby Grid (4)          → roadmap_MP3fN8 (repurposed)
  §10 Use Case                → image_with_text_USECASE_NEW
  §11 Stats (3)               → statistics_column_y9eLJy
  §12 Timeline (4 phases)     → store_features_QmUYDi (repurposed)
  §13 Facebook Comments (6)   → facebook_comments_NEW
  §14 FAQ (8)                 → store_faq_9hjxMb

Does NOT touch:
  - Sticky header / countdown bar (lives in header-group.json, separate scope)
  - Image references (Phase 3)
  - Variant prices / compareAt (Plan A locked these)
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
PRODUCT_JSON = THEME / "templates/product.json"


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))


def backup(path: Path) -> None:
    bk = path.with_suffix(path.suffix + ".phase2.bak")
    if not bk.exists():
        shutil.copy2(path, bk)
        print(f"[backup] {bk.name}")


changes: list[str] = []


def set_setting(target: dict, key: str, value, label: str) -> None:
    """Set target['settings'][key] = value if different. Track change."""
    settings = target.setdefault("settings", {})
    if settings.get(key) != value:
        settings[key] = value
        changes.append(f"{label}.{key} ← {repr(value)[:80]}")


def get_block(section: dict, suffix: str) -> dict | None:
    """Find a block whose ID ends with `suffix` (handles full IDs and shortened ones)."""
    blocks = section.get("blocks", {})
    if suffix in blocks:
        return blocks[suffix]
    # Try block IDs that end with the suffix
    for bid, b in blocks.items():
        if bid.endswith(suffix):
            return b
    return None


def get_block_by_index(section: dict, idx: int) -> tuple[str, dict] | None:
    """Get the block at position `idx` in block_order."""
    block_order = section.get("block_order", [])
    if idx >= len(block_order):
        return None
    bid = block_order[idx]
    return bid, section["blocks"][bid]


# ---------------------------------------------------------------------------
# §2 HERO — shop_product_details_YnRKdn
# H1 = "Let's just say it..." (set via title block custom_title override)
# 4 ❌ pain checkmarks → custom_text_pdQQkk/Fm3qaa/BYd69L/XLBwJd
# 3 transition lines → teazbd / LE8GRw / hJbHX8
# (e7xkQT stays empty for future)
# ---------------------------------------------------------------------------
def populate_hero(sections):
    sec = sections.get("shop_product_details_YnRKdn")
    if not sec:
        return

    # Title block: hero H1 (use_custom_title=true)
    title_block = sec["blocks"].get("title_jJAKcC")
    if title_block:
        set_setting(title_block, "use_custom_title", True, "title_jJAKcC")
        set_setting(title_block, "custom_title", "Let's just say it…", "title_jJAKcC")

    # Trustpilot rating: Mukul's "Excellent 4.8, verified reviews"
    tr = sec["blocks"].get("trustpilot_rating_mrtVHq")
    if tr:
        set_setting(tr, "rating_text", "Excellent — verified reviews", "trustpilot_rating")
        set_setting(tr, "rating_score", "4.8", "trustpilot_rating")

    # 4 pain checkmarks — Mukul's verbatim
    hero_checks = {
        "custom_text_pdQQkk": "<p>❌ You're shaking your hands out more often now.</p>",
        "custom_text_Fm3qaa": "<p>❌ Your thumb, index, and middle fingers feel half-asleep.</p>",
        "custom_text_BYd69L": "<p>❌ Opening a jar is a two-handed job now.</p>",
        "custom_text_XLBwJd": "<p>❌ You're Googling \"carpal tunnel without surgery\" at 2 AM.</p>",
    }
    for bid, text in hero_checks.items():
        b = sec["blocks"].get(bid)
        if b:
            set_setting(b, "text", text, bid)

    # 3 transition lines after the checkmarks
    transitions = {
        "custom_text_teazbd": "<p>You've tried everything they told you to try.</p>",
        "custom_text_LE8GRw": "<p><strong>Braces. Stretches. Heating pads. Pills that wreck your stomach.</strong> Maybe even a cortisone shot that wore off in weeks.</p>",
        "custom_text_hJbHX8": "<p><strong>But here's what nobody told you…</strong></p>",
    }
    for bid, text in transitions.items():
        b = sec["blocks"].get(bid)
        if b:
            set_setting(b, "text", text, bid)


# ---------------------------------------------------------------------------
# §3 PROBLEM AGITATION A — image_with_text_WPzJcE
# Heading: "Why Nothing You've Tried Has Worked"
# Paragraph: drawer/braces/pills/grandchild copy
# ---------------------------------------------------------------------------
def populate_agitation_a(sections):
    sec = sections.get("image_with_text_WPzJcE")
    if not sec:
        return

    # Section-level heading (not used by template — block heading carries it)
    set_setting(sec, "heading", "", "image_with_text_WPzJcE.section")

    blocks = sec.get("blocks", {})
    # heading block
    for bid, b in blocks.items():
        if b.get("type") == "heading":
            set_setting(b, "heading_text", "Why Nothing You've Tried Has Worked", f"agitation_a.{bid}")
            set_setting(b, "heading_accent", "", f"agitation_a.{bid}")
        elif b.get("type") == "paragraph":
            set_setting(b, "paragraph_text",
                "<p><strong>Here's what nobody tells you:</strong> Your drawer manages the pain. Nothing manages the losses.</p>"
                "<p>The jar you can't open. The button you can't fasten. The grandchild you hesitate to lift. Braces and pills don't bring any of that back.</p>"
                "<p><strong>And here's why they never will…</strong></p>",
                f"agitation_a.{bid}")


# ---------------------------------------------------------------------------
# §4 PROBLEM AGITATION B — rich_text_YkP6Md
# Title: "The Part Of You That Works Hardest — Gets Zero Recovery"
# Subtitle below: 100,000 micro-movements + Rested fixes
# ---------------------------------------------------------------------------
def populate_agitation_b(sections):
    sec = sections.get("rich_text_YkP6Md")
    if not sec:
        return

    blocks = sec.get("blocks", {})
    # Find the title block + subtitles by type
    titles = [(bid, b) for bid, b in blocks.items() if b.get("type") == "title"]
    subtitles = [(bid, b) for bid, b in blocks.items() if b.get("type") == "subtitle"]

    if titles:
        bid, b = titles[0]
        set_setting(b, "title", "The Part Of You That Works Hardest — Gets Zero Recovery", f"agitation_b.{bid}")
        set_setting(b, "accent_text", "", f"agitation_b.{bid}")

    # The two subtitle blocks: top = lead-in (empty/short), bottom = main paragraph
    if len(subtitles) >= 2:
        # First subtitle: short lead-in (could be empty)
        bid_top, b_top = subtitles[0]
        set_setting(b_top, "subtitle", "", f"agitation_b.{bid_top}")
        # Second subtitle: main paragraph
        bid_bot, b_bot = subtitles[1]
        set_setting(b_bot, "subtitle",
            "Your back gets a bed. Your feet get shoes. Your eyes get sleep. "
            "Your hands do 100,000 micro-movements a day — and get nothing. No tool, no care, no recovery. "
            "If arthritis or carpal tunnel has a grip on you, that recovery deficit is what nobody addresses. "
            "That's what Rested fixes.",
            f"agitation_b.{bid_bot}")
    elif len(subtitles) == 1:
        bid, b = subtitles[0]
        set_setting(b, "subtitle",
            "Your hands do 100,000 micro-movements a day — and get nothing. That's what Rested fixes.",
            f"agitation_b.{bid}")


# ---------------------------------------------------------------------------
# §5 SOLUTION REVEAL — image_with_text_yU6dxk
# H2 + paragraph + 4 ✅ benefits + CTA "TRY RISK-FREE TODAY"
# ---------------------------------------------------------------------------
def populate_solution_reveal(sections):
    sec = sections.get("image_with_text_yU6dxk")
    if not sec:
        return

    blocks = sec.get("blocks", {})
    for bid, b in blocks.items():
        bt = b.get("type")
        if bt == "heading":
            set_setting(b, "heading_text", "The Recovery Ritual Your Hands Have Been Missing", f"solution.{bid}")
            set_setting(b, "heading_accent", "", f"solution.{bid}")
        elif bt == "paragraph":
            set_setting(b, "paragraph_text",
                "<p>Creams numb the surface. Pills mask the pain. <strong>Rested drives heat and compression into "
                "swollen joints, nerves, and stiff tissue — what braces and PT cannot.</strong></p>"
                "<p>Fifteen minutes. One device. The recovery your hands earned.</p>"
                "<p><strong>Rested gives back what nothing else did.</strong></p>",
                f"solution.{bid}")
        elif bt == "bullet_list":
            set_setting(b, "list_item_1", "End the daily typing + gripping ache", f"solution.{bid}")
            set_setting(b, "list_item_2", "Sleep through without dead-hand wakeups", f"solution.{bid}")
            set_setting(b, "list_item_3", "Hold things without dropping them", f"solution.{bid}")
            set_setting(b, "list_item_4", "Pick up the hobby you quietly set down", f"solution.{bid}")
        elif bt == "button":
            set_setting(b, "button_label", "TRY RISK-FREE TODAY", f"solution.{bid}")
            set_setting(b, "button_redirect_type", "scroll_to_top", f"solution.{bid}")


# ---------------------------------------------------------------------------
# §6 OFFER ACCORDION — store_faq_pV3P8w (5 items)
# ---------------------------------------------------------------------------
def populate_offer_accordion(sections):
    sec = sections.get("store_faq_pV3P8w")
    if not sec:
        return

    set_setting(sec, "heading", "", "offer_accordion.section")
    set_setting(sec, "subtitle", "", "offer_accordion.section")

    accordion_items = [
        ("Description",
         "<p>The Rested Hand Recovery Device is a cordless, rechargeable therapy device that combines deep infrared heat (95°–122°F) with three-mode air compression — the two therapies most studied in clinical literature for arthritis and carpal tunnel pain.</p>"
         "<p>Each 15-minute session delivers joint-deep recovery: heat drives circulation into stiff tissue while cyclical compression decompresses nerves and eases swelling. Designed for daily use at home.</p>"
         "<p><em>This is a wellness device. Not a medical device. Rested does not diagnose, treat, cure, or prevent any disease. For persistent hand pain, consult your physician.</em></p>"),
        ("Why You Need Rested",
         "<p>If you've tried braces, stretches, creams, and pills — and your hands still ache, still drop things, still wake you at night — it's because none of those solutions deliver what research keeps showing hands need: daily heat and compression together.</p>"
         "<p>Rested was built around one idea: the recovery your hands actually earned, in a fifteen-minute ritual you'll actually do.</p>"),
        ("Benefits",
         "<ul>"
         "<li>Eases daily hand pain and chronic stiffness</li>"
         "<li>Improves grip strength over time</li>"
         "<li>Reduces numbness and tingling from median nerve compression</li>"
         "<li>Supports recovery for arthritis and carpal tunnel sufferers</li>"
         "<li>Helps you return to tasks you'd given up</li>"
         "<li>15-minute cordless sessions, usable anywhere</li>"
         "<li>No pills, no injections, no appointments</li>"
         "</ul>"),
        ("How To Use",
         "<p>Slide your hand into the device, press start, and let it run for one 15-minute cycle. Choose your heat level (3 settings) and compression mode (gentle, medium, deep) based on how your hands feel that day.</p>"
         "<p><strong>Most customers use Rested once daily</strong> — evening tends to work best for decompression before sleep. Consistency matters more than intensity: daily use over 3–4 weeks is where most people notice the real shift.</p>"
         "<p>Charge fully before first use. One charge delivers approximately 20 sessions.</p>"),
        ("Guarantee",
         "<p>Yes. Rested is backed by our full <strong>30-day money-back guarantee.</strong></p>"
         "<p>If your hands don't feel different in 30 days, send it back — we cover return shipping, no restocking fee, no questions asked.</p>"),
    ]

    block_order = sec.get("block_order", [])
    for i, (q, a) in enumerate(accordion_items):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "question", q, f"offer_accordion.faq{i+1}")
        set_setting(b, "answer", a, f"offer_accordion.faq{i+1}")


# ---------------------------------------------------------------------------
# §7 AUTHORITY — as_seen_in_logos_byrbEG (3 logos)
# Section title only here. Citation card images come in Phase 3 (Nano Banana
# generates 3 cards with text rendered). For Phase 2, set the section's
# section_title and leave logo blocks blank.
# ---------------------------------------------------------------------------
def populate_authority(sections):
    sec = sections.get("as_seen_in_logos_byrbEG")
    if not sec:
        return
    set_setting(sec, "section_title", "The Clinical Research Your Doctor Didn't Mention",
                "authority.section")


# ---------------------------------------------------------------------------
# §8 TESTIMONIALS — testimonials_44W6N3 (4 reviews)
# ---------------------------------------------------------------------------
def populate_testimonials(sections):
    sec = sections.get("testimonials_44W6N3")
    if not sec:
        return

    set_setting(sec, "heading", "They Didn't Believe It Either. Until Their Hands Worked Again.",
                "testimonials.section")
    set_setting(sec, "subtitle",
        "When braces, creams, and PT failed, here's what happened when they tried Rested.",
        "testimonials.section")

    testimonials = [
        {
            "title": "Haven't woken up with a dead hand in 3 weeks",
            "content": "I'm a designer, had CTS for like 4 years. Doctor was already pushing surgery. Tried this because honestly I'd tried everything. First week, eh, maybe. By week three I realized I hadn't shaken my hand out in days. I just sleep now. First thing that's actually done anything.",
            "author_name": "Rachel M — Austin, TX",
            "rating": 5,
            "verified": True,
        },
        {
            "title": "I knit again",
            "content": "Rheumatologist has me on basically every pill there is. They help but don't give back what you lost, you know? I gave up knitting two years ago — hands seized after 20 minutes. Started using this evenings. Three weeks in I picked up the needles. Knit for an hour. I cried.",
            "author_name": "Margaret D — Portland, OR",
            "rating": 5,
            "verified": True,
        },
        {
            "title": "Bought it to prove my wife wrong. She was right.",
            "content": "Wife has arthritis pretty bad. Kept seeing ads, I told her it's Amazon junk. She bought it anyway. Three days later she hands it to me. 15 minutes and I almost fell asleep. Ordered one for my mom.",
            "author_name": "David R — Cleveland, OH",
            "rating": 5,
            "verified": True,
        },
        {
            "title": "Stopped swapping hands on my tools",
            "content": "Been a mechanic 22 years. Right hand started locking up last winter — couldn't grip a socket wrench. Doc said arthritis in the thumb joint. Wife got me this for my birthday. Use it every night after shop. Three weeks in I stopped swapping hands on tools.",
            "author_name": "Mike T — Buffalo, NY",
            "rating": 5,
            "verified": True,
        },
    ]

    block_order = sec.get("block_order", [])
    for i, t in enumerate(testimonials):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        for k, v in t.items():
            set_setting(b, k, v, f"testimonial_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# §9a ICON BENEFITS — product_benefits_trbtD8 (4 benefit blocks)
# ---------------------------------------------------------------------------
def populate_icon_benefits(sections):
    sec = sections.get("product_benefits_trbtD8")
    if not sec:
        return

    set_setting(sec, "heading_regular", "Give Your Hands What They Actually Earned",
                "benefits.section")
    set_setting(sec, "subtitle",
        "From the daily ache of hands that work nonstop to the hobbies you'd quietly given up — what makes Rested different.",
        "benefits.section")

    benefits = [
        ("🔥 End The Daily Ache", "Stop the typing + gripping burn that builds by 3 PM."),
        ("🛌 Sleep Through The Night", "No more dead-hand wakeups at 2 AM."),
        ("✋ Hold Without Dropping", "Get your grip strength back, jar by jar."),
        ("🧶 Return To What You Loved", "Knit, paint, garden — whatever your hands gave up."),
    ]

    block_order = sec.get("block_order", [])
    for i, (title, desc) in enumerate(benefits):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "title", title, f"benefit_{i+1}.{bid}")
        set_setting(b, "description", desc, f"benefit_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# §9b HOBBY GRID — roadmap_MP3fN8 (4 roadmap_step blocks repurposed)
# ---------------------------------------------------------------------------
def populate_hobby_grid(sections):
    sec = sections.get("roadmap_MP3fN8")
    if not sec:
        return

    set_setting(sec, "heading", "Built For Hands That Used To", "hobby.section")
    set_setting(sec, "subheading", "Backed by clinical research.", "hobby.section")

    hobbies = [
        ("🎨", "Paint", "Steady brush. No mid-stroke wince."),
        ("🧶", "Knit", "An hour without seizing up."),
        ("⌨️", "Type Pain-Free", "Through the workday and beyond."),
        ("💪", "Grip Like Before", "Tools, jars, the dog leash — all of it."),
    ]

    block_order = sec.get("block_order", [])
    for i, (badge, title, desc) in enumerate(hobbies):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "badge_text", badge, f"hobby_{i+1}.{bid}")
        set_setting(b, "title", title, f"hobby_{i+1}.{bid}")
        set_setting(b, "description", desc, f"hobby_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# §10 USE CASE — image_with_text_USECASE_NEW
# ---------------------------------------------------------------------------
def populate_use_case(sections):
    sec = sections.get("image_with_text_USECASE_NEW")
    if not sec:
        return

    blocks = sec.get("blocks", {})
    for bid, b in blocks.items():
        bt = b.get("type")
        if bt == "heading":
            set_setting(b, "heading_text", "End Daily Hand Pain & Chronic Stiffness", f"usecase.{bid}")
            set_setting(b, "heading_accent", "", f"usecase.{bid}")
        elif bt == "paragraph":
            set_setting(b, "paragraph_text",
                "<p>Rested's compression cycle pumps inflammation out of swollen knuckles, "
                "easing stiffness and restoring grip within 3-6 weeks.</p>"
                "<p>Cyclical pressure release decompresses the median nerve, ending numbness within 4-6 weeks.</p>"
                "<p><strong>Old Hand Pain.</strong> Deep infrared heat drives circulation into joints worn down "
                "by years of typing and gripping — bringing function back to hands that "
                "&ldquo;haven't worked right in years&rdquo; within 4-8 weeks.</p>",
                f"usecase.{bid}")
        elif bt == "bullet_list":
            set_setting(b, "list_item_1", "End the daily ache", f"usecase.{bid}")
            set_setting(b, "list_item_2", "Heal pain that \"never got better\"", f"usecase.{bid}")
            set_setting(b, "list_item_3", "Get back to hobbies you gave up", f"usecase.{bid}")


# ---------------------------------------------------------------------------
# §11 STATS BLOCK — statistics_column_y9eLJy (3 statistic blocks)
# ---------------------------------------------------------------------------
def populate_stats(sections):
    sec = sections.get("statistics_column_y9eLJy")
    if not sec:
        return

    set_setting(sec, "heading", "After Everything Else Failed Them…", "stats.section")
    set_setting(sec, "subtitle", "Based on clinical research on heat + compression therapy.",
                "stats.section")

    stats = [
        ("89%", "Pain Reduction",
         "reported within 4 weeks when braces, creams, and PT had failed."),
        ("P ≤ 0.0001", "Statistical Significance",
         "on symptom severity, function, and pain in CTS patients on daily heat."),
        ("3-4 Weeks", "Time To Improvement",
         "in arthritic hand function with consistent heat + compression."),
    ]

    block_order = sec.get("block_order", [])
    for i, (number, title, desc) in enumerate(stats):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "number", number, f"stat_{i+1}.{bid}")
        set_setting(b, "title", title, f"stat_{i+1}.{bid}")
        set_setting(b, "description", desc, f"stat_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# §12 TIMELINE — store_features_QmUYDi (4 phases — repurposed from store-features)
# ---------------------------------------------------------------------------
def populate_timeline(sections):
    sec = sections.get("store_features_QmUYDi")
    if not sec:
        return

    set_setting(sec, "heading", "Your Hands' Journey With Rested", "timeline.section")

    phases = [
        ("Phase 1 — Subtle Improvements Begin",
         "The daily ache lifts faster. Sessions feel warm and good. You think maybe this is working but aren't sure yet."),
        ("Phase 2 — The Difference Becomes Obvious",
         "Your hands don't burn by 3 PM anymore. Sleep through without dead-hand wakeups. Family notices you're not wincing as much."),
        ("Phase 3 — You Start Believing Again",
         "Pick up the hobby you'd given up — knitting, piano, gardening. Pain levels drop noticeably. Feel hopeful about your hands for the first time in years."),
        ("Phase 4 — Like You Have Your Old Hands Back",
         "Stiffness reduced 70-80% from where you started. Grip restored. Others ask what you're doing differently because the change is so obvious."),
    ]

    block_order = sec.get("block_order", [])
    for i, (title, desc) in enumerate(phases):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "title", title, f"phase_{i+1}.{bid}")
        set_setting(b, "description", desc, f"phase_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# §13 FACEBOOK COMMENTS — facebook_comments_NEW (6 review blocks)
# ---------------------------------------------------------------------------
def populate_fb_comments(sections):
    sec = sections.get("facebook_comments_NEW")
    if not sec:
        return

    set_setting(sec, "title", "Don't Spend Another 6 Months Like They Did",
                "fb_comments.section")
    set_setting(sec, "badge_text", "Recently on Facebook", "fb_comments.section")

    comments = [
        ("Linda Kowalski",
         "Had carpal tunnel surgery on my left 4 years ago and was dreading the right. Daughter sent me Rested for Mother's Day. Six weeks in, the right hand isn't waking me up at night. Not racing to surgery anymore.",
         "2 weeks ago"),
        ("Mark T.",
         "60, type all day, wrists were toast by 3pm. 30 days on this — no more. Wish I'd bought it 10 years ago.",
         "3 weeks ago"),
        ("Janelle Foster",
         "Bought it for my mom (RA), ended up using it more than her. Hairstylist hands are ROUGH after a Saturday. Buying my own.",
         "1 week ago"),
        ("Phillip W.",
         "Skeptical husband. Wife wore me down. Tried it once. Bought a second for the office. Credit where it's due.",
         "5 days ago"),
        ("Susan R.",
         "The daily ache was the thing. Used to catch myself shaking my hand out between meetings. Twenty minutes at night and I don't do that anymore.",
         "1 month ago"),
        ("Anna L.",
         "My 78-year-old mother figured out how to use this without help. She calls it her \"after-dinner thing.\" Recommends to her bridge club.",
         "2 weeks ago"),
    ]

    block_order = sec.get("block_order", [])
    for i, (name, comment, date) in enumerate(comments):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "name", name, f"fb_{i+1}.{bid}")
        set_setting(b, "comment", comment, f"fb_{i+1}.{bid}")
        set_setting(b, "date", date, f"fb_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# §14 FAQ — store_faq_9hjxMb (8 questions)
# ---------------------------------------------------------------------------
def populate_faq(sections):
    sec = sections.get("store_faq_9hjxMb")
    if not sec:
        return

    set_setting(sec, "heading", "The Questions People Ask Before They Buy", "faq.section")

    faqs = [
        ("Is this just another cheap Amazon massager rebranded?",
         "<p>No. Rested runs therapeutic heat to 122°F (vs. 104°F on most Amazon devices), has a 5-hour cordless battery, and uses genuine compression — not just vibration. If you've tried a $40 Amazon device and felt nothing, Rested is built for the next tier.</p>"),
        ("I've had carpal tunnel for years. Will compression make nerve pain worse?",
         "<p>Right question. Rested's compression <em>cycles</em> between pressure and full release — the same protocol used in clinical CTS studies. The release phase decompresses the median nerve. Static compression (like a tight brace worn for hours) can worsen nerve pain. Cyclical compression does the opposite.</p>"),
        ("Will it fit my hand? My knuckles are swollen / my hands are small.",
         "<p>Rested fits hand sizes from women's XS to men's XL. The airbags expand around your hand — not the other way around. Arthritic knuckles won't pinch. If it doesn't fit, return it within 30 days for a full refund.</p>"),
        ("How long until I feel a difference?",
         "<p>First session: noticeably warmer, looser. Day 7: daily ache fades faster. Day 21: most report a real shift — fewer night wakeups, easier grip. Day 60: most stop thinking about their hands entirely. Clinical studies show measurable improvement at the 3-4 week mark with daily use.</p>"),
        ("I have a pacemaker / blood thinners / Raynaud's. Is this safe?",
         "<p>Rested uses gentle therapeutic heat (max 122°F) and air compression — no electrical stimulation, no magnetic fields. Pacemaker compatible. For blood thinners, Raynaud's, or any vascular condition, please consult your doctor. Full refund available within 30 days.</p>"),
        ("What if I don't feel a difference in 30 days?",
         "<p>You don't pay. Send it back. We cover return shipping. No restocking fee. No \"tell us why\" survey. We're confident because the people who use Rested daily don't return it.</p>"),
        ("Can I use it on both hands?",
         "<p>Yes. Switch between left and right between sessions. Most people do one hand per fifteen-minute cycle.</p>"),
        ("Is it quiet enough to use during a call or meeting?",
         "<p>Whisper-quiet — quieter than a laptop fan. Use it during Zoom without anyone noticing.</p>"),
    ]

    block_order = sec.get("block_order", [])
    for i, (q, a) in enumerate(faqs):
        if i >= len(block_order):
            break
        bid = block_order[i]
        b = sec["blocks"][bid]
        set_setting(b, "question", q, f"faq_{i+1}.{bid}")
        set_setting(b, "answer", a, f"faq_{i+1}.{bid}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main() -> None:
    backup(PRODUCT_JSON)
    p = load(PRODUCT_JSON)
    sections = p.get("sections", {})

    populate_hero(sections)
    populate_agitation_a(sections)
    populate_agitation_b(sections)
    populate_solution_reveal(sections)
    populate_offer_accordion(sections)
    populate_authority(sections)
    populate_testimonials(sections)
    populate_icon_benefits(sections)
    populate_hobby_grid(sections)
    populate_use_case(sections)
    populate_stats(sections)
    populate_timeline(sections)
    populate_fb_comments(sections)
    populate_faq(sections)

    save(PRODUCT_JSON, p)

    # Re-parse to verify
    load(PRODUCT_JSON)

    print(f"\n=== Phase 2 changes ({len(changes)}) ===")
    for c in changes:
        print(f"  • {c}")

    print(f"\nTotal: {len(changes)} field updates across 14 sections.")


if __name__ == "__main__":
    main()
