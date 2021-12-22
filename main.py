import sys

from autoupdater.countryscript.country_updater import Country_Updater


username, password = sys.argv[1:]
mhm_updater = Country_Updater(
    "MosquitoHabitatMapper",
    "ae4990333e9f41f489550ddbe16a9d0f",
    "8bc5b0ac24d3474e9ab6ce2bfb4f37fe",
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
