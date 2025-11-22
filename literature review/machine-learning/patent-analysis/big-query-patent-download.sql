SELECT
  pub.publication_number,
  -- Get the Title
  (SELECT text FROM UNNEST(title_localized) WHERE language = 'en' LIMIT 1) AS title,
  -- Get the Abstract
  (SELECT text FROM UNNEST(abstract_localized) WHERE language = 'en' LIMIT 1) AS abstract,
  pub.publication_date,
  pub.filing_date,
  pub.country_code,
  -- Get Assignee (Company/University)
  ARRAY_TO_STRING(ARRAY(SELECT name FROM UNNEST(assignee_harmonized)), '; ') AS assignees,
  -- Keep CPC codes
  ARRAY_TO_STRING(ARRAY(SELECT code FROM UNNEST(cpc)), ', ') AS cpc_codes

FROM
  `patents-public-data.patents.publications` AS pub

WHERE
  -- FILTER: ONLY PATENTS PUBLISHED ON OR AFTER JAN 1, 2010
  pub.publication_date >= 20100101

  -- 1. Ensure English text exists
  AND EXISTS (SELECT 1 FROM UNNEST(title_localized) WHERE language = 'en')
  AND EXISTS (SELECT 1 FROM UNNEST(abstract_localized) WHERE language = 'en')

  -- 2. BROAD SEARCH LOGIC (Title + Abstract)
  AND (
    EXISTS (
      SELECT 1 
      FROM UNNEST(title_localized) AS t, UNNEST(abstract_localized) AS a
      WHERE t.language = 'en' AND a.language = 'en'
      
      -- CONDITION A: Organism
      AND REGEXP_CONTAINS(LOWER(CONCAT(t.text, ' ', a.text)), r'microalgae|algae|cyanobacteria|phytoplankton|seaweed')
      
      -- AND
      
      -- CONDITION B: Topic
      AND REGEXP_CONTAINS(LOWER(CONCAT(t.text, ' ', a.text)), r'biofuel|biodiesel|ethanol|biomass|lipid|cultivation|harvesting|photobioreactor|raceway pond|culture')
    )
  )