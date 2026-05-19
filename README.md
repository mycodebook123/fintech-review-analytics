# Fintech Review Analytics

A data engineering and NLP pipeline that scrapes, analyzes, and visualizes Google Play Store reviews for three Ethiopian banks: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

## Project Structure

- `data/raw/` — raw scraped review data (not committed to GitHub)
- `notebooks/` — Jupyter notebooks for analysis
- `src/` — source code modules
- `scripts/` — standalone scripts for scraping, analysis, and DB insertion
- `tests/` — unit tests

## Setup

```bash
pip install -r requirements.txt
```

## Scraping Methodology

Reviews were scraped using the `google-play-scraper` Python library. A minimum of 400 reviews per bank (1,200 total) were collected covering the maximum available date range. Fields collected: review text, rating (1–5), date, bank name, source.

## Banks Analyzed

| Bank                        | App Name           |
| --------------------------- | ------------------ |
| Commercial Bank of Ethiopia | CBE Birr           |
| Bank of Abyssinia           | BOA Mobile Banking |
| Dashen Bank                 | Dashen Bank Mobile |

## Limitations

- Google Play scraper may be rate-limited; extended date ranges were used where needed.
- Reviews are in English only; Amharic reviews were excluded.
- Sampling bias: users are more likely to review after negative experiences.
