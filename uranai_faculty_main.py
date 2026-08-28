import settings.file_path as fp
from settings.constants import *
from library.setting import RegionSetting
import random
from library.faculty_dao import FacultyDAO


def main(faculty_type):

    input_file = fp.get_faculty_csv_file(faculty_type, DEFAULT_YEAR)

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 集落データを抽出
    faculties = extract_faculties(faculty_points)

    num = len(faculties)

    idx = int(random.random() * num)
    faculty = faculties[idx]

    return faculty

def extract_faculties(faculties):

    extracted_faculties = []
    for f in faculties:

        # 都会度10000以下
        if f.urban_point < 10000:
            extracted_faculties.append(f)

    return extracted_faculties

