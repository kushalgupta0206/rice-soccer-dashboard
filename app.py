from shiny import App, ui
import modules.rice_team.rice_team_main as rice_team
import modules.rice_player.rice_player_main as rice_player
import modules.opponent_team.opponent_team_main as opponent_team
import modules.opponent_player.opponent_player_main as opponent_player
import modules.comparison_tool.comparison_tool_main as comparison_tool

app_ui = ui.page_fluid(
    ui.page_navbar(
        rice_team.ui_content(),
        rice_player.ui_content(),
        opponent_team.ui_content(),
        opponent_player.ui_content(),
        comparison_tool.ui_content(),
        title=None,
        id="main_navbar"
    )
)

def server(input, output, session):
    rice_team.server_logic(input, output, session)
    rice_player.server_logic(input, output, session)
    opponent_team.server_logic(input, output, session)
    opponent_player.server_logic(input, output, session)
    comparison_tool.server_logic(input, output, session)

app = App(app_ui, server)