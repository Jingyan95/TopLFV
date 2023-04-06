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
TGaxis.SetMaxDigits(2)
    
def compareBackgrounds(hists, year='2016', c = "OS", ch = "emu", reg = "ll", var = "mva1", varname="v", SamplesName=[]):
    folder='compareBackgrounds'
    if not os.path.exists(folder):
       os.makedirs(folder)
    if not os.path.exists(folder + '/' + year):
       os.makedirs(folder  + '/' + year)
    if not os.path.exists(folder + '/' + year + '/' + c):
       os.makedirs(folder + '/' + year + '/' + c)
    if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch):
       os.makedirs(folder + '/' + year + '/' + c + '/' + ch)
    if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch +'/'+reg):
       os.makedirs(folder + '/' + year + '/' + c + '/' + ch +'/'+reg)

    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.cd()

    legend = ROOT.TLegend(0.1,0.3,1,0.8)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.3)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0., 0.1, 0.99 , 0)#used for the legend
    pad2=ROOT.TPad("pad2", "pad2", 0.1, 0.0, 1, 1 , 0)#used for the hists
    pad1.Draw()
    pad2.Draw()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.1)
    pad1.SetLeftMargin(0.2)
    pad1.SetRightMargin(0.01)
    pad2.SetBottomMargin(0.1)
    pad2.SetLeftMargin(0.1)
    pad2.SetRightMargin(0.1)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)
    pad2.SetLogy(ROOT.kTRUE)

    pad2.cd()
    maxi=0
    for n,G in enumerate(hists):
        if hists[n].GetMaximum()>maxi:
           maxi = hists[n].GetMaximum()
        hists[n].SetFillColor(0)
        hists[n].SetMinimum(0.001)
        legend.AddEntry(hists[n],SamplesName[n],'LP')
    hists[0].SetTitle( '' )
    hists[0].GetYaxis().SetTitle( 'Events' )
    hists[0].GetXaxis().SetTitle(varname)
    hists[0].GetXaxis().SetLabelSize(0.03)
    hists[0].GetYaxis().SetLabelSize(0.03)
    hists[0].GetXaxis().SetTitleSize(0.03)
    hists[0].GetYaxis().SetTitleSize(0.03)
#    hists[0].GetYaxis().SetNoExponent()
    hists[0].GetXaxis().SetTitleOffset(1.1)
    hists[0].GetYaxis().SetTitleOffset(1.5)
    hists[0].GetYaxis().SetNdivisions(804)
    hists[0].GetXaxis().SetNdivisions(808)
    hists[0].GetYaxis().SetRangeUser(0.01,100*maxi)
    hists[0].GetXaxis().SetNoExponent()
    hists[0].Draw('HIST')
    for n,G in enumerate(hists):
        hists[n].Draw('HIST SAME')
        hists[n].Draw('HIST P SAME')
    hists[0].Draw("AXISSAMEY+")
    hists[0].Draw("AXISSAMEX+")
    Lumi = '138'
    if (year == '2016APV'):
        Lumi = '19.5'
    if (year == '2016'):
        Lumi = '16.8'
    if (year == '2017'):
        Lumi = '41.5'
    if (year == '2018'):
        Lumi = '59.8'
    label_cms="CMS"
    Label_cms = ROOT.TLatex(0.115,0.92,label_cms)
    Label_cms.SetTextSize(0.04)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    label_cms1="Work in Progress"
    Label_cms1 = ROOT.TLatex(0.2,0.92,label_cms1)
    Label_cms1.SetNDC()
    Label_cms1.SetTextSize(0.028);
    Label_cms1.SetTextFont(52)
    Label_cms1.Draw()
    Label_lumi = ROOT.TLatex(0.63,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetTextSize(0.035)
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    reg_plot = year + " / " + c + " / " + ch + " / " + reg
    Label_channel = ROOT.TLatex(0.2,0.85,reg_plot)
    Label_channel.SetNDC()
    Label_channel.SetTextSize(0.035)
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")
    pad1.cd()
    legend.Draw("same")
    canvas.Print(folder + '/' + year + '/' + c + '/' + ch + '/' + reg + '/' +var + ".pdf")
    del canvas
    gc.collect()

year_RunII=['2016APV','2016','2017','2018','All']
year=[]
charges=["OS","SS"];
channels=["ee","emu","mumu"];
regions=["ll","llFakeTau","llHadTau","llOther"]
vars=["eleMVA","muMVA","tauMVA"]
varsName=["Electron MVA","Muon MVA","Tau MVA"]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--n', dest = 'NAMETAG', default= '2016' )

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
name = ARGS.NAMETAG

loc = os.path.dirname(sys.path[0])+'/'
HistAddress = loc + 'hists/'
#HistAddress = '/afs/cern.ch/work/j/jingyan/Analysis/CMSSW_10_6_4/src/TopLFV/hists/'

for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
       year.append(year_RunII[numyear])
       
Samples = ['TTTo2L2Nu.root', 'DYM50.root', 'TTW.root', 'TTH.root']
SamplesName = ["t#bar{t}", "DY", "t#bar{t}W", "t#bar{t}H"]

colors =  [ROOT.kBlack,ROOT.kRed,ROOT.kGreen,ROOT.kBlue]
markerStyle =  [20,25,26,27]

Hists = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        print HistAddress + nameyear+ '_' + Samples[f]
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
                        h.SetLineColor(colors[f])
                        h.SetLineWidth(2)
                        h.SetMarkerColor(colors[f])
                        h.SetMarkerStyle(markerStyle[f])
                        l4.append(h)
                    l3.append(l4)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)
                       
#Compare different signals
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(vars):
                    HH = []
                    for f in range(len(Samples)):
                        HH.append(Hists[numyear][f][numc][numch][numreg][numvar])
                    compareBackgrounds(HH, nameyear, namec, namech, namereg, namevar, varsName[numvar], SamplesName)





