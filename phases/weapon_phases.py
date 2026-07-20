WEAPON_SUBTYPE_DATA = {
    "Bow": {
        "item_type": "weapon",
        "sub_type": "Bow",
        "quality_currency": "Blacksmith's Whetstone",
        "quality_count": 20,
        "quality_step_title": "Apply Quality",
        "quality_step_desc": (
            "Use 20x Blacksmith's Whetstones to reach 20% quality.\n"
            "This improves the base physical damage of the bow.\n"
            "Quality must be capped at 20% before using\n"
            "the Infuser in the next step.\n"
            "Cost: <1 Divine (trivial)"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": [
            "+X to Level of all Projectile Skills (T3+)",
            "% Increased Physical Damage (T1-T2)",
            "Adds # to # Physical Damage (high roll)",
            "% Increased Elemental Damage with Attacks (T1-T2)",
            "% Increased Attack Speed (T1)",
            "% Increased Critical Hit Chance (T1)",
            "+% to Critical Damage Bonus (T1)",
            "Adds # to # Fire/Cold/Lightning Damage (correct element, high roll)",
        ],
        "s_tier_trash": [
            "Any mod below T3 tier",
            "Added flat damage of wrong element",
            "Light Radius",
            "Accuracy Rating",
            "Stun-related mods (unless stun build)",
            "Life/Mana on kill",
            "Leech (unless build uses it)",
            "Attribute requirements mods",
        ],
        "s_tier_consider": [],
        "regal_omen_note": (
            "Bows can roll both attack and projectile mods — prefix pool is larger, "
            "so Dextral Coronation to force suffix is often safer."
        ),
        "fracture_priority": [
            "+X to Level of all Projectile Skills",
            "% Increased Physical Damage",
            "Adds # to # Physical Damage (high rolls)",
            "% Increased Attack Speed",
        ],
        "phase9_title": "Finalize",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Insert Runes",
                "description": (
                    "Use an Artificer's Orb to add sockets, then insert your runes.\n"
                    "Rune choices:\n"
                    "- Iron Rune: Physical damage (bleed/phys bow builds)\n"
                    "- Storm Rune: Lightning damage (lightning arrow builds)\n"
                    "- Desert Rune: Fire damage (ignite/explosive builds)\n"
                    "- Glacier Rune: Cold damage (ice shot/freezing builds)\n"
                    "- Soul Rune: Mana — rarely used on bows\n"
                    "\n"
                    "If you have Perfect Runes (flawless versions), use them instead\n"
                    "for higher values."
                ),
                "orbs_used": ["Artificer's Orb"],
                "action": "Artificer's Orb for sockets + insert runes",
            },
            {
                "id": "9.2",
                "title": "Craft Complete!",
                "description": (
                    "Your mirror-tier bow is complete.\n"
                    "A 6x T1 bow like this is worth 700-1200+ divines.\n"
                    "You are now one of the deadliest rangers in Wraeclast.\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier bow",
            },
        ],
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": {
            "3.1": [
                {
                    "label": "Use Coronation Omen (Recommended)",
                    "cost": "~2 div",
                    "risk": "low",
                    "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Saves you from later Annulment costs.",
                },
                {
                    "label": "Skip Omen (YOLO)",
                    "cost": "~0.1 div (orb only)",
                    "risk": "medium",
                    "description": "Random side. 50/50 chance it lands where you want. If wrong, you'll need an Annul (~14 div with omen) to fix it.",
                },
                {
                    "label": "Use Omen of Greater Exaltation Instead",
                    "cost": "~1 div (Greater Exalt Omen)",
                    "risk": "medium",
                    "description": "Adds 2 mods instead of 1 but you lose directional control. Faster if you're filling both sides.",
                },
            ],
            "7.1": [
                {
                    "label": "Full Whittling (Recommended)",
                    "cost": "~20 div/attempt",
                    "risk": "low",
                    "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Removes only the LOWEST ilvl mod — your T1s are safe.",
                },
                {
                    "label": "Budget Whittling",
                    "cost": "~5 div/attempt",
                    "risk": "high",
                    "description": "Perfect Chaos without omens. Removes a RANDOM mod — can destroy your T1s. Only recommended if Whittling omens are unavailable.",
                },
            ],
            "10.2": [
                {
                    "label": "Use Hinekora's Lock (Safe)",
                    "cost": "~150 div per Lock",
                    "risk": "very low",
                    "description": "Preview the sanctify outcome before committing. If bad, modify the item to change the seed. Lock is consumed regardless.",
                },
                {
                    "label": "YOLO Sanctify",
                    "cost": "~1 div per Divine Orb",
                    "risk": "medium",
                    "description": "13% success rate per attempt. No preview — you see the result immediately. ~7-8 attempts expected.",
                },
                {
                    "label": "Use Omen of Sanctification (Guaranteed)",
                    "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                    "risk": "very low",
                    "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
                },
            ],
        },
        "orbs_used_overrides": {
            "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
            "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
        },
        "completed_message": (
            "Your 6x T1 mirror-tier bow is complete.\n"
            "A bow of this caliber is worth 700-1200+ divines.\n"
            "GG, Exile."
        ),
        "action": "Craft a mirror-tier bow",
    },
    "Crossbow": {
        "item_type": "weapon",
        "sub_type": "Crossbow",
        "quality_currency": "Blacksmith's Whetstone",
        "quality_count": 20,
        "quality_step_title": "Apply Quality",
        "quality_step_desc": (
            "Use 20x Blacksmith's Whetstones to reach 20% quality.\n"
            "This improves the base physical damage of the crossbow.\n"
            "Quality must be capped at 20% before using\n"
            "the Infuser in the next step.\n"
            "Cost: <1 Divine (trivial)"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": [
            "+X to Level of all Projectile Skills (T3+)",
            "% Increased Physical Damage (T1-T2)",
            "Adds # to # Physical Damage (high roll)",
            "% Increased Elemental Damage with Attacks (T1-T2)",
            "% Increased Attack Speed (T1)",
            "% Increased Critical Hit Chance (T1)",
            "+% to Critical Damage Bonus (T1)",
            "Adds # to # Fire/Cold/Lightning Damage (correct element, high roll)",
        ],
        "s_tier_trash": [
            "Any mod below T3 tier",
            "Added flat damage of wrong element",
            "Light Radius",
            "Accuracy Rating",
            "Stun-related mods (unless stun build)",
            "Life/Mana on kill",
            "Leech (unless build uses it)",
            "Attribute requirements mods",
        ],
        "s_tier_consider": [],
        "regal_omen_note": (
            "Crossbows can roll both attack and projectile mods — prefix pool is larger, "
            "so Dextral Coronation to force suffix is often safer."
        ),
        "fracture_priority": [
            "+X to Level of all Projectile Skills",
            "% Increased Physical Damage",
            "Adds # to # Physical Damage (high rolls)",
            "% Increased Attack Speed",
        ],
        "phase9_title": "Finalize",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Insert Runes",
                "description": (
                    "Use an Artificer's Orb to add sockets, then insert your runes.\n"
                    "Rune choices:\n"
                    "- Iron Rune: Physical damage (grenade/bolt builds)\n"
                    "- Storm Rune: Lightning damage (shockburst builds)\n"
                    "- Desert Rune: Fire damage (incendiary/grenade builds)\n"
                    "- Glacier Rune: Cold damage (freeze builds)\n"
                    "- Soul Rune: Mana — rarely used on crossbows\n"
                    "\n"
                    "If you have Perfect Runes (flawless versions), use them instead\n"
                    "for higher values."
                ),
                "orbs_used": ["Artificer's Orb"],
                "action": "Artificer's Orb for sockets + insert runes",
            },
            {
                "id": "9.2",
                "title": "Craft Complete!",
                "description": (
                    "Your mirror-tier crossbow is complete.\n"
                    "Crossbows emphasize physical damage with projectile skill levels —\n"
                    "a 6x T1 crossbow like this is worth 700-1200+ divines.\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier crossbow",
            },
        ],
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": {
            "3.1": [
                {
                    "label": "Use Coronation Omen (Recommended)",
                    "cost": "~2 div",
                    "risk": "low",
                    "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Saves you from later Annulment costs.",
                },
                {
                    "label": "Skip Omen (YOLO)",
                    "cost": "~0.1 div (orb only)",
                    "risk": "medium",
                    "description": "Random side. 50/50 chance it lands where you want. If wrong, you'll need an Annul (~14 div with omen) to fix it.",
                },
                {
                    "label": "Use Omen of Greater Exaltation Instead",
                    "cost": "~1 div (Greater Exalt Omen)",
                    "risk": "medium",
                    "description": "Adds 2 mods instead of 1 but you lose directional control. Faster if you're filling both sides.",
                },
            ],
            "7.1": [
                {
                    "label": "Full Whittling (Recommended)",
                    "cost": "~20 div/attempt",
                    "risk": "low",
                    "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Removes only the LOWEST ilvl mod — your T1s are safe.",
                },
                {
                    "label": "Budget Whittling",
                    "cost": "~5 div/attempt",
                    "risk": "high",
                    "description": "Perfect Chaos without omens. Removes a RANDOM mod — can destroy your T1s. Only recommended if Whittling omens are unavailable.",
                },
            ],
            "10.2": [
                {
                    "label": "Use Hinekora's Lock (Safe)",
                    "cost": "~150 div per Lock",
                    "risk": "very low",
                    "description": "Preview the sanctify outcome before committing. If bad, modify the item to change the seed. Lock is consumed regardless.",
                },
                {
                    "label": "YOLO Sanctify",
                    "cost": "~1 div per Divine Orb",
                    "risk": "medium",
                    "description": "13% success rate per attempt. No preview — you see the result immediately. ~7-8 attempts expected.",
                },
                {
                    "label": "Use Omen of Sanctification (Guaranteed)",
                    "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                    "risk": "very low",
                    "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
                },
            ],
        },
        "orbs_used_overrides": {
            "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
            "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
        },
        "completed_message": (
            "Your 6x T1 mirror-tier crossbow is complete.\n"
            "Crossbows emphasize high physical damage with projectile skills —\n"
            "a crossbow of this caliber is worth 700-1200+ divines.\n"
            "GG, Exile."
        ),
        "action": "Craft a mirror-tier crossbow",
    },
    "Wand": {
        "item_type": "weapon",
        "sub_type": "Wand",
        "quality_currency": "Blacksmith's Whetstone",
        "quality_count": 20,
        "quality_step_title": "Apply Quality",
        "quality_step_desc": (
            "Use 20x Blacksmith's Whetstones to reach 20% quality.\n"
            "This improves the base physical damage of the wand.\n"
            "Quality must be capped at 20% before using\n"
            "the Infuser in the next step.\n"
            "Cost: <1 Divine (trivial)"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": [
            "+X to Level of all Spell Skills (T3+) — check element type (Fire/Cold/Lightning/Chaos/Physical/Minion)",
            "% Increased Spell Damage (T1-T2)",
            "% Increased Cast Speed (T1)",
            "+X to Level of all [Element] Spell Skills",
            "% Increased Critical Hit Chance for Spells (T1)",
            "+% to Critical Spell Damage Bonus (T1)",
            "Adds # to # [Element] Damage to Spells (high roll)",
        ],
        "s_tier_trash": [
            "Any mod below T3 tier",
            "Added flat spell damage of wrong element",
            "Light Radius",
            "Accuracy Rating",
            "Stun-related mods (unless stun build)",
            "Life/Mana on kill",
            "Leech (unless build uses it)",
            "Attribute requirements mods",
            "Melee/physical attack mods",
            "Projectile attack mods",
            "Added flat attack damage",
        ],
        "s_tier_consider": [],
        "regal_omen_note": (
            "Wands have a large prefix pool (spell damage, gem levels, flat damage to spells). "
            "Dextral Coronation to force suffix (cast speed, crit) is often safer to avoid prefix bloat."
        ),
        "fracture_priority": [
            "+X to Level of all Spell Skills",
            "% Increased Spell Damage",
            "% Increased Cast Speed",
        ],
        "phase9_title": "Finalize",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Insert Runes",
                "description": (
                    "Use an Artificer's Orb to add sockets, then insert your runes.\n"
                    "Rune choices:\n"
                    "- Soul Rune: Spell damage/mana — best for most caster wands\n"
                    "- Storm Rune: Lightning spell builds\n"
                    "- Desert Rune: Fire spell builds\n"
                    "- Glacier Rune: Cold spell builds\n"
                    "- Iron Rune: Physical spell builds (e.g. Blade Fall)\n"
                    "\n"
                    "If you have Perfect Runes (flawless versions), use them instead\n"
                    "for higher values."
                ),
                "orbs_used": ["Artificer's Orb"],
                "action": "Artificer's Orb for sockets + insert runes",
            },
            {
                "id": "9.2",
                "title": "Craft Complete!",
                "description": (
                    "Your mirror-tier wand is complete.\n"
                    "A 6x T1 caster wand with perfect spell mods is worth\n"
                    "600-1100+ divines depending on element and demand.\n"
                    "Your spells will now delete everything on screen.\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier wand",
            },
        ],
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": {
            "3.1": [
                {
                    "label": "Use Coronation Omen (Recommended)",
                    "cost": "~2 div",
                    "risk": "low",
                    "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Saves you from later Annulment costs.",
                },
                {
                    "label": "Skip Omen (YOLO)",
                    "cost": "~0.1 div (orb only)",
                    "risk": "medium",
                    "description": "Random side. 50/50 chance it lands where you want. If wrong, you'll need an Annul (~14 div with omen) to fix it.",
                },
                {
                    "label": "Use Omen of Greater Exaltation Instead",
                    "cost": "~1 div (Greater Exalt Omen)",
                    "risk": "medium",
                    "description": "Adds 2 mods instead of 1 but you lose directional control. Faster if you're filling both sides.",
                },
            ],
            "7.1": [
                {
                    "label": "Full Whittling (Recommended)",
                    "cost": "~20 div/attempt",
                    "risk": "low",
                    "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Removes only the LOWEST ilvl mod — your T1s are safe.",
                },
                {
                    "label": "Budget Whittling",
                    "cost": "~5 div/attempt",
                    "risk": "high",
                    "description": "Perfect Chaos without omens. Removes a RANDOM mod — can destroy your T1s. Only recommended if Whittling omens are unavailable.",
                },
            ],
            "10.2": [
                {
                    "label": "Use Hinekora's Lock (Safe)",
                    "cost": "~150 div per Lock",
                    "risk": "very low",
                    "description": "Preview the sanctify outcome before committing. If bad, modify the item to change the seed. Lock is consumed regardless.",
                },
                {
                    "label": "YOLO Sanctify",
                    "cost": "~1 div per Divine Orb",
                    "risk": "medium",
                    "description": "13% success rate per attempt. No preview — you see the result immediately. ~7-8 attempts expected.",
                },
                {
                    "label": "Use Omen of Sanctification (Guaranteed)",
                    "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                    "risk": "very low",
                    "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
                },
            ],
        },
        "orbs_used_overrides": {
            "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
            "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
        },
        "completed_message": (
            "Your 6x T1 mirror-tier wand is complete.\n"
            "A caster wand of this caliber is worth 600-1100+ divines.\n"
            "Every spell you cast will now obliterate everything.\n"
            "GG, Exile."
        ),
        "action": "Craft a mirror-tier wand",
    },
    "Sceptre": {
        "item_type": "weapon",
        "sub_type": "Sceptre",
        "quality_currency": "Blacksmith's Whetstone",
        "quality_count": 20,
        "quality_step_title": "Apply Quality",
        "quality_step_desc": (
            "Use 20x Blacksmith's Whetstones to reach 20% quality.\n"
            "This improves the base physical damage of the sceptre.\n"
            "Quality must be capped at 20% before using\n"
            "the Infuser in the next step.\n"
            "Cost: <1 Divine (trivial)"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": [
            "+X to Level of all Spell Skills (T3+) — check element type (Fire/Cold/Lightning/Chaos/Physical/Minion)",
            "+X to Level of all Minion Skills (T3+)",
            "% Increased Spell Damage (T1-T2)",
            "% Increased Minion Damage (T1-T2)",
            "+X to Level of all [Element/Type] Spell Skills",
            "% Increased Cast Speed (T1)",
            "% Increased Critical Hit Chance for Spells (T1)",
            "+% to Critical Spell Damage Bonus (T1)",
            "Adds # to # [Element] Damage to Spells (high roll)",
            "% Increased Spirit (if applicable)",
        ],
        "s_tier_trash": [
            "Any mod below T3 tier",
            "Added flat spell damage of wrong element",
            "Light Radius",
            "Accuracy Rating",
            "Stun-related mods (unless stun build)",
            "Life/Mana on kill",
            "Leech (unless build uses it)",
            "Attribute requirements mods",
            "Melee/physical attack mods",
            "Projectile attack mods",
            "Added flat attack damage",
        ],
        "s_tier_consider": [],
        "regal_omen_note": (
            "Sceptres have a large prefix pool (spell damage, minion damage, gem levels, flat damage). "
            "Dextral Coronation to force suffix (cast speed, crit, spirit) is often safer."
        ),
        "fracture_priority": [
            "+X to Level of all Spell/Minion Skills",
            "% Increased Spell/Minion Damage",
            "% Increased Cast Speed",
            "% Increased Spirit",
        ],
        "phase9_title": "Finalize",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Insert Runes",
                "description": (
                    "Use an Artificer's Orb to add sockets, then insert your runes.\n"
                    "Rune choices:\n"
                    "- Soul Rune: Spell/mana — best for most caster sceptres\n"
                    "- Iron Rune: Physical/minion builds\n"
                    "- Storm Rune: Lightning spell builds\n"
                    "- Desert Rune: Fire spell builds\n"
                    "- Glacier Rune: Cold spell builds\n"
                    "\n"
                    "If you have Perfect Runes (flawless versions), use them instead\n"
                    "for higher values."
                ),
                "orbs_used": ["Artificer's Orb"],
                "action": "Artificer's Orb for sockets + insert runes",
            },
            {
                "id": "9.2",
                "title": "Craft Complete!",
                "description": (
                    "Your mirror-tier sceptre is complete.\n"
                    "A 6x T1 sceptre with perfect caster or minion mods is\n"
                    "worth 600-1200+ divines depending on the mod combination.\n"
                    "Your minions or spells will now dominate Wraeclast.\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier sceptre",
            },
        ],
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": {
            "3.1": [
                {
                    "label": "Use Coronation Omen (Recommended)",
                    "cost": "~2 div",
                    "risk": "low",
                    "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Saves you from later Annulment costs.",
                },
                {
                    "label": "Skip Omen (YOLO)",
                    "cost": "~0.1 div (orb only)",
                    "risk": "medium",
                    "description": "Random side. 50/50 chance it lands where you want. If wrong, you'll need an Annul (~14 div with omen) to fix it.",
                },
                {
                    "label": "Use Omen of Greater Exaltation Instead",
                    "cost": "~1 div (Greater Exalt Omen)",
                    "risk": "medium",
                    "description": "Adds 2 mods instead of 1 but you lose directional control. Faster if you're filling both sides.",
                },
            ],
            "7.1": [
                {
                    "label": "Full Whittling (Recommended)",
                    "cost": "~20 div/attempt",
                    "risk": "low",
                    "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Removes only the LOWEST ilvl mod — your T1s are safe.",
                },
                {
                    "label": "Budget Whittling",
                    "cost": "~5 div/attempt",
                    "risk": "high",
                    "description": "Perfect Chaos without omens. Removes a RANDOM mod — can destroy your T1s. Only recommended if Whittling omens are unavailable.",
                },
            ],
            "10.2": [
                {
                    "label": "Use Hinekora's Lock (Safe)",
                    "cost": "~150 div per Lock",
                    "risk": "very low",
                    "description": "Preview the sanctify outcome before committing. If bad, modify the item to change the seed. Lock is consumed regardless.",
                },
                {
                    "label": "YOLO Sanctify",
                    "cost": "~1 div per Divine Orb",
                    "risk": "medium",
                    "description": "13% success rate per attempt. No preview — you see the result immediately. ~7-8 attempts expected.",
                },
                {
                    "label": "Use Omen of Sanctification (Guaranteed)",
                    "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                    "risk": "very low",
                    "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
                },
            ],
        },
        "orbs_used_overrides": {
            "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
            "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
        },
        "completed_message": (
            "Your 6x T1 mirror-tier sceptre is complete.\n"
            "A sceptre of this caliber with perfect caster or minion mods\n"
            "is worth 600-1200+ divines.\n"
            "GG, Exile."
        ),
        "action": "Craft a mirror-tier sceptre",
    },
    "Staff": {
        "item_type": "weapon",
        "sub_type": "Staff",
        "quality_currency": "Blacksmith's Whetstone",
        "quality_count": 20,
        "quality_step_title": "Apply Quality",
        "quality_step_desc": (
            "Use 20x Blacksmith's Whetstones to reach 20% quality.\n"
            "This improves the base physical damage of the staff.\n"
            "Quality must be capped at 20% before using\n"
            "the Infuser in the next step.\n"
            "Cost: <1 Divine (trivial)"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": [
            "+X to Level of all Spell Skills (T3+) — 2H staves roll higher values",
            "% Increased Spell Damage (T1-T2)",
            "% Increased Cast Speed (T1)",
            "% Increased Critical Hit Chance for Spells (T1)",
            "+% to Critical Spell Damage Bonus (T1)",
            "Adds # to # [Element] Damage to Spells (high roll)",
        ],
        "s_tier_trash": [
            "Any mod below T3 tier",
            "Added flat spell damage of wrong element",
            "Light Radius",
            "Accuracy Rating",
            "Stun-related mods (unless stun build)",
            "Life/Mana on kill",
            "Leech (unless build uses it)",
            "Attribute requirements mods",
            "Melee/physical attack mods",
            "Projectile attack mods",
            "Added flat attack damage",
        ],
        "s_tier_consider": [],
        "regal_omen_note": (
            "Staves have the highest +gem level ceiling of any weapon. "
            "Prefix pool is very large — Dextral Coronation to force suffix first is recommended."
        ),
        "fracture_priority": [
            "+X to Level of all Spell Skills (highest 2H values)",
            "% Increased Spell Damage",
            "% Increased Cast Speed",
        ],
        "phase9_title": "Finalize",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Insert Runes",
                "description": (
                    "Use an Artificer's Orb to add sockets, then insert your runes.\n"
                    "Rune choices:\n"
                    "- Soul Rune: Spell/mana — best for most caster staves\n"
                    "- Storm Rune: Lightning spell builds\n"
                    "- Desert Rune: Fire spell builds\n"
                    "- Glacier Rune: Cold spell builds\n"
                    "- Iron Rune: Physical spell builds\n"
                    "\n"
                    "If you have Perfect Runes (flawless versions), use them instead\n"
                    "for higher values."
                ),
                "orbs_used": ["Artificer's Orb"],
                "action": "Artificer's Orb for sockets + insert runes",
            },
            {
                "id": "9.2",
                "title": "Craft Complete!",
                "description": (
                    "Your 6x T1 mirror-tier staff is complete.\n"
                    "Staves have the highest +gem level ceilings —\n"
                    "this staff is among the most valuable caster weapons possible."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier staff",
            },
        ],
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": {
            "3.1": [
                {
                    "label": "Use Coronation Omen (Recommended)",
                    "cost": "~2 div",
                    "risk": "low",
                    "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Saves you from later Annulment costs.",
                },
                {
                    "label": "Skip Omen (YOLO)",
                    "cost": "~0.1 div (orb only)",
                    "risk": "medium",
                    "description": "Random side. 50/50 chance it lands where you want. If wrong, you'll need an Annul (~14 div with omen) to fix it.",
                },
                {
                    "label": "Use Omen of Greater Exaltation Instead",
                    "cost": "~1 div (Greater Exalt Omen)",
                    "risk": "medium",
                    "description": "Adds 2 mods instead of 1 but you lose directional control. Faster if you're filling both sides.",
                },
            ],
            "7.1": [
                {
                    "label": "Full Whittling (Recommended)",
                    "cost": "~20 div/attempt",
                    "risk": "low",
                    "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Removes only the LOWEST ilvl mod — your T1s are safe.",
                },
                {
                    "label": "Budget Whittling",
                    "cost": "~5 div/attempt",
                    "risk": "high",
                    "description": "Perfect Chaos without omens. Removes a RANDOM mod — can destroy your T1s. Only recommended if Whittling omens are unavailable.",
                },
            ],
            "10.2": [
                {
                    "label": "Use Hinekora's Lock (Safe)",
                    "cost": "~150 div per Lock",
                    "risk": "very low",
                    "description": "Preview the sanctify outcome before committing. If bad, modify the item to change the seed. Lock is consumed regardless.",
                },
                {
                    "label": "YOLO Sanctify",
                    "cost": "~1 div per Divine Orb",
                    "risk": "medium",
                    "description": "13% success rate per attempt. No preview — you see the result immediately. ~7-8 attempts expected.",
                },
                {
                    "label": "Use Omen of Sanctification (Guaranteed)",
                    "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                    "risk": "very low",
                    "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
                },
            ],
        },
        "orbs_used_overrides": {
            "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
            "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
        },
        "completed_message": (
            "Your 6x T1 mirror-tier staff is complete.\n"
            "Staves have the highest +gem level ceilings —\n"
            "this staff is among the most valuable caster weapons possible."
        ),
        "action": "Craft a mirror-tier staff",
    },
    "Quarterstaff": {
        "item_type": "weapon",
        "sub_type": "Quarterstaff",
        "quality_currency": "Blacksmith's Whetstone",
        "quality_count": 20,
        "quality_step_title": "Apply Quality",
        "quality_step_desc": (
            "Use 20x Blacksmith's Whetstones to reach 20% quality.\n"
            "This improves the base physical damage of the quarterstaff.\n"
            "Quality must be capped at 20% before using\n"
            "the Infuser in the next step.\n"
            "Cost: <1 Divine (trivial)"
        ),
        "exceptional_base_step": None,
        "s_tier_keep": [
            "+X to Level of all Melee Skills (T3+)",
            "% Increased Physical Damage (T1-T2)",
            "Adds # to # Physical Damage (high roll)",
            "Adds # to # Elemental Damage (high roll)",
            "% Increased Attack Speed (T1)",
            "% Increased Critical Hit Chance (T1)",
            "+% to Critical Damage Bonus (T1)",
        ],
        "s_tier_trash": [
            "Any mod below T3 tier",
            "Added flat damage of wrong element",
            "Light Radius",
            "Accuracy Rating",
            "Stun-related mods (unless stun build)",
            "Life/Mana on kill",
            "Leech (unless build uses it)",
            "Attribute requirements mods",
        ],
        "s_tier_consider": [],
        "regal_omen_note": "",
        "fracture_priority": [
            "+X to Level of all Melee Skills",
            "% Increased Physical Damage",
            "Adds # to # Elemental Damage",
        ],
        "phase9_title": "Finalize",
        "phase9_steps": [
            {
                "id": "9.1",
                "title": "Insert Runes",
                "description": (
                    "Use an Artificer's Orb to add sockets, then insert your runes.\n"
                    "Rune choices depending on build:\n"
                    "- Iron Rune: Physical damage\n"
                    "- Storm Rune: Lightning damage (lightning builds)\n"
                    "- Desert Rune: Fire damage (fire builds)\n"
                    "- Glacier Rune: Cold damage (cold/freeze builds)\n"
                    "- Soul Rune: Mana — rarely used on quarterstaves\n"
                    "\n"
                    "If you have Perfect Runes (flawless versions), use them instead\n"
                    "for higher values."
                ),
                "orbs_used": ["Artificer's Orb"],
                "action": "Artificer's Orb for sockets + insert runes",
            },
            {
                "id": "9.2",
                "title": "Craft Complete!",
                "description": (
                    "Your mirror-tier quarterstaff is complete.\n"
                    "A 6x T1 quarterstaff blending martial and elemental mods\n"
                    "is worth 700-1300+ divines.\n"
                    "Your monk will now obliterate everything in sight.\n"
                    "GG, Exile."
                ),
                "orbs_used": [],
                "action": "Admire your completed mirror-tier quarterstaff",
            },
        ],
        "phase10_title": "Phase 10: Sanctify",
        "alternatives": {
            "3.1": [
                {
                    "label": "Use Coronation Omen (Recommended)",
                    "cost": "~2 div",
                    "risk": "low",
                    "description": "Guarantees the Regal adds to your chosen side (prefix or suffix). Saves you from later Annulment costs.",
                },
                {
                    "label": "Skip Omen (YOLO)",
                    "cost": "~0.1 div (orb only)",
                    "risk": "medium",
                    "description": "Random side. 50/50 chance it lands where you want. If wrong, you'll need an Annul (~14 div with omen) to fix it.",
                },
                {
                    "label": "Use Omen of Greater Exaltation Instead",
                    "cost": "~1 div (Greater Exalt Omen)",
                    "risk": "medium",
                    "description": "Adds 2 mods instead of 1 but you lose directional control. Faster if you're filling both sides.",
                },
            ],
            "7.1": [
                {
                    "label": "Full Whittling (Recommended)",
                    "cost": "~20 div/attempt",
                    "risk": "low",
                    "description": "Omen of Whittling (~15 div) + Perfect Chaos (~5 div). Removes only the LOWEST ilvl mod — your T1s are safe.",
                },
                {
                    "label": "Budget Whittling",
                    "cost": "~5 div/attempt",
                    "risk": "high",
                    "description": "Perfect Chaos without omens. Removes a RANDOM mod — can destroy your T1s. Only recommended if Whittling omens are unavailable.",
                },
            ],
            "10.2": [
                {
                    "label": "Use Hinekora's Lock (Safe)",
                    "cost": "~150 div per Lock",
                    "risk": "very low",
                    "description": "Preview the sanctify outcome before committing. If bad, modify the item to change the seed. Lock is consumed regardless.",
                },
                {
                    "label": "YOLO Sanctify",
                    "cost": "~1 div per Divine Orb",
                    "risk": "medium",
                    "description": "13% success rate per attempt. No preview — you see the result immediately. ~7-8 attempts expected.",
                },
                {
                    "label": "Use Omen of Sanctification (Guaranteed)",
                    "cost": "~1.4 div (1 Divine + ~0.4 Omen)",
                    "risk": "very low",
                    "description": "Omen of Sanctification guarantees 100% sanctify success on your next Divine Orb. Spend ~0.4 div to skip the RNG entirely.",
                },
            ],
        },
        "orbs_used_overrides": {
            "3.1": ["Perfect Regal Orb", "Omen of Dextral Coronation"],
            "6.1": ["Perfect Exalted Orb", "Omen of Dextral Exaltation"],
        },
        "completed_message": (
            "Your 6x T1 mirror-tier quarterstaff is complete.\n"
            "A quarterstaff of this caliber is worth 700-1300+ divines.\n"
            "GG, Exile."
        ),
        "action": "Craft a mirror-tier quarterstaff",
    },
}
