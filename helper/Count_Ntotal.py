import os
import ROOT
import sys
dataset = {}

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'bin'))

import nano_files_2016APV
import nano_files_2016
import nano_files_2017
import nano_files_2018

mc_2016APV = False
data_2016APV = False
mc_2016 = True
data_2016 = False
mc_2017 = False
data_2017 = False
mc_2018 = False
data_2018 = False

if mc_2016APV:
    dataset.update(nano_files_2016APV.mc2016APV_samples)
if data_2016APV:
    dataset.update(nano_files_2016APV.data2016APV_samples)
if mc_2016:
    dataset.update(nano_files_2016.mc2016_samples)
if data_2016:
    dataset.update(nano_files_2016.data2016_samples)
if mc_2017:
    dataset.update(nano_files_2017.mc2017_samples)
if data_2017:
    dataset.update(nano_files_2017.data2017_samples)
if mc_2018:
    dataset.update(nano_files_2018.mc2018_samples)
if data_2018:
    dataset.update(nano_files_2018.data2018_samples)

for key, value in dataset.items():
    print('-----------------------')
    print(key)
    nEventsraw = 0
    nFiles = 0
    list = value[0]
    for a in list:
        filenames = os.listdir(a)
        for fname in filenames:
            filename = a + '/' + fname
            if 'fail' in fname:
                continue
            if 'log' in fname:
                continue
            f = ROOT.TFile.Open(filename)
            if not f:
                continue
            tree_events = f.Get('Events')
            nFiles += 1
            nEventsraw += tree_events.GetEntries()
            f.Close()
    print('nEventsraw = %d' % nEventsraw)
    print('nFiles = %d' % nFiles)
