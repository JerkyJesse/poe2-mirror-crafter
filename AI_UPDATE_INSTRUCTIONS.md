# PoE2 Mirror Crafter — AI Update Instructions

This document is for future AI agents (or human maintainers) tasked with updating
this application after a Path of Exile 2 patch. Follow the checklist and per-file
guide below to ensure accuracy.

---

## 1. Pre-Update Checklist — External Data Sources

Before touching any code, check these sources for changes:

| Source | URL | What to Look For |
|--------|-----|------------------|
| **PoE2 Official Patch Notes** | https://www.pathofexile.com/forum/view-forum/patch-notes-poe2 | New currency items, crafting mechanic changes, new item types, tier reworks, ilvl requirement changes |
| **poe2db.tw** | https://poe2db.tw/ | Mod pools per item type, base item variants, ilvl/tier thresholds, new bases, catalyst types, rune types, anointable notables |
| **poe.ninja (PoE2)** | https://poe.ninja/economy/poe2 | Live currency prices — compare against `FALLBACK_PRICES` to verify staleness |

**Always cross-reference patch notes with poe2db** — patch notes say *what* changed;
poe2db shows the *exact data* (mod names, tiers, ilvl requirements).

---

## 2. File-by-File Update Guide

### 2.1 `prices.py` — Currency Prices & Name Mapping

**What to update:**

1. **`FALLBACK_PRICES`** (line 5–55) — Static price dictionary used when poe.ninja API
   is unreachable. These go stale as the league economy matures.

   - Compare each orb's divine value against poe.ninja "Standard" league prices.
   - **Add new entries** for any new currency/omen/catalyst items from patch notes.
   - **Remove entries** for removed/renamed items.
   - Update `"chaos"` and `"divine"` values based on current market rates.

2. **`ORB_NAME_MAP`** (line 68–105) — Maps internal orb names to poe.ninja API names.
   When GGG renames items, update both keys and values here.

   - Search poe.ninja for the new name; map it accordingly.
   - Ensure every orb referenced in any phase step or budget tier exists here.

3. **`_ORB_ATTEMPTS`** in `crafting_app.py` (line 160–189) — Estimated number of
   attempts per orb type used in budget estimation. If crafting mechanics change
   (e.g., Fracturing Orb success rate), update these numbers.

   - Cross-reference with patch notes for mechanic changes.
   - If a new currency is added, add an entry here with a reasonable attempt estimate.

4. **`POE2_CURRENCY_API`** (line 57–60) — If poe.ninja changes their API endpoint
   or league naming convention, update this URL.

**Signals data is stale:**
- Prices in the app look obviously wrong vs. poe.ninja
- A new currency/officially revealed item is referenced in the app but missing from FALLBACK_PRICES
- poe.ninja API returns empty or errors with a permanent status code

---

### 2.2 `phases/base_phases.py` — Universal Crafting Phases

This file defines the 10-phase crafting flow shared by all item types. Most
phase content is generic, but specific orb names and descriptions need review.

**What to update:**

1. **`ORB_COLORS`** (line 1–27) — Add color entries for any new orb/currency types
   that appear in phase steps. Pick RGB values consistent with the existing palette
   (e.g., T1 orbs are gold-ish, omens are darker tones).

2. **`PREMIUM_ORB_NAMES`** (line 29–55) — List of high-value orbs displayed with
   premium styling. Add new high-tier currency here.

3. **`ORB_ICON_FILENAMES`** (line 57–85) — Maps orb names to icon filenames for
   the icon loader. Add entries for new orbs.

4. **Phase descriptions** — Throughout the `build_phases()` function, scan for:
   - References to specific orb names (e.g., "Perfect Chaos Orb") — rename if GGG renamed them.
   - References to ilvl requirements (e.g., "ilvl 82+") — verify against poe2db.
   - References to crafting mechanics (e.g., fracture success rates) — verify against patch notes.
   - References to mod tier counts (e.g., "6x T1") — verify PoE2 didn't change max affixes.

5. **`ORB_COLORS.update()`** (line 90–110) — Extended color entries for
   armour/jewellery-specific currencies. Add new catalysts, emotion types, etc.

**Signals data is stale:**
- Phase instructions mention orb names that don't exist in-game anymore
- ilvl requirements changed in a patch
- Fracture/sanctify mechanics reworked

---

### 2.3 `phases/weapon_phases.py` — Weapon-Specific Data

Each weapon type (Bow, Crossbow, Wand, Sceptre, Staff, Quarterstaff) has a
dictionary with these fields:

| Field | What to Verify | Source |
|-------|---------------|--------|
| `s_tier_keep` | Desirable mods per weapon type | poe2db.tw — browse the weapon's mod pool, note T1-T2 mods |
| `s_tier_trash` | Undesirable mods | poe2db.tw — note low-value or build-irrelevant mods |
| `s_tier_consider` | Situational mods | Community build guides, meta analysis |
| `fracture_priority` | Mods to fracture first (ordered by value) | Trade site, community consensus |
| `regal_omen_note` | Advice on Coronation Omen direction | Depends on prefix/suffix pool distribution |
| `quality_currency` | Which quality currency applies | Patch notes — verify it's still correct for each weapon type |
| `quality_step_desc` | Description on applying quality | Verify the count (usually 20) |
| `phase9_steps` | Finalization steps per weapon type | Verify rune types are still current |
| `alternatives` | Step alternatives (regal, whittling, sanctify) | Verify orb names and costs |

**To update a weapon type:**

1. Go to `https://poe2db.tw/us/{Weapon_Type}` (replace with actual weapon name)
2. Review the modifier pool — update `s_tier_keep`, `s_tier_trash`, `s_tier_consider`
3. Check ilvl requirements for T1 mods — update `regal_omen_note` if prefix/suffix distribution changed
4. Re-order `fracture_priority` based on current market value
5. Update `alternatives` cost estimates if orb prices shifted dramatically

**To add a new weapon type:**

1. Copy an existing weapon entry as a template
2. Fill in all fields from poe2db.tw data
3. Add the key to `WEAPON_SUBTYPE_DATA` at the bottom of the file
4. Update `CATEGORIES["Weapons"]["sub_types"]` in `phases/__init__.py`

**Signals data is stale:**
- New weapon bases added to the game
- Mod pools rebalanced (new prefixes/suffixes added or removed)
- Quality currency changed for a weapon type

---

### 2.4 `phases/armour_phases.py` — Armour-Specific Data

Contains data for: Body Armour (7 variants by attribute), Helmet, Boots, Gloves,
Shield, Focus.

Same verification process as weapons, but pay special attention to:

- **Body armour attribute variants** (STR, DEX, INT, STR/DEX, STR/INT, DEX/INT,
  STR/DEX/INT) — ensure each variant's mod priorities match its attribute strengths.
- **Boots** — Movement Speed is the #1 priority; verify it's still a suffix and
  still T1-T2 desirable.
- **Gloves** — Verify attack mods (flat damage, attack speed) are still glove-exclusive.
- **Shield** — Verify block mod locations (prefix vs suffix).
- **Focus** — Verify spell caster mod pools haven't changed.

**To add a new armour type:**

1. Copy an existing armour entry as a template
2. Fill in all fields from poe2db.tw data
3. Add the key to `ARMOUR_SUBTYPE_DATA` at the bottom of the file
4. Update `CATEGORIES["Armour"]["sub_types"]` in `phases/__init__.py`

---

### 2.5 `phases/jewellery_phases.py` — Jewellery-Specific Data

Contains data for: Ring, Amulet, Belt.

**What to update:**

1. **Catalyst types** — Verify the catalyst list in `_CATALYST_QUALITY_DESC` matches
   poe2db.tw. Add/remove catalyst types if GGG changed them.

2. **Mod priorities per jewellery type** — Ring, Amulet, and Belt have their own
   `s_tier_keep` lists. Verify against poe2db.tw mod pools.

3. **Amulet fracture priorities** — `+Level of all Skill Gems` is the #1 priority;
   verify it's still the rarest/most valuable prefix.

4. **Belt charm slots** — Verify the charm list in `phase9_steps` matches current
   in-game charms.

5. **Distilled Emotions** — If GGG adds new anointable notables or changes the
   anointing system, update `phase9_steps` for Amulet.

---

### 2.6 `phases/__init__.py` — Category Definitions & Budget Tiers

**What to update:**

1. **`CATEGORIES`** (line 93–115) — If new item categories are added (e.g., "Flasks"),
   add a new category entry. Each category needs:
   - `icon` — string identifier
   - `sub_types` — list of subtype keys matching `*_phases.py` data
   - `data` — reference to the subtype data dict
   - `description` — short description
   - `budget_tiers` — orb quantity estimates for budget calculation

2. **Budget tier orb quantities** (`_WEAPON_BUDGET_TIERS`, `_ARMOUR_BUDGET_TIERS`,
   `_JEWELLERY_BUDGET_TIERS`) — Lines 12–91. These estimate how many of each orb
   a mirror-tier craft consumes. Update when:
   - Crafting mechanics change expected attempt counts
   - New orbs replace old ones in the crafting process
   - Community data shows different average attempt counts

3. **`calculate_tier_thresholds()`** (line 118–156) — Uses live prices to compute
   tier costs. No changes needed unless the tier system fundamentally changes.

---

### 2.7 `crafting_app.py` — Application Logic

**What to update:**

1. **`_ORB_ATTEMPTS`** (line 160–189) — Estimated attempts per orb for budget
   calculation. Update if crafting success rates change. Cross-reference with:
   - Community data on average attempts per craft
   - Patch notes for mechanical changes
   - New orbs that need entries

---

### 2.8 `renderer.py` — Visual Rendering

**What to update:**

1. **`icon_chars`** (line 1012–1037) — Fallback text abbreviations for orbs
   when icons fail to load. Add entries for new orb types.

2. **`ORB_COLORS` import** — Already imports from `base_phases.py`, so adding
   colors there covers this file.

---

## 3. Step-by-Step Update Procedure

Run through these steps in order when updating after a patch:

### Step 1: Scan Patch Notes
1. Read the full patch notes at https://www.pathofexile.com/forum/view-forum/patch-notes-poe2
2. Note every:
   - New currency item, omen, catalyst, rune
   - Renamed or removed item
   - Crafting mechanic change
   - New item base type or subtype
   - Tier restructuring or ilvl requirement change
   - Mod pool changes (added/removed mods)

### Step 2: Update Currency Data (`prices.py`)
1. Add/remove entries in `FALLBACK_PRICES`
2. Add/remove entries in `ORB_NAME_MAP`
3. Add new orb colors in `phases/base_phases.py` → `ORB_COLORS`
4. Add new orb icon filenames in `phases/base_phases.py` → `ORB_ICON_FILENAMES`
5. Update `crafting_app.py` → `_ORB_ATTEMPTS`
6. Update `renderer.py` → `icon_chars`

### Step 3: Update Budget Tiers (`phases/__init__.py`)
1. Review orb quantities in all three `_BUDGET_TIERS` dicts
2. Adjust based on any mechanic changes affecting attempt counts
3. Add entries for new orbs used in the crafting pipeline

### Step 4: Update Phase Data (`phases/base_phases.py`)
1. Review all phase descriptions for:
   - Outdated orb names
   - Changed ilvl requirements
   - Changed crafting mechanics (fracture %, sanctify %, etc.)
2. Update `PREMIUM_ORB_NAMES` if premium orb list changed

### Step 5: Update Item-Specific Data
For each item type in `weapon_phases.py`, `armour_phases.py`, `jewellery_phases.py`:

1. Visit `https://poe2db.tw/` and navigate to the item's mod page
2. Verify `s_tier_keep` — add new desirable T1-T2 mods, remove mods that no longer exist
3. Verify `s_tier_trash` — add new trash mods, remove mods that were upgraded
4. Verify `fracture_priority` — re-order based on current market value
5. Verify `alternatives` — update cost estimates if orb prices shifted significantly
6. Verify `phase9_steps` — check rune/catalyst/anoint options still valid

### Step 6: Run the Application
1. `pip install -r requirements.txt` (if not already installed)
2. `python main.py`
3. Verify:
   - App launches without errors
   - Price panel shows "Source: live" (API working)
   - Navigate through a few item types — phase data loads correctly
   - Confirm steps — no missing orb references
   - Budget estimate shows reasonable numbers

---

## 4. Validation Checklist

After completing updates, verify:

- [ ] App starts without import errors or crashes
- [ ] All categories (Weapons, Armour, Jewellery) show their sub-types
- [ ] Selecting a sub-type begins crafting with all 10 phases visible
- [ ] Phase descriptions reference correct orb names (no `KeyError` from `get_price`)
- [ ] Price panel shows live prices for all orbs in a given step
- [ ] Budget running total updates as steps are confirmed
- [ ] Alternatives display correct options and cost estimates
- [ ] Save/load functionality works (saves in `%APPDATA%\poe2-mirror-crafter\saves`)
- [ ] No missing orb icons (fallback text letters appear if icon download failed)

---

## 5. Key External Reference URLs

| Resource | URL |
|----------|-----|
| PoE2 Official Patch Notes | https://www.pathofexile.com/forum/view-forum/patch-notes-poe2 |
| poe2db.tw (mod database) | https://poe2db.tw/ |
| poe.ninja PoE2 Economy | https://poe.ninja/economy/poe2 |
| PoE2 Wiki | https://www.poewiki.net/wiki/Path_of_Exile_2 |

---

## 6. Common Pitfalls

1. **GGG renames items between patches** — e.g., "Omen of Whittling" might become
   "Omen of Sculpting". The `ORB_NAME_MAP` must match the poe.ninja API name exactly.

2. **New leagues change divine:chaos ratios dramatically** — `FALLBACK_PRICES`
   should reflect "Standard" league values for stability. The live API handles
   current league.

3. **poe2db.tw may lag behind patches** — Always cross-reference with official
   patch notes. If poe2db is outdated, use in-game data (ALT-hover on items)
   as the authoritative source.

4. **Budget tier orb quantities are community estimates** — If community consensus
   shifts (e.g., expected Whittling attempts changes from 20 to 15), update the
   `_BUDGET_TIERS` dicts accordingly.

5. **Don't forget the `completed_message` fields** — Each subtype entry has
   a `completed_message` that mentions estimated divine costs. Update these
   when budget estimates change significantly.
