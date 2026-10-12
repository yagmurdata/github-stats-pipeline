import sqlite3

import pandas as pd

conn = sqlite3.connect("repos.db")

print("\nTop 5 repos by stars")
print(pd.read_sql("""
    SELECT full_name, stars, language
    FROM repos
    ORDER BY stars DESC
    LIMIT 5
""", conn))

print("\nRepos per language")
print(pd.read_sql("""
    SELECT language, COUNT(*) AS repos, ROUND(AVG(stars)) AS avg_stars
    FROM repos
    GROUP BY language
    ORDER BY repos DESC
""", conn))

print("\nOldest 5 repos")
print(pd.read_sql("""
    SELECT full_name, created_at
    FROM repos
    ORDER BY created_at ASC
    LIMIT 5
""", conn))

conn.close()