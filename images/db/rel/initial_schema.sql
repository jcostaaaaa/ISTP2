create table competition
(
    id_comp bigserial
        constraint competition_pk
            primary key,
    name    varchar
);

alter table competition
    owner to is;






create table game
(
    id_game      bigserial
        constraint game_pk
            primary key,
    id_home_team bigint
        constraint game_teams_id_team_fk
            references teams,
    id_away_team bigint
        constraint game_teams_id_team_fk_2
            references teams,
    gh           integer,
    ga           integer,
    date         date,
    id_comp      bigint
        constraint game_competition_id_comp_fk
            references competition
);

alter table game
    owner to is;





create table teams
(
    id_team      bigserial
        constraint teams_pk
            primary key,
    name_team    varchar,
    country_team varchar,
    latitude     bigint,
    longitude    bigint
);

alter table teams
    owner to is;



