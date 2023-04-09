import sys
import os
import subprocess
import readline
import string
import csv, subprocess



import argparse
# set up an argument parser                                                                                                                                                                                        
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--n', dest = 'NAMETAG', default= '2016' )

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG
loc = os.path.dirname(sys.path[0])+'/'
dire = loc + 'hists/'

import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018

SAMPLES = {}
mc_2016APV = False
data_2016APV = False
mc_2016 = True
data_2016 = False
mc_2017 = False
data_2017 = False
mc_2018 = False
data_2018 = False

if mc_2016APV:
    SAMPLES.update(nano_files_2016APV.mc2016APV_samples)
if data_2016APV:
    SAMPLES.update(nano_files_2016APV.data2016APV_samples)
if mc_2016:
    SAMPLES.update(nano_files_2016.mc2016_samples)
if data_2016:
    SAMPLES.update(nano_files_2016.data2016_samples)
if mc_2017:
    SAMPLES.update(nano_files_2017.mc2017_samples)
if data_2017:
    SAMPLES.update(nano_files_2017.data2017_samples)
if mc_2018:
    SAMPLES.update(nano_files_2018.mc2018_samples)
if data_2018:
    SAMPLES.update(nano_files_2018.data2018_samples)

for key, value in SAMPLES.items():
    if name  not in key:
       continue
    year = value[3]
    nf = value[8]
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i+nf] for i in range(0,len(files),nf)]
            submit = 'universe = vanilla\n' ##writing .sub file
            submit += 'executable = Jobs/' + key + '/' + key + '_' + str(idx) + '.sh' + '\n'
            submit += 'arguments = $(Process)\n'
            submit += 'output = Jobs/'+ key + '/' + key + '_' + str(idx) + '_$(Process).out' + '\n'
            submit += 'error = Jobs/'+ key + '/' + key + '_' + str(idx) + '_$(Process).err' + '\n'
            submit += 'log = Jobs/'+ key + '/' + key + '_' + str(idx) + '_$(Process).log' + '\n'
            submit += '+JobFlavour = "espresso"\n' ##finish writing .sh file
            submit += 'queue '+str(len(sequance)) +'\n'
            submitName = key + '_' + str(idx) + '.sub'
            sub1 = open('Jobs/'+key+'/'+submitName,'wt')
            sub1.write(submit+'\n')
            sub1.close()
            subprocess.call('rm '+ dire + year + '/' + key +'_' + str(idx) + '_*.root', shell=True)
            qsub = "condor_submit Jobs/" + key + '/' + submitName 
            print qsub
            subprocess.call(qsub, shell=True)

