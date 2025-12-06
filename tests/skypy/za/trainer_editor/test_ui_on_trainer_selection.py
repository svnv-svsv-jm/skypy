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
        form_id=random.randint(0, 3),  # type: ignore
        sex=random.choice([0, 1, 2]),  # type: ignore
        item=random.randint(0, 20),  # type: ignore
        level=random.randint(0, 100),  # type: ignore
        ball_id=random.choice(list(settings.za_ball_mappings.values())),  # type: ignore
        waza_1=ZAWazaData(waza_id=random.randint(0, 20)),  # type: ignore
        waza_2=ZAWazaData(waza_id=random.randint(0, 20)),  # type: ignore
        waza_3=ZAWazaData(waza_id=random.randint(0, 20)),  # type: ignore
        waza_4=ZAWazaData(waza_id=random.randint(0, 20)),  # type: ignore
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


def test_on_trainer_selected_raises_error(
    za_trainer_editor_app: ZATrainerEditor,
) -> None:
    """Test `on_trainer_selected` raises `ValueError` if trainer not found."""
    with pytest.raises(ValueError):
        za_trainer_editor_app.on_trainer_selected("invalid_trainer")


@pytest.mark.parametrize("trainer_id", [1])
def test_on_trainer_selected_switches_trainer(
    za_trainer_editor_app: ZATrainerEditor,
    trainer_id: int,
) -> None:
    """Test `on_trainer_selected` updates the trainer frame."""
    app = za_trainer_editor_app

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

    # Tests
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


class TestDataLeakageBetweenTrainers:
    """Tests to catch data leakage when switching between trainers.

    Bug report: User selects trainer A, edits pokemon, then selects trainer B
    and sees some of trainer A's pokemon data appearing in trainer B.
    Usually affects "the last ones" (pokemon 5 and 6).
    """

    def test_editing_trainer_a_does_not_affect_trainer_b_data(
        self,
        za_trainer_editor_app: ZATrainerEditor,
    ) -> None:
        """When I edit Trainer A's pokemon and switch to Trainer B,
        Trainer B should show its OWN data, not Trainer A's edits.

        NOTE: var.set() on Entry fields triggers trace callbacks that update the data.
        option_menu.set() does NOT trigger command callbacks (only user clicks do).
        """
        app = za_trainer_editor_app

        # Get two different trainers
        trainer_a = app.trdata.values[0]
        trainer_b = app.trdata.values[1]

        # Store original data for trainer B
        trainer_b_original_poke5_level = trainer_b.poke_5.level
        trainer_b_original_poke6_level = trainer_b.poke_6.level

        # Step 1: Select Trainer A
        app.on_trainer_selected(trainer_a.tr_id)

        # Verify we're viewing trainer A
        assert app.trainer_frame.trainer_ref is trainer_a
        assert app.trainer_frame.pokemon_fields[4].pokemon_ref is trainer_a.poke_5

        # Step 2: Simulate user editing Trainer A's Pokemon 5 via UI
        # var.set() triggers trace callbacks that update the data model
        new_level_for_a = 99
        app.trainer_frame.pokemon_fields[4].level_field.var.set(str(new_level_for_a))

        # Also edit Pokemon 6 (the "last ones" mentioned in bug report)
        app.trainer_frame.pokemon_fields[5].level_field.var.set("88")

        # Verify trainer A's data was actually modified
        assert trainer_a.poke_5.level == new_level_for_a, (
            f"Edit failed: trainer_a.poke_5.level should be {new_level_for_a}, "
            f"got {trainer_a.poke_5.level}"
        )
        assert trainer_a.poke_6.level == 88

        # Step 3: Switch to Trainer B
        app.on_trainer_selected(trainer_b.tr_id)

        # Verify we're now viewing trainer B
        assert app.trainer_frame.trainer_ref is trainer_b
        assert app.trainer_frame.pokemon_fields[4].pokemon_ref is trainer_b.poke_5

        # Step 4: Verify Trainer B's DATA was NOT modified
        # This is the critical check - trainer B's data should be unchanged
        assert trainer_b.poke_5.level == trainer_b_original_poke5_level, (
            f"DATA LEAKAGE! Trainer B's poke_5.level was modified! "
            f"Expected {trainer_b_original_poke5_level}, got {trainer_b.poke_5.level}"
        )
        assert trainer_b.poke_6.level == trainer_b_original_poke6_level, (
            f"DATA LEAKAGE! Trainer B's poke_6.level was modified! "
            f"Expected {trainer_b_original_poke6_level}, got {trainer_b.poke_6.level}"
        )

        # Step 5: Verify UI shows Trainer B's data (not Trainer A's)
        assert app.trainer_frame.pokemon_fields[4].level_field.var.get() == str(
            trainer_b_original_poke5_level
        ), "UI shows wrong level for trainer B's poke_5"
        assert app.trainer_frame.pokemon_fields[5].level_field.var.get() == str(
            trainer_b_original_poke6_level
        ), "UI shows wrong level for trainer B's poke_6"

        # Step 6: Verify Trainer A's edits are still intact
        assert trainer_a.poke_5.level == new_level_for_a
        assert trainer_a.poke_6.level == 88

    def test_switching_trainers_preserves_edits_on_original_trainer(
        self,
        za_trainer_editor_app: ZATrainerEditor,
    ) -> None:
        """When I edit Trainer A, switch to B, then back to A,
        Trainer A should still have my edits.
        """
        app = za_trainer_editor_app

        trainer_a = app.trdata.values[0]
        trainer_b = app.trdata.values[1]

        # Select Trainer A and edit
        app.on_trainer_selected(trainer_a.tr_id)
        app.trainer_frame.pokemon_fields[4].level_field.var.set("77")

        # Verify edit took effect
        assert trainer_a.poke_5.level == 77

        # Switch to Trainer B
        app.on_trainer_selected(trainer_b.tr_id)

        # Switch back to Trainer A
        app.on_trainer_selected(trainer_a.tr_id)

        # Verify edit is still there
        assert trainer_a.poke_5.level == 77
        assert app.trainer_frame.pokemon_fields[4].level_field.var.get() == "77"

    def test_editing_waza_via_dropdown_does_not_leak_between_trainers(
        self,
        za_trainer_editor_app: ZATrainerEditor,
    ) -> None:
        """Waza (moves) edits via dropdown should not leak between trainers.

        This simulates user clicking on a move dropdown by invoking the command callback.
        """
        app = za_trainer_editor_app

        trainer_a = app.trdata.values[0]
        trainer_b = app.trdata.values[1]

        # Store original waza for trainer B
        trainer_b_poke5_waza1_id = trainer_b.poke_5.waza_1.waza_id

        # Select Trainer A
        app.on_trainer_selected(trainer_a.tr_id)

        # Simulate user clicking on waza dropdown by calling the command callback
        new_waza_name = settings.za_waza_table[50]  # Some move
        waza_frame = app.trainer_frame.pokemon_fields[4].waza_frames[0]
        waza_frame.option_menu._command(new_waza_name)

        # Verify trainer A's waza was modified
        assert (
            trainer_a.poke_5.waza_1.waza_id == 50
        ), f"Trainer A's waza edit failed! Expected 50, got {trainer_a.poke_5.waza_1.waza_id}"

        # Switch to Trainer B
        app.on_trainer_selected(trainer_b.tr_id)

        # Verify Trainer B's waza was NOT modified
        assert trainer_b.poke_5.waza_1.waza_id == trainer_b_poke5_waza1_id, (
            f"DATA LEAKAGE! Trainer B's waza was modified! "
            f"Expected {trainer_b_poke5_waza1_id}, got {trainer_b.poke_5.waza_1.waza_id}"
        )

    def test_editing_species_dropdown_does_not_leak(
        self,
        za_trainer_editor_app: ZATrainerEditor,
    ) -> None:
        """Species dropdown edits should not leak between trainers.

        This simulates user clicking on species dropdown by invoking command callback.
        """
        app = za_trainer_editor_app

        trainer_a = app.trdata.values[0]
        trainer_b = app.trdata.values[1]

        # Store original species for trainer B
        trainer_b_poke5_dev_id = trainer_b.poke_5.dev_id

        # Select Trainer A
        app.on_trainer_selected(trainer_a.tr_id)

        # Simulate user clicking on species dropdown
        new_species_name = settings.za_species_table[25]  # Pikachu
        dev_id_dropdown = app.trainer_frame.pokemon_fields[4].dev_id_field.option_menu
        dev_id_dropdown._command(new_species_name)

        # Verify trainer A's species was modified
        assert (
            trainer_a.poke_5.dev_id == 25
        ), f"Trainer A's species edit failed! Expected 25, got {trainer_a.poke_5.dev_id}"

        # Switch to Trainer B
        app.on_trainer_selected(trainer_b.tr_id)

        # Verify Trainer B's species was NOT modified
        assert trainer_b.poke_5.dev_id == trainer_b_poke5_dev_id, (
            f"DATA LEAKAGE! Trainer B's species was modified! "
            f"Expected {trainer_b_poke5_dev_id}, got {trainer_b.poke_5.dev_id}"
        )

    def test_multiple_trainer_switches_no_data_accumulation(
        self,
        za_trainer_editor_app: ZATrainerEditor,
    ) -> None:
        """Switching between multiple trainers should not accumulate stale data."""
        app = za_trainer_editor_app

        # Get 3 trainers
        trainer_a = app.trdata.values[0]
        trainer_b = app.trdata.values[1]
        trainer_c = app.trdata.values[2]

        # Store original data
        original_b_poke5_level = trainer_b.poke_5.level
        original_c_poke5_level = trainer_c.poke_5.level

        # Edit trainer A
        app.on_trainer_selected(trainer_a.tr_id)
        app.trainer_frame.pokemon_fields[4].level_field.var.set("11")

        # Switch to B, edit
        app.on_trainer_selected(trainer_b.tr_id)
        app.trainer_frame.pokemon_fields[4].level_field.var.set("22")

        # Switch to C
        app.on_trainer_selected(trainer_c.tr_id)

        # C should have its original data
        assert trainer_c.poke_5.level == original_c_poke5_level, (
            f"Trainer C data was corrupted! "
            f"Expected {original_c_poke5_level}, got {trainer_c.poke_5.level}"
        )

        # Verify A and B have their edits (not the original values)
        assert trainer_a.poke_5.level == 11
        assert trainer_b.poke_5.level == 22
        # B should NOT have its original value anymore
        assert (
            trainer_b.poke_5.level != original_b_poke5_level
            or original_b_poke5_level == 22
        )


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
