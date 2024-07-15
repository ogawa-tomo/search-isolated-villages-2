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
    return render_template("index.html")


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
    region = request.args.get("region")
    village_pop_lower_limit = int(request.args.get("populationLowerLimit"))
    village_pop_upper_limit = int(request.args.get("populationUpperLimit"))
    village_size_lower_limit = 0 # int(request.form["village_size_lower_limit"])
    village_size_upper_limit = 100 # int(request.form["village_size_upper_limit"])
    island_setting = request.args.get("islandSetting")
    key_words = request.args.get("keyWords")
    page = int(request.args.get("page"))

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

    per_page = 20
    offset = per_page * (page - 1)

    # 集落データを読み込み
    dao = VillageDAO(fp.villages_file(setting.year))
    villages_data = dao.read_village_data()
    villages_objects = setting.extract_villages(villages_data)
    response = {
        "pages": - (-len(villages_objects) // per_page),
        "per_page": per_page,
        "villages": []
    }
    limited_villages_objects = villages_objects[offset:offset + per_page]
    for village in limited_villages_objects:
        response["villages"].append(village.to_dict())
    
    return json.dumps(response, ensure_ascii=False)

@app.route("/api/<faculty>/result", methods=["GET"])
def api_faculty_result(faculty):
    year = 2020 # request.form["year"]
    region = request.args.get("region")
    island_setting = request.args.get("islandSetting")
    key_words = request.args.get("keyWords")
    page = int(request.args.get("page"))

    faculty_setting = FacultySetting(year, region, faculty, island_setting, key_words)
    input_file = fp.get_faculty_csv_file(faculty_setting.faculty, faculty_setting.year)

    # 施設データを読み込み
    dao = FacultyDAO(input_file)
    faculty_points = dao.read_faculty_point_data()

    # 施設を条件に従って抽出
    faculty_objects = faculty_setting.extract_objects(faculty_points)

    per_page = 20
    offset = per_page * (page - 1)
    response = {
        "pages": - (-len(faculty_objects) // per_page),
        "per_page": per_page,
        "faculties": []
    }
    limited_faculty_objects = faculty_objects[offset:offset + per_page]
    for faculty_object in limited_faculty_objects:
        response["faculties"].append(faculty_object.to_dict())
    
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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
