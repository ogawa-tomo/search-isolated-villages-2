import json
from library.setting import RegionSetting
from tqdm import tqdm
from library.point import *
from library import common_function as cf
from settings.constants import *
from abc import ABCMeta, abstractmethod


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

    def get_points(self):
        return self.points


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


class NotTargetFacultyException(Exception):
    """
    対象施設でないとき吐く例外（例：小学校でない）
    """
    pass
