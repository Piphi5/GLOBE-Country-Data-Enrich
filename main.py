import sys

from autoupdater.countryscript.country_updater import Country_Updater


username, password = sys.argv[1:]
updater = Country_Updater(username, password)
updater.run()
