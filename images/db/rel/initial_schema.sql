CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;




create table competition
(
    id_comp uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name    varchar
);

create table game
(
    id_game    uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_home_team uuid
        constraint game_teams_id_team_fk
            references teams,
    id_away_team uuid
        constraint game_teams_id_team_fk_2
            references teams,
    gh           integer,
    ga           integer,
    date         date,
    id_comp      uuid
        constraint game_competition_id_comp_fk
            references competition
);


create table teams
(
    id_team   uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_team    varchar,
    country_team varchar,
    geo GEOMETRY
);

alter table teams
    owner to is;



alter table game
    owner to is;



alter table competition
    owner to is;

