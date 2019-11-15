

import numpy as np
import pandas as pd
import os

import glob
import fnmatch
import pathlib
import os

col_names = ['datetime','setting1','setting2','pcount','CourseOp','ProcedureNo','WaterFlow1','WaterFlow2','motorSetting',
             'RequestRPM1','RequestRPM2','CurrentRPM1','CurrentRPM2','RPMKeep1','RPMKeep2','DehyLoadLevel','DCurrent1','DCurrent2','QCurrent1',
             'QCurrent2','LifeTestCount1','LifeTestCount2','WaterFreq','CirPumpState','vibX1','vibX2','vibY1','vibY2','vibZ1',
             'vibZ2','UB1','UB2','QCurrent21','QCurrent22','WashStartLoad1','WashStartLoad2','WashMotorLoad1','WashMotorLoad2','WaterFlow21',
             'WaterFlow22','RinseStep','MotorDir']

def extract_data(path, filename):
    print(filename)
    df = pd.read_csv(filename, sep=' ', header=None)
    #print(df.head())

    df.drop(df.columns[df.index[42:103]], axis=1, inplace=True)
    df.columns = col_names
    #print(df.head())

    idx = df.index[df['RinseStep'] == 8].tolist()
    df_output = df.loc[idx]
    #print(df_output)
    #print(df_output.values)

    df_out = pd.DataFrame()
    df_list = []
    for index, row in df_output.iterrows():
        WaterFlow = (int(hex(row['WaterFlow1']), 16) << 8) | int(hex(row['WaterFlow2']), 16)
        RequestRPM = (int(hex(row['RequestRPM1']), 16) << 8) | int(hex(row['RequestRPM2']), 16)
        CurrentRPM = (int(hex(row['CurrentRPM1']), 16) << 8) | int(hex(row['CurrentRPM2']), 16)
        RPMKeep = (int(hex(row['RPMKeep1']), 16) << 8) | int(hex(row['RPMKeep2']), 16)
        DCurrent = (int(hex(row['DCurrent1']), 16) << 8) | int(hex(row['DCurrent2']), 16)
        QCurrent = (int(hex(row['QCurrent1']), 16) << 8) | int(hex(row['QCurrent2']), 16)
        LifeTestCount = (int(hex(row['LifeTestCount1']), 16) << 8) | int(hex(row['LifeTestCount2']), 16)
        vibX = (int(hex(row['vibX1']), 16) << 8) | int(hex(row['vibX2']), 16)
        vibY = (int(hex(row['vibY1']), 16) << 8) | int(hex(row['vibY2']), 16)
        vibZ = (int(hex(row['vibZ1']), 16) << 8) | int(hex(row['vibZ2']), 16)
        UB = (int(hex(row['UB1']), 16) << 8) | int(hex(row['UB2']), 16)
        QCurrent2 = (int(hex(row['QCurrent21']), 16) << 8) | int(hex(row['QCurrent22']), 16)
        WashStartLoad = (int(hex(row['WashStartLoad1']), 16) << 8) | int(hex(row['WashStartLoad2']), 16)
        WashMotorLoad = (int(hex(row['WashMotorLoad1']), 16) << 8) | int(hex(row['WashMotorLoad2']), 16)
        WaterFlow2 = (int(hex(row['WaterFlow21']), 16) << 8) | int(hex(row['WaterFlow22']), 16)
        if df_out.shape[0] >= 140 and RequestRPM != 0:
            continue
        if RequestRPM == 0 and df_out.shape[0] != 0:
            df_out = df_out.reset_index(drop=True)
            df_list.append(df_out)
            df_out = pd.DataFrame()
        elif RequestRPM == 0:
            continue
        else:
            col_names_new = [
                             'RequestRPM', 'CurrentRPM',
                             'WaterFreq', 'vibX', 'vibY', 'vibZ', 'UB', 'QCurrent2', 'RinseStep']
            a = pd.DataFrame(data=[[RequestRPM, CurrentRPM, row['WaterFreq'], vibX, vibY, vibZ,
                                    UB, QCurrent2, row['RinseStep']]], columns=col_names_new)
            df_out = df_out.append(a)

    index = 0
    for dfs in df_list:
        index = index + 1

        dfs.to_csv(filename + '{0}_Extract.txt'.format(index),
                   sep=' ',
                   index=False, header=False)

path = "D:/StillworkData/1kg타월/"
pattern = '*[0-9][0-9][0-9].txt'
file_list = glob.glob(path + pattern)

for filename in file_list:
    extract_data(path, filename)








#df_output.to_csv(r'D:/StillworkData/1kg타월/V600_no01_1kgTowel_C3_HIGH_20190611_01_001_Extract.txt', sep=' ', index=False, header=False)
