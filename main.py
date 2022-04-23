import sys

from autoupdater.countryscript.country_updater import Country_Updater


username, password = sys.argv[1:]
mhm_updater = Country_Updater(
    "MosquitoHabitatMapper",
    "ae4990333e9f41f489550ddbe16a9d0f",
    "a018521fbc3f42bc848d3fa4c52e02ce",
    username,
    password,
)
lc_updater = Country_Updater(
    "LandCover",
    "ff0dda11e84141c0a630c47e2a8203bf",
    "fe54b831415f44d2b1640327ae276fb8",
    username,
    password,
)

mhm_updater.run()
lc_updater.run()
