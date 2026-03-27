from shiny import ui, render
import matplotlib.pyplot as plt
from mplsoccer import Radar

def general_ui():
    return ui.div(
        ui.output_plot("duel_radar_plot", height="600px", width="100%")
    )

def general_server(input, output, session, filtered_comparison_data):
    @render.plot
    def duel_radar_plot():
        result = filtered_comparison_data()
        df = result["data"]
        name_col = result["name_col"]
        name1 = df[df["comparison_label"] == "Entity_1"][name_col].values[0]
        name2 = df[df["comparison_label"] == "Entity_2"][name_col].values[0]
        
        if df.empty or len(df) < 2:
            return None
            
        params = ["Kept Possession %", "Progressed with Ball %", "Recovered Possession %", "Stopped Progression %", "Aerial Win %"]
        cols = ["ground_kept_pct", "ground_prog_pct", "ground_rec_pct", "ground_stop_pct", "aerial_win_pct"]
        
        low = [0] * 5
        high = [1] * 5

        val_1 = df[df["comparison_label"] == "Entity_1"][cols].values.flatten()
        val_2 = df[df["comparison_label"] == "Entity_2"][cols].values.flatten()
        
        radar = Radar(
          params, low, high,
          round_int=[False]*len(params),
          num_rings=6,
          ring_width=1,
          center_circle_radius=1
      )


        fig, ax = radar.setup_axis(figsize=(14, 14), facecolor='#fbfbfb')

        radar.draw_circles(ax=ax, facecolor="#dddddd", edgecolor="white", alpha=0.5)

        radar_poly1, radar_poly2, vertices1, vertices2 = radar.draw_radar_compare(
            val_1, val_2,
            ax=ax,
            kwargs_radar={"facecolor": "#70e0be", "alpha": 0.5, "edgecolor": "#70e0be", "lw": 2},
            kwargs_compare={"facecolor": "#d63391", "alpha": 0.5, "edgecolor": "#d63391", "lw": 2}
        )

        ax.scatter(vertices1[:, 0], vertices1[:, 1], c="#70e0be", edgecolors="white", s=60, zorder=4)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c="#d63391", edgecolors="white", s=60, zorder=4)

        ax.text(-10, 8, input.comparison_type() + ' 1 - '+ name1, color="#70e0be", fontsize=12, ha='left')
        ax.text(10, 8, input.comparison_type() + ' 2 - ' + name2, color="#d63391", fontsize=12, ha='right')

        radar.draw_range_labels(ax=ax, fontsize=10)
        radar.draw_param_labels(ax=ax, fontsize=10)

        return fig
