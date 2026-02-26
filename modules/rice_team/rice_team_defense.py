from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

def shots_against_ui():
    return ui.div(
        ui.output_plot("shot_against_map_plot")
    )

def shots_against_server(input, output, session, filtered_events):
    @render.plot
    def shot_against_map_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        shots_df = df[df["type_primary"] == "shot_against"].copy()

        pitch = VerticalPitch(
            pitch_type='wyscout',
            pitch_color='#aabb97',
            line_color='white',
            half=False
        )
        fig, ax = pitch.draw(figsize=(5, 7))

        if shots_df.empty:
            return fig

        goals_against = shots_df[shots_df["type_secondary"].str.contains("conceded_goal", case=False, na=False)]
        shots_against = shots_df[~shots_df["type_secondary"].str.contains("conceded_goal", case=False, na=False)]

        for subset, color, label in [
            (shots_against, "white", "Shot Against"),
            (goals_against, "red",   "Goal Against"),
        ]:
            if not subset.empty:
                pitch.scatter(
                    subset["location_x"], subset["location_y"],
                    s=150, ax=ax,
                    color=color, edgecolors="black", linewidths=1.2,
                    label=label
                )

        ax.set_xlim(14, 86)
        ax.set_ylim(-2, 20)
        
        ax.set_title("Shots Against (Own Half)", fontsize=15)
        ax.legend(loc="upper right")
        return fig

def defense_ui():
    return ui.div(
        shots_against_ui(),
    )

def defense_server(input, output, session, filtered_events):
    shots_against_server(input, output, session, filtered_events)