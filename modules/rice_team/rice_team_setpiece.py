from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def free_kicks_ui():
    return ui.div(
        ui.output_plot("free_kicks_plot")
    )

def free_kicks_server(input, output, session, filtered_events):
    @render.plot
    def free_kicks_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        fk_df = df[df["type_primary"] == "free_kick"].copy()

        pitch = Pitch(
            pitch_type='wyscout',
            pitch_color='#aabb97',
            line_color='white'
        )
        fig, ax = pitch.draw(figsize=(10, 7))

        if fk_df.empty:
            return fig

        fk_goals  = fk_df[fk_df["type_secondary"].str.contains("goal", case=False, na=False)]
        fk_shots  = fk_df[
            fk_df["type_secondary"].str.contains("free_kick_shot", case=False, na=False) &
            ~fk_df["type_secondary"].str.contains("goal", case=False, na=False)
        ]
        fk_passes = fk_df[
            ~fk_df["type_secondary"].str.contains("free_kick_shot", case=False, na=False) &
            ~fk_df["type_secondary"].str.contains("goal", case=False, na=False)
        ]

        for subset, color, label in [
            (fk_passes, "yellow", "Pass / Cross"),
            (fk_shots,  "white",  "Shot"),
            (fk_goals,  "green",  "Goal"),
        ]:
            if not subset.empty:
                pitch.scatter(
                    subset["location_x"], subset["location_y"],
                    s=150, ax=ax,
                    color=color, edgecolors="black", linewidths=1.2,
                    label=label
                )

        ax.set_title("Free Kick Locations", fontsize=15)
        ax.legend(loc="upper right")
        return fig