from library.point_dao import PopPointDAO
from library.village_dao import VillageDAO
from library.pop_polygon_dao import PopPolygonDAO
from library.r774_point_dao import R774PointDAO
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

    # r774データの読み込み
    r774_dao = R774PointDAO(fp.r774_file)
    all_r774_points = r774_dao.read_r774_point_data()

    # 都道府県ごとに、htmlを作って格納
    print("都道府県ごとにメッシュ図を作って保存")
    for pref in tqdm(RegionSetting.get_all_prefs()):

        # ポリゴンデータの読み込み
        dao = PopPolygonDAO(fp.pop_polygon_dir + "/" + pref + ".csv")
        polygons_in_pref = dao.read_pop_polygon_data()

        # 集落データの読み込み
        villages_in_pref = extract_points_by_pref(all_villages, pref)

        # R774データの読み込み
        r774_points_in_pref = extract_points_by_pref(all_r774_points, pref)

        # マップづくり
        map_file = os.path.join(fp.mesh_map_dir, pref + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(villages_in_pref, OUTPUT_MAP_NUM, pref=pref)
        output_map.add_polygons(polygons_in_pref)
        output_map.add_r774_points(r774_points_in_pref)


def extract_points_by_pref(all_points, pref):
    """
    都道府県別にポイントを抽出する
    :param all_points:
    :param pref:
    :return:
    """
    points_in_pref = []
    for v in all_points:
        if v.pref == pref:
            points_in_pref.append(v)
    return points_in_pref


if __name__ == "__main__":
    main()
