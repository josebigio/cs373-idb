--Search function attempts

--Proof of concept
--SELECT to_tsvector('Here we go. Test 1,2,3');
--SELECT to_tsvector('He, Helium, F fluorine K potssum impossible yoda it isS He');
--SELECT atomic_number, symbol, element FROM (SELECT atomic_number, symbol, element, to_tsvector('simple',symbol) as document from elements) p_search
--WHERE p_search.document @@ to_tsvector('he');


SELECT atomic_number, symbol, element, name, period_number  FROM (SELECT atomic_number, symbol, element, g.name, period_number,
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
setweight(to_tsvector(discoverer), 'A') ||
setweight(to_tsvector(elements.description), 'B')
    as document from elements
    JOIN groups g ON elements.column_number = g.group_number) p_search
    WHERE p_search.document @@ to_tsquery('Alali')
    ORDER BY ts_rank(p_search.document, to_tsquery('Alali')) DESC;