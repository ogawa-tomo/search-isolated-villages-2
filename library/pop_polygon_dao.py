import csv
from library.point import *
from tqdm import tqdm


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
            "population"
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

    def clear_pop_polygon_data(self):
        """
        クリアしてヘッダを書き込む
        :return:
        """
        with open(self.path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")
            # ヘッダ
            writer.writerow(self.columns)

    # def add_pop_polygon_data(self, pop_polygons):
    #     """
    #     人口メッシュポリゴンデータをcsvに追記する
    #     :param pop_polygons:
    #     :return:
    #     """
    #     self.make_pop_polygon_data(pop_polygons, "a")

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

                writer.writerow(row)

    def read_pop_polygon_data(self):
        """
        人口点入力データを読み込み、点クラスのリストを返す
        :return:
        """

        pop_polygons = []
        print("人口ポリゴンを読み込み中")

        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in tqdm(enumerate(reader)):

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
        data = "[" + str(coordinates) + "]"
        return data

    # @staticmethod
    # def make_coordinates(coordinates):
    #     """
    #     座標をハイフンでつないだ文字列を返す
    #     :param coordinates:
    #     :return:
    #     """
    #     coordinates = ""
    #     for i, c in enumerate(coordinates):
    #         if i == 0:
    #             neighbor_ids = str(c.coordinate)
    #         else:
    #             coordinates += "-" + str(n.id)
    #     return neighbor_ids


# if __name__ == "__main__":
#     dao = PopPolygonDAO("pop_polygons.csv")
#     polygons = dao.read_pop_polygon_data()
#     for p in polygons:
#         print(p.key_code)
#         print(p.coordinates)
#         print(p.coordinates[0])
#         print(p.coordinates[0][0])
#
#     dao.make_pop_polygon_data(polygons)
#     polygons = dao.read_pop_polygon_data()
#     for p in polygons:
#         print(p.key_code)
#         print(p.coordinates)
#         print(p.coordinates[0])
#         print(p.coordinates[0][0])

