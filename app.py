import pandas as pd
import scrap
import json
import time


###########
########### FALTA FAZER A REPARTICAO DE DUAS TABELAS CSV, UMA PARA JOGADORES E OUTRA PARA OS JOGOS
###########
def create_player_table(table):
    players_table = table[table["Position"].notna()]
    players_table = players_table.drop(columns=['Venue', 'Status', 'Result', 'Goals_for', 'Goals_against', 'xGA'])
    return players_table

def create_matches_table(table):
    matches_table = table[table["Position"].isna()]
    matches_table = matches_table.rename(columns={'Player': 'Matchweek'})
    matches_table = matches_table.drop(columns=['Position', 'Matches_played', 'Minutes_played', 'Goals', 'Assists', 'Penalty_kicks_made', 'Yellow_cards', 'Red_cards', 'npxG', 'xAG'])
    matches_table = matches_table[['Team','Name','Status','Venue', 'Result', 'Goals_for', 'Goals_against','xG','xGA']]
    matches_table = matches_table.rename(columns={'Name': 'Matchweek'})
    return matches_table

def start_scrap(input):
    if(input == 1):
        teams = scrap.get_teams()
        for team in teams.keys():
            try:
                teams[team] = {'Players' : scrap.scrap_players(team), 'Matches': scrap.scrap_matches(team)}
                print(f'{team} data recieved')
            except Exception as e:
                print(f'WARNING --------      {team} gave an error ({e})     ----------- WARNING')
                time.sleep(10)
                continue
            time.sleep(10)
        with open("clubs_and_players.json", "w") as fp:
            json.dump(teams, fp)
        with open("clubs_and_players.txt", "w") as fp:
            json.dump(teams, fp)
        return "Arquivo carregado"
    elif(input == 0):
        try:
            with open("clubs_and_players.txt", "r") as fp:
                final_file = json.load(fp)
                records = []
                for team, rest in final_file.items(): #will have to change the code abaixo cause I added a dictionary player
                    for i,j in rest.items():
                        for player, stats in j.items():
                            record = {'Team': team, 'Name' : player}
                            record.update(stats)
                            records.append(record)
                df = pd.DataFrame(records)
                df.to_csv("./final_files/csvs/tabela.csv", index=False)
                df_player = create_player_table(df)
                df_matches = create_matches_table(df)
                df_player.to_csv("./final_files/csvs/tabela_jogadores.csv", index=False)
                df_matches.to_csv("./final_files/csvs/tabela_partidas.csv", index=False)
                print("THE DATA HAS BEEN SAVED IN YOUR FILES")
                return final_file
        except FileNotFoundError:
            return "Não há arquivo para ser lido"
    return "Not a valid answer"

question = f'///////////////   S E L E C T I O N    ////////////////\n            1  ->  WILL SCRAP ALL DATA FROM INTERNET\n            0  ->  WILL CREATE TABLES\n            9  ->  WILL END THE PROGRAM :       '

while(True):
    terminal_answer = int(input(question))
    if(terminal_answer == 9):
        print("SYSTEM ENDED! THANK YOU FOR YOUR EXPERIENCE")
        break
    clubs = start_scrap(terminal_answer)
    print()
    print()