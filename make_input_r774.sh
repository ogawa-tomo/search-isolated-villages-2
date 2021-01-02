#!/bin/bash

pypy make_input_main_5.py
pipenv run python make_input_main_6.py

for faculty in elementary_school post_office new_town michinoeki station abandoned_station research_institute
do
pipenv run python make_input_faculty_main_3.py $faculty
done
