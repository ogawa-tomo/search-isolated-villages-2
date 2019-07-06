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
        # point_pop_lower_limit = int(request.form["point_pop_lower_limit"])
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
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=POST_OFFICE, setting=fs, faculty_ja="郵便局", result=result)


@app.route("/elementary_school")
def index_elementary_school():
    return render_template("faculty.html", faculty="elementary_school", faculty_ja="小学校")


@app.route("/elementary_school/result", methods=["GET", "POST"])
def result_elementary_school():
    faculty = ELEMENTARY_SCHOOL
    region = request.form["region"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=ELEMENTARY_SCHOOL, setting=fs, faculty_ja="小学校", result=result)


if __name__ == "__main__":
    app.run()
