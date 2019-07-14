import settings.file_path as fp
import sys
from settings.constants import *
import library.shp_functions as sf


def main():

    faculty_type = sys.argv[1]
    if faculty_type == ELEMENTARY_SCHOOL:
        input_dir = fp.elementary_schools_shp_dir
        output_file = fp.elementary_schools_json_file
    elif faculty_type == POST_OFFICE:
        input_dir = fp.post_office_shp_dir
        output_file = fp.post_office_json_file
    elif faculty_type == NEW_TOWN:
        input_dir = fp.new_town_shp_dir
        output_file = fp.new_town_json_file
    elif faculty_type == MICHINOEKI:
        input_dir = fp.michinoeki_shp_dir
        output_file = fp.michinoeki_json_file
    else:
        raise Exception("施設タイプ名が不正です")

    print("zipファイルを展開")
    sf.extract_zip(input_dir)

    print("フォルダ内のファイルを展開")
    sf.extract_files(input_dir)

    print("shpファイルを結合")
    merged_data = sf.merge_shp(input_dir)

    print("jsonに変換して吐き出し")
    json_data = merged_data.to_json()
    with open(output_file, "w", encoding="utf8") as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
