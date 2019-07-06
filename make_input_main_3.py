import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
import glob
from library.village_dao import VillageDAO
from library.json_data_reader import *
from library.pop_data_reader import *
from library.island_checker import IslandChecker
from tqdm import tqdm
import settings.file_path as fp
from library.point_dao import PopPointDAO
import make_input_main_2
from make_input_main_2 import PointContainer


def main():

    # 人口データ読み込み
    dao = PopPointDAO(fp.pop_point_file)
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
    make_input_main_2.register_mainland_island_container(
        pop_points, mainland_pop_point_container, island_pop_point_container)

    # 本土と離島の集落のコンテナ
    mainland_village_container = PointContainer()
    island_village_container = PointContainer()
    make_input_main_2.register_mainland_island_container(
        villages, mainland_village_container, island_village_container)

    # 都会度の計算（本土の集落の都会度を、本土の人口点で計算）
    register_urban_point(mainland_village_container, mainland_pop_point_container)

    # 都会度の計算（離島の集落の都会度を、全人口点で計算）
    register_urban_point(island_village_container, all_pop_point_container)

    # 並べ替え
    villages = sorted(villages)

    # 抽出した集落をtxtファイルに保存
    dao = VillageDAO(fp.villages_file)
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

            v.urban_point_round = round(v.urban_point, 4)  # html表示用


# class VillagePointManager(object):
#
#     def __init__(self, pop_points):
#
#         self.pop_points = pop_points
#         self.pop_points_by_calc_segment = {}
#         for calc_segment in RegionSetting.get_calc_segments():
#             self.pop_points_by_calc_segment[calc_segment] = []
#         self.allocate_pop_points_to_segments()
#
#         self.villages = []
#         self.villages_by_calc_segment = {}
#         for calc_segment in RegionSetting.get_calc_segments():
#             self.villages_by_calc_segment[calc_segment] = []
#
#     def allocate_pop_points_to_segments(self):
#         """
#         ポイントをセグメントに振り分ける関数
#         :return:
#         """
#         for p in self.pop_points:
#             calc_segment = RegionSetting.get_calc_segment_by_pref(p.pref)
#             self.pop_points_by_calc_segment[calc_segment].append(p)
#
#     def extract_villages(self, village_size_upper_limit):
#         """
#         集落の抽出
#         :param village_size_upper_limit:
#         :return:
#         """
#
#         registered = []  # 既に集落に登録された点
#         print("集落を抽出中")
#         for p in tqdm(self.pop_points):
#             if p in registered:
#                 continue
#
#             # p周辺の人口集中ポイントを登録
#             try:
#                 village_points = p.get_my_village_points([], village_size_upper_limit)
#             except cf.TooBigVillageException:
#                 # サイズが閾値を超えた場合には例外が返ってくる
#                 continue
#
#             registered.extend(village_points)
#
#             v = Village()
#             v.make_village(village_points)
#
#             self.villages.append(v)
#             calc_segment = RegionSetting.get_calc_segment_by_pref(v.pref)
#             self.villages_by_calc_segment[calc_segment].append(v)
#
#     def register_urban_point(self):
#         """
#         各集落の都会度を計算する
#         :return:
#         """
#         for calc_segment in RegionSetting.get_calc_segments():
#             print(calc_segment + "の集落の都会度を計算中")
#             for v in tqdm(self.villages_by_calc_segment[calc_segment]):
#
#                 for p in self.pop_points_by_calc_segment[calc_segment]:
#
#                     # -----集落周縁からの都会度（集落内メッシュを計算に含めず、最短距離で計算）
#                     if p in v.points:
#                         continue
#                     dist = v.get_distance(p)
#                     v.urban_point += cf.calc_urban_point(p.population, dist)
#
#                 v.urban_point_round = round(v.urban_point, 4)  # html表示用
#
#         # ついでに並べ替え
#         self.villages = sorted(self.villages)
#
#     def get_villages(self):
#         return self.villages


if __name__ == "__main__":
    main()
