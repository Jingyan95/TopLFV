import os
import ROOT
import sys
dataset = {}

import gen_files_2016

mc_2016 = True

if mc_2016:
    dataset.update(gen_files_2016.mc2016_samples)

for key, value in dataset.items():
    print '-----------------------'
    print key
    nEvents = 0
    SumOfGenWeights = 0
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
            events = f.Get('nEvents')
            genweights = f.Get('nEventsGenWeighted')
            nFiles += 1
            nEvents += events.GetBinContent(1)
            SumOfGenWeights += genweights.GetBinContent(1)
            f.Close()
    print 'nEvents = %d'%(nEvents)
    print 'SumOfGenWeights = %d'%(SumOfGenWeights)
    print 'nFiles = %d'%(nFiles)
