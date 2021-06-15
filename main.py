import sys

from autoupdater.countryscript.country_updater import Country_Updater


username, password = sys.argv[1:]
mhm_updater = Country_Updater(
    "MosquitoHabitatMapper",
    "2793f3d9c4d4447ea4f21b3ad74965d4",
    "4e8bdb70b3d6424b8831e9cc621cf3b6",
    username,
    password,
)
lc_updater = Country_Updater(
    "LandCover",
    "ff0dda11e84141c0a630c47e2a8203bf",
    "c68acbfc68db4409b495fd4636646aa6",
    username,
    password,
)

mhm_updater.run()
lc_updater.run()
