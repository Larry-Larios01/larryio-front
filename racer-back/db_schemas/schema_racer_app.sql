create  table users (
id uuid not null primary key,
name text
)

create  table competition (
id uuid not null primary key,
name text

),

create table competitionMaster (

	id_player uuid,
	id_competition uuid


)

ALTER TABLE competitionMaster
ADD CONSTRAINT fk_comp
FOREIGN KEY (id_competition)
REFERENCES competition (id)



