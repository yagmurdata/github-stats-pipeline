import sqlite3
from datetime import date

import pandas as pd
import requests


def extract():
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "topic:data-engineering",
        "sort": "stars",
        "order": "desc",
        "per_page": 50,
    }
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()["items"]


def transform(items):
    df = pd.DataFrame(items)[
        ["full_name", "stargazers_count", "forks_count",
         "language", "created_at", "html_url"]
    ]
    df = df.rename(columns={"stargazers_count": "stars", "forks_count": "forks"})
    df["language"] = df["language"].fillna("Unknown")
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date.astype(str)
    df["pulled_on"] = date.today().isoformat()
    return df


def load(df):
    conn = sqlite3.connect("repos.db")
    df.to_sql("repos", conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    items = extract()
    df = transform(items)
    load(df)
    print(f"Loaded {len(df)} repos into repos.db")