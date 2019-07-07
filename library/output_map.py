import folium
from library.point import Village, FacultyPoint
import os
import settings.file_path as fp


class OutputMap(object):

    def __init__(self, path):

        self.path = path

    def output_map(self, points, num):

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
        copyright_stamen = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>,' \
                           ' under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. ' \
                           'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, ' \
                           'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'

        map_ = folium.Map(location=[lat, lon], tiles="Stamen Terrain", attr=copyright_stamen)
        map_.add_tile_layer("OpenStreetMap", attr=copyright_osm)
        folium.LayerControl().add_to(map_)

        for i, p in enumerate(points[:num]):
            marker = self.get_marker(p, i + 1)
            marker.add_to(map_)

        if not os.path.isdir(fp.output_dir):
            os.makedirs(fp.output_dir)
        map_.save(self.path)

    @staticmethod
    def get_marker(p, rank):
        if type(p) is Village:
            name = "".join([p.pref, p.city, p.district])
        elif type(p) is FacultyPoint:
            name = p.name
        else:
            raise Exception
        desc = "".join([str(rank), "位：", name])

        # lat_lon = ", ".join([str(p.latitude_round), str(p.longitude_round)])
        # popup = " ".join([desc, lat_lon])

        # url = p.get_google_map_url()
        # popup = " ".join([desc, url])

        lat_lon = ",".join([str(p.latitude_round), str(p.longitude_round)])
        url = p.get_google_map_url()
        a_tag = "<a href=\"" + url + "\" target=_blank>" + lat_lon + "</a>"
        # popup = " ".join([desc, a_tag])
        popup = "<br>".join([desc, a_tag])

        marker = folium.Marker([p.latitude, p.longitude], popup=popup,
                               icon=folium.Icon(icon="home", prefix="fa"))
        return marker



