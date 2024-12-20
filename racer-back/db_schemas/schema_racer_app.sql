create  table users (
id uuid not null primary key,
name text
)

create  table competition (
id uuid not null primary key,
name text

),

create table competition_master (

	id_player uuid,
	id_competition uuid


)

ALTER TABLE competitionMaster
ADD CONSTRAINT fk_comp
FOREIGN KEY (id_competition)
REFERENCES competition (id)

ALTER TABLE competitionMaster RENAME TO competition_master;


select * from competition 

select * from competitionmaster c 

 SELECT u."id",u."name",
           COUNT(CASE WHEN place = 1 THEN 1 END) AS first_place,
           COUNT(CASE WHEN place = 2 THEN 1 END) AS second_place,
           COUNT(CASE WHEN place = 3 THEN 1 END) AS third_place
    FROM competitionMaster c
    INNER JOIN users u ON u.id = c.id_player
    GROUP BY u."name", u."id";

UPDATE competition
SET laps = 1
WHERE laps IS NULL;

ALTER TABLE competition 
ADD COLUMN laps INT;


delete
from competition c
where c.id = '33944477-d608-4058-80a8-e97ab698aadc'


SELECT * FROM users WHERE id = 'fb2e136e-2b17-4fa2-8a52-2c6d073c04f9'