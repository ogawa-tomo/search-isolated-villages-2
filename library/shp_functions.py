import glob
import os
import zipfile
from tqdm import tqdm
import geopandas as gpd
import shutil
import pandas as pd


def extract_zip(directory):
    """
    ディレクトリ内のzipファイルを展開する
    :param directory:
    :return:
    """
    files = glob.glob(os.path.join(directory, "*.zip"))
    for file in tqdm(files):
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
        json_data = convert_polygon_shp_to_point_json(file)
        json_file = os.path.basename(file)
        json_file = json_file.replace(".shp", ".txt")
        with open(os.path.join(json_dir, json_file), "w", encoding="utf8") as f:
            f.write(json_data)


def shp_dir_to_json_polygon_dir(shp_dir, json_polygon_dir):
    """
    shp_dirのポリゴンデータをポリゴンのままjsonにしてjson_polygon_dirに吐き出す
    :param shp_dir:
    :param json_polygon_dir:
    :return:
    """

    # jsonディレクトリ内を削除
    json_files = glob.glob(os.path.join(json_polygon_dir, "*.txt"))
    for file in json_files:
        os.remove(file)

    # shpをjsonに変換して吐く
    files = glob.glob(os.path.join(shp_dir, "*.shp"))
    for file in tqdm(files):
        json_data = gpd.read_file(file).to_json()
        json_file = os.path.basename(file)
        json_file = json_file.replace(".shp", ".txt")
        with open(os.path.join(json_polygon_dir, json_file), "w", encoding="utf8") as f:
            f.write(json_data)


def convert_polygon_shp_to_point_json(shp_file):
    """
    shpファイルをポイントのjsonデータにして返す
    :param shp_file:
    :return:
    """
    data = gpd.read_file(shp_file)
    data["geometry"] = data.centroid
    return data.to_json()


def extract_files(directory):
    """
    ディレクトリ内の、そのまたディレトリ内のファイルを全てコピーし、ディレクトリ直下にペースト
    :param directory:
    :return:
    """
    for folder_name in tqdm(glob.glob(os.path.join(directory, "*"))):
        if os.path.isdir(folder_name):
            files = glob.glob(os.path.join(folder_name, "*"))
            for file in files:
                name = os.path.basename(file)
                shutil.copyfile(file, os.path.join(directory, name))


def merge_shp(directory, encoding=None):
    """
    ディレクトリ内のshpを結合したデータを返す
    :param directory:
    :param encoding: エンコーディング指定。指定しない場合はデフォルト
    :return:
    """
    files = glob.glob(os.path.join(directory, "*shp"))
    merged_data = None
    for i, file in tqdm(enumerate(files)):
        if i == 0:
            if encoding is not None:
                merged_data = gpd.read_file(file, encoding=encoding)
            else:
                merged_data = gpd.read_file(file)
            continue
        if encoding is not None:
            data = gpd.read_file(file, encoding=encoding)
        else:
            data = gpd.read_file(file)
        merged_data = pd.concat([merged_data, data], sort=True)
    return merged_data

