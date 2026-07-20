import os
import shutil
import urllib.request
import pygame
import threading

_APP_NAME = "poe2-mirror-crafter"


def _get_appdata_dir():
    appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
    path = os.path.join(appdata, _APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def _get_legacy_assets_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "currency_icons")


def _migrate_icons_from_legacy():
    legacy = _get_legacy_assets_dir()
    if not os.path.isdir(legacy):
        return
    target = _ASSETS_DIR
    moved = 0
    for entry in os.listdir(legacy):
        src = os.path.join(legacy, entry)
        dst = os.path.join(target, entry)
        if os.path.isfile(src) and not os.path.exists(dst):
            shutil.move(src, dst)
            moved += 1
    try:
        remaining = os.listdir(legacy)
        if not remaining:
            os.rmdir(legacy)
    except OSError:
        pass
    return moved


_ASSETS_DIR = os.path.join(_get_appdata_dir(), "assets", "currency_icons")
_icon_cache = {}
_icon_urls = {}
_download_lock = threading.Lock()
_download_done = False

CDN_BASE = "https://cdn.poe2db.tw/image"
CDN_FALLBACK_URLS = {
    "Divine Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyModValues.webp",
    "Chaos Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyRerollRare.webp",
    "Exalted Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyAddModToRare.webp",
    "Perfect Exalted Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyAddModToRare.webp",
    "Perfect Chaos Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyRerollRare.webp",
    "Orb of Annulment": f"{CDN_BASE}/Art/2DItems/Currency/AnnullOrb.webp",
    "Perfect Regal Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyUpgradeMagicToRare.webp",
    "Perfect Orb of Transmutation": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyUpgradeToMagic.webp",
    "Perfect Orb of Augmentation": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyAddModToMagic.webp",
    "Blacksmith's Whetstone": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyWeaponQuality.webp",
    "Artificer's Orb": f"{CDN_BASE}/Art/2DItems/Currency/CurrencyAddEquipmentSocket.webp",
    "Fracturing Orb": f"{CDN_BASE}/Art/2DItems/Currency/FracturingOrb.webp",
    "Vaal Blacksmith's Infuser": f"{CDN_BASE}/Art/2DItems/Currency/IncursionCraftingOrbs/VaalBlacksmithsWhetstone.webp",
    "Omen of Whittling": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens1Dark.webp",
    "Omen of Sinistral Annulment": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens2Purple.webp",
    "Omen of Dextral Annulment": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens3Purple.webp",
    "Omen of Sinistral Erasure": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens2Dark.webp",
    "Omen of Dextral Erasure": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens3Dark.webp",
    "Omen of Sinistral Exaltation": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens2Yellow.webp",
    "Omen of Dextral Exaltation": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens3Yellow.webp",
    "Omen of Sinistral Coronation": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens1Red.webp",
    "Omen of Dextral Coronation": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens2Red.webp",
    "Omen of Greater Exaltation": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens1Yellow.webp",
    "Omen of Greater Annulment": f"{CDN_BASE}/Art/2DItems/Currency/Omens/VoodooOmens1Purple.webp",
    "Omen of Abyssal Echoes": f"{CDN_BASE}/Art/2DItems/Currency/Omens/OmenOnAbyssRerollOptions.webp",
    "Omen of Sanctification": f"{CDN_BASE}/Art/2DItems/Currency/Omens/OmenOnDivineSanctify.webp",
    "Hinekora's Lock": f"{CDN_BASE}/Art/2DItems/Currency/HinekorasLock.webp",
}


def _ensure_assets_dir():
    if not os.path.isdir(_ASSETS_DIR):
        os.makedirs(_ASSETS_DIR)
    _migrate_icons_from_legacy()


def _sanitize_filename(name):
    out = name.replace(" ", "_")
    out = out.replace("'", "")
    out = out.replace('"', "")
    out = out.replace("/", "_")
    out = out.replace("\\", "_")
    return out


def _cache_path(orb_name):
    return os.path.join(_ASSETS_DIR, _sanitize_filename(orb_name) + ".png")


def load_cached_icons():
    _ensure_assets_dir()
    global _icon_cache
    _icon_cache = {}
    if not os.path.isdir(_ASSETS_DIR):
        return
    all_files = os.listdir(_ASSETS_DIR)
    for fname in all_files:
        if not fname.lower().endswith(".png"):
            continue
        full_path = os.path.join(_ASSETS_DIR, fname)
        try:
            img = pygame.image.load(full_path)
            orb_name = os.path.splitext(fname)[0].replace("_", " ")
            orb_name = _reverse_sanitize(orb_name)
            _icon_cache[orb_name] = img
        except Exception:
            pass


def _reverse_sanitize(name):
    reverse_map = {
        "Perfect Orb of Transmutation": "Perfect Orb of Transmutation",
        "Perfect Orb of Augmentation": "Perfect Orb of Augmentation",
        "Perfect Regal Orb": "Perfect Regal Orb",
        "Perfect Chaos Orb": "Perfect Chaos Orb",
        "Perfect Exalted Orb": "Perfect Exalted Orb",
        "Orb of Annulment": "Orb of Annulment",
        "Divine Orb": "Divine Orb",
        "Fracturing Orb": "Fracturing Orb",
        "Omen of Whittling": "Omen of Whittling",
        "Artificers Orb": "Artificer's Orb",
        "Blacksmiths Whetstone": "Blacksmith's Whetstone",
        "Vaal Blacksmiths Infuser": "Vaal Blacksmith's Infuser",
        "Chaos Orb": "Chaos Orb",
        "Exalted Orb": "Exalted Orb",
        "Hinekoras Lock": "Hinekora's Lock",
    }
    return reverse_map.get(name, name)


def set_icon_urls(urls):
    global _icon_urls
    _icon_urls = dict(urls)


def download_icons_async(callback=None):
    def _download():
        global _download_done
        with _download_lock:
            _ensure_assets_dir()
            merged = dict(CDN_FALLBACK_URLS)
            merged.update(_icon_urls)
            downloaded = False
            for orb_name, url in merged.items():
                path = _cache_path(orb_name)
                if os.path.exists(path):
                    continue
                try:
                    req = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            "Referer": "https://poe2db.tw/",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = resp.read()
                    with open(path, "wb") as f:
                        f.write(data)
                    downloaded = True
                except Exception:
                    pass
            if downloaded:
                load_cached_icons()
            _download_done = True
            if callback:
                callback()

    t = threading.Thread(target=_download, daemon=True)
    t.start()
    return t


def get_orb_icon(orb_name, size):
    if orb_name in _icon_cache:
        src = _icon_cache[orb_name]
        sw, sh = src.get_size()
        if sw == size and sh == size:
            return src
        return pygame.transform.smoothscale(src, (size, size))
    return None



