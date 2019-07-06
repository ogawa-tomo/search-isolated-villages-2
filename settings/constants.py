import os

# 抽出する集落範囲上限
VILLAGE_SIZE_UPPER_LIMIT = 150  # 5次メッシュ

# 隣接判定の緯度閾値
# NEIGHBOR_THRESHOLD_LAT = 0.012  # 3次メッシュ
# NEIGHBOR_THRESHOLD_LAT = 0.006  # 4次メッシュ
NEIGHBOR_THRESHOLD_LAT = 0.003  # 5次メッシュ

# 隣接判定の経度閾値
# NEIGHBOR_THRESHOLD_LON = 0.018  # 3次メッシュ
# NEIGHBOR_THRESHOLD_LON = 0.009  # 4次メッシュ
NEIGHBOR_THRESHOLD_LON = 0.0045  # 5次メッシュ

# メッシュ内にあると判定する閾値
IS_IN_MESH_THRESHOLD_LAT = 0.0011  # 5次メッシュ
IS_IN_MESH_THRESHOLD_LON = 0.0016  # 5次メッシュ

# 緯度1度あたりの距離（km）
LAT_DISTANCE = 111

# 経度1度あたりの距離（km）
LON_DISTANCE = 91

# 都会度計算時に人口に乗じる値
POP_PARAM = 1

# 都会度計算時に距離に乗じる値
DIST_PARAM = 2

# マップ出力の最大点数
OUTPUT_MAP_NUM = 100

# 結果のページに出す集落数
OUTPUT_HTML_NUM = 1000

# 同一座標とみなす閾値
SAME_COORDINATE_THRESHOLD = 0.0001

ELEMENTARY_SCHOOL = "elementary_school"

POST_OFFICE = "post_office"



