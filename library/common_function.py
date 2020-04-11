import math
from settings.constants import *
import time


def get_distance(x1, y1, x2, y2):
    """
    日本周辺の緯度経度からの距離（km）
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    dx = abs(x1 - x2) * LON_DISTANCE
    dy = abs(y1 - y2) * LAT_DISTANCE
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist


def get_google_map_url(lat, lon):
    """
    google mapのURL（航空写真）を得る
    :param lat:
    :param lon:
    :return:
    """
    lat = str(round(lat, 4))  # 丸める
    lon = str(round(lon, 4))  # 丸める
    url = "https://maps.google.com/maps?q=" + lat + "," + lon + "&t=k"
    return url


def calc_urban_point(pop, dist):
    """
    対するメッシュの距離と人口から寄与する都会度を計算する
    :param pop:
    :param dist:
    :return:
    """
    return (pop ** POP_PARAM) / (dist ** DIST_PARAM)


class TooBigVillageException(Exception):
    """
    大きすぎる集落を抽出したときに返す例外クラス
    """
    pass


def create_modified_map(lat, lon, zoom, map_file, new_map_file):
    """
    マップファイルの中心とズームを編集して新たにマップを作る
    :param lat:
    :param lon:
    :param zoom:
    :param map_file:
    :param new_map_file:
    :return:
    """
    
    # マップ読み込み
    with open(map_file, "r", encoding="utf8") as f:
        lines = f.readlines()

    # 新データ作り
    new_lines = []
    for i, line in enumerate(lines):
        if line.lstrip()[:6] == "center":
            # centerを編集
            new_line = "center: [" + str(lat) + ", " + str(lon) + "],"
        elif line.lstrip()[:4] == "zoom":
            new_line = "zoom: " + str(zoom) + ","
        else:
            new_line = line
        new_lines.append(new_line)

    # 新データに置き換え
    new_map_file_path_list = new_map_file.lstrip("./").split("\\")
    new_map_file = os.path.join(*new_map_file_path_list)  # ファイル名に"/"があるとエラー
    with open(new_map_file, "w", encoding="utf8") as f:
        f.write("\n".join(new_lines))
