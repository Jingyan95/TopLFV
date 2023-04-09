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

for key, value in SAMPLES.items():
    year = value[3]
    os.system('rm -f '+ key + '.root')
    nf = value[8]
    hadd='hadd ' + key + '.root '
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i+nf] for i in range(0,len(files),nf)]
            for num,  seq in enumerate(sequance):
                hadd +=  year + '/' + key +'_' + str(idx) +'_' + str(num) + '.root '
            break
    os.system(hadd)
    

    

