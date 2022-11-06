#!/bin/bash

for year in 2015 2020
do

pypy make_input_main_5.py $year
pipenv run python make_input_main_6.py $year

for faculty in elementary_school post_office new_town michinoeki station abandoned_station research_institute
do
echo $faculty
pipenv run python make_input_faculty_main_3.py $faculty $year
done

done
