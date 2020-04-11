import sys
sys.path.append("./")  # pypyで実行するためにこれが必要
import glob
from library.json_data_reader import *
from library.point_dao import PopPointDAO
from library.pop_polygon_dao import PopPolygonDAO
import settings.file_path as fp


def main():
    """
    人口ポリゴンデータのcsvを都道府県別に作成
    :return:
    """

    # 人口データ読み込み
    dao = PopPointDAO(fp.pop_point_file)
    all_points = dao.read_pop_point_data()

    # 人口ポリゴンデータの作成
    make_mesh_polygon_data(fp.raw_mesh_json_polygon_dir, all_points, fp.pop_polygon_dir)


def make_mesh_polygon_data(raw_mesh_json_polygon_dir, all_points, pop_polygon_dir):
    """
    メッシュポリゴンのデータリストを作成し都道府県ごとに書き込み
    :param raw_mesh_json_polygon_dir:
    :param all_points:
    :param pop_polygon_dir
    :return:
    """
    print("メッシュポリゴンデータ作成")

    # 書き出しファイルを都道府県ごとに初期化
    for pref in RegionSetting.get_all_prefs():
        polygon_dao = PopPolygonDAO(pop_polygon_dir + "/" + pref + ".csv")
        polygon_dao.clear_pop_polygon_data()
    # polygon_dao = PopPolygonDAO(pop_polygon_file)
    # polygon_dao.clear_pop_polygon_data()

    # 1次メッシュ区分ごとに処理しファイルに追記していく
    mesh_files = glob.glob(os.path.join(raw_mesh_json_polygon_dir, "*.txt"))
    matched_points = 0  # ポリゴンとマッチしたポイントの数
    for mesh_file in tqdm(mesh_files):

        # 都道府県ごとのポリゴンリストを初期化
        all_polygons_in_pmesh = {}
        for pref in RegionSetting.get_all_prefs():
            all_polygons_in_pmesh[pref] = []

        # メッシュデータ読み込み
        mpd = JsonMeshPolygonDataReader(mesh_file)

        # 人口ゼロも含めて全てのポリゴン
        all_polygons_in_pmesh_including_zero = mpd.get_polygons()

        # keyが一致するポリゴンを探し、ポリゴンに同じ値を格納する
        points = all_points[matched_points:]  # すでにマッチしたポイントは除外して探索
        searched_polygons = 0
        for point in points:
            polygons = all_polygons_in_pmesh_including_zero[searched_polygons:]  # 探し終わったポリゴンを除外して探索
            for polygon in polygons:
                searched_polygons += 1  # 探索したポリゴンの数
                if polygon.key_code == point.key_code:

                    # 同じkeycodeのポイントが見つかったら、同じ値を格納
                    polygon.id = point.id
                    polygon.population = point.population
                    polygon.latitude = point.latitude
                    polygon.longitude = point.longitude
                    polygon.pref = point.pref
                    polygon.city = point.city
                    polygon.district = point.district
                    polygon.is_island = point.is_island

                    # ポリゴンを都道府県ごとにリストに追加
                    all_polygons_in_pmesh[polygon.pref].append(polygon)

                    # マッチしたポイントをカウント
                    matched_points += 1
                    break

            # 一次メッシュ内の全てのポリゴンを探索したら、break
            if searched_polygons >= len(all_polygons_in_pmesh_including_zero):
                break

        # 都道府県ごとに書き出し
        for pref in RegionSetting.get_all_prefs():
            polygon_dao = PopPolygonDAO(pop_polygon_dir + "/" + pref + ".csv")
            polygon_dao.add_pop_polygon_data(all_polygons_in_pmesh[pref])


if __name__ == "__main__":
    main()
