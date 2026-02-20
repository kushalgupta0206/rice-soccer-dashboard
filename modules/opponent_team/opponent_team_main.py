import pandas as pd
from pathlib import Path
from shiny import ui, render, reactive

def get_opp_team_id():
    data_path = Path(__file__).parent.parent.parent / "data" / "american_athletic_womens_soccer_fall_2025_team_data.csv"
    df = pd.read_csv(data_path)
    return dict(zip(df["wy_team_id"].astype(str), df["wy_team_name"]))

def load_match_data():
    data_path = Path(__file__).parent.parent.parent / "data" / "american_athletic_womens_soccer_fall_2025_match_data.csv"
    return pd.read_csv(data_path)

def get_match_choices_for_team(df, team_id):
    if team_id is None:
        return {}
    team_id = int(float(team_id))
    team_matches = df[(df["home_team_id"].astype(float) == team_id) | (df["away_team_id"].astype(float) == team_id)]
    return dict(zip(team_matches["wy_match_id"].astype(str), team_matches["label_date"]))

def ui_content():
    opp_team_choices = get_opp_team_id()
    df = load_match_data()
    initial_team = list(opp_team_choices.keys())[0] if opp_team_choices else None
    initial_matches = get_match_choices_for_team(df, initial_team) if initial_team else {}
    
    return ui.nav_panel(
        "Opponent Team",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_selectize(
                    "selected_opp_team", 
                    "Select Opponent:", 
                    choices=opp_team_choices,
                    selected=initial_team
                ),
                ui.input_selectize(
                    "selected_opp_matches", 
                    "Select Matches:", 
                    choices=initial_matches, 
                    multiple=True
                ),
                ui.input_select(
                    "selected_opp_team_area",
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
            ui.output_text_verbatim("debug_selection_opp_team"),
        ),
        value="tab_3_val"
    )

def server_logic(input, output, session):
    df = load_match_data()
    
    @reactive.Effect
    @reactive.event(input.selected_opp_team)
    def update_match_choices():
        team_id = input.selected_opp_team()
        if team_id:
            new_choices = get_match_choices_for_team(df, team_id)
            ui.update_selectize(
                "selected_opp_matches",
                choices=new_choices,
                selected=None
            )
    
    @render.text
    def debug_selection_opp_team():
        team_id = input.selected_opp_team()
        match_ids = input.selected_opp_matches()
        return f"Selected Opponent Team: {team_id}\nSelected Match IDs: {match_ids}"