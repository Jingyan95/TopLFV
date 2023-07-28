import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = 1;')
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
from plotter import StackHist, Hist2D, CompareBackgrounds, SummaryPlot, CompareEstimate
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'helper'))
from cutflow import CutflowTables
from bkg_estimate import BackgroundEstimate
TGaxis.SetMaxDigits(2)


year_RunII = ['2016APV', '2016', '2017', '2018', 'All']

charges = ['OS', 'SS']

channels = ['ee', 'emu', 'mumu']

regions = [
    'll',                         #0
    'llOnZMetg20Jetgeq1',         #1
    'llOffZMetg20B1',             #2
    'llOffZMetg20B2',             #3
    'llStl300',                   #4
    'llOnZ',                      #5
    'llbtagg1p3',                 #6
    'llStg300OffZbtagl1p3',       #7
    'llStg300OffZbtagl1p3Tight',  #8
    'llMetg20Jetgeq1',            #9
    'llMetg20Jetgeq1B1',          #10
    'llMetg20Jetgeq1B0']          #11
regionsName = [
    ['No cuts', '', ''],
    ['p_{T}^{miss}>20GeV, njet#geq1', 'OnZ', ', Z+jets CR'],
    ['p_{T}^{miss}>20GeV, njet#geq1', 'OffZ, nbjet=1', ', SR'],
    ['p_{T}^{miss}>20GeV, njet#geq1', 'OffZ, nbjet=2', ', t#bar{t}+jets CR'],
    ['S_{T}<300GeV', '', ', CR'],
    ['OnZ', '', ', Z+jets CR'],
    ['btag>1.3', '', ', t#bar{t}+jets CR'],
    ['S_{T}>300GeV, OffZ', 'btag<1.3', ', SR(Alt, Loose)'],
    ['S_{T}>300GeV, OffZ', 'btag<1.3, njet#geq1 or S_{T}>500GeV', ', SR(Alt, Tight)'],
    ['p_{T}^{miss}>20GeV, njet#geq1', '', ', Background Estimation'],
    ,['p_{T}^{miss}>20GeV, njet#geq1', 'nbjet=1', ', Background Estimation'],
    ['p_{T}^{miss}>20GeV, njet#geq1', 'nbjet=0', ', Background Estimation']]
regionsNameLatex = [
    '2$l+\\tau_h$, no cuts',
    '2$l+\\tau_h$, Z + jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, on Z',
    '2$l+\\tau_h$, SR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, off Z, nbjet $=1$',
    '2$l+\\tau_h$, $t\\bar{t}$ + jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, off Z, nbjet $=2$',
    '2$l+\\tau_h$, CR, $S_T<300$ GeV',
    '2$l+\\tau_h$, Z + jets CR, on Z',
    '2$l+\\tau_h$, $t\\bar{t}$ + jets CR, btag $>1.3$',
    '2$l+\\tau_h$, SR (Alt, Loose), $S_T>300$ GeV, off Z, btag $<1.3$',
    '2$l+\\tau_h$, SR (Alt, Tight), $S_T>300$ GeV, off Z, btag $<1.3$, njet $\\geq 1$ or $S_T>500$ GeV',
    '2$l+\\tau_h$, Background Estimation, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$',
    '2$l+\\tau_h$, Background Estimation, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$',
    '2$l+\\tau_h$, Background Estimation, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=0$']

vars = [
    'llM', 'llDr', 'lep1Pt', 'lep2Pt',
    'taPt', 'taPtHadronic', 'taEta', 'taEtaHadronic', 'taVsJetWP', 'taDxy', 'taDz', 'taDecayMode',
    'jet1Pt', 'njet', 'nbjet', 'MET', 'subSR', 'LFVemuM', 'LFVetaM', 'LFVmutaM',
    'LFVemuDr', 'LFVetaDr', 'LFVmutaDr', 'LFVePt', 'LFVmuPt', 'LFVtaPt', 'BalepPt',
    'Topmass', 'Ht', 'St', 'btagSum']
varsName = [
    'm(l#bar{l}) [GeV]', '#DeltaR(l#bar{l})',
    'Leading lepton p_{T} [GeV]', 'Sub-leading lepton p_{T} [GeV]',
    '#tau p_{T} [GeV]', '#tau_{h} p_{T} [GeV]', '#tau #eta', '#tau_{h} #eta',
    '#tau vs Jets WP', '#tau d_{xy} [cm]', '#tau d_{z} [cm]', '#tau Decay Mode',
    'Leading jet p_{T} [GeV]', 'njet', 'nbjet (Loose WP)', 'MET [GeV]', 'SR subdivided',
    'm(e#bar{#mu}) [GeV]', 'm(e#bar{#tau}) [GeV]', 'm(#mu#bar{#tau}) [GeV]',
    '#DeltaR(e,#bar{#mu}) [GeV]', '#DeltaR(e,#bar{#tau}) [GeV]', '#DeltaR(#mu,#bar{#tau}) [GeV]',
    'LFV electron p_{T} [GeV]', 'LFV muon p_{T} [GeV]', 'LFV tau p_{T} [GeV]',
    'Bachelor lepton p_{T} [GeV]', 'm(top) [GeV]', 'H_{T} [GeV]', 'S_{T} [GeV]', 'Sum of btagging scores']

vars2D = [
    'nbjetvsOnZ', 'nbjetvsOnZHadronic', 'TauIdvsOnZ', 'TauIdvsOnZHadronic',
    'TauIdvsOnZ_pt20to40', 'TauIdvsOnZ_pt40to60', 'TauIdvsOnZ_pt60to100', 'TauIdvsOnZ_pt100to220']
    # 'TauIdvsOnZ_pt20to40', 'TauIdvsOnZ_pt40to60', 'TauIdvsOnZ_pt60to80', 'TauIdvsOnZ_pt80to100',
    # 'TauIdvsOnZ_pt100to120', 'TauIdvsOnZ_pt120to140', 'TauIdvsOnZ_pt140to160', 'TauIdvsOnZ_pt160to180',
    # 'TauIdvsOnZ_pt180to200', 'TauIdvsOnZ_pt200to220']
vars2DName = [
    ['All Events', 'nbjet (Loose WP)'],
    ['Events with #tau_{h}', 'nbjet (Loose WP)'],
    ['All Events', '#tau vs Jets WP'],
    ['Events with #tau_{h}', '#tau vs Jets WP'],
    ['Events with 20.0 < #tau p_{T} < 40.0 [GeV]', '#tau vs Jets WP'],
    ['Events with 40.0 < #tau p_{T} < 60.0 [GeV]', '#tau vs Jets WP'],
    ['Events with 60.0 < #tau p_{T} < 100.0 [GeV]', '#tau vs Jets WP'],
    ['Events with 100.0 < #tau p_{T} < 220.0 [GeV]', '#tau vs Jets WP']]
    # ['Events with 80.0 < #tau p_{T} < 100.0 [GeV]', '#tau vs Jets WP'],
    # ['Events with 100.0 < #tau p_{T} < 120.0 [GeV]', '#tau vs Jets WP'],
    # ['Events with 120.0 < #tau p_{T} < 140.0 [GeV]', '#tau vs Jets WP'],
    # ['Events with 140.0 < #tau p_{T} < 160.0 [GeV]', '#tau vs Jets WP'],
    # ['Events with 160.0 < #tau p_{T} < 180.0 [GeV]', '#tau vs Jets WP'],
    # ['Events with 180.0 < #tau p_{T} < 200.0 [GeV]', '#tau vs Jets WP'],
    # ['Events with 200.0 < #tau p_{T} < 220.0 [GeV]', '#tau vs Jets WP']]
vars2DBinLabels = [
    [['On Z', 'Off Z'], ['0', '1', '2', '3']],
    [['On Z', 'Off Z'], ['0', '1', '2', '3']],
    [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    # [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    # [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    # [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    # [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    # [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    # [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']],
    [['On Z', 'Off Z'], ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']]]
vars2DLines = [
    [[1], [2, 3]],
    [[1], []]]

# Samples = ['Data.root', 'TX.root', 'VV.root', 'DY.root', 'TT.root', 'LFVStScalarU.root', 'LFVTtScalarU.root']
# SamplesName = ['Data', 't#bar{t}X', 'VV', 'DY', 't#bar{t}', 'C_{ll`tu}^{ST}', 'C_{ll`tu}^{TT}']
# SamplesNameLatex = ['Data', '$t\\bar{t}X$', 'VV', 'DY', '$t\\bar{t}$', 'St Scalar U', 'Tt Scalar U']
# SamplesNameStack = ['Data', 't#bar{t}+X', 'VV(V)', 'DY', 't#bar{t}', 'CLFV top production', 'CLFV top decay']
Samples = ['fr_LFVStScalarU.root', 'sim_LFVStScalarU.root']
SamplesName = ['C_{ll`tu}^{ST} fr', 'C_{ll`tu}^{ST} sim']
SamplesNameLatex = ['fr St Scalar U', 'sim St Scalar U']
SamplesNameStack = ['fr CLFV top production', 'sim CLFV top production']

colors = [ROOT.kBlack, ROOT.kYellow, ROOT.kGreen, ROOT.kOrange - 3, ROOT.kRed - 4, ROOT.kViolet + 1, ROOT.kGray]
markerStyle = [20, 25, 26, 27, 28, 29, 30]

SaveMVA = False


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--v', dest = 'VERBOSE', default = True)
parser.add_argument('--n', dest = 'NAMETAG', default = '2016')
ARGS = parser.parse_args()
verbose = ARGS.VERBOSE
name = ARGS.NAMETAG


year = []
for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
        year.append(year_RunII[numyear])


# Read in histograms
loc = os.path.dirname(sys.path[0]) + '/'
HistAddress = loc + 'hists/'
Hists = []
Hists2D = []
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
                            h.Reset('ICE')
                        l4.append(h)

                    for numvar, namevar in enumerate(vars2D):
                        h_2D = Files[f].Get(namec + '_' + namech + '_' + namereg + '_' + namevar)
                        # Take care of underflow/overflow
                        for xBin in range(1, h_2D.GetXaxis().GetNbins() + 1):
                            h_2D.SetBinContent(xBin, 1, h_2D.GetBinContent(xBin, 0) + h_2D.GetBinContent(xBin, 1))
                            h_2D.SetBinContent(xBin, h_2D.GetYaxis().GetNbins(), h_2D.GetBinContent(xBin, h_2D.GetYaxis().GetNbins()) + h_2D.GetBinContent(xBin, h_2D.GetYaxis().GetNbins() + 1))
                        for yBin in range(1, h_2D.GetYaxis().GetNbins() + 1):
                            h_2D.SetBinContent(1, yBin, h_2D.GetBinContent(0, yBin) + h_2D.GetBinContent(1, yBin))
                            h_2D.SetBinContent(h_2D.GetXaxis().GetNbins(), yBin, h_2D.GetBinContent(h_2D.GetXaxis().GetNbins(), yBin) + h_2D.GetBinContent(h_2D.GetXaxis().GetNbins() + 1, yBin))
                        # No CR in SS channels
                        if ('SS' in namec) and ('B2' in namereg or 'OnZ' in namereg or 'Stl300' in namereg or 'btagg1p3' in namereg):
                            h_2D.Reset('ICE')
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


# Make cutflow tables and background estimates
for numyear, nameyear in enumerate(year):
    CutflowTables(Hists, numyear, nameyear, regions, regionsNameLatex, charges, channels, Samples, SamplesNameLatex)

    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            tauWPcut = 5
            tauWPstr = 'Tight'
            # binEdges = [20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0]
            binEdges = [20.0, 40.0, 60.0, 100.0, 220.0]

            # BackgroundEstimate(Hists2D, numyear, Samples.index('DY.root'), [], charges.index('OS'), numch, numreg,
            #                    vars2D.index('TauIdvsOnZ'), -1, 1, tauWPcut,
            #                    '$\\bm{\\tau_h}$ vs Jets $\\bm{\\geq}$ ' + tauWPstr + ' WP',
            #                    '$\\bm{\\tau_h}$ vs Jets $\\bm{<}$ ' + tauWPstr + ' WP', 'On Z', 'Off Z',
            #                    '2016-DY-OS-' + namech + '-' + namereg, True)
            # BackgroundEstimate(Hists2D, numyear, Samples.index('Data.root'), [1, 2, 3, 4, 5, 6], charges.index('OS'), numch, numreg,
            #                    vars2D.index('TauIdvsOnZ'), vars2D.index('TauIdvsOnZHadronic'), 1, tauWPcut,
            #                    '$\\bm{\\tau_h}$ vs Jets $\\bm{\\geq}$ ' + tauWPstr + ' WP',
            #                    '$\\bm{\\tau_h}$ vs Jets $\\bm{<}$ ' + tauWPstr + ' WP', 'On Z', 'Off Z',
            #                    '2016-All-OS-' + namech + '-' + namereg, True)

            # Plot comparing background estimate vs simulation with pt bins
            for sample in ['DY.root', 'TT.root']:
                ff = []
                errFf = []
                pred = []
                errPred = []
                sim = []
                errSim = []
                for ptIdx in range(len(binEdges) - 1):
                    results = BackgroundEstimate(Hists2D, numyear, Samples.index(sample), [], charges.index('OS'), numch, numreg,
                                                 vars2D.index('TauIdvsOnZ_pt' + str(int(binEdges[ptIdx])) + 'to' + str(int(binEdges[ptIdx + 1]))),
                                                 -1, 1, tauWPcut, '$\\bm{\\tau_h}$ vs Jets $\\bm{\\geq}$ ' + tauWPstr + ' WP',
                                                 '$\\bm{\\tau_h}$ vs Jets $\\bm{<}$ ' + tauWPstr + ' WP', 'On Z', 'Off Z', nameyear, 'OS',
                                                 namech, namereg, 'pt' + str(int(binEdges[ptIdx])) + 'to' + str(int(binEdges[ptIdx + 1])), False)
                    ff.append(results[0])
                    errFf.append(results[1])
                    pred.append(results[2])
                    errPred.append(results[3])
                    sim.append(results[4])
                    errSim.append(results[5])
                print(namech, namereg, sample)
                print('fake', ff, errFf)
                print('prediction', pred, errPred)
                print('simulation', sim, errSim)
                CompareEstimate(ff, errFf, [], [], binEdges, sample, 'OS', namech, namereg,
                                regionsName[numreg], nameyear, 'bkg_estimate_ff_vspt', '#tau p_{T} [GeV]',
                                sample[0:-5] + ' Fake Factor', ['Fake Factor'])
                CompareEstimate(pred, errPred, [sim], [errSim], binEdges, sample, 'OS', namech, namereg,
                                regionsName[numreg], nameyear, 'bkg_estimate_vspt', '#tau p_{T} [GeV]',
                                sample[0:-5] + ' Background Estimation', ['Prediction', 'Actual'])

'''
# Make 1D histograms
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(vars):

                    if ('MVA' in namevar) and (not SaveMVA):
                        continue

                    if not namevar == 'taPt': continue

                    H1 = []
                    H1Signal = []
                    # H2 = []
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
                        # h2 = Hists[numyear][f][numc][numch][numreg][numvar].Clone()
                        # h2.SetLineColor(colors[f])
                        # h2.SetLineWidth(2)
                        # h2.SetMarkerColor(colors[f])
                        # h2.SetMarkerStyle(markerStyle[f])
                        # H2.append(h2)

                        # print(Samples[f], namevar)
                        # for bIdx in range(1, h1.GetNbinsX() + 1):
                        #     

                    StackHist(H1, H1Signal, SamplesNameStack, namec, namech, namereg, regionsName[numreg], nameyear, namevar, varsName[numvar])
                    # CompareBackgrounds(H2, nameyear, namec, namech, namereg, namevar, varsName[numvar], SamplesName)

# Make summary histograms
for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        H = []
        HSignal = []
        for f in range(len(Samples)):
            h = Hists[numyear][f][0][0][numreg][15].Clone()
            h.Reset('ICE')
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

# Make 2D histograms
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):

                for f in range(len(Samples)):
                    for numvar, namevar in enumerate(vars2D):
                        if numvar >= 4: continue
                        h2D = Hists2D[numyear][f][numc][numch][numreg][numvar].Clone()
                        Hist2D(h2D, Samples[f], namec, namech, namereg, nameyear, vars2D[numvar],
                               vars2DName[numvar][0], vars2DName[numvar][1], [], [], vars2DBinLabels[numvar][0], vars2DBinLabels[numvar][1])

                # Make 2D histograms for fake tau background estimation
                for numvar in range(0, len(vars2D), 2):
                    if numvar >= 4: continue
                    dataH2 = Hists2D[numyear][0][numc][numch][numreg][numvar].Clone() # Get data
                    for f in range(1, len(Samples)):
                        mcH2 = Hists2D[numyear][f][numc][numch][numreg][numvar + 1].Clone() # Subtract hadronic taus
                        dataH2.Add(mcH2, -1.0)
                    Hist2D(dataH2, 'All.....', namec, namech, namereg, nameyear, vars2D[numvar],
                           vars2DName[numvar][0], vars2DName[numvar][1], vars2DLines[numvar / 2][0], vars2DLines[numvar / 2][1],
                           vars2DBinLabels[numvar][0], vars2DBinLabels[numvar][1])
'''