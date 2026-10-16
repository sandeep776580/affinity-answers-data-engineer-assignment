
-- Affinity Answers Data Engineer Intern Assignment
-- Database: Rfam (MySQL)

-- QUESTION 1: Count Acacia taxa.

SELECT COUNT(*) AS acacia_taxa_count
FROM taxonomy
WHERE species LIKE 'Acacia %';


-- QUESTION 2: Find the wheat type with the longest sequence.

SELECT
    t.species AS wheat_type,
    MAX(rs.length) AS longest_sequence_length
FROM rfamseq AS rs
JOIN taxonomy AS t
    ON rs.ncbi_id = t.ncbi_id
WHERE t.species LIKE '%Triticum%'
   OR t.species LIKE '%wheat%'
GROUP BY t.species
ORDER BY longest_sequence_length DESC
LIMIT 1;


-- QUESTION 3: Page 9, 15 families per page.
-- Maximum sequence length greater than 1,000,000.
-- Offset = (9 - 1) * 15 = 120.

SELECT
    f.rfam_acc AS family_accession,
    f.rfam_id AS family_name,
    MAX(rs.length) AS max_sequence_length
FROM family AS f
JOIN full_region AS fr
    ON fr.rfam_acc = f.rfam_acc
JOIN rfamseq AS rs
    ON rs.rfamseq_acc = fr.rfamseq_acc
GROUP BY
    f.rfam_acc,
    f.rfam_id
HAVING MAX(rs.length) > 1000000
ORDER BY
    max_sequence_length DESC,
    family_accession ASC
LIMIT 15 OFFSET 120;
