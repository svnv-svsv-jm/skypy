"""Constants for Pokemon Legends ZA.

NOTE: These mappings are based on standard Pokemon IDs and need to be verified
against the actual Pokemon Legends ZA game data. The IDs may differ from the
national Pokedex numbers.

To update these mappings:
1. Extract actual IDs from the ZA game files (data.trpfs_complete.json)
2. Cross-reference with external sources (Serebii, Pikalytics)
3. Update the enum values to match the game's internal IDs
"""

from enum import IntEnum


# Pokemon Species IDs for ZA
class POKEMONSPECIES(IntEnum):
    """Pokemon species IDs for Pokemon Legends ZA.

    These IDs are based on standard Pokemon numbering and may need adjustment
    based on the actual game data structure.
    """

    # NOTE: Pikachu is ID 25 based on test data
    Pikachu = 25

    # TODO: Add more Pokemon based on actual ZA game data
    # The game reportedly has 260+ Pokemon starting with Zygarde as #001
    # These IDs need to be extracted from the game files and mapped correctly


# Move IDs for ZA
class MOVES(IntEnum):
    """Move IDs for Pokemon Legends ZA.

    Based on datamine from Kaphotics using PKHeX.Core via the 1.0.1 ExeFS.
    Source: https://pastebin.com/K6xyBaQ5
    """

    # Basic moves
    Fire_Punch = 7
    Ice_Punch = 8
    Thunder_Punch = 9
    Swords_Dance = 14
    Gust = 16
    Wing_Attack = 17
    Whirlwind = 18
    Fly = 19
    Vine_Whip = 22
    Headbutt = 29
    Tackle = 33
    Body_Slam = 34
    Take_Down = 36
    Double_Edge = 38
    Tail_Whip = 39
    Poison_Sting = 40
    Pin_Missile = 42
    Leer = 43
    Bite = 44
    Growl = 45
    Roar = 46
    Supersonic = 48
    Ember = 52
    Flamethrower = 53
    Mist = 54
    Water_Gun = 55
    Hydro_Pump = 56
    Surf = 57
    Ice_Beam = 58
    Blizzard = 59
    Psybeam = 60
    Bubble_Beam = 61
    Hyper_Beam = 63
    Peck = 64
    Absorb = 71
    Leech_Seed = 73
    Growth = 74
    Razor_Leaf = 75
    Solar_Beam = 76
    Poison_Powder = 77
    Stun_Spore = 78
    Sleep_Powder = 79
    String_Shot = 81
    Fire_Spin = 83
    Thunder_Shock = 84
    Thunderbolt = 85
    Thunder_Wave = 86
    Thunder = 87
    Rock_Throw = 88
    Earthquake = 89
    Dig = 91
    Toxic = 92
    Confusion = 93
    Psychic = 94
    Hypnosis = 95
    Quick_Attack = 98
    Teleport = 100
    Screech = 103
    Double_Team = 104
    Recover = 105
    Harden = 106
    Smokescreen = 108
    Confuse_Ray = 109
    Light_Screen = 113
    Haze = 114
    Reflect = 115
    Focus_Energy = 116
    Metronome = 118
    Self_Destruct = 120
    Lick = 122
    Fire_Blast = 126
    Waterfall = 127
    Swift = 129
    Amnesia = 133
    Glare = 137
    Leech_Life = 141
    Splash = 150
    Acid_Armor = 151
    Explosion = 153
    Rock_Slide = 157
    Super_Fang = 162
    Slash = 163
    Substitute = 164
    Flame_Wheel = 172
    Curse = 174
    Protect = 182
    Mach_Punch = 183
    Sludge_Bomb = 188
    Spikes = 191
    Zap_Cannon = 192
    Perish_Song = 195
    Icy_Wind = 196
    Detect = 197
    Outrage = 200
    Giga_Drain = 202
    Endure = 203
    Charm = 204
    Rollout = 205
    Spark = 209
    Steel_Wing = 211
    Safeguard = 219
    Dynamic_Punch = 223
    Megahorn = 224
    Dragon_Breath = 225
    Iron_Tail = 231
    Metal_Claw = 232
    Morning_Sun = 234
    Synthesis = 235
    Moonlight = 236
    Twister = 239
    Crunch = 242
    Extreme_Speed = 245
    Shadow_Ball = 247
    Future_Sight = 248
    Rock_Smash = 249
    Whirlpool = 250
    Heat_Wave = 257
    Will_O_Wisp = 261
    Charge = 268
    Taunt = 269
    Wish = 273
    Brick_Break = 280
    Knock_Off = 282
    Feather_Dance = 297
    Hyper_Voice = 304
    Fake_Tears = 313
    Overheat = 315
    Rock_Tomb = 317
    Metal_Sound = 319
    Sand_Tomb = 328
    Bullet_Seed = 331
    Aerial_Ace = 332
    Iron_Defense = 334
    Dragon_Claw = 337
    Bulk_Up = 339
    Bounce = 340
    Mud_Shot = 341
    Volt_Tackle = 344
    Magical_Leaf = 345
    Calm_Mind = 347
    Leaf_Blade = 348
    Rock_Blast = 350
    Water_Pulse = 352
    U_turn = 369
    Close_Combat = 370
    Heal_Block = 377
    Toxic_Spikes = 390
    Aqua_Ring = 392
    Flare_Blitz = 394
    Aura_Sphere = 396
    Poison_Jab = 398
    Dark_Pulse = 399
    Night_Slash = 400
    Air_Slash = 403
    X_Scissor = 404
    Bug_Buzz = 405
    Dragon_Pulse = 406
    Dragon_Rush = 407
    Power_Gem = 408
    Focus_Blast = 411
    Energy_Ball = 412
    Brave_Bird = 413
    Earth_Power = 414
    Giga_Impact = 416
    Nasty_Plot = 417
    Bullet_Punch = 418
    Ice_Shard = 420
    Shadow_Claw = 421
    Thunder_Fang = 422
    Ice_Fang = 423
    Fire_Fang = 424
    Shadow_Sneak = 425
    Psycho_Cut = 427
    Zen_Headbutt = 428
    Flash_Cannon = 430
    Draco_Meteor = 434
    Discharge = 435
    Lava_Plume = 436
    Leaf_Storm = 437
    Power_Whip = 438
    Gunk_Shot = 441
    Iron_Head = 442
    Stone_Edge = 444
    Stealth_Rock = 446
    Wood_Hammer = 452
    Aqua_Jet = 453
    Head_Smash = 457
    Psyshock = 473
    Sludge_Wave = 482
    Heavy_Slam = 484
    Volt_Switch = 521
    Bulldoze = 523
    Work_Up = 526
    Electroweb = 527
    Wild_Charge = 528
    Drill_Run = 529
    Horn_Leech = 532
    Heat_Crash = 535
    Cotton_Guard = 538
    Psystrike = 540
    Hurricane = 542
    Snarl = 555
    Icicle_Crash = 556
    Flying_Press = 560
    Sticky_Web = 564
    Phantom_Force = 566
    Trick_or_Treat = 567
    Parabolic_Charge = 570
    Forests_Curse = 571
    Freeze_Dry = 573
    Disarming_Voice = 574
    Parting_Shot = 575
    Topsy_Turvy = 576
    Draining_Kiss = 577
    Play_Rough = 583
    Fairy_Wind = 584
    Moonblast = 585
    Boomburst = 586
    Kings_Shield = 588
    Diamond_Storm = 591
    Steam_Eruption = 592
    Hyperspace_Hole = 593
    Water_Shuriken = 594
    Mystical_Fire = 595
    Spiky_Shield = 596
    Eerie_Impulse = 598
    Geomancy = 601
    Dazzling_Gleam = 605
    Nuzzle = 609
    Infestation = 611
    Power_Up_Punch = 612
    Oblivion_Wing = 613
    Thousand_Arrows = 614
    Thousand_Waves = 615
    Lands_Wrath = 616
    Light_of_Ruin = 617
    Hyperspace_Fury = 621
    Leafage = 670
    Lunge = 679
    Core_Enforcer = 687
    Brutal_Swing = 693
    Liquidation = 710
    No_Retreat = 748
    Breaking_Swipe = 784
    Flip_Turn = 812
    Agility = 97


# Item IDs for ZA
class ITEMS(IntEnum):
    """Item IDs for Pokemon Legends ZA.

    These IDs are based on standard item numbering and may need adjustment
    based on the actual game data structure.
    """

    # NOTE: Light_Ball ID is confirmed from test data
    Light_Ball = 104

    # TODO: Add more items based on actual ZA game data
    # Reference: https://www.serebii.net/legendsz-a/items.shtml
    # The game includes Poke Balls, Mega Stones, Mints, Evolution Items,
    # TMs, Training Items, Battle Held Items, Berries, Treasures, Medicines,
    # Fossils, and Key Items


# Export the enums
__all__ = ["POKEMONSPECIES", "MOVES", "ITEMS"]
