from library.setting import RegionSetting


class PointContainer(object):
    """
    点をセグメントごとに保持するクラス
    """
    def __init__(self):

        # self.__id_count = 0
        self.__points = []
        self.__points_by_calc_segment = {}
        for calc_segment in RegionSetting.get_calc_segments():
            self.__points_by_calc_segment[calc_segment] = []

    def add_point(self, point):
        """
        ポイントを追加する
        :param point:
        :return:
        """
        # ID管理
        # point.id = self.__id_count
        # self.__id_count += 1

        # 追加
        self.__points.append(point)
        calc_segment = RegionSetting.get_calc_segment_by_pref(point.pref)
        self.__points_by_calc_segment[calc_segment].append(point)

    def register_points(self, points):
        """
        ポイントリストを追加する
        :param points:
        :return:
        """
        for p in points:
            self.add_point(p)

    def get_points_by_calc_segment(self, calc_segment):
        """
        セグメントごとのポイントを返すメソッド
        :param calc_segment:
        :return:
        """
        return self.__points_by_calc_segment[calc_segment]

    def get_points(self):
        return self.__points
