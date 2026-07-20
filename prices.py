import urllib.request
import json
import threading

FALLBACK_PRICES = {
    "Divine Orb": {"chaos": 38, "divine": 1.0},
    "Chaos Orb": {"chaos": 1, "divine": 0.026},
    "Exalted Orb": {"chaos": 0.11, "divine": 0.003},
    "Perfect Exalted Orb": {"chaos": 108, "divine": 2.83},
    "Perfect Chaos Orb": {"chaos": 197, "divine": 5.18},
    "Greater Chaos Orb": {"chaos": 14, "divine": 0.38},
    "Greater Exalted Orb": {"chaos": 3, "divine": 0.016},
    "Orb of Annulment": {"chaos": 25, "divine": 0.66},
    "Fracturing Orb": {"chaos": 390, "divine": 10.1},
    "Orb of Alchemy": {"chaos": 0.09, "divine": 0.002},
    "Omen of Whittling": {"chaos": 570, "divine": 15},
    "Omen of Sinistral Annulment": {"chaos": 532, "divine": 14},
    "Omen of Dextral Annulment": {"chaos": 532, "divine": 14},
    "Omen of Sinistral Erasure": {"chaos": 380, "divine": 10},
    "Omen of Dextral Erasure": {"chaos": 380, "divine": 10},
    "Omen of Sinistral Exaltation": {"chaos": 228, "divine": 6},
    "Omen of Dextral Exaltation": {"chaos": 228, "divine": 6},
    "Omen of Greater Exaltation": {"chaos": 38, "divine": 1},
    "Omen of Abyssal Echoes": {"chaos": 760, "divine": 20},
    "Omen of Greater Annulment": {"chaos": 190, "divine": 5},
    "Omen of Dextral Coronation": {"chaos": 76, "divine": 2},
    "Omen of Sinistral Coronation": {"chaos": 76, "divine": 2},
    "Omen of Sanctification": {"chaos": 15, "divine": 0.4},
    "Perfect Orb of Transmutation": {"chaos": 0.76, "divine": 0.02},
    "Perfect Orb of Augmentation": {"chaos": 0.76, "divine": 0.02},
    "Perfect Regal Orb": {"chaos": 3.8, "divine": 0.1},
    "Artificer's Orb": {"chaos": 0.1, "divine": 0.003},
    "Blacksmith's Whetstone": {"chaos": 0.02, "divine": 0.0005},
    "Greater Transmutation Orb": {"chaos": 0.1, "divine": 0.003},
    "Greater Augmentation Orb": {"chaos": 0.1, "divine": 0.003},
    "Greater Regal Orb": {"chaos": 0.5, "divine": 0.013},
    "Vaal Blacksmith's Infuser": {"chaos": 95, "divine": 2.5},
    "Hinekora's Lock": {"chaos": 5700, "divine": 150.0},
    "Armourer's Scrap": {"chaos": 0.02, "divine": 0.0005},
    "Flesh Catalyst": {"chaos": 3, "divine": 0.08},
    "Neural Catalyst": {"chaos": 3, "divine": 0.08},
    "Carapace Catalyst": {"chaos": 2, "divine": 0.05},
    "Uul-Netol's Catalyst": {"chaos": 5, "divine": 0.13},
    "Xoph's Catalyst": {"chaos": 5, "divine": 0.13},
    "Tul's Catalyst": {"chaos": 4, "divine": 0.11},
    "Esh's Catalyst": {"chaos": 4, "divine": 0.11},
    "Chayula's Catalyst": {"chaos": 8, "divine": 0.21},
    "Reaver Catalyst": {"chaos": 4, "divine": 0.11},
    "Sibilant Catalyst": {"chaos": 4, "divine": 0.11},
    "Skittering Catalyst": {"chaos": 6, "divine": 0.16},
    "Adaptive Catalyst": {"chaos": 3, "divine": 0.08},
    "Necrotic Catalyst": {"chaos": 2, "divine": 0.05},
    "Distilled Emotion": {"chaos": 15, "divine": 0.39},
    "Catalyst": {"chaos": 3, "divine": 0.08},
}

POE2_CURRENCY_API = (
    "https://poe.ninja/api/data/poe2/currencyoverview"
    "?league=Standard&type=Currency"
)

CACHED_PRICES = dict(FALLBACK_PRICES)
PRICE_CACHE_VALID = True
PRICE_SOURCE = "static"
ORB_ICON_URLS = {}
_fetch_lock = threading.Lock()

ORB_NAME_MAP = {
    "Divine Orb": "Divine Orb",
    "Chaos Orb": "Chaos Orb",
    "Exalted Orb": "Exalted Orb",
    "Orb of Annulment": "Orb of Annulment",
    "Perfect Exalted Orb": "Perfect Exalted Orb",
    "Perfect Chaos Orb": "Perfect Chaos Orb",
    "Greater Chaos Orb": "Greater Chaos Orb",
    "Greater Exalted Orb": "Greater Exalted Orb",
    "Orb of Alchemy": "Orb of Alchemy",
    "Fracturing Orb": "Fracturing Orb",
    "Omen of Whittling": "Omen of Whittling",
    "Omen of Sinistral Annulment": "Omen of Sinistral Annulment",
    "Omen of Dextral Annulment": "Omen of Dextral Annulment",
    "Omen of Sinistral Erasure": "Omen of Sinistral Erasure",
    "Omen of Dextral Erasure": "Omen of Dextral Erasure",
    "Omen of Sinistral Exaltation": "Omen of Sinistral Exaltation",
    "Omen of Dextral Exaltation": "Omen of Dextral Exaltation",
    "Omen of Greater Exaltation": "Omen of Greater Exaltation",
    "Omen of Abyssal Echoes": "Omen of Abyssal Echoes",
    "Omen of Greater Annulment": "Omen of Greater Annulment",
    "Omen of Dextral Coronation": "Omen of Dextral Coronation",
    "Omen of Sinistral Coronation": "Omen of Sinistral Coronation",
    "Omen of Sanctification": "Omen of Sanctification",
    "Perfect Orb of Transmutation": "Perfect Orb of Transmutation",
    "Perfect Orb of Augmentation": "Perfect Orb of Augmentation",
    "Perfect Regal Orb": "Perfect Regal Orb",
    "Artificer's Orb": "Artificer's Orb",
    "Blacksmith's Whetstone": "Blacksmith's Whetstone",
    "Greater Transmutation Orb": "Greater Transmutation Orb",
    "Greater Augmentation Orb": "Greater Augmentation Orb",
    "Greater Regal Orb": "Greater Regal Orb",
    "Hinekora's Lock": "Hinekora's Lock",
    "Armourer's Scrap": "Armourer's Scrap",
    "Flesh Catalyst": "Flesh Catalyst",
    "Distilled Emotion": "Distilled Emotion",
}


def _parse_price(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _normalize(name):
    return name.lower().replace("'", "").replace(" ", "")


def fetch_prices_async(callback=None):
    def _fetch():
        global CACHED_PRICES, PRICE_CACHE_VALID, PRICE_SOURCE, ORB_ICON_URLS
        with _fetch_lock:
            try:
                req = urllib.request.Request(
                    POE2_CURRENCY_API,
                    headers={"User-Agent": "PoE2CraftingGuide/1.0"},
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                lines = data.get("lines", [])
                if not lines:
                    raise ValueError("Empty API response")
                live_prices = {}
                live_icons = {}
                for entry in lines:
                    name = entry.get("currencyTypeName", "")
                    chaos_val = _parse_price(
                        entry.get("chaosEquivalent", 0)
                    )
                    receive_val = _parse_price(
                        entry.get("receive", {}).get("value", 0)
                    )
                    icon_url = entry.get("icon", "")
                    if icon_url:
                        live_icons[name] = icon_url
                    if chaos_val <= 0 and receive_val <= 0:
                        continue
                    divine_val = (
                        receive_val
                        if receive_val > 0
                        else chaos_val
                        / max(
                            live_prices.get("Divine Orb", {}).get(
                                "chaos", 1
                            ),
                            1,
                        )
                    )
                    live_prices[name] = {
                        "chaos": chaos_val,
                        "divine": divine_val,
                    }
                CACHED_PRICES.update(live_prices)
                ORB_ICON_URLS = dict(live_icons)
                PRICE_SOURCE = "live"
                PRICE_CACHE_VALID = True
                if callback:
                    callback(CACHED_PRICES)
            except Exception as e:
                CACHED_PRICES = dict(FALLBACK_PRICES)
                ORB_ICON_URLS = {}
                PRICE_SOURCE = "static"
                PRICE_CACHE_VALID = True
                if callback:
                    callback(None)

    t = threading.Thread(target=_fetch, daemon=True)
    t.start()
    return t


def get_price(orb_name):
    if orb_name in CACHED_PRICES:
        return CACHED_PRICES[orb_name]

    for api_name, mapped in ORB_NAME_MAP.items():
        if mapped.lower() == orb_name.lower() and api_name in CACHED_PRICES:
            return CACHED_PRICES[api_name]

    for key in CACHED_PRICES:
        if _normalize(orb_name) == _normalize(key):
            return CACHED_PRICES[key]

    return None


def prices_available():
    return PRICE_CACHE_VALID and len(CACHED_PRICES) > 0


def price_source():
    return PRICE_SOURCE


def get_icon_urls():
    return dict(ORB_ICON_URLS)
