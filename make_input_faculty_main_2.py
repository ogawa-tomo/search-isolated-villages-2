import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
import glob
import settings.file_path as fp
from library.point_dao import PopPointDAO
from library.json_data_reader import *
from library.faculty_dao import FacultyDAO, CorrectFacultyDAO
from tqdm import tqdm
from library.island_checker import IslandChecker


def main():
    """
    jsonデータを読んでcsvにして返す
    :return:
    """

    faculty_type = sys.argv[1]
    if faculty_type == ELEMENTARY_SCHOOL:
        input_file = fp.elementary_schools_json_file
        output_file = fp.elementary_schools_file
    elif faculty_type == POST_OFFICE:
        input_file = fp.post_office_json_file
        output_file = fp.post_office_file
    else:
        raise Exception("施設タイプ名が不正です")

    # 人口データ読み込み
    p_dao = PopPointDAO(fp.pop_point_file)
    pop_points = p_dao.read_pop_point_data()

    # 施設データマネージャクラス
    fpm = FacultyPointManager(pop_points, faculty_type)
    fpm.read_faculty_data(input_file)

    # 施設データ修正
    cf_dao = CorrectFacultyDAO(fp.correct_faculty_file)
    correct_faculty_data = cf_dao.read_data()
    correct_faculty = CorrectFaculty(fpm.faculty_points, correct_faculty_data)
    correct_faculty.correct_faculty()

    # 施設データにそれが含まれる人口点データとその住所登録（なければ登録しない）
    fpm.register_in_pop_point()

    # 孤立した施設データに住所を登録
    fpm.register_address_to_isolated_points(fp.raw_region_json_dir)

    # 施設データに都会度を登録
    fpm.register_urban_point()

    # csv吐き出し
    f_dao = FacultyDAO(output_file)
    f_dao.make_faculty_point_data(fpm.faculty_points)


class FacultyPointManager(object):

    def __init__(self, pop_points, faculty_type):

        self.pop_points = pop_points
        self.pop_points_by_calc_segment = {}
        for calc_segment in RegionSetting.get_calc_segments():
            self.pop_points_by_calc_segment[calc_segment] = []
        self.allocate_pop_points_to_segments()

        self.faculty_type = faculty_type

        self.faculty_points = []
        self.faculty_points_by_calc_segment = {}
        for calc_segment in RegionSetting.get_calc_segments():
            self.faculty_points_by_calc_segment[calc_segment] = []

        self.isolated_points = []

    def allocate_pop_points_to_segments(self):
        """
        ポイントをセグメントに振り分ける関数
        :return:
        """
        for p in self.pop_points:
            calc_segment = RegionSetting.get_calc_segment_by_pref(p.pref)
            self.pop_points_by_calc_segment[calc_segment].append(p)

    def read_faculty_data(self, faculty_json_file):
        """
        施設のJsonデータを読む
        :param faculty_json_file:
        :return:
        """
        fdr = JsonFacultyPointDataReader(faculty_json_file, self.faculty_type)
        self.faculty_points = fdr.get_points()

    def register_in_pop_point(self):
        """
        最も近い点とその住所を登録
        :return:
        """

        print("最も近い人口点とその住所を登録")
        ic = IslandChecker(fp.island_data_file)
        for point in tqdm(self.faculty_points):

            min_dist = 0
            nearest_pop_point = None
            for i, pop_point in enumerate(self.pop_points):
                dist = point.get_distance(pop_point)
                if i == 0:
                    min_dist = dist
                    nearest_pop_point = pop_point
                    continue
                if dist < min_dist:
                    min_dist = dist
                    nearest_pop_point = pop_point

            if point.get_is_in_mesh(nearest_pop_point):

                # 人口メッシュ内にあると判断すれば、

                # 人口ポイントを登録
                point.in_mesh_point = nearest_pop_point

                # 住所登録
                point.pref = nearest_pop_point.pref
                point.city = nearest_pop_point.city
                point.district = nearest_pop_point.district

                # 島チェック
                if ic.is_island(point):
                    continue

                # ポイントを登録（セグメントごとも含む）
                calc_segment = RegionSetting.get_calc_segment_by_pref(point.pref)
                self.faculty_points_by_calc_segment[calc_segment].append(point)

            else:

                # 最も近いメッシュ内にもないと判断すれば、その旨を登録
                self.isolated_points.append(point)

    def register_address_to_isolated_points(self, raw_region_json_dir):
        """
        孤立点に住所を登録
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

        # 各Pointごとに、一番近い小地域ポイントの住所を登録
        print("孤立点に住所登録")
        ic = IslandChecker(fp.island_data_file)
        for point in tqdm(self.isolated_points):

            min_dist = 0
            nearest_region_point = None
            for i, region_point in enumerate(region_points):
                dist = point.get_distance(region_point)
                if i == 0:
                    min_dist = dist
                    nearest_region_point = region_point
                    continue
                if dist < min_dist:
                    min_dist = dist
                    nearest_region_point = region_point
            point.pref = nearest_region_point.pref
            point.city = nearest_region_point.city
            point.district = nearest_region_point.district

            # 島チェック
            if ic.is_island(point):
                continue

            # ポイントを登録（セグメントごとも含む）
            calc_segment = RegionSetting.get_calc_segment_by_pref(point.pref)
            self.faculty_points_by_calc_segment[calc_segment].append(point)

    def register_urban_point(self):
        """
        施設の都会度を計算する
        :return:
        """
        for calc_segment in RegionSetting.get_calc_segments():
            print(calc_segment + "の施設の都会度を計算中")
            for f_point in tqdm(self.faculty_points_by_calc_segment[calc_segment]):

                # 代表点
                if f_point in self.isolated_points:
                    f_repr_point = f_point
                else:
                    f_repr_point = f_point.in_mesh_point

                for p_point in self.pop_points_by_calc_segment[calc_segment]:

                    dist = f_repr_point.get_distance(p_point)
                    if dist == 0:
                        continue
                    f_point.urban_point += cf.calc_urban_point(p_point.population, dist)

                f_point.urban_point_round = round(f_point.urban_point, 4)  # html表示用

        # ついでに並べ替え
        self.faculty_points = sorted(self.faculty_points)


class CorrectFaculty(object):
    """
    施設データを修正するクラス
    """
    def __init__(self, raw_faculty_data, correct_faculty_data):
        self.raw_faculty_data = raw_faculty_data
        self.correct_faculty_data = correct_faculty_data

    def correct_faculty(self):
        """
        修正データと一致する点があれば緯度経度書き換え
        :return:
        """
        print("施設データを修正")
        for raw_f in tqdm(self.raw_faculty_data):
            for cor_f in self.correct_faculty_data:
                if raw_f.name == cor_f.name \
                        and abs(raw_f.latitude - cor_f.raw_lat) < SAME_COORDINATE_THRESHOLD\
                        and abs(raw_f.longitude - cor_f.raw_lon) < SAME_COORDINATE_THRESHOLD:
                    raw_f.latitude = cor_f.correct_lat
                    raw_f.longitude = cor_f.correct_lon
                    break


if __name__ == "__main__":
    main()
