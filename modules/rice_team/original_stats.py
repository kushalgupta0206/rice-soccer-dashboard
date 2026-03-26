import pandas as pd

def parse_timestamp(t):
    parts = str(t).split(":")
    return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

def get_key_passes(df):
    df = df.copy()
    df["timestamp"] = df["timestamp"].apply(parse_timestamp)

    passes = df[df["type_primary"] == "pass"]
    shots = df[df["type_primary"] == "shot"]

    key_passes = []

    for pass_index, pass_row in passes.iterrows():
        same_shots = shots[
            (shots["possession_id"] == pass_row["possession_id"]) &
            (shots["wy_team_id"] == pass_row["wy_team_id"])
        ]

        for shot_index, shot_row in same_shots.iterrows():
            if 0 < (shot_row["timestamp"] - pass_row["timestamp"]) <= 5:
                row = pass_row.copy()
                row["shot_is_goal"] = shot_row["shot_is_goal"]
                key_passes.append(row)
                break

    return pd.DataFrame(key_passes)

def get_possessions_with_shot(df):
    shots = df[df["type_primary"] == "shot"]
 
    possession_ids_with_shot = set(shots["possession_id"].unique())
 
    return df[df["possession_id"].isin(possession_ids_with_shot)]

def get_shots_by_15_min(df):
    shots = df[df["type_primary"] == "shot"].copy()
 
    bins   = [0, 15, 30, 45, 60, 75, 90]
    labels = ["0-15", "16-30", "31-45", "46-60", "61-75", "76-90"]
 
    shots["period_15"] = pd.cut(shots["minute"], bins=bins, labels=labels, right=True)
 
    result = shots.groupby(["wy_match_id", "opponent_team_name", "period_15"], observed=True).size().reset_index(name="shots")
    result["period_15"] = pd.Categorical(result["period_15"], categories=labels, ordered=True)
    return result.sort_values(["wy_match_id", "period_15"]).reset_index(drop=True)