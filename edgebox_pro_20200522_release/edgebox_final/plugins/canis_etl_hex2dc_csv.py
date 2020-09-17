# -*- coding: utf-8 -*-
"""
Create Time: 2020/4/30 8:30
Author: Liuqing Zhang
"""
import time
import pandas as pd
import numpy as np
# path = r"G:\edgebox_pro\edgebox_final\data_ch0_1587436303.txt"
path = r"C:\Users\liu\Desktop\沖壓流程Doc\cy\20200109CANIS PRO与NI数据对比\对比2\CanisPro_0109\振动传感器\data-chan0-64k-2020-01-09-15-10-43 - 副本.txt"
path1 = r"C:\Users\liu\Desktop\沖壓流程Doc\cy\20200109CANIS PRO与NI数据对比\对比2\CanisPro_0109\振动传感器\data-chan0-64k.pk"

def etl_hex2dc_csv(fileName, toFileName=""):
    t1 = time.time()
    with open(fileName, "r") as target:
        lines = target.read().splitlines()
        lines2int = [int(l,16) for l in lines]
    lines2arr = np.array(lines2int)
    idx_l = np.where(lines2arr < np.power(2, 23))
    idx_h = np.where(lines2arr > np.power(2, 23))
    ac_arr = lines2arr.astype(np.float32)
    ac_arr[idx_l] = ac_arr[idx_l] * 4.5 / (np.power(2, 23) -1) * (4.64/2.05)
    # ac_arr[idx_l] = ac_arr[idx_l].dot(4.5).dot(4.64/2.05) / (np.power(2, 23) -1)
    ac_arr[idx_h] = 4.5 * (ac_arr[idx_h] - np.power(2, 24)) / (np.power(2, 23)-1) * (4.64 / 2.05)
    # # ac_arr[idx_h] = (ac_arr[idx_h] - np.power(2, 24)).dot(4.5) / (np.power(2, 23)-1) * (4.64 / 2.05)
    # pd.DataFrame(ac_arr, columns=["Sensor"]).to_csv(toFileName,
    #                                                 chunksize=20000,
    #                                                 index=False)
    if toFileName != "":
        pd.DataFrame(ac_arr).to_pickle(toFileName)
    t4 = time.time()
    print("ms:"+ str((t4-t1)*1000))
    return ac_arr


# etl_hex2dc_csv(path, path1)