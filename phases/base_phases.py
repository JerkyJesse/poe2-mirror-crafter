ORB_COLORS = {
    "Blacksmith's Whetstone": (55, 55, 70),
    "Perfect Orb of Transmutation": (45, 100, 150),
    "Perfect Orb of Augmentation": (40, 95, 165),
    "Perfect Regal Orb": (155, 125, 35),
    "Perfect Chaos Orb": (160, 30, 30),
    "Perfect Exalted Orb": (165, 145, 40),
    "Orb of Annulment": (100, 95, 90),
    "Divine Orb": (165, 130, 35),
    "Fracturing Orb": (160, 70, 35),
    "Omen of Whittling": (95, 40, 35),
    "Artificer's Orb": (95, 75, 65),
    "Vaal Blacksmith's Infuser": (170, 35, 30),
    "Omen of Dextral Coronation": (80, 50, 50),
    "Omen of Dextral Erasure": (120, 30, 30),
    "Omen of Dextral Annulment": (95, 50, 50),
    "Omen of Dextral Exaltation": (110, 75, 45),
    "Omen of Sinistral Coronation": (50, 80, 50),
    "Omen of Sinistral Erasure": (30, 120, 30),
    "Omen of Sinistral Annulment": (50, 95, 50),
    "Omen of Sinistral Exaltation": (75, 110, 45),
    "Omen of Greater Exaltation": (130, 105, 35),
    "Omen of Greater Annulment": (80, 40, 80),
    "Omen of Abyssal Echoes": (60, 60, 120),
    "Omen of Sanctification": (180, 80, 60),
    "Hinekora's Lock": (180, 140, 50),
}

ORB_COLORS.update({
    "Armourer's Scrap": (55, 55, 70),
    "Perfect Orb of Annulment": (100, 95, 90),
    "Perfect Orb of Exaltation": (165, 145, 40),
    "Orb of Alchemy": (140, 115, 30),
    "Catalyst": (120, 90, 150),
    "Distilled Emotion": (80, 150, 170),
    "Flesh Catalyst": (180, 60, 60),
    "Neural Catalyst": (60, 120, 180),
    "Carapace Catalyst": (80, 80, 60),
    "Reaver Catalyst": (180, 100, 50),
    "Sibilant Catalyst": (100, 60, 160),
    "Skittering Catalyst": (160, 160, 60),
    "Adaptive Catalyst": (140, 100, 60),
    "Necrotic Catalyst": (80, 60, 100),
    "Xoph's Catalyst": (200, 60, 40),
    "Tul's Catalyst": (40, 140, 200),
    "Esh's Catalyst": (140, 100, 200),
    "Chayula's Catalyst": (160, 40, 160),
    "Uul-Netol's Catalyst": (100, 80, 70),
})

def _fmt_keep_list(items):
    """Format a list of S-Tier keep items into indented bullet lines."""
    if not items:
        return ""
    return "\n".join(f"  {item}" for item in items)


def _fmt_trash_list(items):
    """Format a list of trash mods into indented bullet lines."""
    if not items:
        return ""
    return "\n".join(f"  {item}" for item in items)


def _apply_alternatives(step, step_id, alternatives):
    """If alternatives exist for this step_id, attach them to the step dict."""
    if step_id in alternatives:
        step["alternatives"] = alternatives[step_id]
    return step


def build_phases(custom):
    """Build the complete 10-phase crafting guide from a customization dict.

    Returns a list of 10 phase dicts, each containing a list of step dicts.
    """
    alternatives = custom.get("alternatives", {})
    orbs_override = custom.get("orbs_used_overrides", {})
    item_type = custom.get("item_type", "weapon")

    # ------------------------------------------------------------------
    # Phase 1: Acquire & Prepare Base
    # ------------------------------------------------------------------
    phase1_steps = [
        {
            "id": "1.1",
            "title": "Choose Base Type",
            "description": (
                "Pick the base with the best implicit for your build:\n"
                "  - Highest base attack speed / defence\n"
                "  - Best implicit mod (crit, stun, splash, chain, etc.)\n"
                "  - Correct attribute requirements\n"
                "Check poe2db.tw for all base variants."
            ),
            "orbs_used": [],
            "action": "Inspect bases on trade site or stash",
        },
        {
            "id": "1.2",
            "title": "Verify Item Level",
            "description": (
                "Hold ALT while hovering the item.\n"
                "You need ilvl 82+. ilvl 84+ is ideal.\n\n"
                "High ilvl bases drop from:\n"
                "  - Tier 15+ Waystones\n"
                "  - Breachstones / Simulacrum\n"
                "  - Pinnacle bosses"
            ),
            "orbs_used": [],
            "action": "ALT-hover item to check ilvl",
        },
        {
            "id": "1.3",
            "title": custom.get("quality_step_title", "Apply Quality"),
            "description": custom.get(
                "quality_step_desc",
                "Apply quality currency to max-out base quality.\n"
                "Consult custom quality data for specific counts.",
            ),
            "orbs_used": orbs_override.get(
                "1.3", [custom.get("quality_currency", "Blacksmith's Whetstone")]
            ),
            "action": "Apply quality currency",
        },
    ]

    # Step 1.4 — Exceptional Base (custom or generic)
    exc_step = custom.get("exceptional_base_step")
    if exc_step is not None:
        phase1_steps.append(exc_step)
    else:
        phase1_steps.append({
            "id": "1.4",
            "title": "Exceptional Base + Infuser",
            "description": (
                "The base item MUST be Exceptional tier (best in class)\n"
                "with a +1 extra Socket implicit modifier.\n\n"
                "Use Vaal Blacksmith's Infuser x2 to overcap quality\n"
                "beyond the 20% quality cap.\n"
                "Each Infuser adds random quality (1-5%) past\n"
                "the cap — it is NOT guaranteed to hit 5% per use.\n"
                "You get exactly 2 Infuser attempts. Whatever\n"
                "quality you land is final.\n\n"
                "+1 extra Socket means the item can hold an\n"
                "additional rune, giving it 2-3 rune sockets total."
            ),
            "orbs_used": ["Vaal Blacksmith's Infuser"],
            "action": "Confirm Exceptional base + 2x Vaal Blacksmith's Infuser for extra quality",
        })

    phase1 = {
        "name": "Phase 1: Acquire & Prepare Base",
        "number": 1,
        "icon": "base",
        "steps": phase1_steps,
    }

    # ------------------------------------------------------------------
    # Phase 2: Magic Stage
    # ------------------------------------------------------------------
    s_tier_keep = custom.get("s_tier_keep", [])
    s_tier_trash = custom.get("s_tier_trash", [])
    s_tier_consider = custom.get("s_tier_consider", [])

    keep_text = _fmt_keep_list(s_tier_keep)
    trash_text = _fmt_trash_list(s_tier_trash)
    consider_text = _fmt_keep_list(s_tier_consider) if s_tier_consider else ""

    check_desc = "S-TIER (KEEP):\n" + keep_text + "\n\nTRASH (START OVER):\n" + trash_text
    if consider_text:
        check_desc += "\n\nCONSIDER (situational):\n" + consider_text

    phase2_steps = [
        {
            "id": "2.1",
            "title": "Perfect Transmutation",
            "description": (
                "Apply Perfect Orb of Transmutation to white base.\n"
                "Min Mod Level: 50 — filters out all low-tier trash.\n"
                "Cost: ~0.02 div per attempt."
            ),
            "orbs_used": ["Perfect Orb of Transmutation"],
            "action": "Use Perfect Transmutation on base",
        },
        {
            "id": "2.2",
            "title": "Check Mod - TRASH?",
            "description": check_desc,
            "orbs_used": [],
            "action": "Check the mod tier and type",
        },
        {
            "id": "2.3",
            "title": "Perfect Augmentation",
            "description": (
                "Apply Perfect Orb of Augmentation (2nd mod).\n"
                "Min Mod Level: 50.\n"
                "Cost: ~0.02 div per attempt.\n\n"
                "Both mods must be T1-T2 and useful.\n"
                "If either is trash: THROW AWAY BASE, start over."
            ),
            "orbs_used": ["Perfect Orb of Augmentation"],
            "action": "Use Perfect Augmentation on magic item",
        },
        {
            "id": "2.4",
            "title": "Verify Both Mods",
            "description": (
                "PROCEED: Both mods T1-T2 + useful for build.\n"
                "CONSIDER: One T1 + one T2-T3 that's usable.\n"
                "TRASH: Either mod below T3 or useless.\n\n"
                "Expected: 10-30 attempts to find double-keeper.\n"
                "Don't proceed with mediocre magic item!"
            ),
            "orbs_used": [],
            "action": "Evaluate both mods — trash or keep?",
        },
    ]

    phase2 = {
        "name": "Phase 2: Magic Stage",
        "number": 2,
        "icon": "magic",
        "steps": phase2_steps,
    }

    # ------------------------------------------------------------------
    # Phase 3: Regal & Isolate T1
    # ------------------------------------------------------------------
    regal_omen_note = custom.get("regal_omen_note", "")

    step_3_1_desc = (
        "Apply Perfect Regal Orb: Magic -> Rare (+1 mod).\n"
        "Min Mod Level: 50. Cost: ~0.1 div.\n\n"
        "Use Coronation Omen for direction:\n"
        "  - 1P+1S (balanced): skip omen, let it be random\n"
        "  - 2 prefixes: Omen of Dextral Coronation -> force suffix\n"
        "  - 2 suffixes: Omen of Sinistral Coronation -> force prefix"
    )
    if regal_omen_note:
        step_3_1_desc += "\n\n" + regal_omen_note

    step_3_1 = _apply_alternatives(
        {
            "id": "3.1",
            "title": "Perfect Regal Orb",
            "description": step_3_1_desc,
            "orbs_used": orbs_override.get(
                "3.1", ["Perfect Regal Orb", "Omen of Dextral Coronation"]
            ),
            "action": "Use Perfect Regal Orb (consider Coronation Omen)",
        },
        "3.1",
        alternatives,
    )

    fracture_priority = custom.get("fracture_priority", [])
    fp_text = "\n".join(f"  - {item}" for item in fracture_priority) if fracture_priority else ""

    phase3_steps = [
        step_3_1,
        {
            "id": "3.2",
            "title": "Identify #1 Fracture Target",
            "description": (
                "Which mod is your #1 priority for fracture?\n"
                + fp_text + "\n\n"
                "If #1 is already present: skip to Annul step.\n"
                "If missing: proceed to Chaos spam step."
            ),
            "orbs_used": [],
            "action": "Decide your fracture target mod",
        },
        {
            "id": "3.3",
            "title": "Perfect Chaos Spam (if needed)",
            "description": (
                "Use Perfect Chaos Orbs + Erasure Omens.\n"
                "Perfect Chaos min mod level: 50.\n"
                "~5.18 div per Perfect Chaos Orb.\n"
                "Erasure Omens ~10 div each.\n\n"
                "WARNING: May burn dozens before finding target.\n"
                "If both magic-stage mods are strong, skip this."
            ),
            "orbs_used": ["Perfect Chaos Orb", "Omen of Dextral Erasure"],
            "action": "Spam Perfect Chaos until #1 T1 appears",
        },
        {
            "id": "3.4",
            "title": "Targeted Annul",
            "description": (
                "Use Annulment Orbs + directional Omens.\n"
                "Protect your T1:\n"
                "  - T1 is prefix: Omen of Dextral Annulment + Annul\n"
                "  - T1 is suffix: Omen of Sinistral Annulment + Annul\n\n"
                "Annul Omens ~14 div each. Expensive but saves your T1."
            ),
            "orbs_used": ["Orb of Annulment", "Omen of Dextral Annulment"],
            "action": "Annul unwanted mods with directional omens",
        },
        {
            "id": "3.5",
            "title": "Ensure 4+ Mods",
            "description": (
                "Fracturing Orb requires 4+ affixes.\n"
                "If below 4, use Perfect Exalted + directional Omens\n"
                "to fill back to 4+.\n\n"
                "Fewer mods = higher fracture chance (max 25% at 4)."
            ),
            "orbs_used": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
            "action": "Fill to exactly 4 mods for best fracture odds",
        },
    ]

    phase3 = {
        "name": "Phase 3: Regal & Isolate T1",
        "number": 3,
        "icon": "regal",
        "steps": phase3_steps,
    }

    # ------------------------------------------------------------------
    # Phase 4: Fracture
    # ------------------------------------------------------------------
    phase4_steps = [
        {
            "id": "4.1",
            "title": "Apply Fracturing Orb",
            "description": (
                "Use Fracturing Orb on the 4-mod rare item.\n"
                "Locks ONE random mod permanently.\n"
                "Cost: ~10 div per Fracturing Orb.\n\n"
                "With 4 mods, 1 desired: 25% success chance.\n"
                "Expected: ~4 attempts = ~40 div total."
            ),
            "orbs_used": ["Fracturing Orb"],
            "action": "Apply Fracturing Orb and pray to RNG",
        },
        {
            "id": "4.2",
            "title": "Evaluate Fracture Result",
            "description": (
                "SUCCESS: It locked your desired T1 mod!\n"
                "  -> Proceed to Phase 5. Best outcome.\n\n"
                "FAILURE: It fractured a different mod.\n"
                "  -> Item is bricked for your purposes.\n"
                "  -> Reforging Bench (3 bricks -> 1 roll)\n"
                "  -> Start over from Phase 1.\n\n"
                "The fractured mod is PERMANENT and cannot be removed."
            ),
            "orbs_used": [],
            "action": "Check which mod got fractured",
        },
    ]

    phase4 = {
        "name": "Phase 4: Fracture",
        "number": 4,
        "icon": "fracture",
        "steps": phase4_steps,
    }

    # ------------------------------------------------------------------
    # Phase 5: Clean Up
    # ------------------------------------------------------------------
    phase5_steps = [
        {
            "id": "5.1",
            "title": "Annul Non-Fractured Mods",
            "description": (
                "The fractured mod is locked and cannot be removed.\n"
                "Use targeted Annulment Omens to strip everything else:\n"
                "  - All suffix junk: Omen of Sinistral Annulment + Annul\n"
                "  - All prefix junk: Omen of Dextral Annulment + Annul\n\n"
                "Annul Orbs skip fractured mods automatically."
            ),
            "orbs_used": ["Orb of Annulment", "Omen of Dextral Annulment", "Omen of Sinistral Annulment"],
            "action": "Strip all non-fractured mods with targeted annuls",
        },
        {
            "id": "5.2",
            "title": "Clean Slate Ready",
            "description": (
                "You now have a rare item with ONLY the fractured T1 mod.\n"
                "PoE2 allows 1-mod rare items (unlike PoE1).\n\n"
                "Optional: Use Coronation Omen + Perfect Regal\n"
                "to add a mod in a specific direction first.\n"
                "Or go straight to Exalting in Phase 6."
            ),
            "orbs_used": [],
            "action": "Confirm clean slate ready for Phase 6",
        },
    ]

    phase5 = {
        "name": "Phase 5: Clean Up",
        "number": 5,
        "icon": "annul",
        "steps": phase5_steps,
    }

    # ------------------------------------------------------------------
    # Phase 6: Fill Slots
    # ------------------------------------------------------------------
    step_6_1 = _apply_alternatives(
        {
            "id": "6.1",
            "title": "Fill Suffixes First",
            "description": (
                "Use Omen of Dextral Exaltation + Perfect Exalted Orb\n"
                "to fill all 3 suffix slots.\n\n"
                "Perfect Exalted: min mod level 50.\n"
                "~2.83 div per orb. Omen ~6 div each.\n\n"
                "Fill one side completely before the other\n"
                "to avoid accidentally filling wrong side."
            ),
            "orbs_used": orbs_override.get("6.1", ["Perfect Exalted Orb", "Omen of Dextral Exaltation"]),
            "action": "Fill suffixes with Perfect Exalts + Omen of Dextral Exaltation",
        },
        "6.1",
        alternatives,
    )

    phase6_steps = [
        step_6_1,
        {
            "id": "6.2",
            "title": "Fill Prefixes",
            "description": (
                "Use Omen of Sinistral Exaltation + Perfect Exalted Orb\n"
                "to fill remaining prefix slots.\n\n"
                "If a Perfect Exalt adds a low-tier mod:\n"
                "  DO NOT annul immediately if on correct side.\n"
                "  Wait until all 6 slots filled, then Whittling (Phase 7)."
            ),
            "orbs_used": ["Perfect Exalted Orb", "Omen of Sinistral Exaltation"],
            "action": "Fill prefixes with Perfect Exalts + Omen of Sinistral Exaltation",
        },
        {
            "id": "6.3",
            "title": "Verify 6/6 Mods",
            "description": (
                "You should now have 6 mods (3P + 3S).\n"
                "The fractured T1 is protected.\n"
                "Some mods may be below T1 — that's fine.\n"
                "Whittling (Phase 7) will fix them.\n\n"
                "If using Greater Exaltation Omen:\n"
                "adds 2 mods at once (faster, less control). ~1 div."
            ),
            "orbs_used": [],
            "action": "Confirm all 6 mod slots are filled",
        },
    ]

    phase6 = {
        "name": "Phase 6: Fill Slots",
        "number": 6,
        "icon": "exalt",
        "steps": phase6_steps,
    }

    # ------------------------------------------------------------------
    # Phase 7: Whittling
    # ------------------------------------------------------------------
    step_7_1 = _apply_alternatives(
        {
            "id": "7.1",
            "title": "Begin Whittling Loop",
            "description": (
                "Omen of Whittling forces Chaos to remove LOWEST ilvl mod.\n"
                "Use with Perfect Chaos Orb (min mod level 50).\n\n"
                "Cost per attempt:\n"
                "  Omen of Whittling: ~15 div\n"
                "  Perfect Chaos Orb:  ~5 div\n"
                "  TOTAL:              ~20 div per attempt"
            ),
            "orbs_used": ["Perfect Chaos Orb", "Omen of Whittling"],
            "action": "Start Whittling: Omen of Whittling + Perfect Chaos",
        },
        "7.1",
        alternatives,
    )

    phase7_steps = [
        step_7_1,
        {
            "id": "7.2",
            "title": "Evaluate Each Whittling",
            "description": (
                "After each Whittling attempt:\n"
                "  a) Removed low-tier, added T1 -> Progress!\n"
                "  b) Removed low-tier, added non-T1 -> Continue\n"
                "  c) Removed a T1 (rare) -> Stop, reassess\n\n"
                "T1 mods have high ilvl requirements,\n"
                "so they're usually safe from Whittling."
            ),
            "orbs_used": [],
            "action": "Check which mod was removed/replaced",
        },
        {
            "id": "7.3",
            "title": "Repeat Until All T1",
            "description": (
                "Continue Whittling until ALL 6 mods are T1.\n\n"
                "Budget estimate:\n"
                "  ~4 non-T1 mods x ~5 attempts x ~20 div = ~400 div\n"
                "  (Conservative — bad luck can double/triple this)\n\n"
                "Budget alternative: Perfect Chaos without omens.\n"
                "~5 div/attempt but REMOVES RANDOM MOD (can hit T1)."
            ),
            "orbs_used": [],
            "action": "Repeat Whittling until 6x T1 achieved",
        },
    ]

    phase7 = {
        "name": "Phase 7: Whittling",
        "number": 7,
        "icon": "whittle",
        "steps": phase7_steps,
    }

    # ------------------------------------------------------------------
    # Phase 8: Divine
    # ------------------------------------------------------------------
    phase8_steps = [
        {
            "id": "8.1",
            "title": "Check Roll Ranges",
            "description": (
                "All 6 mods are T1 but numeric values vary.\n"
                "Hold ALT to see tier and roll range for each mod.\n\n"
                "Know which mods matter most for your build.\n"
                "Prioritize them for divine targets."
            ),
            "orbs_used": [],
            "action": "ALT-hover to check roll ranges",
        },
        {
            "id": "8.2",
            "title": "Divine Orb Spam",
            "description": (
                "Divine Orbs reroll ALL numeric values simultaneously.\n"
                "Each mod rerolls independently within its tier range.\n"
                "Cost: ~1 div per Divine Orb.\n\n"
                "Can take 10-200+ Divines depending on mod pool.\n"
                "Some T1 ranges are tight (95-100%), others wide (50-100%)."
            ),
            "orbs_used": ["Divine Orb"],
            "action": "Use Divine Orbs until rolls are satisfactory",
        },
        {
            "id": "8.3",
            "title": "Know When to Stop",
            "description": (
                "For mirror service: all mods must be perfect/near-perfect.\n"
                "For personal use: 95th percentile is usually fine.\n\n"
                "A true perfect 6x T1 max-roll item is exponentially rarer\n"
                "than 'good enough' and may not be worth the extra cost."
            ),
            "orbs_used": [],
            "action": "Decide if rolls are good enough or keep divining",
        },
    ]

    phase8 = {
        "name": "Phase 8: Divine",
        "number": 8,
        "icon": "divine",
        "steps": phase8_steps,
    }

    # ------------------------------------------------------------------
    # Phase 9: Finalize (custom)
    # ------------------------------------------------------------------
    phase9_steps = custom.get("phase9_steps", [
        {
            "id": "9.1",
            "title": "Insert Runes",
            "description": (
                "Common rune choices:\n"
                "  Iron (phys)  |  Storm (lightning)  |  Desert (fire)\n"
                "  Glacier (cold)  |  Soul (spell, mana)\n\n"
                "Use Perfect Runes for max effect if budget allows."
            ),
            "orbs_used": [],
            "action": "Insert appropriate runes into sockets",
        },
        {
            "id": "9.2",
            "title": "Craft Complete!",
            "description": custom.get(
                "completed_message",
                "Your 6x T1 mirror-tier item is complete.\n"
                "Total estimated cost: 600-1,100+ div (conservative).\n"
                "Bad RNG can push this to 2,000-5,000+ div.\n\n"
                "You now hold an item that can compete\n"
                "for mirror service on the trade market.\n\n"
                "GG, Exile.",
            ),
            "orbs_used": [],
            "action": custom.get(
                "craft_action",
                "Admire your completed mirror-tier item",
            ),
        },
    ])

    phase9 = {
        "name": "Phase 9: " + custom.get("phase9_title", "Finalize"),
        "number": 9,
        "icon": "socket",
        "steps": phase9_steps,
    }

    # ------------------------------------------------------------------
    # Phase 10: Sanctify
    # ------------------------------------------------------------------
    step_10_2 = _apply_alternatives(
        {
            "id": "10.2",
            "title": "Sanctify with Divine Orb",
            "description": (
                "Use a Divine Orb to sanctify the item.\n"
                "A successful sanctify UPGRADES one modifier\n"
                "to a higher tier (e.g. T1 -> T0, +4 -> +5 skills).\n\n"
                "Success rate: ~13% per Divine Orb.\n"
                "Expected: ~7-8 Divine Orbs per successful sanctify.\n\n"
                "OMEN OF SANCTIFICATION (~0.4 div each):\n"
                "Guarantees your next Divine Orb WILL sanctify.\n"
                "100% success rate -- use on expensive crafts\n"
                "to avoid burning through Divine Orbs.\n\n"
                "HINEKORA'S LOCK (optional, ~150 div each):\n"
                "Use before sanctifying to preview the outcome.\n"
                "If the preview is bad, modify the item to change\n"
                "the seed; the Lock is consumed regardless.\n"
                "Locks are strongly recommended on high-value items."
            ),
            "orbs_used": ["Divine Orb", "Omen of Sanctification", "Hinekora's Lock"],
            "action": "Apply Divine Orb (with Omen/Lock) to sanctify",
        },
        "10.2",
        alternatives,
    )

    phase10_steps = [
        {
            "id": "10.1",
            "title": "Final Preparations",
            "description": (
                "Before sanctifying, ensure EVERYTHING is done:\n"
                "  - All 6 mods are T1 (Phase 7)\n"
                "  - Rolls are satisfactory (Phase 8)\n"
                "  - Runes inserted into sockets (Phase 9)\n"
                "  - Quality capped at maximum\n"
                "  - Anointed if applicable\n\n"
                "Sanctifying is FINAL and irreversible\n"
                "without a Hinekora's Lock preview.\n"
                "Do NOT skip any prior steps."
            ),
            "orbs_used": [],
            "action": "Double-check all preparations are complete",
        },
        step_10_2,
        {
            "id": "10.3",
            "title": "Sanctification Complete",
            "description": (
                "SUCCESS: A modifier tier has been upgraded!\n"
                "Your item now has a T0 or enhanced mod\n"
                "that normal crafting cannot achieve.\n\n"
                "FAILURE: The sanctify attempt failed.\n"
                "The item is unchanged — you can try again\n"
                "with another Divine Orb.\n\n"
                "Sanctified mods stack with catalysts/quality\n"
                "for exponential effect on your final values.\n\n"
                "Your sanctified mirror-tier item is complete.\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Evaluate the sanctify result",
        },
    ]

    phase10 = {
        "name": custom.get("phase10_title", "Phase 10: Sanctify"),
        "number": 10,
        "icon": "divine",
        "steps": phase10_steps,
    }

    return [phase1, phase2, phase3, phase4, phase5, phase6, phase7, phase8, phase9, phase10]
