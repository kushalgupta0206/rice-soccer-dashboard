from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def attack_ui():
    return ui.div(
        ui.output_plot("loss_scatter_plot"),
        ui.output_plot("pass_map_plot")
    )

def attack_server(input, output, session, filtered_events):
    @render.plot
    def loss_scatter_plot():
        player_id = input.selected_rice_player()
        df = filtered_events()
        df_filtered = df[df['wy_player_id'] == int(float(player_id))]
        if df_filtered is None or df_filtered.empty:
            return None
        
        loss_df = df_filtered[
            (df_filtered["type_primary"] == "pass") & 
            (df_filtered["type_secondary"].str.contains("loss", case=False, na=False))
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

    @render.plot
    def pass_map_plot():
        player_id = input.selected_rice_player()
        df = filtered_events()
        df_filtered = df[df['wy_player_id'] == int(float(player_id))]
        if df_filtered is None or df_filtered.empty:
            return None
        
        key_pass_df = df_filtered[
            (df_filtered["type_primary"] == "pass") 
            # & 
            # (df["type_secondary"].str.contains("key", case=False, na=False))
        ]
        
        pitch = Pitch(pitch_type='wyscout', pitch_color='#aabb97', line_color='white') 
        fig, ax = pitch.draw(figsize=(10, 7))

        if not key_pass_df.empty:
            pitch.arrows(
                key_pass_df["location_x"], 
                key_pass_df["location_y"],  
                key_pass_df["pass_end_location_x"],
                key_pass_df["pass_end_location_y"], 
                ax=ax, 
                width=2,  
                headwidth=3,   
                headlength=5, 
                color="blue", 
                label="Key Passes"
            )
            ax.legend(loc='upper right')
        ax.set_title("Passes", fontsize=15)
        return fig