import sys
from library.faculty_dao import FacultyDAO
import settings.file_path as fp
from library.setting import RegionSetting
from library.pop_polygon_dao import PopPolygonDAO
from library.r774_point_dao import R774PointDAO
from tqdm import tqdm
from library.output_map import OutputMap
from settings.constants import *


def main():
    """
    都道府県ごとに人口分布と秘境上位のマーカーを表示するhtmlを作成する
    :return:
    """

    faculty_type = sys.argv[1]

    # 施設データの読み込み
    input_file = fp.get_faculty_csv_file(faculty_type)
    dao = FacultyDAO(input_file)
    all_faculties = dao.read_faculty_point_data()

    # r774データの読み込み
    r774_dao = R774PointDAO(fp.r774_file)
    all_r774_points = r774_dao.read_r774_point_data()

    # 都道府県ごとに、htmlを作って格納
    print("都道府県ごとにメッシュ図を作って保存")
    for pref in tqdm(RegionSetting.get_all_prefs()):

        # ポリゴンデータの読み込み
        dao = PopPolygonDAO(fp.pop_polygon_dir + "/" + pref + ".csv")
        polygons_in_pref = dao.read_pop_polygon_data()

        # 施設データの読み込み
        faculties_inf_pref = extract_points_by_pref(all_faculties, pref)

        # R774データの読み込み
        r774_points_in_pref = extract_points_by_pref(all_r774_points, pref)

        # マップづくり
        map_file = os.path.join(fp.get_faculty_mesh_map_dir(faculty_type), pref + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(faculties_inf_pref, OUTPUT_MAP_NUM, pref=pref)
        output_map.add_polygons(polygons_in_pref)
        output_map.add_r774_points(r774_points_in_pref)


def extract_points_by_pref(all_points, pref):

    points_in_pref = []
    for f in all_points:
        if f.pref == pref:
            points_in_pref.append(f)
    return points_in_pref


if __name__ == "__main__":
    main()
