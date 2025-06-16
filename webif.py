from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from library.setting import Setting, FacultySetting, VillageSetting
import time
import search_village_main
import search_faculty_main
import search_max_urban_points_main
import uranai_main
import uranai_faculty_main
from settings.constants import *
from library import common_function as cf
import settings.file_path as fp
import tokaido_taiketsu_main
import json
from library.village_dao import VillageDAO
from library.faculty_dao import FacultyDAO

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
title = "秘境集落探索ツール"


@app.route("/")
def index():
    """
    秘境集落探索ツール
    :return:
    """
    return redirect("https://search-isolated-villages.com")


@app.route("/result", methods=["GET", "POST"])
def post():
    """
    秘境集落探索ツール結果
    :return:
    """
    if request.method == "POST":

        start = time.time()

        year = request.form["year"]
        region = request.form["region"]
        village_pop_lower_limit = int(request.form["village_pop_lower_limit"])
        village_pop_upper_limit = int(request.form["village_pop_upper_limit"])
        village_size_lower_limit = int(request.form["village_size_lower_limit"])
        village_size_upper_limit = int(request.form["village_size_upper_limit"])
        island_setting = request.form["island_setting"]
        key_words = request.form["key_words"]

        setting = VillageSetting(
            year,
            region,
            village_pop_lower_limit,
            village_pop_upper_limit,
            village_size_lower_limit,
            village_size_upper_limit,
            island_setting,
            key_words
        )

        result = search_village_main.main(setting)

        elapsed_time = time.time() - start
        print(str(elapsed_time) + "[sec]")

        return render_template("index.html", result=result, setting=setting)
    else:
        return redirect(url_for('index'))

@app.route("/api/result", methods=["GET"])
def api_result():

    year = 2020 # request.form["year"]
    region = convert_region_name(request.args.get("area"))
    village_pop_lower_limit = int(request.args.get("populationLowerLimit"))
    village_pop_upper_limit = int(request.args.get("populationUpperLimit"))
    village_size_lower_limit = 0 # int(request.form["village_size_lower_limit"])
    village_size_upper_limit = 100 # int(request.form["village_size_upper_limit"])
    island_setting = convert_island_setting(request.args.get("islandSetting"))
    key_words = request.args.get("keywords")

    setting = VillageSetting(
        year,
        region,
        village_pop_lower_limit,
        village_pop_upper_limit,
        village_size_lower_limit,
        village_size_upper_limit,
        island_setting,
        key_words
    )

    # 集落データを読み込み
    dao = VillageDAO(fp.villages_file(setting.year))
    villages_data = dao.read_village_data()
    villages_objects = setting.extract_villages(villages_data)
    response = {
        "villages": [village.to_dict() for village in villages_objects]
    }
    
    return json.dumps(response, ensure_ascii=False)

@app.route("/api/<faculty>/result", methods=["GET"])
def api_faculty_result(faculty):
    year = 2020 # request.form["year"]
    region = convert_region_name(request.args.get("area"))
    island_setting = convert_island_setting(request.args.get("islandSetting"))
    key_words = request.args.get("keywords")

    faculty_setting = FacultySetting(year, region, faculty, island_setting, key_words)
    input_file = fp.get_faculty_csv_file(faculty_setting.faculty, faculty_setting.year)

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 施設を条件に従って抽出
    faculty_objects = faculty_setting.extract_objects(faculty_points)

    response = {
        "faculties": [faculty.to_dict() for faculty in faculty_objects]
    }
    
    return json.dumps(response, ensure_ascii=False)

@app.route("/api/fortune/result", methods=["GET"])
def api_fortune_result():
    village = uranai_main.api_main()
    return json.dumps(village.to_dict(), ensure_ascii=False)

@app.route("/api/fortune/<faculty>/result", methods=["GET"])
def api_fortune_faculty_result(faculty):
    result = uranai_faculty_main.main(faculty)
    return json.dumps(result.to_dict(), ensure_ascii=False)
    

@app.route("/mesh_map")
def get_mesh_map():
    """
    メッシュマップの中心とズームを編集して返す
    :return:
    """
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    zoom = request.args.get("zoom")
    map_file = request.args.get("map_file")

    # マップファイルの中心を編集
    new_map_file = os.path.join(fp.output_dir, "map_" + str(time.time()).replace(".", "") + ".html")
    print(new_map_file)
    cf.create_modified_map(lat, lon, zoom, map_file, new_map_file)
    # new_map_file = new_map_file.replace("\\", "/")  # バックスラッシュをスラッシュに置換
    q = int(os.stat(new_map_file).st_mtime)  # キャッシュをクリアして再読み込みするためのパラメータ

    return redirect(new_map_file + "?q=" + str(q))


@app.route("/uranai")
def uranai():
    return render_template("uranai.html")


@app.route("/uranai/result", methods=["GET", "POST"])
def result_uranai():
    result = uranai_main.main()
    return render_template("uranai.html", result=result)

@app.route("/<faculty>")
def index_faculty(faculty):
    """
    秘境施設探索ツール
    :param faculty: 施設名
    :return:
    """
    if faculty not in FACULTIES:
        raise Exception('施設名が不正')
    return render_template("faculty.html", faculty=faculty, faculty_ja=get_faculty_ja(faculty))


@app.route("/<faculty>/result", methods=["GET", "POST"])
def result_faculty(faculty):
    """
    秘境施設探索ツール結果
    :param faculty: 施設名
    :return:
    """
    faculty = faculty
    year = request.form["year"]
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(year, region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=faculty, setting=fs, faculty_ja=get_faculty_ja(faculty), result=result)


@app.route("/<faculty>/uranai")
def uranai_faculty(faculty):
    return render_template("uranai_faculty.html", faculty=faculty, faculty_ja=get_faculty_ja(faculty))


@app.route("/<faculty>/uranai/result", methods=["GET", "POST"])
def uranai_faculty_result(faculty):
    faculty = faculty
    result = uranai_faculty_main.main(faculty)
    return render_template("uranai_faculty.html", faculty=faculty, result=result, faculty_ja=get_faculty_ja(faculty))

@app.route("/about")
def about():
    """
    秘境集落探索ツール
    :return:
    """
    return render_template("about.html")

def convert_region_name(region_en_name):
    region_dict = {
        "all_country": "全国",
        "hokkaido": "北海道",
        "tohoku": "東北",
        "kanto": "関東",
        "hokuriku": "北陸",
        "chubu": "中部",
        "kinki": "近畿",
        "chugoku": "中国",
        "shikoku": "四国",
        "kyushu": "九州",
        "okinawa": "沖縄",
        "aomori": "青森県",
        "iwate": "岩手県",
        "miyagi": "宮城県",
        "akita": "秋田県",
        "yamagata": "山形県",
        "fukushima": "福島県",
        "ibaraki": "茨城県",
        "tochigi": "栃木県",
        "gunma": "群馬県",
        "saitama": "埼玉県",
        "chiba": "千葉県",
        "tokyo": "東京都",
        "kanagawa": "神奈川県",
        "niigata": "新潟県",
        "toyama": "富山県",
        "ishikawa": "石川県",
        "fukui": "福井県",
        "yamanashi": "山梨県",
        "nagano": "長野県",
        "gifu": "岐阜県",
        "shizuoka": "静岡県",
        "aichi": "愛知県",
        "mie": "三重県",
        "shiga": "滋賀県",
        "kyoto": "京都府",
        "osaka": "大阪府",
        "hyogo": "兵庫県",
        "nara": "奈良県",
        "wakayama": "和歌山県",
        "tottori": "鳥取県",
        "shimane": "島根県",
        "okayama": "岡山県",
        "hiroshima": "広島県",
        "yamaguchi": "山口県",
        "tokushima": "徳島県",
        "kagawa": "香川県",
        "ehime": "愛媛県",
        "kochi": "高知県",
        "fukuoka": "福岡県",
        "saga": "佐賀県",
        "nagasaki": "長崎県",
        "kumamoto": "熊本県",
        "oita": "大分県",
        "miyazaki": "宮崎県",
        "kagoshima": "鹿児島県"
    }
    return region_dict[region_en_name]

def convert_island_setting(island_setting_en):
    if island_setting_en == "exclude_islands":
        return EXCLUDE_ISLANDS
    elif island_setting_en == "include_islands":
        return INCLUDE_ISLANDS
    elif island_setting_en == "only_islands":
        return ONLY_ISLANDS

if __name__ == "__main__":
    app.run(host='0.0.0.0')
