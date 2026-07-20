"""PoE2 Modifier Reference — comprehensive prefix/suffix lookup by item type.

Each entry is a dict:
    name     - Human-readable mod template
    affix    - "prefix" or "suffix"
    types    - list of item sub-type names that can roll this mod
    tags     - list of searchable keywords (lowercase)
    tier_max - best possible tier (T1 or T0 via Sanctify)
"""

# fmt: off
_MODS = [
    # ═══════════════════════════════════════════════════════════════════════
    #  +Level to Gems  (the most valuable mod family)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+X to Level of all Projectile Skills",
        "affix": "prefix",
        "types": ["Bow", "Crossbow"],
        "tags": ["gem", "level", "projectile", "bow", "crossbow", "damage"],
        "tier_max": "T0",
    },
    {
        "name": "+X to Level of all Spell Skills",
        "affix": "prefix",
        "types": ["Wand", "Sceptre", "Staff", "Focus"],
        "tags": ["gem", "level", "spell", "caster", "damage"],
        "tier_max": "T0",
    },
    {
        "name": "+X to Level of all [Element] Spell Skills",
        "affix": "prefix",
        "types": ["Wand", "Sceptre", "Staff", "Focus"],
        "tags": ["gem", "level", "element", "fire", "cold", "lightning", "chaos", "physical", "spell"],
        "tier_max": "T0",
    },
    {
        "name": "+X to Level of all Melee Skills",
        "affix": "prefix",
        "types": ["Quarterstaff"],
        "tags": ["gem", "level", "melee", "quarterstaff", "monk", "damage"],
        "tier_max": "T0",
    },
    {
        "name": "+X to Level of all Skill Gems",
        "affix": "prefix",
        "types": ["Amulet"],
        "tags": ["gem", "level", "amulet", "skill", "rare", "valuable"],
        "tier_max": "T0",
    },
    {
        "name": "+X to Level of Socketed Gems",
        "affix": "prefix",
        "types": ["Helmet"],
        "tags": ["gem", "level", "helmet", "socket", "rare"],
        "tier_max": "T0",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  % Increased Damage
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Physical Damage",
        "affix": "prefix",
        "types": ["Bow", "Crossbow", "Quarterstaff"],
        "tags": ["physical", "damage", "weapon", "attack", "%inc"],
        "tier_max": "T0",
    },
    {
        "name": "% Increased Spell Damage",
        "affix": "prefix",
        "types": ["Wand", "Sceptre", "Staff", "Focus"],
        "tags": ["spell", "damage", "caster", "%inc"],
        "tier_max": "T0",
    },
    {
        "name": "% Increased Elemental Damage with Attacks",
        "affix": "prefix",
        "types": ["Bow", "Crossbow", "Ring"],
        "tags": ["elemental", "damage", "attack", "%inc", "fire", "cold", "lightning"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased [Type] Damage",
        "affix": "prefix",
        "types": ["Ring", "Belt"],
        "tags": ["damage", "%inc", "elemental", "attack", "caster"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Added Flat Damage
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "Adds # to # Physical Damage",
        "affix": "prefix",
        "types": ["Bow", "Crossbow", "Quarterstaff"],
        "tags": ["flat", "physical", "damage", "weapon", "attack"],
        "tier_max": "T0",
    },
    {
        "name": "Adds # to # Fire/Cold/Lightning Damage",
        "affix": "prefix",
        "types": ["Bow", "Crossbow", "Quarterstaff"],
        "tags": ["flat", "elemental", "damage", "fire", "cold", "lightning", "weapon"],
        "tier_max": "T0",
    },
    {
        "name": "Adds # to # [Element] Damage to Spells",
        "affix": "prefix",
        "types": ["Wand", "Sceptre", "Staff"],
        "tags": ["flat", "elemental", "damage", "spell", "caster"],
        "tier_max": "T0",
    },
    {
        "name": "Adds # to # Physical Damage to Attacks",
        "affix": "prefix",
        "types": ["Ring", "Gloves"],
        "tags": ["flat", "physical", "damage", "attack", "ring", "gloves"],
        "tier_max": "T2",
    },
    {
        "name": "Adds # to # [Element] Damage to Attacks",
        "affix": "prefix",
        "types": ["Ring", "Gloves"],
        "tags": ["flat", "elemental", "damage", "attack", "ring", "gloves"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Attack Speed  (suffix on weapons / gloves)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Attack Speed",
        "affix": "suffix",
        "types": ["Bow", "Crossbow", "Quarterstaff", "Gloves", "Ring"],
        "tags": ["attack", "speed", "aspd", "dps"],
        "tier_max": "T1",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Cast Speed  (suffix on caster items)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Cast Speed",
        "affix": "suffix",
        "types": ["Wand", "Sceptre", "Staff", "Focus", "Ring", "Amulet"],
        "tags": ["cast", "speed", "cspd", "caster", "spell"],
        "tier_max": "T1",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Critical Strike  (mostly suffixes)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Critical Hit Chance",
        "affix": "suffix",
        "types": ["Bow", "Crossbow", "Quarterstaff", "Helmet", "Ring"],
        "tags": ["crit", "critical", "chance", "strike"],
        "tier_max": "T1",
    },
    {
        "name": "% Increased Critical Hit Chance for Spells",
        "affix": "suffix",
        "types": ["Wand", "Sceptre", "Staff", "Focus"],
        "tags": ["crit", "critical", "chance", "spell", "caster"],
        "tier_max": "T1",
    },
    {
        "name": "+% to Critical Damage Bonus",
        "affix": "suffix",
        "types": ["Bow", "Crossbow", "Quarterstaff", "Ring"],
        "tags": ["crit", "critical", "multi", "damage", "bonus"],
        "tier_max": "T1",
    },
    {
        "name": "+% to Critical Spell Damage Bonus",
        "affix": "suffix",
        "types": ["Wand", "Sceptre", "Staff", "Focus"],
        "tags": ["crit", "critical", "multi", "damage", "spell", "caster"],
        "tier_max": "T1",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Defences  (prefixes on armour)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Armour / Evasion / Energy Shield",
        "affix": "prefix",
        "types": ["Body Armour", "Helmet", "Boots", "Gloves", "Shield"],
        "tags": ["defence", "armour", "evasion", "es", "%inc", "body", "helm", "boots", "shield"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Energy Shield",
        "affix": "prefix",
        "types": ["Focus"],
        "tags": ["defence", "es", "energy shield", "%inc", "focus"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Global Defences",
        "affix": "prefix",
        "types": ["Amulet", "Belt"],
        "tags": ["defence", "global", "armour", "evasion", "es", "amulet", "belt"],
        "tier_max": "T2",
    },
    {
        "name": "Hybrid %Defence + Life",
        "affix": "prefix",
        "types": ["Body Armour"],
        "tags": ["defence", "life", "hybrid", "body", "armour", "evasion", "es"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Life / Energy Shield  (prefixes)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+# to maximum Life",
        "affix": "prefix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["life", "life", "hp", "defence", "survival", "universal"],
        "tier_max": "T2",
    },
    {
        "name": "+# to maximum Energy Shield",
        "affix": "prefix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Shield", "Focus",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["es", "energy shield", "defence", "survival"],
        "tier_max": "T2",
    },
    {
        "name": "+# to maximum Mana",
        "affix": "prefix",
        "types": ["Helmet", "Boots", "Gloves", "Shield", "Focus"],
        "tags": ["mana", "mom", "mind over matter", "caster"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Resistances  (suffixes)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+#% to Fire Resistance",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield", "Focus",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["resist", "fire", "elemental", "defence"],
        "tier_max": "T2",
    },
    {
        "name": "+#% to Cold Resistance",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield", "Focus",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["resist", "cold", "elemental", "defence"],
        "tier_max": "T2",
    },
    {
        "name": "+#% to Lightning Resistance",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield", "Focus",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["resist", "lightning", "elemental", "defence"],
        "tier_max": "T2",
    },
    {
        "name": "+#% to Chaos Resistance",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield", "Focus",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["resist", "chaos", "defence", "rare", "valuable"],
        "tier_max": "T2",
    },
    {
        "name": "+#% to all Maximum Resistances",
        "affix": "suffix",
        "types": ["Amulet"],
        "tags": ["resist", "max res", "all res", "amulet", "rare"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Attributes  (suffixes)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+# to Strength",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["attribute", "str", "strength"],
        "tier_max": "T2",
    },
    {
        "name": "+# to Dexterity",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["attribute", "dex", "dexterity"],
        "tier_max": "T2",
    },
    {
        "name": "+# to Intelligence",
        "affix": "suffix",
        "types": [
            "Body Armour", "Helmet", "Boots", "Gloves", "Shield", "Focus",
            "Ring", "Amulet", "Belt",
        ],
        "tags": ["attribute", "int", "intelligence", "int"],
        "tier_max": "T2",
    },
    {
        "name": "+# to all Attributes",
        "affix": "suffix",
        "types": ["Ring", "Amulet", "Belt"],
        "tags": ["attribute", "all attrs", "omni", "str", "dex", "int"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Movement Speed  (boots-only suffix)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "#% increased Movement Speed",
        "affix": "suffix",
        "types": ["Boots"],
        "tags": ["movement", "speed", "movespeed", "ms", "boots", "essential"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Block / Shield
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+#% to Block Chance",
        "affix": "prefix",
        "types": ["Shield"],
        "tags": ["block", "shield", "defence", "tank"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Spell Block Chance",
        "affix": "prefix",
        "types": ["Shield"],
        "tags": ["block", "spell block", "shield", "defence", "caster"],
        "tier_max": "T2",
    },
    {
        "name": "#% of Block Chance applied to Spells",
        "affix": "suffix",
        "types": ["Shield"],
        "tags": ["block", "spell block", "shield", "defence"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Block Recovery",
        "affix": "suffix",
        "types": ["Shield"],
        "tags": ["block", "recovery", "shield"],
        "tier_max": "T1",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Life Recovery / Flasks / Leech
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Life Recovery Rate",
        "affix": "suffix",
        "types": ["Body Armour"],
        "tags": ["life", "recovery", "regen", "body"],
        "tier_max": "T2",
    },
    {
        "name": "% Additional Physical Damage Reduction",
        "affix": "suffix",
        "types": ["Body Armour"],
        "tags": ["physical", "reduction", "pdr", "defence", "tank", "body"],
        "tier_max": "T2",
    },
    {
        "name": "Physical Damage taken as Element",
        "affix": "prefix",
        "types": ["Body Armour"],
        "tags": ["phys", "taken as", "elemental", "shift", "defence", "body"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Flask Life Recovery Rate",
        "affix": "suffix",
        "types": ["Belt", "Ring"],
        "tags": ["flask", "life", "recovery", "belt"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Flask Mana Recovery Rate",
        "affix": "suffix",
        "types": ["Belt", "Ring"],
        "tags": ["flask", "mana", "recovery", "belt"],
        "tier_max": "T2",
    },
    {
        "name": "#% increased Flask Charges Gained",
        "affix": "suffix",
        "types": ["Belt"],
        "tags": ["flask", "charges", "belt"],
        "tier_max": "T2",
    },
    {
        "name": "#% reduced Flask Charges Used",
        "affix": "suffix",
        "types": ["Belt"],
        "tags": ["flask", "charges", "belt"],
        "tier_max": "T2",
    },
    {
        "name": "#% of Physical Damage Leeched as Life",
        "affix": "suffix",
        "types": ["Bow", "Crossbow", "Quarterstaff", "Ring", "Amulet"],
        "tags": ["leech", "life", "physical", "recovery"],
        "tier_max": "T2",
    },
    {
        "name": "#% of Physical Damage Leeched as Mana",
        "affix": "suffix",
        "types": ["Bow", "Crossbow", "Quarterstaff", "Ring", "Amulet"],
        "tags": ["leech", "mana", "physical", "recovery"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Rarity / Mana Regen / Utility
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Rarity of Items Found",
        "affix": "suffix",
        "types": ["Helmet", "Boots", "Gloves", "Ring", "Amulet"],
        "tags": ["rarity", "iir", "magic find", "mf", "loot"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Mana Regeneration Rate",
        "affix": "suffix",
        "types": ["Helmet", "Focus", "Ring", "Amulet"],
        "tags": ["mana", "regen", "caster", "recovery"],
        "tier_max": "T2",
    },
    {
        "name": "% Reduced Effect of Curses on You",
        "affix": "suffix",
        "types": ["Ring", "Amulet", "Belt"],
        "tags": ["curse", "utility", "defence", "map mod"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Boots-specific
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "#% chance to gain Onslaught on Kill",
        "affix": "suffix",
        "types": ["Boots"],
        "tags": ["onslaught", "speed", "boots", "movement"],
        "tier_max": "T1",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Gloves-specific
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+# to Melee Strike Range",
        "affix": "suffix",
        "types": ["Gloves"],
        "tags": ["melee", "range", "strike", "gloves", "attack"],
        "tier_max": "T1",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Belt-specific
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "+# Charm Slots",
        "affix": "implicit",
        "types": ["Belt"],
        "tags": ["charm", "slots", "implicit", "belt"],
        "tier_max": "base",
    },
    {
        "name": "% Increased Effect of Charms",
        "affix": "suffix",
        "types": ["Belt"],
        "tags": ["charm", "belt", "effect"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Cooldown Recovery Rate",
        "affix": "suffix",
        "types": ["Belt"],
        "tags": ["cdr", "cooldown", "belt", "caster", "travel"],
        "tier_max": "T2",
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  Consider / Situational
    # ═══════════════════════════════════════════════════════════════════════
    {
        "name": "% Increased Stun Threshold",
        "affix": "suffix",
        "types": ["Body Armour", "Helmet", "Boots", "Gloves", "Shield"],
        "tags": ["stun", "threshold", "defence", "situational"],
        "tier_max": "T2",
    },
    {
        "name": "% Reduced Extra Damage from Critical Strikes",
        "affix": "suffix",
        "types": ["Body Armour"],
        "tags": ["crit", "reduction", "defence", "body"],
        "tier_max": "T2",
    },
    {
        "name": "% Increased Spirit",
        "affix": "suffix",
        "types": ["Sceptre"],
        "tags": ["spirit", "sceptre", "minion", "aura"],
        "tier_max": "T1",
    },
    {
        "name": "% Chance to Avoid Elemental Ailments",
        "affix": "suffix",
        "types": ["Ring", "Amulet", "Belt"],
        "tags": ["ailment", "avoid", "shock", "freeze", "ignite"],
        "tier_max": "T2",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
#  Item-type → category mapping
# ═══════════════════════════════════════════════════════════════════════════

_ITEM_CATEGORIES = {
    "Bow": "Weapons",
    "Crossbow": "Weapons",
    "Wand": "Weapons",
    "Sceptre": "Weapons",
    "Staff": "Weapons",
    "Quarterstaff": "Weapons",
    "Body Armour": "Armour",
    "Helmet": "Armour",
    "Boots": "Armour",
    "Gloves": "Armour",
    "Shield": "Armour",
    "Focus": "Armour",
    "Ring": "Jewellery",
    "Amulet": "Jewellery",
    "Belt": "Jewellery",
}


def search_mods(query, category=None, item_type=None):
    """Return list of matching mod dicts.

    query     - case-insensitive partial match against name + tags
    category  - optional filter: "Weapons" | "Armour" | "Jewellery"
    item_type - optional filter: specific sub-type e.g. "Bow", "Ring"
    """
    q = query.strip().lower()
    if not q:
        return []

    results = []
    for mod in _MODS:
        # item-type filter (most restrictive first)
        if item_type and item_type not in mod["types"]:
            continue

        # category filter
        if category and not any(
            _ITEM_CATEGORIES.get(t) == category for t in mod["types"]
        ):
            continue

        # match against name (normalised) + tags
        searchable = mod["name"].lower() + " " + " ".join(mod["tags"])
        if q in searchable:
            results.append(mod)

    return results


def mods_for_item_type(item_type):
    """Return all mods that can roll on a given item sub-type."""
    return [m for m in _MODS if item_type in m["types"]]


def all_mods_for_category(category):
    """Return all mods for a category (Weapons / Armour / Jewellery)."""
    results = []
    seen = set()
    for mod in _MODS:
        for t in mod["types"]:
            if _ITEM_CATEGORIES.get(t) == category and mod["name"] not in seen:
                results.append(mod)
                seen.add(mod["name"])
    return results


def prefix_only(mods):
    return [m for m in mods if m["affix"] == "prefix"]


def suffix_only(mods):
    return [m for m in mods if m["affix"] == "suffix"]


def get_affix_badge(mod):
    """Return (label, color) for the affix badge."""
    badges = {
        "prefix": ("PREFIX", (180, 95, 30)),    # orange
        "suffix": ("SUFFIX", (60, 120, 180)),    # blue
        "implicit": ("IMPLICIT", (150, 30, 150)),  # purple
    }
    return badges.get(mod["affix"], ("???", (100, 100, 100)))
