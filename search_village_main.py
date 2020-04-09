from library.village_dao import VillageDAO
from library.pop_polygon_dao import PopPolygonDAO
import settings.file_path as fp
from library.island_checker import IslandChecker
from library.setting import RegionSetting
from library.output_map import OutputMap
from settings.constants import *
import time


def main(s):

    # 集落データを読み込み
    dao = VillageDAO(fp.villages_file)
    villages = dao.read_village_data()

    # 集落データを条件に従って抽出
    villages = extract_villages(villages, s)

    # マップ出力
    map_file = os.path.join(fp.output_dir, "map_" + str(time.time()).replace(".", "") + ".html")
    output_map = OutputMap(map_file)
    output_map.output_map(villages, OUTPUT_MAP_NUM)

    # ポリゴン人口データを読み込み
    # dao = PopPolygonDAO(fp.pop_polygon_file)
    # polygons = dao.read_pop_polygon_data()
    #
    # # ポリゴンデータを条件に従って抽出
    # polygons = extract_objects(polygons, s)

    # 設定に従ってポリゴンを抽出
    polygons = read_polygons(fp.pop_polygon_dir, s)

    # ポリゴンをマップに追加
    output_map.add_polygons(polygons)

    # 結果
    result = Result(villages, s, map_file)

    return result


def extract_objects(objects, s):
    """
    集落またはポリゴンを条件に従って抽出する
    :param objects:
    :param s:
    :return:
    """
    extracted_objects = []
    for ob in objects:

        # 地域チェック
        if s.region == ZENKOKU:
            pass
        elif RegionSetting.is_region(s.region):
            # 地域指定のとき
            if RegionSetting.get_region_by_pref(ob.pref) != s.region:
                continue
        elif RegionSetting.is_pref(s.region):
            # 都道府県指定のとき
            if ob.pref != s.region:
                continue
        else:
            raise Exception("地域が不正です")

        # 島チェック
        if s.island_setting == INCLUDE_ISLANDS:
            # どちらでも通す
            pass
        elif s.island_setting == EXCLUDE_ISLANDS:
            if ob.is_island:
                # 島だったら通さない
                continue
        elif s.island_setting == ONLY_ISLANDS:
            if not ob.is_island:
                # 本土だったら通さない
                continue
        else:
            raise Exception("離島設定が不正です")

        # キーワードチェック
        if s.key_words != "":
            key_words = s.key_words.split()
            address = ob.pref + ob.city + ob.district
            key_word_in_address = True
            for key_word in key_words:
                if key_word not in address:
                    # 住所に含まれていないキーワードが1つでもあればFalse
                    key_word_in_address = False
                    break
            if not key_word_in_address:
                continue

        extracted_objects.append(ob)

    return extracted_objects


def extract_villages(villages, s):
    """
    集落を条件に従って抽出する
    :param villages:
    :param s:
    :return:
    """

    all_villages = extract_objects(villages, s)
    extracted_villages = []

    for v in all_villages:

        # 人口・サイズチェックのみ追加
        if s.village_pop_lower_limit <= v.population <= s.village_pop_upper_limit \
                and s.village_size_lower_limit <= v.size <= s.village_size_upper_limit:
            extracted_villages.append(v)

    return extracted_villages


def read_polygons(pop_polygon_dir, s):
    """
    設定で指定された都道府県のポリゴンを抽出する
    :param pop_polygon_dir:
    :param s:
    :return:
    """

    # ポリゴンを抽出する都道府県
    polygon_prefs = []
    if s.region == ZENKOKU:
        # 全部
        polygon_prefs = RegionSetting.get_all_prefs()
    elif RegionSetting.is_region(s.region):
        # 地域指定のとき、地域に含まれる都道府県
        polygon_prefs = RegionSetting.get_region_prefs(s.region)
    elif RegionSetting.is_pref(s.region):
        # 都道府県指定のとき、その都道府県
        polygon_prefs.append(s.region)
    else:
        raise Exception("地域が不正です")

    # 抽出するポリゴン
    polygons = []
    for pref in polygon_prefs:
        dao = PopPolygonDAO(pop_polygon_dir + "/" + pref + ".csv")
        polygons.extend(dao.read_pop_polygon_data())

    return polygons


class Result(object):
    """
    結果を記録するクラス
    """
    def __init__(self, sorted_villages, setting, map_file):
        self.sorted_villages = sorted_villages
        self.setting = setting
        self.region = setting.region
        self.num = OUTPUT_HTML_NUM
        self.map_file = map_file
        self.output_map_num = OUTPUT_MAP_NUM

    def get_mesh_map_get_url(self):

        # 地図の中心点
        lat_list = []
        lon_list = []
        for v in self.sorted_villages:
            lat_list.append(v.latitude)
            lon_list.append(v.longitude)
        lat = (min(lat_list) + max(lat_list)) / 2
        lon = (min(lon_list) + max(lon_list)) / 2
        url = "/mesh_map?lat=" + str(lat) + "&lon=" + str(lon) + "&zoom=" + "10" + self.map_file
        return url
