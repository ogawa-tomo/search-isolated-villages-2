import os
import time


# 境界メッシュshpデータ格納ディレクトリ
raw_mesh_shp_dir = os.path.join("./raw_data", "mesh_shp")

# 境界jsonデータ格納ディレクトリ
raw_mesh_json_dir = os.path.join("./input_data", "mesh_json")
# raw_mesh_json_dir = os.path.join("./input_data", "mesh_json_test")

# 境界jsonデータ（メッシュポリゴン）格納ディレクトリ
raw_mesh_json_polygon_dir = os.path.join("./input_data", "mesh_json_polygon")
# raw_mesh_json_polygon_dir = os.path.join("./input_data", "mesh_json_polygon_test")

# 小地域shpデータ格納ディレクトリ
def raw_region_shp_dir(year):
    return os.path.join("./raw_data", "region_shp", str(year))

# 小地域jsonデータ格納ディレクトリ
def raw_region_json_dir(year):
    return os.path.join("./input_data", "region_json", str(year))

# 人口データ格納ディレクトリ
def raw_pop_dir(year):
    return os.path.join("./raw_data", "population", str(year))
# raw_pop_dir = os.path.join("./raw_data", "population_test")

# 島データファイル
island_data_file = os.path.join("./settings", "islands.csv")

# 隣接点つき人口データファイル
def pop_point_file(year):
    return os.path.join("./input_data", "pop_points", str(year),"pop_points.csv")

# 都会度対決のための人口データファイル
def pop_point_file_for_tokaido_taiketsu(year):
    return os.path.join("./input_data", "pop_points_for_tokaido_taiketsu", str(year), "pop_points_for_tokaido_taiketsu.csv")

# 都会度極大点探索ツール用に極大点のみを集めた人口データファイル
def pop_point_file_for_maximum_urban_points(year):
    return os.path.join("./input_data", "pop_points_for_maximum_urban_points", str(year), "pop_points_for_maximum_urban_points.csv")

# 人口ポリゴンデータディレクトリ
def pop_polygon_dir(year):
    return os.path.join("./input_data", "pop_polygons", str(year))

# 集落データファイル
def villages_file(year):
    return os.path.join("./input_data", "villages", str(year), "villages.csv")

# メッシュ図格納ディレクトリ
def mesh_map_dir(year):
    return os.path.join("./static", "mesh_map", str(year))

# r774生jsonデータファイル
r774_raw_json_file = os.path.join("./raw_data", "r774_geojson", "r774__________________.geojson")

# r774データファイル
r774_file = os.path.join("./input_data", "r774_points.csv")

# 都会度極大点地図データ格納ディレクトリ
def max_urban_points_map_dir(year):
    return os.path.join("./static", "max_urban_points_map", str(year))

# # 学校生データファイル
# elementary_schools_shp_dir = os.path.join("./raw_data", "elementary_school_shp")
#
# # 学校jsonデータファイル
# elementary_schools_json_file = os.path.join("./input_data", "elementary_schools_json.txt")
#
# # 学校csvデータファイル
# elementary_schools_file = os.path.join("./input_data", "elementary_schools.csv")
#
# # 郵便局生データファイル
# post_office_shp_dir = os.path.join("./raw_data", "post_office_shp")
#
# # 郵便局jsonデータファイル
# post_office_json_file = os.path.join("./input_data", "post_offices_json.txt")
#
# # 郵便局csvデータファイル
# post_office_file = os.path.join("./input_data", "post_offices.csv")
#
# # ニュータウン生データファイル
# new_town_shp_dir = os.path.join("./raw_data", "new_town_shp")
#
# # ニュータウンjsonデータファイル
# new_town_json_file = os.path.join("./input_data", "new_towns_json.txt")
#
# # ニュータウンcsvデータファイル
# new_town_file = os.path.join("./input_data", "new_towns.csv")
#
# # 道の駅生データファイル
# michinoeki_shp_dir = os.path.join("./raw_data", "michinoeki_shp")
#
# # 道の駅jsonデータファイル
# michinoeki_json_file = os.path.join("./input_data", "michinoeki_json.txt")
#
# # 道の駅csvデータファイル
# michinoeki_file = os.path.join("./input_data", "michinoeki.csv")
#
# # 駅生データファイル
# station_shp_dir = os.path.join("./raw_data", "station_shp")
#
# # 駅jsonデータファイル
# station_json_file = os.path.join("./input_data", "station_json.txt")
#
# # 駅csvデータファイル
# station_file = os.path.join("./input_data", "station.csv")
#
# # 駅時系列データファイル
# abandoned_station_shp_dir = os.path.join("./raw_data", "abandoned_station_shp")
#
# # 駅時系列jsonデータファイル
# abandoned_station_json_file = os.path.join("./input_data", "abandoned_station_json.txt")
#
# # 駅時系列csvデータファイル
# abandoned_station_file = os.path.join("./input_data", "abandoned_station.csv")


def get_faculty_shp_dir(faculty_type):
    """
    施設生データファイル
    :param faculty_type:
    :return:
    """
    return os.path.join("./raw_data", faculty_type + "_shp")


def get_faculty_json_file(faculty_type):
    """
    施設jsonデータファイル
    :param faculty_type:
    :return:
    """
    return os.path.join("./input_data", faculty_type, faculty_type + "_json.txt")


def get_faculty_csv_file(faculty_type, year):
    """
    施設csvデータファイル
    :param faculty_type:
    :return:
    """
    return os.path.join("./input_data", faculty_type, str(year), faculty_type + ".csv")


def get_faculty_mesh_map_dir(faculty_type, year):
    """
    施設の人口メッシュ図格納ディレクトリ
    :param faculty_type:
    :return:
    """
    return os.path.join("./static", "mesh_map_" + faculty_type, str(year))


# 施設修正データファイル
correct_faculty_file = os.path.join("./settings", "correct_faculty.csv")

# アウトプットフォルダ
# output_dir = os.path.join("./tmp")
output_dir = os.path.join("./static", "output")

# マップ出力
# output_map_file = os.path.join("./output", "map_" + str(time.time()).replace(".", "") + ".html")
