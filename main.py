import requests

url = "https://api-nba-v1.p.rapidapi.com/standings"

querystring = {"league": "standard", "season": "2021"}

headers = {
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "4492ae6de4msh1b49a74c289262fp19578bjsn0b92373d96d9"
}

response = requests.request("GET", url, headers=headers, params=querystring)
# convert response into a json object for easier use
jsonRes = response.json()

# store user input team names
home_team = input('Enter Home teams name')
away_team = input('Enter Away teams name')

# initalize empty object to hold team data that needs to be compared.
team_data = {}

# Step 1: Search for team data based on user input.

for team in jsonRes['response']:
    # store team name in a variable for easy use later
    team_name = team['team']['name']
    # compare if user inputted team name matches the current team_name you are on in the loop
    if team_name == home_team or team_name == away_team:
        # if team is a match store team_name and win percentage in the team_data object
        team_data[team_name] = {}
        team_data[team_name]['win_percentage'] = float(
            team['win']['percentage'])
        team_data[team_name]['win_streak'] = team['winStreak']
        team_data[team_name]['streak'] = team['streak']
        team_data[team_name]['home_win_percentage'] = float(
            team['win']['home'] / team['win']['total'])
        team_data[team_name]['away_win_percentage'] = float(
            team['win']['away'] / team['win']['total'])
        team_data[team_name]['prediction_score'] = float(
            team['win']['percentage'])

        # print(team_data)


def assignTeamPredictionScore(teams):

    homeTeam = team_data[home_team]
    awayTeam = team_data[away_team]

    for team in teams:
        if team['win_streak']:
            if team['streak'] >= 5:
                team['prediction_score'] += .25
            elif team['win_streak'] == 3:
                team['prediction_score'] += .15
            else:
                team['prediction_score'] += .10

    if homeTeam['home_win_percentage'] > awayTeam['away_win_percentage']:
        homeTeam['prediction_score'] += .20
    elif awayTeam['away_win_percentage'] > homeTeam['home_win_percentage']:
        awayTeam['prediction_score'] += .20
    else:
        return


assignTeamPredictionScore([team_data[home_team], team_data[away_team]])

if team_data[home_team]['prediction_score'] > team_data[away_team]['prediction_score']:
    print(home_team + ' is the winner!')
else:
    print(away_team + ' is the winner!')
