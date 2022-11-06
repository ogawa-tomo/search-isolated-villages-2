from settings.regions import *
from settings.constants import *
import library.common_function as cf

class Setting(object):

    def __init__(
            self,
            year,
            region,
            island_setting,
            key_words,
    ):
        self.year = year
        self.region = region
        self.island_setting = island_setting
        self.key_words = key_words
    
    def extract_objects(self, objects):
        """
        地域、島設定、キーワードをもとにオブジェクトを抽出して返す
        """
        extracted_objects = []

        for ob in objects:
            # 地域チェック
            if self.region == ZENKOKU:
                pass
            elif RegionSetting.is_region(self.region):
                # 地域指定のとき
                if RegionSetting.get_region_by_pref(ob.pref) != self.region:
                    continue
            elif RegionSetting.is_pref(self.region):
                # 都道府県指定のとき
                if ob.pref != self.region:
                    continue
            else:
                raise Exception("地域が不正です")

            # 島チェック
            if self.island_setting == INCLUDE_ISLANDS:
                # どちらでも通す
                pass
            elif self.island_setting == EXCLUDE_ISLANDS:
                if ob.is_island:
                    # 島だったら通さない
                    continue
            elif self.island_setting == ONLY_ISLANDS:
                if not ob.is_island:
                    # 本土だったら通さない
                    continue
            else:
                raise Exception("離島設定が不正です")

            # キーワードチェック
            if self.key_words != "":
                key_words = self.key_words.split()
                address = ob.pref + ob.city + ob.district
                key_word_in_address = True
                for key_word in key_words:
                    if key_word not in address:
                        # 住所に含まれていないキーワードが1つでもあればFalse
                        key_word_in_address = False
                        break
                if not key_word_in_address:
                    continue

            extracted_objects.append(ob)

        return extracted_objects
    
    def extract_r774_points(self, r774_points):
        """
        r774ポイントを条件に従って抽出する
        :param r774_points:
        :param s:
        :return:
        """

        extracted_points = []
        for p in r774_points:

            # 地域チェック
            if self.region == ZENKOKU:
                pass
            elif RegionSetting.is_region(self.region):
                # 地域指定のとき
                if RegionSetting.get_region_by_pref(p.pref) != self.region:
                    continue
            elif RegionSetting.is_pref(self.region):
                # 都道府県指定のとき
                if p.pref != self.region:
                    continue
            else:
                raise Exception("地域が不正です")

            # キーワードチェック
            if self.key_words != "":
                key_words = s.key_words.split()
                address = p.pref + p.city + p.district + p.name
                key_word_in_address = True
                for key_word in key_words:
                    if key_word not in address:
                        # 住所に含まれていないキーワードが1つでもあればFalse
                        key_word_in_address = False
                        break
                if not key_word_in_address:
                    continue

            extracted_points.append(p)

        return extracted_points


class VillageSetting(Setting):
    """
    集落探索の設定クラス
    """

    def __init__(
            self,
            year,
            region,
            village_pop_lower_limit,
            village_pop_upper_limit,
            village_size_lower_limit,
            village_size_upper_limit,
            island_setting,
            key_words,
    ):
        super().__init__(year, region, island_setting, key_words)
        # self.region = region
        self.village_pop_lower_limit = village_pop_lower_limit
        self.village_pop_upper_limit = village_pop_upper_limit
        self.village_size_lower_limit = village_size_lower_limit
        self.village_size_upper_limit = village_size_upper_limit
        # self.island_setting = island_setting
        # self.key_words = key_words
    
    def extract_villages(self, villages):

        """
        集落を条件に従って抽出する
        """

        all_villages = self.extract_objects(villages)
        extracted_villages = []

        for v in all_villages:

            # 人口・サイズチェックのみ追加
            if self.village_pop_lower_limit <= v.population <= self.village_pop_upper_limit \
                    and self.village_size_lower_limit <= v.size <= self.village_size_upper_limit:
                extracted_villages.append(v)

        return extracted_villages


class FacultySetting(Setting):
    """
    施設探索の設定クラス
    """

    def __init__(self, year, region, faculty, island_setting, key_words):
        super().__init__(year, region, island_setting, key_words)
        # self.region = region
        self.faculty = faculty
        # self.island_setting = island_setting
        # self.key_words = key_words


class Result(object):
    """
    結果を記録するクラス
    """
    def __init__(self, objects, setting, map_file):
        # self.sorted_villages = sorted_villages
        self.objects = objects
        self.setting = setting
        self.region = setting.region
        self.num = OUTPUT_HTML_NUM
        self.map_file = map_file
        self.output_map_num = OUTPUT_MAP_NUM

        # 都道府県判定（メッシュ地図を表示するかの判断のため）
        if RegionSetting.is_pref(setting.region):
            self.is_pref = True
        else:
            self.is_pref = False

    def get_mesh_map_get_url(self):

        # 地図の中心点
        lat_list = []
        lon_list = []
        for v in self.objects:
            lat_list.append(v.latitude)
            lon_list.append(v.longitude)
        lat = (min(lat_list) + max(lat_list)) / 2
        lon = (min(lon_list) + max(lon_list)) / 2
        # url = "/mesh_map?lat=" + str(lat) + "&lon=" + str(lon) + "&zoom=" + "10&map_file=" + self.map_file
        url = cf.get_mesh_map_get_url(lat, lon, ZOOM_DEFAULT, self.map_file)
        return url


class RegionSetting(object):
    """
    地域区分設定を扱うクラス
    """

    region_prefs = REGION_PREFS
    # calc_segment = CALC_SEGMENT
    calc_segment_regions = CALC_SEGMENT_REGIONS
    # region_kanji = REGION_KANJI

    @classmethod
    def get_region_prefs(cls, region):
        if region == ZENKOKU:
            return cls.get_all_prefs()
        else:
            return cls.region_prefs[region]

    @classmethod
    def get_all_prefs(cls):
        all_prefs = []
        for region in cls.region_prefs.keys():
            all_prefs.extend(cls.region_prefs[region])
        return all_prefs

    @classmethod
    def is_region(cls, name):
        """
        地域ならTrue
        :param name:
        :return:
        """
        if name in cls.get_region_list():
            return True
        else:
            return False

    @classmethod
    def is_pref(cls, name):
        """
        都道府県ならTrue
        :param name:
        :return:
        """
        if name in cls.get_all_prefs():
            return True
        else:
            return False

    @classmethod
    def get_calc_segment(cls, region):
        for segment in cls.calc_segment_regions.keys():
            segment_regions = cls.calc_segment_regions[segment]
            if region in segment_regions:
                return segment
        return Exception("地域名が不正です")

    # @classmethod
    # def get_region_kanji(cls, region):
    #     return cls.region_kanji[region]

    @classmethod
    def get_calc_segment_prefs_by_region(cls, region):
        calc_segment = cls.get_calc_segment(region)
        regions = cls.calc_segment_regions[calc_segment]
        prefs = []
        for region in regions:
            temp_prefs = cls.get_region_prefs(region)
            prefs.extend(temp_prefs)
        return prefs

    @classmethod
    def get_calc_segments(cls):
        return cls.calc_segment_regions.keys()

    @classmethod
    def get_region_by_pref(cls, pref):
        for region in cls.region_prefs.keys():
            if pref in cls.region_prefs[region]:
                return region
        raise Exception

    @classmethod
    def get_calc_segment_by_pref(cls, pref):
        region = cls.get_region_by_pref(pref)
        return cls.get_calc_segment(region)

    @classmethod
    def get_region_list(cls):
        return cls.region_prefs.keys()
