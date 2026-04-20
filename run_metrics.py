"""
metrics.py — Logging utilities for Morning News Summarizer.

Outputs per run:
  1. metrics.csv  — appended and committed back to the repo
  2. GitHub Actions Job Summary — written to $GITHUB_STEP_SUMMARY
"""

import csv
import os
import statistics
from datetime import datetime, timezone
from pathlib import Path

METRICS_FILE = Path(__file__).parent / "metrics.csv"

CSV_FIELDS = [
    "run_date",          # ISO-8601 UTC timestamp
    "status",            # SUCCESS | FAILED
    "scrapers_ok",       # number of scrapers that succeeded
    "scrapers_failed",   # number of scrapers that failed
    "articles_scraped",  # total articles attempted
    "articles_ok",       # articles successfully summarized
    "avg_compression",   # mean compression % across all articles (blank on full failure)
    "avg_rouge1",
    "avg_rouge2",
    "avg_rougeL",
]


# ── per-article accumulator ────────────────────────────────────────────────────

class RunMetrics:
    """Accumulate stats during a run, then flush to CSV + Job Summary."""

    def __init__(self):
        self.articles_scraped = 0
        self.articles_ok = 0
        self.compression_ratios: list[float] = []
        self.rouge1_scores: list[float] = []
        self.rouge2_scores: list[float] = []
        self.rougeL_scores: list[float] = []
        self.scrapers_ok = 0
        self.scrapers_failed = 0
        self.failed_scrapers: list[str] = []

    # ── call these from your scraper functions ─────────────────────────────────

    def record_article_attempt(self):
        self.articles_scraped += 1

    def record_article_success(
        self,
        original_words: int,
        summary_words: int,
        rouge_scores: dict,
    ):
        self.articles_ok += 1
        compression = round((1 - summary_words / original_words) * 100, 2)
        self.compression_ratios.append(compression)
        self.rouge1_scores.append(rouge_scores["rouge1"])
        self.rouge2_scores.append(rouge_scores["rouge2"])
        self.rougeL_scores.append(rouge_scores["rougeL"])

    def record_scraper_success(self):
        self.scrapers_ok += 1

    def record_scraper_failure(self, name: str):
        self.scrapers_failed += 1
        self.failed_scrapers.append(name)

    # ── derived values ─────────────────────────────────────────────────────────

    @property
    def status(self) -> str:
        return "FAILED" if self.scrapers_failed > 0 or self.articles_ok == 0 else "SUCCESS"

    def _mean_or_blank(self, values: list[float]) -> str:
        if not values:
            return ""
        return str(round(statistics.mean(values), 4))

    # ── flush ──────────────────────────────────────────────────────────────────

    def flush(self):
        """Write metrics to CSV and GitHub Actions Job Summary."""
        row = {
            "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": self.status,
            "scrapers_ok": self.scrapers_ok,
            "scrapers_failed": self.scrapers_failed,
            "articles_scraped": self.articles_scraped,
            "articles_ok": self.articles_ok,
            "avg_compression": self._mean_or_blank(self.compression_ratios),
            "avg_rouge1": self._mean_or_blank(self.rouge1_scores),
            "avg_rouge2": self._mean_or_blank(self.rouge2_scores),
            "avg_rougeL": self._mean_or_blank(self.rougeL_scores),
        }

        _write_csv(row)
        _write_job_summary(row, self.failed_scrapers)
        _print_summary(row, self.failed_scrapers)


# ── CSV ────────────────────────────────────────────────────────────────────────

def _write_csv(row: dict):
    file_exists = METRICS_FILE.exists()
    with METRICS_FILE.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    print(f"[metrics] Appended row to {METRICS_FILE}")


# ── GitHub Actions Job Summary ─────────────────────────────────────────────────

def _write_job_summary(row: dict, failed_scrapers: list[str]):
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return  # not running inside GitHub Actions

    status_emoji = "✅" if row["status"] == "SUCCESS" else "❌"
    failed_note = (
        f" — failed: {', '.join(failed_scrapers)}" if failed_scrapers else ""
    )

    lines = [
        f"## {status_emoji} Morning News Summarizer — {row['run_date']}",
        "",
        "| Metric | Value |",
        "| ------ | ----- |",
        f"| Status | **{row['status']}**{failed_note} |",
        f"| Scrapers OK / Failed | {row['scrapers_ok']} / {row['scrapers_failed']} |",
        f"| Articles scraped | {row['articles_scraped']} |",
        f"| Articles summarized | {row['articles_ok']} |",
        f"| Avg compression | {row['avg_compression'] or 'n/a'}{'%' if row['avg_compression'] else ''} |",
        f"| Avg ROUGE-1 | {row['avg_rouge1'] or 'n/a'} |",
        f"| Avg ROUGE-2 | {row['avg_rouge2'] or 'n/a'} |",
        f"| Avg ROUGE-L | {row['avg_rougeL'] or 'n/a'} |",
        "",
    ]

    with open(summary_file, "a") as f:
        f.write("\n".join(lines) + "\n")

    print("[metrics] Wrote GitHub Actions Job Summary.")


# ── local console summary ──────────────────────────────────────────────────────

def _print_summary(row: dict, failed_scrapers: list[str]):
    print("\n" + "=" * 48)
    print(f"  RUN COMPLETE — {row['status']}")
    print("=" * 48)
    print(f"  Scrapers  : {row['scrapers_ok']} ok, {row['scrapers_failed']} failed"
          + (f" ({', '.join(failed_scrapers)})" if failed_scrapers else ""))
    print(f"  Articles  : {row['articles_ok']}/{row['articles_scraped']} summarized")
    if row["avg_compression"]:
        print(f"  Compression: {row['avg_compression']}%")
        print(f"  ROUGE-1/2/L: {row['avg_rouge1']} / {row['avg_rouge2']} / {row['avg_rougeL']}")
    print("=" * 48 + "\n")