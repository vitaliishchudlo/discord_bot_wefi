import sqlite3

from data import config


def make_migrations():
    conn = sqlite3.connect(config.PATH_DATABASE)
    cur = conn.cursor()
    for migrate in migrates:
        cur.execute(migrate)
    conn.commit()
    conn.close()
    return True


migrates = (
    """
    create table achievement_users(
    id integer
        constraint achievement_users_pk
            primary key autoincrement,
    discord_id numeric not null,
    username varchar(50) not null);
    """,
    """
    create table achievement_games(
    id integer
        constraint achievement_games_pk
            primary key autoincrement,
    name varchar(50) not null,
    type varchar(50) not null);
    """,
    """
    create table achievement_statistics(
    id integer
        constraint achievement_statistics_pk
            primary key autoincrement,
    discord_id numeric not null,
    username varchar(50) not null,
    game varchar(50) not null,
    type varchar(50) not null,
    count numeric(11) not null);
    """,
    """
    create table registration_users(
    id integer
        constraint achievement_statistics_pk
            primary key autoincrement,
    discord_id numeric not null,
    username varchar(50) not null,
    captcha varchar(50) not null);
    """,
)

#     FOREIGN KEY (discord_id) REFERENCES achievement_users (discord_id),
#     FOREIGN KEY (username) REFERENCES achievement_users (username),
#     FOREIGN KEY (game) REFERENCES achievement_games (name));
