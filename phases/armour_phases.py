def _make_alternatives():
    return {
        "3.1": {
            "title": "Alternative: Perfect Chaos + Erasure",
            "description": (
                "Use Perfect Chaos + Omen of Dextral Erasure instead of Regal.\n"
                "Sometimes spamming chaos with an erasure omen is better control\n"
                "than regaling and hoping for the right direction.\n"
                "Cost: ~15 div per attempt vs ~0.1 div for Regal.",
            ),
            "orbs_used": ["Perfect Chaos Orb", "Omen of Dextral Erasure"],
            "action": "Spam Perfect Chaos + Erasure Omen",
        },
        "6.1": [
                {
                    "label": "Standard Exaltation (Recommended)",
                    "cost": "~9 div per mod",
                    "risk": "low",
                    "description": "Use Omen of Dextral Exaltation + Perfect Exalted Orb. One suffix at a time with full directional control. ~3 div per Exalt, ~6 div per Omen.",
                },
                {
                    "label": "Add Greater Exaltation Omen (2x mods)",
                    "cost": "+~1 div (Greater Omen)",
                    "risk": "low",
                    "description": "Stack Greater Exaltation Omen with Dextral Exaltation. Both omens work together: 2 guaranteed-suffix mods per Exalt instead of 1. Halves the number of Exalts needed.",
                },
            ],
        "6.2": [
                {
                    "label": "Standard Exaltation (Recommended)",
                    "cost": "~9 div per mod",
                    "risk": "low",
                    "description": "Use Omen of Sinistral Exaltation + Perfect Exalted Orb. One prefix at a time with full directional control. ~3 div per Exalt, ~6 div per Omen.",
                },
                {
                    "label": "Add Greater Exaltation Omen (2x mods)",
                    "cost": "+~1 div (Greater Omen)",
                    "risk": "low",
                    "description": "Stack Greater Exaltation Omen with Sinistral Exaltation. Both omens work together: 2 guaranteed-prefix mods per Exalt instead of 1. Halves the number of Exalts needed.",
                },
            ],
        "7.1": {
            "title": "Alternative: Omen of Dextral Annulment + Perfect Exalt",
            "description": (
                "Instead of Whittling, use Dextral Annulment + Perfect Exalt.\n"
                "Annul removes a suffix, Exalt fills it back T1.\n"
                "Cost: ~20 div per attempt. Higher chance of T1 result\n"
                "than Whittling but also harder to hit T1 on exalt.\n\n"
                "Better when: you have 1-2 bad suffixes, rest T1.",
            ),
            "orbs_used": ["Orb of Annulment", "Omen of Dextral Annulment", "Perfect Exalted Orb"],
            "action": "Annul suffix + Perfect Exalt fill",
        },
        "10.2": [
            {
                "label": "Use Omen of Sanctification (Guaranteed)",
                "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                "risk": "very low",
                "description": "Omen of Sanctification guarantees 100% sanctify success. Skip the RNG entirely for ~0.4 div.",
            },
            {
                "label": "YOLO Sanctify (No Lock)",
                "cost": "~1 div per Divine Orb",
                "risk": "medium",
                "description": "13% success rate. No Lock, no Omen. ~7-8 attempts expected on average.",
            },
            {
                "label": "Lock + Sanctification Omen (Ultimate Safety)",
                "cost": "~151.4 div (Lock ~150 + Divine ~1 + Omen ~0.4)",
                "risk": "very low",
                "description": "Combine Hinekora's Lock (preview outcome) with Omen of Sanctification (guaranteed success). Preview the sanctify and if the result is good, the Omen guarantees it lands.",
            },
        ],
    }


_STANDARD_ALTERNATIVES = _make_alternatives()

_STANDARD_ORBS_OVERRIDES = {
    "1.3": ["Armourer's Scrap"],
    "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
    "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
}

_BASE_TRASH = [
    "Any mod below T3 tier",
    "Light Radius",
    "Stun and Block Recovery",
    "Thorns/Reflect damage",
    "Life/Mana on kill",
    "Reduced Attribute Requirements (unless needed)",
]

# ---------------------------------------------------------------------------
# Phase 9 shared helper
# ---------------------------------------------------------------------------

def _boots_phase9():
    return [
        {
            "id": "9.1",
            "title": "Insert Runes",
            "description": (
                "Boots can have rune sockets.\n"
                "Use Artificer's Orbs to add sockets.\n\n"
                "Boots rune recommendations:\n"
                "  Iron Rune (if phys mitigation needed)\n"
                "  Stone Rune (stun threshold/armour)\n"
                "  Desert/Storm/Glacier Rune (resists)\n"
                "  Soul Rune (if ES hybrid)\n\n"
                "Use Perfect Runes for maximum effect."
            ),
            "orbs_used": ["Artificer's Orb"],
            "action": "Apply Artificer's Orbs for sockets + insert runes",
        },
        {
            "id": "9.2",
            "title": "Craft Complete!",
            "description": (
                "Your 6x T1 mirror-tier boots are complete.\n"
                "Total estimated cost: 400-800+ div (conservative).\n"
                "Movement Speed on boots is the most important suffix\n"
                "in the game — this piece literally drives your build.\n\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Admire your completed mirror-tier boots",
        },
    ]


def _gloves_phase9():
    return [
        {
            "id": "9.1",
            "title": "Insert Runes",
            "description": (
                "Gloves can have rune sockets.\n"
                "Use Artificer's Orbs to add sockets.\n\n"
                "Gloves rune recommendations:\n"
                "  Iron Rune (if phys mitigation needed)\n"
                "  Stone Rune (stun threshold/armour)\n"
                "  Desert/Storm/Glacier Rune (resists)\n"
                "  Soul Rune (if ES hybrid)\n\n"
                "Use Perfect Runes for maximum effect."
            ),
            "orbs_used": ["Artificer's Orb"],
            "action": "Apply Artificer's Orbs for sockets + insert runes",
        },
        {
            "id": "9.2",
            "title": "Craft Complete!",
            "description": (
                "Your 6x T1 mirror-tier gloves are complete.\n"
                "Total estimated cost: 400-800+ div (conservative).\n"
                "Gloves are the only armour slot that rolls attack mods —\n"
                "flat damage and attack speed make this piece a damage engine.\n\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Admire your completed mirror-tier gloves",
        },
    ]


def _shield_phase9():
    return [
        {
            "id": "9.1",
            "title": "Insert Runes",
            "description": (
                "Shields can have rune sockets.\n"
                "Use Artificer's Orbs to add sockets.\n\n"
                "Shield rune recommendations:\n"
                "  Iron Rune (phys mitigation / block)\n"
                "  Stone Rune (stun threshold)\n"
                "  Desert/Storm/Glacier Rune (resists)\n"
                "  Soul Rune (if ES shield)\n\n"
                "Use Perfect Runes for maximum effect."
            ),
            "orbs_used": ["Artificer's Orb"],
            "action": "Apply Artificer's Orbs for sockets + insert runes",
        },
        {
            "id": "9.2",
            "title": "Craft Complete!",
            "description": (
                "Your 6x T1 mirror-tier shield is complete.\n"
                "A perfect shield defines a build's maximum tank —\n"
                "this piece dramatically increases your effective HP.\n\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Admire your completed mirror-tier shield",
        },
    ]


def _focus_phase9():
    return [
        {
            "id": "9.1",
            "title": "Insert Runes",
            "description": (
                "Foci can have rune sockets.\n"
                "Use Artificer's Orbs to add sockets.\n\n"
                "Focus rune recommendations:\n"
                "  Soul Rune (spell damage, ES)\n"
                "  Desert/Storm/Glacier Rune (resists)\n\n"
                "Use Perfect Runes for maximum effect."
            ),
            "orbs_used": ["Artificer's Orb"],
            "action": "Apply Artificer's Orbs for sockets + insert runes",
        },
        {
            "id": "9.2",
            "title": "Craft Complete!",
            "description": (
                "Your 6x T1 mirror-tier focus is complete.\n"
                "A perfect focus rivals a shield for casters —\n"
                "maximizing spell damage, cast speed, and ES.\n\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Admire your completed mirror-tier focus",
        },
    ]


# ---------------------------------------------------------------------------
# 1. Body Armour (STR)
# ---------------------------------------------------------------------------
_STR_BODY = {
    "quality_currency": "Armourer's Scrap",
    "quality_count": 20,
    "quality_step_title": "Apply Quality",
    "quality_step_desc": (
        "Use 20x Armourer's Scraps to reach 20% quality.\n"
        "This improves the base Armour, Evasion, or Energy Shield\n"
        "rating of the body armour depending on its base type.\n"
        "Cost: <1 Divine (trivial)"
    ),
    "exceptional_base_step": None,
    "s_tier_keep": [
        "% Increased Armour / Evasion / Energy Shield (T1-T2)",
        "+# to maximum Life (T1-T2)",
        "+# to maximum Energy Shield (T1-T2)",
        "Hybrid %Defence + Life (T1-T2, top priority)",
        "+#% to Fire Resistance (T1-T2)",
        "+#% to Cold Resistance (T1-T2)",
        "+#% to Lightning Resistance (T1-T2)",
        "+#% to Chaos Resistance (T1-T2)",
        "+# to Strength / Dexterity / Intelligence (T1-T2)",
        "Physical Damage taken as Element (T1-T2)",
        "% Increased Life Recovery Rate (T1-T2)",
        "% Additional Physical Damage Reduction (T1-T2)",
    ],
    "s_tier_trash": _BASE_TRASH,
    "s_tier_consider": [
        "% Increased Stun Threshold (if stun-vulnerable build)",
        "% Reduced Extra Damage from Critical Strikes",
        "+# to maximum Mana (if MoM build)",
        "+#% to Spell Suppression (if Dex base)",
    ],
    "regal_omen_note": (
        "Body armour prefixes: %Defence, +Life, +ES, Hybrid Defence/Life. "
        "Suffixes: Resistances, Attributes, Recovery, Spell Suppression. "
        "If targeting +Life or %Defence prefix, use Sinistral Coronation."
    ),
    "fracture_priority": [
        "% Increased Armour / Evasion / Energy Shield (prefix)",
        "+# to maximum Life (prefix)",
        "+#% to Chaos Resistance (suffix, rarest resist)",
    ],
    "phase9_title": "Finalize",
    "phase9_steps": [
        {
            "id": "9.1",
            "title": "Artificer's Orbs for Sockets",
            "description": (
                "Body armour can have up to 2-3 rune sockets\n"
                "depending on base type and implicits.\n\n"
                "Use Artificer's Orbs to add sockets.\n"
                "Each orb adds 1 socket (chance-based)."
            ),
            "orbs_used": ["Artificer's Orb"],
            "action": "Apply Artificer's Orbs for sockets",
        },
        {
            "id": "9.2",
            "title": "Insert Runes",
            "description": (
                "Armour rune recommendations:\n"
                "  Iron Rune (if phys mitigation needed)\n"
                "  Stone Rune (stun threshold/armour)\n"
                "  Desert/Storm/Glacier Rune (resists)\n"
                "  Soul Rune (if ES hybrid)\n\n"
                "Use Perfect Runes for maximum effect."
            ),
            "orbs_used": [],
            "action": "Insert appropriate armour runes",
        },
        {
            "id": "9.3",
            "title": "Craft Complete!",
            "description": (
                "Your 6x T1 mirror-tier body armour is complete.\n"
                "Total estimated cost: 500-1,000+ div (conservative).\n"
                "Body armour is one of the most impactful slots —\n"
                "this piece defines your build's survivability.\n\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Admire your completed mirror-tier body armour",
        },
    ],
    "completed_message": (
        "Your 6x T1 mirror-tier body armour is complete.\n"
        "Total estimated cost: 500-1,000+ div (conservative).\n"
        "Body armour is one of the most impactful slots —\n"
        "this piece defines your build's survivability.\n\n"
        "GG, Exile."
    ),
    "action": "Admire your completed mirror-tier body armour",
    "phase10_title": "Phase 10: Sanctify",
    "alternatives": _STANDARD_ALTERNATIVES,
    "orbs_used_overrides": _STANDARD_ORBS_OVERRIDES,
}

# ---------------------------------------------------------------------------
# 2. Helmet
# ---------------------------------------------------------------------------

_HELMET = {
    "quality_currency": "Armourer's Scrap",
    "quality_count": 20,
    "quality_step_title": "Apply Quality",
    "quality_step_desc": (
        "Use 20x Armourer's Scraps to reach 20% quality.\n"
        "This improves the base defence rating of the helmet.\n"
        "Cost: <1 Divine (trivial)\n\n"
        "Helmets have smaller defence values than body armour,\n"
        "but can roll powerful utility mods on suffixes."
    ),
    "exceptional_base_step": None,
    "s_tier_keep": [
        "% Increased [Defence Type] (T1-T2)",
        "+# to maximum Life (T1-T2)",
        "+# to maximum Energy Shield (T1-T2, if INT base)",
        "+#% to Fire Resistance (T1-T2)",
        "+#% to Cold Resistance (T1-T2)",
        "+#% to Lightning Resistance (T1-T2)",
        "+#% to Chaos Resistance (T1-T2)",
        "+# to [Relevant Attribute] (T1-T2)",
        "+#% to Critical Hit Chance (T1, if attack build)",
        "+# to Level of Socketed [Type] Gems (T1-T2, rare but powerful)",
        "% Increased Rarity of Items Found (T1-T2)",
        "% Increased Mana Regeneration Rate (T1-T2, if caster)",
    ],
    "s_tier_trash": _BASE_TRASH + [
        "Socketed gems are supported by [low-level support]",
    ],
    "s_tier_consider": [
        "% Increased Stun Threshold (if stun-vulnerable build)",
        "+# to maximum Mana (if MoM build)",
    ],
    "regal_omen_note": (
        "Helmets have a diluted prefix pool (defence, +Life, +gems, "
        "+ES). Suffixes include resists, attributes, and utility. "
        "+Gem mods are only available on prefixes — if that's your "
        "target, Sinistral Coronation is the play."
    ),
    "fracture_priority": [
        "+# to Level of Socketed Gems (prefix, rarest)",
        "% Increased [Defence] (prefix)",
        "+# to maximum Life (prefix)",
        "+#% to Chaos Resistance (suffix)",
    ],
    "phase9_title": "Finalize",
    "phase9_steps": [
        {
            "id": "9.1",
            "title": "Insert Runes",
            "description": (
                "Helmets can have rune sockets.\n"
                "Use Artificer's Orbs to add sockets.\n\n"
                "Helmet rune recommendations:\n"
                "  Iron Rune (phys mitigation)\n"
                "  Glacier Rune (cold res / chill)\n"
                "  Desert/Storm Rune (fire / lightning res)\n"
                "  Soul Rune (ES / spell)\n\n"
                "Use Perfect Runes for maximum effect."
            ),
            "orbs_used": ["Artificer's Orb"],
            "action": "Apply Artificer's Orbs for sockets + insert runes",
        },
        {
            "id": "9.2",
            "title": "Craft Complete!",
            "description": (
                "Your 6x T1 mirror-tier helmet is complete.\n"
                "Helmets can roll +gems and powerful utility mods —\n"
                "this piece enables key build thresholds.\n\n"
                "GG, Exile."
            ),
            "orbs_used": [],
            "action": "Admire your completed mirror-tier helmet",
        },
    ],
    "completed_message": (
        "Your 6x T1 mirror-tier helmet is complete.\n"
        "Helmets can roll +gems and powerful utility mods —\n"
        "this piece enables key build thresholds.\n\n"
        "GG, Exile."
    ),
    "action": "Admire your completed mirror-tier helmet",
    "phase10_title": "Phase 10: Sanctify",
    "alternatives": _STANDARD_ALTERNATIVES,
    "orbs_used_overrides": _STANDARD_ORBS_OVERRIDES,
}

# ---------------------------------------------------------------------------
# 9. Boots
# ---------------------------------------------------------------------------
_BOOTS = {
    "quality_currency": "Armourer's Scrap",
    "quality_count": 20,
    "quality_step_title": "Apply Quality",
    "quality_step_desc": (
        "Use 20x Armourer's Scraps to reach 20% quality.\n"
        "This improves the base defence rating of the boots.\n"
        "Cost: <1 Divine (trivial)\n\n"
        "Boots are the ONLY armour slot that rolls Movement Speed —\n"
        "this is the most critical suffix."
    ),
    "exceptional_base_step": None,
    "s_tier_keep": [
        "% Increased [Defence Type] (T1-T2)",
        "+# to maximum Life (T1-T2)",
        "+# to maximum Energy Shield (T1-T2)",
        "#% increased Movement Speed (T1-T2) - ESSENTIAL",
        "+#% to Fire Resistance (T1-T2)",
        "+#% to Cold Resistance (T1-T2)",
        "+#% to Lightning Resistance (T1-T2)",
        "+#% to Chaos Resistance (T1-T2)",
        "+# to [Relevant Attribute] (T1-T2)",
        "% Increased Rarity of Items Found (T1-T2)",
        "#% chance to gain Onslaught on Kill (T1)",
    ],
    "s_tier_trash": _BASE_TRASH + [
        "Any boots without at least T3 movespeed are TRASH regardless of other mods",
    ],
    "s_tier_consider": [
        "% Increased Stun Threshold (if stun-vulnerable build)",
        "+# to maximum Mana (if MoM build)",
    ],
    "regal_omen_note": (
        "Movement Speed is a suffix. If your magic stage landed a "
        "good prefix + bad suffix, use Sinistral Coronation to force "
        "prefixes and keep your movespeed slot open."
    ),
    "fracture_priority": [
        "#% increased Movement Speed (suffix, most critical)",
        "% Increased Defence (prefix)",
        "+# to maximum Life (prefix)",
    ],
    "phase9_title": "Finalize",
    "phase9_steps": _boots_phase9(),
    "completed_message": (
        "Your 6x T1 mirror-tier boots are complete.\n"
        "Total estimated cost: 400-800+ div (conservative).\n"
        "Movement Speed on boots is the most important suffix\n"
        "in the game — this piece literally drives your build.\n\n"
        "GG, Exile."
    ),
    "action": "Admire your completed mirror-tier boots",
    "phase10_title": "Phase 10: Sanctify",
    "alternatives": _STANDARD_ALTERNATIVES,
    "orbs_used_overrides": _STANDARD_ORBS_OVERRIDES,
}

# ---------------------------------------------------------------------------
# 10. Gloves
# ---------------------------------------------------------------------------
_GLOVES = {
    "quality_currency": "Armourer's Scrap",
    "quality_count": 20,
    "quality_step_title": "Apply Quality",
    "quality_step_desc": (
        "Use 20x Armourer's Scraps to reach 20% quality.\n"
        "This improves the base defence rating of the gloves.\n"
        "Cost: <1 Divine (trivial)\n\n"
        "Gloves can roll attack-specific mods (added flat damage,\n"
        "attack speed, melee range) that other armour slots cannot."
    ),
    "exceptional_base_step": None,
    "s_tier_keep": [
        "% Increased [Defence Type] (T1-T2)",
        "+# to maximum Life (T1-T2)",
        "Adds # to # Physical Damage to Attacks (T1-T2)",
        "Adds # to # [Element] Damage to Attacks (T1-T2)",
        "% Increased Attack Speed (T1)",
        "+#% to Fire Resistance (T1-T2)",
        "+#% to Cold Resistance (T1-T2)",
        "+#% to Lightning Resistance (T1-T2)",
        "+#% to Chaos Resistance (T1-T2)",
        "+# to [Relevant Attribute] (T1-T2)",
        "+# to Melee Strike Range (T1, if melee)",
    ],
    "s_tier_trash": _BASE_TRASH + [
        "Adds # to # Non-Physical Damage below T3",
        "Socketed gems are supported by [low-level support]",
    ],
    "s_tier_consider": [
        "% Increased Stun Threshold (if stun-vulnerable build)",
        "+# to maximum Mana (if MoM build)",
        "% Increased Rarity of Items Found (T1-T2)",
    ],
    "regal_omen_note": (
        "Gloves have valuable attack prefixes (flat damage) and "
        "suffixes (attack speed). Assess your magic stage split "
        "before choosing omen direction."
    ),
    "fracture_priority": [
        "Adds # to # Physical Damage to Attacks (prefix)",
        "+# to maximum Life (prefix)",
        "% Increased Attack Speed (suffix)",
    ],
    "phase9_title": "Finalize",
    "phase9_steps": _gloves_phase9(),
    "completed_message": (
        "Your 6x T1 mirror-tier gloves are complete.\n"
        "Total estimated cost: 400-800+ div (conservative).\n"
        "Gloves are the only armour slot that rolls attack mods —\n"
        "flat damage and attack speed make this piece a damage engine.\n\n"
        "GG, Exile."
    ),
    "action": "Admire your completed mirror-tier gloves",
    "phase10_title": "Phase 10: Sanctify",
    "alternatives": _STANDARD_ALTERNATIVES,
    "orbs_used_overrides": _STANDARD_ORBS_OVERRIDES,
}

# ---------------------------------------------------------------------------
# 11. Shield
# ---------------------------------------------------------------------------
_SHIELD = {
    "quality_currency": "Armourer's Scrap",
    "quality_count": 20,
    "quality_step_title": "Apply Quality",
    "quality_step_desc": (
        "Use 20x Armourer's Scraps to reach 20% quality.\n"
        "This improves the base defence rating of the shield.\n"
        "Cost: <1 Divine (trivial)\n\n"
        "Shields provide Block Chance as an implicit and can roll\n"
        "powerful block-related mods on both prefixes and suffixes."
    ),
    "exceptional_base_step": None,
    "s_tier_keep": [
        "% Increased [Defence Type] (T1-T2)",
        "+# to maximum Life (T1-T2)",
        "+# to maximum Energy Shield (T1-T2, if INT shield)",
        "+#% to Block Chance (T1-T2)",
        "% Increased Spell Block Chance (T1-T2, if available)",
        "+#% to Fire Resistance (T1-T2)",
        "+#% to Cold Resistance (T1-T2)",
        "+#% to Lightning Resistance (T1-T2)",
        "+#% to Chaos Resistance (T1-T2)",
        "+# to [Relevant Attribute] (T1-T2)",
        "#% of Block Chance applied to Spells (T1-T2)",
        "% Increased Block Recovery (T1, if relevant)",
    ],
    "s_tier_trash": _BASE_TRASH,
    "s_tier_consider": [
        "% Increased Stun Threshold (if stun-vulnerable build)",
        "+# to maximum Mana (if MoM build)",
    ],
    "regal_omen_note": (
        "Shields have block mods on both sides. Determine if your "
        "priority is defence (prefix -> Sinistral Coronation) or "
        "block (depends on which side your base has)."
    ),
    "fracture_priority": [
        "+#% to Block Chance (prefix or suffix)",
        "% Increased Defence (prefix)",
        "+# to maximum Life (prefix)",
    ],
    "phase9_title": "Finalize",
    "phase9_steps": _shield_phase9(),
    "completed_message": (
        "Your 6x T1 mirror-tier shield is complete.\n"
        "A perfect shield defines a build's maximum tank —\n"
        "this piece dramatically increases your effective HP.\n\n"
        "GG, Exile."
    ),
    "action": "Admire your completed mirror-tier shield",
    "phase10_title": "Phase 10: Sanctify",
    "alternatives": _STANDARD_ALTERNATIVES,
    "orbs_used_overrides": _STANDARD_ORBS_OVERRIDES,
}

# ---------------------------------------------------------------------------
# 12. Focus
# ---------------------------------------------------------------------------
_FOCUS = {
    "quality_currency": "Armourer's Scrap",
    "quality_count": 20,
    "quality_step_title": "Apply Quality",
    "quality_step_desc": (
        "Use 20x Armourer's Scraps to reach 20% quality.\n"
        "This improves the base Energy Shield of the focus.\n"
        "Cost: <1 Divine (trivial)"
    ),
    "exceptional_base_step": None,
    "s_tier_keep": [
        "% Increased Energy Shield (T1-T2)",
        "+# to maximum Energy Shield (T1-T2)",
        "% Increased Spell Damage (T1-T2)",
        "% Increased Cast Speed (T1)",
        "+# to Level of all Spell Skill Gems (T1-T2)",
        "+#% to Critical Hit Chance for Spells (T1)",
        "+#% to Critical Spell Damage Bonus (T1)",
        "+#% to Fire Resistance (T1-T2)",
        "+#% to Cold Resistance (T1-T2)",
        "+#% to Lightning Resistance (T1-T2)",
        "+#% to Chaos Resistance (T1-T2)",
        "+# to Intelligence (T1-T2)",
    ],
    "s_tier_trash": _BASE_TRASH,
    "s_tier_consider": [
        "% Increased Mana Regeneration Rate (T1-T2)",
        "+# to maximum Mana (T1-T2)",
    ],
    "regal_omen_note": (
        "Foci have spell caster prefixes (Spell Damage, +Gems, "
        "+ES) and caster suffixes (Cast Speed, Crit, Int). "
        "Prefixes are heavily contested — Sinistral Coronation "
        "recommended for locking spell damage / +gems first."
    ),
    "fracture_priority": [
        "+# to Level of all Spell Skill Gems (prefix)",
        "% Increased Spell Damage (prefix)",
        "% Increased Cast Speed (suffix)",
    ],
    "phase9_title": "Finalize",
    "phase9_steps": _focus_phase9(),
    "completed_message": (
        "Your 6x T1 mirror-tier focus is complete.\n"
        "A perfect focus rivals a shield for casters —\n"
        "maximizing spell damage, cast speed, and ES.\n\n"
        "GG, Exile."
    ),
    "action": "Admire your completed mirror-tier focus",
    "phase10_title": "Phase 10: Sanctify",
    "alternatives": _STANDARD_ALTERNATIVES,
    "orbs_used_overrides": _STANDARD_ORBS_OVERRIDES,
}

# ---------------------------------------------------------------------------
# Exported dictionary
# ---------------------------------------------------------------------------

ARMOUR_SUBTYPE_DATA = {
    "Body Armour": _STR_BODY,
    "Helmet": _HELMET,
    "Boots": _BOOTS,
    "Gloves": _GLOVES,
    "Shield": _SHIELD,
    "Focus": _FOCUS,
}
