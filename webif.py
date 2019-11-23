from flask import Flask, render_template, request, redirect, url_for
from library.setting import Setting, FacultySetting
import time
import search_village_main
import search_faculty_main
from settings.constants import *

app = Flask(__name__)
title = "秘境集落探索ツール"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def post():
    if request.method == "POST":

        start = time.time()

        region = request.form["region"]
        village_pop_lower_limit = int(request.form["village_pop_lower_limit"])
        village_pop_upper_limit = int(request.form["village_pop_upper_limit"])
        village_size_lower_limit = int(request.form["village_size_lower_limit"])
        village_size_upper_limit = int(request.form["village_size_upper_limit"])
        island_setting = request.form["island_setting"]
        key_words = request.form["key_words"]

        setting = Setting(
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


@app.route("/post_office")
def index_post_office():
    return render_template("faculty.html", faculty="post_office", faculty_ja="郵便局")


@app.route("/post_office/result", methods=["GET", "POST"])
def result_post_office():
    faculty = POST_OFFICE
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=POST_OFFICE, setting=fs, faculty_ja="郵便局", result=result)


@app.route("/elementary_school")
def index_elementary_school():
    return render_template("faculty.html", faculty="elementary_school", faculty_ja="小学校")


@app.route("/elementary_school/result", methods=["GET", "POST"])
def result_elementary_school():
    faculty = ELEMENTARY_SCHOOL
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=ELEMENTARY_SCHOOL, setting=fs, faculty_ja="小学校", result=result)


@app.route("/new_town")
def index_new_town():
    return render_template("faculty.html", faculty="new_town", faculty_ja="ニュータウン")


@app.route("/new_town/result", methods=["GET", "POST"])
def result_new_town():
    faculty = NEW_TOWN
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=NEW_TOWN, setting=fs, faculty_ja="ニュータウン", result=result)


@app.route("/michinoeki")
def index_michinoeki():
    return render_template("faculty.html", faculty="michinoeki", faculty_ja="道の駅")


@app.route("/michinoeki/result", methods=["GET", "POST"])
def result_michinoeki():
    faculty = MICHINOEKI
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=MICHINOEKI, setting=fs, faculty_ja="道の駅", result=result)


@app.route("/station")
def index_station():
    return render_template("faculty.html", faculty="station", faculty_ja="駅")


@app.route("/station/result", methods=["GET", "POST"])
def result_station():
    faculty = STATION
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=STATION, setting=fs, faculty_ja="駅", result=result)


@app.route("/abandoned_station")
def index_abandoned_station():
    return render_template("faculty.html", faculty="abandoned_station", faculty_ja="廃駅")


@app.route("/abandoned_station/result", methods=["GET", "POST"])
def result_abandoned_station():
    faculty = ABANDONED_STATION
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=ABANDONED_STATION, setting=fs, faculty_ja="廃駅", result=result)


@app.route("/hospital")
def index_hospital():
    return render_template("faculty.html", faculty="hospital", faculty_ja="医療機関")


@app.route("/hospital/result", methods=["GET", "POST"])
def result_hospital():
    faculty = HOSPITAL
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=HOSPITAL, setting=fs, faculty_ja="医療機関", result=result)


if __name__ == "__main__":
    app.run()
