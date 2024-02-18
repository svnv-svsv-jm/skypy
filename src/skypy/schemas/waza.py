__all__ = ["WazaData"]

from ._base import BaseSchema


class WazaData(BaseSchema):
    """Waza data."""

    move_id: int
    ca_use_move: bool
    type: str
    quality: int
    category: int
    accuracy: int
    pp: int
    hit_max: int
    hit_min: int
    crit_max: int
    crit_min: int
    recoil: int
    raw_healing: int
    raw_target: int
    affinity: str
    flag_makes_contact: bool
    flag_charge: bool
    flag_rechargeg: bool
    flag_protect: bool
    flag_reflectable: bool
    flag_snatch: bool
    flag_mirror: bool
    flag_punch: bool
    flag_sound: bool
    flag_dance: bool
    flag_gravity: bool
    flag_defrost: bool
    flag_distance_triple: bool
    flag_heal: bool
    flag_ignore_substitute: bool
    flag_fail_sky_battle: bool
    flag_animate_ally: bool
    flag_metronome: bool
    flag_fail_encore: bool
    flag_fail_me_first: bool
    flag_future_attack: bool
    flag_pressure: bool
    flag_combo: bool
    flag_no_sleep_talk: bool
    flag_no_assist: bool
    flag_fail_copy_cat: bool
    flag_fail_mimic: bool
    flag_fail_instruct: bool
    flag_powder: bool
    flag_bite: bool
    flag_bullet: bool
    flag_no_multi_hit: bool
    flag_no_effectiveness: bool
    flag_sheer_force: bool
    flag_slicing: bool
    flag_wind: bool
    unknown56: bool
    unknown57: bool
    unknown58: bool
    unknown59: bool
    unknown60: bool
    unused61: bool
    unused62: bool
    unused63: bool
    unused64: bool
    unused65: bool
    unused66: bool
    unused67: bool
    unused68: bool
    unused69: bool
    unused70: bool
    flag_cant_use_twice: bool
    inflict___value: int
    inflict___change: int
    inflict___turn1: int
    inflict___turn2: int
    inflict___turn3: int
    stat_amps___fstat1: int
    stat_amps___fstat2: int
    stat_amps___fstat3: int
    stat_amps___fstat1_stage: int
    stat_amps___fstat2_stage: int
    stat_amps___fstat3_stage: int
    stat_amps___fstat1_percent: int
    stat_amps___fstat2_percent: int
    stat_amps___fstat3_percent: int