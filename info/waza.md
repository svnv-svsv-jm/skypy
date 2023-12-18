# Information about moves

See [this file](./src/skypy/const/waza.py).

## Stat changes

Let's check Close Combat's data (notice `370` is the move's ID):

```json
 'move_id': {370: 'WAZA_INFAITO'},
 'can_use_move': {370: True},
 'type': {370: 'Fighting'},
 'quality': {370: 7},
 'category': {370: 1},
 'power': {370: 120},
 'accuracy': {370: 100},
 'pp': {370: 5},
 'priority': {370: 0},
 'hit_max': {370: 0},
 'hit_min': {370: 0},
 'crit_stage': {370: 0},
 'flinch': {370: 0},
 'effect_sequence': {370: 229},
 'recoil': {370: 0},
 'raw_healing': {370: 0},
 'raw_target': {370: 0}, // one opponent
 'affinity': {370: 'Attack'},
 'flag_makes_contact': {370: True},
 'flag_charge': {370: False},
 'flag_rechargeg': {370: False},
 'flag_protect': {370: True},
 'flag_reflectable': {370: False},
 'flag_snatch': {370: False},
 'flag_mirror': {370: True},
 'flag_punch': {370: False},
 'flag_sound': {370: False},
 'flag_dance': {370: False},
 'flag_gravity': {370: False},
 'flag_defrost': {370: False},
 'flag_distance_triple': {370: False},
 'flag_heal': {370: False},
 'flag_ignore_substitute': {370: False},
 'flag_fail_sky_battle': {370: False},
 'flag_animate_ally': {370: False},
 'flag_metronome': {370: True},
 'flag_fail_encore': {370: False},
 'flag_fail_me_first': {370: False},
 'flag_future_attack': {370: False},
 'flag_pressure': {370: False},
 'flag_combo': {370: False},
 'flag_no_sleep_talk': {370: False},
 'flag_no_assist': {370: False},
 'flag_fail_copy_cat': {370: False},
 'flag_fail_mimic': {370: False},
 'flag_fail_instruct': {370: False},
 'flag_powder': {370: False},
 'flag_bite': {370: False},
 'flag_bullet': {370: False},
 'flag_no_multi_hit': {370: False},
 'flag_no_effectiveness': {370: False},
 'flag_sheer_force': {370: False},
 'flag_slicing': {370: False},
 'flag_wind': {370: False},
 'unknown56': {370: False},
 'unknown57': {370: False},
 'unknown58': {370: False},
 'unknown59': {370: False},
 'unknown60': {370: False},
 'unused61': {370: False},
 'unused62': {370: False},
 'unused63': {370: False},
 'unused64': {370: False},
 'unused65': {370: False},
 'unused66': {370: False},
 'unused67': {370: False},
 'unused68': {370: False},
 'unused69': {370: False},
 'unused70': {370: False},
 'flag_cant_use_twice': {370: False},
 'inflict.value': {370: 0},
 'inflict.chance': {370: 0},
 'inflict.turn1': {370: 0},
 'inflict.turn2': {370: 0},
 'inflict.turn3': {370: 0},
 'stat_amps.fstat1': {370: 2},
 'stat_amps.fstat2': {370: -1},
 'stat_amps.fstat3': {370: 100},
 'stat_amps.fstat1_stage': {370: 4},
 'stat_amps.fstat2_state': {370: -1},
 'stat_amps.fstat3_stage': {370: 100},
 'stat_amps.fstat1_percent': {370: 0},
 'stat_amps.fstat2_percent': {370: 0},
 'stat_amps.fstat3_percent': {370: 0},
 'name': {370: 'close combat'}
```

The `stat_amps.fstat*` is the data for the first of three possible stat changes:

```json
'stat_amps.fstat1': {370: 2}, // 2: defense
'stat_amps.fstat2': {370: -1}, // drop by one stage
'stat_amps.fstat3': {370: 100}, // 100% chance of this
'stat_amps.fstat1_stage': {370: 4}, // 4: sp. defense
'stat_amps.fstat2_state': {370: -1}, // drop by one stage
'stat_amps.fstat3_stage': {370: 100}, // 100% chance of this
```

## Status condition

Let's check out Toxic, move ID `92`:

```json
'inflict.value': {92: 5}, // inflicts the Poison status condition
'inflict.chance': {92: 0}, // always
'inflict.turn1': {92: 1}, // unknown
'inflict.turn2': {92: 15}, // value 15 found only in Toxic, Poison Fang and Malignant Chain
'inflict.turn3': {92: 15}, // thus, this value must indicate the Toxic variation for the Poison status
```
