"""
Script: db_insert.py
Purpose: Create database schema and insert reviews into PostgreSQL.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

# ── Connection settings ───────────────────────────────────────────────────────
DB_USER     = "postgres"
DB_PASSWORD = "meklit1234"  
DB_HOST     = "localhost"
DB_PORT     = "5432"
DB_NAME     = "fintech_reviews"

def get_engine():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS banks (
                id      SERIAL PRIMARY KEY,
                name    VARCHAR(100) UNIQUE NOT NULL
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS reviews (
                id              SERIAL PRIMARY KEY,
                bank_id         INTEGER REFERENCES banks(id),
                review          TEXT,
                rating          INTEGER,
                date            DATE,
                source          VARCHAR(50),
                sentiment_score FLOAT,
                sentiment_label VARCHAR(20),
                theme           VARCHAR(50)
            );
        """))
        conn.commit()
    print("Tables created successfully.")

def insert_data(engine):
    df = pd.read_csv("data/raw/reviews_with_themes.csv")

    # Insert banks
    banks = df["bank"].unique()
    with engine.connect() as conn:
        for bank in banks:
            conn.execute(text(
                "INSERT INTO banks (name) VALUES (:name) ON CONFLICT (name) DO NOTHING"
            ), {"name": bank})
        conn.commit()
    print(f"Inserted {len(banks)} banks.")

    # Get bank id mapping
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name FROM banks"))
        bank_map = {row[1]: row[0] for row in result}

    # Insert reviews
    df["bank_id"] = df["bank"].map(bank_map)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    records = df[["bank_id","review","rating","date","source",
                  "sentiment_score","sentiment_label","theme"]].to_dict(orient="records")

    with engine.connect() as conn:
        for record in records:
            conn.execute(text("""
                INSERT INTO reviews
                    (bank_id, review, rating, date, source,
                     sentiment_score, sentiment_label, theme)
                VALUES
                    (:bank_id, :review, :rating, :date, :source,
                     :sentiment_score, :sentiment_label, :theme)
            """), record)
        conn.commit()
    print(f"Inserted {len(records)} reviews.")

def run_queries(engine):
    print("\n── Sample SQL Queries ──────────────────────────────")
    with engine.connect() as conn:

        print("\n1. Review count per bank:")
        r = conn.execute(text("""
            SELECT b.name, COUNT(*) as review_count
            FROM reviews r JOIN banks b ON r.bank_id = b.id
            GROUP BY b.name ORDER BY review_count DESC
        """))
        for row in r: print(f"   {row[0]}: {row[1]}")

        print("\n2. Average rating per bank:")
        r = conn.execute(text("""
            SELECT b.name, ROUND(AVG(r.rating)::numeric, 2) as avg_rating
            FROM reviews r JOIN banks b ON r.bank_id = b.id
            GROUP BY b.name ORDER BY avg_rating DESC
        """))
        for row in r: print(f"   {row[0]}: {row[1]}")

        print("\n3. Sentiment distribution:")
        r = conn.execute(text("""
            SELECT sentiment_label, COUNT(*) as count
            FROM reviews GROUP BY sentiment_label ORDER BY count DESC
        """))
        for row in r: print(f"   {row[0]}: {row[1]}")

        print("\n4. Most common themes:")
        r = conn.execute(text("""
            SELECT theme, COUNT(*) as count
            FROM reviews GROUP BY theme ORDER BY count DESC
        """))
        for row in r: print(f"   {row[0]}: {row[1]}")

def main():
    print("Connecting to PostgreSQL...")
    engine = get_engine()
    print("Connected.")
    create_tables(engine)
    insert_data(engine)
    run_queries(engine)
    print("\nDone!")

if __name__ == "__main__":
    main()