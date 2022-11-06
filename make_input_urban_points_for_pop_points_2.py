import settings.file_path as fp
from library.point_dao import PopPointDAO
from library.setting import RegionSetting
from tqdm import tqdm
from library.output_map import OutputMap
from settings.constants import *
import sys

try:
    year = sys.argv[1]
except IndexError:
    raise Exception('引数でデータ年を指定してください')

def main():
    """
    都道府県ごとに人口分布と秘境上位のマーカーを表示するhtmlを作成する
    """

    # 人口データの読み込み
    input_file = fp.pop_point_file_for_maximum_urban_points(year)
    dao = PopPointDAO(input_file)
    pop_points = dao.read_pop_point_data(read_neighbors=False)

    # 都道府県ごとにhtmlを作って格納
    print("都道府県ごとにhtmlを作って格納")
    for pref in tqdm(RegionSetting.get_all_prefs()):
        
        points_in_pref = extract_points_by_pref(pop_points, pref)

        map_file = os.path.join(fp.max_urban_points_map_dir(year), pref + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(points_in_pref, OUTPUT_MAP_NUM, pref=pref)


def extract_points_by_pref(all_points, pref):

    points_in_pref = []
    for p in all_points:
        if p.pref == pref:
            points_in_pref.append(p)
    return points_in_pref

if __name__ == "__main__":
    main()