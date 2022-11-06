import urllib.request
import urllib.error
from settings.download_url import *
import settings.file_path as fp
import os
from tqdm import tqdm
import sys

"""
estatのページから以下のデータをダウンロードし、raw_dataフォルダに格納する
・メッシュのファイル
・人工データ
・小地域のshpファイル
"""
try:
    year = sys.argv[1]
except IndexError:
    raise Exception('引数でデータ年を指定してください')

print("メッシュのshpファイルをダウンロード")
for mesh_num in tqdm(PRIMARY_MESH_NUMS):
    url = MESH_SHP_URL_FORMER + str(mesh_num) + MESH_SHP_URL_LATTER
    title = os.path.join(fp.raw_mesh_shp_dir, str(mesh_num) + ".zip")
    urllib.request.urlretrieve(url, title)

print("人口データをダウロード")
for mesh_num in tqdm(PRIMARY_MESH_NUMS):
    url = pop_url(mesh_num, year)
    title = os.path.join(fp.raw_pop_dir(year), str(mesh_num) + ".zip")
    try:
        urllib.request.urlretrieve(url, title)
    except urllib.error.HTTPError:
        # 人口がない1次メッシュはデータがないのでエラーになる
        pass

print("小地域データをダウンロード")
for i in tqdm(range(1, 48)):
    pref_num = str(i).zfill(2)
    url = region_url(pref_num, year)
    title = os.path.join(fp.raw_region_shp_dir(year), pref_num + ".zip")
    urllib.request.urlretrieve(url, title)
