--Search function attempts

--Proof of concept
--SELECT to_tsvector('Here we go. Test 1,2,3');
--SELECT to_tsvector('He, Helium, F fluorine K potssum impossible yoda it isS He');
--SELECT atomic_number, symbol, element FROM (SELECT atomic_number, symbol, element, to_tsvector('simple',symbol) as document from elements) p_search
--WHERE p_search.document @@ to_tsvector('he');


CREATE MATERIALIZED VIEW unique_lexeme AS
SELECT word FROM ts_stat('SELECT 
	setweight(to_tsvector(CAST(atomic_number AS VARCHAR)),''A'') || 
			  setweight(to_tsvector(element), ''A'' )|| 
	  setweight(to_tsvector(''simple'', symbol), ''A'')||
    setweight(to_tsvector(CAST(period_number AS VARCHAR)), ''D'') || 
    setweight(to_tsvector(CAST(column_number AS VARCHAR)), ''D'') || 
                setweight(to_tsvector(phase), ''C'') || 
    setweight(to_tsvector(''simple'',most_stable_crystal),''C'') ||
    			 setweight(to_tsvector(type), ''C'') || 
     setweight(to_tsvector(CAST(ionic_radius AS VARCHAR)), ''D'') || 
    setweight(to_tsvector(CAST(atomic_radius AS VARCHAR)), ''C'') || 
setweight(to_tsvector(CAST(electronegativity AS VARCHAR)), ''C'') || 
setweight(to_tsvector(CAST(first_ionization_potential AS VARCHAR)), ''C'') || 
		  setweight(to_tsvector(CAST(density AS VARCHAR)), ''C'') ||
  setweight(to_tsvector(CAST(melting_point_k AS VARCHAR)), ''C'') || 
  setweight(to_tsvector(CAST(boiling_point_k AS VARCHAR)), ''C'') || 
         setweight(to_tsvector(CAST(isotopes AS VARCHAR)), ''C'') || 
         	setweight(to_tsvector(CAST(year_of_discovery AS VARCHAR)), ''B'') || 
setweight(to_tsvector(CAST(specific_heat_capacity AS VARCHAR)), ''B'') || 
setweight(to_tsvector(CAST(electron_configuration AS VARCHAR)), ''C'') ||
setweight(to_tsvector(discoverer), ''A'')
	as document from elements');

CREATE INDEX words_idx ON search_words USING gin(word gin_trgm_ops);
REFRESH MATERIALIZED VIEW unique_lexeme;

SELECT word WHERE similarity(word, '1980') > 0.5
ORDER BY word <-> '1980'
LIMIT 10;

SELECT atomic_number, symbol, element FROM (SELECT atomic_number, symbol, element, 
	setweight(to_tsvector(CAST(atomic_number AS VARCHAR)),'A') || 
	setweight(to_tsvector('atomic number'), 'A') ||
			  setweight(to_tsvector(element), 'A' )|| 
	  setweight(to_tsvector('simple', symbol), 'A')||
    setweight(to_tsvector(CAST(period_number AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(column_number AS VARCHAR)), 'D') || 
                setweight(to_tsvector(phase), 'C') || 
    setweight(to_tsvector('simple',most_stable_crystal),'C') ||
    			 setweight(to_tsvector(type), 'C') || 
     setweight(to_tsvector(CAST(ionic_radius AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(atomic_radius AS VARCHAR)), 'C') || 
setweight(to_tsvector(CAST(electronegativity AS VARCHAR)), 'C') || 
setweight(to_tsvector(CAST(first_ionization_potential AS VARCHAR)), 'C') || 
		  setweight(to_tsvector(CAST(density AS VARCHAR)), 'C') ||
  setweight(to_tsvector(CAST(melting_point_k AS VARCHAR)), 'C') || 
  setweight(to_tsvector(CAST(boiling_point_k AS VARCHAR)), 'C') || 
         setweight(to_tsvector(CAST(isotopes AS VARCHAR)), 'C') || 
         	setweight(to_tsvector(CAST(year_of_discovery AS VARCHAR)), 'B') || 
setweight(to_tsvector(CAST(specific_heat_capacity AS VARCHAR)), 'B') || 
setweight(to_tsvector(CAST(electron_configuration AS VARCHAR)), 'C') ||
setweight(to_tsvector(discoverer), 'A')
	as document from elements) p_search
	WHERE p_search.document @@ to_tsquery('4')
	ORDER BY ts_rank(p_search.document, to_tsquery('atomic & 4')) DESC;

SELECT atomic_number, symbol, element FROM (SELECT atomic_number, symbol, element, 
	setweight(to_tsvector(CAST(atomic_number AS VARCHAR)),'A') || 
			  setweight(to_tsvector(element), 'A' )|| 
	  setweight(to_tsvector('simple', symbol), 'A')||
    setweight(to_tsvector(CAST(period_number AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(column_number AS VARCHAR)), 'D') || 
                setweight(to_tsvector(phase), 'C') || 
    setweight(to_tsvector('simple',most_stable_crystal),'C') ||
    			 setweight(to_tsvector(type), 'C') || 
     setweight(to_tsvector(CAST(ionic_radius AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(atomic_radius AS VARCHAR)), 'C') || 
setweight(to_tsvector(CAST(electronegativity AS VARCHAR)), 'C') || 
setweight(to_tsvector(CAST(first_ionization_potential AS VARCHAR)), 'C') || 
		  setweight(to_tsvector(CAST(density AS VARCHAR)), 'C') ||
  setweight(to_tsvector(CAST(melting_point_k AS VARCHAR)), 'C') || 
  setweight(to_tsvector(CAST(boiling_point_k AS VARCHAR)), 'C') || 
         setweight(to_tsvector(CAST(isotopes AS VARCHAR)), 'C') || 
         	setweight(to_tsvector(CAST(year_of_discovery AS VARCHAR)), 'B') || 
setweight(to_tsvector(CAST(specific_heat_capacity AS VARCHAR)), 'B') || 
setweight(to_tsvector(CAST(electron_configuration AS VARCHAR)), 'C') ||
setweight(to_tsvector(discoverer), 'A') 
	as document from elements) p_search
	WHERE p_search.document @@ to_tsquery('del & Rio')
	ORDER BY ts_rank(p_search.document, to_tsquery('del & Rio')) DESC;

	SELECT atomic_number, symbol, element FROM (SELECT atomic_number, symbol, element, 
	setweight(to_tsvector(CAST(atomic_number AS VARCHAR)),'A') || 
			  setweight(to_tsvector(element), 'A' )|| 
	  setweight(to_tsvector('simple', symbol), 'A')||
    setweight(to_tsvector(CAST(period_number AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(column_number AS VARCHAR)), 'D') || 
                setweight(to_tsvector(phase), 'C') || 
    setweight(to_tsvector('simple',most_stable_crystal),'C') ||
    			 setweight(to_tsvector(type), 'C') || 
     setweight(to_tsvector(CAST(ionic_radius AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(atomic_radius AS VARCHAR)), 'C') || 
setweight(to_tsvector(CAST(electronegativity AS VARCHAR)), 'C') || 
setweight(to_tsvector(CAST(first_ionization_potential AS VARCHAR)), 'C') || 
		  setweight(to_tsvector(CAST(density AS VARCHAR)), 'C') ||
  setweight(to_tsvector(CAST(melting_point_k AS VARCHAR)), 'C') || 
  setweight(to_tsvector(CAST(boiling_point_k AS VARCHAR)), 'C') || 
         setweight(to_tsvector(CAST(isotopes AS VARCHAR)), 'C') || 
         	setweight(to_tsvector(CAST(year_of_discovery AS VARCHAR)), 'A') || 
setweight(to_tsvector(CAST(specific_heat_capacity AS VARCHAR)), 'B') || 
setweight(to_tsvector(CAST(electron_configuration AS VARCHAR)), 'C') ||
setweight(to_tsvector(discoverer), 'A') 
	as document from elements) p_search
	WHERE p_search.document @@ to_tsquery('1801')
	ORDER BY ts_rank(p_search.document, to_tsquery('1801')) DESC;
--Attempting a search in the system
--SELECT atomic_number, symbol, element FROM (SELECT atomic_number, symbol, element, to_tsvector('simple',symbol) as document from elements) p_search
--WHERE p_search.document @@ 'He';

--SELECT to_tsvector(CAST(e.atomic_number AS VARCHAR)) || to_tsvector(e.element) || to_tsvector('simple',e.symbol)
	--as document
	--from elements e
	--group by atomic_number @@ to_tsquery('Tungsten');

--SELECT to_tsvector(CAST(e.atomic_number AS VARCHAR)) || to_tsvector(e.element) || to_tsvector('simple',e.symbol)
	--as document
	--from elements e
	--group by atomic_number @@ to_tsquery('56');
