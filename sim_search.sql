CREATE EXTENSION pg_trgm;

SELECT similarity('berlium', 'beryllium');

SELECT similarity('berlylium', 'beryllium');

SELECT similarity('sdium', 'sodium');

CREATE MATERIALIZED VIEW unique_lexeme AS 
SELECT word FROM ts_stat('SELECT to_tsvector('simple', elements.element)
FROM elements');
 
 REFRESH MATERIALIZED VIEW unique_lexeme;

SELECT word from unique_lexeme
WHERE similarity(word, 'berlium')>=0.4
ORDER BY word <-> 'beryllium'
LIMIT 3;

