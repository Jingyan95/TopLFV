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
from plotter import StackHist, Hist2D, CompareBackgrounds, SummaryPlot, SimplePlot
TGaxis.SetMaxDigits(2)

year_RunII = ['2016APV', '2016', '2017', '2018', 'All']
year = []
charges = ["OS", "SS"]
channels = ["ee", "emu", "mumu"]

regions = ["ll",
    "llOnZMetg20Jetgeq1",
    "llOffZMetg20B1",
    "llOffZMetg20B2",
    "llStl300",
    "llOnZ",
    "llbtagg1p3",
    "llStg300OffZbtagl1p3",
    "llStg300OffZbtagl1p3Tight",
    "llMetg20Jetgeq1"]
    # "llOnZMetg20Jetgeq1Loose",
    # "llOffZMetg20B1Loose",
    # "llOffZMetg20B2Loose"]
regionsName = [["No cuts", "", ""],
    ["p_{T}^{miss}>20GeV, njet#geq1", "OnZ", ", Z+jets CR"],
    ["p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1", ", SR"],
    ["p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2", ", t#bar{t}+jets CR"],
    ["S_{T}<300GeV", "", ", CR"],
    ["OnZ", "", ", Z+jets CR"],
    ["btag>1.3", "", ", t#bar{t}+jets CR"],
    ["S_{T}>300GeV, OffZ", "btag<1.3", ", SR(Alt, Loose)"],
    ["S_{T}>300GeV, OffZ", "btag<1.3, njet#geq1 or S_{T}>500GeV", ", SR(Alt, Tight)"],
    ["p_{T}^{miss}>20GeV, njet#geq1", "Background", "Estimation"]]
    # ["p_{T}^{miss}>20GeV, njet#geq1", "OnZ", ", Z+jets CR (Loose)"],
    # ["p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1", ", SR (Loose)"],
    # ["p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2", ", t#bar{t}+jets CR (Loose)"]]

vars = ["llM", "llDr", "lep1Pt", "lep2Pt",
    "taPt", "taPtHadronic", "taEta", "taEtaHadronic", "taVsJetWP", "taDxy", "taDz",
    "jet1Pt", "njet", "nbjet", "MET", "subSR", "LFVemuM", "LFVetaM", "LFVmutaM",
    "LFVemuDr", "LFVetaDr", "LFVmutaDr", "LFVePt", "LFVmuPt", "LFVtaPt", "BalepPt",
    "Topmass", "Ht", "St", "btagSum"]
varsName = ["m(l#bar{l}) [GeV]", "#DeltaR(l#bar{l})",
    "Leading lepton p_{T} [GeV]", "Sub-leading lepton p_{T} [GeV]",
    "#tau p_{T} [GeV]", "#tau_{h} p_{T} [GeV]", "#tau #eta", "#tau_{h} #eta",
    "#tau vs Jets WP", "#tau d_{xy} [cm]", "#tau d_{z} [cm]",
    "Leading jet p_{T} [GeV]", "njet", "nbjet (Loose WP)", "MET [GeV]", "SR subdivided",
    "m(e#bar{#mu}) [GeV]", "m(e#bar{#tau}) [GeV]", "m(#mu#bar{#tau}) [GeV]",
    "#DeltaR(e,#bar{#mu}) [GeV]", "#DeltaR(e,#bar{#tau}) [GeV]", "#DeltaR(#mu,#bar{#tau}) [GeV]",
    "LFV electron p_{T} [GeV]", "LFV muon p_{T} [GeV]", "LFV tau p_{T} [GeV]",
    "Bachelor lepton p_{T} [GeV]", "m(top) [GeV]", "H_{T} [GeV]", "S_{T} [GeV]", "Sum of btagging scores"]

vars2D = ["nbjetvsOnZ", "nbjetvsOnZHadronic"]
vars2DName = [["All Events", "nbjet (Loose WP)"], ["Events with #tau_{h}", "#tau_{h} p_{T} [GeV]"]]
vars2DBinLabels = [[["On Z", "Off Z"], ["0", "1", "2", "3"]], [["On Z", "Off Z"], ["0", "1", "2", "3"]]]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest = 'VERBOSE', default = True)
parser.add_argument('--n', dest = 'NAMETAG', default = '2016')

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG

loc = os.path.dirname(sys.path[0]) + '/'
HistAddress = loc + 'hists/'

for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
        year.append(year_RunII[numyear])

Samples = ['Data.root', 'TX.root', 'VV.root', 'DY.root', 'TT.root', 'LFVStScalarU.root', 'LFVTtScalarU.root']
SamplesName = ["Data", "t#bar{t}X", "VV", "DY", "t#bar{t}", "C_{ll`tu}^{ST}", "C_{ll`tu}^{TT}"]
SamplesNameStack = ["Data", "t#bar{t}+X", "VV(V)", "DY", "t#bar{t}", "CLFV top production", "CLFV top decay"]

colors = [ROOT.kBlack, ROOT.kYellow, ROOT.kGreen, ROOT.kOrange - 3, ROOT.kRed - 4, ROOT.kViolet + 1, ROOT.kGray]
markerStyle = [20, 25, 26, 27, 28, 29, 30]

SaveMVA = False

# Read in histograms
Hists = []
Hists2D = []
min2D = 1e-4
max2D = -1.0
for numyear, nameyear in enumerate(year):
    l0 = []
    l0_2D = []
    Files = []
    for f in range(len(Samples)):
        l1 = []
        l1_2D = []
        print(HistAddress + nameyear + '_' + Samples[f])
        Files.append(ROOT.TFile.Open(HistAddress + nameyear + '_' + Samples[f]))
        for numc, namec in enumerate(charges):
            l2 = []
            l2_2D = []
            for numch, namech in enumerate(channels):
                l3 = []
                l3_2D = []
                for numreg, namereg in enumerate(regions):
                    l4 = []
                    l4_2D = []

                    for numvar, namevar in enumerate(vars):
                        h = Files[f].Get(namec + '_' + namech + '_' + namereg + '_' + namevar)
                        # Take care of underflow/overflow
                        h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins() + 1))
                        # No CR in SS channels
                        if ('SS' in namec) and ('B2' in namereg or 'OnZ' in namereg or 'Stl300' in namereg or 'btagg1p3' in namereg):
                            h.Reset("ICE")
                        l4.append(h)

                    for numvar, namevar in enumerate(vars2D):
                        h_2D = Files[f].Get(namec + '_' + namech + '_' + namereg + '_' + namevar)
                        # Take care of underflow/overflow
                        for xBin in range(1, h_2D.GetXaxis().GetNbins() + 1):
                            h_2D.SetBinContent(xBin, 1, h_2D.GetBinContent(xBin, 0) + h_2D.GetBinContent(xBin, 1))
                            h_2D.SetBinContent(xBin, h.GetYaxis().GetNbins(), h_2D.GetBinContent(xBin, h.GetYaxis().GetNbins()) + h_2D.GetBinContent(xBin, h.GetYaxis().GetNbins() + 1))
                        for yBin in range(1, h_2D.GetYaxis().GetNbins() + 1):
                            h_2D.SetBinContent(1, yBin, h_2D.GetBinContent(0, yBin) + h_2D.GetBinContent(1, yBin))
                            h_2D.SetBinContent(h.GetXaxis().GetNbins(), yBin, h_2D.GetBinContent(h.GetXaxis().GetNbins(), yBin) + h_2D.GetBinContent(h.GetXaxis().GetNbins() + 1, yBin))
                        if h_2D.GetMinimum(0.0) < min2D:
                            print(nameyear, namec, namech, namereg, namevar, h_2D.GetMinimum(0.0))
                        # Set 0 values to minimum
                        for xBin in range(1, h_2D.GetXaxis().GetNbins() + 1):
                            for yBin in range(1, h_2D.GetYaxis().GetNbins() + 1):
                                if h_2D.GetBinContent(xBin, yBin) < min2D:
                                    h_2D.SetBinContent(xBin, yBin, min2D)
                        # Get max histogram value
                        if h_2D.GetMaximum() > max2D:
                            max2D = h_2D.GetMaximum()
                        # No CR in SS channels
                        if ('SS' in namec) and ('B2' in namereg or 'OnZ' in namereg or 'Stl300' in namereg or 'btagg1p3' in namereg):
                            h_2D.Reset("ICE")
                        l4_2D.append(h_2D)

                    l3.append(l4)
                    l3_2D.append(l4_2D)
                l2.append(l3)
                l2_2D.append(l3_2D)
            l1.append(l2)
            l1_2D.append(l2_2D)
        l0.append(l1)
        l0_2D.append(l1_2D)
    Hists.append(l0)
    Hists2D.append(l0_2D)

# Make histograms
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
                    StackHist(H1, H1Signal, SamplesNameStack, namec, namech, namereg, regionsName[numreg], nameyear, namevar, varsName[numvar])
                    # CompareBackgrounds(H2, nameyear, namec, namech, namereg, namevar, varsName[numvar], SamplesName)

# Summary histograms
for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        H = []
        HSignal = []
        for f in range(len(Samples)):
            h = Hists[numyear][f][0][0][numreg][15].Clone()
            h.Reset("ICE")
            for numc, namec in enumerate(charges):
                for numch, namech in enumerate(channels):
                    h += Hists[numyear][f][numc][numch][numreg][15]
            h.SetFillColor(colors[f])
            if 'LFV' not in Samples[f]:
                h.SetLineColor(colors[0])
                H.append(h)
            else:
                h.SetLineColor(colors[f])
                HSignal.append(h)
        SummaryPlot(H, HSignal, SamplesNameStack, namereg, regionsName[numreg], nameyear)

# Fake tau background estimation
min2D = 1
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):

                for f in range(len(Samples)):
                    for numvar, namevar in enumerate(vars2D):
                        h2D = Hists2D[numyear][f][numc][numch][numreg][numvar].Clone()
                        Hist2D(h2D, Samples[f], namec, namech, namereg, regionsName[numreg], nameyear, min2D, max2D,
                            vars2D[numvar], vars2DName[numvar][0], vars2DName[numvar][1],
                            [], [], vars2DBinLabels[numvar][0], vars2DBinLabels[numvar][1])

                for numvar in range(0, len(vars2D), 2):
                    dataH2 = Hists2D[numyear][0][numc][numch][numreg][numvar].Clone() # Get data
                    for f in range(1, len(Samples)):
                        mcH2 = Hists2D[numyear][f][numc][numch][numreg][numvar + 1].Clone() # Subtract hadronic taus
                        dataH2.Add(mcH2, -1.0)
                    for xBin in range(1, dataH2.GetXaxis().GetNbins() + 1): # Set 0 values to minimum
                        for yBin in range(1, dataH2.GetYaxis().GetNbins() + 1):
                            if dataH2.GetBinContent(xBin, yBin) < min2D:
                                dataH2.SetBinContent(xBin, yBin, min2D)
                    Hist2D(dataH2, "All.....", namec, namech, namereg, regionsName[numreg], nameyear, min2D, max2D,
                        vars2D[numvar], vars2DName[0][0], vars2DName[0][1],
                        [1], [0, 0.2, 0.4, 0.6, 0.8, 1, 2, 3], vars2DBinLabels[numvar][0], vars2DBinLabels[numvar][1])

                    if 'OS' in namec:
                        if 'llMetg20Jetgeq1' in namereg:
                            if 'emu' not in namech:
                                print('---------------------------------------')
                                print(nameyear, namec, namech)
                                # Estimate background with nbjetvsOnZ
                                numC = dataH2.GetBinContent(1, 2)
                                numA = dataH2.GetBinContent(1, 3)
                                numB = dataH2.GetBinContent(2, 3)
                                numFake = numC / numA
                                numD = int(numC / numA * numB)
                                errC = dataH2.GetBinError(1, 2)
                                errA = dataH2.GetBinError(1, 3)
                                errB = dataH2.GetBinError(2, 3)
                                errFake = numFake * math.sqrt((errC / numC)**2 + (errA / numA)**2)
                                errD = int(numD * math.sqrt((errC / numC)**2 + (errA / numA)**2 + (errB / numB)**2))
                                print("fake factor: %.2f\pm%.2f" % (numFake, errFake))
                                print("prediction: %d\pm%d" % (numD, errD))
                                # Validate estimation with nbjetvsOnZ
                                numC = dataH2.GetBinContent(1, 3)
                                numA = dataH2.GetBinContent(1, 4)
                                numB = dataH2.GetBinContent(2, 4)
                                numFake = numC / numA
                                numD = int(numC / numA * numB)
                                errC = dataH2.GetBinError(1, 3)
                                errA = dataH2.GetBinError(1, 4)
                                errB = dataH2.GetBinError(2, 4)
                                errFake = numFake * math.sqrt((errC / numC)**2 + (errA / numA)**2)
                                errD = int(numD * math.sqrt((errC / numC)**2 + (errA / numA)**2 + (errB / numB)**2))
                                print("fake factor: %.2f\pm%.2f" % (numFake, errFake))
                                print("validation: %d\pm%d" % (numD, errD))
