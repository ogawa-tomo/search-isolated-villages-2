import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
from library.json_data_reader import JsonR774PointDataReader
import settings.file_path as fp
from library.r774_point_dao import R774PointDAO
import library.make_input_functions as mif

try:
    year = sys.argv[1]
except IndexError:
    raise Exception('引数でデータ年を指定してください')

def main():
    """
    r774のデータを読み込んで作成
    :return:
    """

    # 小地域データ読み込み
    region_points = mif.read_region_data(fp.raw_region_json_dir(year))

    # r774geojsonデータを読み込み
    r774_data_reader = JsonR774PointDataReader(fp.r774_raw_json_file)
    r774_points = r774_data_reader.get_points()

    # r774データに住所登録
    mif.register_address(r774_points, region_points)

    # r774データを書き出し
    r774_dao = R774PointDAO(fp.r774_file)
    r774_dao.make_r774_point_data(r774_points)


if __name__ == "__main__":
    main()
