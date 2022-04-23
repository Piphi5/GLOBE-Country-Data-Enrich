import csv
import os

from arcgis.gis import GIS
from arcgis.features import GeoAccessor
from arcgis.geometry import Geometry
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
        self.protocol = protocol
        self.filename = f"{protocol}CountryEnriched.csv"

    def fix_germany(self, country_df):
        # Germany has some geometry that isn't compatible with shapely so its removed here
        germany_entry = country_df[country_df["AFF_ISO"] == "DE"]
        germany_index = germany_entry.index[0]
        germany_dict = dict(germany_entry["SHAPE"].iloc[0])
        germany_dict["rings"] = germany_dict["rings"][:-1]
        country_df.at[germany_index, "SHAPE"] = Geometry(germany_dict)

    def get_data(self):
        data_source = self.gis.content.get(itemid=self.inputid)
        source_df = GeoAccessor.from_layer(data_source.layers[0])

        # Remove entries with null geometries
        source_df = source_df.dropna(subset=[source_df.spatial.name])

        countries_item = self.gis.content.get(itemid="2b93b06dc0dc4e809d3c8db5cb96ba69")
        country_map = GeoAccessor.from_layer(countries_item.layers[0])

        self.fix_germany(country_map)

        self.enriched_df = source_df.spatial.join(country_map)

        self.enriched_df = self.enriched_df.drop(
            labels=[
                "index_right",
                "FID",
                "AFF_ISO",
                "ISO",
                "Shape__Area",
                "Shape__Length",
                "SHAPE",
            ],
            axis=1,
        )
        self.to_csv()

    def to_csv(self):
        self.enriched_df.to_csv(
            self.filename,
            sep=",",
            index=False,
            encoding="utf-8",
            quoting=csv.QUOTE_ALL,
            quotechar='"',
            escapechar="”",
        )

    def update_layers(self):
        item = self.gis.content.get(self.outputid)
        item_layer_collection = FeatureLayerCollection.fromitem(item)
        response = item_layer_collection.manager.overwrite(
            os.path.join(os.getcwd(), self.filename)
        )

        print(response)
        # Makes sure it was successful in updating the layer
        assert response["success"]

    def run(self):
        self.get_data()
        self.update_layers()
