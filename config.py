# Базова віртуальна роздільна здатність
V_WIDTH = 1000
V_HEIGHT = 650
FPS = 60

# Кольори
BG_DEFAULT = (24, 20, 24)
PANEL_BG = (32, 28, 30)
PANEL_BORDER = (60, 50, 55)
TEXT_WHITE = (240, 235, 225)
ACCENT_GOLD = (245, 195, 65)
BUTTON_BG = (48, 40, 44)
BUTTON_HOVER = (75, 60, 65)
BUTTON_DISABLED = (38, 32, 35)

# --- 12 Локацій із хардкорними цінами розблокування ---
LOCATIONS_DATA = [
    # --- TIER 1: Побутові світи ---
    {
        "id": "kitchen",
        "name": "Бабусина кухня",
        "tier": 1,
        "cost": 0,
        "image_file": "assets/backgrounds/kitchen.png",
        "ambient": "Затишна безпечна зона без цвілі",
        "curse_rate": 0.0,
        "income_mult": 1.0,
        "horror_type": "ghost_grandma",
        "fallback_color": (45, 35, 30),
        "upgrades": {
            "sweet_tea": {"name": "Солодкий Чайок", "cost": 15, "growth": 1.15, "power": 0.5, "type": "passive", "desc": "Розмочує сухарики для старту", "secret_req": None},
            "toaster": {"name": "Старий Тостер", "cost": 50, "growth": 1.16, "power": 1.5, "type": "passive", "desc": "Смажить скибки цілодобово", "secret_req": None},
            "butter_knife": {"name": "Ніж з Ринку", "cost": 120, "growth": 1.18, "power": 2.5, "type": "click", "desc": "+2.5 сили кліку", "secret_req": None},
            "mayo": {"name": "Майонез 72%", "cost": 350, "growth": 1.20, "power": 8.0, "type": "passive", "desc": "Змащує економіку кухні", "secret_req": None},
            "secret_recipe": {"name": "Таємна Закваска", "cost": 1500, "growth": 1.25, "power": 55.0, "type": "passive", "desc": "Старовинний секрет прабабусі", "secret_req": "secret_baking_book"},
        }
    },
    {
        "id": "dorm",
        "name": "Студентський Гуртожиток",
        "tier": 1,
        "cost": 25000,
        "image_file": "assets/backgrounds/dorm.png",
        "ambient": "Запах смаженого хліба на спільній плиті",
        "curse_rate": 0.015,
        "income_mult": 1.5,
        "horror_type": "dorm_demon",
        "fallback_color": (35, 30, 25),
        "upgrades": {
            "pan_toast": {"name": "Хліб на Сковорідці", "cost": 1200, "growth": 1.16, "power": 15.0, "type": "passive", "desc": "Швидкий сніданок студента", "secret_req": None},
            "electric_kettle": {"name": "Кип'ятильник у Кружці", "cost": 3500, "growth": 1.18, "power": 45.0, "type": "passive", "desc": "Гріє воду і крихти", "secret_req": None},
            "roommate_share": {"name": "Ділитись із Сусідом", "cost": 8000, "growth": 1.20, "power": 20.0, "type": "click", "desc": "+20 до сили кліку", "secret_req": None},
            "dorm_secret_stash": {"name": "Чайовий Фонд", "cost": 18000, "growth": 1.24, "power": 180.0, "type": "passive", "desc": "Скинулися всім поверхом на хліб", "secret_req": "auto_knead_1"},
        }
    },
    {
        "id": "kiosk",
        "name": "Нічний Кіоск Фортуна",
        "tier": 1,
        "cost": 250000,
        "image_file": "assets/backgrounds/kiosk.png",
        "ambient": "Неонова вітрина та шум нічного міста",
        "curse_rate": 0.025,
        "income_mult": 2.2,
        "horror_type": "neon_stalker",
        "fallback_color": (25, 45, 55),
        "upgrades": {
            "hot_dog_bun": {"name": "Булочка для Хот-дога", "cost": 15000, "growth": 1.18, "power": 80.0, "type": "click", "desc": "+80 сили кліку", "secret_req": None},
            "coffee_machine": {"name": "Автомат з Кавою", "cost": 45000, "growth": 1.20, "power": 400.0, "type": "passive", "desc": "Бадьорить покупців", "secret_req": None},
            "uv_lamp": {"name": "УФ-Лампа", "cost": 90000, "growth": 1.24, "power": 0.10, "type": "decay_reduce", "desc": "-10% росту цвілі", "secret_req": None},
            "kiosk_underground_grill": {"name": "Підпільний Гриль", "cost": 180000, "growth": 1.25, "power": 1500.0, "type": "passive", "desc": "Нічні гарячі буханці без націнки", "secret_req": "bulk_discount"},
        }
    },

    # --- TIER 2: Індустріальні світи ---
    {
        "id": "factory",
        "name": "Хлібозавод №1",
        "tier": 2,
        "cost": 2500000,
        "image_file": "assets/backgrounds/factory.png",
        "ambient": "Конвеєри гудуть на повну потужність",
        "curse_rate": 0.035,
        "income_mult": 3.5,
        "horror_type": "mutant_pigeon",
        "fallback_color": (30, 40, 50),
        "upgrades": {
            "shaurma_bread": {"name": "Шаурма в Батоні", "cost": 150000, "growth": 1.18, "power": 500.0, "type": "click", "desc": "+500 сили кліку", "secret_req": None},
            "pigeon_team": {"name": "Зграя Голубів", "cost": 400000, "growth": 1.20, "power": 3500.0, "type": "passive", "desc": "Приносять зерно на завод", "secret_req": None},
            "samogon_tank": {"name": "Дідовий Бродильник", "cost": 950000, "growth": 1.22, "power": 9500.0, "type": "passive", "desc": "Прискорює заводські печі", "secret_req": None},
            "hyper_conveyor": {"name": "Гіпер-Конвеєр", "cost": 2000000, "growth": 1.26, "power": 30000.0, "type": "passive", "desc": "Автоматизована подача тіста", "secret_req": "hyper_conveyor_tech"},
        }
    },
    {
        "id": "old_mill",
        "name": "Покинутий Млин",
        "tier": 2,
        "cost": 25000000,
        "image_file": "assets/backgrounds/old_mill.png",
        "ambient": "Скрипучі дерев'яні жорна мелють темне борошно",
        "curse_rate": 0.05,
        "income_mult": 5.0,
        "horror_type": "mill_witch",
        "fallback_color": (40, 35, 20),
        "upgrades": {
            "stone_millstone": {"name": "Кам'яні Жорна", "cost": 1500000, "growth": 1.20, "power": 25000.0, "type": "passive", "desc": "Мелють цілодобово", "secret_req": None},
            "wind_catcher": {"name": "Вітряні Лопаті", "cost": 4000000, "growth": 1.22, "power": 75000.0, "type": "passive", "desc": "Сила бурі крутить млин", "secret_req": None},
            "ancient_sieve": {"name": "Древнє Решето", "cost": 9000000, "growth": 1.24, "power": 4500.0, "type": "click", "desc": "+4500 сили кліку", "secret_req": None},
            "spirit_wind_sieve": {"name": "Решето Духів", "cost": 20000000, "growth": 1.26, "power": 250000.0, "type": "passive", "desc": "Просіює борошно крізь простір", "secret_req": "spore_shield"},
        }
    },
    {
        "id": "bunker",
        "name": "Бункер Госрезерву",
        "tier": 2,
        "cost": 250000000,
        "image_file": "assets/backgrounds/bunker.png",
        "ambient": "Гермодвері та нескінченні ящики сухарів",
        "curse_rate": 0.055,
        "income_mult": 7.5,
        "horror_type": "bunker_stalker",
        "fallback_color": (20, 28, 20),
        "upgrades": {
            "mre_crackers": {"name": "Армійські Галети", "cost": 15000000, "growth": 1.20, "power": 200000.0, "type": "passive", "desc": "Зберігаються 50 років", "secret_req": None},
            "sealed_silo": {"name": "Гермо-Сховище", "cost": 45000000, "growth": 1.22, "power": 650000.0, "type": "passive", "desc": "Тонни стратегічного зерна", "secret_req": None},
            "cryo_freeze": {"name": "Кріо-Охолоджувач", "cost": 90000000, "growth": 1.28, "power": 0.15, "type": "decay_reduce", "desc": "-15% росту цвілі в бункері", "secret_req": None},
            "bunker_cold_fusion": {"name": "Бункерний Реактор", "cost": 200000000, "growth": 1.26, "power": 2200000.0, "type": "passive", "desc": "Живить сушарки ядерною енергією", "secret_req": "heritage_flour"},
        }
    },

    # --- TIER 3: Кібер & Космос ---
    {
        "id": "cyber",
        "name": "Кібер-Мегаполіс 2077",
        "tier": 3,
        "cost": 2500000000,
        "image_file": "assets/backgrounds/cyber.png",
        "ambient": "Хмарочоси, неон та нейронне замішування",
        "curse_rate": 0.08,
        "income_mult": 12.0,
        "horror_type": "cyber_glitch_skull",
        "fallback_color": (35, 15, 45),
        "upgrades": {
            "neural_oven": {"name": "Нейро-Піч GPT-Loaf", "cost": 180000000, "growth": 1.24, "power": 2000000.0, "type": "passive", "desc": "AI знає ідеальну температуру", "secret_req": None},
            "cyber_implant": {"name": "Біо-Клікер", "cost": 450000000, "growth": 1.22, "power": 120000.0, "type": "click", "desc": "+120000 сили кліку", "secret_req": None},
            "nanobot_swarm": {"name": "Рій Наноботів", "cost": 950000000, "growth": 1.26, "power": 8500000.0, "type": "passive", "desc": "Збирають батони з атомів", "secret_req": None},
            "neural_dough_matrix": {"name": "Нейромережа Тіста", "cost": 2000000000, "growth": 1.28, "power": 25000000.0, "type": "passive", "desc": "Генеративний дизайн паляниць", "secret_req": "auto_knead_2"},
        }
    },
    {
        "id": "orbital_station",
        "name": "Станція Паляниця-1",
        "tier": 3,
        "cost": 25000000000,
        "image_file": "assets/backgrounds/orbital.png",
        "ambient": "Невагомість і орбітальні печі",
        "curse_rate": 0.10,
        "income_mult": 18.0,
        "horror_type": "zero_g_corpse",
        "fallback_color": (15, 25, 40),
        "upgrades": {
            "zero_g_mixer": {"name": "Міксер Невагомості", "cost": 1500000000, "growth": 1.24, "power": 20000000.0, "type": "passive", "desc": "Тісто ширяє у вакуумі", "secret_req": None},
            "solar_baker": {"name": "Сонячні Дзеркала", "cost": 4500000000, "growth": 1.25, "power": 70000000.0, "type": "passive", "desc": "Випікання енергією сонця", "secret_req": None},
            "orbital_beam": {"name": "Орбітальний Промінь", "cost": 10000000000, "growth": 1.28, "power": 200000000.0, "type": "passive", "desc": "Транслює хліб на Землю", "secret_req": None},
            "gravity_focus_lens": {"name": "Граві-Фокусувач", "cost": 22000000000, "growth": 1.30, "power": 500000000.0, "type": "passive", "desc": "Стискає космічне борошно променем", "secret_req": "cosmic_crust"},
        }
    },
    {
        "id": "cosmic",
        "name": "Космічна Бездня",
        "tier": 3,
        "cost": 250000000000,
        "image_file": "assets/backgrounds/cosmic.png",
        "ambient": "Гравітаційні бублики викривляють простір",
        "curse_rate": 0.14,
        "income_mult": 28.0,
        "horror_type": "cosmic_eye_void",
        "fallback_color": (20, 10, 35),
        "upgrades": {
            "kvas_reactor": {"name": "Квас-Реактор", "cost": 15000000000, "growth": 1.24, "power": 350000000.0, "type": "passive", "desc": "Турбіни на космічному квасі", "secret_req": None},
            "plasma_slicer": {"name": "Плазмовий Різак", "cost": 45000000000, "growth": 1.22, "power": 2500000.0, "type": "click", "desc": "+2.5M сили кліку", "secret_req": None},
            "quantum_dough_machine": {"name": "Квантовий Синхронізатор", "cost": 150000000000, "growth": 1.30, "power": 2500000000.0, "type": "passive", "desc": "Тісто існує у всіх вимірах", "secret_req": "quantum_baking_tech"},
        }
    },

    # --- TIER 4: Елдріч & Потойбіччя ---
    {
        "id": "black_hole",
        "name": "Чорна Хлібна Діра",
        "tier": 4,
        "cost": 2500000000000,
        "image_file": "assets/backgrounds/black_hole.png",
        "ambient": "Горизонт подій затягує крихти у сингулярність",
        "curse_rate": 0.20,
        "income_mult": 45.0,
        "horror_type": "event_horizon_maw",
        "fallback_color": (10, 5, 20),
        "upgrades": {
            "gravity_crust": {"name": "Гравітаційна Скоринка", "cost": 150000000000, "growth": 1.25, "power": 3000000000.0, "type": "passive", "desc": "Стискає енергію в хліб", "secret_req": None},
            "singularity_knife": {"name": "Сингулярний Клинок", "cost": 450000000000, "growth": 1.24, "power": 25000000.0, "type": "click", "desc": "+25M сили кліку", "secret_req": None},
            "dark_matter_oven": {"name": "Піч Темної Матерії", "cost": 1200000000000, "growth": 1.28, "power": 18000000000.0, "type": "passive", "desc": "Пече анти-хліб", "secret_req": None},
            "antimatter_crust_shredder": {"name": "Антиматерійний Шредер", "cost": 2200000000000, "growth": 1.30, "power": 45000000000.0, "type": "passive", "desc": "Розщеплює темну скоринку на чисту міць", "secret_req": "black_hole_dough"},
        }
    },
    {
        "id": "astral_bakery",
        "name": "Астральна Пекарня",
        "tier": 4,
        "cost": 25000000000000,
        "image_file": "assets/backgrounds/astral.png",
        "ambient": "Хлібні духи замішують вічність",
        "curse_rate": 0.28,
        "income_mult": 70.0,
        "horror_type": "astral_phantom",
        "fallback_color": (25, 10, 30),
        "upgrades": {
            "soul_yeast": {"name": "Дріжджі Душ", "cost": 1500000000000, "growth": 1.26, "power": 25000000000.0, "type": "passive", "desc": "Бродіння на духовній енергії", "secret_req": None},
            "ethereal_touch": {"name": "Ефірний Дотик", "cost": 4500000000000, "growth": 1.25, "power": 150000000.0, "type": "click", "desc": "+150M сили кліку", "secret_req": None},
            "infinite_loaf": {"name": "Нескінченна Хлібина", "cost": 12000000000000, "growth": 1.30, "power": 120000000000.0, "type": "passive", "desc": "Ніколи не закінчується", "secret_req": None},
            "astral_alchemy_cauldron": {"name": "Алхімічний Казан", "cost": 22000000000000, "growth": 1.32, "power": 300000000000.0, "type": "passive", "desc": "Варить філософський буханець", "secret_req": "eldritch_touch"},
        }
    },
    {
        "id": "void",
        "name": "Темний Підвал Цвілі",
        "tier": 4,
        "cost": 250000000000000,
        "image_file": "assets/backgrounds/void.png",
        "ambient": "Абсолютна темрява (Екстремальна швидкість цвілі)",
        "curse_rate": 0.40,
        "income_mult": 120.0,
        "horror_type": "eldritch_tentacle_maw",
        "fallback_color": (15, 0, 5),
        "upgrades": {
            "dark_yeast": {"name": "Чорні Дріжджі", "cost": 15000000000000, "growth": 1.30, "power": 200000000000.0, "type": "passive", "desc": "Заборонене бродіння (+цвіль)", "secret_req": None},
            "eldritch_blade": {"name": "Потойбічний Тесак", "cost": 45000000000000, "growth": 1.28, "power": 1000000000.0, "type": "click", "desc": "+1B сили кліку", "secret_req": None},
            "void_synth": {"name": "Синтезатор Безодні", "cost": 120000000000000, "growth": 1.35, "power": 800000000000.0, "type": "passive", "desc": "Матеріалізація чистої пітьми", "secret_req": None},
            "void_maw_core": {"name": "Паща Небуття", "cost": 220000000000000, "growth": 1.35, "power": 2500000000000.0, "type": "passive", "desc": "Цвіль поглинає закони фізики", "secret_req": "mold_resonance"},
        }
    }
]

# --- 24 Хардкорні Досягнення з нагородою в Медалях Пекаря ---
ACHIEVEMENTS_DATA = [
    {"id": "click_100", "name": "Швидкі Пальці", "desc": "Зробити 100 кліків", "req_type": "clicks", "req_val": 100, "reward_medals": 1},
    {"id": "click_1000", "name": "Майстер Кліку", "desc": "Зробити 1 000 кліків", "req_type": "clicks", "req_val": 1000, "reward_medals": 2},
    {"id": "click_5000", "name": "Кулеметний Натиск", "desc": "Зробити 5 000 кліків", "req_type": "clicks", "req_val": 5000, "reward_medals": 5},
    {"id": "click_25000", "name": "Клікер-Сингулярність", "desc": "Зробити 25 000 кліків", "req_type": "clicks", "req_val": 25000, "reward_medals": 10},

    {"id": "baked_50k", "name": "Студентська Випічка", "desc": "Напекти 50 000 крихт", "req_type": "baked", "req_val": 50000, "reward_medals": 1},
    {"id": "baked_2m", "name": "Хлібний Магнат", "desc": "Напекти 2 000 000 крихт", "req_type": "baked", "req_val": 2000000, "reward_medals": 3},
    {"id": "baked_100m", "name": "Індустріальний Гігант", "desc": "Напекти 100 000 000 крихт", "req_type": "baked", "req_val": 100000000, "reward_medals": 6},
    {"id": "baked_10b", "name": "Володар Тіста", "desc": "Напекти 10 000 000 000 крихт", "req_type": "baked", "req_val": 10000000000, "reward_medals": 12},
    {"id": "baked_500b", "name": "Галактичний Батон", "desc": "Напекти 500 000 000 000 крихт", "req_type": "baked", "req_val": 500000000000, "reward_medals": 20},
    {"id": "baked_10t", "name": "Абсолютна Паляниця", "desc": "Напекти 10 000 000 000 000 крихт", "req_type": "baked", "req_val": 10000000000000, "reward_medals": 35},

    {"id": "crit_50", "name": "Хлібний Берсерк", "desc": "Здійснити 50 критичних кліків", "req_type": "crits", "req_val": 50, "reward_medals": 2},
    {"id": "crit_300", "name": "Смертоносна Скоринка", "desc": "Здійснити 300 критичних кліків", "req_type": "crits", "req_val": 300, "reward_medals": 5},
    {"id": "crit_1500", "name": "Караючий Скибкоріз", "desc": "Здійснити 1 500 критичних кліків", "req_type": "crits", "req_val": 1500, "reward_medals": 12},

    {"id": "relic_25", "name": "Колекціонер Сухарів", "desc": "Зібрати 25 Золотих Сухариків", "req_type": "relics", "req_val": 25, "reward_medals": 3},
    {"id": "relic_150", "name": "Скарбниця Пекаря", "desc": "Зібрати 150 Золотих Сухариків", "req_type": "relics", "req_val": 150, "reward_medals": 8},
    {"id": "relic_1000", "name": "Золотий Пантеон", "desc": "Зібрати 1 000 Золотих Сухариків", "req_type": "relics", "req_val": 1000, "reward_medals": 25},
    {"id": "prestige_3", "name": "Сансара Випічки", "desc": "Здійснити 3 переродження", "req_type": "prestiges", "req_val": 3, "reward_medals": 4},
    {"id": "prestige_15", "name": "Вічне Переродження", "desc": "Здійснити 15 перероджень", "req_type": "prestiges", "req_val": 15, "reward_medals": 15},

    {"id": "loc_4", "name": "Мандрівник", "desc": "Розблокувати 4 різні локації", "req_type": "unlocked_locs", "req_val": 4, "reward_medals": 3},
    {"id": "loc_8", "name": "Дослідник Світів", "desc": "Розблокувати 8 локацій", "req_type": "unlocked_locs", "req_val": 8, "reward_medals": 8},
    {"id": "loc_12", "name": "Всесвітній Пекар", "desc": "Розблокувати всі 12 світів", "req_type": "unlocked_locs", "req_val": 12, "reward_medals": 20},

    {"id": "survive_5_screams", "name": "Безстрашний", "desc": "Пережити 5 скримерів від цвілі", "req_type": "jumpscares", "req_val": 5, "reward_medals": 5},
    {"id": "survive_15_screams", "name": "Володар Жаху", "desc": "Пережити 15 скримерів від цвілі", "req_type": "jumpscares", "req_val": 15, "reward_medals": 15},
    {"id": "max_5_perks", "name": "Абсолютний Майстер", "desc": "Прокачати 5 різних перків до максимуму", "req_type": "max_perks_count", "req_val": 5, "reward_medals": 18},
]

# --- 16 Унікальних Артефактів у Скарбниці Медалей ---
MEDAL_ARTIFACTS = {
    # 1. Базовий клік
    "baker_glove": {
        "name": "Рукавичка Пекаря",
        "cost": 5,
        "desc": "+50% сили базового кліку назавжди",
        "effect_type": "click_boost",
        "power": 0.50
    },
    "diamond_whisk": {
        "name": "Діамантовий Вінчик",
        "cost": 20,
        "desc": "+100% сили кліку додатково",
        "effect_type": "click_boost",
        "power": 1.00
    },
    "titanium_rolling_pin": {
        "name": "Титанова Скалка",
        "cost": 45,
        "desc": "+250% сили кліку на всіх локаціях",
        "effect_type": "click_boost",
        "power": 2.50
    },

    # 2. Критичні кліки
    "holy_recipe": {
        "name": "Священний Рецепт",
        "cost": 15,
        "desc": "+10% до шансу критичного кліку",
        "effect_type": "crit_boost",
        "power": 0.10
    },
    "berserk_blade": {
        "name": "Лезо Берсерка",
        "cost": 35,
        "desc": "Критичний множник збільшується з x5 до x10",
        "effect_type": "crit_mult_boost",
        "power": 5.0
    },
    "singularity_cleaver": {
        "name": "Сингулярний Секач",
        "cost": 75,
        "desc": "Критичний множник зростає ще на +10x (до x20!)",
        "effect_type": "crit_mult_boost",
        "power": 10.0
    },

    # 3. Глобальний дохід
    "golden_spike": {
        "name": "Золотий Колосок",
        "cost": 10,
        "desc": "+20% до глобального видобутку на всіх світах",
        "effect_type": "global_boost",
        "power": 0.20
    },
    "cosmic_yeast": {
        "name": "Зоряна Закваска",
        "cost": 30,
        "desc": "+40% до загального пасивного доходу",
        "effect_type": "global_boost",
        "power": 0.40
    },
    "eternal_dough_core": {
        "name": "Ядро Вічного Тіста",
        "cost": 60,
        "desc": "+80% до всього видобутку між забігами",
        "effect_type": "global_boost",
        "power": 0.80
    },
    "philosopher_flour": {
        "name": "Борошно Безсмертя",
        "cost": 120,
        "desc": "Подвоює глобальний видобуток (+100% дохід)",
        "effect_type": "global_boost",
        "power": 1.00
    },

    # 4. Захист від цвілі
    "thermo_chamber": {
        "name": "Термо-Сховище",
        "cost": 15,
        "desc": "-15% до швидкості наростання цвілі",
        "effect_type": "decay_reduce",
        "power": 0.15
    },
    "mold_repeller": {
        "name": "Ультразвуковий Відлякувач",
        "cost": 40,
        "desc": "-20% до швидкості поширення цвілі",
        "effect_type": "decay_reduce",
        "power": 0.20
    },
    "aegis_sterilizer": {
        "name": "Стерилізатор Егіда",
        "cost": 70,
        "desc": "-30% до швидкості цвілі на всіх відкритих світах",
        "effect_type": "decay_reduce",
        "power": 0.30
    },

    # 5. Економіка, Сухарики та Старт
    "merchant_ledger": {
        "name": "Гільдійська Книга",
        "cost": 25,
        "desc": "-15% знижка на купівлю всіх споруд у магазині",
        "effect_type": "building_discount",
        "power": 0.15
    },
    "relic_magnet": {
        "name": "Сухарний Магніт",
        "cost": 50,
        "desc": "+1% шанс отримати Золотий Сухарик при кожному кліку",
        "effect_type": "relic_chance_boost",
        "power": 0.01
    },
    "ancestral_treasury": {
        "name": "Скарбниця Предків",
        "cost": 85,
        "desc": "+25 000 стартових крихт після кожного переродження",
        "effect_type": "start_crumbs_boost",
        "power": 25000
    }
}

# --- Дерево Престижу ---
PRESTIGE_REQ_CRUMBS = 50000

PRESTIGE_TREE_DATA = {
    # 0. ЦЕНТР
    "core_seed": {
        "id": "core_seed",
        "name": "Первородне Зерно",
        "branch": "Ядро",
        "desc": "+25% до видобутку на всіх локаціях за кожен рівень.",
        "base_cost": 1,
        "cost_growth": 2.0,
        "max_level": 5,
        "reqs": [],
        "rel_pos": (0, 0),
        "effect_type": "global_mult",
        "power_per_level": 0.25,
    },

    # 1. ЗАХІД: Автоматизація
    "auto_knead_1": {
        "id": "auto_knead_1",
        "name": "Фантомне Тісто",
        "branch": "Автоматизація",
        "desc": "+3 автокліки/сек (Відкриває Чайовий Фонд у Гуртожитку).",
        "base_cost": 2,
        "cost_growth": 2.2,
        "max_level": 4,
        "reqs": ["core_seed"],
        "rel_pos": (-260, 0),
        "effect_type": "auto_clicker",
        "power_per_level": 3,
    },
    "auto_knead_2": {
        "id": "auto_knead_2",
        "name": "Сингулярність",
        "branch": "Автоматизація",
        "desc": "+15% пасиву (Відкриває Нейроматрицю в Кіберпанку).",
        "base_cost": 6,
        "cost_growth": 2.5,
        "max_level": 3,
        "reqs": ["auto_knead_1"],
        "rel_pos": (-520, 0),
        "effect_type": "passive_mult",
        "power_per_level": 0.15,
    },
    "crit_slicer": {
        "id": "crit_slicer",
        "name": "Критичний Ніж",
        "branch": "Автоматизація",
        "desc": "+10% шанс на критичний клік (x5 крихт) за рівень.",
        "base_cost": 4,
        "cost_growth": 2.2,
        "max_level": 4,
        "reqs": ["auto_knead_1"],
        "rel_pos": (-260, -170),
        "effect_type": "crit_chance",
        "power_per_level": 0.10,
    },
    "combo_clicker": {
        "id": "combo_clicker",
        "name": "Турбо-Комбо",
        "branch": "Автоматизація",
        "desc": "+25% до сили кліку за рівень.",
        "base_cost": 8,
        "cost_growth": 2.4,
        "max_level": 3,
        "reqs": ["crit_slicer"],
        "rel_pos": (-520, -170),
        "effect_type": "click_mult",
        "power_per_level": 0.25,
    },
    "hyper_conveyor_tech": {
        "id": "hyper_conveyor_tech",
        "name": "Гіпер-Конвеєри",
        "branch": "Автоматизація",
        "desc": "Відкриває секретну споруду 'Гіпер-Конвеєр' на Хлібозаводі.",
        "base_cost": 10,
        "cost_growth": 1.0,
        "max_level": 1,
        "reqs": ["auto_knead_2"],
        "rel_pos": (-760, 0),
        "effect_type": "unlock_secret",
        "power_per_level": 1.0,
    },

    # 2. СХІД: Окультизм
    "mold_affinity": {
        "id": "mold_affinity",
        "name": "Симбіоз з Цвіллю",
        "branch": "Окультизм",
        "desc": "Рівень Цвілі збільшує дохід (+0.5x множник за рівень).",
        "base_cost": 3,
        "cost_growth": 2.2,
        "max_level": 4,
        "reqs": ["core_seed"],
        "rel_pos": (260, 0),
        "effect_type": "mold_power",
        "power_per_level": 0.5,
    },
    "eldritch_touch": {
        "id": "eldritch_touch",
        "name": "Око Паляниці",
        "branch": "Окультизм",
        "desc": "+1.5x до кліку в темряві (Відкриває Казан в Астралі).",
        "base_cost": 7,
        "cost_growth": 2.5,
        "max_level": 3,
        "reqs": ["mold_affinity"],
        "rel_pos": (520, 0),
        "effect_type": "void_buff",
        "power_per_level": 1.5,
    },
    "mold_resonance": {
        "id": "mold_resonance",
        "name": "Цвілевий Резонанс",
        "branch": "Окультизм",
        "desc": "+20% пасиву від цвілі (Відкриває Пащу Небуття в Підвалі).",
        "base_cost": 5,
        "cost_growth": 2.3,
        "max_level": 3,
        "reqs": ["mold_affinity"],
        "rel_pos": (260, 170),
        "effect_type": "passive_mult",
        "power_per_level": 0.20,
    },
    "spore_shield": {
        "id": "spore_shield",
        "name": "Споровий Щит",
        "branch": "Окультизм",
        "desc": "-25% росту Цвілі (Відкриває Решето Духів на Млині).",
        "base_cost": 8,
        "cost_growth": 2.5,
        "max_level": 3,
        "reqs": ["mold_resonance"],
        "rel_pos": (520, 170),
        "effect_type": "curse_resist",
        "power_per_level": 0.25,
    },
    "secret_baking_book": {
        "id": "secret_baking_book",
        "name": "Книга Закваски",
        "branch": "Окультизм",
        "desc": "Відкриває секретну будівлю 'Таємна Закваска' на Кухні.",
        "base_cost": 12,
        "cost_growth": 1.0,
        "max_level": 1,
        "reqs": ["spore_shield"],
        "rel_pos": (760, 170),
        "effect_type": "unlock_secret",
        "power_per_level": 1.0,
    },

    # 3. ПІВНІЧ: Космос
    "cosmic_crust": {
        "id": "cosmic_crust",
        "name": "Квантова Скоринка",
        "branch": "Космос",
        "desc": "Видобуток x1.4 (Відкриває Граві-Фокусувач на Станції).",
        "base_cost": 4,
        "cost_growth": 2.4,
        "max_level": 4,
        "reqs": ["core_seed"],
        "rel_pos": (0, -170),
        "effect_type": "global_mult",
        "power_per_level": 0.40,
    },
    "infinite_gravity": {
        "id": "infinite_gravity",
        "name": "Бублик Простору",
        "branch": "Космос",
        "desc": "Подвоює силу базового кліку (x2 за рівень).",
        "base_cost": 10,
        "cost_growth": 3.0,
        "max_level": 3,
        "reqs": ["cosmic_crust"],
        "rel_pos": (0, -340),
        "effect_type": "click_mult",
        "power_per_level": 1.0,
    },
    "antimatter_yeast": {
        "id": "antimatter_yeast",
        "name": "Антиматерія Дріжджів",
        "branch": "Космос",
        "desc": "+50% до пасиву космічних і кібер-будівель за рівень.",
        "base_cost": 15,
        "cost_growth": 2.8,
        "max_level": 3,
        "reqs": ["cosmic_crust"],
        "rel_pos": (260, -170),
        "effect_type": "passive_mult",
        "power_per_level": 0.50,
    },
    "black_hole_dough": {
        "id": "black_hole_dough",
        "name": "Чорна Діра Тіста",
        "branch": "Космос",
        "desc": "Весь видобуток x3.0 (Відкриває Шредер у Чорній Дірі).",
        "base_cost": 30,
        "cost_growth": 3.5,
        "max_level": 2,
        "reqs": ["infinite_gravity", "antimatter_yeast"],
        "rel_pos": (260, -340),
        "effect_type": "global_mult",
        "power_per_level": 2.0,
    },
    "quantum_baking_tech": {
        "id": "quantum_baking_tech",
        "name": "Квантове Тісто",
        "branch": "Космос",
        "desc": "Відкриває секретну будівлю 'Квантовий Синхронізатор' у Космосі.",
        "base_cost": 25,
        "cost_growth": 1.0,
        "max_level": 1,
        "reqs": ["black_hole_dough"],
        "rel_pos": (0, -510),
        "effect_type": "unlock_secret",
        "power_per_level": 1.0,
    },

    # 4. ПІВДЕНЬ: Економіка
    "bulk_discount": {
        "id": "bulk_discount",
        "name": "Оптові Договори",
        "branch": "Економіка",
        "desc": "-10% ціни будівель (Відкриває Гриль у Кіоску).",
        "base_cost": 3,
        "cost_growth": 2.0,
        "max_level": 4,
        "reqs": ["core_seed"],
        "rel_pos": (0, 170),
        "effect_type": "cost_discount",
        "power_per_level": 0.10,
    },
    "heritage_flour": {
        "id": "heritage_flour",
        "name": "Спадок Пекаря",
        "branch": "Економіка",
        "desc": "+1000 стартових крихт (Відкриває Реактор у Бункері).",
        "base_cost": 5,
        "cost_growth": 2.0,
        "max_level": 5,
        "reqs": ["bulk_discount"],
        "rel_pos": (0, 340),
        "effect_type": "start_crumbs",
        "power_per_level": 1000,
    },
    "night_snack": {
        "id": "night_snack",
        "name": "Нічний Перекус",
        "branch": "Економіка",
        "desc": "+30% до сили кліку та пасиву назавжди за рівень.",
        "base_cost": 8,
        "cost_growth": 2.2,
        "max_level": 3,
        "reqs": ["bulk_discount"],
        "rel_pos": (-260, 170),
        "effect_type": "global_mult",
        "power_per_level": 0.30,
    },
    "golden_crunch": {
        "id": "golden_crunch",
        "name": "Золотий Хрускіт",
        "branch": "Економіка",
        "desc": "0.5% шанс при кліку вибити +1 Золотий Сухарик!",
        "base_cost": 14,
        "cost_growth": 2.6,
        "max_level": 3,
        "reqs": ["night_snack"],
        "rel_pos": (-260, 340),
        "effect_type": "relic_drop",
        "power_per_level": 0.005,
    },
    "magnetic_toast": {
        "id": "magnetic_toast",
        "name": "Магнітний Сухарик",
        "branch": "Економіка",
        "desc": "+25% до кількості отриманих Сухариків при ресеті.",
        "base_cost": 22,
        "cost_growth": 2.8,
        "max_level": 3,
        "reqs": ["golden_crunch"],
        "rel_pos": (-260, 510),
        "effect_type": "relic_mult",
        "power_per_level": 0.25,
    },
}