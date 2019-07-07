import os
import glob
from tqdm import tqdm
from library.island_checker import IslandChecker
import settings.file_path as fp
from library.json_data_reader import JsonRegionPointDataReader


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
