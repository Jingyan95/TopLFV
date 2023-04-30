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
from plotter import StackHist,CompareBackgrounds,SummaryPlot
TGaxis.SetMaxDigits(2)
    
year_RunII=['2016APV','2016','2017','2018','All']
year=[]
charges=["OS","SS"];
channels=["ee","emu","mumu"];
regions=["ll","llOnZ","llOffZ","llOffZMetg20Jetgeq1","llOffZMetg20B1","llOffZMetg20B2"]
regionsName=[["No cuts","",""],["OnZ","",", Z+jets CR"],["OffZ","",""],["OffZ, p_{T}^{miss}>20GeV","njet#geq1",", SR(Loose)"],["OffZ, p_{T}^{miss}>20GeV","nbjet=1",", SR(Tight)"],["OffZ, p_{T}^{miss}>20GeV","nbjet=2",", t#bar{t}+jets CR"]]
vars=["elMVAv1Prompt","elMVAv1HF","elMVAv1Other","elMVAv2Prompt","elMVAv2HF","elMVAv2Other","elMVAv3Prompt","elMVAv3HF","elMVAv3Other",
      "muMVAv1Prompt","muMVAv1HF","muMVAv1Other","muMVAv2Prompt","muMVAv2HF","muMVAv2Other","muMVAv3Prompt","muMVAv3HF","muMVAv3Other",
      "taMVAv1Had","taMVAv1Fake","taMVAv1Other","taMVAv2Had","taMVAv2Fake","taMVAv2Other","taMVAv3Had","taMVAv3Fake","taMVAv3Other",
      "llM","llDr","lep1Pt","lep2Pt","taPt","jet1Pt","njet","nbjet","MET","subSR","LFVemuM","LFVetaM","LFVmutaM",
      "LFVemuDr","LFVetaDr","LFVmutaDr","LFVePt","LFVmuPt","LFVtaPt","BalepPt","Topmass"]

varsName=["Prompt electron MVA v1","HF electron MVA v1","Other electron MVA v1",
          "Prompt electron MVA v2","HF electron MVA v2","Other electron MVA v2",
          "Prompt electron MVA v3","HF electron MVA v3","Other electron MVA v3",
          "Prompt muon MVA v1","HF muon MVA v1","Other muon MVA v1",
          "Prompt muon MVA v2","HF muon MVA v2","Other muon MVA v2",
          "Prompt muon MVA v3","HF muon MVA v3","Other muon MVA v3",
          "Hadronic tau MVA v1","Fake tau MVA v1","Other tau MVA v1",
          "Hadronic tau MVA v2","Fake tau MVA v2","Other tau MVA v2",
          "Hadronic tau MVA v3","Fake tau MVA v3","Other tau MVA v3",
          "m(l#bar{l}) [GeV]","#DeltaR(l#bar{l})","Leading lepton p_{T} [GeV]",
          "Sub-leading lepton p_{T} [GeV]","Tau p_{T} [GeV]",
          "Leading jet p_{T} [GeV]", "njet", "nbjet (Loose WP)","MET [GeV]","SR subdivided",
          "m(e#bar{#mu}) [GeV]", "m(e#bar{#tau}) [GeV]", "m(#mu#bar{#tau}) [GeV]",
          "#DeltaR(e,#bar{#mu}) [GeV]", "#DeltaR(e,#bar{#tau}) [GeV]", "#DeltaR(#mu,#bar{#tau}) [GeV]",
          "LFV electron p_{T} [GeV]", "LFV muon p_{T} [GeV]", "LFV tau p_{T} [GeV]",
          "Bachelor lepton p_{T} [GeV]", "m(top) [GeV]"]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--n', dest = 'NAMETAG', default= '2016' )

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG

loc = os.path.dirname(sys.path[0])+'/'
HistAddress = loc + 'hists/'

for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
       year.append(year_RunII[numyear])
       
Samples = ['Data.root', 'TX.root', 'VV.root', 'DY.root', 'TT.root', 'LFVStScalarU.root', 'LFVTtScalarU.root']
SamplesName = ["Data", "t#bar{t}X", "VV", "DY", "t#bar{t}", "C_{ll`tu}^{ST}", "C_{ll`tu}^{TT}"]
SamplesNameStack = ["Data", "t#bar{t}+X", "VV(V)", "DY", "t#bar{t}", "CLFV top production", "CLFV top decay"]

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kOrange-3,ROOT.kRed-4,ROOT.kViolet+1,ROOT.kGray]
markerStyle =  [20,25,26,27,28,29,30]

SaveMVA = False

Hists = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        print HistAddress + nameyear+ '_' + Samples[f]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numc, namec in enumerate(charges):
            l2=[]
            for numch, namech in enumerate(channels):
                l3=[]
                for numreg, namereg in enumerate(regions):
                    l4=[]
                    for numvar, namevar in enumerate(vars):
                        h = Files[f].Get(namec + '_' + namech + '_' + namereg + '_' + namevar)
                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
                        if ('SS' in namec) and ('B2' in namereg or 'OnZ' in namereg):
                           h.Reset("ICE")
                        l4.append(h)
                    l3.append(l4)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)
                       
#Make histograms
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(vars):
                    if ('MVA' in namevar) and (not SaveMVA):
                        continue
                    H1 = []
                    H1Signal = []
                    H2 = []
                    for f in range(len(Samples)):
                        h1 = Hists[numyear][f][numc][numch][numreg][numvar].Clone()
                        h1.SetFillColor(colors[f])
                        if 'LFV' not in Samples[f]:
                            h1.SetLineColor(colors[0])
                            H1.append(h1)
                        else:
                            h1.SetLineColor(colors[f])
                            H1Signal.append(h1)
                        if 'Data' in Samples[f]:
                            continue
                        h2 = Hists[numyear][f][numc][numch][numreg][numvar].Clone()
                        h2.SetLineColor(colors[f])
                        h2.SetLineWidth(2)
                        h2.SetMarkerColor(colors[f])
                        h2.SetMarkerStyle(markerStyle[f])
                        H2.append(h2)
                    StackHist(H1, H1Signal, SamplesNameStack, namec, namech, namereg, regionsName[numreg], nameyear, namevar,varsName[numvar])
                    #CompareBackgrounds(H2, nameyear, namec, namech, namereg, namevar, varsName[numvar], SamplesName)

for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        H = []
        HSignal = []
        for f in range(len(Samples)):
            h = Hists[numyear][f][0][0][numreg][36].Clone()
            h.Reset("ICE")
            for numc, namec in enumerate(charges):
                for numch, namech in enumerate(channels):
                    h+=Hists[numyear][f][numc][numch][numreg][36]
            h.SetFillColor(colors[f])
            if 'LFV' not in Samples[f]:
                h.SetLineColor(colors[0])
                H.append(h)
            else:
                h.SetLineColor(colors[f])
                HSignal.append(h)
        SummaryPlot(H, HSignal, SamplesNameStack, namereg, regionsName[numreg], nameyear)
        