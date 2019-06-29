from library.faculty_dao import FacultyDAO
import settings.file_path as fp
from settings.constants import *
from library.island_checker import IslandChecker
from library.setting import RegionSetting


def main(faculty_setting):

    if faculty_setting.faculty == ELEMENTARY_SCHOOL:
        input_file = fp.elementary_schools_file
    elif faculty_setting.faculty == POST_OFFICE:
        input_file = fp.post_office_file
    else:
        raise Exception("施設タイプ名が不正です")

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 施設を条件に従って抽出
    faculties = extract_faculties(faculty_points, faculty_setting)

    # 結果
    result = Result(faculties, faculty_setting)

    return result


def extract_faculties(faculty_points, fs):

    extracted_faculties = []
    ic = IslandChecker(fp.island_data_file)
    for f in faculty_points:

        # 地域チェック
        if fs.region == "全国":
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
        if ic.is_island(f):
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
    def __init__(self, faculties, setting):
        self.faculties = faculties
        self.setting = setting
        self.region = setting.region
