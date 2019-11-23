from library.faculty_dao import FacultyDAO
import settings.file_path as fp
from settings.constants import *
from library.island_checker import IslandChecker
from library.setting import RegionSetting
from library.output_map import OutputMap
import time


def main(faculty_setting):

    if faculty_setting.faculty == ELEMENTARY_SCHOOL:
        input_file = fp.elementary_schools_file
    elif faculty_setting.faculty == POST_OFFICE:
        input_file = fp.post_office_file
    elif faculty_setting.faculty == NEW_TOWN:
        input_file = fp.new_town_file
    elif faculty_setting.faculty == MICHINOEKI:
        input_file = fp.michinoeki_file
    elif faculty_setting.faculty == STATION:
        input_file = fp.station_file
    elif faculty_setting.faculty == ABANDONED_STATION:
        input_file = fp.abandoned_station_file
    elif faculty_setting.faculty == BUS_STOP:
        input_file = fp.bus_stop_file
    else:
        raise Exception("施設タイプ名が不正です")

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 施設を条件に従って抽出
    faculties = extract_faculties(faculty_points, faculty_setting)

    # マップ出力
    map_file = os.path.join(fp.output_dir, "map_" + str(time.time()).replace(".", "") + ".html")
    output_map = OutputMap(map_file)
    output_map.output_map(faculties, OUTPUT_MAP_NUM)

    # 結果
    result = Result(faculties, faculty_setting, OUTPUT_HTML_NUM, map_file)

    return result


def extract_faculties(faculty_points, fs):

    extracted_faculties = []
    for f in faculty_points:

        # 地域チェック
        if fs.region == ZENKOKU:
            pass
        elif RegionSetting.is_region(fs.region):
            # 地域指定のとき
            if RegionSetting.get_region_by_pref(f.pref) != fs.region:
                continue
        elif RegionSetting.is_pref(fs.region):
            # 都道府県指定のとき
            if f.pref != fs.region:
                continue

        # 島チェック
        if fs.island_setting == INCLUDE_ISLANDS:
            # どちらでも通す
            pass
        elif fs.island_setting == EXCLUDE_ISLANDS:
            if f.is_island:
                # 島だったら通さない
                continue
        elif fs.island_setting == ONLY_ISLANDS:
            if not f.is_island:
                # 本土だったら通さない
                continue

        # キーワードチェック
        if fs.key_words != "":
            key_words = fs.key_words.split()
            address = f.pref + f.city + f.district + " " + f.name
            key_word_in_address = True
            for key_word in key_words:
                if key_word not in address:
                    # 住所に含まれていないキーワードが1つでもあればFalse
                    key_word_in_address = False
                    break
            if not key_word_in_address:
                continue

        extracted_faculties.append(f)

    return extracted_faculties


class Result(object):
    """
    結果を記録するクラス
    """
    def __init__(self, faculties, setting, num, map_file):
        self.faculties = faculties
        self.setting = setting
        self.region = setting.region
        self.num = num
        self.map_file = map_file
