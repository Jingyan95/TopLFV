import sys
import os
import subprocess
import readline
import string
import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018


import argparse
# set up an argument parser                                                                                                                                                                         
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--n', dest = 'NAMETAG', default= '2016' )

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG
loc = os.path.dirname(sys.path[0])+'/'


SAMPLES = {}
mc_2016APV = False
data_2016APV = False
mc_2016 = True
data_2016 = True
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

rootlib1 = subprocess.check_output("root-config --cflags", shell=True)
rootlib11="".join([s for s in rootlib1.strip().splitlines(True) if s.strip()])
rootlib2 = subprocess.check_output("root-config --libs", shell=True)
rootlib22="".join([s for s in rootlib2.strip().splitlines(True) if s.strip()])

cms = '/afs/cern.ch/work/j/jingyan/public/CMSSW_10_6_4/src/'
dire = loc+'bin'
dire_h = loc+'hists/'

for key, value in SAMPLES.items():
#########################################
    if name  not in key:
       continue
    nf = value[8]
    if not os.path.exists('Jobs/'+key):
       os.makedirs('Jobs/'+key)
    for idx, S in enumerate(value[0]):
        SHNAME = key +'_' + str(idx) +'.sh'
        SHNAME1 = key +'_' + str(idx) +'_$1.C'
        SHFILE="#!/bin/bash\n" +\
        "cd "+ cms + "\n"+\
        "eval `scramv1 runtime -sh`\n"+\
        "cd "+ dire + "\n"+\
        'g++ -fPIC -fno-var-tracking -Wno-deprecated -D_GNU_SOURCE -O2  -I./../include   '+ rootlib11 +' -ldl  -o ' + SHNAME1.split('.')[0] + ' Jobs/' + key + '/' + SHNAME1+ ' ../lib/main.so ' + rootlib22 + '  -lMinuit -lTreePlayer' + "\n"+\
        "./" + SHNAME1.split('.')[0] + "\n"+\
        'FILE='+ dire_h + value[3] + '/' + key +'_' + str(idx) +'_$1.root'+ "\n"+\
        'if [ -f "$FILE" ]; then'+ "\n"+\
        '    rm  ' + SHNAME1.split('.')[0] + "\n"+\
        'fi'
        #os.system("writing .sh file")
        subprocess.call('rm -f Jobs/'+key+'/*', shell=True)
        open('Jobs/'+key+'/'+SHNAME, 'wt').write(SHFILE)
        print "-----------------------------------"
        print 'Writing Jobs/'+key+'/'+SHNAME
        os.system("chmod +x "+'Jobs/'+key+'/'+SHNAME)
        print "chmod +x "+'Jobs/'+key+'/'+SHNAME
        #delete log files
        os.system("rm -rf "+ S +'log')
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i+nf] for i in range(0,len(files),nf)]
            #print value[0]
            #print sequance
            for num,  seq in enumerate(sequance):
                text = ''
                text += '    TChain* ch    = new TChain("Events") ;\n'
                for filename in seq:
                    text += '    ch ->Add("' + S+ filename + '");\n'
                text += '    MyAnalysis t1(ch, "' + value[3] + '" , "'+ value[1] + '" , "' + value[4] + '", false);\n'
                text += '    t1.Loop("'+dire_h+ value[3] + '/' + key +'_' + str(idx) +'_' +str(num)  + '.root", "' + value[1] + '" , "'+ value[2] + '" , "'+ value[3] + '" , "'+ value[4] + '" , ' + value[5] + ' , '+ value[6] + ' , '+ value[7] + ');\n'
                SHNAME1 = key +'_' + str(idx) +'_' +str(num) + '.C'
                SHFILE1='#include "MyAnalysis.h"\n' +\
                'int main(){\n' +\
                text +\
                'return 0;' +\
                '}'
                open('Jobs/'+key+'/'+SHNAME1, 'wt').write(SHFILE1)
    if verbose : 
        print key + ' jobs are made'
   


