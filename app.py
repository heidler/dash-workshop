from ast import arg
from dash import Dash, html, dcc
from numpy import sort
import plotly.express as px
import pandas as pd
from lol import get_live_data, get_champions, get_items, tag_filter

pd.set_option("display.max_columns", None)

# ZÍSKÁNÍ DAT Z Riot API
api_key = "RGAPI-61cd73fd-2a60-4934-892d-22a8482e079e"
region = "https://eun1.api.riotgames.com"

champions = get_champions(
    "http://ddragon.leagueoflegends.com/cdn/12.9.1/data/en_US/champion.json"
)
items = get_items("http://ddragon.leagueoflegends.com/cdn/12.9.1/data/en_US/item.json")
print(items)

# live_data = get_live_data("https://127.0.0.1:2999/liveclientdata/allgamedata")


# GRAPH

champions.sort_values("stats_hp", inplace=True)

champions = tag_filter(champions, "Mage", "tags")
champions = champions.loc[champions["partype"] == "Mana"]
champions.sort_values("stats_hp", inplace=True)

fig = px.bar(
    champions,
    x="name",
    y="stats_hp",
    color="partype",
    text_auto=".2s",
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
fig.update_layout(
    title=f"Hrdinové League of Legends",
    xaxis_title="Hrdina",
    yaxis_title="Počet životů",
    legend_title="Energie",
    font_color="red",
    title_font_color="green",
    font_family="Arial",
    title_font_family="Comic Sans MS",
    font_size=16,
    title_x=0.5,
)
fig.update_layout(xaxis_categoryorder="total ascending")

fig.add_shape(
    type="line",
    line_color="red",
    line_width=3,
    opacity=1,
    line_dash="dot",
    x0=0,
    x1=1,
    xref="paper",
    y0=500,
    y1=500,
    yref="y",
)

fig.add_annotation(
    text="Nechci!", x="Kled", y=350, arrowhead=1, showarrow=True, font_size=10
)

# DASH
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
