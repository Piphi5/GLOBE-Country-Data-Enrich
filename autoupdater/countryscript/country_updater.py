from arcgis.gis import GIS
from arcgis import features
from arcgis.features import GeoAccessor
from arcgis.features import FeatureLayerCollection

temp_layer_name = "Temp_layer"


class Country_Updater:
    def __init__(self, protocol, inputid, outputid, username, password):
        self.gis = GIS(
            url="https://igestrategies.maps.arcgis.com",
            username=username,
            password=password,
        )
        self.inputid = inputid
        self.outputid = outputid
        self.filename = f"{protocol}CountryEnriched.csv"

    def get_data(self):
        item = self.gis.content.get(itemid=self.inputid)
        countries_item = self.gis.content.get(itemid="2b93b06dc0dc4e809d3c8db5cb96ba69")
        self.temp_layer = features.analysis.join_features(
            target_layer=item,
            join_layer=countries_item,
            spatial_relationship="intersects",
            join_operation="JoinOneToMany",
            output_name=temp_layer_name,
        )
        self.temp_df = GeoAccessor.from_layer(self.temp_layer.layers[0])
        self.temp_df = self.temp_df.drop(
            labels=["AFF_ISO", "ISO", "Join_Count", "OBJECTID", "TARGET_FID", "SHAPE"],
            axis=1,
        )

        return self.temp_df

    def to_csv(self):
        self.temp_df.to_csv(self.filename)

    def update_layers(self):
        self.temp_df.to_csv(self.filename)
        item = self.gis.content.get(self.outputid)
        item_layer_collection = FeatureLayerCollection.fromitem(item)
        response = item_layer_collection.manager.overwrite(self.filename)

        delete_output = self.temp_layer.delete()
        return response["success"], delete_output

    def run(self):
        self.get_data()
        self.update_layers()
