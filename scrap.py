import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

teams_urls = { #links should be refresh by the end of a competition (not every club has all-competitions page)
    # "Grêmio": "https://fbref.com/en/squads/d5ae3703/2024/c24/Gremio-Stats-Serie-A",
    # "Flamengo": "https://fbref.com/en/squads/639950ae/2024/c24/Flamengo-Stats-Serie-A",
    # "Botafogo": "https://fbref.com/en/squads/d9fdd9d9/2024/c24/Botafogo-RJ-Stats-Serie-A",
    # "Palmeiras": "https://fbref.com/en/squads/abdce579/2024/c24/Palmeiras-Stats-Serie-A",
    # "Fortaleza": "https://fbref.com/en/squads/a9d0ab0e/2024/c24/Fortaleza-Stats-Serie-A",
    # "Cruzeiro": "https://fbref.com/en/squads/03ff5eeb/2024/c24/Cruzeiro-Stats-Serie-A",
    # "São Paulo": "https://fbref.com/en/squads/5f232eb1/2024/c24/Sao-Paulo-Stats-Serie-A",
    # "Bahia": "https://fbref.com/en/squads/157b7fee/2024/c24/Bahia-Stats-Serie-A",
    # "Athletico Paranaense": "https://fbref.com/en/squads/2091c619/2024/c24/Athletico-Paranaense-Stats-Serie-A",
    # "Atlético Mineiro": "https://fbref.com/en/squads/422bb734/2024/c24/Atletico-Mineiro-Stats-Serie-A",
    # "Red Bull Bragantino": "https://fbref.com/en/squads/f98930d1/2024/c24/Red-Bull-Bragantino-Stats-Serie-A",
    # "Vasco": "https://fbref.com/en/squads/83f55dbe/2024/c24/Vasco-da-Gama-Stats-Serie-A",
    # "Criciúma": "https://fbref.com/en/squads/3f7595bb/2024/c24/Criciuma-Stats-Serie-A",
    # "Juventude": "https://fbref.com/en/squads/d081b697/2024/c24/Juventude-Stats-Serie-A",
    # "Internacional": "https://fbref.com/en/squads/6f7e1f03/2024/c24/Internacional-Stats-Serie-A",
    # "Corinthians": "https://fbref.com/en/squads/bf4acd28/2024/c24/Corinthians-Stats-Serie-A",
    # "Vitória": "https://fbref.com/en/squads/33f95fe0/2024/c24/Vitoria-Stats-Serie-A",
    # "Cuiabá": "https://fbref.com/en/squads/f0e6fb14/2024/c24/Cuiaba-Stats-Serie-A",
    "Fluminense": "https://fbref.com/en/squads/84d9701c/2024/c24/Fluminense-Stats-Serie-A",
    "Atlético Goianiense": "https://fbref.com/en/squads/32d508ca/2024/c24/Atletico-Goianiense-Stats-Serie-A"
}

def get_teams():
    teams = {}
    for i in teams_urls.keys():
        teams[i] = {}
    return teams

def get_players_stats(team_url):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = team_url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    tbody = pageSoup.find('tbody', class_=False)
    rows = tbody.find_all('tr', class_=False)

    players = {}

    for row in rows:

        player_name = row.find('a', class_=False).text
        if player_name in players:
        # Count how many players with the same name are already in the dictionary
            count = sum(1 for key in players.keys() if key.startswith(player_name))
            player_name = f"{player_name} ({count + 1})"

        stats = {}
        
        stats_list = row.find("td", class_='center')
        stats["Position"] = stats_list.text
        stats_list = row.find_all("td", class_="right")
        
        stats["Matches_played"] = float(stats_list[0].text) if (stats_list[0].text != "") else float(0)
        if((stats_list[2].text) != ""):
            if (stats_list[2].text.find(',') != -1):
                stats["Minutes_played"] = float((stats_list[2].text).replace(",","."))
            else:
                stats["Minutes_played"] = float(stats_list[2].text)
        else:
            stats["Minutes_played"] = 0
        stats["Goals"] = float(stats_list[4].text) if (stats_list[4].text != "") else float(0)
        stats["Assists"] = float(stats_list[5].text) if (stats_list[5].text != "") else float(0)
        stats["Penalty_kicks_made"] = float(stats_list[8].text) if (stats_list[8].text != "") else float(0)
        stats["Yellow_cards"] = float(stats_list[10].text) if (stats_list[10].text != "") else float(0)
        stats["Red_cards"] = float(stats_list[11].text) if (stats_list[11].text != "") else float(0)
        stats["xG"] = float(stats_list[12].text) if (stats_list[12].text != "") else float(0)
        stats["npxG"] = float(stats_list[13].text) if (stats_list[13].text != "") else float(0)
        stats["xAG"] = float(stats_list[14].text) if (stats_list[14].text != "") else float(0)

        players[player_name] = stats 
    
    return players

def scrap_players(team):
    dict_players_of_team = get_players_stats(teams_urls[team])
    return dict_players_of_team

def get_matches(team_url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = team_url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    table_matchs = pageSoup.find_all('tbody', class_=False)[1]
    rows = table_matchs.find_all('tr', class_=False)

    matches = {}
    for row in rows:
        match = {}
        td = row.find_all('td', class_="left")
        matchweek = td[0].text
        match["Venue"] = td[2].text
        td = row.find_all('td', class_="center")
        match['Status'] = False if td[0].text == '' else True
        match["Result"] = td[0].text
        td = row.find_all('td', class_="right")
        match['Goals_for'] = float(td[1].text) if (td[1].text != "") else float(0)
        match['Goals_against'] = float(td[2].text) if (td[2].text != "") else float(0)
        match['xG'] = float(td[3].text) if (td[3].text != "") else float(0)
        match['xGA'] = float(td[4].text) if (td[4].text != "") else float(0)
        matches[matchweek] = match
    return matches

def scrap_matches(team):
    dict_matches = get_matches(teams_urls[team])
    return dict_matches
