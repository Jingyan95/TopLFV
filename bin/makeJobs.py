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

# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--n', dest='NAMETAG', default='201')
parser.add_argument('--t', dest='NTHREAD', default=6) # Number of threads
ARGS = parser.parse_args()

rootlib1 = subprocess.check_output("root-config --cflags", shell=True)
rootlib11 = "".join([str(s, encoding='utf-8') for s in rootlib1.strip().splitlines(True) if s.strip()])
rootlib2 = subprocess.check_output("root-config --libs", shell=True)
rootlib22 = "".join([str(s, encoding='utf-8') for s in rootlib2.strip().splitlines(True) if s.strip()])

loc = os.path.dirname(sys.path[0]) + '/'
dire_h = loc + 'hists/'

for key, value in SAMPLES.items():
    if ARGS.NAMETAG not in key:
        continue
    nf = value[8]
    if not os.path.exists('Jobs/' + value[3] + '/' + key):
        os.makedirs('Jobs/' + value[3] + '/' + key)
    nThread = ARGS.NTHREAD
    if ('LFV' in key) or ('DYM10' in key) or ('WWW' in key) or ('WWZ' in key) or ('WZZ' in key) or ('ZZZ' in key):
        nThread = 1 # Samples with low stats
    for idx, S in enumerate(value[0]):
        SHNAME = key + '_' + str(idx) + '.sh'
        SHNAME1 = key + '_' + str(idx) + '_$1.C'
        SHFILE = "#!/bin/bash\n" +\
        'FILE=' + dire_h + value[3] + '/' + key + '_' + str(idx) + '_$1.root' + '\n' +\
        'source /cvmfs/sft.cern.ch/lcg/views/LCG_104c/x86_64-el9-gcc13-opt/setup.sh\n' +\
        'cd ' + loc + '\n' +\
        'g++ -fPIC -fno-var-tracking -Wno-deprecated -D_GNU_SOURCE -O2 -I./include ' + rootlib11 + ' -ldl -o ' + SHNAME1.split('.')[0] + ' bin/Jobs/' + value[3] + '/' + key + '/' + SHNAME1 + ' lib/main.so ' + rootlib22 + ' -lMinuit -lTreePlayer' + '\n' +\
        './' + SHNAME1.split('.')[0] + '\n' +\
        'if [ -f "$FILE" ]; then' + '\n' +\
        '    rm -f ' + SHNAME1.split('.')[0] + '\n' +\
        'fi\n'
        subprocess.call('rm -f Jobs/' + value[3] + '/' + key + '/*', shell=True)
        open('Jobs/' + value[3] + '/' + key + '/' + SHNAME, 'wt').write(SHFILE)
        print("-----------------------------------")
        print('Writing Jobs/' + value[3] + '/' + key + '/' + SHNAME)
        os.system('chmod +x ' + 'Jobs/' + value[3] + '/' + key + '/' + SHNAME)
        print('chmod +x ' + 'Jobs/' + value[3] + '/' + key + '/' + SHNAME)
        # Delete log files
        os.system('rm -rf ' + S + 'log')
        for subdir, dirs, files in os.walk(S):
            sequence = [files[i:i + nf] for i in range(0, len(files), nf)]
            for num, seq in enumerate(sequence):
                text = ''
                text += '    system("rm -f ' + dire_h + value[3] + '/' + key + '_' + str(idx) + '_' + str(num) + '*.root");\n'
                text += '    ROOT::EnableThreadSafety();\n'
                text += '    UInt_t nThread = ' + str(nThread) + ';\n'
                text += '    std::stringstream Summary;\n'
                text += '    Summary<<"\\nNumber of threads requested "<<nThread<<".\\n";\n'
                text += '    auto workerIDs = ROOT::TSeqI(nThread);\n'
                text += '    std::atomic<ULong64_t> progress(0);\n'
                text += '    std::atomic<ULong64_t> counter(0);\n'
                text += '    auto workItem = [&](UInt_t workerID) {\n'
                text += '        TChain* ch = new TChain("Events") ;\n'
                for filename in seq:
                    text += '        ch ->Add("' + S + filename + '");\n'
                text += '        MyAnalysis t1(ch, "' + value[3] + '" , "' + value[1] + '" , "' + value[4] + '", nThread, workerID, false);\n'
                text += '        auto workerSummary = t1.Loop(Form("' + dire_h + value[3] + '/' + key + '_' + str(idx) + '_' + str(num) + '_%u.root",workerID), "' + value[1] + '" , "' + value[2] + '" , "' + value[3] + '" , "' + value[4] + '" , ' + value[5] + ' , '+ value[6] + ' , ' + value[7] + ', std::ref(progress), std::ref(counter));\n'
                text += '        Summary<<workerSummary.str();\n'
                text += '    };\n'
                text += '    std::vector<std::thread> workers;\n'
                text += '    for (auto workerID : workerIDs) {\n'
                text += '        workers.emplace_back(workItem, workerID);\n'
                text += '    }\n'
                text += '    for (auto&& worker : workers) worker.join();\n'
                text += '    std::cout<<Summary.str();\n'
                text += '    system("hadd ' + dire_h + value[3] + '/' + key + '_' + str(idx) + '_' + str(num) + '.root ' + dire_h + value[3] + '/' + key + '_' + str(idx) + '_' + str(num) + '_*.root");\n'
                text += '    system("rm -f ' + dire_h + value[3] + '/' + key + '_' + str(idx) + '_' + str(num) + '_*.root");\n'
                SHNAME1 = key + '_' + str(idx) + '_' + str(num) + '.C'
                SHFILE1 = '#include "MyAnalysis.h"\n' +\
                '#include "ROOT/TSeq.hxx"\n' +\
                '#include <thread>\n' +\
                '#include <atomic>\n\n' +\
                'std::mutex MyAnalysis::mtx_;\n\n' +\
                'int main(){\n' +\
                text +\
                '    return 0;\n' +\
                '}\n'
                open('Jobs/' + value[3] + '/' + key + '/' + SHNAME1, 'wt').write(SHFILE1)
    if ARGS.VERBOSE:
        print(key + ' jobs are made')

end = time.time()
print('Runtime was %.2f seconds.' % (end - start))
