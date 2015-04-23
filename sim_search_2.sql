CREATE EXTENSION pg_trgm;

SELECT similarity('berlium', 'beryllium');

SELECT similarity('berlylium', 'beryllium');

SELECT similarity('sdium', 'sodium');

CREATE MATERIALIZED VIEW unique_lexeme AS 
SELECT word FROM ts_stat('SELECT atomic_number, symbol, element, name, period_number  FROM (SELECT atomic_number, symbol, element, g.name, period_number,
	to_tsvector(CAST(atomic_number AS VARCHAR)|| 
			  to_tsvector(element)|| 
	  to_tsvector('simple', symbol)||
    to_tsvector(CAST(period_number AS VARCHAR)) || 
    to_tsvector(CAST(column_number AS VARCHAR)) || 
                to_tsvector(phase) || 
    to_tsvector('simple',most_stable_crystal) ||
    			 to_tsvector(type) || 
     to_tsvector(CAST(ionic_radius AS VARCHAR)) || 
    to_tsvector(CAST(atomic_radius AS VARCHAR)) || 
to_tsvector(CAST(electronegativity AS VARCHAR)) || 
to_tsvector(CAST(first_ionization_potential AS VARCHAR)) || 
		  to_tsvector(CAST(density AS VARCHAR)) ||
  to_tsvector(CAST(melting_point_k AS VARCHAR)) || 
  to_tsvector(CAST(boiling_point_k AS VARCHAR)) || 
         to_tsvector(CAST(isotopes AS VARCHAR)) || 
         	to_tsvector(CAST(year_of_discovery AS VARCHAR)) || 
to_tsvector(CAST(specific_heat_capacity AS VARCHAR)) || 
to_tsvector(CAST(electron_configuration AS VARCHAR)) ||
to_tsvector(discoverer) ||
to_tsvector(elements.description)
	as document from elements
	JOIN groups g ON elements.column_number = g.group_number');
 
 REFRESH MATERIALIZED VIEW unique_lexeme;

SELECT word from unique_lexeme
WHERE similarity(word, '34')>=0.4
ORDER BY word <-> '34'
LIMIT 3;
