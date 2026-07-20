_JEWELLERY_ALTERNATIVES = {
    "3.1": [
        {
            "label": "Use Coronation Omen (Recommended)",
            "cost": "~2 div",
            "risk": "low",
            "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Critical for protecting your magic-stage mods.",
        },
        {
            "label": "Skip Omen (YOLO)",
            "cost": "~0.1 div (orb only)",
            "risk": "medium",
            "description": "Random side. 50/50 chance. Wrong side = Annul (~14 div with omen) to fix.",
        },
    ],
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
    "7.1": [
        {
            "label": "Full Whittling (Recommended)",
            "cost": "~20 div/attempt",
            "risk": "low",
            "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Targets lowest ilvl mod only.",
        },
        {
            "label": "Budget Whittling",
            "cost": "~5 div/attempt",
            "risk": "high",
            "description": "Perfect Chaos without omens. RANDOM removal — can destroy your T1s.",
        },
    ],
    "10.2": [
        {
            "label": "Use Hinekora's Lock (Safe)",
            "cost": "~150 div per Lock",
            "risk": "very low",
            "description": "Preview sanctify outcome. If bad, modify item to change seed. Lock consumed regardless.",
        },
        {
            "label": "Use Omen of Sanctification (Guaranteed)",
            "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
            "risk": "very low",
            "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
        },
        {
            "label": "Lock + Sanctification Omen (Ultimate Safety)",
            "cost": "~151.4 div (Lock ~150 + Divine ~1 + Omen ~0.4)",
            "risk": "very low",
            "description": "Combine Hinekora's Lock (preview outcome) with Omen of Sanctification (guaranteed success). Preview the sanctify and if the result is good, the Omen guarantees it lands.",
        },
    ],
}

_JEWELLERY_ORBS_OVERRIDES = {
    "1.3": ["Flesh Catalyst"],
    "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
    "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
}

_CATALYST_QUALITY_DESC = (
    "Use Catalysts to add quality to the ring.\n"
    "Catalysts enhance specific modifier types:\n\n"
    "  Flesh Catalyst \u2014 Life modifiers\n"
    "  Neural Catalyst \u2014 Mana modifiers\n"
    "  Carapace Catalyst \u2014 Defence modifiers\n"
    "  Uul-Netol's \u2014 Physical modifiers\n"
    "  Xoph's \u2014 Fire modifiers\n"
    "  Tul's \u2014 Cold modifiers\n"
    "  Esh's \u2014 Lightning modifiers\n"
    "  Chayula's \u2014 Chaos modifiers\n"
    "  Reaver Catalyst \u2014 Attack modifiers\n"
    "  Sibilant Catalyst \u2014 Caster modifiers\n"
    "  Skittering Catalyst \u2014 Speed modifiers\n"
    "  Adaptive Catalyst \u2014 Attribute modifiers\n"
    "  Necrotic Catalyst \u2014 Minion modifiers\n\n"
    "Apply 20x of the catalyst matching your PRIMARY desired mod.\n"
    "Quality on jewellery enhances the numeric values\n"
    "of matching modifiers (20% quality = 20% increased effect).\n\n"
    "CHOOSE WISELY: Catalyst type is permanent once applied."
)

_FINAL_CATALYST_STEP = {
    "id": "9.1",
    "title": "Final Catalyst Quality",
    "description": (
        "Confirm your catalyst quality is maxed (20%).\n"
        "The catalyst type was chosen in Phase 1.\n\n"
        "Double-check that the catalyst type enhances\n"
        "your PRIMARY desired modifier.\n\n"
        "e.g. Flesh Catalyst enhances +Life;\n"
        "Reaver Catalyst enhances attack mods;\n"
        "Sibilant Catalyst enhances caster mods.\n\n"
        "Catalysts are consumed on use; each\n"
        "adds 1% quality up to a 20% cap."
    ),
    "orbs_used": ["Catalyst"],
    "action": "Apply catalysts to reach 20% if not done",
}

_RING_S_TIER_KEEP = [
    "+# to maximum Life (T1-T2)",
    "+# to maximum Energy Shield (T1-T2)",
    "Adds # to # Physical Damage to Attacks (T1-T2)",
    "Adds # to # Fire/Cold/Lightning Damage to Attacks (T1-T2)",
    "% Increased Elemental Damage with Attacks (T1-T2)",
    "% Increased Cast Speed (T1)",
    "% Increased Attack Speed (T1)",
    "+#% to Fire Resistance (T1-T2)",
    "+#% to Cold Resistance (T1-T2)",
    "+#% to Lightning Resistance (T1-T2)",
    "+#% to Chaos Resistance (T1-T2)",
    "+# to all Attributes (T1-T2)",
    "+# to Strength/Dexterity/Intelligence (T1-T2)",
    "% Increased Critical Hit Chance (T1)",
    "+% to Critical Damage Bonus (T1)",
    "#% of Physical Damage Leeched as Life/Mana (T1-T2)",
    "% Increased Rarity of Items Found (T1-T2)",
    "% Increased Mana Regeneration Rate (T1-T2)",
]

_RING_S_TIER_TRASH = [
    "Any mod below T3 tier",
    "Light Radius",
    "Reduced Flask Charges Gained",
    "+# to Accuracy Rating",
    "+# Life gained on Kill",
    "+# Mana gained on Kill",
    "Reduced Attribute Requirements",
    "% Increased Light Radius",
    "Stun and Block Recovery",
    "Thorns damage",
]

_RING_S_TIER_CONSIDER = [
    "% Increased Flask Life Recovery Rate",
    "% Increased Flask Mana Recovery Rate",
    "% Reduced Effect of Curses on You",
    "% Chance to Avoid Elemental Ailments",
]

_AMULET_S_TIER_KEEP = _RING_S_TIER_KEEP + [
    "+# to Level of all Skill Gems (T1-T2) \u2014 CRITICAL, rarest amulet mod",
    "+# to Level of all [Type] Skill Gems (T1-T2)",
    "% Increased Global Defences (T1-T2)",
    "+#% to all Maximum Resistances (T1-T2, very rare)",
]

_BELT_S_TIER_KEEP = [
    "+# to maximum Life (T1-T2)",
    "+# to maximum Energy Shield (T1-T2)",
    "% Increased Global Defences (T1-T2)",
    "+#% to Fire Resistance (T1-T2)",
    "+#% to Cold Resistance (T1-T2)",
    "+#% to Lightning Resistance (T1-T2)",
    "+#% to Chaos Resistance (T1-T2)",
    "+# to Strength/Dexterity/Intelligence (T1-T2)",
    "% Increased Flask Life Recovery Rate (T1-T2)",
    "% Increased Flask Mana Recovery Rate (T1-T2)",
    "#% increased Flask Charges Gained (T1-T2)",
    "#% reduced Flask Charges Used (T1-T2)",
    "+# Charm Slots (implicit, check base type)",
    "% Increased Effect of Charms (T1-T2)",
    "% Increased Cooldown Recovery Rate (T1-T2)",
]

JEWELLERY_SUBTYPE_DATA = {
    "Ring": {
        "quality_currency": "Flesh Catalyst",
        "quality_count": 20,
        "quality_step_title": "Apply Catalyst Quality",
        "quality_step_desc": _CATALYST_QUALITY_DESC,
        "exceptional_base_step": None,
        "s_tier_keep": _RING_S_TIER_KEEP,
        "s_tier_trash": _RING_S_TIER_TRASH,
        "s_tier_consider": _RING_S_TIER_CONSIDER,
        "regal_omen_note": (
            "Rings have a very large mod pool. Check which side (prefix vs suffix) "
            "your desired mods are on BEFORE Regaling. Common ring prefixes: "
            "Life, ES, flat damage, %damage. Common suffixes: Resists, attributes, "
            "cast/attack speed, crit."
        ),
        "fracture_priority": [
            "+# to maximum Life (prefix, most universal)",
            "Adds # to # [Type] Damage to Attacks (prefix)",
            "% Increased [Type] Damage (prefix)",
            "+#% to Chaos Resistance (suffix, rarest resist)",
        ],
        "phase9_title": "Finalize & Catalyst",
        "phase9_steps": [
            dict(_FINAL_CATALYST_STEP),
            {
                "id": "9.2",
                "title": "No Sockets or Runes",
                "description": (
                    "Rings do NOT have sockets or runes.\n"
                    "Rings are complete when their 6 mods\n"
                    "are T1 with max quality.\n\n"
                    "If this is a Desecrated ring, verify\n"
                    "that Desecrated mods are revealed and\n"
                    "that you're satisfied with them."
                ),
                "orbs_used": [],
                "action": "Confirm no further modifications needed",
            },
            {
                "id": "9.3",
                "title": "Craft Complete!",
                "description": (
                    "Your 6x T1 mirror-tier ring is complete.\n"
                    "Total estimated cost: 400-900+ div (conservative).\n\n"
                    "Rings are one of the most competitive slots \u2014\n"
                    "a perfect ring defines a build's damage\n"
                    "and survivability simultaneously.\n\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier ring",
            },
        ],
        "completed_message": (
            "Your 6x T1 mirror-tier ring is complete.\n"
            "Total estimated cost: 400-900+ div (conservative).\n\n"
            "Rings are one of the most competitive slots \u2014\n"
            "a perfect ring defines a build's damage\n"
            "and survivability simultaneously.\n\n"
            "GG, Exile."
        ),
        "action": "Admire your completed mirror-tier ring",
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": _JEWELLERY_ALTERNATIVES,
        "orbs_used_overrides": _JEWELLERY_ORBS_OVERRIDES,
    },
    "Amulet": {
        "quality_currency": "Flesh Catalyst",
        "quality_count": 20,
        "quality_step_title": "Apply Catalyst Quality",
        "quality_step_desc": _CATALYST_QUALITY_DESC.replace(
            "quality to the ring", "quality to the amulet"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": _AMULET_S_TIER_KEEP,
        "s_tier_trash": _RING_S_TIER_TRASH,
        "s_tier_consider": _RING_S_TIER_CONSIDER,
        "regal_omen_note": (
            "Amulets have the +Gem Level prefix \u2014 the single most valuable mod. "
            "If your magic stage has 2 prefixes and neither is +Gems, consider trashing. "
            "If one is +Gems, use Dextral Coronation to force suffixes and protect "
            "the gem level."
        ),
        "fracture_priority": [
            "+# to Level of all Skill Gems (prefix, rarest + most valuable)",
            "+# to maximum Life (prefix)",
            "+#% to Chaos Resistance (suffix)",
            "% Increased Global Defences (prefix)",
        ],
        "phase9_title": "Finalize & Anoint",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Anoint with Distilled Emotions",
                "description": (
                    "Amulets can be Anointed at the Blight Altar.\n"
                    "Anointing consumes Distilled Emotions to\n"
                    "add a Notable Passive Skill to the amulet.\n\n"
                    "Choose a Notable that synergizes with your build.\n"
                    "Popular choices:\n"
                    "  Charisma (reduced mana reservation)\n"
                    "  Whispers of Doom (+1 curse)\n"
                    "  Sovereignty (increased aura effect)\n"
                    "  Heart of Ice/Fire/Thunder (elemental pen)\n"
                    "  Cleansed Thoughts (chaos res doubled)\n\n"
                    "Check the passive tree for all Notable options.\n"
                    "Anoints are PERMANENT \u2014 choose carefully."
                ),
                "orbs_used": ["Distilled Emotion"],
                "action": "Anoint amulet with Distilled Emotions at Blight Altar",
            },
            {
                "id": "9.2",
                "title": "Final Catalyst Quality",
                "description": _FINAL_CATALYST_STEP["description"],
                "orbs_used": ["Catalyst"],
                "action": "Apply catalysts to reach 20% if not done",
            },
            {
                "id": "9.3",
                "title": "No Sockets",
                "description": "Amulets do NOT have sockets or runes.",
                "orbs_used": [],
                "action": "Confirm no further modifications needed",
            },
            {
                "id": "9.4",
                "title": "Craft Complete!",
                "description": (
                    "Your 6x T1 mirror-tier amulet is complete.\n"
                    "Total estimated cost: 500-1,200+ div (conservative).\n\n"
                    "Amulets with +Level of Gems are among the\n"
                    "most valuable items in the game \u2014 a perfect\n"
                    "amulet is build-defining.\n\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier amulet",
            },
        ],
        "completed_message": (
            "Your 6x T1 mirror-tier amulet is complete.\n"
            "Total estimated cost: 500-1,200+ div (conservative).\n\n"
            "Amulets with +Level of Gems are among the\n"
            "most valuable items in the game.\n\n"
            "GG, Exile."
        ),
        "action": "Admire your completed mirror-tier amulet",
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": _JEWELLERY_ALTERNATIVES,
        "orbs_used_overrides": _JEWELLERY_ORBS_OVERRIDES,
    },
    "Belt": {
        "quality_currency": "Flesh Catalyst",
        "quality_count": 20,
        "quality_step_title": "Apply Catalyst Quality",
        "quality_step_desc": _CATALYST_QUALITY_DESC.replace(
            "quality to the ring", "quality to the belt"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": _BELT_S_TIER_KEEP,
        "s_tier_trash": _RING_S_TIER_TRASH,
        "s_tier_consider": _RING_S_TIER_CONSIDER,
        "regal_omen_note": (
            "Belt suffixes are dense (resists, attributes, flask mods). "
            "Dextral Coronation to force suffixes is usually optimal."
        ),
        "fracture_priority": [
            "+# to maximum Life (prefix)",
            "+#% to Chaos Resistance (suffix)",
            "% Increased Flask Effect/Recovery (prefix or suffix)",
        ],
        "phase9_title": "Finalize & Catalyst",
        "phase9_steps": [
            dict(_FINAL_CATALYST_STEP),
            {
                "id": "9.2",
                "title": "Confirm Charm Slots",
                "description": (
                    "Belts can have 1-3 Charm Slots as an implicit\n"
                    "based on the base type.\n\n"
                    "Charms provide powerful conditional buffs.\n"
                    "Slot charms that complement your build:\n"
                    "  - Topaz Charm (shock immunity)\n"
                    "  - Ruby Charm (ignite immunity)\n"
                    "  - Sapphire Charm (freeze/chill immunity)\n"
                    "  - Amethyst Charm (chaos res)\n"
                    "  - Quartz Charm (phasing)\n\n"
                    "Charms are NOT part of the crafting process \u2014\n"
                    "they are slotted separately."
                ),
                "orbs_used": [],
                "action": "Equip appropriate charms",
            },
            {
                "id": "9.3",
                "title": "Craft Complete!",
                "description": (
                    "Your 6x T1 mirror-tier belt is complete.\n"
                    "Total estimated cost: 400-800+ div (conservative).\n\n"
                    "A perfect belt with max life, resists, and\n"
                    "flask mods is a core defensive layer.\n\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier belt",
            },
        ],
        "completed_message": (
            "Your 6x T1 mirror-tier belt is complete.\n"
            "Total estimated cost: 400-800+ div (conservative).\n\n"
            "GG, Exile."
        ),
        "action": "Admire your completed mirror-tier belt",
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": _JEWELLERY_ALTERNATIVES,
        "orbs_used_overrides": _JEWELLERY_ORBS_OVERRIDES,
    },
}
