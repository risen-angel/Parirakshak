import pandas as pd

def calculate_scores(df):
    df["damage"] = (
        (20.83 * df["vibration"]) +
        (0.25 * df["stress"]) +
        (50 * df["crack"])
    )

    df["score"] = 100 - df["damage"]
    df["score"] = df["score"].clip(0, 100)

    def get_status(score):
        if score >= 90:
            return "green"
        elif score >= 70:
            return "yellow"
        else:
            return "red"

    df["status"] = df["score"].apply(get_status)

    return df
