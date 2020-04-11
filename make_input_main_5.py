from library.point_dao import PopPointDAO
from library.village_dao import VillageDAO
from library.pop_polygon_dao import PopPolygonDAO
import settings.file_path as fp
from library.setting import RegionSetting
from library.output_map import OutputMap
from settings.constants import *
import os
from tqdm import tqdm


def main():
    """
    都道府県ごとに人口分布と秘境上位のマーカーを表示するhtmlを作成する
    :return:
    """

    # 集落データの読み込み
    dao = VillageDAO(fp.villages_file)
    all_villages = dao.read_village_data()

    # 都道府県ごとに、htmlを作って格納
    print("都道府県ごとにメッシュ図を作って保存")
    for pref in tqdm(RegionSetting.get_all_prefs()):

        # ポリゴンデータの読み込み
        dao = PopPolygonDAO(fp.pop_polygon_dir + "/" + pref + ".csv")
        polygons_in_pref = dao.read_pop_polygon_data()

        # 集落データの読み込み
        villages_in_pref = extract_villages_by_pref(all_villages, pref)
        villages_in_pref = villages_in_pref

        # マップづくり
        map_file = os.path.join(fp.mesh_map_dir, pref + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(villages_in_pref, OUTPUT_MAP_NUM, pref=pref)
        output_map.add_polygons(polygons_in_pref)


def extract_villages_by_pref(all_villages, pref):
    """
    都道府県別に集落を抽出する
    :param all_villages:
    :param pref:
    :return:
    """
    villages_in_pref = []
    for v in all_villages:
        if v.pref == pref:
            villages_in_pref.append(v)
    return villages_in_pref


if __name__ == "__main__":
    main()
