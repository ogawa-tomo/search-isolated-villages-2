import csv
from settings.constants import *


class IslandChecker(object):

    def __init__(self, path):

        self.islands = []

        with open(path, "r", encoding="utf8") as f:

            reader = csv.reader(f)

            for i, line in enumerate(reader):
                island = Island(line[0], line[1], line[2], line[3], line[4])
                self.islands.append(island)

    def is_island(self, point):
        """
        島かどうかを判定する関数
        :param point:
        :return:
        """

        for island in self.islands:

            if island.pref == point.pref:

                if point.city.startswith(island.city) and point.district.startswith(island.district):
                    # 市町村名と地区名が島データの地区名から始まるまたは空欄なら

                    if island.latitude is None and island.longitude is None:
                        # 座標指定がなければTrue
                        return True
                    elif abs(island.latitude - point.latitude) < SAME_COORDINATE_THRESHOLD\
                            and abs(island.longitude - point.longitude) < SAME_COORDINATE_THRESHOLD:
                        # 座標が一致すればTrue
                        return True

        # どの島にも当てはまらなかったらFalse

        return False


class Island(object):

    def __init__(self, pref, city, district, latitude, longitude):
        self.pref = pref
        self.city = city
        self.district = district
        if latitude == "":
            self.latitude = None
        else:
            self.latitude = float(latitude)
        if longitude == "":
            self.longitude = None
        else:
            self.longitude = float(longitude)
