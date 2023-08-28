import sys
import os
import subprocess
import readline
import string
import argparse
# set up an argument parser
parser = argparse.ArgumentParser()

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'bin'))
parser.add_argument('--n', dest = 'NAMETAG', default= 'All' )
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

for key, value in SAMPLES.items():
    year = value[3]
    os.system('rm -f '+ year + '/' +key + '.root ')
    nf = value[8]
    hadd='hadd ' + year + '/' + key + '.root '
    if value[1]=='data':
        addedFilesData[year].append( year + '/' + key + '.root ')
    else:
        os.system('rm -f ' + key + '.root')
        hadd='hadd ' + key + '.root '
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i+nf] for i in range(0,len(files),nf)]
            for num,  seq in enumerate(sequance):
                hadd +=  year + '/' + key +'_' + str(idx) +'_' + str(num) + '.root '
            break
    os.system(hadd)

if (name == 'All') or (name == '2016APV'):
    haddData_2016APV ='hadd 2016APV_Data' + '.root ' + ' '.join(addedFilesData['2016APV'])
    os.system('rm -f 2016APV_Data.root')
    os.system(haddData_2016APV)

if (name == 'All') or (name == '2016'):
    haddData_2016 ='hadd 2016_Data' + '.root ' + ' '.join(addedFilesData['2016'])
    os.system('rm -f 2016_Data.root')
    os.system(haddData_2016)

if (name == 'All') or (name == '2017'):
    haddData_2017 ='hadd 2017_Data' + '.root ' + ' '.join(addedFilesData['2017'])
    os.system('rm -f 2017_Data.root')
    os.system(haddData_2017)

if (name == 'All') or (name == '2018'):
    haddData_2018 ='hadd 2018_Data' + '.root ' + ' '.join(addedFilesData['2018'])
    os.system('rm -f 2018_Data.root')
    os.system(haddData_2018)

