import sys
import os
import subprocess
import readline
import string
import argparse
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "bin"))
import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018


start = time.time()

# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--n", dest="NAMETAG", default="All")
ARGS = parser.parse_args()
name = ARGS.NAMETAG

SAMPLES = {}
if name == "All" or name == "2016APV":
    SAMPLES.update(nano_files_2016APV.mc2016APV_samples)
    SAMPLES.update(nano_files_2016APV.data2016APV_samples)
if name == "All" or name == "2016":
    SAMPLES.update(nano_files_2016.mc2016_samples)
    SAMPLES.update(nano_files_2016.data2016_samples)
if name == "All" or name == "2017":
    SAMPLES.update(nano_files_2017.mc2017_samples)
    SAMPLES.update(nano_files_2017.data2017_samples)
if name == "All" or name == "2018":
    SAMPLES.update(nano_files_2018.mc2018_samples)
    SAMPLES.update(nano_files_2018.data2018_samples)

addedFiles = {"2016APV": [], "2016": [], "2017": [], "2018": []}

for key, value in SAMPLES.items():
    year = value[3]
    addedFiles[year].append( year + '/' + key + '.root ')
    os.system("rm -f " + year + "/" + key + ".root ")
    nf = value[8]
    hadd = "hadd " + year + "/" + key + ".root "
    for idx, S in enumerate(value[0]):
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i + nf] for i in range(0, len(files), nf)]
            for num, seq in enumerate(sequance):
                hadd += year + "/" + key + "_" + str(idx) + "_" + str(num) + ".root "
            break
    os.system(hadd)

if (name == "All") or (name == "2016APV"):
    hadd_2016APV = "hadd 2016APV_Hists1D.root " + " ".join(addedFiles["2016APV"])
    os.system("rm -f 2016APV_Hists1D.root")
    os.system(hadd_2016APV)

if (name == "All") or (name == "2016"):
    hadd_2016 = "hadd 2016_Hists1D.root " + " ".join(addedFiles["2016"])
    os.system("rm -f 2016_Hists1D.root")
    os.system(hadd_2016)

if (name == "All") or (name == "2017"):
    hadd_2017 = "hadd 2017_Hists1D.root " + " ".join(addedFiles["2017"])
    os.system("rm -f 2017_Hists1D.root")
    os.system(hadd_2017)

if (name == "All") or (name == "2018"):
    hadd_2018 = "hadd 2018_Hists1D.root " + " ".join(addedFiles["2018"])
    os.system("rm -f 2018_Hists1D.root")
    os.system(hadd_2018)

if (name == "All"):
    os.system("rm -f All_Hists1D.root")
    os.system("hadd All_Hists1D.root *_Hists1D.root")

end = time.time()
print('Runtime was %.2f minutes.' % ((end - start)/60.0))
