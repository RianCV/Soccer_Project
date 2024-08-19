CREATE TABLE Players (
    Team TEXT NOT NULL,
    Name TEXT NOT NULL,
    Position TEXT NOT NULL,
    Matches_played FLOAT NOT NULL,
    Minutes_played FLOAT NOT NULL,
    Goals FLOAT NOT NULL,
    Assists FLOAT NOT NULL,
    Penalty_kicks_made FLOAT NOT NULL,
    Yellow_cards FLOAT NOT NULL,
    Red_cards FLOAT NOT NULL,
    xG FLOAT NOT NULL,
    npxG FLOAT NOT NULL,
    xAG FLOAT NOT NULL
);

CREATE TABLE Matches (
    Team TEXT NOT NULL,
    Matchweek TEXT NOT NULL,
    Status TEXT NOT NULL,
    Venue TEXT NOT NULL,
    Result TEXT NOT NULL,
    Goals_for FLOAT NOT NULL,
    Goals_against FLOAT NOT NULL,
    xG FLOAT NOT NULL,
    xGA FLOAT NOT NULL
);
