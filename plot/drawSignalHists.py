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
    
def compareSignals(hists, year='2016', ch = "emu", reg = "ll", var = "pt", varname="v", SamplesName=[]):
    folder='CompareSignals'
    if not os.path.exists(folder):
       os.makedirs(folder)
    if not os.path.exists(folder + '/' + year):
       os.makedirs(folder  + '/' + year)
    if not os.path.exists(folder + '/' + year + '/' + ch):
       os.makedirs(folder + '/' + year + '/' + ch)
    if not os.path.exists(folder + '/' + year + '/' + ch +'/'+reg):
       os.makedirs(folder + '/' + year + '/' + ch +'/'+reg)

    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,950,780)
    canvas.SetGrid();
    canvas.cd()

    legend = ROOT.TLegend(0.01,0.3,1,0.8)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.16)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0., 0.125, 0.99 , 0)#used for the legend
    pad2=ROOT.TPad("pad2", "pad2", 0.125, 0.0, 1, 1 , 0)#used for the hists
    pad1.Draw()
    pad2.Draw()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.1)
    pad1.SetLeftMargin(0.2)
    pad1.SetRightMargin(0.01)
    pad2.SetBottomMargin(0.1)
    pad2.SetLeftMargin(0.085)
    pad2.SetRightMargin(0.1)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)
    pad2.SetLogy(ROOT.kFALSE)

    pad2.cd()
    maxi=0
    for n,G in enumerate(hists):
        hists[n].SetFillColor(0)
        int = 1
        if hists[n].Integral()>0:
            int=hists[n].Integral()
        hists[n].Scale(1/int)
        if hists[n].GetMaximum()>maxi:
           maxi = hists[n].GetMaximum()
        legend.AddEntry(hists[n],SamplesName[n],'LP')
    hists[0].SetTitle( '' )
    hists[0].GetYaxis().SetTitle( 'Normalized Events' )
    hists[0].GetXaxis().SetTitle(varname)
    hists[0].GetXaxis().SetLabelSize(0.03)
    hists[0].GetYaxis().SetLabelSize(0.03)
    hists[0].GetXaxis().SetTitleSize(0.03)
    hists[0].GetYaxis().SetTitleSize(0.03)
    hists[0].GetYaxis().SetNoExponent()
    hists[0].GetXaxis().SetTitleOffset(1.1)
    hists[0].GetYaxis().SetTitleOffset(1.5)
    hists[0].GetYaxis().SetNdivisions(804)
    hists[0].GetXaxis().SetNdivisions(808)
    hists[0].GetYaxis().SetRangeUser(0,1.6*maxi)
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
    Label_cms = ROOT.TLatex(0.103,0.91,label_cms)
    Label_cms.SetTextSize(0.04)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    label_cms1="Simulation Private Work"
    Label_cms1 = ROOT.TLatex(0.188,0.91,label_cms1)
    Label_cms1.SetNDC()
    Label_cms1.SetTextSize(0.028);
    Label_cms1.SetTextFont(52)
    Label_cms1.Draw()
    Label_lumi = ROOT.TLatex(0.785,0.91,"13 TeV")
    Label_lumi.SetTextSize(0.035)
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    reg_plot = "C_{ll`tu}^{scalar}: top production"
    Label_channel = ROOT.TLatex(0.15,0.82,reg_plot)
    Label_channel.SetNDC()
    Label_channel.SetTextSize(0.035)
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")
    pad1.cd()
    legend.Draw("same")
    canvas.Print("SRbin.pdf")
    del canvas
    gc.collect()

year_RunII=['2016APV','2016','2017','2018','All']
year=[]
channels=["emu","etau","mutau","All"];
regions=["ll","llMl150","llMg150"]
vars=["LFVePt","LFVmuPt","LFVtauPt","llM","llDr"]
varsName=["LFV electron p_{T}^{GEN} (GeV)", "LFV muon p_{T}^{GEN} (GeV)", "LFV tau p_{T}^{GEN} (GeV)", "m(e#mu)^{GEN} (GeV)", "#DeltaR(e,#mu)^{GEN}"]

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
       
Samples = ['emu_llStg300OffZbtagl1p3.root', 'eta_llStg300OffZbtagl1p3.root', 'muta_llStg300OffZbtagl1p3.root']
HistsName = ['emu_llStg300OffZbtagl1p3', 'eta_llStg300OffZbtagl1p3', 'muta_llStg300OffZbtagl1p3']
SamplesName = ["e#mutu", "e#tautu", "#mu#tautu"]

colors =  [ROOT.kBlack,ROOT.kRed,ROOT.kBlue]
markerStyle =  [20,25,25]

Hists = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        Files.append(ROOT.TFile.Open(nameyear+ '_' + Samples[f]))
        print HistAddress + nameyear+ '_' + Samples[f]
        print HistsName[f]
        h = Files[f].Get(HistsName[f])
        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
        h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
        h.SetLineColor(colors[f])
        h.SetLineWidth(2)
        h.SetMarkerColor(colors[f])
        h.SetMarkerStyle(markerStyle[f])
        l0.append(h)
    Hists.append(l0)
                       
#Compare different signals
HH = []
HH.append(Hists[0][0])
HH.append(Hists[0][1])
HH.append(Hists[0][2])
compareSignals(HH, nameyear, '', '', '', 'SRbin', SamplesName)





