import csv
from library.point import *
from tqdm import tqdm


class R774PointDAO(object):

    def __init__(self, path):
        self.path = path
        self.columns = [
            "pref",
            "city",
            "district",
            "latitude",
            "longitude",
            "name",
            "description"
        ]
        self.pref_idx = self.columns.index("pref")
        self.city_idx = self.columns.index("city")
        self.district_idx = self.columns.index("district")
        self.lat_idx = self.columns.index("latitude")
        self.lon_idx = self.columns.index("longitude")
        self.name_idx = self.columns.index("name")
        self.description_idx = self.columns.index("description")

    def make_r774_point_data(self, r774_points):
        """
        人口点データをcsvに書き込む
        :param r774_points:
        :return:
        """
        with open(self.path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")

            # ヘッダ
            writer.writerow(self.columns)

            # データ
            for p in r774_points:

                row = []
                for _ in range(len(self.columns)):
                    row.append(None)

                row[self.pref_idx] = p.pref
                row[self.city_idx] = p.city
                row[self.district_idx] = p.district
                row[self.lat_idx] = p.latitude
                row[self.lon_idx] = p.longitude
                row[self.name_idx] = p.name
                row[self.description_idx] = p.description

                writer.writerow(row)

    def read_r774_point_data(self):
        """
        人口点入力データを読み込み、点クラスのリストを返す
        :return:
        """

        r774_points = []
        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in tqdm(enumerate(reader)):

                if i == 0:
                    continue

                # Pointを作る
                p = R774Point()

                p.pref = line[self.pref_idx]
                p.city = line[self.city_idx]
                p.district = line[self.district_idx]
                p.latitude = float(line[self.lat_idx])
                p.longitude = float(line[self.lon_idx])
                p.name = line[self.name_idx]
                p.description = line[self.description_idx]

                # リストに登録
                r774_points.append(p)

        return r774_points
