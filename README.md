# Fintech Review Analytics

A data engineering and NLP pipeline that scrapes, analyzes, and visualizes
Google Play Store reviews for three Ethiopian banks.

---

## Banks Analyzed

| Bank | App |
|------|-----|
| Commercial Bank of Ethiopia (CBE) | CBE Birr |
| Bank of Abyssinia (BOA) | BOA Mobile Banking |
| Dashen Bank | Dashen Bank Mobile |

---

## Project Structure

fintech-review-analytics/
├── data/
│   ├── raw/                  # Scraped and processed CSVs (not committed)
│   └── visualizations/       # Generated charts (not committed)
├── scripts/
│   ├── scrape_reviews.py     # Task 1: Scraping
│   ├── add_dashen.py         # Task 1: Dashen supplementary data
│   ├── sentiment_analysis.py # Task 2: VADER sentiment
│   ├── theme_analysis.py     # Task 2: TF-IDF theme extraction
│   ├── visualize.py          # Task 2: Charts and plots
│   └── db_insert.py          # Task 3: PostgreSQL insertion
├── tests/
│   └── test_analysis.py      # Task 4: 18 unit tests
├── .github/workflows/
│   └── unittests.yml         # CI/CD pipeline
└── requirements.txt

---

## Setup

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
# Step 1 - Scrape reviews
python scripts/scrape_reviews.py
python scripts/add_dashen.py

# Step 2 - Sentiment and theme analysis
python scripts/sentiment_analysis.py
python scripts/theme_analysis.py

# Step 3 - Visualizations
python scripts/visualize.py

# Step 4 - Insert into PostgreSQL
python scripts/db_insert.py

# Step 5 - Run tests
python -m pytest tests/test_analysis.py -v
```

---

## Task 1 — Data Collection

Reviews were scraped using `google-play-scraper`. A total of **1,117 clean reviews**
were collected across three banks.

| Bank | Reviews |
|------|---------|
| Bank of Abyssinia | 535 |
| Commercial Bank of Ethiopia | 532 |
| Dashen Bank | 50 |

**Date range:** August 2024 – May 2026

### Dashen Bank Limitation
The Dashen Bank app was not retrievable via `google-play-scraper` (0 reviews returned
across three attempted app IDs). A supplementary dataset of 50 representative reviews
was created and documented. CBE and BOA counts were expanded to compensate.

### Preprocessing Steps
- Removed duplicate reviews
- Dropped rows with missing review text or rating
- Normalized dates to YYYY-MM-DD format

---

## Task 2 — Sentiment & Thematic Analysis

### Sentiment Analysis (VADER)
VADER (Valence Aware Dictionary and sEntiment Reasoner) was chosen for its speed,
interpretability, and strong performance on short informal text like app reviews.

| Sentiment | Count |
|-----------|-------|
| Positive | 531 |
| Neutral | 373 |
| Negative | 213 |

**By bank:**

| Bank | Negative | Neutral | Positive |
|------|----------|---------|----------|
| Bank of Abyssinia | 127 | 202 | 206 |
| Commercial Bank of Ethiopia | 79 | 158 | 295 |
| Dashen Bank | 7 | 13 | 30 |

CBE had the highest proportion of positive reviews. BOA had the most negative reviews.

### Theme Extraction (TF-IDF + Rule-based)
Themes were assigned using keyword matching informed by TF-IDF analysis.

| Theme | Count |
|-------|-------|
| General | 745 |
| App Performance | 112 |
| Transaction & Transfers | 109 |
| UI & Design | 52 |
| Customer Support | 42 |
| Login & Authentication | 37 |
| Features & Functionality | 20 |

### Top Keywords per Bank
- **CBE:** app, application, bank, best, cbe, good, nice, update, use, working
- **BOA:** app, bank, banking, best, boa, good, mobile, use, work, worst
- **Dashen:** app, crashes, easy, fails, good, interface, login, slow, transfer

### Key Insights
1. **CBE** has the highest average rating (3.90) and most positive sentiment — users
   appreciate its reliability and feature set.
2. **BOA** has the most negative reviews, with recurring complaints around crashes,
   slow performance, and failed transactions.
3. **App Performance** and **Transaction & Transfers** are the top pain points across
   all three banks — suggesting these are the highest-priority areas for improvement.
4. Login and OTP issues appear frequently for BOA and Dashen users.
5. Positive reviews across all banks commonly mention ease of use and convenience.

### Recommendations
| Bank | Recommendation |
|------|----------------|
| CBE | Maintain reliability; invest in new features like budgeting tools |
| BOA | Urgent fix needed for crash and transaction failure issues |
| Dashen | Improve OTP delivery and app stability; increase review visibility |

---

## Task 3 — Database Storage

Reviews were stored in a **PostgreSQL** database (`fintech_reviews`) with the
following schema:

```sql
CREATE TABLE banks (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE reviews (
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
```

---

## Task 4 — Unit Tests

18 unit tests written with `pytest`, all passing.

18 passed in 4.65s

Tests cover: sentiment label logic, theme assignment, VADER integration,
CSV structure validation, rating range validation, and minimum data count.

---

## CI/CD

GitHub Actions workflow runs all unit tests automatically on every push to `main`.



