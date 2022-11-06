from library.point_dao import PopPointDAO
import settings.file_path as fp
import os
from library.setting import RegionSetting, Result
import time
from settings.constants import *
from library.output_map import OutputMap


def main(s):

    # 人口データを読み込み
    dao = PopPointDAO(fp.pop_point_file_for_maximum_urban_points(s.year))
    points = dao.read_pop_point_data(read_neighbors=False)

    # 人口点を条件に従って抽出
    points = s.extract_objects(points)

    # マップ出力
    if RegionSetting.is_pref(s.region):
        # 都道府県の場合は、既に出力してある都道府県別のhtmlファイル（人口分布つき）
        map_file = os.path.join(fp.max_urban_points_map_dir(s.year), s.region + ".html")
    else:
        # 都道府県でない場合は、その場でmapを作る（人口分布なし）
        map_file = os.path.join(fp.output_dir, "map_" + str(time.time()).replace(".", "") + ".html")
        output_map = OutputMap(map_file)
        output_map.output_map(points, OUTPUT_MAP_NUM)

    # 結果
    result = Result(points, s, map_file)

    return result

