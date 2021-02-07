--PRAGMA table_info(doctor);
--PRAGMA foreign_key_list(doctor);
--SELECT * FROM data LEFT JOIN doctor ON data.doctor=doctor.doctor where doctor.institution = 'labo 1' ;
--PRAGMA table_info(doctor);

SELECT COUNT(compagny) FROM ds WHERE compagny='Compagny C';