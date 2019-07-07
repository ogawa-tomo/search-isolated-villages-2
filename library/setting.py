from settings.regions import *
from settings.constants import *


class Setting(object):

    def __init__(
            self,
            region,
            village_pop_lower_limit,
            village_pop_upper_limit,
            village_size_lower_limit,
            village_size_upper_limit,
            island_setting,
            key_words,
    ):
        self.region = region
        self.village_pop_lower_limit = village_pop_lower_limit
        self.village_pop_upper_limit = village_pop_upper_limit
        self.village_size_lower_limit = village_size_lower_limit
        self.village_size_upper_limit = village_size_upper_limit
        self.island_setting = island_setting
        self.key_words = key_words


class FacultySetting(object):
    """
    施設探索の設定クラス
    """

    def __init__(self, region, faculty, island_setting, key_words):
        self.region = region
        self.faculty = faculty
        self.island_setting = island_setting
        self.key_words = key_words


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
