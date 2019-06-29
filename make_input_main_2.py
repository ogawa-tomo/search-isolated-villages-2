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


def main():

    # データマネージャクラス生成
    ppm = PopPointManager()

    # ポイント・人口データ読み込み
    ppm.read_pop_data(fp.raw_mesh_json_dir, fp.raw_pop_dir)

    # 住所データ読み込み
    ppm.register_address(fp.raw_region_json_dir)

    # 隣接点の登録
    ppm.register_neighbors()

    # 人口データの作成
    dao = PopPointDAO(fp.pop_point_file)
    dao.make_pop_point_data(ppm.pop_points)

    # # ----集落の抽出----
    # ppm.extract_villages(VILLAGE_SIZE_UPPER_LIMIT)
    #
    # # 都会度の計算
    # ppm.register_urban_point()
    #
    # # 抽出した集落をtxtファイルに保存
    # dao = VillageDAO(fp.villages_file)
    # dao.make_village_data(ppm.get_villages())


class PopPointManager(object):
    """
    人口ポイントデータを管理するクラス
    """

    def __init__(self):
        self.all_points = []
        self.pop_points = []
        self.pop_points_by_calc_segment = {}
        for calc_segment in RegionSetting.get_calc_segments():
            self.pop_points_by_calc_segment[calc_segment] = []
        self.villages = []
        self.villages_by_calc_segment = {}
        for calc_segment in RegionSetting.get_calc_segments():
            self.villages_by_calc_segment[calc_segment] = []

    def read_pop_data(self, raw_mesh_json_dir, raw_pop_dir):
        """
        ポイントのJsonデータと人口データを読み、人口つきポイントオブジェクトのリストに登録
        :param raw_mesh_json_dir:
        :param raw_pop_dir:
        :return:
        """

        print("メッシュ人口データ読み込み")
        # 1次メッシュ区分ごとに処理
        i = 0
        mesh_files = glob.glob(os.path.join(raw_mesh_json_dir, "*.txt"))
        for mesh_file in tqdm(mesh_files):

            # メッシュデータ読み込み
            mpd = JsonMeshPointDataReader(mesh_file)

            # 一次メッシュコード読み込み
            first_mesh_code = os.path.basename(mesh_file).lstrip("MESH0").rstrip(".txt")

            # 人口データ読み込み
            pop_file = os.path.join(raw_pop_dir, "tblT000876Q" + first_mesh_code + ".txt")
            prd = PopRawDataReader(pop_file)
            pop_data = prd.get_data()

            # 各Pointごとに、Keyが一致する人口データを探し、人口点リストに格納（なければ格納しない）
            for point in mpd.get_points():
                for d in pop_data:
                    if point.key_code == d.get_key_code():
                        point.population = d.get_population()
                        point.id = i
                        i += 1
                        self.all_points.append(point)
                        break

    def register_address(self, raw_region_json_dir):
        """
        住所を読み込み、人口点として登録する
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

        # 各Pointごとに、一番近い小地域ポイントの住所を登録
        print("住所登録")
        ic = IslandChecker(fp.island_data_file)
        for point in tqdm(self.all_points):

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

            # 島チェック
            if ic.is_island(point):
                continue

            # ポイントを人口点として登録（セグメントごとも含む）
            self.pop_points.append(point)
            calc_segment = RegionSetting.get_calc_segment_by_pref(point.pref)
            self.pop_points_by_calc_segment[calc_segment].append(point)

    def register_neighbors(self):
        """
        人口ポイントについて、隣接点を登録する
        :return:
        """

        for calc_segment in RegionSetting.get_calc_segments():
            print(calc_segment + "の隣接点を登録中")
            target_points = self.pop_points_by_calc_segment[calc_segment].copy()
            for p in tqdm(self.pop_points_by_calc_segment[calc_segment]):
                target_points.remove(p)
                for tp in target_points:
                    if p.get_is_adjacent(tp):
                        p.add_neighbor(tp)
                        tp.add_neighbor(p)

    # def extract_villages(self, village_size_upper_limit):
    #     """
    #     集落の抽出
    #     :param village_size_upper_limit:
    #     :return:
    #     """
    #
    #     registered = []  # 既に集落に登録された点
    #     print("集落を抽出中")
    #     for p in tqdm(self.pop_points):
    #         if p in registered:
    #             continue
    #
    #         # p周辺の人口集中ポイントを登録
    #         try:
    #             village_points = p.get_my_village_points([], village_size_upper_limit)
    #         except cf.TooBigVillageException:
    #             # サイズが閾値を超えた場合には例外が返ってくる
    #             continue
    #
    #         registered.extend(village_points)
    #
    #         v = Village()
    #         v.make_village(village_points)
    #
    #         self.villages.append(v)
    #         calc_segment = RegionSetting.get_calc_segment_by_pref(v.pref)
    #         self.villages_by_calc_segment[calc_segment].append(v)

    def register_urban_point(self):
        """
        各集落の都会度を計算する
        :return:
        """
        for calc_segment in RegionSetting.get_calc_segments():
            print(calc_segment + "の集落の都会度を計算中")
            for v in tqdm(self.villages_by_calc_segment[calc_segment]):

                for p in self.pop_points_by_calc_segment[calc_segment]:

                    # -----集落周縁からの都会度（集落内メッシュを計算に含めず、最短距離で計算）
                    if p in v.points:
                        continue
                    dist = v.get_distance(p)
                    v.urban_point += cf.calc_urban_point(p.population, dist)

                v.urban_point_round = round(v.urban_point, 4)  # html表示用

        # ついでに並べ替え
        self.villages = sorted(self.villages)

    def get_villages(self):
        return self.villages


if __name__ == "__main__":
    main()
