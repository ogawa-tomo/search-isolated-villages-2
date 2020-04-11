import csv
from library.point import *
import json


class PopPolygonDAO(object):

    def __init__(self, path):
        self.path = path
        self.columns = [
            "id",
            "key",
            "coordinates",
            "latitude",
            "longitude",
            "pref",
            "city",
            "district",
            "population",
            "is_island"
        ]
        self.id_idx = self.columns.index("id")
        self.key_idx = self.columns.index("key")
        self.coordinates_idx = self.columns.index("coordinates")
        self.latitude_idx = self.columns.index("latitude")
        self.longitude_idx = self.columns.index("longitude")
        self.pref_idx = self.columns.index("pref")
        self.city_idx = self.columns.index("city")
        self.district_idx = self.columns.index("district")
        self.pop_idx = self.columns.index("population")
        self.is_island_idx = self.columns.index("is_island")

    def clear_pop_polygon_data(self):
        """
        クリアしてヘッダを書き込む
        :return:
        """
        with open(self.path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")
            # ヘッダ
            writer.writerow(self.columns)

    def add_pop_polygon_data(self, pop_polygons):
        """
        人口メッシュポリゴンデータをcsvに追記する
        :param pop_polygons: 人口メッシュポリゴンクラス（PopMeshPolygon）インスタンスの集合
        :return:
        """
        with open(self.path, "a", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")

            # ヘッダ
            # writer.writerow(self.columns)

            # データ
            for p in pop_polygons:

                row = []
                for _ in range(len(self.columns)):
                    row.append(None)

                row[self.id_idx] = p.id
                row[self.key_idx] = p.key_code
                row[self.coordinates_idx] = self.make_coordinates(p.coordinates)
                row[self.latitude_idx] = p.latitude
                row[self.longitude_idx] = p.longitude
                row[self.pref_idx] = p.pref
                row[self.city_idx] = p.city
                row[self.district_idx] = p.district
                row[self.pop_idx] = p.population
                row[self.is_island_idx] = p.is_island

                writer.writerow(row)

    def read_pop_polygon_data(self):
        """
        人口点入力データを読み込み、点クラスのリストを返す
        :return:
        """

        pop_polygons = []
        # print("人口ポリゴンを読み込み中")

        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):

                if i == 0:
                    continue

                # 人口Pointを作る
                p = PopMeshPolygon()

                p.id = line[self.id_idx]
                p.key_code = line[self.key_idx]
                p.coordinates = self.read_coordinates(line[self.coordinates_idx])
                p.latitude = float(line[self.latitude_idx])
                p.longitude = float(line[self.longitude_idx])
                p.pref = line[self.pref_idx]
                p.city = line[self.city_idx]
                p.district = line[self.district_idx]
                p.population = int(line[self.pop_idx])
                if line[self.is_island_idx] == "True":
                    p.is_island = True
                else:
                    p.is_island = False

                pop_polygons.append(p)

        return pop_polygons

    @staticmethod
    def read_coordinates(coordinates_data):
        # 形式→[[[122.971875, 24.4375], [122.96874999999999, 24.4375], [122.96874999999999, 24.43958333333333], [122.971875, 24.43958333333333], [122.971875, 24.4375]]]
        coordinates_str_list = coordinates_data.lstrip("[").rstrip("]").split("], [")
        coordinates = []
        for csl in coordinates_str_list:
            coordinate_str_list = csl.split(",")
            coordinate = [float(coordinate_str_list[0]), float(coordinate_str_list[1])]
            coordinates.append(coordinate)
        return coordinates

    @staticmethod
    def make_coordinates(coordinates):
        # 形式→[[[122.971875, 24.4375], [122.96874999999999, 24.4375], [122.96874999999999, 24.43958333333333], [122.971875, 24.43958333333333], [122.971875, 24.4375]]]
        data = [coordinates]
        return data

    def get_polygon_geojson_data(self, polygons):
        """
        ポリゴンのgeojsonデータを作る（座標とkeycodeだけでよい）
        :param polygons:
        :return:
        """
        geodict = {
            "type": "FeatureCollection",
            "features": []
        }

        for i, p in enumerate(polygons):
            feature = {
                "id": i,
                "type": "Feature",
                "properties": {},
                "geometry":
                    {
                        "type": "Polygon",
                        "coordinates": None
                    }
            }
            feature["properties"]["KEY_CODE"] = p.key_code
            feature["geometry"]["coordinates"] = self.make_coordinates(p.coordinates)
            geodict["features"].append(feature)

        geojson = json.dumps(geodict)
        return geojson

