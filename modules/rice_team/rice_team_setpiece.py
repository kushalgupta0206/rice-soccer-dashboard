from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Pitch

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

def corner_map_ui():
    return ui.div(
        ui.output_plot("corner_map_plot")
    )


def corner_map_server(input, output, session, filtered_events):
    @render.plot
    def corner_map_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        corner_df = df[df["type_primary"] == "corner"].copy()

        pitch = VerticalPitch(
            pitch_type='wyscout',
            pitch_color='#aabb97',
            line_color='white',
            half=True
        )
        fig, ax = pitch.draw(figsize=(5, 7))

        if not corner_df.empty:
            pitch.scatter(
                corner_df["pass_end_location_x"], corner_df["pass_end_location_y"],
                s=150, ax=ax,
                color="black", edgecolors="white", linewidths=1.2,
                label="Corner Delivery"
            )

        ax.set_title(f"Corner Deliveries (n={len(corner_df)})", fontsize=15)
        ax.legend(loc="upper right")
        return fig

def free_kick_cross_map_ui():
    return ui.div(
        ui.output_plot("free_kick_cross_map_plot")
    )

def free_kick_cross_map_server(input, output, session, filtered_events):
    @render.plot
    def free_kick_cross_map_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        fk_cross_df = df[
            df["type_secondary"].str.contains("free_kick_cross", case=False, na=False)
        ].copy()

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if fk_cross_df.empty:
            ax.set_title("Free Kick Cross Deliveries", fontsize=15)
            return fig

        pitch.arrows(
            fk_cross_df["location_x"], fk_cross_df["location_y"],
            fk_cross_df["pass_end_location_x"], fk_cross_df["pass_end_location_y"],
            width=1, headwidth=5, headlength=5,
            color="black", alpha=0.6, ax=ax
        )

        ax.set_title(f"Free Kick Cross Deliveries (n={len(fk_cross_df)})", fontsize=15)
        return fig

def setpiece_ui():
    return ui.div(
        free_kicks_ui(),
        corner_map_ui(),
        free_kick_cross_map_ui(),
    )

def setpiece_server(input, output, session, filtered_events):
    free_kicks_server(input, output, session, filtered_events)
    corner_map_server(input, output, session, filtered_events)
    free_kick_cross_map_server(input, output, session, filtered_events)