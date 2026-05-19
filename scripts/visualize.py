"""
Script: visualize.py
Purpose: Generate visualizations for sentiment and theme analysis results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import os

os.makedirs("data/visualizations", exist_ok=True)

df = pd.read_csv("data/raw/reviews_with_themes.csv")

# ── Plot 1: Sentiment distribution per bank ──────────────────────────────────
sentiment_counts = df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10, 6))
sentiment_counts.plot(kind="bar", ax=ax, color=["#e74c3c", "#95a5a6", "#2ecc71"])
ax.set_title("Sentiment Distribution by Bank", fontsize=14, fontweight="bold")
ax.set_xlabel("Bank")
ax.set_ylabel("Number of Reviews")
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right")
ax.legend(title="Sentiment")
plt.tight_layout()
plt.savefig("data/visualizations/sentiment_by_bank.png", dpi=150)
plt.close()
print("Saved: sentiment_by_bank.png")

# ── Plot 2: Average rating per bank ──────────────────────────────────────────
avg_rating = df.groupby("bank")["rating"].mean().sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(avg_rating.index, avg_rating.values, color=["#3498db", "#e67e22", "#9b59b6"])
ax.set_title("Average Rating by Bank", fontsize=14, fontweight="bold")
ax.set_xlabel("Average Rating (1–5)")
ax.set_xlim(0, 5)
for bar, val in zip(bars, avg_rating.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
            f"{val:.2f}", va="center", fontsize=11)
plt.tight_layout()
plt.savefig("data/visualizations/avg_rating_by_bank.png", dpi=150)
plt.close()
print("Saved: avg_rating_by_bank.png")

# ── Plot 3: Theme distribution per bank ──────────────────────────────────────
theme_counts = df.groupby(["bank", "theme"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
theme_counts.plot(kind="bar", ax=ax)
ax.set_title("Review Themes by Bank", fontsize=14, fontweight="bold")
ax.set_xlabel("Bank")
ax.set_ylabel("Number of Reviews")
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right")
ax.legend(title="Theme", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig("data/visualizations/themes_by_bank.png", dpi=150)
plt.close()
print("Saved: themes_by_bank.png")

# ── Plot 4: Rating distribution (all banks combined) ─────────────────────────
rating_counts = df["rating"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(rating_counts.index, rating_counts.values,
       color=["#e74c3c","#e67e22","#f1c40f","#2ecc71","#27ae60"])
ax.set_title("Overall Rating Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Rating (Stars)")
ax.set_ylabel("Number of Reviews")
ax.set_xticks([1, 2, 3, 4, 5])
plt.tight_layout()
plt.savefig("data/visualizations/rating_distribution.png", dpi=150)
plt.close()
print("Saved: rating_distribution.png")

# ── Plot 5: Sentiment score over time (monthly) ───────────────────────────────
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby(["month", "bank"])["sentiment_score"].mean().unstack()

fig, ax = plt.subplots(figsize=(12, 5))
for bank in monthly.columns:
    ax.plot(monthly.index.astype(str), monthly[bank], marker="o", label=bank)
ax.set_title("Average Sentiment Score Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Avg Sentiment Score")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("data/visualizations/sentiment_over_time.png", dpi=150)
plt.close()
print("Saved: sentiment_over_time.png")

print("\nAll visualizations saved to data/visualizations/")