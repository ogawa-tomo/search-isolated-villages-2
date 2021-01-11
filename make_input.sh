#!/bin/bash

# pipfileにgeopandasを記載していると、なぜかherokuにデプロイできない。
# したがってデータ生成時のみインストールし、終わったらアンインストールする。
pipenv install geopandas

pipenv run python download_raw_data.py
pipenv run python make_input_main_1.py
pypy make_input_main_2.py
pypy make_input_main_3.py
pypy make_input_main_4.py
pypy make_input_main_5.py
pipenv run python make_input_main_6.py

pypy make_input_tokaido_taiketsu.py

for faculty in elementary_school post_office new_town michinoeki station abandoned_station research_institute
do
echo $faculty
pipenv run python make_input_faculty_main_1.py $faculty
pypy make_input_faculty_main_2.py $faculty
pipenv run python make_input_faculty_main_3.py $faculty
done

pipenv uninstall geopandas
