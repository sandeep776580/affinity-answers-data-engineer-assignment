# Affinity Answers — Data Engineer Intern Take-Home

This repository organizes the three questions from the take-home assignment.

## Project structure

- `question1_python/`: product search scraper for MD Computers
- `question2_sql/`: SQL answers and query notes for the Rfam database
- `question3_shell/`: company CSV processing script
- `requirements.txt`: Python dependencies

> Important: This is a working starter implementation, not a claim that the live target website/database has been verified in this environment. Run every test yourself, inspect the output, and be prepared to explain the code. The assignment explicitly asks you not to submit code you have not run and understood.

## Requirements

- Python 3.10+
- `pip`
- Git
- For Question 3: Git Bash, WSL, Linux, or macOS shell. The script uses `curl`, `python3`, and standard shell utilities.
- For Question 2: access to the Rfam database or a compatible MySQL/MariaDB client to verify query results.

## Setup

From the repository root:

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Git Bash / macOS / Linux:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Question 1 — Python scraper

Run:
```bash
python question1_python/scrape_products.py
```
Enter a product search term, for example `external harddrive`.

The scraper requests the search page and extracts product-card text using common HTML selectors. E-commerce pages sometimes change their HTML or block automated requests; if no products are found, inspect the saved/returned HTML and adjust selectors rather than assuming the site has no results. Respect the site's terms and robots policy; do not send rapid repeated requests.

## Question 2 — SQL

See `question2_sql/answers.sql` and `question2_sql/NOTES.md`.

The assignment references Rfam's public database documentation. Confirm the database engine/version and actual table/column names before running. The two taxonomy questions require querying the live database; do not invent result counts or species names.

For pagination, page 9 with 15 results per page uses an offset of `(9 - 1) * 15 = 120`.

## Question 3 — shell script

Run from Git Bash, WSL, Linux, or macOS:
```bash
bash question3_shell/company_report.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
```

The script downloads the CSV and uses Python's CSV parser to handle quoted fields safely, then sorts by founding year. Companies with missing or non-numeric founding years are placed at the end.

## Before submitting

1. Run Question 1 with at least two different search terms and capture the output.
2. Verify all SQL column names and execute the queries against Rfam. Record the real answers for questions 1 and 2.
3. Run Question 3 and check that rows are sorted by founding year.
4. Add your own brief explanations in `question2_sql/NOTES.md` and here in this README.
5. Record a screen video showing each program/query being run and explain what it does.
6. Push the repository to GitHub and share the repository URL with the recruiter.
