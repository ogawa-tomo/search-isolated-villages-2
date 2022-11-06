import library.make_input_functions as mif
from library.point import Point
import settings.file_path as fp
from library.setting import RegionSetting
from library.point_dao import PopPointDAOForTokaidoTaiketsu


def main(year, point1_name, point1_lat, point1_lon, point2_name, point2_lat, point2_lon):

    dao = PopPointDAOForTokaidoTaiketsu(fp.pop_point_file_for_tokaido_taiketsu(year))
    point1_tokaido = dao.get_tokaido(point1_lat, point1_lon)
    point2_tokaido = dao.get_tokaido(point2_lat, point2_lon)

    point1_latlon = str(round(point1_lat, 4)) + ", " + str(round(point1_lon, 4))
    point2_latlon = str(round(point2_lat, 4)) + ", " + str(round(point2_lon, 4))

    result = Result(point1_name, point1_latlon, point1_tokaido, point2_name, point2_latlon, point2_tokaido)

    return result


class Result(object):

    def __init__(self, point1_name, point1_latlon, point1_tokaido, point2_name, point2_latlon, point2_tokaido):
        self.point1_name = point1_name
        self.point1_latlon = point1_latlon
        self.point1_tokaido = round(point1_tokaido, 2)
        self.point2_name = point2_name
        self.point2_latlon = point2_latlon
        self.point2_tokaido = round(point2_tokaido, 2)
        if point1_tokaido > point2_tokaido:
            self.winner = point1_name
        else:
            self.winner = point2_name
