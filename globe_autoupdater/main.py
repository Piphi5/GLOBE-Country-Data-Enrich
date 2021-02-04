import sys

from country_data.country_updater import Country_Updater


username, password = sys.argv[1:]
updater = Country_Updater(username, password)
updater.run()