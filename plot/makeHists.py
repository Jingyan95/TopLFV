import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetEndErrorSize(0)
from array import array
from ROOT import TColor
from ROOT import TGaxis
import gc
from operator import truediv
import copy
import argparse

year_RunII = ['2016APV', '2016', '2017', '2018']
year = []
channels = ["OS_ee", "OS_emu", "OS_mumu", "SS_ee", "SS_emu", "SS_mumu"]
nbins = [2, 6, 2, 2, 4, 2]
minbin = [1, 3, 9, 11, 13, 17]
regions = ["llOffZMetg20B1"]
vars = ["subSR"]
varsName = ["SR subdivided"]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest = 'VERBOSE', default = True)
parser.add_argument('--n', dest = 'NAMETAG', default = 'RunII')

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG

loc = os.path.dirname(sys.path[0]) + '/'
HistAddress = loc + 'hists/Combine/'

for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
        year.append(year_RunII[numyear])

Samples = ['Data.root', 'TX.root', 'VV.root', 'DY.root', 'TT.root', 'LFVemuScalarU.root', 'LFVetaScalarU.root', 'LFVmutaScalarU.root']
SamplesName = ["Data", "t#bar{t}X", "VV", "DY", "t#bar{t}", "C_{e#mutu}", "C_{e#mutu}", "C_{#mu#tautu}"]
SamplesNameStack = ["Data", "t#bar{t}+X", "VV(V)", "DY", "t#bar{t}", "CLFV e#mutu", "CLFV e#tautu", "CLFV #mu#tautu"]
SamplesNameCombine = ["data_obs_llOffZMetg20B1", "ttX_llOffZMetg20B1", "VV_llOffZMetg20B1", "DY_llOffZMetg20B1", "tt_llOffZMetg20B1", "emu_llOffZMetg20B1", "eta_llOffZMetg20B1", "muta_llOffZMetg20B1"]


Hists = []
for numyear, nameyear in enumerate(year):
    l0 = []
    Files = []
    for f in range(len(Samples)):
        l1 = []
        print (HistAddress + nameyear + '_' + Samples[f])
        Files.append(ROOT.TFile.Open(HistAddress + nameyear + '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2 = []
            for numreg, namereg in enumerate(regions):
                l3 = []
                for numvar, namevar in enumerate(vars):
                    h = Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)

HistsCombine = []
for numch, namech in enumerate(channels):
    template = ROOT.TH1F('tmp_'+namech, 'tmp', nbins[numch], 0, nbins[numch])
    l0 = []
    for numyear, nameyear in enumerate(year):
        l1 = []
        for f in range(len(Samples)):
            h = template.Clone()
            H = Hists[numyear][f][numch][0][0].Clone()
            for i in range(nbins[numch]):
                h.SetBinContent(i+1,H.GetBinContent(i+minbin[numch]))
                h.SetBinError(i+1,H.GetBinError(i+minbin[numch]))
            l1.append(h)
        l0.append(l1)
    HistsCombine.append(l0)

for numyear, nameyear in enumerate(year):
    fout = ROOT.TFile(nameyear+"_llOffZMetg20B1.root","recreate")
    for f in range(len(Samples)):
        for numch, namech in enumerate(channels):
            h = HistsCombine[numch][numyear][f].Clone()
            h.SetName(SamplesNameCombine[f]+'_'+namech)
            h.Write()
    fout.Close()
