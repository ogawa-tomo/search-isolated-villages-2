from library.village_dao import VillageDAO
import settings.file_path as fp
from settings.constants import *
from library.setting import RegionSetting
import random


def main(region):

    # 集落データを読み込み
    dao = VillageDAO(fp.villages_file)
    villages = dao.read_village_data()

    # 集落データを抽出
    villages = extract_villages(villages, region)

    num = len(villages)
    print(str(num) + "集落")

    # village = random.choice(villages)
    idx = int(random.random() * num)
    village = villages[idx]

    # マップ出力
    map_file = os.path.join(fp.mesh_map_dir, village.pref + ".html")

    result = Result(region, village, map_file, num, idx)

    return result


def extract_villages(villages, region):

    extracted_villages = []
    for v in villages:

        # 地域チェック
        if region == ZENKOKU:
            pass
        elif RegionSetting.is_region(region):
            # 地域指定のとき
            if RegionSetting.get_region_by_pref(v.pref) != region:
                continue
        elif RegionSetting.is_pref(region):
            # 都道府県指定のとき
            if v.pref != region:
                continue
        else:
            raise Exception("地域が不正です")

        # 50人以下かつ都会度30000以下
        # または
        # 500人以下かつ10メッシュ以下かつ10000以下
        c1 = v.population <= 50 and v.urban_point < 30000
        c2 = v.population <= 500 and v.size <= 10 and v.urban_point < 10000
        if c1 or c2:
            extracted_villages.append(v)
    return extracted_villages


class Result(object):

    def __init__(self, region, village, map_file, num, idx):
        self.region = region
        self.village = village
        self.map_file = map_file
        self.num = num
        self.idx = idx
