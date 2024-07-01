import sys
import os
import subprocess
import argparse
import time

import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018


start = time.time()

SAMPLES = {}
mc_2016APV = True
data_2016APV = True
mc_2016 = True
data_2016 = True
mc_2017 = True
data_2017 = True
mc_2018 = True
data_2018 = True
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

jobruntime = 21600 # 6 hrs

# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--n', dest='NAMETAG', default='201')
parser.add_argument('--t', dest='NCPUS', default=6) # Number of CPUs requested
ARGS = parser.parse_args()

loc = os.path.dirname(sys.path[0]) + '/'
dire = loc + 'hists/'

for key, value in SAMPLES.items():
    if ARGS.NAMETAG not in key:
        continue
    year = value[3]
    nf = value[8]
    nCPUS = ARGS.NCPUS
    if ('LFV' in key) or ('DYM10' in key) or ('WWW' in key) or ('WWZ' in key) or ('WZZ' in key) or ('ZZZ' in key):
        nCPUS = 1
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i + nf] for i in range(0, len(files), nf)]
            submit = 'universe = vanilla\n' # Writing .sub file
            submit += 'executable = Jobs/' + value[3] + '/' + key + '/' + key + '_' + str(idx) + '.sh\n'
            submit += 'arguments = $(Process)\n'
            submit += 'output = Jobs/' + value[3] + '/' + key + '/' + key + '_' + str(idx) + '_$(Process).out\n'
            submit += 'error = Jobs/' + value[3] + '/' + key + '/' + key + '_' + str(idx) + '_$(Process).err\n'
            submit += 'log = Jobs/' + value[3] + '/' + key + '/' + key + '_' + str(idx) + '_$(Process).log\n'
            submit += 'batch_name = ' + key + '\n'
            submit += 'request_cpus = ' + str(nCPUS) + '\n'
            submit += '+MaxRuntime = ' + str(jobruntime) + '\n' 
            submit += 'periodic_hold = (JobStatus == 2) && (time() - EnteredCurrentStatus) > ' + str(int(0.8 * jobruntime)) + '\n'
            submit += 'periodic_hold_reason = "Job is getting close to be terminated due to run time"\n'
            submit += 'periodic_hold_subcode = 42\n'
            submit += 'queue ' + str(len(sequance)) + '\n'
            submitName = key + '_' + str(idx) + '.sub'
            subprocess.call('rm -f Jobs/' + value[3] + '/' + key + '/*.out', shell=True)
            subprocess.call('rm -f Jobs/' + value[3] + '/' + key + '/*.err', shell=True)
            subprocess.call('rm -f Jobs/' + value[3] + '/' + key + '/*.log', shell=True)
            sub1 = open('Jobs/' + value[3] + '/' + key + '/' + submitName, 'wt')
            sub1.write(submit)
            sub1.close()
            qsub = "condor_submit Jobs/" + value[3] + '/' + key + '/' + submitName
            print("------------------------------------------------------")
            print(qsub)
            subprocess.call(qsub, shell=True)

end = time.time()
print('Runtime was %.2f minutes.' % ((end - start)/60.0))
