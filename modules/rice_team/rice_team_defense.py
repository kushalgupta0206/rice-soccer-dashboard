from shiny import ui, render
import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import VerticalPitch, Pitch


def shots_against_ui():
    return ui.div(
        ui.output_plot("shots_against_plot")
    )


def shots_against_server(input, output, session, filtered_events):

    @render.plot
    def shots_against_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        shots_df = df[df["type_primary"] == "shot_against"].copy()

        pitch = VerticalPitch(
            pitch_type="wyscout",
            pitch_color="#aabb97",
            line_color="white",
            half=False
        )

        fig, ax = pitch.draw(figsize=(5, 7))

        if shots_df.empty:
            return fig

        goals_against = shots_df[
            shots_df["type_secondary"].str.contains("conceded_goal", case=False, na=False)
        ]

        non_goal_shots = shots_df[
            ~shots_df["type_secondary"].str.contains("conceded_goal", case=False, na=False)
        ]

        for subset, color, label in [
            (non_goal_shots, "white", "Shot Against"),
            (goals_against, "red", "Goal Against"),
        ]:
            if not subset.empty:
                pitch.scatter(
                    subset["location_x"],
                    subset["location_y"],
                    s=150,
                    ax=ax,
                    color=color,
                    edgecolors="black",
                    linewidths=1.2,
                    label=label
                )

        ax.set_xlim(14, 86)
        ax.set_ylim(-2, 20)

        ax.set_title("Shots Against (Own Half)", fontsize=15)
        ax.legend(loc="upper right")

        return fig



def defensive_events_ui():
    return ui.div(
        ui.output_plot("defensive_events_plot")
    )

def defensive_events_server(input, output, session, filtered_events):
    @render.plot
    def defensive_events_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        interceptions = df[
            df["type_primary"].str.contains("interception", case=False, na=False)
        ]

        defensive_duel = df[
            df["type_secondary"].str.contains("defensive_duel", case=False, na=False)
        ]

        sliding_tackle = df[
            df["type_secondary"].str.contains("sliding_tackle|shot_block", case=False, na=False)
        ]

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        for subset, color, label in [
            (defensive_duel, "blue", "Defensive Duel"),
            (sliding_tackle, "red", "Sliding Tackle / Shot Block"),
            (interceptions, "pink", "Interception"),
        ]:
            if not subset.empty:
                pitch.scatter(
                    subset["location_x"],
                    subset["location_y"],
                    s=150,
                    ax=ax,
                    color=color,
                    edgecolors="black",
                    linewidths=1.2,
                    label=label
                )

        ax.set_title("Defensive Events", fontsize=15)
        ax.legend(loc="upper right")
        return fig


def duel_map_ui():
    return ui.div(
        ui.output_plot("duel_map_plot")
    )


def duel_map_server(input, output, session, filtered_events):

    @render.plot
    def duel_map_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        ground_duels = df[df["type_secondary"].str.contains("ground_duel", case=False, na=False)]
        aerial_duels = df[df["type_secondary"].str.contains("aerial_duel", case=False, na=False)]

        ground_won = ground_duels[
            (ground_duels["ground_duel_kept_possession"].astype(str).str.upper() == "TRUE") |
            (ground_duels["ground_duel_recovered_possession"].astype(str).str.upper() == "TRUE")
        ]

        ground_lost = ground_duels[
            (ground_duels["ground_duel_kept_possession"].astype(str).str.upper() != "TRUE") &
            (ground_duels["ground_duel_recovered_possession"].astype(str).str.upper() != "TRUE")
        ]

        aerial_won = aerial_duels[
            aerial_duels["aerial_duel_first_touch"].astype(str).str.upper() == "TRUE"
        ]

        aerial_lost = aerial_duels[
            aerial_duels["aerial_duel_first_touch"].astype(str).str.upper() != "TRUE"
        ]

        won_df = pd.concat([ground_won, aerial_won])
        lost_df = pd.concat([ground_lost, aerial_lost])

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        for subset, color, label in [
            (lost_df, "red", "Lost"),
            (won_df, "green", "Won"),
        ]:
            if not subset.empty:
                pitch.scatter(
                    subset["location_x"],
                    subset["location_y"],
                    s=150,
                    ax=ax,
                    color=color,
                    edgecolors="black",
                    linewidths=1.2,
                    label=label
                )

        ax.set_title("Duel Map", fontsize=15)
        ax.legend(loc="upper right")

        return fig

def turnover_map_ui():
    return ui.div(
        ui.output_plot("turnover_map_plot")
    )

def turnover_map_server(input, output, session, filtered_events):
    @render.plot
    def turnover_map_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        turnover_df = df[df["type_secondary"].str.contains("loss", case=False, na=False)].copy()

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if not turnover_df.empty:
            pitch.scatter(
                turnover_df["location_x"], turnover_df["location_y"],
                s=150, ax=ax,
                color="red", edgecolors="black", linewidths=1.2,
                label="Turnover"
            )

        ax.set_title(f"Turnover Map", fontsize=15)
        ax.legend(loc="upper right")
        return fig

def defense_ui():
    return ui.div(
        shots_against_ui(),
        defensive_events_ui(),
        duel_map_ui(),
        turnover_map_ui(),
    )


def defense_server(input, output, session, filtered_events):
    shots_against_server(input, output, session, filtered_events)
    defensive_events_server(input, output, session, filtered_events)
    duel_map_server(input, output, session, filtered_events)
    turnover_map_server(input, output, session, filtered_events)