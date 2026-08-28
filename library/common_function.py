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
    # dx = abs(x1 - x2) * LON_DISTANCE
    # dy = abs(y1 - y2) * LAT_DISTANCE
    # dist = math.sqrt(dx ** 2 + dy ** 2)

    # 地球が真球と仮定して計算　https://komoriss.com/calculate-distance-between-two-points-from-latitude-and-longitude/
    if x1 == x2 and y1 == y2:
        return 0
    lon1 = x1 * math.pi / 180
    lat1 = y1 * math.pi / 180
    lon2 = x2 * math.pi / 180
    lat2 = y2 * math.pi / 180
    dist = 6371 * math.acos(math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1) + math.sin(lat1) * math.sin(lat2))
    
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

