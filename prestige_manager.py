import math
import copy
from config import PRESTIGE_TREE_DATA, PRESTIGE_REQ_CRUMBS

class PrestigeManager:
    def __init__(self):
        self.relics = 0
        self.total_relics = 0
        self.perk_levels = {k: 0 for k in PRESTIGE_TREE_DATA}
        self.tree_config = copy.deepcopy(PRESTIGE_TREE_DATA)

    def calculate_pending_relics(self, total_baked):
        if total_baked < PRESTIGE_REQ_CRUMBS:
            return 0
        base_relics = int(math.sqrt(total_baked / PRESTIGE_REQ_CRUMBS))
        lvl_mag = self.get_perk_level("magnetic_toast")
        if lvl_mag > 0:
            base_relics = int(base_relics * (1.0 + self.tree_config["magnetic_toast"]["power_per_level"] * lvl_mag))
        return base_relics

    def get_perk_level(self, perk_id):
        return self.perk_levels.get(perk_id, 0)

    def is_perk_visible(self, perk_id):
        perk = self.tree_config[perk_id]
        if not perk["reqs"]:
            return True
        return all(self.get_perk_level(req) >= 1 for req in perk["reqs"])

    def get_perk_cost(self, perk_id):
        lvl = self.get_perk_level(perk_id)
        perk = self.tree_config[perk_id]
        if lvl >= perk["max_level"]:
            return 0
        return int(perk["base_cost"] * (perk["cost_growth"] ** lvl))

    def can_buy_perk(self, perk_id):
        perk = self.tree_config[perk_id]
        lvl = self.get_perk_level(perk_id)
        if lvl >= perk["max_level"]:
            return False
        if self.relics < self.get_perk_cost(perk_id):
            return False
        for req in perk["reqs"]:
            if self.get_perk_level(req) < 1:
                return False
        return True

    def unlock_perk(self, perk_id):
        if self.can_buy_perk(perk_id):
            cost = self.get_perk_cost(perk_id)
            self.relics -= cost
            self.perk_levels[perk_id] = self.perk_levels.get(perk_id, 0) + 1
            return True
        return False

    def get_global_multiplier(self):
        mult = 1.0
        lvl_seed = self.get_perk_level("core_seed")
        if lvl_seed > 0:
            mult += self.tree_config["core_seed"]["power_per_level"] * lvl_seed

        lvl_cosmic = self.get_perk_level("cosmic_crust")
        if lvl_cosmic > 0:
            mult += self.tree_config["cosmic_crust"]["power_per_level"] * lvl_cosmic

        lvl_blackhole = self.get_perk_level("black_hole_dough")
        if lvl_blackhole > 0:
            mult += self.tree_config["black_hole_dough"]["power_per_level"] * lvl_blackhole

        lvl_quantum = self.get_perk_level("quantum_loaf")
        if lvl_quantum > 0:
            mult += self.tree_config["quantum_loaf"]["power_per_level"] * lvl_quantum

        lvl_snack = self.get_perk_level("night_snack")
        if lvl_snack > 0:
            mult += self.tree_config["night_snack"]["power_per_level"] * lvl_snack

        return mult

    def get_click_multiplier(self):
        mult = 1.0
        lvl = self.get_perk_level("infinite_gravity")
        if lvl > 0:
            mult += self.tree_config["infinite_gravity"]["power_per_level"] * lvl

        lvl_combo = self.get_perk_level("combo_clicker")
        if lvl_combo > 0:
            mult += self.tree_config["combo_clicker"]["power_per_level"] * lvl_combo

        return mult

    def get_crit_chance(self):
        lvl = self.get_perk_level("crit_slicer")
        if lvl > 0:
            return self.tree_config["crit_slicer"]["power_per_level"] * lvl
        return 0.0

    def get_relic_drop_chance(self):
        lvl = self.get_perk_level("golden_crunch")
        if lvl > 0:
            return self.tree_config["golden_crunch"]["power_per_level"] * lvl
        return 0.0

    def get_curse_resist_multiplier(self):
        resist = 0.0
        lvl_shield = self.get_perk_level("spore_shield")
        if lvl_shield > 0:
            resist += self.tree_config["spore_shield"]["power_per_level"] * lvl_shield

        lvl_beam = self.get_perk_level("bactericidal_beam")
        if lvl_beam > 0:
            resist += self.tree_config["bactericidal_beam"]["power_per_level"] * lvl_beam

        return max(0.15, 1.0 - resist)

    def get_passive_multiplier(self):
        mult = 1.0
        lvl_sing = self.get_perk_level("auto_knead_2")
        if lvl_sing > 0:
            mult += self.tree_config["auto_knead_2"]["power_per_level"] * lvl_sing

        lvl_res = self.get_perk_level("mold_resonance")
        if lvl_res > 0:
            mult += self.tree_config["mold_resonance"]["power_per_level"] * lvl_res

        lvl_antimatter = self.get_perk_level("antimatter_yeast")
        if lvl_antimatter > 0:
            mult += self.tree_config["antimatter_yeast"]["power_per_level"] * lvl_antimatter

        lvl_teleport = self.get_perk_level("realm_teleport")
        if lvl_teleport > 0:
            mult += self.tree_config["realm_teleport"]["power_per_level"] * lvl_teleport

        return mult

    def get_cost_multiplier(self):
        lvl = self.get_perk_level("bulk_discount")
        if lvl > 0:
            discount = self.tree_config["bulk_discount"]["power_per_level"] * lvl
            return max(0.15, 1.0 - discount)
        return 1.0

    def get_auto_click_power(self):
        lvl = self.get_perk_level("auto_knead_1")
        if lvl > 0:
            return self.tree_config["auto_knead_1"]["power_per_level"] * lvl
        return 0

    def get_start_crumbs(self):
        lvl = self.get_perk_level("heritage_flour")
        if lvl > 0:
            return self.tree_config["heritage_flour"]["power_per_level"] * lvl
        return 0.0

    def get_mold_multiplier(self, curse_level):
        lvl = self.get_perk_level("mold_affinity")
        if lvl > 0:
            power = self.tree_config["mold_affinity"]["power_per_level"] * lvl
            return 1.0 + (curse_level / 100.0) * power
        return 1.0

    def get_location_multiplier(self, loc_idx):
        lvl = self.get_perk_level("eldritch_touch")
        if lvl > 0 and loc_idx >= 3:
            return 1.0 + (self.tree_config["eldritch_touch"]["power_per_level"] * lvl)
        return 1.0