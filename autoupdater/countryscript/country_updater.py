import sys, os

from arcgis.gis import GIS
from arcgis import features
from arcgis.features import GeoAccessor
from autoupdater.utils import OverwriteFS

temp_layer_name = "Temp_layer"
filename = "Data.csv"


class Country_Updater:
    def __init__(self, username, password):
        self.gis = GIS(
            url="https://igestrategies.maps.arcgis.com",
            username=username,
            password=password,
        )

    def get_data(self):
        mhm_item = self.gis.content.get(itemid="2793f3d9c4d4447ea4f21b3ad74965d4")
        countries_item = self.gis.content.get(itemid="2b93b06dc0dc4e809d3c8db5cb96ba69")
        self.temp_layer = features.analysis.join_features(
            target_layer=mhm_item.layers[0],
            join_layer=countries_item.layers[0],
            spatial_relationship="intersects",
            output_name=temp_layer_name,
        )
        self.temp_df = GeoAccessor.from_layer(self.temp_layer.layers[0])
        self.temp_df = self.temp_df.drop(
            labels=["AFF_ISO", "ISO", "Join_Count", "OBJECTID", "TARGET_FID"], axis=1
        )

        return self.temp_df

    def update_layers(self):
        self.temp_df.to_csv(filename)
        item_id = "a988ac7da45747519292b67b05ff288a"
        item = self.gis.content.get(item_id)
        
        sys.stdout = open(os.devnull, 'w')
        overwrite_output = OverwriteFS.overwriteFeatureService(
            item, updateFile=filename, touchItems=True, verbose=True
        )
        sys.stdout = sys.__stdout__

        delete_output = self.temp_layer.delete()
        return overwrite_output["success"], delete_output

    def run(self):
        self.get_data()
        self.update_layers()


if __name__ == "__main__":
    import sys

    username, password = sys.argv
    updater = Country_Updater(username, password)
    updater.run()
