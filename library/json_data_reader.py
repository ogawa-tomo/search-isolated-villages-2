import json
from library.setting import RegionSetting
from tqdm import tqdm
from library.point import *
from library import common_function as cf
from settings.constants import *
from abc import ABCMeta, abstractmethod
import copy


class JsonPointDataReader(object):
    """
    geojson形式のデータを読み込む基底クラス
    """

    def __init__(self, file):
        self.file = file
        self.raw_data_set = self.get_raw_data_set()

    def get_raw_data_set(self):
        with open(self.file, "r") as f:
            data = f.read()
        data = json.loads(data)
        data = data["features"]
        return data


class JsonRegionPointDataReader(JsonPointDataReader):

    """
    geojson形式の小地域データを読み込むクラス
    """

    def __init__(self, file):
        super().__init__(file)
        self.region_points = []
        self.read_points()

    def read_points(self):

        # print("地域点の読み込み中")
        for raw_data in self.raw_data_set:
            data = JsonRegionPointData(raw_data)
            p = RegionPoint()
            p.key_code = data.get_key_code()
            p.latitude = data.get_latitude()
            p.longitude = data.get_longitude()
            p.pref = data.get_pref()
            p.city = data.get_city()
            p.district = data.get_district()

            self.region_points.append(p)

    def get_points(self):
        return self.region_points


class JsonMeshPointDataReader(JsonPointDataReader):
    """
    geojson形式の人口メッシュデータを読み込むクラス
    """

    def __init__(self, file):
        super().__init__(file)
        self.points = []
        self.read_points()

    def read_points(self):
        """
        点の読み込み（人口のある点と海岸点）
        :return:
        """

        # print("人口点の読み込み中")
        for raw_data in self.raw_data_set:
            """
            jsonデータから全ポイントデータのリストを生成
            """

            p = PopPoint()

            data = JsonPointData(raw_data)
            # p.population = data.get_population()
            p.key_code = data.get_key_code()
            p.latitude = data.get_latitude()
            p.longitude = data.get_longitude()
            # p.first_mesh_code = self.first_mesh_code
            # p.coast = data.get_coast()

            self.points.append(p)

    def get_points(self):
        return self.points


class JsonFacultyPointDataReader(JsonPointDataReader):
    """
    geojson形式の施設点データを読み込むクラス
    """

    # def __init__(self, file, faculty_type):
    def __init__(self, file, data_class):
        super().__init__(file)
        self.points = []
        # self.faculty_type = faculty_type

        self.data_class = data_class

        # if self.faculty_type == ELEMENTARY_SCHOOL:
        #     self.data_class = JsonElementarySchoolData
        # elif self.faculty_type == POST_OFFICE:
        #     self.data_class = JsonPostOfficeData
        # else:
        #     raise Exception("施設タイプ名が不正です")

        self.read_points()

    def read_points(self):
        """
        点の読み込み（人口のある点と海岸点）
        :return:
        """

        print("施設点の読み込み中")
        for raw_data in tqdm(self.raw_data_set):
            """
            jsonデータから全ポイントデータのリストを生成
            """

            p = FacultyPoint()

            try:
                data = self.data_class(raw_data)
            except NotTargetFacultyException:
                continue

            p.name = data.get_name()
            p.latitude = data.get_latitude()
            p.longitude = data.get_longitude()

            self.points.append(p)

        if self.data_class == JsonAbandonedStationData:
            print("廃駅の重複を削除")
            self.abandoned_station_deduplication()

    def get_points(self):
        return self.points

    def abandoned_station_deduplication(self):
        """
        廃駅の重複を削除するメソッド
        :return:
        """
        new_points = set()  # 追加する駅
        points_copy = self.points.copy()
        added_station_coordinates = set()
        added_station_ids = set()
        for p in tqdm(self.points):

            # 自分が営業中のとき：なにもしない
            if p.name["abandoned_year_1"] == "9999" or p.name["abandoned_year_1"] == "999":
                continue

            # 自分が廃駅のとき：同じ座標またはIDの駅を探す
            register_abandoned_station = copy.copy(p)  # まずは自分が登録候補
            # points_copy.pop(0)
            for pc in points_copy:
                # print(pc.name)
                if self.is_same_station(p, pc):

                    # 同じ駅が営業中のとき：登録候補をNoneにしてbreak
                    if pc.name["abandoned_year_1"] == "9999" or pc.name["abandoned_year_1"] == "999":
                        register_abandoned_station = None
                        break
                    # 同じ駅のほうが自分より新しいとき：相手が登録候補に
                    elif int(register_abandoned_station.name["abandoned_year_1"]) < int(pc.name["abandoned_year_1"]):
                        register_abandoned_station = copy.copy(pc)

            if register_abandoned_station is not None:
                # if register_abandoned_station.name.split("-")[2] not in added_station_ids:
                # 同じ座標の駅も同じIDの駅も登録済みでなければ、登録
                if register_abandoned_station.latitude + register_abandoned_station.longitude not in added_station_coordinates\
                        and register_abandoned_station.name["id"] not in added_station_ids:
                    added_station_coordinates.add(register_abandoned_station.latitude + register_abandoned_station.longitude)
                    added_station_ids.add(register_abandoned_station.name["id"])
                    register_abandoned_station.name = register_abandoned_station.name["name"] + " (~" \
                                                      + str(int(register_abandoned_station.name["abandoned_year_1"]) + 1)\
                                                      + ")"
                    new_points.add(register_abandoned_station)
        new_points = list(new_points)

        self.points = new_points

    @staticmethod
    def is_same_station(s1, s2):
        """
        座標またはIDが一致していれば同じ駅（廃駅用のメソッド）
        :param s1:
        :param s2:
        :return:
        """
        if s1.latitude == s2.latitude and s1.longitude == s2.longitude:
            return True
        elif s1.name["id"] == s2.name["id"]:
            return True
        else:
            return False


class JsonPointData(object):
    """
    geojson形式のポイントデータを保持し、値を取り出すメソッドを提供するクラス
    """

    def __init__(self, data):
        self.data = data

    def get_key_code(self):
        key_code = self.data["properties"]["KEY_CODE"]
        return key_code

    def get_latitude(self):
        latitude = self.data["geometry"]["coordinates"][1]
        return latitude

    def get_longitude(self):
        longitude = self.data["geometry"]["coordinates"][0]
        return longitude


class JsonRegionPointData(JsonPointData):
    """
    geojson形式の小地域ポイントデータを保持するクラス
    """

    def get_pref(self):
        pref = self.read_data(self.data["properties"]["PREF_NAME"])
        return pref

    def get_city(self):
        city = self.read_data(self.data["properties"]["CITY_NAME"])
        return city

    def get_district(self):
        district = self.read_data(self.data["properties"]["S_NAME"])
        return district

    @staticmethod
    def read_data(data):
        if data is None:
            return ""
        else:
            return data


class JsonFacultyData(JsonPointData, metaclass=ABCMeta):

    @abstractmethod
    def get_name(self):
        pass


class JsonPostOfficeData(JsonFacultyData):

    def get_name(self):
        name = self.data["properties"]["P30_005"]
        return name


class JsonElementarySchoolData(JsonFacultyData):

    def __init__(self, data):
        super().__init__(data)
        if data["properties"]["P29_004"] != "16001":
            # 小学校でないデータにはエラーを返す
            raise NotTargetFacultyException

    def get_name(self):
        name = self.data["properties"]["P29_005"]
        return name


class JsonNewTownData(JsonFacultyData):

    def get_name(self):

        name = self.data["properties"]["P26_005"]
        if name is None:
            name = self.data["properties"]["P26_006"]
            if name is None:
                name = self.data["properties"]["P26_004"]
        return name


class JsonMichinoekiData(JsonFacultyData):

    def get_name(self):
        return self.data["properties"]["P35_006"]


class JsonStationData(JsonFacultyData):

    def get_name(self):
        return self.data["properties"]["N02_003"] + " " + self.data["properties"]["N02_005"] + "駅"


class JsonAbandonedStationData(JsonFacultyData):

    def get_name(self):
        # {"name": [路線名] [駅名]駅, "abandoned_year_1": [廃止年-1], "id": [id]}
        name = {"name": self.data["properties"]["N05_002"] + " " + self.data["properties"]["N05_011"] + "駅",
                "abandoned_year_1": self.data["properties"]["N05_005e"],
                "id": self.data["properties"]["N05_006"]}

        return name


class JsonResearchInstituteData(JsonFacultyData):

    def __init__(self, data):
        super().__init__(data)
        if self.data["properties"]["P16_002"] == 6:
            # 企業研究施設は除く
            raise NotTargetFacultyException

    def get_name(self):
        return self.data["properties"]["P16_001"]


class NotTargetFacultyException(Exception):
    """
    対象施設でないとき吐く例外（例：小学校でない）
    """
    pass
