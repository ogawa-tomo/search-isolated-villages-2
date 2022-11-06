from library.faculty_dao import FacultyDAO
from library.r774_point_dao import R774PointDAO
import settings.file_path as fp
from settings.constants import *
from library.island_checker import IslandChecker
from library.setting import RegionSetting, Result
from library.output_map import OutputMap
import time
import library.common_function as cf


def main(faculty_setting):

    input_file = fp.get_faculty_csv_file(faculty_setting.faculty, faculty_setting.year)

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 施設を条件に従って抽出
    # faculties = extract_faculties(faculty_points, faculty_setting)
    faculties = faculty_setting.extract_objects(faculty_points)

    # マップ出力
    if RegionSetting.is_pref(faculty_setting.region):
        # 都道府県の場合は、既に出力してある都道府県別のhtmlファイル（人口分布つき）
        map_file = os.path.join(fp.get_faculty_mesh_map_dir(faculty_setting.faculty), faculty_setting.region + ".html")
    else:
        # 都道府県でない場合は、その場でmapを作る（人口分布なし）

        # r774データを読み込み、条件に従って抽出
        r774_dao = R774PointDAO(fp.r774_file)
        r774_points = r774_dao.read_r774_point_data()
        # r774_points = extract_r774_points(r774_points, faculty_setting)
        r774_points = faculty_setting.extract_r774_points(r774_points)

        # map作成
        map_file = os.path.join(fp.output_dir, "map_" + str(time.time()).replace(".", "") + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(faculties, OUTPUT_MAP_NUM)
        output_map.add_r774_points(r774_points)

    # 結果
    # result = Result(faculties, faculty_setting, OUTPUT_HTML_NUM, map_file)
    result = Result(faculties, faculty_setting, map_file)

    return result


# def extract_faculties(faculty_points, fs):

#     extracted_faculties = []
#     for f in faculty_points:

#         # 地域チェック
#         if fs.region == ZENKOKU:
#             pass
#         elif RegionSetting.is_region(fs.region):
#             # 地域指定のとき
#             if RegionSetting.get_region_by_pref(f.pref) != fs.region:
#                 continue
#         elif RegionSetting.is_pref(fs.region):
#             # 都道府県指定のとき
#             if f.pref != fs.region:
#                 continue

#         # 島チェック
#         if fs.island_setting == INCLUDE_ISLANDS:
#             # どちらでも通す
#             pass
#         elif fs.island_setting == EXCLUDE_ISLANDS:
#             if f.is_island:
#                 # 島だったら通さない
#                 continue
#         elif fs.island_setting == ONLY_ISLANDS:
#             if not f.is_island:
#                 # 本土だったら通さない
#                 continue

#         # キーワードチェック
#         if fs.key_words != "":
#             key_words = fs.key_words.split()
#             address = f.pref + f.city + f.district + " " + f.name
#             key_word_in_address = True
#             for key_word in key_words:
#                 if key_word not in address:
#                     # 住所に含まれていないキーワードが1つでもあればFalse
#                     key_word_in_address = False
#                     break
#             if not key_word_in_address:
#                 continue

#         extracted_faculties.append(f)

#     return extracted_faculties


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
#     def __init__(self, faculties, setting, num, map_file):
#         self.faculties = faculties
#         self.setting = setting
#         self.region = setting.region
#         self.num = num
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
#         for f in self.faculties:
#             lat_list.append(f.latitude)
#             lon_list.append(f.longitude)
#         lat = (min(lat_list) + max(lat_list)) / 2
#         lon = (min(lon_list) + max(lon_list)) / 2
#         # url = "/mesh_map?lat=" + str(lat) + "&lon=" + str(lon) + "&zoom=" + "10&map_file=" + self.map_file
#         url = cf.get_mesh_map_get_url(lat, lon, ZOOM_DEFAULT, self.map_file)
#         return url
