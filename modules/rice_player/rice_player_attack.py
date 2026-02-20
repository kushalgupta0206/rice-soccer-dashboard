from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def attack_ui():
    return ui.div(
        ui.output_plot("loss_scatter_plot")
    )

def attack_server(input, output, session, filtered_events):
    @render.plot
    def loss_scatter_plot():
        df = filtered_events()
        if df is None or df.empty:
            return None
        
        loss_df = df[
            (df["type_primary"] == "pass") & 
            (df["type_secondary"].str.contains("loss", case=False, na=False))
        ]

        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 7))

        if not loss_df.empty:
            pitch.scatter(
                loss_df["pass_end_location_x"], 
                loss_df["pass_end_location_y"], 
                ax=ax, 
                color="red", 
                edgecolors="black", 
                label="Pass Losses"
            )
            ax.legend(loc='upper right')
        
        ax.set_title("End Locations of Failed Passes", fontsize=15)
        return fig