#!/bin/bash

# Executa comandos SQL no sqlite3
sqlite3 database.db <<EOF
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;
.read setup.sql
.mode csv
.import /Applications/my_Stuff/soccer_app/final_files/csvs/tabela_partidas.csv Matches
.import /Applications/my_Stuff/soccer_app/final_files/csvs/tabela_jogadores.csv Players
EOF

