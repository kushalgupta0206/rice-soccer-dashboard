from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

def shots_ui():
    return ui.div(
        ui.output_plot("shot_map_plot")
    )

def shots_server(input, output, session, filtered_events):
    @render.plot
    def shot_map_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        shots_df = df[df["type_primary"] == "shot"].copy()

        pitch = VerticalPitch(
            pitch_type='wyscout',
            pitch_color='#aabb97',
            line_color='white',
            half=True
        )
        fig, ax = pitch.draw(figsize=(5, 7))

        if shots_df.empty:
            return fig

        goals      = shots_df[shots_df["type_secondary"].str.contains("goal", case=False, na=False)]
        on_target  = shots_df[
            (shots_df["shot_on_target"].astype(str).str.upper() == "TRUE") &
            ~shots_df["type_secondary"].str.contains("goal", case=False, na=False)
        ]
        off_target = shots_df[
            (shots_df["shot_on_target"].astype(str).str.upper() != "TRUE") &
            ~shots_df["type_secondary"].str.contains("goal", case=False, na=False)
        ]

        for subset, color, label in [
            (off_target, "red",   "Off Target"),
            (on_target,  "white", "On Target"),
            (goals,      "green", "Goal"),
        ]:
            if not subset.empty:
                pitch.scatter(
                    subset["location_x"], subset["location_y"],
                    s=150, ax=ax,
                    color=color, edgecolors="black", linewidths=1.2,
                    label=label
                )

        ax.set_title("Shot Map (Opponent Half)", fontsize=15)
        ax.legend(loc="upper right")
        return fig