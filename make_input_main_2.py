import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
import glob
from library.json_data_reader import *
from library.pop_data_reader import *
from library.island_checker import IslandChecker
from tqdm import tqdm
import settings.file_path as fp
from library.point_dao import PopPointDAO


def main():

    # データマネージャクラス生成
    # ppm = PopPointManager()

    # ポイント・人口データ読み込み
    # ppm.read_pop_data(fp.raw_mesh_json_dir, fp.raw_pop_dir)
    all_points = read_pop_data(fp.raw_mesh_json_dir, fp.raw_pop_dir)

    # 小地域データ読み込み
    region_points = read_region_data(fp.raw_region_json_dir)

    # 住所データ読み込み
    # ppm.register_address(fp.raw_region_json_dir)
    register_address(all_points, region_points)

    # 住所をもとに本土の点と離島の点をそれぞれコンテナに登録
    mainland_point_container = PointContainer()
    island_point_container = PointContainer()
    register_mainland_island_container(all_points, mainland_point_container, island_point_container)

    # 隣接点の登録（本土と離島それぞれ）
    # ppm.register_neighbors()
    print("本土の隣接点を登録")
    register_neighbors(mainland_point_container)
    print("離島の隣接点を登録")
    register_neighbors(island_point_container)

    # 人口データの作成
    dao = PopPointDAO(fp.pop_point_file)
    dao.make_pop_point_data(all_points)


def read_pop_data(raw_mesh_json_dir, raw_pop_dir):
    """
    メッシュ点のJsonデータと人口データを読み、人口つきポイントオブジェクトのリストを返す
    :param raw_mesh_json_dir:
    :param raw_pop_dir:
    :return:
    """
    print("メッシュ人口データ読み込み")
    all_points = []
    id_count = 0

    # 1次メッシュ区分ごとに処理
    mesh_files = glob.glob(os.path.join(raw_mesh_json_dir, "*.txt"))
    for mesh_file in tqdm(mesh_files):

        # メッシュデータ読み込み
        mpd = JsonMeshPointDataReader(mesh_file)

        # 一次メッシュコード読み込み
        first_mesh_code = os.path.basename(mesh_file).lstrip("MESH0").rstrip(".txt")

        # 人口データ読み込み
        pop_file = os.path.join(raw_pop_dir, "tblT000876Q" + first_mesh_code + ".txt")
        try:
            prd = PopRawDataReader(pop_file)
        except FileNotFoundError:
            # 人口データがなければ無視
            continue
        pop_data = prd.get_data()

        # 各Pointごとに、Keyが一致する人口データを探し、人口点リストに格納（なければ格納しない）
        for point in mpd.get_points():
            for d in pop_data:
                if point.key_code == d.get_key_code():
                    point.population = d.get_population()
                    point.id = id_count
                    id_count += 1
                    all_points.append(point)
                    break

    return all_points


def read_region_data(raw_region_json_dir):
    """
    小地域データを読み込む
    :param raw_region_json_dir:
    :return:
    """
    # 小地域データ読み込み
    print("小地域データ読み込み")
    region_points = []
    region_files = glob.glob(os.path.join(raw_region_json_dir, "*txt"))
    for region_file in tqdm(region_files):
        rpd = JsonRegionPointDataReader(region_file)
        region_points.extend(rpd.get_points())
    return region_points


def register_address(all_points, region_points):
    """
    ポイントリストに住所を登録する
    :param all_points:
    :param region_points:
    :return:
    """
    # 小地域データ読み込み
    # print("小地域データ読み込み")
    # region_points = []
    # region_files = glob.glob(os.path.join(raw_region_json_dir, "*txt"))
    # for region_file in tqdm(region_files):
    #     rpd = JsonRegionPointDataReader(region_file)
    #     region_points.extend(rpd.get_points())

    # 各Pointごとに、一番近い小地域ポイントの住所を登録
    print("住所登録")
    for point in tqdm(all_points):

        min_dist = 0
        nearest_region_point = None
        for i, region_point in enumerate(region_points):
            dist = point.get_distance(region_point)
            if i == 0:
                min_dist = dist
                nearest_region_point = region_point
                continue
            if dist < min_dist:
                min_dist = dist
                nearest_region_point = region_point
        point.pref = nearest_region_point.pref
        point.city = nearest_region_point.city
        point.district = nearest_region_point.district


def register_mainland_island_container(all_points, mainland_point_container, island_point_container):
    """
    all_pointの住所を読み取り、離島判定をして本土と離島コンテナに振り分ける
    :param all_points:
    :param mainland_point_container:
    :param island_point_container:
    :return:
    """
    ic = IslandChecker(fp.island_data_file)
    print("島チェック")
    for point in tqdm(all_points):
        if ic.is_island(point):
            point.is_island = True
            island_point_container.add_point(point)
        else:
            point.is_island = False
            mainland_point_container.add_point(point)


def register_neighbors(point_container):
    """
    隣接点を登録する（セグメントごとに計算）
    :param point_container:
    :return:
    """
    for calc_segment in RegionSetting.get_calc_segments():
        print(calc_segment + "の隣接点を登録中")
        target_points = point_container.get_points_by_calc_segment(calc_segment).copy()
        for p in tqdm(point_container.get_points_by_calc_segment(calc_segment)):
            target_points.remove(p)
            for tp in target_points:
                if p.get_is_adjacent(tp):
                    p.add_neighbor(tp)
                    tp.add_neighbor(p)


class PointContainer(object):
    """
    点をセグメントごとに保持するクラス
    """
    def __init__(self):

        # self.__id_count = 0
        self.__points = []
        self.__points_by_calc_segment = {}
        for calc_segment in RegionSetting.get_calc_segments():
            self.__points_by_calc_segment[calc_segment] = []

    def add_point(self, point):
        """
        ポイントを追加する
        :param point:
        :return:
        """
        # ID管理
        # point.id = self.__id_count
        # self.__id_count += 1

        # 追加
        self.__points.append(point)
        calc_segment = RegionSetting.get_calc_segment_by_pref(point.pref)
        self.__points_by_calc_segment[calc_segment].append(point)

    def register_points(self, points):
        """
        ポイントリストを追加する
        :param points:
        :return:
        """
        for p in points:
            self.add_point(p)

    def get_points_by_calc_segment(self, calc_segment):
        """
        セグメントごとのポイントを返すメソッド
        :param calc_segment:
        :return:
        """
        return self.__points_by_calc_segment[calc_segment]

    def get_points(self):
        return self.__points



# class PopPointManager(object):
#     """
#     人口ポイントデータを管理するクラス
#     """
#
#     def __init__(self):
#
#         # 全ての点（人口ない点も含む）
#         self.all_points = []
#
#         # 人口点（島でない）
#         self.pop_point_id_count = 0
#         self.pop_points = []
#         self.pop_points_by_calc_segment = {}
#         for calc_segment in RegionSetting.get_calc_segments():
#             self.pop_points_by_calc_segment[calc_segment] = []
#
#         # 人口点（島）
#         self.pop_island_point_id_count = 0
#         self.pop_island_points = []
#         self.pop_island_points_by_calc_segment = {}
#         for calc_segment in RegionSetting.get_calc_segments():
#             self.pop_island_points_by_calc_segment[calc_segment] = []
#
#         # 集落
#         self.villages = []
#         self.villages_by_calc_segment = {}
#         for calc_segment in RegionSetting.get_calc_segments():
#             self.villages_by_calc_segment[calc_segment] = []
#
#     def read_pop_data(self, raw_mesh_json_dir, raw_pop_dir):
#         """
#         ポイントのJsonデータと人口データを読み、人口つきポイントオブジェクトのリストに登録
#         :param raw_mesh_json_dir:
#         :param raw_pop_dir:
#         :return:
#         """
#
#         print("メッシュ人口データ読み込み")
#         # 1次メッシュ区分ごとに処理
#         # i = 0
#         mesh_files = glob.glob(os.path.join(raw_mesh_json_dir, "*.txt"))
#         for mesh_file in tqdm(mesh_files):
#
#             # メッシュデータ読み込み
#             mpd = JsonMeshPointDataReader(mesh_file)
#
#             # 一次メッシュコード読み込み
#             first_mesh_code = os.path.basename(mesh_file).lstrip("MESH0").rstrip(".txt")
#
#             # 人口データ読み込み
#             pop_file = os.path.join(raw_pop_dir, "tblT000876Q" + first_mesh_code + ".txt")
#             prd = PopRawDataReader(pop_file)
#             pop_data = prd.get_data()
#
#             # 各Pointごとに、Keyが一致する人口データを探し、人口点リストに格納（なければ格納しない）
#             for point in mpd.get_points():
#                 for d in pop_data:
#                     if point.key_code == d.get_key_code():
#                         point.population = d.get_population()
#                         # point.id = i
#                         # i += 1
#                         self.all_points.append(point)
#                         break
#
#     def register_address(self, raw_region_json_dir):
#         """
#         住所を読み込み、人口点として登録する
#         :param raw_region_json_dir:
#         :return:
#         """
#
#         # 小地域データ読み込み
#         print("小地域データ読み込み")
#         region_points = []
#         region_files = glob.glob(os.path.join(raw_region_json_dir, "*txt"))
#         for region_file in tqdm(region_files):
#             rpd = JsonRegionPointDataReader(region_file)
#             region_points.extend(rpd.get_points())
#
#         # 各Pointごとに、一番近い小地域ポイントの住所を登録
#         print("住所登録")
#         ic = IslandChecker(fp.island_data_file)
#         j = 0
#         for point in tqdm(self.all_points):
#
#             min_dist = 0
#             nearest_region_point = None
#             for i, region_point in enumerate(region_points):
#                 dist = point.get_distance(region_point)
#                 if i == 0:
#                     min_dist = dist
#                     nearest_region_point = region_point
#                     continue
#                 if dist < min_dist:
#                     min_dist = dist
#                     nearest_region_point = region_point
#             point.pref = nearest_region_point.pref
#             point.city = nearest_region_point.city
#             point.district = nearest_region_point.district
#
#             # 島チェック
#             if ic.is_island(point):
#                 continue
#
#             # ポイントを人口点として登録（セグメントごとも含む）
#             point.id = j  # 島でないと分かった段階でID振る
#             j += 1
#             self.pop_points.append(point)
#             calc_segment = RegionSetting.get_calc_segment_by_pref(point.pref)
#             self.pop_points_by_calc_segment[calc_segment].append(point)
#
#     def add_pop_point(self, point):
#         """
#         人口点リスト（離島でない）にポイントを登録
#         :param point:
#         :return:
#         """
#         point.id = self.pop_point_id_count
#
#     def register_neighbors(self):
#         """
#         人口ポイントについて、隣接点を登録する
#         :return:
#         """
#
#         for calc_segment in RegionSetting.get_calc_segments():
#             print(calc_segment + "の隣接点を登録中")
#             target_points = self.pop_points_by_calc_segment[calc_segment].copy()
#             for p in tqdm(self.pop_points_by_calc_segment[calc_segment]):
#                 target_points.remove(p)
#                 for tp in target_points:
#                     if p.get_is_adjacent(tp):
#                         p.add_neighbor(tp)
#                         tp.add_neighbor(p)
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
