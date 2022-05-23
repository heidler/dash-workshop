from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils import get_live_data
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Dash(__name__)

stats = [
    "scores_assists",
    "scores_creepScore",
    "scores_deaths",
    "scores_kills",
    "scores_wardScore",
]

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("League of Legends"),
                html.P(id="time"),
            ],
            style={"textAlign": "center"},
        ),
        html.H2("Stats"),
        dcc.Dropdown(stats, "scores_creepScore", id="stats"),
        html.H2("Team"),
        dcc.Checklist(["ORDER", "CHAOS"], ["ORDER", "CHAOS"], id="team", inline=True),
        dcc.Graph(id="fig"),
        html.Div(
            [
                html.H2("Events", style={"textAlign": "center"}),
                dash_table.DataTable(
                    id="table",
                    filter_action="native",
                    sort_action="native",
                    sort_by=[{"column_id": "EventTime", "direction": "desc"}],
                    sort_mode="multi",
                    page_size=10,
                ),
            ]
        ),
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
    ]
)


@app.callback(
    Output(component_id="fig", component_property="figure"),
    Output(component_id="time", component_property="children"),
    Output(component_id="table", component_property="data"),
    Output(component_id="table", component_property="columns"),
    Input(component_id="stats", component_property="value"),
    Input(component_id="team", component_property="value"),
    Input(component_id="interval", component_property="n_intervals"),
)
def update_layout(input_dropdown, input_checklist, interval):
    live_data = get_live_data("https://127.0.0.1:2999/liveclientdata/allgamedata")
    game_data = live_data["game_data"]
    player_data = live_data["player_data"]
    events = live_data["events"]

    player_data = player_data[player_data["team"].isin(input_checklist)]

    table_data = events.fillna("").to_dict("records")
    table_cols = [{"name": i, "id": i} for i in events.columns]

    fig = px.bar(player_data, x="summonerName", y=input_dropdown, color="team")
    fig.update_layout(showlegend=False)

    clock = f"Time: {game_data['gameTime']}"

    return fig, clock, table_data, table_cols


if __name__ == "__main__":
    app.run_server(debug=False)
