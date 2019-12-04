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


@app.route("/<faculty>")
def index_faculty(faculty):
    """
    秘境施設探索ツール
    :param faculty: 施設名
    :return:
    """
    return render_template("faculty.html", faculty=faculty, faculty_ja=get_faculty_ja(faculty))


@app.route("/<faculty>/result", methods=["GET", "POST"])
def result_faculty(faculty):
    """
    秘境施設探索ツール結果
    :param faculty: 施設名
    :return:
    """
    faculty = faculty
    region = request.form["region"]
    island_setting = request.form["island_setting"]
    key_words = request.form["key_words"]
    fs = FacultySetting(region, faculty, island_setting, key_words)
    result = search_faculty_main.main(fs)
    return render_template("faculty.html", faculty=faculty, setting=fs, faculty_ja=get_faculty_ja(faculty), result=result)


if __name__ == "__main__":
    app.run()
