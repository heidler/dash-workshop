from utils import get_data, transform_champions, role_filter
import plotly.express as px
import pandas as pd

# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)

data = get_data(
    "http://ddragon.leagueoflegends.com/cdn/12.9.1/data/en_US/champion.json"
)

# data = get_data("assets/champion.json", file=True)
champions = transform_champions(data)

# print(champions)
# print(champions.columns)
# print(champions["roles"])

champions = role_filter(champions, "Assassin")
champions = champions.loc[champions["partype"] == "Mana"]
champions.sort_values("stats_mp", inplace=True)

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
    xaxis_categoryorder="total ascending",
)

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

fig.show()
