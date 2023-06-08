import sys
import os
import subprocess
import readline
import string
import argparse
# set up an argument parser
parser = argparse.ArgumentParser()

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'bin'))
parser.add_argument('--n', dest = 'NAMETAG', default= '2016' )
ARGS = parser.parse_args()
name = ARGS.NAMETAG

import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018

SAMPLES = {}
if name == 'All' or name == '2016APV':
    SAMPLES.update(nano_files_2016APV.mc2016APV_samples)
    SAMPLES.update(nano_files_2016APV.data20APV_samples)
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
addedFilesTX = {"2016APV": [], "2016": [], "2017": [], "2018": []}
addedFilesVV = {"2016APV": [], "2016": [], "2017": [], "2018": []}
addedFilesTT = {"2016APV": [], "2016": [], "2017": [], "2018": []}
addedFilesDY = {"2016APV": [], "2016": [], "2017": [], "2018": []}

for key, value in SAMPLES.items():
    year = value[3]
    os.system('rm -f ' + year + '/' + key + '.root ')
    nf = value[8]
    hadd = 'hadd ' + year + '/' + key + '.root '
    if value[1] == 'data':
        addedFilesData[year].append(year + '/' + key + '.root ')
    elif ('TTW' in key) or ('TTH' in key) or ('TTZ' in key):
        addedFilesTX[year].append(year + '/' + key + '.root ')
    elif ('WW' in key) or ('WZ' in key) or ('ZZ' in key):
        addedFilesVV[year].append(year + '/' + key + '.root ')
    elif ('TTTo' in key):
        addedFilesTT[year].append(year + '/' + key + '.root ')
    elif ('DYM' in key):
        addedFilesDY[year].append(year + '/' + key + '.root ')
    else:
        os.system('rm -f ' + key + '.root')
        hadd = 'hadd ' + key + '.root '
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i + nf] for i in range(0, len(files), nf)]
            for num, seq in enumerate(sequance):
                hadd +=  year + '/' + key + '_' + str(idx) + '_' + str(num) + '.root '
            break
    os.system(hadd)

if (name == '2016'):
    haddData_2016 = 'hadd 2016_Data' + '.root ' + ' '.join(addedFilesData['2016'])
    haddTX_2016 = 'hadd 2016_TX' + '.root ' + ' '.join(addedFilesTX['2016'])
    haddVV_2016 = 'hadd 2016_VV' + '.root ' + ' '.join(addedFilesVV['2016'])
    haddTT_2016 = 'hadd 2016_TT' + '.root ' + ' '.join(addedFilesTT['2016'])
    haddDY_2016 = 'hadd 2016_DY' + '.root ' + ' '.join(addedFilesDY['2016'])
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
