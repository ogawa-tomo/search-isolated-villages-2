import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
import settings.file_path as fp
from library.point_dao import PopPointDAO, PopPointDAOForTokaidoTaiketsu
import library.make_input_functions as mif
from library.point_container import PointContainer
from tqdm import tqdm
import library.common_function as cf
from library.setting import RegionSetting


def main():
    """
    ・都会度対決ツール用に全人口点に都会度を付与
    ・都会度極大点探索ツール用に都会度の極大点を抽出
    """

    # 人口データ読み込み
    p_dao = PopPointDAO(fp.pop_point_file)
    pop_points = p_dao.read_pop_point_data()

    # 小地域データ読み込み
    # region_points = mif.read_region_data(fp.raw_region_json_dir)

    # 全人口点のコンテナ
    all_pop_point_container = PointContainer()
    all_pop_point_container.register_points(pop_points)

    # 本土と離島の人口点のコンテナ
    mainland_pop_point_container = PointContainer()
    island_pop_point_container = PointContainer()
    mif.register_mainland_island_container(pop_points, mainland_pop_point_container, island_pop_point_container)

    # 都会度の計算（本土の人口点の都会度を、本土の人口点で計算）
    register_urban_point(mainland_pop_point_container, mainland_pop_point_container)

    # 都会度の計算（離島の施設の都会度を、全人口点で計算）
    register_urban_point(island_pop_point_container, all_pop_point_container)

    # 都会度対決用のcsv吐き出し
    dao = PopPointDAOForTokaidoTaiketsu(fp.pop_point_file_for_tokaido_taiketsu)
    dao.make_pop_point_data(pop_points)

    # 都会度の極大点を抽出
    maximum_urban_points = get_maximum_urban_points(pop_points)

    # 並べ替え（都会度高い順）
    maximum_urban_points = sorted(maximum_urban_points, reverse=True)

    # 都会度の極大点ファイルを書き出し
    dao = PopPointDAO(fp.pop_point_file_for_maximum_urban_points)
    dao.make_pop_point_data(maximum_urban_points)


def register_urban_point(point_container, pop_point_container):
    """
    人口点の都会度を計算する
    """
    for calc_segment in RegionSetting.get_calc_segments():
        print(calc_segment + " の人口点の都会度を計算中")

        for p1 in tqdm(point_container.get_points_by_calc_segment(calc_segment)):
            
            # 初期化
            p1.urban_point = 0

            for p2 in pop_point_container.get_points_by_calc_segment(calc_segment):

                dist = p1.get_distance(p2)
                if dist == 0:
                    continue
                
                p1.urban_point += cf.calc_urban_point(p2.population, dist)


def get_maximum_urban_points(pop_points):

    maximum_urban_points = []

    for p in pop_points:
        urban_points = [n.urban_point for n in p.neighbors]
        urban_points.append(p.urban_point)
        if max(urban_points) == p.urban_point:
            maximum_urban_points.append(p)
    
    return maximum_urban_points


if __name__ == "__main__":
    main()