
-- Affinity Answers Data Engineer Intern Assignment
-- Database: Rfam (MySQL)

-- ============================================================
-- QUESTION 1: Count Acacia taxa in the taxonomy table.
-- ============================================================

SELECT COUNT(*) AS acacia_taxa_count
FROM taxonomy
WHERE species LIKE 'Acacia %';


-- ============================================================
-- QUESTION 2: Find the wheat type with the longest sequence.
-- ============================================================

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


-- ============================================================
-- QUESTION 3: Return page 9 of families whose maximum DNA
-- sequence length exceeds 1,000,000.
-- Page size: 15
-- Offset: (9 - 1) * 15 = 120
-- ============================================================

SELECT
    f.rfam_acc AS family_accession,
    f.rfam_id AS family_name,
    MAX(rs.length) AS max_sequence_length
FROM rfamseq AS rs
JOIN full_region AS fr
    ON fr.rfamseq_acc = rs.rfamseq_acc
JOIN family AS f
    ON f.rfam_acc = fr.rfam_acc
WHERE rs.length > 1000000
GROUP BY
    f.rfam_acc,
    f.rfam_id
ORDER BY
    max_sequence_length DESC,
    family_accession ASC
LIMIT 15 OFFSET 120;
