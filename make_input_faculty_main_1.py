import settings.file_path as fp
import sys
from settings.constants import *
import library.shp_functions as sf
import geopandas as gpd
import json


def main():

    faculty_type = sys.argv[1]
    input_dir = fp.get_faculty_shp_dir(faculty_type)
    output_file = fp.get_faculty_json_file(faculty_type)

    print("zipファイルを展開")
    sf.extract_zip(input_dir)

    print("フォルダ内のファイルを展開")
    sf.extract_files(input_dir)

    if faculty_type == STATION:
        print("geojsonを読み込み")
        merged_data = gpd.read_file(os.path.join(input_dir, "N02-18_Station.geojson"), driver="GeoJson")
    elif faculty_type == ABANDONED_STATION:
        print("geojsonを読み込み")
        merged_data = gpd.read_file(os.path.join(input_dir, "N05-18_Station2.geojson"), driver="GeoJson")
    elif faculty_type == RESEARCH_INSTITUTE:
        print("shpファイルを読み込んで結合")
        merged_data = sf.merge_shp(input_dir, encoding="shift_jis")
    else:
        print("shpファイルを読み込んで結合")
        merged_data = sf.merge_shp(input_dir)

    print("データを点データに変換")
    merged_data["geometry"] = merged_data.centroid

    print("jsonに変換して吐き出し")
    json_data = merged_data.to_json(default=support_bytes_default)

    with open(output_file, "w", encoding="shift_jis") as f:
        f.write(json_data)


def support_bytes_default(o):
    if isinstance(o, bytes):
        return "0"
    raise TypeError(repr(o) + " is not JSON serializable")


if __name__ == "__main__":
    main()
