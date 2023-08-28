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
from plotter import CompareEff, PlotSF
TGaxis.SetMaxDigits(2)

year_RunII = ['2016APV', '2016', '2017', '2018']
year = []
charges = ["OS", "SS"]
channels = ["ee", "emu", "mue", "mumu"]
passes = ["All", "Pass"]

vars = ["lep1Pt", "lep2Pt", "lep1Eta", "lep2Eta"]
varsName = ["Leading lepton p_{T} [GeV]", "Sub-leading lepton p_{T} [GeV]",
            "Leading lepton #eta", "Sub-leading lepton #eta"]
varsD2 = ["lepPt", "lepEta"]
varsD2Name = [["Leading lepton p_{T} [GeV]", "Sub-leading lepton p_{T} [GeV]"],
            ["Leading lepton #eta", "Sub-leading lepton #eta"]]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest = 'VERBOSE', default = True)
parser.add_argument('--n', dest = 'NAMETAG', default = 'RunII')

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG

loc = os.path.dirname(sys.path[0]) + '/'
HistAddress = loc + 'hists/'

for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
        year.append(year_RunII[numyear])

Samples = ['Data.root', 'TTTo2L2Nu.root', 'TTW.root']
SamplesName = ["Data", "MC"]

colors = [ROOT.kBlack,ROOT.kRed,ROOT.kRed]
markerStyle = [20, 25, 25]

Hists = []
HistsD2 = []
for numyear, nameyear in enumerate(year):
    l0 = []
    l0D2 = []
    Files = []
    for f in range(len(Samples)):
        l1 = []
        l1D2 = []
        print (HistAddress + nameyear + '_' + Samples[f])
        Files.append(ROOT.TFile.Open(HistAddress + nameyear + '_' + Samples[f]))
        for numc, namec in enumerate(charges):
            l2 = []
            l2D2 = []
            for numch, namech in enumerate(channels):
                l3 = []
                l3D2 = []
                for nump, namep in enumerate(passes):
                    l4 = []
                    l4D2 = []
                    for numvar, namevar in enumerate(vars):
                        h = Files[f].Get(namec + '_' + namech + '_' + namep + '_' + namevar)
                        l4.append(h)
                    for numvarD2, namevarD2 in enumerate(varsD2):
                        h2 = Files[f].Get(namec + '_' + namech + '_' + namep + '_' + namevarD2)
                        l4D2.append(h2)
                    l3.append(l4)
                    l3D2.append(l4D2)
                l2.append(l3)
                l2D2.append(l3D2)
            l1.append(l2)
            l1D2.append(l2D2)
        l0.append(l1)
        l0D2.append(l1D2)
    Hists.append(l0)
    HistsD2.append(l0D2)

# Make histograms
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numvar, namevar in enumerate(vars):
                H1 = []
                for f in range(len(Samples)):
                    if (numc==0 and f==2):
                        continue 
                    if (numc==1 and f==1):
                        continue
                    h1 = Hists[numyear][f][numc][numch][1][numvar].Clone()
                    h1.SetLineColor(colors[f])
                    h1.SetLineWidth(2)
                    h1.SetMarkerColor(colors[f])
                    h1.SetMarkerStyle(markerStyle[f])
                    h1.Divide(Hists[numyear][f][numc][numch][0][numvar])
                    H1.append(h1)
                CompareEff(H1, SamplesName, namec, namech, nameyear, namevar, varsName[numvar])

for numyear, nameyear in enumerate(year):
    fileout = ROOT.TFile(nameyear + 'TriggerSF.root','recreate')
    for numch, namech in enumerate(channels):
        hData = HistsD2[numyear][0][0][numch][1][0].Clone()
        hData.Divide(HistsD2[numyear][0][0][numch][0][0])
        hMC = HistsD2[numyear][1][0][numch][1][0].Clone()
        hMC.Divide(HistsD2[numyear][1][0][numch][0][0])
        hSF = hData.Clone()
        hSF.Divide(hMC)
        hSF.SetName(namech)
        hSF.Write()
        PlotSF(hSF, namech, nameyear, varsD2Name[0])
    fileout.Close()

