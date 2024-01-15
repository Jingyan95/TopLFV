import os
import ROOT
import sys
dataset = {}

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'bin'))

import nano_files_2016APV_dilepton
import nano_files_2016_dilepton
import nano_files_2017_dilepton
import nano_files_2018_dilepton

mc_2016APV = True
data_2016APV = True
mc_2016 = True
data_2016 = True
mc_2017 = True
data_2017 = True
mc_2018 = True
data_2018 = True

if mc_2016APV:
    dataset.update(nano_files_2016APV_dilepton.mc2016APV_samples)
if data_2016APV:
    dataset.update(nano_files_2016APV_dilepton.data2016APV_samples)
if mc_2016:
    dataset.update(nano_files_2016_dilepton.mc2016_samples)
if data_2016:
    dataset.update(nano_files_2016_dilepton.data2016_samples)
if mc_2017:
    dataset.update(nano_files_2017_dilepton.mc2017_samples)
if data_2017:
    dataset.update(nano_files_2017_dilepton.data2017_samples)
if mc_2018:
    dataset.update(nano_files_2018_dilepton.mc2018_samples)
if data_2018:
    dataset.update(nano_files_2018_dilepton.data2018_samples)

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
