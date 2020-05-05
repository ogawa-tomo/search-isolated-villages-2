import settings.file_path as fp
from settings.constants import *
from library.setting import RegionSetting
import random
from library.faculty_dao import FacultyDAO


def main(faculty_type):

    input_file = fp.get_faculty_csv_file(faculty_type)

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 集落データを抽出
    faculties = extract_faculties(faculty_points)

    num = len(faculties)
    print(str(num) + "施設")

    # village = random.choice(villages)
    idx = int(random.random() * num)
    faculty = faculties[idx]

    # マップ出力
    map_file = os.path.join(fp.get_faculty_mesh_map_dir(faculty_type), faculty.pref + ".html")

    result = Result(faculty, map_file, num, idx)

    return result


def extract_faculties(faculties):

    extracted_faculties = []
    for f in faculties:

        # 都会度10000以下
        if f.urban_point < 10000:
            extracted_faculties.append(f)

    return extracted_faculties


class Result(object):

    def __init__(self, faculty, map_file, num, idx):
        self.faculty = faculty
        self.map_file = map_file
        self.num = num
        self.idx = idx

