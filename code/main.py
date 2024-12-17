# %% [markdown]
# ### 参考文献
# pygribで気象庁のGRIB2ファイルを読む：https://qiita.com/kurukuruz/items/6fc0be9efa34a2fd6741

# %%
# coding: utf-8
import os
import subprocess
import pygrib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
import wxparams as wx

# %%
df_input = pd.read_excel('../input.xlsx', dtype=str, index_col=None)
print(df_input)

# %%
latitude_ls = list(df_input['latitude'])
latitude_ls = [float(i) for i in latitude_ls]
longitude_ls = list(df_input['longitude'])
longitude_ls = [float(i) for i in longitude_ls]
year_ls = list(df_input['year'])
month_ls = list(df_input['month'])
day_ls = list(df_input['day'])
time_ls = list(df_input['time'])
size = df_input.shape[0]

# %%
cwd = os.getcwd()

# GSM
# url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2020/08/01/Z__C_RJTD_20200801060000_GSM_GPV_Rjp_Lsurf_FD0000-0312_grib2.bin'

# MSM
# url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2023/08/02/Z__C_RJTD_20230802000000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin'
url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2023/08/02/Z__C_RJTD_20230802000000_MSM_GPV_Rjp_Lsurf_FH16-33_grib2.bin'
# url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2023/08/02/Z__C_RJTD_20230802000000_MSM_GPV_Rjp_Lsurf_FH34-39_grib2.bin'
# url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2023/08/02/Z__C_RJTD_20230802000000_MSM_GPV_Rjp_Lsurf_FH40-51_grib2.bin'
# url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2023/08/02/Z__C_RJTD_20230802000000_MSM_GPV_Rjp_Lsurf_FH52-78_grib2.bin'

# ダウンロード
# subprocess.run(['curl', '-O', url_surf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)

# %%
## GRIB2ファイルを読み込み，変数に格納して出力する関数
def readgrib2(url_surf):
    file_surf = os.path.join(grib2dir, os.path.basename(url_surf))
    grbs = pygrib.open(file_surf)
    return(file_surf, grbs)

# file_surf, grbs = readgrib2(url_surf)

# %%
for k in range(size):
    latitude = latitude_ls[k]
    longitude = longitude_ls[k]
    time_diff = timedelta(hours=9) # UTCとJSTの差分
    df = pd.DataFrame()

    datatype = "MSM"
    year = year_ls[k]
    month = month_ls[k]
    date = day_ls[k]
    time = time_ls[k]
    initialtime = f"{year}{month}{date}{time}"
    cwd = os.getcwd()
    os.chdir('../storage/grib2')
    grib2dir = os.getcwd()
    os.chdir('../../code')

    url_list = [f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{year}/{month}/{date}/Z__C_RJTD_{initialtime}_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin'\
    ,f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{year}/{month}/{date}/Z__C_RJTD_{initialtime}_MSM_GPV_Rjp_Lsurf_FH16-33_grib2.bin'\
    ,f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{year}/{month}/{date}/Z__C_RJTD_{initialtime}_MSM_GPV_Rjp_Lsurf_FH34-39_grib2.bin'\
    ,f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{year}/{month}/{date}/Z__C_RJTD_{initialtime}_MSM_GPV_Rjp_Lsurf_FH40-51_grib2.bin'\
    ,f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{year}/{month}/{date}/Z__C_RJTD_{initialtime}_MSM_GPV_Rjp_Lsurf_FH52-78_grib2.bin']

    if time != "000000" and time != "120000":
        url_list = url_list[0:3]

    for url_surf in url_list:
        os.chdir('../storage/grib2')
        # subprocess.run(['curl', '-O', url_surf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd) # データダウンロード
        subprocess.run(['curl', '-O', url_surf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # データダウンロード
        os.chdir('../../code')
        file_surf, grbs = readgrib2(url_surf)
        # データを取り出す
        prmsl = grbs.select(parameterName='Pressure reduced to MSL')
        sp    = grbs.select(parameterName='Pressure')
        uwind = grbs.select(parameterName='u-component of wind')
        vwind = grbs.select(parameterName='v-component of wind')
        temp  = grbs.select(parameterName='Temperature')
        rh    = grbs.select(parameterName='Relative humidity')
        lcc   = grbs.select(parameterName='Low cloud cover')
        mcc   = grbs.select(parameterName='Medium cloud cover')
        hcc   = grbs.select(parameterName='High cloud cover')
        tcc   = grbs.select(parameterName='Total cloud cover')
        tp    = grbs.select(parameterName='Total precipitation')
        dswrf = grbs.select(parameterName='Downward short-wave radiation flux')

        df1d = pd.DataFrame({
            "validDate": [msg.validDate + time_diff for msg in temp],
            "temperature": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] - 273.15 for msg in temp
            ],
            "rh": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in rh
            ],
            "prmsl": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in prmsl
            ],
            "sp": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in sp
            ],
            "uwind": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in uwind
            ],
            "vwind": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in vwind
            ],
            "lcc": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in mcc
            ],
            "mcc": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in rh
            ],
            "hcc": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in hcc
            ],
            "tcc": [
                msg.data(
                    lat1=latitude-0.025,
                    lat2=latitude+0.025,
                    lon1=longitude-0.03125,
                    lon2=longitude+0.03125,
                )[0][0][0] for msg in tcc
            ],
            # "dswrf": [
            #     msg.data(
            #         lat1=latitude-0.025,
            #         lat2=latitude+0.025,
            #         lon1=longitude-0.03125,
            #         lon2=longitude+0.03125,
            #     )[0][0][0] for msg in dswrf
            # ]
        })
        print(df1d)
        print("processing")
        df = pd.concat([df, df1d])

    #　風速をU, V成分から風向風速に変換する
    U = df["uwind"]
    V = df["vwind"]
    Wspd, Wdir = wx.UV_to_SpdDir(U, V) # UV_to_SpdDir(U, V)
    df["windspeed"] = Wspd
    df["winddirection"] = Wdir

    print(df)
    df.to_csv(f'../storage/csv/{latitude}_{longitude}_{initialtime}.csv')

print("--Completed--")


