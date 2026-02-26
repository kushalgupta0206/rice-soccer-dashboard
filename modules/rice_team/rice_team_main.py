import pandas as pd
from pathlib import Path
from shiny import ui, render, reactive
from . import rice_team_attack as attack
from . import rice_team_defence as defence
from . import rice_team_setpiece as setpiece

def get_match_choices():
    data_path = Path(__file__).parent.parent.parent / "data" / "american_athletic_womens_soccer_fall_2025_match_data.csv"
    df = pd.read_csv(data_path)
    team_id = 61585
    team_matches = df[(df["home_team_id"] == team_id) | (df["away_team_id"] == team_id)]
    return dict(zip(team_matches["wy_match_id"].astype(str), team_matches["label_date"]))

def ui_content():
    match_choices = get_match_choices()
    return ui.nav_panel(
        "Rice Team",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_selectize(
                    "selected_rice_matches",
                    "Select Matches:",
                    choices=match_choices,
                    multiple=True
                ),
                ui.input_select(
                    "selected_rice_team_area",
                    "Area:",
                    choices={
                        "Attack": "Attack",
                        "Defence": "Defence",
                        "Set-Pieces": "Set-Pieces"
                    }
                ),
                open="always",
                width="400px",
                style="min-height: 800px; padding: 20px;"
            ),
            ui.output_text_verbatim("debug_selection_rice_team"),
            ui.output_text_verbatim("debug_selection_rice_team"),
            attack.attack_ui(),
            shots.shots_ui(),
            shots_against.shots_against_ui(),
            free_kicks.free_kicks_ui(),
        ),
        value="tab_1_val"
    )

def server_logic(input, output, session):
    data_path = Path(__file__).parent.parent.parent / "data" / "american_athletic_womens_soccer_fall_2025_event_data_selected_cols.csv"
    event_df = pd.read_csv(data_path)

    @reactive.calc
    def filtered_events():
        selected = input.selected_rice_matches()
        if not selected:
            return pd.DataFrame()
        return event_df[event_df["wy_match_id"].astype(str).isin(selected)]

    @render.ui
    def dynamic_content_rice_team():
        area = input.selected_rice_team_area()
        if area == "Attack":
            return attack.attack_ui()
        elif area == "Defence":
            return defence.defence_ui()
        elif area == "Set-Pieces":
            return setpiece.setpiece_ui()

    attack.attack_server(input, output, session, filtered_events)
    defence.defence_server(input, output, session, filtered_events)
    setpiece.setpiece_server(input, output, session, filtered_events)