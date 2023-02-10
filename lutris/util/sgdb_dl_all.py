"""Functions to download covers for all games from SteamGridDB"""
from lutris import settings
from lutris.gui import dialogs

from lutris.database import games as games_db
from lutris.util.downloader import Downloader
from lutris.util.http import HTTPError, Request

gamelist = games_db.get_games()


def sgdb_dl_all(type):
    # Check if the setting is enabled
    key = sgdb_key_test() if settings.read_setting("sgdb_integration") else dialogs.ErrorDialog(
        "SteamGridDB integration is disabled. Go to preferences to enable it.")
    todl = check_games(type)
    for game in todl:
        searchurl = "https://www.steamgriddb.com/api/v2/search/autocomplete/" + game
        id = get_game_in_sgdb(Request(searchurl, headers=key).json())
        geturl = "https://www.steamgriddb.com/api/v2/grids/game/" + id + "?dimensions=" + get_dimension(type)
        Downloader(geturl, f"{type}_PATH", overwrite=True)


def sgdb_key_test():
    # Setup SGDB URL by retrieving the API Key
    key = settings.read_setting("sgdb_api_key")
    headers = {'Authorization': 'Bearer ' + key}
    if len(key) <= 0:
        dialogs.ErrorDialog(
            "SteamGridDB API Key not set in preferences.")
    try:
        Request("https://www.steamgriddb.com/api/v2/grids/game/1?dimensions=600x900", headers=headers)
    except HTTPError:
        dialogs.ErrorDialog(
            "An error occured with the API Key.")
    return key


def check_games(type):
    a = []
    for game in gamelist:
        if game[f"has_custom_{type}"] is None or game[f"has_custom_{type}"] == 0:
            a.append(game["name"])
            game[f"has_custom_{type}"] = 1
    return a


def get_dimension(type):
    if type == "banner":
        return "920x430"
    else:
        return "600x900"


def get_game_in_sgdb(req):
    if len(req["data"]) == 0:
        print("Could not find a cover for game")
    else:
        print("Found game")
        id = req["data"][0]["id"]
        return id

    # dialog = DownloadDialog(url, destination)
    # runner = row.runner
    # row.install_progress.set_fraction(0.0)
    # dest_path = self.get_dest_path(runner)
    # url = runner[self.COL_URL]
    # if not url:
    #     ErrorDialog(_("Version %s is not longer available") % runner[self.COL_VER])
    #     return
    # GLib.timeout_add(100, self.get_progress, downloader, row)
    # self.installing[runner[self.COL_VER]] = downloader
    # downloader.start()
    # self.update_listboxrow(row)
