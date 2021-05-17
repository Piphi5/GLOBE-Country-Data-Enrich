from datetime import datetime
import numpy as np
import sys, os


from arcgis.gis import GIS
from arcgis import features
from arcgis.features import GeoAccessor
from autoupdater.utils import OverwriteFS

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
            target_layer=item.layers[0],
            join_layer=countries_item.layers[0],
            spatial_relationship="intersects",
            output_name=temp_layer_name,
        )
        self.temp_df = GeoAccessor.from_layer(self.temp_layer.layers[0])
        self.temp_df = self.temp_df.drop(
            labels=["AFF_ISO", "ISO", "Join_Count", "OBJECTID", "TARGET_FID", "SHAPE"],
            axis=1,
        )

        convert_to_datetime = np.vectorize(
            lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        )

        if type(self.temp_df.loc[0, "measuredDate"]) is str:
            self.temp_df["measuredDate"] = convert_to_datetime(
                df["measuredDate"].to_numpy()
            )

        protocol = self.temp_df.loc[0, "protocol"]
        measured_at = protocol.replace("_", "") + "MeasuredAt"
        if type(self.temp_df.loc[0, measured_at]) is str:
            self.temp_df[measured_at] = convert_to_datetime(df[measured_at].to_numpy())

        return self.temp_df

    def to_csv(self):
        self.temp_df.to_csv(self.filename)

    def update_layers(self):
        self.temp_df.to_csv(self.filename)
        item = self.gis.content.get(self.outputid)

        overwrite_output = OverwriteFS.overwriteFeatureService(
            item, updateFile=self.filename, touchItems=True, verbose=True
        )

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
