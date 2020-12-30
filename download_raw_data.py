import urllib.request
import urllib.error
from settings.download_url import *
import settings.file_path as fp
import os
from tqdm import tqdm

"""
estatのページから以下のデータをダウンロードし、raw_dataフォルダに格納する
・メッシュのファイル
・人工データ
・小地域のshpファイル
"""

print("メッシュのshpファイルをダウンロード")
for mesh_num in tqdm(PRIMARY_MESH_NUMS):
    url = MESH_SHP_URL_FORMER + str(mesh_num) + MESH_SHP_URL_LATTER
    title = os.path.join(fp.raw_mesh_shp_dir, str(mesh_num) + ".zip")
    urllib.request.urlretrieve(url, title)

print("人口データをダウロード")
for mesh_num in tqdm(PRIMARY_MESH_NUMS):
    url = POP_URL_FORMER + str(mesh_num) + POP_URL_LATTER
    title = os.path.join(fp.raw_pop_dir, str(mesh_num) + ".zip")
    try:
        urllib.request.urlretrieve(url, title)
    except urllib.error.HTTPError:
        # 人口がない1次メッシュはデータがないのでエラーになる
        pass

print("小地域データをダウンロード")
for i in tqdm(range(1, 48)):
    num_str = str(i)
    if i < 10:
        num_str = "0" + num_str
    url = REGION_URL_FORMER + num_str + REGION_URL_LATTER
    title = os.path.join(fp.raw_region_shp_dir, num_str + ".zip")
    urllib.request.urlretrieve(url, title)
