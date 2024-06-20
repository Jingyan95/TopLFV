import sys
import os
import subprocess
import readline
import string
import argparse

# set up an argument parser
parser = argparse.ArgumentParser()

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'bin'))
parser.add_argument('--n', dest = 'NAMETAG', default = 'All')
ARGS = parser.parse_args()
name = ARGS.NAMETAG

import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018

SAMPLES = {}
if name == 'All' or name == '2016APV':
    SAMPLES.update(nano_files_2016APV.mc2016APV_samples)
    SAMPLES.update(nano_files_2016APV.data2016APV_samples)
if name == 'All' or name == '2016':
    SAMPLES.update(nano_files_2016.mc2016_samples)
    SAMPLES.update(nano_files_2016.data2016_samples)
if name == 'All' or name == '2017':
    SAMPLES.update(nano_files_2017.mc2017_samples)
    SAMPLES.update(nano_files_2017.data2017_samples)
if name == 'All' or name == '2018':
    SAMPLES.update(nano_files_2018.mc2018_samples)
    SAMPLES.update(nano_files_2018.data2018_samples)

addedFilesData = {"2016APV": [], "2016": [], "2017": [], "2018": []}
addedFilesTX = {"2016APV": [], "2016": [], "2017": [], "2018": []} # TTX, TTTo2L2Nu
addedFilesVV = {"2016APV": [], "2016": [], "2017": [], "2018": []} # VV, VVV, WWTo2L2Nu
addedFilesTT = {"2016APV": [], "2016": [], "2017": [], "2018": []} # TTToSemiLeptonic
addedFilesDY = {"2016APV": [], "2016": [], "2017": [], "2018": []} # DY, ZZTo2L2Nu

for key, value in SAMPLES.items():
    year = value[3]
    os.system('rm -f ' + year + '/' + key + '.root ')
    nf = value[8]
    hadd = 'hadd ' + year + '/' + key + '.root '
    if value[1] == 'data':
        addedFilesData[year].append(year + '/' + key + '.root ')
    elif ('TTToSemiLeptonic' in key):
        addedFilesTT[year].append(year + '/' + key + '.root ')
    elif ('DYM' in key or 'ZZTo2L2Nu' in key):
        addedFilesDY[year].append(year + '/' + key + '.root ')
    elif ('TTW' in key) or ('TTH' in key) or ('TTZ' in key) or ('TTTo2L2Nu' in key):
        addedFilesTX[year].append(year + '/' + key + '.root ')
    elif ('WW' in key) or ('WZ' in key) or ('ZZ' in key) or ('WWTo2L2Nu' in key):
        addedFilesVV[year].append(year + '/' + key + '.root ')
    else:
        os.system('rm -f ' + key + '.root')
        hadd = 'hadd ' + key + '.root '
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i + nf] for i in range(0, len(files), nf)]
            for num, seq in enumerate(sequance):
                hadd += year + '/' + key + '_' + str(idx) + '_' + str(num) + '.root '
            break
    os.system(hadd)

if (name == 'All') or (name == '2016APV'):
    haddData_2016APV = 'hadd 2016APV_Data.root ' + ' '.join(addedFilesData['2016APV'])
    haddTX_2016APV = 'hadd 2016APV_TX.root ' + ' '.join(addedFilesTX['2016APV'])
    haddVV_2016APV = 'hadd 2016APV_VV.root ' + ' '.join(addedFilesVV['2016APV'])
    haddTT_2016APV = 'hadd 2016APV_TT.root ' + ' '.join(addedFilesTT['2016APV'])
    haddDY_2016APV = 'hadd 2016APV_DY.root ' + ' '.join(addedFilesDY['2016APV'])
    os.system('rm -f 2016APV_Data.root')
    os.system('rm -f 2016APV_TX.root')
    os.system('rm -f 2016APV_VV.root')
    os.system('rm -f 2016APV_TT.root')
    os.system('rm -f 2016APV_DY.root')
    os.system(haddData_2016APV)
    os.system(haddTX_2016APV)
    os.system(haddVV_2016APV)
    os.system(haddTT_2016APV)
    os.system(haddDY_2016APV)

if (name == 'All') or (name == '2016'):
    haddData_2016 = 'hadd 2016_Data.root ' + ' '.join(addedFilesData['2016'])
    haddTX_2016 = 'hadd 2016_TX.root ' + ' '.join(addedFilesTX['2016'])
    haddVV_2016 = 'hadd 2016_VV.root ' + ' '.join(addedFilesVV['2016'])
    haddTT_2016 = 'hadd 2016_TT.root ' + ' '.join(addedFilesTT['2016'])
    haddDY_2016 = 'hadd 2016_DY.root ' + ' '.join(addedFilesDY['2016'])
    os.system('rm -f 2016_Data.root')
    os.system('rm -f 2016_TX.root')
    os.system('rm -f 2016_VV.root')
    os.system('rm -f 2016_TT.root')
    os.system('rm -f 2016_DY.root')
    os.system(haddData_2016)
    os.system(haddTX_2016)
    os.system(haddVV_2016)
    os.system(haddTT_2016)
    os.system(haddDY_2016)

if (name == 'All') or (name == '2017'):
    haddData_2017 = 'hadd 2017_Data.root ' + ' '.join(addedFilesData['2017'])
    haddTX_2017 = 'hadd 2017_TX.root ' + ' '.join(addedFilesTX['2017'])
    haddVV_2017 = 'hadd 2017_VV.root ' + ' '.join(addedFilesVV['2017'])
    haddTT_2017 = 'hadd 2017_TT.root ' + ' '.join(addedFilesTT['2017'])
    haddDY_2017 = 'hadd 2017_DY.root ' + ' '.join(addedFilesDY['2017'])
    os.system('rm -f 2017_Data.root')
    os.system('rm -f 2017_TX.root')
    os.system('rm -f 2017_VV.root')
    os.system('rm -f 2017_TT.root')
    os.system('rm -f 2017_DY.root')
    os.system(haddData_2017)
    os.system(haddTX_2017)
    os.system(haddVV_2017)
    os.system(haddTT_2017)
    os.system(haddDY_2017)

if (name == 'All') or (name == '2018'):
    haddData_2018 = 'hadd 2018_Data.root ' + ' '.join(addedFilesData['2018'])
    haddTX_2018 = 'hadd 2018_TX.root ' + ' '.join(addedFilesTX['2018'])
    haddVV_2018 = 'hadd 2018_VV.root ' + ' '.join(addedFilesVV['2018'])
    haddTT_2018 = 'hadd 2018_TT.root ' + ' '.join(addedFilesTT['2018'])
    haddDY_2018 = 'hadd 2018_DY.root ' + ' '.join(addedFilesDY['2018'])
    os.system('rm -f 2018_Data.root')
    os.system('rm -f 2018_TX.root')
    os.system('rm -f 2018_VV.root')
    os.system('rm -f 2018_TT.root')
    os.system('rm -f 2018_DY.root')
    os.system(haddData_2018)
    os.system(haddTX_2018)
    os.system(haddVV_2018)
    os.system(haddTT_2018)
    os.system(haddDY_2018)

if (name == 'All'):
    os.system('rm -f All_Data.root')
    os.system('rm -f All_TX.root')
    os.system('rm -f All_VV.root')
    os.system('rm -f All_TT.root')
    os.system('rm -f All_DY.root')
    os.system('rm -f All_LFVStScalarU.root')
    os.system('rm -f All_LFVTtScalarU.root')
    os.system('hadd All_Data.root *_Data.root')
    os.system('hadd All_TX.root *_TX.root')
    os.system('hadd All_VV.root *_VV.root')
    os.system('hadd All_TT.root *_TT.root')
    os.system('hadd All_DY.root *_DY.root')
    os.system('hadd All_LFVStScalarU.root *_LFVStScalarU.root')
    os.system('hadd All_LFVTtScalarU.root *_LFVTtScalarU.root')
