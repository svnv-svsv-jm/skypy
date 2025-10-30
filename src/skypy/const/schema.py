import typing as ty

BallIDs = ty.Literal[
    "NONE",
    "MASUTAABOORU",
    "MONSUTAABOORU",
    "HAIPAABOORU",
    "TAIMAABOORU",
    "RIPIITOBOORU",
    "GOOZYASUBOORU",
    "KUIKKUBOORU",
    "HIIRUBOORU",
    "NESUTOBOORU",
    "HEBIIBOORU",
    "PUREMIABOORU",
]
BALLIDS = ty.get_args(BallIDs)

StatsColumns = ty.Literal[
    "base_stats.HP",
    "base_stats.ATK",
    "base_stats.DEF",
    "base_stats.SPA",
    "base_stats.SPD",
    "base_stats.SPE",
]
STATS_COLUMNS = ty.get_args(StatsColumns)

IntColumns = ty.Literal[
    "type_1",
    "type_2",
    "ability_1",
    "ability_2",
    "ability_hidden",
    "xp_growth",
    "catch_rate",
    "egg_group_1",
    "egg_group_2",
    "egg_hatch_steps",
    "base_friendship",
    "evo_stage",
    "dex.index",
    "dex.group",
    "kitakami_dex",
    "exp_addend",
    "moneyRate",
]
INT_COLUMNS = list(ty.get_args(IntColumns))
