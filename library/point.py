from settings.constants import *
from library import common_function as cf
import os


class Point(object):
    def __init__(self):
        self.key_code = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.pref = ""
        self.city = ""
        self.district = ""
        # self.len_district = 0

    def get_distance(self, p):
        """
        自分とpの距離を調べる関数
        :param p:
        :return: 距離km
        """
        return cf.get_distance(self.longitude, self.latitude, p.longitude, p.latitude)

    def get_google_map_url(self):
        return cf.get_google_map_url(self.latitude, self.longitude)

    def __repr__(self):
        return self.key_code

    def get_mesh_map_get_url(self, map_file):
        """
        メッシュ地図をgetパラメータで取得するURLを発行する
        :param map_file:
        :return:
        """
        url = cf.get_mesh_map_get_url(self.latitude, self.longitude, ZOOM_POINT, map_file)
        return url


class FacultyPoint(Point):

    def __init__(self):
        super().__init__()
        self.name = ""
        self.in_mesh_point = None
        self.longitude_round = None
        self.latitude_round = None
        self.urban_point = 0
        self.urban_point_round = None

    def get_is_in_mesh(self, mesh_point):

        # 緯度経度の差だけで判断
        dx = abs(self.longitude - mesh_point.longitude)
        dy = abs(self.latitude - mesh_point.latitude)
        if dx < IS_IN_MESH_THRESHOLD_LON and dy < IS_IN_MESH_THRESHOLD_LAT:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.urban_point < other.urban_point


class RegionPoint(Point):

    def get_pref(self):
        return self.pref

    def get_city(self):
        return self.city

    def get_district(self):
        return self.district

    def set_len_district(self):
        self.len_district = len(self.district)


class PopPoint(Point):
    """
    人口メッシュポイントデータクラス
    """

    def __init__(self):
        super().__init__()
        self.id = 0
        self.population = 0
        self.coast = False
        self.neighbors = []
        self.neighbor_ids = ""
        self.is_island = None
        # self.coast_distance = 0
        # self.urban_point = 0
        # self.is_village_point = True

    def add_neighbor(self, p):
        self.neighbors.append(p)

    def get_is_adjacent(self, p):
        """
        自分とpが隣接しているかを調べる関数
        :param p:
        :return:
        """
        # 緯度経度の差だけで判断
        dx = abs(self.longitude - p.longitude)
        dy = abs(self.latitude - p.latitude)
        if dx < NEIGHBOR_THRESHOLD_LON and dy < NEIGHBOR_THRESHOLD_LAT:
            return True
        else:
            return False

    def get_my_village_points(self, ignore_org, village_size_upper_limit):
        """
        自分に隣接する、人口閾値以上のポイントを返す関数
        :param ignore_org:
        :param village_size_upper_limit
        :return:
        """

        ignore = ignore_org.copy()
        ignore.append(self)
        if len(ignore) > village_size_upper_limit:
            raise cf.TooBigVillageException
        my_village_points = [self]
        for p in self.neighbors:
            if p in ignore:
                continue
            my_village_points.append(p)
            try:
                points = p.get_my_village_points(ignore, village_size_upper_limit)  # 再帰的に呼ぶ
            except cf.TooBigVillageException:
                # サイズの閾値を超えると例外が返ってくる
                raise cf.TooBigVillageException
            ignore.extend(points)
            my_village_points.extend(points)
            my_village_points = list(set(my_village_points))

        return my_village_points


class PopMeshPolygon(Point):
    """
    人口メッシュクラス
    """
    def __init__(self):
        super().__init__()
        self.id = 0
        self.coordinates = []
        self.population = 0
        self.is_island = None


class Village(object):
    """
    集落クラス（ポイントの集合）
    """

    def __init__(self):
        self.points = []
        self.size = 0
        self.population = 0
        self.point_keys = []
        self.perimeter_points = []

        self.center_point = None
        self.latitude = None
        self.longitude = None
        self.latitude_round = None
        self.longitude_round = None

        self.pref = ""
        self.city = ""
        self.district = ""

        # 都会度
        self.urban_point = 0
        self.urban_point_round = 0  # html表示用

        # 離島かどうか
        self.is_island = None

    def make_village(self, mesh_points):

        # 人口・サイズ
        self.points = mesh_points
        self.size = len(self.points)
        self.population = self.calc_pop()
        for p in self.points:
            self.point_keys.append(p.key_code)
            if len(p.neighbors) < 8:
                # 隣接点が8未満なら周縁の点
                self.perimeter_points.append(p)

        # 緯度経度
        self.center_point = self.get_center_point()
        self.latitude = self.center_point.latitude
        self.longitude = self.center_point.longitude
        self.latitude_round = round(self.latitude, LAT_LON_ROUND)  # html表示用
        self.longitude_round = round(self.longitude, LAT_LON_ROUND)  # html表示用

        # 住所
        self.pref = self.center_point.pref
        self.city = self.center_point.city
        self.district = self.center_point.district

        # 離島かどうか
        self.is_island = self.center_point.is_island

    def calc_pop(self):
        population = 0
        for p in self.points:
            population += p.population
        return population

    def get_center_point(self):
        """
        最も人口の多いポイント
        :return:
        """
        max_pop = 0
        center_point = None
        for p in self.points:
            if p.population > max_pop:
                max_pop = p.population
                center_point = p
        return center_point

    def get_distance(self, point):
        """
        集落から集落外ポイントへの距離（最短地点）
        :param point:
        :return:
        """
        dist = 0
        for i, p in enumerate(self.perimeter_points):
            tmp_dist = p.get_distance(point)
            if i == 0:
                dist = tmp_dist
                continue
            if tmp_dist < dist:
                dist = tmp_dist
        return dist

    # def get_is_coast(self):
    #     for p in self.points:
    #         if p.coast:
    #             return True
    #     return False
    #
    # def set_coast_distance(self):
    #     """
    #     海岸点が含まれていれば0
    #     そうでなければ、中心点からの距離
    #     :return:
    #     """
    #
    #     if self.get_is_coast():
    #         self.coast_distance = 0
    #     else:
    #         self.coast_distance = self.center_point.coast_distance

    # def calc_urban_point(self):
    #     """
    #     都会度を計算する
    #     :return:
    #     """
    #
    #     # 中心点以外のポイントのリスト
    #     points = self.points.copy()
    #     points.remove(self.center_point)
    #
    #     # 中心点の都会度からそれ以外のポイントによる都会度をひく
    #     urban_point = self.center_point.urban_point
    #     for p in points:
    #         dist = self.center_point.get_distance(p)
    #         pop = p.population
    #         up = cf.calc_urban_point(pop, dist)
    #         urban_point -= up
    #
    #     return urban_point

    def __repr__(self):
        return str(
            "urban_point = " + str(self.urban_point) + ", " +
            "population = " + str(self.population) +
            "points = " + str(self.point_keys)
        )

    def __lt__(self, other):
        return self.urban_point < other.urban_point

    def get_google_map_url(self):
        url = cf.get_google_map_url(self.latitude, self.longitude)
        return url

    def get_mesh_map_get_url(self, map_file):
        """
        メッシュ地図をgetパラメータで取得するURLを発行する
        :param map_file:
        :return:
        """
        # date = int(os.stat(map_file).st_mtime)
        # url = "/mesh_map?lat=" + str(self.latitude) + "&lon=" + str(self.longitude)+ "&zoom=" + "14" + "&map_file=" + map_file
        url = cf.get_mesh_map_get_url(self.latitude, self.longitude, ZOOM_POINT, map_file)
        return url

