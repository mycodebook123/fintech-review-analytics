"""
Script: theme_analysis.py
Purpose: Extract themes/topics from reviews using TF-IDF keyword analysis
         and rule-based theme assignment.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Define theme keywords
THEMES = {
    "Transaction & Transfers": ["transfer", "transaction", "send", "money", "payment", "pay", "deposit"],
    "Login & Authentication": ["login", "otp", "password", "fingerprint", "register", "sign", "access"],
    "App Performance": ["crash", "slow", "freeze", "load", "error", "bug", "update", "stable", "speed"],
    "UI & Design": ["interface", "design", "ui", "layout", "easy", "navigate", "simple", "clean", "dark"],
    "Customer Support": ["support", "customer", "service", "help", "response", "agent", "call", "contact"],
    "Features & Functionality": ["feature", "balance", "statement", "bill", "notification", "limit", "account"],
}

def assign_theme(review_text):
    text = str(review_text).lower()
    for theme, keywords in THEMES.items():
        if any(kw in text for kw in keywords):
            return theme
    return "General"

def run_theme_analysis(input_path="data/raw/reviews_with_sentiment.csv",
                       output_path="data/raw/reviews_with_themes.csv"):

    print("Loading reviews...")
    df = pd.read_csv(input_path)

    print("Assigning themes...")
    df["theme"] = df["review"].apply(assign_theme)

    print("\nTheme distribution:")
    print(df["theme"].value_counts())

    print("\nThemes by bank:")
    print(df.groupby(["bank", "theme"]).size().unstack(fill_value=0))

    print("\nTop TF-IDF keywords per bank:")
    for bank in df["bank"].unique():
        bank_reviews = df[df["bank"] == bank]["review"].astype(str).tolist()
        vectorizer = TfidfVectorizer(max_features=10, stop_words="english")
        try:
            vectorizer.fit_transform(bank_reviews)
            keywords = vectorizer.get_feature_names_out()
            print(f"  {bank}: {', '.join(keywords)}")
        except Exception as e:
            print(f"  {bank}: could not extract keywords ({e})")

    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")
    return df

if __name__ == "__main__":
    run_theme_analysis()