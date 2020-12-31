import csv
from library.point import FacultyPoint
from settings.constants import *


class FacultyDAO(object):

    def __init__(self, path):
        self.path = path
        self.columns = [
            "name",
            "pref",
            "city",
            "district",
            "latitude",
            "longitude",
            "urban_point",
            "in_mesh_point",
            "is_island"
        ]
        self.name_idx = self.columns.index("name")
        self.pref_idx = self.columns.index("pref")
        self.city_idx = self.columns.index("city")
        self.district_idx = self.columns.index("district")
        self.lat_idx = self.columns.index("latitude")
        self.lon_idx = self.columns.index("longitude")
        self.urban_point_idx = self.columns.index("urban_point")
        self.in_mesh_point_idx = self.columns.index("in_mesh_point")
        self.is_island_idx = self.columns.index("is_island")

    def make_faculty_point_data(self, faculty_points):
        """
        施設点データをcsvに書き込む
        :param faculty_points:
        :return:
        """

        with open(self.path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")

            # ヘッダ
            writer.writerow(self.columns)

            # データ
            for p in faculty_points:

                row = []
                for _ in range(len(self.columns)):
                    row.append(None)

                row[self.name_idx] = p.name
                row[self.pref_idx] = p.pref
                row[self.city_idx] = p.city
                row[self.district_idx] = p.district
                row[self.lat_idx] = p.latitude
                row[self.lon_idx] = p.longitude
                row[self.urban_point_idx] = p.urban_point
                row[self.in_mesh_point_idx] = p.in_mesh_point
                row[self.is_island_idx] = p.is_island

                writer.writerow(row)

    def read_faculty_point_data(self):
        """
        施設点データを読み込んでリストを返す
        :return:
        """
        faculty_points = []

        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):

                if i == 0:
                    continue

                # Pointを作る
                p = FacultyPoint()

                p.name = line[self.name_idx]
                p.pref = line[self.pref_idx]
                p.city = line[self.city_idx]
                p.district = line[self.district_idx]
                p.latitude = float(line[self.lat_idx])
                p.longitude = float(line[self.lon_idx])
                p.urban_point = float(line[self.urban_point_idx])
                if line[self.is_island_idx] == "True":
                    p.is_island = True
                else:
                    p.is_island = False

                # html出力用
                p.latitude_round = round(p.latitude, LAT_LON_ROUND)
                p.longitude_round = round(p.longitude, LAT_LON_ROUND)
                p.urban_point_round = round(p.urban_point, URBAN_POINT_ROUND)

                # リストに登録
                faculty_points.append(p)

        return faculty_points


class CorrectFacultyDAO(object):
    """
    施設座標修正データを読み込むクラス
    """

    def __init__(self, path):
        self.path = path
        self.columns = [
            "name",
            "raw_lat",
            "raw_lon",
            "correct_lat",
            "correct_lon"
        ]
        self.name_idx = self.columns.index("name")
        self.raw_lat_idx = self.columns.index("raw_lat")
        self.raw_lon_idx = self.columns.index("raw_lon")
        self.correct_lat_idx = self.columns.index("correct_lat")
        self.correct_lon_idx = self.columns.index("correct_lon")

    def read_data(self):
        """
        施設点データを読み込んでリストを返す
        :return:
        """
        points = []

        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):

                if i == 0:
                    continue

                # Pointを作る
                p = CorrectFacultyData()

                p.name = line[self.name_idx]
                p.raw_lat = float(line[self.raw_lat_idx])
                p.raw_lon = float(line[self.raw_lon_idx])
                p.correct_lat = float(line[self.correct_lat_idx])
                p.correct_lon = float(line[self.correct_lon_idx])

                # リストに登録
                points.append(p)

        return points


class CorrectFacultyData(object):
    """
    施設の修正データを保持するクラス
    """
    def __init__(self):
        self.name = None
        self.raw_lat = None
        self.raw_lon = None
        self.correct_lat = None
        self.correct_lon = None
