"""PoE2 Crafting Phases — Weapon, Armour, Jewellery"""

from .base_phases import build_phases
from .weapon_phases import WEAPON_SUBTYPE_DATA
from .armour_phases import ARMOUR_SUBTYPE_DATA
from .jewellery_phases import JEWELLERY_SUBTYPE_DATA

# =============================================================================
#  Per-category mirror-tier orb configurations
# =============================================================================

_WEAPON_BUDGET_TIERS = {
    "Mirror": {
        "label": "Mirror Craft",
        "description": "Perfect approach — maximum safety, 6x T1 guaranteed",
        "orbs": {
            "Perfect Orb of Transmutation": 30,
            "Perfect Orb of Augmentation": 30,
            "Perfect Regal Orb": 8,
            "Omen of Dextral Coronation": 3,
            "Perfect Chaos Orb": 30,
            "Omen of Dextral Erasure": 6,
            "Orb of Annulment": 5,
            "Omen of Dextral Annulment": 3,
            "Perfect Exalted Orb": 20,
            "Omen of Dextral Exaltation": 5,
            "Omen of Sinistral Exaltation": 5,
            "Fracturing Orb": 5,
            "Omen of Whittling": 25,
            "Divine Orb": 40,
            "Omen of Sanctification": 2,
            "Hinekora's Lock": 2,
            "Vaal Blacksmith's Infuser": 2,
            "Artificer's Orb": 2,
        },
    },
}

_ARMOUR_BUDGET_TIERS = {
    "Mirror": {
        "label": "Mirror Craft",
        "description": "Perfect approach — max safety, mirror-service ready",
        "orbs": {
            "Perfect Orb of Transmutation": 25,
            "Perfect Orb of Augmentation": 25,
            "Perfect Regal Orb": 6,
            "Omen of Dextral Coronation": 3,
            "Perfect Chaos Orb": 25,
            "Omen of Dextral Erasure": 5,
            "Orb of Annulment": 4,
            "Omen of Dextral Annulment": 3,
            "Perfect Exalted Orb": 16,
            "Omen of Dextral Exaltation": 4,
            "Omen of Sinistral Exaltation": 4,
            "Fracturing Orb": 5,
            "Omen of Whittling": 20,
            "Divine Orb": 35,
            "Omen of Sanctification": 2,
            "Hinekora's Lock": 2,
            "Artificer's Orb": 2,
            "Armourer's Scrap": 20,
        },
    },
}

_JEWELLERY_BUDGET_TIERS = {
    "Mirror": {
        "label": "Mirror Craft",
        "description": "Flawless approach — maximum safety, mirror-service ready",
        "orbs": {
            "Perfect Orb of Transmutation": 20,
            "Perfect Orb of Augmentation": 20,
            "Perfect Regal Orb": 5,
            "Omen of Dextral Coronation": 2,
            "Perfect Chaos Orb": 20,
            "Omen of Dextral Erasure": 3,
            "Orb of Annulment": 4,
            "Omen of Dextral Annulment": 3,
            "Perfect Exalted Orb": 12,
            "Omen of Dextral Exaltation": 3,
            "Omen of Sinistral Exaltation": 3,
            "Fracturing Orb": 5,
            "Omen of Whittling": 15,
            "Divine Orb": 30,
            "Omen of Sanctification": 2,
            "Hinekora's Lock": 2,
            "Catalyst": 20,
            "Distilled Emotion": 3,
        },
    },
}

CATEGORIES = {
    "Weapons": {
        "icon": "weapon",
        "sub_types": list(WEAPON_SUBTYPE_DATA.keys()),
        "data": WEAPON_SUBTYPE_DATA,
        "description": "Swords, Axes, Maces, Bows, Wands, Staves, Sceptres, Quarterstaves, Crossbows — anything you wield.",
        "budget_tiers": _WEAPON_BUDGET_TIERS,
    },
    "Armour": {
        "icon": "armour",
        "sub_types": list(ARMOUR_SUBTYPE_DATA.keys()),
        "data": ARMOUR_SUBTYPE_DATA,
        "description": "Body Armour, Helmets, Boots, Gloves, Shields — your defensive shell.",
        "budget_tiers": _ARMOUR_BUDGET_TIERS,
    },
    "Jewellery": {
        "icon": "jewellery",
        "sub_types": list(JEWELLERY_SUBTYPE_DATA.keys()),
        "data": JEWELLERY_SUBTYPE_DATA,
        "description": "Rings, Amulets, Belts — where life, resists, and power converge.",
        "budget_tiers": _JEWELLERY_BUDGET_TIERS,
    },
}


def calculate_tier_thresholds(category_name):
    """Calculate mirror-tier cost (in Divine Orbs) using live prices.

    Returns a list with a single dict:
        [{key, label, description, threshold, color}]
    where 'threshold' is None (open-ended).
    """
    from prices import get_price

    cat = CATEGORIES.get(category_name)
    if cat is None:
        return default_tier_thresholds()

    tiers_config = cat.get("budget_tiers")
    if tiers_config is None:
        return default_tier_thresholds()

    config = tiers_config.get("Mirror")
    if config is None:
        return default_tier_thresholds()

    total_div = 0.0
    orbs = config.get("orbs", {})
    for orb_name, qty in orbs.items():
        if qty <= 0:
            continue
        price = get_price(orb_name)
        if price:
            total_div += price.get("divine", 0) * qty
        else:
            total_div += 0.1 * qty

    return [{
        "key": "Mirror",
        "label": config["label"],
        "description": config.get("description", ""),
        "threshold": None,
        "color": "red",
    }]


def default_tier_thresholds():
    """Fallback mirror-tier threshold when no category is selected."""
    return [
        {"key": "Mirror", "label": "Mirror Craft", "description": "Maximum safety, 6x T1 guaranteed", "threshold": None, "color": "red"},
    ]


def get_phases(category, sub_type):
    """Build and return the full crafting phase list for a given category + sub-type."""
    cat = CATEGORIES.get(category)
    if cat is None:
        raise KeyError(f"Unknown category: {category}")
    custom = cat["data"].get(sub_type)
    if custom is None:
        raise KeyError(f"Unknown sub-type '{sub_type}' in category '{category}'")
    return build_phases(custom)


def get_categories():
    """Return the CATEGORIES dict."""
    return CATEGORIES
