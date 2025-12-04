import random
from unittest.mock import patch

import pytest

from skypy import settings
from skypy.schemas import ZAPokemonData, ZAWazaData
from skypy.za import ZATrainerEditor


def _validate_pkmns(
    app: ZATrainerEditor,
    pkmn_index: int,
    pokemon: ZAPokemonData,
) -> None:
    """Validate the pokemon data in the trainer frame."""
    assert (
        app.trainer_frame.pokemon_fields[pkmn_index].dev_id_field.option_menu.get()
        == pokemon.dev_id_english
    )
    assert (
        app.trainer_frame.pokemon_fields[pkmn_index].item_field.option_menu.get()
        == pokemon.item_english
    )
    assert app.trainer_frame.pokemon_fields[pkmn_index].level_field.var.get() == str(
        pokemon.level
    )
    assert app.trainer_frame.pokemon_fields[pkmn_index].form_id_field.var.get() == str(
        pokemon.form_id
    )
    assert app.trainer_frame.pokemon_fields[
        pkmn_index
    ].sex_field.option_menu.get() == str(pokemon.sex)
    assert (
        app.trainer_frame.pokemon_fields[pkmn_index].ball_id_field.option_menu.get()
        == pokemon.ball_id_english
    )
    assert app.trainer_frame.pokemon_fields[
        pkmn_index
    ].scale_value_field.var.get() == str(pokemon.scale_value)
    for waza_frame, waza in zip(
        app.trainer_frame.pokemon_fields[pkmn_index].waza_frames,
        (
            pokemon.waza_1,
            pokemon.waza_2,
            pokemon.waza_3,
            pokemon.waza_4,
        ),
    ):
        assert waza_frame.option_menu.get() == waza.waza_id_english
        assert waza_frame.plus_checkbox.get() == waza.is_plus_waza


def _create_random_pokemon_data() -> ZAPokemonData:
    return ZAPokemonData(
        dev_id=random.randint(0, 20),
        form_id=random.randint(0, 3),
        sex=random.choice([0, 1, 2]),
        item=random.randint(0, 20),
        level=random.randint(0, 100),
        ball_id=random.choice(list(settings.za_ball_mappings.values())),
        waza_1=ZAWazaData(waza_id=random.randint(0, 20)),
        waza_2=ZAWazaData(waza_id=random.randint(0, 20)),
        waza_3=ZAWazaData(waza_id=random.randint(0, 20)),
        waza_4=ZAWazaData(waza_id=random.randint(0, 20)),
    )


@pytest.mark.parametrize("trainer_id", [1])
def test_on_trainer_selected(
    za_trainer_editor_app: ZATrainerEditor,
    trainer_id: int,
) -> None:
    """Test `on_trainer_selected` calls `TrainerFrame.update_trainer_data`."""
    app = za_trainer_editor_app
    with patch.object(
        type(app.trainer_frame),
        "update_trainer_data",
    ) as update_trainer_data:
        app.on_trainer_selected(app.trdata.values[0].tr_id)
        update_trainer_data.assert_called()

    """Test `on_trainer_selected` raises `ValueError` if trainer not found."""
    with pytest.raises(ValueError):
        app.on_trainer_selected("invalid_trainer")

    """Test `on_trainer_selected` updates the trainer frame."""
    # Edit to random values
    app.trdata.values[trainer_id].money_rate = random.randint(0, 20)
    app.trdata.values[trainer_id].view_horizontal_angle = random.uniform(-180, 180)
    app.trdata.values[trainer_id].view_vertical_angle = random.uniform(-180, 180)
    app.trdata.values[trainer_id].view_range = random.uniform(0, 100)
    app.trdata.values[trainer_id].hearing_range = random.uniform(0, 100)
    app.trdata.values[trainer_id].poke_1 = _create_random_pokemon_data()
    app.trdata.values[trainer_id].poke_2 = _create_random_pokemon_data()
    app.trdata.values[trainer_id].poke_3 = _create_random_pokemon_data()
    app.trdata.values[trainer_id].poke_4 = _create_random_pokemon_data()
    app.trdata.values[trainer_id].poke_5 = _create_random_pokemon_data()
    app.trdata.values[trainer_id].poke_6 = _create_random_pokemon_data()
    app.trdata.values[trainer_id].meg_evolution = random.choice([True, False])
    app.trdata.values[trainer_id].last_hand = random.choice([True, False])
    app.trdata.values[trainer_id].ai_basic = random.choice([True, False])
    app.trdata.values[trainer_id].ai_high = random.choice([True, False])
    app.trdata.values[trainer_id].ai_expert = random.choice([True, False])
    app.trdata.values[trainer_id].ai_double = random.choice([True, False])
    app.trdata.values[trainer_id].ai_raid = random.choice([True, False])
    app.trdata.values[trainer_id].ai_weak = random.choice([True, False])
    app.trdata.values[trainer_id].ai_item = random.choice([True, False])
    app.trdata.values[trainer_id].ai_change = random.choice([True, False])
    # Call
    app.on_trainer_selected(app.trdata.values[trainer_id].tr_id)
    assert (
        app.trainer_frame.trainer_id_field.var.get()
        == app.trdata.values[trainer_id].tr_id
    )
    assert app.trainer_frame.money_rate_field.var.get() == str(
        app.trdata.values[trainer_id].money_rate
    )
    assert (
        app.trainer_frame.meg_evolution_checkbox.var.get()
        == app.trdata.values[trainer_id].meg_evolution
    )
    assert (
        app.trainer_frame.last_hand_checkbox.var.get()
        == app.trdata.values[trainer_id].last_hand
    )
    assert (
        app.trainer_frame.ai_basic_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_basic
    )
    assert (
        app.trainer_frame.ai_high_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_high
    )
    assert (
        app.trainer_frame.ai_expert_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_expert
    )
    assert (
        app.trainer_frame.ai_double_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_double
    )
    assert (
        app.trainer_frame.ai_raid_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_raid
    )
    assert (
        app.trainer_frame.ai_weak_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_weak
    )
    assert (
        app.trainer_frame.ai_item_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_item
    )
    assert (
        app.trainer_frame.ai_change_checkbox.var.get()
        == app.trdata.values[trainer_id].ai_change
    )
    assert (
        float(app.trainer_frame.view_horizontal_angle_field.var.get())
        == app.trdata.values[trainer_id].view_horizontal_angle
    )
    assert (
        float(app.trainer_frame.view_vertical_angle_field.var.get())
        == app.trdata.values[trainer_id].view_vertical_angle
    )
    assert (
        float(app.trainer_frame.view_range_field.var.get())
        == app.trdata.values[trainer_id].view_range
    )
    _validate_pkmns(app, 0, app.trdata.values[trainer_id].poke_1)
    _validate_pkmns(app, 1, app.trdata.values[trainer_id].poke_2)
    _validate_pkmns(app, 2, app.trdata.values[trainer_id].poke_3)
    _validate_pkmns(app, 3, app.trdata.values[trainer_id].poke_4)
    _validate_pkmns(app, 4, app.trdata.values[trainer_id].poke_5)
    _validate_pkmns(app, 5, app.trdata.values[trainer_id].poke_6)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
