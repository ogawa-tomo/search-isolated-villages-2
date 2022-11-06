import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
from library.village_dao import VillageDAO
from library.json_data_reader import *
from tqdm import tqdm
import settings.file_path as fp
from library.point_dao import PopPointDAO
from make_input_main_2 import PointContainer
# import library.common_function as cf
import library.make_input_functions as mif

"""
人口ポイントデータの隣接関係から集落を抽出する
集落の都会度を計算する
集落のcsvデータを吐き出す
"""

try:
    year = sys.argv[1]
except IndexError:
    raise Exception('引数でデータ年を指定してください')

def main():

    # 人口データ読み込み
    dao = PopPointDAO(fp.pop_point_file(year))
    pop_points = dao.read_pop_point_data()

    # 集落データマネージャクラス
    # vpm = VillagePointManager(pop_points)

    # 集落の抽出
    # vpm.extract_villages(VILLAGE_SIZE_UPPER_LIMIT)
    villages = extract_villages(pop_points, VILLAGE_SIZE_UPPER_LIMIT)

    # 全人口点のコンテナ
    all_pop_point_container = PointContainer()
    all_pop_point_container.register_points(pop_points)

    # 本土と離島の人口点のコンテナ
    mainland_pop_point_container = PointContainer()
    island_pop_point_container = PointContainer()
    mif.register_mainland_island_container(pop_points, mainland_pop_point_container, island_pop_point_container)

    # 本土と離島の集落のコンテナ
    mainland_village_container = PointContainer()
    island_village_container = PointContainer()
    mif.register_mainland_island_container(villages, mainland_village_container, island_village_container)

    # 都会度の計算（本土の集落の都会度を、本土の人口点で計算）
    register_urban_point(mainland_village_container, mainland_pop_point_container)

    # 都会度の計算（離島の集落の都会度を、全人口点で計算）
    register_urban_point(island_village_container, all_pop_point_container)

    # 並べ替え
    villages = sorted(villages)

    # 抽出した集落をtxtファイルに保存
    dao = VillageDAO(fp.villages_file(year))
    dao.make_village_data(villages)


def extract_villages(pop_points, village_size_upper_limit):
    """
    人口点データから集落を抽出する
    :param pop_points:
    :param village_size_upper_limit:
    :return:
    """
    extracted_villages = []
    registered = []  # 既に集落に登録された点
    print("集落を抽出中")
    for p in tqdm(pop_points):
        if p in registered:
            continue

        # p周辺の人口ポイントを登録
        try:
            village_points = p.get_my_village_points([], village_size_upper_limit)
        except cf.TooBigVillageException:
            # サイズが閾値を超えた場合には例外が返ってくる
            continue

        registered.extend(village_points)

        v = Village()
        v.make_village(village_points)
        extracted_villages.append(v)

    return extracted_villages


def register_urban_point(village_container, pop_point_container):
    """
    集落の都会度を、人口点より計算する
    :param village_container:
    :param pop_point_container:
    :return:
    """
    for calc_segment in RegionSetting.get_calc_segments():
        print(calc_segment + "の集落の都会度を計算中")
        for v in tqdm(village_container.get_points_by_calc_segment(calc_segment)):

            for p in pop_point_container.get_points_by_calc_segment(calc_segment):

                # -----集落周縁からの都会度（集落内メッシュを計算に含めず、最短距離で計算）
                if p in v.points:
                    continue
                dist = v.get_distance(p)
                v.urban_point += cf.calc_urban_point(p.population, dist)

            v.urban_point_round = round(v.urban_point, LAT_LON_ROUND)  # html表示用


if __name__ == "__main__":
    main()
