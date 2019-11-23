import os
import time


# 境界メッシュshpデータ格納ディレクトリ
raw_mesh_shp_dir = os.path.join("./raw_data", "mesh_shp")

# 境界jsonデータ格納ディレクトリ
raw_mesh_json_dir = os.path.join("./input_data", "mesh_json")

# 小地域shpデータ格納ディレクトリ
raw_region_shp_dir = os.path.join("./raw_data", "region_shp")

# 小地域jsonデータ格納ディレクトリ
raw_region_json_dir = os.path.join("./input_data", "region_json")

# 人口データ格納ディレクトリ
raw_pop_dir = os.path.join("./raw_data", "population")

# 島データファイル
island_data_file = os.path.join("./settings", "islands.csv")

# 隣接点つき人口データファイル
pop_point_file = os.path.join("./input_data", "pop_points.csv")

# 集落データファイル
villages_file = os.path.join("./input_data", "villages.csv")

# 学校生データファイル
elementary_schools_shp_dir = os.path.join("./raw_data", "elementary_school_shp")

# 学校jsonデータファイル
elementary_schools_json_file = os.path.join("./input_data", "elementary_schools_json.txt")

# 学校csvデータファイル
elementary_schools_file = os.path.join("./input_data", "elementary_schools.csv")

# 郵便局生データファイル
post_office_shp_dir = os.path.join("./raw_data", "post_office_shp")

# 郵便局jsonデータファイル
post_office_json_file = os.path.join("./input_data", "post_offices_json.txt")

# 郵便局csvデータファイル
post_office_file = os.path.join("./input_data", "post_offices.csv")

# ニュータウン生データファイル
new_town_shp_dir = os.path.join("./raw_data", "new_town_shp")

# ニュータウンjsonデータファイル
new_town_json_file = os.path.join("./input_data", "new_towns_json.txt")

# ニュータウンcsvデータファイル
new_town_file = os.path.join("./input_data", "new_towns.csv")

# 道の駅生データファイル
michinoeki_shp_dir = os.path.join("./raw_data", "michinoeki_shp")

# 道の駅jsonデータファイル
michinoeki_json_file = os.path.join("./input_data", "michinoeki_json.txt")

# 道の駅csvデータファイル
michinoeki_file = os.path.join("./input_data", "michinoeki.csv")

# 駅生データファイル
station_shp_dir = os.path.join("./raw_data", "station_shp")

# 駅jsonデータファイル
station_json_file = os.path.join("./input_data", "station_json.txt")

# 駅csvデータファイル
station_file = os.path.join("./input_data", "station.csv")

# 駅時系列データファイル
abandoned_station_shp_dir = os.path.join("./raw_data", "abandoned_station_shp")

# 駅時系列jsonデータファイル
abandoned_station_json_file = os.path.join("./input_data", "abandoned_station_json.txt")

# 駅時系列csvデータファイル
abandoned_station_file = os.path.join("./input_data", "abandoned_station.csv")

# 施設修正データファイル
correct_faculty_file = os.path.join("./settings", "correct_faculty.csv")

# アウトプットフォルダ
output_dir = os.path.join("./static", "output")

# マップ出力
# output_map_file = os.path.join("./output", "map_" + str(time.time()).replace(".", "") + ".html")
