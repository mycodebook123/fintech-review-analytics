"""
Script: sentiment_analysis.py
Purpose: Run VADER sentiment analysis on scraped reviews,
         assign sentiment labels, and save enriched CSV.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os

def get_sentiment_label(compound_score):
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"

def run_sentiment(input_path="data/raw/reviews.csv",
                  output_path="data/raw/reviews_with_sentiment.csv"):

    print("Loading reviews...")
    df = pd.read_csv(input_path)
    print(f"  → {len(df)} reviews loaded")

    analyzer = SentimentIntensityAnalyzer()

    print("Running VADER sentiment analysis...")
    scores = df["review"].astype(str).apply(lambda x: analyzer.polarity_scores(x))
    df["sentiment_score"] = scores.apply(lambda x: x["compound"])
    df["sentiment_label"] = df["sentiment_score"].apply(get_sentiment_label)

    print("\nSentiment distribution:")
    print(df["sentiment_label"].value_counts())

    print("\nSentiment by bank:")
    print(df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")

    return df

if __name__ == "__main__":
    run_sentiment()