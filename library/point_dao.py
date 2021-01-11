import csv
from library.point import *
from tqdm import tqdm
import library.common_function as cf
from library.setting import RegionSetting
from library.island_checker import IslandChecker
import settings.file_path as fp
from settings.constants import *

class PopPointDAO(object):

    def __init__(self, path):
        self.path = path
        self.columns = [
            "id",
            "key",
            "neighbors",
            "pref",
            "city",
            "district",
            "population",
            "latitude",
            "longitude",
            "is_island"
            # "coast",
            # "coast_distance",
            # "urban_point",
            # "is_village_point"
        ]
        self.id_idx = self.columns.index("id")
        self.key_idx = self.columns.index("key")
        self.neighbors_idx = self.columns.index("neighbors")
        self.pref_idx = self.columns.index("pref")
        self.city_idx = self.columns.index("city")
        self.district_idx = self.columns.index("district")
        self.pop_idx = self.columns.index("population")
        self.lat_idx = self.columns.index("latitude")
        self.lon_idx = self.columns.index("longitude")
        self.is_island_idx = self.columns.index("is_island")
        # self.coast_idx = self.columns.index("coast")
        # self.coast_distance_idx = self.columns.index("coast_distance")
        # self.urban_point_idx = self.columns.index("urban_point")
        # self.is_village_point_idx = self.columns.index("is_village_point")

    def make_pop_point_data(self, pop_points):
        """
        人口点データをcsvに書き込む
        :param pop_points:
        :return:
        """
        with open(self.path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")

            # ヘッダ
            writer.writerow(self.columns)

            # データ
            for p in pop_points:

                row = []
                for _ in range(len(self.columns)):
                    row.append(None)

                row[self.id_idx] = p.id
                row[self.key_idx] = p.key_code
                row[self.neighbors_idx] = self.make_neighbor_ids(p.neighbors)
                row[self.pref_idx] = p.pref
                row[self.city_idx] = p.city
                row[self.district_idx] = p.district
                row[self.pop_idx] = p.population
                row[self.lat_idx] = p.latitude
                row[self.lon_idx] = p.longitude
                row[self.is_island_idx] = p.is_island
                # row[self.coast_idx] = p.coast
                # row[self.coast_distance_idx] = p.coast_distance
                # row[self.urban_point_idx] = p.urban_point
                # row[self.is_village_point_idx] = p.is_village_point

                writer.writerow(row)

    def read_pop_point_data(self):
        """
        人口点入力データを読み込み、点クラスのリストを返す
        :return:
        """

        pop_points = []
        print("人口点を読み込み中")

        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in tqdm(enumerate(reader)):

                if i == 0:
                    continue

                # 人口Pointを作る
                p = PopPoint()

                p.key_code = line[self.key_idx]
                if line[self.neighbors_idx] != "":
                    p.neighbor_ids = [int(k) for k in line[self.neighbors_idx].split("-")]
                else:
                    p.neighbor_ids = []
                p.pref = line[self.pref_idx]
                p.city = line[self.city_idx]
                p.district = line[self.district_idx]
                p.population = int(line[self.pop_idx])
                p.latitude = float(line[self.lat_idx])
                p.longitude = float(line[self.lon_idx])
                if line[self.is_island_idx] == "True":
                    p.is_island = True
                else:
                    p.is_island = False

                # リストに登録
                pop_points.append(p)

        # 隣接点を登録（all_pop_pointsがID順に並んでいることを前提にしている）
        for p in pop_points:
            for idx in p.neighbor_ids:
                p.add_neighbor(pop_points[idx])

        return pop_points

    @staticmethod
    def make_neighbor_ids(neighbors):
        """
        隣接点IDをハイフンでつないだ文字列を返す
        :param neighbors:
        :return:
        """
        neighbor_ids = ""
        for i, n in enumerate(neighbors):
            if i == 0:
                neighbor_ids = str(n.id)
            else:
                neighbor_ids += "-" + str(n.id)
        return neighbor_ids


class PopPointDAOForTokaidoTaiketsu(object):

    def __init__(self, path):
        self.path = path
        self.columns = [
            "key",
            "latitude",
            "longitude",
            "urban_point"
        ]
        # self.id_idx = self.columns.index("id")
        self.key_idx = self.columns.index("key")
        # self.neighbors_idx = self.columns.index("neighbors")
        # self.pref_idx = self.columns.index("pref")
        # self.city_idx = self.columns.index("city")
        # self.district_idx = self.columns.index("district")
        # self.pop_idx = self.columns.index("population")
        self.lat_idx = self.columns.index("latitude")
        self.lon_idx = self.columns.index("longitude")
        # self.coast_idx = self.columns.index("coast")
        # self.coast_distance_idx = self.columns.index("coast_distance")
        self.urban_point_idx = self.columns.index("urban_point")
        # self.is_village_point_idx = self.columns.index("is_village_point")

    def make_pop_point_data(self, pop_points):
        """
        人口点データをcsvに書き込む
        :param pop_points:
        :return:
        """
        with open(self.path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")

            # ヘッダ
            writer.writerow(self.columns)

            # データ
            for p in pop_points:

                row = []
                for _ in range(len(self.columns)):
                    row.append(None)

                row[self.key_idx] = p.key_code
                row[self.lat_idx] = p.latitude
                row[self.lon_idx] = p.longitude
                row[self.urban_point_idx] = p.urban_point

                writer.writerow(row)
    
    def get_tokaido(self, lat, lon):

        with open(self.path, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            for i, line in tqdm(enumerate(reader)):

                if i == 0:
                    continue
                p_lat = float(line[self.lat_idx])
                p_lon = float(line[self.lon_idx])

                dx = abs(lon - p_lon)
                dy = abs(lat - p_lat)

                if dx < IS_IN_MESH_THRESHOLD_LON and dy < IS_IN_MESH_THRESHOLD_LAT:
                    return float(line[self.urban_point_idx])
        
        raise Exception



