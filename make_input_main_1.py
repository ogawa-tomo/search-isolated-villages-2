import glob
import os
from tqdm import tqdm
import settings.file_path as fp
import library.shp_functions as sf


def main():
    """
    zipファイルを展開する
    メッシュと小地域のshpファイルをポイント変換しjsonのtxtファイルにして吐き出す
    :return:
    """

    print("zipファイルを展開")
    sf.extract_zip(fp.raw_mesh_shp_dir)
    sf.extract_zip(fp.raw_region_shp_dir)
    sf.extract_zip(fp.raw_pop_dir)

    print("境界データをshpからjsonに変換")
    sf.shp_dir_to_json_dir(fp.raw_mesh_shp_dir, fp.raw_mesh_json_dir)

    print("小地域データをshpからjsonに変換")
    sf.shp_dir_to_json_dir(fp.raw_region_shp_dir, fp.raw_region_json_dir)


if __name__ == "__main__":
    main()
