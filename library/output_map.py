import folium
from library.point import Village, FacultyPoint, PopPoint


class OutputMap(object):

    def __init__(self, path):

        self.html_path = path
        self.map = None

    def output_map(self, points, num, pref=None):

        # 地図の中心点
        if len(points) == 0:
            # ポイントがないなら日本の中心
            lat = 35
            lon = 135
        else:
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
        self.map = folium.Map(location=[lat, lon], tiles="cartodbpositron", control_scale=True)
        # map_.add_tile_layer("OpenStreetMap", attr=copyright_osm)
        # folium.LayerControl().add_to(self.map)

        for i, p in enumerate(points[:num]):
            marker = self.get_marker(p, i + 1, pref=pref)
            marker.add_to(self.map)

        # if not os.path.isdir(fp.output_dir):
        #     os.makedirs(fp.output_dir)
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
        if type(p) is Village or type(p) is PopPoint:
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
        a_tag = "<a href=\"" + url + "\" target=_blank>Googleマップ（" + lat_lon + "）</a>"
        # popup = " ".join([desc, a_tag])

        popup = None
        if type(p) is Village:
            population = str(p.population) + "人"
            popup = "<br>".join([desc, a_tag, population])
        elif type(p) is FacultyPoint or type(p) is PopPoint:
            popup = "<br>".join([desc, a_tag])

        # marker = folium.Marker([p.latitude, p.longitude], popup=popup,
        #                        icon=folium.Icon(icon="home", prefix="fa"))
        marker = folium.Marker([p.latitude, p.longitude], popup=popup)
        return marker

    def add_r774_points(self, r774_points):
        """
        R774のポイントを追加する
        :param r774_points:
        :return:
        """

        for p in r774_points:

            # 説明URLをつくる
            descriptions = p.description.split(" ")
            descriptions_url = ""
            for d in descriptions:
                desc_url = "<a href=\"" + d + "\" target=\"_blank\">" + d + "</a><br>"
                descriptions_url += desc_url

            # マーカーのポップアップをつくる
            r774_twitter = "https://twitter.com/kendou774"
            r774_osm = "http://umap.openstreetmap.fr/ja/map/r774_368811#5/36.297/139.680"
            muramoto_twitter = "https://twitter.com/muramototomoya"
            popup = "<br>".join([
                "<b>" + p.name + "</b>",
                "",
                descriptions_url,
                "出典：",
                "<a href=\"" + r774_osm + "\" target=\"_blank\">R774@まとめ屋 さんの訪問先まとめマップ</a>",
                "R774@まとめ屋 さん <a href=\"" + r774_twitter + "\" target=\"_blank\">@kendou774</a>",
                "muramoto さん <a href=\"" + muramoto_twitter + "\" target=\"_blank\">@muramototomoya</a>"
            ])

            marker = folium.Marker([p.latitude, p.longitude], popup=popup, icon=folium.Icon(color='red', icon='info-sign'))
            marker.add_to(self.map)

        self.map.save(self.html_path)
