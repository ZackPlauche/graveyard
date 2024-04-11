from steamscraper import SteamProfile



profile = SteamProfile.from_url('https://steamcommunity.com/id/zackyp123')
print(vars(profile))