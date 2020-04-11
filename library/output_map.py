import folium
from library.point import Village, FacultyPoint
import os
import settings.file_path as fp
from library.pop_polygon_dao import PopPolygonDAO
import pandas as pd
import csv


class OutputMap(object):

    def __init__(self, path):

        self.html_path = path
        self.geojson_path = path.replace(".html", ".geojson")
        self.csv_path = path.replace(".html", "csv")
        self.map = None

    def output_map(self, points, num, pref=None):

        # 集落なしなら表示なし
        if len(points) == 0:
            return

        # 地図の中心点
        lat_list = []
        lon_list = []
        for p in points:
            lat_list.append(p.latitude)
            lon_list.append(p.longitude)
        lat = (min(lat_list) + max(lat_list)) / 2
        lon = (min(lon_list) + max(lon_list)) / 2

        copyright_osm = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        # copyright_stamen = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>,' \
        #                    ' under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. ' \
        #                    'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, ' \
        #                    'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'

        # self.map = folium.Map(location=[lat, lon], tiles="Stamen Terrain", attr=copyright_stamen)
        self.map = folium.Map(location=[lat, lon], tiles="cartodbpositron")
        # map_.add_tile_layer("OpenStreetMap", attr=copyright_osm)
        # folium.LayerControl().add_to(self.map)

        for i, p in enumerate(points[:num]):
            marker = self.get_marker(p, i + 1, pref=pref)
            marker.add_to(self.map)

        self.map.save(self.html_path)

    @staticmethod
    def get_marker(p, rank, pref=None):
        """
        マーカーを作る
        :param p:
        :param rank:
        :param pref: 都道府県指定（指定された場合、「～県〇位」のように記述）
        :return:
        """
        if type(p) is Village:
            name = "".join([p.pref, p.city, p.district])
        elif type(p) is FacultyPoint:
            name = p.name
        else:
            raise Exception

        if pref is None:
            desc = "".join([str(rank), "位：<br>", name])
        else:
            desc = "".join([pref, str(rank), "位：<br>", name])

        # lat_lon = ", ".join([str(p.latitude_round), str(p.longitude_round)])
        # popup = " ".join([desc, lat_lon])

        # url = p.get_google_map_url()
        # popup = " ".join([desc, url])

        lat_lon = ",".join([str(p.latitude_round), str(p.longitude_round)])
        url = p.get_google_map_url()
        a_tag = "<a href=\"" + url + "\" target=_blank>Google_Map(" + lat_lon + ")</a>"
        # popup = " ".join([desc, a_tag])
        population = str(p.population) + "人"
        popup = "<br>".join([desc, a_tag, population])

        # marker = folium.Marker([p.latitude, p.longitude], popup=popup,
        #                        icon=folium.Icon(icon="home", prefix="fa"))
        marker = folium.Marker([p.latitude, p.longitude], popup=popup)
        return marker

    def add_polygons(self, polygons):
        """
        ポリゴンのコロプレス図を追加する
        :param polygons:
        :return:
        """
        # ポリゴンのgeojsonを取得
        dao = PopPolygonDAO("hoge")  # pathは関係ない
        geojson_data = dao.get_polygon_geojson_data(polygons)
        # with open(self.geojson_path, "w", encoding="utf8") as f:
        #     f.write(geojson_data)

        # ポリゴンのpandasデータフレームを作る
        with open(self.csv_path, "w", encoding="utf8") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(["key_code", "population"])
            for p in polygons:
                writer.writerow([p.key_code, p.population])
        polygon_df = pd.read_csv(self.csv_path)
        os.remove(self.csv_path)
        polygon_df["key_code"] = polygon_df["key_code"].astype("str")

        # コロプレス図をつくる
        folium.Choropleth(
            geo_data=geojson_data,
            name="choropleth",
            data=polygon_df,
            columns=["key_code", "population"],
            key_on="feature.properties.KEY_CODE",
            fill_color="OrRd",
            threshold_scale=[0, 25, 50, 75, 100, 125, 150, 10000],
            fill_opacity=0.7,
            line_opacity=0.2,
        ).add_to(self.map)

        self.map.save(self.html_path)















