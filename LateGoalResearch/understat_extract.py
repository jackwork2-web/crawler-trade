import requests

url = "https://understat.com/league/EPL/2024"

html = requests.get(url).text

keywords = [
    "datesData",
    "teamsData",
    "playersData",
    "JSON.parse",
    "calendarData",
    "matchesData",
    "standings"
]

for keyword in keywords:
    print(f"{keyword}: {keyword in html}")
