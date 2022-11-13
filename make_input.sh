#!/bin/bash

# pipfileにgeopandasを記載していると、なぜかherokuにデプロイできない。
# したがってデータ生成時のみインストールし、終わったらアンインストールする。
pipenv install geopandas

for year in 2015 2020
do

pipenv run python download_raw_data.py $year
pipenv run python make_input_main_1.py $year
pypy make_input_main_2.py $year
pypy make_input_main_3.py $year
pypy make_input_main_4.py $year
pypy make_input_main_5.py $year
pipenv run python make_input_main_6.py $year

# pypy make_input_urban_points_for_pop_points_1.py $year
# pipenv run python make_input_urban_points_for_pop_points_2.py $year

for faculty in elementary_school post_office new_town michinoeki station abandoned_station research_institute hot_spring
do
echo $faculty
pipenv run python make_input_faculty_main_1.py $faculty
pypy make_input_faculty_main_2.py $faculty $year
pipenv run python make_input_faculty_main_3.py $faculty $year
done

done

pipenv uninstall geopandas
