import glob
import geopandas as gpd
import os
from tqdm import tqdm
import settings.file_path as fp
import zipfile


def main():
    """
    zipファイルを展開する
    メッシュと小地域のshpファイルをポイント変換しjsonのtxtファイルにして吐き出す
    :return:
    """

    print("zipファイルを展開")
    extract_zip(fp.raw_mesh_shp_dir)
    extract_zip(fp.raw_region_shp_dir)
    extract_zip(fp.raw_pop_dir)

    print("境界データをshpからjsonに変換")
    shp_dir_to_json_dir(fp.raw_mesh_shp_dir, fp.raw_mesh_json_dir)

    print("小地域データをshpからjsonに変換")
    shp_dir_to_json_dir(fp.raw_region_shp_dir, fp.raw_region_json_dir)


def extract_zip(directory):
    """
    ディレクトリ内のzipファイルを展開する
    :param directory:
    :return:
    """
    files = glob.glob(os.path.join(directory, "*.zip"))
    for file in files:
        with zipfile.ZipFile(file, "r") as f:
            f.extractall(directory)


def shp_dir_to_json_dir(shp_dir, json_dir):
    """
    shp_dirのポリゴンデータをポイントのjsonにしてjson_dirに吐き出す
    :param shp_dir:
    :param json_dir:
    :return:
    """

    # jsonディレクトリ内を削除
    json_files = glob.glob(os.path.join(json_dir, "*.txt"))
    for file in json_files:
        os.remove(file)

    # shpをjsonに変換して吐く
    files = glob.glob(os.path.join(shp_dir, "*.shp"))
    for file in tqdm(files):
        # data = gpd.read_file(file)
        # data["geometry"] = data.centroid
        # json_data = data.to_json()
        json_data = convert_polygon_shp_to_point_json(file)
        json_file = os.path.basename(file)
        json_file = json_file.replace(".shp", ".txt")
        with open(os.path.join(json_dir, json_file), "w", encoding="utf8") as f:
            f.write(json_data)


def convert_polygon_shp_to_point_json(shp_file):
    """
    shpファイルをjsonデータにして返す
    :param shp_file:
    :return:
    """
    data = gpd.read_file(shp_file)
    data["geometry"] = data.centroid
    return data.to_json()


if __name__ == "__main__":
    main()
