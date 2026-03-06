from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Pitch
import numpy as np

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

def attack_heatmap_ui():
    return ui.div(
        ui.output_plot("attack_heatmap_plot")
    )

def attack_heatmap_server(input, output, session, filtered_events):
    @render.plot
    def attack_heatmap_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        pitch = Pitch(pitch_type='wyscout', pitch_color='#1a472a', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if df.empty:
            ax.set_title("Attacking Activity Heatmap", fontsize=15)
            return fig

        pitch.kdeplot(
            df["location_x"], df["location_y"],
            ax=ax,
            cmap="RdYlGn_r",
            fill=True,
            levels=100,
            alpha=0.85,
            bw_adjust=0.8,
            thresh=0.10,
        )

        ax.set_title("Attacking Activity Heatmap", fontsize=15)
        return fig

def progressive_passes_ui():
    return ui.div(
        ui.output_plot("progressive_passes_plot")
    )

def progressive_passes_server(input, output, session, filtered_events):
    @render.plot
    def progressive_passes_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        prog_df = df[
            df["type_secondary"].str.contains("progressive_pass", case=False, na=False) &
            (df["pass_accurate"].astype(str).str.upper() == "TRUE")
        ].copy()

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if prog_df.empty:
            ax.set_title("Progressive Pass Map", fontsize=15)
            return fig

        pitch.arrows(
            prog_df["location_x"], prog_df["location_y"],
            prog_df["pass_end_location_x"], prog_df["pass_end_location_y"],
            width=1, headwidth=5, headlength=5,
            color="black", alpha=0.6, ax=ax
        )

        ax.set_title(f"Progressive Pass Map (n={len(prog_df)})", fontsize=15)
        return fig

def final_third_passes_ui():
    return ui.div(
        ui.output_plot("final_third_passes_plot")
    )


def final_third_passes_server(input, output, session, filtered_events):
    @render.plot
    def final_third_passes_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        pass_df = df[
            df["type_secondary"].str.contains("pass_to_final_third", case=False, na=False) &
            (df["pass_accurate"].astype(str).str.upper() == "TRUE")
        ].copy()

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if pass_df.empty:
            ax.set_title("Passes to Final Third", fontsize=15)
            return fig

        pitch.arrows(
            pass_df["location_x"], pass_df["location_y"],
            pass_df["pass_end_location_x"], pass_df["pass_end_location_y"],
            width=1, headwidth=5, headlength=5,
            color="black", alpha=0.6, ax=ax
        )

        ax.set_title(f"Passes to Final Third (n={len(pass_df)})", fontsize=15)
        return fig

def progressive_runs_ui():
    return ui.div(
        ui.output_plot("progressive_runs_plot")
    )

def progressive_runs_server(input, output, session, filtered_events):
    @render.plot
    def progressive_runs_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None

        prog_df = df[
            df["type_secondary"].str.contains("progressive_run", case=False, na=False)
        ].copy()

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if prog_df.empty:
            ax.set_title("Progressive Run Map", fontsize=15)
            return fig

        pitch.arrows(
            prog_df["location_x"], prog_df["location_y"],
            prog_df["carry_end_location_x"], prog_df["carry_end_location_y"],
            width=1, headwidth=5, headlength=5,
            color="black", alpha=0.6, ax=ax
        )

        ax.set_title(f"Progressive Run Map (n={len(prog_df)})", fontsize=15)
        return fig

def attack_ui():
    return ui.div(
        shots_ui(),
        progressive_passes_ui(),
        final_third_passes_ui(),
        progressive_runs_ui(),
        attack_heatmap_ui()
    )

def attack_server(input, output, session, filtered_events):
    shots_server(input, output, session, filtered_events)
    progressive_passes_server(input, output, session, filtered_events)
    final_third_passes_server(input, output, session, filtered_events)
    progressive_runs_server(input, output, session, filtered_events)
    attack_heatmap_server(input, output, session, filtered_events)