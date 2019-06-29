from library.village_dao import VillageDAO
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

    # 結果
    result = Result(villages, s, OUTPUT_HTML_NUM)

    return result


def extract_villages(villages, s):
    """
    集落を条件に従って抽出する
    :param villages:
    :param s:
    :return:
    """

    extracted_villages = []
    # ic = IslandChecker(fp.island_data_file)
    for v in villages:

        # 地域チェック
        if s.region == "全国":
            pass
        elif RegionSetting.is_region(s.region):
            # 地域指定のとき
            if RegionSetting.get_region_by_pref(v.pref) != s.region:
                continue
        elif RegionSetting.is_pref(s.region):
            # 都道府県指定のとき
            if v.pref != s.region:
                continue

        # 島チェック（人口点読み込み側で済）
        # if ic.is_island(v):
        #     continue

        # キーワードチェック
        if s.key_words != "":
            key_words = s.key_words.split()
            address = v.pref + v.city + v.district
            key_word_in_address = True
            for key_word in key_words:
                if key_word not in address:
                    # 住所に含まれていないキーワードが1つでもあればFalse
                    key_word_in_address = False
                    break
            if not key_word_in_address:
                continue

        # 人口・サイズチェック
        if s.village_pop_lower_limit <= v.population <= s.village_pop_upper_limit \
                and s.village_size_lower_limit <= v.size <= s.village_size_upper_limit:
            extracted_villages.append(v)

    return extracted_villages


class Result(object):
    """
    結果を記録するクラス
    """
    def __init__(self, sorted_villages, setting, num):
        self.sorted_villages = sorted_villages
        self.setting = setting
        self.region = setting.region
        self.num = num
