import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
import glob
from library.json_data_reader import *
from library.pop_data_reader import *
from library.island_checker import IslandChecker
from tqdm import tqdm
import settings.file_path as fp
from library.point_dao import PopPointDAO
from library.pop_polygon_dao import PopPolygonDAO
# import library.common_function as cf
import library.make_input_functions as mif
from library.point_container import PointContainer
from library.setting import RegionSetting


"""
人口ポイントと小地域ポイントのjsonデータを読み込む
小地域ポイントデータをもとに、人口ポイントデータに住所を付与する
人口ポイントデータに隣接関係を付与する
人口ポイントデータをcsvに吐き出す
"""

try:
    year = sys.argv[1]
except IndexError:
    raise Exception('引数でデータ年を指定してください')

def main():

    # ポイント・人口データ読み込み
    all_points = read_pop_data(fp.raw_mesh_json_dir, fp.raw_pop_dir(year))

    # 小地域データ読み込み
    region_points = mif.read_region_data(fp.raw_region_json_dir(year))

    # 住所データ読み込み
    mif.register_address(all_points, region_points)

    # 住所をもとに本土の点と離島の点をそれぞれコンテナに登録
    mainland_point_container = PointContainer()
    island_point_container = PointContainer()
    mif.register_mainland_island_container(all_points, mainland_point_container, island_point_container)

    # 隣接点の登録（本土と離島それぞれ）
    # ppm.register_neighbors()
    print("本土の隣接点を登録")
    register_neighbors(mainland_point_container)
    print("離島の隣接点を登録")
    register_neighbors(island_point_container)

    # 人口データの作成
    dao = PopPointDAO(fp.pop_point_file(year)) # 九州・沖縄しか読めていない・・・？
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
        if year == '2015':
          year_code = "tblT000876Q"
        elif year == '2020':
          year_code = "tblT001102Q"
        pop_file = os.path.join(raw_pop_dir, year_code + first_mesh_code + ".txt")
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
                    if len(p.neighbors) >= 8:
                        break


if __name__ == "__main__":
    main()
