"""
Script: scrape_reviews.py
Purpose: Scrape Google Play Store reviews for three Ethiopian banks,
         clean the data, and save to CSV.

Note: Dashen Bank's app (com.dashenbank.mobilebanking) returned 0 reviews
via google-play-scraper, likely due to regional availability restrictions
or the app not being indexed in the scraper's data source. As per project
guidelines, we compensated by expanding the review count for CBE and BOA
to meet the 1,200 total minimum.
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import os

# ── App IDs from Google Play Store ──────────────────────────────────────────
APPS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia":           "com.boa.boaMobileBanking",
}

# Dashen Bank note - documented limitation
DASHEN_NOTE = """
Dashen Bank Scraping Limitation:
- App ID attempted: com.dashen.dashensmart, com.dashen.amolite, com.dashenbank.mobilebanking
- Result: 0 reviews returned by google-play-scraper
- Reason: App may not be indexed or available in scraper data source
- Resolution: Increased CBE and BOA review counts to 700 each to meet 1,200 total
"""

def scrape_bank(bank_name, app_id, count=700):
    """Scrape reviews for a single bank app."""
    print(f"\nScraping {bank_name} ...")
    result, _ = reviews(
        app_id,
        lang="en",
        country="et",
        sort=Sort.NEWEST,
        count=count,
    )
    df = pd.DataFrame(result)
    df["bank"]   = bank_name
    df["source"] = "Google Play"
    print(f"  → {len(df)} reviews collected")
    return df


def clean_reviews(df):
    """Clean and standardize the raw reviews dataframe."""
    df = df[["content", "score", "at", "bank", "source"]].copy()
    df.columns = ["review", "rating", "date", "bank", "source"]

    before = len(df)
    df.dropna(subset=["review", "rating"], inplace=True)
    print(f"  → Dropped {before - len(df)} rows with missing review/rating")

    before = len(df)
    df.drop_duplicates(subset=["review"], inplace=True)
    print(f"  → Removed {before - len(df)} duplicate reviews")

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)

    return df


def main():
    print(DASHEN_NOTE)

    all_reviews = []
    for bank_name, app_id in APPS.items():
        df = scrape_bank(bank_name, app_id, count=700)
        all_reviews.append(df)

    combined = pd.concat(all_reviews, ignore_index=True)
    print(f"\nTotal raw reviews collected: {len(combined)}")

    print("\nCleaning data...")
    cleaned = clean_reviews(combined)
    print(f"Total clean reviews: {len(cleaned)}")

    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/reviews.csv"
    cleaned.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")

    print("\nReviews per bank:")
    print(cleaned["bank"].value_counts())

    print("\nDate range:")
    print(f"  Earliest: {cleaned['date'].min()}")
    print(f"  Latest:   {cleaned['date'].max()}")

    print("\nRating distribution:")
    print(cleaned["rating"].value_counts().sort_index())


if __name__ == "__main__":
    main()