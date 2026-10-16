
# Rfam SQL Queries — Notes

## Database connection

- Database: Rfam
- Engine: MySQL
- Host: mysql-rfam-public.ebi.ac.uk
- Port: 4497
- User: rfamro

## Query 1: Acacia taxa count

Counts taxonomy records whose species name begins with `Acacia `.

Verified result:

- Acacia taxa count: 326

## Query 2: Longest wheat sequence

Joins `rfamseq` with `taxonomy`, filters wheat-related species, and returns the species with the greatest sequence length.

Verified result:

- Wheat type: Triticum durum (durum wheat)
- Longest sequence length: 836514780

## Query 3: Paginated families

Returns 15 families for page 9, with a maximum sequence length greater than 1,000,000. Results are sorted by maximum sequence length in descending order, with accession as a tie-breaker.

- Page size: 15
- Page number: 9
- Offset: 120
- Minimum maximum sequence length: greater than 1,000,000

The query is included in `answers.sql`. Execution against the public Rfam server timed out, so its live results could not be verified. No result rows are claimed for this query.

## Run the queries

From the project root:

```powershell
python question2_sql/run_queries.py
```

The runner reports the results of successful queries and reports database errors when a query cannot complete.
