"""
Tests: test_analysis.py
Purpose: Unit tests for sentiment analysis and theme extraction functions.
"""

import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ── Import functions from scripts ────────────────────────────────────────────
from scripts.sentiment_analysis import get_sentiment_label
from scripts.theme_analysis import assign_theme


# ── Sentiment label tests ────────────────────────────────────────────────────
def test_positive_sentiment():
    assert get_sentiment_label(0.5) == "positive"

def test_negative_sentiment():
    assert get_sentiment_label(-0.5) == "negative"

def test_neutral_sentiment():
    assert get_sentiment_label(0.0) == "neutral"

def test_boundary_positive():
    assert get_sentiment_label(0.05) == "positive"

def test_boundary_negative():
    assert get_sentiment_label(-0.05) == "negative"

def test_boundary_neutral_low():
    assert get_sentiment_label(0.04) == "neutral"

# ── Theme assignment tests ────────────────────────────────────────────────────
def test_theme_transaction():
    assert assign_theme("I cannot complete my transfer") == "Transaction & Transfers"

def test_theme_login():
    assert assign_theme("OTP not received, cannot login") == "Login & Authentication"

def test_theme_performance():
    assert assign_theme("The app crashes every time") == "App Performance"

def test_theme_ui():
    assert assign_theme("The interface is clean and easy to navigate") == "UI & Design"

def test_theme_support():
    assert assign_theme("Customer support never responds") == "Customer Support"

def test_theme_general():
    assert assign_theme("This is a bank") == "General"

# ── VADER integration test ────────────────────────────────────────────────────
def test_vader_positive():
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores("This app is excellent and works perfectly")["compound"]
    assert score >= 0.05

def test_vader_negative():
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores("This app is terrible and always crashes")["compound"]
    assert score <= -0.05

# ── Data structure tests ──────────────────────────────────────────────────────
def test_reviews_csv_exists():
    assert os.path.exists("data/raw/reviews_with_themes.csv")

def test_reviews_csv_columns():
    df = pd.read_csv("data/raw/reviews_with_themes.csv")
    required = ["review", "rating", "date", "bank", "source", "sentiment_score", "sentiment_label", "theme"]
    for col in required:
        assert col in df.columns, f"Missing column: {col}"

def test_reviews_minimum_count():
    df = pd.read_csv("data/raw/reviews_with_themes.csv")
    assert len(df) >= 1000

def test_ratings_valid_range():
    df = pd.read_csv("data/raw/reviews_with_themes.csv")
    assert df["rating"].between(1, 5).all()