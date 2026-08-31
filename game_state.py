import copy
import random
from config import LOCATIONS_DATA, ACHIEVEMENTS_DATA, MEDAL_ARTIFACTS
from prestige_manager import PrestigeManager

class LocationInstance:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.tier = data["tier"]
        self.cost = data["cost"]
        self.unlocked = (data["cost"] == 0)
        self.ambient = data["ambient"]
        self.curse_rate = data["curse_rate"]
        self.income_mult = data["income_mult"]
        self.horror_type = data["horror_type"]
        self.curse_level = 0.0
        self.click_power = 1.0
        self.passive_income = 0.0
        self.decay_reduction = 0.0

        self.upgrades = copy.deepcopy(data["upgrades"])
        for k in self.upgrades:
            self.upgrades[k]["count"] = 0

class GameState:
    def __init__(self):
        self.prestige = PrestigeManager()
        self.locations = [LocationInstance(ld) for ld in LOCATIONS_DATA]
        self.current_location_idx = 0
        self.crumbs = 0.0
        self.total_baked = 0.0
        self.total_clicks = 0
        self.total_crits = 0
        self.total_prestiges = 0
        self.total_jumpscares = 0
        
        self.medals = 0
        self.unlocked_artifacts = set()
        self.unlocked_achievements = set()
        self.claimed_achievements = set()
        self.auto_click_timer = 0.0
        self.reset_standard_run()

    def reset_standard_run(self):
        self.crumbs = self.prestige.get_start_crumbs()
        self.total_baked = self.crumbs
        self.auto_click_timer = 0.0
        self.current_location_idx = 0

        cost_discount = self.prestige.get_cost_multiplier()
        self.locations = [LocationInstance(ld) for ld in LOCATIONS_DATA]
        for loc in self.locations:
            for k in loc.upgrades:
                loc.upgrades[k]["cost"] = max(1, int(loc.upgrades[k]["cost"] * cost_discount))

    @property
    def current_location(self):
        return self.locations[self.current_location_idx]

    @property
    def curse_level(self):
        return self.current_location.curse_level

    def trigger_prestige(self):
        earned = self.prestige.calculate_pending_relics(self.total_baked)
        if earned > 0:
            self.prestige.relics += earned
            self.prestige.total_relics += earned
            self.total_prestiges += 1
            self.reset_standard_run()
            return True
        return False

    def is_upgrade_secret_unlocked(self, secret_req):
        if not secret_req:
            return True
        return self.prestige.get_perk_level(secret_req) >= 1

    def unlock_location(self, loc_idx):
        loc = self.locations[loc_idx]
        if not loc.unlocked and self.crumbs >= loc.cost:
            self.crumbs -= loc.cost
            loc.unlocked = True
            return True
        return False

    def claim_achievement_reward(self, ach_id):
        if ach_id in self.unlocked_achievements and ach_id not in self.claimed_achievements:
            for ach in ACHIEVEMENTS_DATA:
                if ach["id"] == ach_id:
                    self.medals += ach.get("reward_medals", 1)
                    self.claimed_achievements.add(ach_id)
                    return ach
        return None

    def buy_artifact(self, art_key):
        if art_key not in self.unlocked_artifacts and art_key in MEDAL_ARTIFACTS:
            art = MEDAL_ARTIFACTS[art_key]
            if self.medals >= art["cost"]:
                self.medals -= art["cost"]
                self.unlocked_artifacts.add(art_key)
                return True
        return False

    def get_artifact_multiplier(self, effect_type):
        mult = 0.0
        for art_key in self.unlocked_artifacts:
            if art_key in MEDAL_ARTIFACTS:
                art = MEDAL_ARTIFACTS[art_key]
                if art["effect_type"] == effect_type:
                    mult += art["power"]
        return mult

    def get_location_passive(self, loc):
        if not loc.unlocked:
            return 0.0
        global_boost = 1.0 + self.get_artifact_multiplier("global_boost")
        inc = loc.passive_income * loc.income_mult * self.prestige.get_global_multiplier() * global_boost
        inc *= self.prestige.get_passive_multiplier()
        inc *= self.prestige.get_mold_multiplier(loc.curse_level)
        return inc

    def get_total_passive_income(self):
        return sum(self.get_location_passive(loc) for loc in self.locations)

    def calculate_click_value(self):
        loc = self.current_location
        global_boost = 1.0 + self.get_artifact_multiplier("global_boost")
        click_boost = 1.0 + self.get_artifact_multiplier("click_boost")

        power = loc.click_power * loc.income_mult * self.prestige.get_global_multiplier() * global_boost * click_boost
        power *= self.prestige.get_click_multiplier()
        power *= self.prestige.get_mold_multiplier(loc.curse_level)
        power *= self.prestige.get_location_multiplier(self.current_location_idx)

        crit_chance = self.prestige.get_crit_chance() + self.get_artifact_multiplier("crit_boost")
        is_crit = False
        if crit_chance > 0 and random.random() < crit_chance:
            power *= 5.0
            is_crit = True

        relic_dropped = False
        relic_chance = self.prestige.get_relic_drop_chance()
        if relic_chance > 0 and random.random() < relic_chance:
            self.prestige.relics += 1
            self.prestige.total_relics += 1
            relic_dropped = True

        return max(1.0, power), is_crit, relic_dropped

    def manual_click(self):
        self.total_clicks += 1
        power, is_crit, relic_dropped = self.calculate_click_value()
        if is_crit:
            self.total_crits += 1
        self.add_crumbs(power)
        return power, is_crit, relic_dropped

    def get_effective_click_power(self):
        power, _, _ = self.calculate_click_value()
        return power

    def add_crumbs(self, amount):
        self.crumbs += amount
        self.total_baked += amount

    def update_passive(self, dt):
        total_dt_income = 0.0
        for i, loc in enumerate(self.locations):
            if loc.unlocked:
                loc_inc = self.get_location_passive(loc)
                total_dt_income += loc_inc * dt

                if loc.curse_rate > 0:
                    is_active = (i == self.current_location_idx)
                    rate_factor = 1.0 if is_active else 0.60
                    gain = loc.curse_rate * rate_factor
                    artifact_decay_red = self.get_artifact_multiplier("decay_reduce")
                    resist = loc.decay_reduction + (1.0 - self.prestige.get_curse_resist_multiplier()) + artifact_decay_red
                    effective_gain = max(0.0, gain * max(0.05, 1.0 - resist))
                    loc.curse_level = min(100.0, loc.curse_level + effective_gain * dt)

        self.crumbs += total_dt_income
        self.total_baked += total_dt_income

        auto_clicks = self.prestige.get_auto_click_power()
        if auto_clicks > 0:
            self.auto_click_timer += dt
            if self.auto_click_timer >= (1.0 / auto_clicks):
                val, _, _ = self.calculate_click_value()
                self.add_crumbs(val)
                self.auto_click_timer = 0.0

    def check_achievements(self):
        new_unlocked = []
        unlocked_locs_count = sum(1 for loc in self.locations if loc.unlocked)
        max_perks_count = sum(
            1 for k in self.prestige.tree_config
            if self.prestige.get_perk_level(k) > 0 and self.prestige.get_perk_level(k) >= self.prestige.tree_config[k]["max_level"]
        )

        for ach in ACHIEVEMENTS_DATA:
            aid = ach["id"]
            if aid in self.unlocked_achievements:
                continue

            r_type = ach["req_type"]
            r_val = ach["req_val"]

            passed = False
            if r_type == "clicks" and self.total_clicks >= r_val and self.total_clicks > 0:
                passed = True
            elif r_type == "baked" and self.total_baked >= r_val and self.total_baked > 0:
                passed = True
            elif r_type == "crits" and self.total_crits >= r_val and self.total_crits > 0:
                passed = True
            elif r_type == "relics" and self.prestige.total_relics >= r_val and self.prestige.total_relics > 0:
                passed = True
            elif r_type == "prestiges" and self.total_prestiges >= r_val and self.total_prestiges > 0:
                passed = True
            elif r_type == "unlocked_locs" and unlocked_locs_count >= r_val and unlocked_locs_count > 1:
                passed = True
            elif r_type == "jumpscares" and self.total_jumpscares >= r_val and self.total_jumpscares > 0:
                passed = True
            elif r_type == "max_perks_count" and max_perks_count >= r_val and max_perks_count > 0:
                passed = True

            if passed:
                self.unlocked_achievements.add(aid)
                new_unlocked.append(ach)

        return new_unlocked

    def buy_upgrade(self, key):
        loc = self.current_location
        if key in loc.upgrades:
            upg = loc.upgrades[key]
            if not self.is_upgrade_secret_unlocked(upg.get("secret_req")):
                return False
            if self.crumbs >= upg["cost"]:
                self.crumbs -= upg["cost"]
                upg["count"] += 1
                if upg["type"] == "click":
                    loc.click_power += upg["power"]
                elif upg["type"] == "decay_reduce":
                    loc.decay_reduction += upg["power"]
                else:
                    loc.passive_income += upg["power"]
                upg["cost"] = int(upg["cost"] * upg["growth"])
                return True
        return False