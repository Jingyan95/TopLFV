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

def StackHist(hists, SignalHists, Fnames, c="charge", ch = "channel", reg = "region", regName = ["region",""], year='2016', var="sample", varname="v"):
    folder='StackHist'
    hs = ROOT.THStack("hs","")
    for num in range(1,len(hists)):
        hs.Add(hists[num])

    binwidth= array( 'd' )
    bincenter= array( 'd' )
    yvalue= array( 'd' )
    yerrup= array( 'd' )
    yerrdown= array( 'd' )
    T=hists[0].Clone()
    for b in range(T.GetNbinsX()):
        if T.GetBinContent(b+1)>0:
            binwidth.append(0)
            bincenter.append(T.GetBinCenter(b+1))
            yvalue.append(T.GetBinContent(b+1))
            yerrup.append(T.GetBinError(b+1))
            yerrdown.append(T.GetBinError(b+1))
    if len(bincenter)>0:
       dummy = ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdown,yerrup)
    else:
       dummy = ROOT.TGraphAsymmErrors() 

    canvas = ROOT.TCanvas(year+c+ch+reg+var,year+c+ch+reg+var,50,50,865,780)
    canvas.SetGrid()
    canvas.SetBottomMargin(0.17)
    canvas.cd()
    
    ROOT.gStyle.SetErrorX(0)

    legend = ROOT.TLegend(0.42,0.69,0.57,0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend2 = ROOT.TLegend(0.57,0.69,0.72,0.88)
    legend2.SetBorderSize(0)
    legend2.SetFillStyle(0)
    legend2.SetTextFont(42)
    legend2.SetTextSize(0.05)
    legend3 = ROOT.TLegend(0.412,0.56,0.75,0.683)
    legend3.SetBorderSize(0)
    legend3.SetFillStyle(0)
    legend3.SetTextFont(42)
    legend3.SetTextSize(0.05)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.305 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.05)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kTRUE)
    
    for H in range(len(SignalHists)):
        if H>0:
           SignalHists[H].Scale(100)
        else:
           SignalHists[H].Scale(0.5)

    y_max=2000*hists[0].GetMaximum()
    if y_max<2000*hs.GetStack().Last().GetMaximum():
        y_max=2000*hs.GetStack().Last().GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetLineWidth(2)
    x_min=hists[0].GetXaxis().GetBinLowEdge(1)
    x_max=hists[0].GetXaxis().GetBinLowEdge(hists[0].GetXaxis().GetNbins())+hists[0].GetXaxis().GetBinWidth(hists[0].GetXaxis().GetNbins())

    frame = pad1.DrawFrame(x_min,0.2,x_max,y_max)
    frame.SetTitle("")
    frame.GetYaxis().SetTitle('Events')
    frame.GetXaxis().SetLabelSize(0)
    frame.GetYaxis().SetTitleOffset(0.87)
    frame.GetYaxis().SetTitleSize(0.07)
    frame.GetYaxis().SetLabelSize(0.05)
    #frame.GetYaxis().SetNoExponent()
    pad1.Update()
    dummy.Draw("P")
    hs.Draw("histSAME")
    for H in range(len(SignalHists)):
        SignalHists[H].SetLineWidth(3)
        SignalHists[H].SetFillColor(0)
        SignalHists[H].SetLineStyle(H+1)
        SignalHists[H].Draw("histSAME")
    dummy.Draw("PSAME")
    frame.Draw("AXISSAMEY+")
    frame.Draw("AXISSAMEX+")
    pad1.Update()

    SumofMC = hs.GetStack().Last()
    binwidth= array( 'd' )
    bincenter= array( 'd' )
    yvalue= array( 'd' )
    yerrup= array( 'd' )
    yerrdown= array( 'd' )
    yvalueRatio= array( 'd' )
    yerrupRatio= array( 'd' )
    yerrdownRatio= array( 'd' )
    for b in range(SumofMC.GetNbinsX()):
        if SumofMC.GetBinContent(b+1)>0:
            binwidth.append(SumofMC.GetBinWidth(b+1)/2)
            bincenter.append(SumofMC.GetBinCenter(b+1))
            yvalue.append(SumofMC.GetBinContent(b+1))
            yerrup.append(SumofMC.GetBinError(b+1))
            yerrdown.append(SumofMC.GetBinError(b+1))
            yvalueRatio.append(1)
            yerrupRatio.append(SumofMC.GetBinError(b+1)/SumofMC.GetBinContent(b+1))
            yerrdownRatio.append(SumofMC.GetBinError(b+1)/SumofMC.GetBinContent(b+1))
    if len(bincenter)>0:
       error = ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdown,yerrup)
       errorRatio = ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalueRatio,binwidth,binwidth,yerrdownRatio,yerrupRatio)
    else:
       error = ROOT.TGraphAsymmErrors()
       errorRatio = ROOT.TGraphAsymmErrors()
    error.SetFillColor(13)
    error.SetLineColor(13)
    error.SetFillStyle(3254)
    error.SetLineWidth(4)
    error.Draw("2")

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
    Label_cms = ROOT.TLatex(0.15,0.92,label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.SetTextSize(0.081)
    Label_cms.Draw()
    label_cms1="Work in progress"
    Label_cms1 = ROOT.TLatex(0.255,0.92,label_cms1)
    Label_cms1.SetNDC()
    Label_cms1.SetTextSize(0.063)
    Label_cms1.SetTextFont(52)
    Label_cms1.Draw()
    if (year == 'All'):
       Label_lumi = ROOT.TLatex(0.625,0.92,Lumi+" fb^{-1} (13 TeV)")
    else:
       Label_lumi = ROOT.TLatex(0.673,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.SetTextSize(0.063)
    Label_lumi.Draw("same")
    ch_plot = ch
    if 'ee' in ch:
        if 'SS' in c:
            ch_plot='ee#tau_{h}'
        else:
            ch_plot='e#bar{e}#tau_{h}'
    if 'emu' in ch:
        if 'SS' in c:
            ch_plot='e#mu#tau_{h}'
        else:
            ch_plot='e#bar{#mu}#tau_{h}'
    if 'mumu' in ch:
        if 'SS' in c:
            ch_plot='#mu#mu#tau_{h}'
        else:
            ch_plot='#mu#bar{#mu}#tau_{h}'
    Label_channel = ROOT.TLatex(0.18,0.8,ch_plot)
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.SetTextSize(0.063)
    Label_channel.Draw("same")
    Label_region = ROOT.TLatex(0.18,0.72,regName[0])
    Label_region.SetNDC()
    Label_region.SetTextFont(42)
    Label_region.SetTextSize(0.063)
    Label_region.Draw("same")
    Label_region2 = ROOT.TLatex(0.18,0.64,regName[1])
    Label_region2.SetNDC()
    Label_region2.SetTextFont(42)
    Label_region2.SetTextSize(0.063)
    Label_region2.Draw("same")

    legend.AddEntry(dummy,Fnames[0],'ep')
    for num in range(1,len(hists)):
        if num<(len(hists)-2):
           legend.AddEntry(hists[num],Fnames[num],'F')
        else:
           legend2.AddEntry(hists[num],Fnames[num],'F')
    error.SetLineWidth(1)
    legend2.AddEntry(error,'Stat. only','F')
    for H in range(len(SignalHists)):
        if H==0:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H]+" (#mu_{#scale[0.8]{ll`tu}}^{#scale[0.8]{vector}} = 0.5)",'L')
        else:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H]+" (#mu_{#scale[0.8]{ll`tu}}^{#scale[0.8]{vector}} = 100)",'L')
    legend.Draw("same")
    legend2.Draw("same")
    legend3.Draw("same")

    pad1.Update()

    pad2.cd()
    dummy_ratio = hists[0].Clone()
    dummy_ratio.SetTitle("")
    dummy_ratio.SetMarkerStyle(20)
    dummy_ratio.SetMarkerSize(1.2)
    dummy_ratio.SetLineWidth(2)
    dummy_ratio.GetXaxis().SetTitle(varname)
#    dummy_ratio.GetXaxis().CenterTitle()
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()
    dummy_ratio.GetYaxis().SetNoExponent()
    dummy_ratio.GetXaxis().SetTitleSize(0.05/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.05/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.115)
    dummy_ratio.GetYaxis().SetLabelSize(0.1125)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.007)
    dummy_ratio.GetYaxis().SetTitleOffset(0.36)
    dummy_ratio.GetXaxis().SetTitleOffset(0.9)
    dummy_ratio.GetYaxis().SetNdivisions(504)
    dummy_ratio.GetYaxis().SetRangeUser(0.2,1.8)
    if ('njet' in var):
       dummy_ratio.GetXaxis().SetNdivisions(-006)
    if ('nbjet' in var):
       dummy_ratio.GetXaxis().SetNdivisions(-004)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('#frac{Data}{Pred.}')
    dummy_ratio.Draw('E1')
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    errorRatio.SetFillColor(13)
    errorRatio.SetLineColor(13)
    errorRatio.SetFillStyle(3254)
    errorRatio.SetLineWidth(4)
    errorRatio.Draw("2")
    if not os.path.exists(folder):
       os.makedirs(folder)
    if not os.path.exists(folder + '/' + year):
       os.makedirs(folder  + '/' + year)
    if not os.path.exists(folder + '/' + year + '/' + c):
       os.makedirs(folder + '/' + year + '/' + c)
    if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch):
       os.makedirs(folder + '/' + year + '/' + c + '/' + ch)
    if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch +'/'+reg):
       os.makedirs(folder + '/' + year + '/' + c + '/' + ch +'/'+ reg)
    canvas.Print(folder + '/' + year + '/' + c + '/' + ch +'/'+ reg +'/'+var + ".pdf")
    del canvas
    gc.collect()
    
def CompareBackgrounds(hists, year='2016', c = "OS", ch = "emu", reg = "ll", var = "mva1", varname="v", SamplesName=[]):
    folder='CompareBackgrounds'
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
        legend.AddEntry(hists[n],SamplesName[n+1],'LP')
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
regions=["ll","llOnZ","llOffZ","llOffZMetg20Jetgeq1","llOffZMetg20Jetgeq1Bleq1","llOffZMetg20Jetgeq1Bgeq1"]
regionsName=[["No cuts",""],["OnZ",""],["OffZ",""],["OffZ, p_{T}^{miss}>20","njet#geq1"],["OffZ, p_{T}^{miss}>20","njet#geq1, nbjet#leq1"],["OffZ, p_{T}^{miss}>20","njet#geq1, nbjet#geq1"]]
vars=["elMVAv1Prompt","elMVAv1HF","elMVAv1Other","elMVAv2Prompt","elMVAv2HF","elMVAv2Other","elMVAv3Prompt","elMVAv3HF","elMVAv3Other",
      "muMVAv1Prompt","muMVAv1HF","muMVAv1Other","muMVAv2Prompt","muMVAv2HF","muMVAv2Other","muMVAv3Prompt","muMVAv3HF","muMVAv3Other",
      "taMVAv1Had","taMVAv1Fake","taMVAv1Other","taMVAv2Had","taMVAv2Fake","taMVAv2Other","taMVAv3Had","taMVAv3Fake","taMVAv3Other",
      "llM","llDr","lep1Pt","lep2Pt","taPt","jet1Pt","njet","nbjet","MET"]

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
          "Leading jet p_{T} [GeV]", "njet", "nbjet","MET [GeV]"]

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
       
Samples = ['Data.root', 'TTTo2L2Nu.root', 'DYM50.root', 'TX.root', 'VV.root', 'LFVStScalarU.root', 'LFVTtScalarU.root']
SamplesName = ["Data", "t#bar{t}", "DY", "t#bar{t}X", "VV", "C_{ll`tu}^{ST}", "C_{ll`tu}^{TT}"]
SamplesNameStack = ["Data", "t#bar{t}", "DY", "t#bar{t}X", "VV(V)", "CLFV top production", "CLFV top decay"]

colors =  [ROOT.kBlack,ROOT.kRed-4,ROOT.kOrange-3,ROOT.kYellow,ROOT.kGreen,ROOT.kViolet+1,ROOT.kGray]
markerStyle =  [20,25,26,27,28,29,30]

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
                        l4.append(h)
                    l3.append(l4)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)
                       
#Compare different backgrounds
for numyear, nameyear in enumerate(year):
    for numc, namec in enumerate(charges):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(vars):
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
                    CompareBackgrounds(H2, nameyear, namec, namech, namereg, namevar, varsName[numvar], SamplesName)