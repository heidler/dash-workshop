import requests
import pandas as pd
import time


def get_request(endpoint, region=None, api_key=None, verify=True):
    if (not region) & (not api_key):
        url = endpoint
    else:
        url = f"{region}{endpoint}/?api_key={api_key}"
    print(f"URL: {url}")

    return requests.get(url, verify=verify).json()


def get_live_data(endpoint):
    def get_item_name(x):
        if x:
            return x["displayName"]

    data = get_request(endpoint, verify=False)

    all_players = pd.DataFrame.from_dict(data["allPlayers"])
    events = pd.DataFrame.from_dict(data["events"]["Events"]).fillna("")

    try:
        assisters = (
            pd.DataFrame.from_records(events["Assisters"])
            .reindex(events.index)
            .add_prefix("Assist")
        )
        events = events.join(assisters).drop(columns=["Assisters"])
        events["EventTime"] = pd.to_datetime(events["EventTime"], unit="s").dt.strftime(
            "%M:%S"
        )
    except:
        None

    game_data = data["gameData"]

    game_data["gameTime"] = time.strftime(
        "%H:%M:%S", time.gmtime(game_data["gameTime"])
    )

    scores = pd.DataFrame.from_records(all_players["scores"]).add_prefix("scores_")
    summoner_spells = pd.DataFrame.from_records(all_players["summonerSpells"])
    summoner_spells_one = pd.DataFrame.from_records(
        summoner_spells["summonerSpellOne"]
    )["displayName"].rename("summonerSpells_one")
    summoner_spells_two = pd.DataFrame.from_records(
        summoner_spells["summonerSpellTwo"]
    )["displayName"].rename("summonerSpells_two")
    runes = pd.DataFrame.from_records(all_players["runes"])
    keystone = pd.DataFrame.from_records(runes["keystone"])["displayName"].rename(
        "runes_keystone"
    )
    primary_rune_tree = pd.DataFrame.from_records(runes["primaryRuneTree"])[
        "displayName"
    ].rename("runes_primaryTree")
    secondary_rune_tree = pd.DataFrame.from_records(runes["secondaryRuneTree"])[
        "displayName"
    ].rename("runes_secondaryTree")
    items = pd.DataFrame.from_records(all_players["items"])
    items = items.apply(lambda y: y.apply(get_item_name), axis=1).rename(
        columns={
            0: "items_SlotOne",
            1: "items_SlotTwo",
            2: "items_SlotThree",
            3: "items_SlotFour",
            4: "items_SlotFive",
            5: "items_SlotSix",
            6: "items_SlotSeven",
        }
    )
    all_players = (
        all_players.join(scores)
        .join(summoner_spells_one)
        .join(summoner_spells_two)
        .join(keystone)
        .join(primary_rune_tree)
        .join(secondary_rune_tree)
        .join(items)
        .drop(columns=["scores", "summonerSpells", "runes", "items"])
    )

    live_data = {"player_data": all_players, "game_data": game_data, "events": events}

    return live_data


def get_champions(endpoint):
    champions = (
        pd.DataFrame.from_dict(get_request(endpoint)["data"], orient="index")
        .reset_index(drop=True)
        .drop(columns=["version", "id", "image"])
    )
    stats = (
        pd.DataFrame.from_dict(champions["stats"].dropna().to_dict(), orient="index")
        .reindex(champions.index)
        .add_prefix("stats_")
    )
    info = (
        pd.DataFrame.from_dict(champions["info"].dropna().to_dict(), orient="index")
        .reindex(champions.index)
        .add_prefix("info_")
    )
    champions = champions.join(info).drop(columns="info")
    champions = champions.join(stats).drop(columns="stats")
    champions.rename(columns={"tags": "roles"}, inplace=True)

    return champions


def get_items(endpoint):
    items = pd.DataFrame.from_dict(get_request(endpoint)["data"], orient="index")
    gold = (
        pd.DataFrame.from_dict(items["gold"].dropna().to_dict(), orient="index")
        .reindex(items.index)
        .add_prefix("gold_")
    )
    stats = (
        pd.DataFrame.from_dict(items["stats"].dropna().to_dict(), orient="index")
        .reindex(items.index)
        .add_prefix("stats_")
    )
    items = items.join(stats).join(gold).drop(columns=["gold", "stats"])

    return items


def role_filter(df, role):
    def filter_tags(x, tag):
        if tag in x:
            return True
        else:
            return False

    return df.loc[df["roles"].apply(filter_tags, args=[role]) == True]
