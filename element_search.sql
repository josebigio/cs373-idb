
SELECT atomic_number, symbol, element, period_number, column_number, phase, most_stable_crystal, type, ionic_radius, electronegativity, first_ionization_potential, density, melting_point_k,
 boiling_point_k, isotopes, year_of_discovery, specific_heat_capacity, electron_configuration, discoverer FROM (SELECT atomic_number, symbol, element, period_number, column_number, phase, most_stable_crystal, type, ionic_radius, electronegativity, first_ionization_potential, density, melting_point_k,
 boiling_point_k, isotopes, year_of_discovery, specific_heat_capacity, electron_configuration, discoverer,
	setweight(to_tsvector(CAST(atomic_number AS VARCHAR)),'A') || 
			  setweight(to_tsvector(element), 'A' )|| 
	  setweight(to_tsvector('simple', symbol), 'A')||
    setweight(to_tsvector(CAST(period_number AS VARCHAR)), 'D') || 
    setweight(to_tsvector(CAST(column_number AS VARCHAR)), 'D') || 
              setweight(to_tsvector(coalesce(string_agg(CAST(phase AS VARCHAR), ' '),'')), 'C') || 
    setweight(to_tsvector('simple',coalesce(string_agg(CAST(most_stable_crystal AS VARCHAR), ' '), '')),'C') ||
    			 setweight(to_tsvector('simple',coalesce(string_agg(CAST(type AS VARCHAR), ' '), '')), 'C') || 
     setweight(to_tsvector('simple',coalesce(string_agg(CAST(ionic_radius AS VARCHAR), ' '), '')), 'D') || 
    setweight(to_tsvector('simple',coalesce(string_agg(CAST(atomic_radius AS VARCHAR), ' '), '')), 'C') || 
setweight(to_tsvector('simple',coalesce(string_agg(CAST(electronegativity AS VARCHAR), ' '), '')), 'C') || 
setweight(to_tsvector('simple',coalesce(string_agg(CAST(first_ionization_potential AS VARCHAR), ' '), '')), 'C') || 
		  setweight(to_tsvector(coalesce(string_agg(CAST(density AS VARCHAR), ' '), '')), 'C') ||
  setweight(to_tsvector('simple', coalesce(string_agg(CAST(melting_point_k AS VARCHAR), ' '), '')), 'C') || 
  setweight(to_tsvector('simple', coalesce(string_agg(CAST(boiling_point_k AS VARCHAR), ' '), '')), 'C') || 
        setweight(to_tsvector('simple', coalesce(string_agg(CAST(isotopes AS VARCHAR), ' '), '')), 'C') || 
         setweight(to_tsvector('simple', coalesce(string_agg(CAST(year_of_discovery AS VARCHAR), ' '), '')), 'B') || 
setweight(to_tsvector('simple', coalesce(string_agg(CAST(specific_heat_capacity AS VARCHAR), ' '), '')), 'B') || 
setweight(to_tsvector('simple',coalesce(string_agg(CAST(electron_configuration AS VARCHAR), ' '), '')), 'C') ||
setweight(to_tsvector('simple', coalesce(string_agg(discoverer, ' '), '')), 'A')  
	as document from elements
  group by atomic_number) p
	WHERE p.document @@ to_tsquery('Helium')
	ORDER BY ts_rank(p.document, to_tsquery('Helium')) DESC;


