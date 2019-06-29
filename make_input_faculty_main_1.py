import glob
import geopandas as gpd
import os
from tqdm import tqdm
import settings.file_path as fp
import sys
import make_input_main_1
from settings.constants import *


def main():

    print("shpデータをjsonに変換")

    faculty_type = sys.argv[1]
    if faculty_type == ELEMENTARY_SCHOOL:
        input_file = fp.elementary_schools_shp_file
        output_file = fp.elementary_schools_json_file
    elif faculty_type == POST_OFFICE:
        input_file = fp.post_office_shp_file
        output_file = fp.post_office_json_file
    else:
        raise Exception("施設タイプ名が不正です")

    json_data = make_input_main_1.convert_polygon_shp_to_point_json(input_file)
    with open(output_file, "w", encoding="utf8") as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
