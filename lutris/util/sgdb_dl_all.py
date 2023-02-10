"""Functions to download covers for all games from SteamGridDB"""
import os

from requests import Request
from lutris import settings
from lutris.gui import dialogs

from lutris.gui.dialogs.download import DownloadDialog
from lutris.database import games as games_db


def sgdb_dl_all():
    # Check if the setting is enabled
    sgdb_dl_step() if sgdb_dl_all_check() else dialogs.ErrorDialog(
        "SteamGridDB integration is disabled. Go to Preferences and enable it.")


def sgdb_dl_all_check():
    True if settings.read_setting("sgdb_integration") == "True" else False


def sgdb_dl_step():
    # Setup SGDB URL by retrieving the API Key
    baseurl = "https://www.steamgriddb.com/api/v2/search/autocomplete/"
    key = settings.read_setting("sgdb_api_key")
    if len(key) <= 0:
        dialogs.ErrorDialog(
            "SteamGridDB API Key not set in Preferences.")
    else:
        url = baseurl + key
        print(Request(url))
    # else:

    # gamelist = games_db.get_games()
    # for game in gamelist:
    #     name = game['name']
    # dialog = DownloadDialog(url, destination)
    # downloader = Downloader(url, dest_path, overwrite=True)
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
