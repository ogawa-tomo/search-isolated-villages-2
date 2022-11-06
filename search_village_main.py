from library.village_dao import VillageDAO
from library.pop_polygon_dao import PopPolygonDAO
from library.r774_point_dao import R774PointDAO
import settings.file_path as fp
from library.island_checker import IslandChecker
from library.setting import RegionSetting, Result
from library.output_map import OutputMap
from settings.constants import *
import time
import library.common_function as cf


def main(s):

    # 集落データを読み込み
    dao = VillageDAO(fp.villages_file(s.year))
    villages = dao.read_village_data()

    # 集落データを条件に従って抽出
    # villages = extract_villages(villages, s)
    villages = s.extract_villages(villages)

    # マップ出力
    if RegionSetting.is_pref(s.region):
        # 都道府県の場合は、既に出力してある都道府県別のhtmlファイル（人口分布つき）
        map_file = os.path.join(fp.mesh_map_dir(s.year), s.region + ".html")
    else:
        # 都道府県でない場合は、その場でmapを作る（人口分布なし）

        # r774データを読み込み、条件に従って抽出
        r774_dao = R774PointDAO(fp.r774_file)
        r774_points = r774_dao.read_r774_point_data()
        # r774_points = extract_r774_points(r774_points, s)
        r774_points = s.extract_r774_points(r774_points)

        # map作成
        map_file = os.path.join(fp.output_dir, "map_" + str(time.time()).replace(".", "") + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(villages, OUTPUT_MAP_NUM)
        output_map.add_r774_points(r774_points)

    # 結果
    result = Result(villages, s, map_file)

    return result


# def extract_objects(objects, s):
#     """
#     集落またはポリゴンを条件に従って抽出する
#     :param objects:
#     :param s:
#     :return:
#     """
#     extracted_objects = []
#     for ob in objects:

#         # 地域チェック
#         if s.region == ZENKOKU:
#             pass
#         elif RegionSetting.is_region(s.region):
#             # 地域指定のとき
#             if RegionSetting.get_region_by_pref(ob.pref) != s.region:
#                 continue
#         elif RegionSetting.is_pref(s.region):
#             # 都道府県指定のとき
#             if ob.pref != s.region:
#                 continue
#         else:
#             raise Exception("地域が不正です")

#         # 島チェック
#         if s.island_setting == INCLUDE_ISLANDS:
#             # どちらでも通す
#             pass
#         elif s.island_setting == EXCLUDE_ISLANDS:
#             if ob.is_island:
#                 # 島だったら通さない
#                 continue
#         elif s.island_setting == ONLY_ISLANDS:
#             if not ob.is_island:
#                 # 本土だったら通さない
#                 continue
#         else:
#             raise Exception("離島設定が不正です")

#         # キーワードチェック
#         if s.key_words != "":
#             key_words = s.key_words.split()
#             address = ob.pref + ob.city + ob.district
#             key_word_in_address = True
#             for key_word in key_words:
#                 if key_word not in address:
#                     # 住所に含まれていないキーワードが1つでもあればFalse
#                     key_word_in_address = False
#                     break
#             if not key_word_in_address:
#                 continue

#         extracted_objects.append(ob)

#     return extracted_objects


# def extract_villages(villages, s):
#     """
#     集落を条件に従って抽出する
#     :param villages:
#     :param s:
#     :return:
#     """

#     all_villages = extract_objects(villages, s)
#     extracted_villages = []

#     for v in all_villages:

#         # 人口・サイズチェックのみ追加
#         if s.village_pop_lower_limit <= v.population <= s.village_pop_upper_limit \
#                 and s.village_size_lower_limit <= v.size <= s.village_size_upper_limit:
#             extracted_villages.append(v)

#     return extracted_villages


# def extract_r774_points(r774_points, s):
#     """
#     r774ポイントを条件に従って抽出する
#     :param r774_points:
#     :param s:
#     :return:
#     """

#     extracted_points = []
#     for p in r774_points:

#         # 地域チェック
#         if s.region == ZENKOKU:
#             pass
#         elif RegionSetting.is_region(s.region):
#             # 地域指定のとき
#             if RegionSetting.get_region_by_pref(p.pref) != s.region:
#                 continue
#         elif RegionSetting.is_pref(s.region):
#             # 都道府県指定のとき
#             if p.pref != s.region:
#                 continue
#         else:
#             raise Exception("地域が不正です")

#         # キーワードチェック
#         if s.key_words != "":
#             key_words = s.key_words.split()
#             address = p.pref + p.city + p.district + p.name
#             key_word_in_address = True
#             for key_word in key_words:
#                 if key_word not in address:
#                     # 住所に含まれていないキーワードが1つでもあればFalse
#                     key_word_in_address = False
#                     break
#             if not key_word_in_address:
#                 continue

#         extracted_points.append(p)

#     return extracted_points


# class Result(object):
#     """
#     結果を記録するクラス
#     """
#     def __init__(self, sorted_villages, setting, map_file):
#         self.sorted_villages = sorted_villages
#         self.setting = setting
#         self.region = setting.region
#         self.num = OUTPUT_HTML_NUM
#         self.map_file = map_file
#         self.output_map_num = OUTPUT_MAP_NUM

#         # 都道府県判定（メッシュ地図を表示するかの判断のため）
#         if RegionSetting.is_pref(setting.region):
#             self.is_pref = True
#         else:
#             self.is_pref = False

#     def get_mesh_map_get_url(self):

#         # 地図の中心点
#         lat_list = []
#         lon_list = []
#         for v in self.sorted_villages:
#             lat_list.append(v.latitude)
#             lon_list.append(v.longitude)
#         lat = (min(lat_list) + max(lat_list)) / 2
#         lon = (min(lon_list) + max(lon_list)) / 2
#         # url = "/mesh_map?lat=" + str(lat) + "&lon=" + str(lon) + "&zoom=" + "10&map_file=" + self.map_file
#         url = cf.get_mesh_map_get_url(lat, lon, ZOOM_DEFAULT, self.map_file)
#         return url
