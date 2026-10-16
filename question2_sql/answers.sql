
-- Affinity Answers Data Engineer Intern - Question 2
-- Database: Rfam (MySQL 8)

-- Q1. Count Acacia taxa in the taxonomy table.
SELECT COUNT(*) AS acacia_taxa_count
FROM taxonomy
WHERE species LIKE 'Acacia %';


-- Q2. Find the wheat species with the longest source sequence.
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


-- Q3. Families with maximum source sequence length > 1,000,000.
-- Page 9, with 15 results per page: OFFSET = (9 - 1) * 15 = 120.
SELECT
    f.rfam_acc AS family_accession,
    f.rfam_id AS family_name,
    MAX(rs.length) AS max_sequence_length
FROM family AS f
JOIN full_region AS fr
    ON fr.rfam_acc = f.rfam_acc
JOIN rfamseq AS rs
    ON rs.rfamseq_acc = fr.rfamseq_acc
WHERE rs.length > 1000000
GROUP BY f.rfam_acc, f.rfam_id
ORDER BY max_sequence_length DESC, family_accession ASC
LIMIT 15 OFFSET 120;
