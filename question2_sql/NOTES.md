# Question 2 — Verification notes

The PDF asks:
1. How many types of Acacia plants are in `taxonomy`?
2. Which type of wheat has the longest DNA sequence, using `rfamseq` and `taxonomy`?
3. Paginate families whose maximum DNA sequence length exceeds 1,000,000; descending length; return accession, name, and maximum length; page 9 at 15 rows/page.

## Do not submit unverified query assumptions

Before relying on `answers.sql`, inspect the actual Rfam schema. Confirm:
- the scientific-name field and taxonomy key in `taxonomy`;
- the sequence identifier and sequence-length representation in `rfamseq`;
- the relationship between families, regions, and sequences;
- whether the database supports `LENGTH(seq)` or has a dedicated sequence-length column.

If sequence length is stored as a numeric column, use that column instead of `LENGTH(seq)`. If the schema uses different joins, adapt the query and explain why.

## Pagination calculation

Page 9 starts after 8 full pages:
`(9 - 1) * 15 = 120`, so use `LIMIT 15 OFFSET 120` for MySQL/MariaDB.

## Record verified outputs here before submission

- Acacia count: TODO — run query against the actual database.
- Wheat type: TODO — run query against the actual database.
- Pagination query tested: TODO — record database/version and result.
