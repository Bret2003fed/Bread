import os
import json

SAVE_FILE = "save_data.json"

class SaveManager:
    @staticmethod
    def save_game(game):
        data = {
            "crumbs": game.crumbs,
            "total_baked": game.total_baked,
            "total_clicks": game.total_clicks,
            "total_crits": game.total_crits,
            "total_prestiges": game.total_prestiges,
            "total_jumpscares": game.total_jumpscares,
            "bought_relics_count": game.bought_relics_count,
            "medals": game.medals,
            "unlocked_artifacts": list(game.unlocked_artifacts),
            "unlocked_achievements": list(game.unlocked_achievements),
            "claimed_achievements": list(game.claimed_achievements),
            "current_location_idx": game.current_location_idx,
            "locations": [
                {
                    "id": loc.id,
                    "unlocked": loc.unlocked,
                    "curse_level": loc.curse_level,
                    "click_power": loc.click_power,
                    "passive_income": loc.passive_income,
                    "decay_reduction": loc.decay_reduction,
                    "upgrades": {k: {"count": v["count"], "cost": v["cost"]} for k, v in loc.upgrades.items()}
                }
                for loc in game.locations
            ],
            "prestige": {
                "relics": game.prestige.relics,
                "total_relics": game.prestige.total_relics,
                "perk_levels": game.prestige.perk_levels
            }
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Помилка збереження: {e}")

    @staticmethod
    def load_game(game):
        if not os.path.exists(SAVE_FILE):
            return False
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            game.crumbs = float(data.get("crumbs", 0.0))
            game.total_baked = float(data.get("total_baked", 0.0))
            game.total_clicks = int(data.get("total_clicks", 0))
            game.total_crits = int(data.get("total_crits", 0))
            game.total_prestiges = int(data.get("total_prestiges", 0))
            game.total_jumpscares = int(data.get("total_jumpscares", 0))
            game.bought_relics_count = int(data.get("bought_relics_count", 0))
            game.medals = int(data.get("medals", 0))
            game.unlocked_artifacts = set(data.get("unlocked_artifacts", []))
            game.unlocked_achievements = set(data.get("unlocked_achievements", []))
            game.claimed_achievements = set(data.get("claimed_achievements", []))
            game.current_location_idx = int(data.get("current_location_idx", 0))

            saved_locs = data.get("locations", [])
            for s_loc in saved_locs:
                for loc in game.locations:
                    if loc.id == s_loc.get("id"):
                        loc.unlocked = s_loc.get("unlocked", loc.unlocked)
                        loc.curse_level = float(s_loc.get("curse_level", 0.0))
                        loc.click_power = float(s_loc.get("click_power", 1.0))
                        loc.passive_income = float(s_loc.get("passive_income", 0.0))
                        loc.decay_reduction = float(s_loc.get("decay_reduction", 0.0))
                        saved_upgs = s_loc.get("upgrades", {})
                        for k, v in saved_upgs.items():
                            if k in loc.upgrades:
                                loc.upgrades[k]["count"] = v.get("count", 0)
                                loc.upgrades[k]["cost"] = v.get("cost", loc.upgrades[k]["cost"])

            saved_prestige = data.get("prestige", {})
            game.prestige.relics = int(saved_prestige.get("relics", 0))
            game.prestige.total_relics = int(saved_prestige.get("total_relics", 0))
            loaded_levels = saved_prestige.get("perk_levels", {})
            for perk_id, lvl in loaded_levels.items():
                if perk_id in game.prestige.perk_levels:
                    game.prestige.perk_levels[perk_id] = int(lvl)

            return True
        except Exception as e:
            print(f"Помилка завантаження: {e}")
            return False

    @staticmethod
    def reset_save(game):
        if os.path.exists(SAVE_FILE):
            try:
                os.remove(SAVE_FILE)
            except Exception:
                pass
        game.prestige.relics = 0
        game.prestige.total_relics = 0
        game.prestige.perk_levels = {k: 0 for k in game.prestige.tree_config}
        game.total_clicks = 0
        game.total_crits = 0
        game.total_prestiges = 0
        game.total_jumpscares = 0
        game.bought_relics_count = 0
        game.medals = 0
        game.unlocked_artifacts = set()
        game.unlocked_achievements = set()
        game.claimed_achievements = set()
        game.reset_standard_run()