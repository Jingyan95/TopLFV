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
TGaxis.SetMaxDigits(2)

def CompareEff(hists, Fnames, c = "charge", ch = "channel", year = '2016', var = "sample", varname = "v"):
    folder = 'CompareEff'
    
    dummy = hists[0].Clone()

    canvas = ROOT.TCanvas(year+c+ch+var,year+c+ch+var,50,50,865,780)
    canvas.SetGrid()
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    ROOT.gStyle.SetErrorX(0)

    legend = ROOT.TLegend(0.62,0.69,0.77,0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)

    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99, 0) # used for the hist plot
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.305, 0) # used for the ratio plot
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
    pad1.SetLogy(ROOT.kFALSE)

    y_max = 1.3*dummy.GetMaximum()
    y_min = 0.5*dummy.GetMinimum()
    x_min = dummy.GetXaxis().GetBinLowEdge(1)
    x_max = dummy.GetXaxis().GetBinLowEdge(hists[0].GetXaxis().GetNbins())+hists[0].GetXaxis().GetBinWidth(hists[0].GetXaxis().GetNbins())
    frame = pad1.DrawFrame(x_min,y_min,x_max,y_max)
    frame.GetYaxis().SetTitle('Efficiency')
    frame.GetXaxis().SetLabelSize(0)
    frame.GetXaxis().SetNoExponent()
    frame.GetYaxis().SetTitleOffset(0.87)
    frame.GetYaxis().SetTitleSize(0.07)
    frame.GetYaxis().SetLabelSize(0.05)
    frame.GetYaxis().SetNoExponent()
    pad1.Update()
    dummy.Draw("PSAME")
    hists[1].Draw("PSAME")
    frame.Draw("AXISSAMEY+")
    frame.Draw("AXISSAMEX+")
    pad1.Update()

    Lumi = '138'
    if (year == '2016APV'):
        Lumi = '19.5'
    if (year == '2016'):
        Lumi = '16.8'
    if (year == '2017'):
        Lumi = '41.5'
    if (year == '2018'):
        Lumi = '59.8'
    label_cms = "CMS"
    Label_cms = ROOT.TLatex(0.15, 0.92, label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.SetTextSize(0.081)
    Label_cms.Draw()
    label_cms1 = "Work in progress"
    Label_cms1 = ROOT.TLatex(0.255, 0.92, label_cms1)
    Label_cms1.SetNDC()
    Label_cms1.SetTextSize(0.063)
    Label_cms1.SetTextFont(52)
    Label_cms1.Draw()
    if (year == 'All'):
       Label_lumi = ROOT.TLatex(0.672,0.92,Lumi+" fb^{-1} (13 TeV)")
    else:
       Label_lumi = ROOT.TLatex(0.673,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.SetTextSize(0.063)
    Label_lumi.Draw("same")
    ch_plot = ch
    if 'ee' in ch:
        if 'SS' in c:
            ch_plot='ee'
        else:
            ch_plot='e#bar{e}'
    if 'emu' in ch:
        if 'SS' in c:
            ch_plot='e#mu'
        else:
            ch_plot='e#bar{#mu}'
    if 'mue' in ch:
        if 'SS' in c:
            ch_plot='#me'
        else:
            ch_plot='#bar{#mu}e'
    if 'mumu' in ch:
        if 'SS' in c:
            ch_plot='#mu#mu'
        else:
            ch_plot='#mu#bar{#mu}'
    Label_channel = ROOT.TLatex(0.17, 0.78, ch_plot)
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.SetTextSize(0.058)
    Label_channel.Draw("same")

    for num in range(len(hists)):
        legend.AddEntry(hists[num], Fnames[num], 'ep')
    legend.Draw("same")

    pad1.Update()

    pad2.cd()
    dummy_ratio = hists[0].Clone()
    dummy_ratio.SetTitle("")
    dummy_ratio.SetMarkerStyle(20)
    dummy_ratio.SetMarkerSize(1.2)
    dummy_ratio.SetLineWidth(2)
    dummy_ratio.GetXaxis().SetTitle(varname)
    # dummy_ratio.GetXaxis().CenterTitle()
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
    dummy_ratio.GetYaxis().SetRangeUser(0.91,1.06)
    if ('njet' in var):
        dummy_ratio.GetXaxis().SetNdivisions(6)
    if ('nbjet' in var):
        dummy_ratio.GetXaxis().SetNdivisions(4)
    dummy_ratio.Divide(hists[1])
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Ratio')
    dummy_ratio.Draw('E1')
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder + '/' + year):
        os.makedirs(folder  + '/' + year)
    if not os.path.exists(folder + '/' + year + '/' + c):
        os.makedirs(folder + '/' + year + '/' + c)
    if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch):
        os.makedirs(folder + '/' + year + '/' + c + '/' + ch)
    canvas.Print(folder + '/' + year + '/' + c + '/' + ch + '/' + var + ".pdf")
    del canvas
    gc.collect()

def PlotSF(hist, ch = "channel", year = '2016', varnames = "v"):
    folder = 'ScaleFactor'
    ROOT.gStyle.SetPaintTextFormat("1.3f")
    dummy = hist.Clone()
    canvas = ROOT.TCanvas(year+ch,year+ch,50,50,865,750)
    # canvas.SetTopMargin(0.12)
    canvas.SetBottomMargin(0.12)
    canvas.SetLeftMargin(0.12)
    canvas.SetRightMargin(0.08)
    canvas.cd()
    dummy.GetXaxis().SetTitle(varnames[0])
    dummy.GetXaxis().SetNoExponent()
    dummy.GetXaxis().SetTitleOffset(1.3)
    dummy.GetYaxis().SetTitle(varnames[1])
    dummy.GetYaxis().SetNoExponent()
    dummy.GetZaxis().SetRangeUser(0.96,1)
    dummy.Draw("TEXTE  COL")
    label_cms = "CMS"
    Label_cms = ROOT.TLatex(0.13, 0.912, label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.SetTextSize(0.05)
    Label_cms.Draw()
    label_cms1 = "Work in progress"
    Label_cms1 = ROOT.TLatex(0.225, 0.912, label_cms1)
    Label_cms1.SetNDC()
    Label_cms1.SetTextSize(0.04)
    Label_cms1.SetTextFont(52)
    Label_cms1.Draw()
    Label_year = ROOT.TLatex(0.835,0.912,year)
    if 'APV' in year:
        Label_year = ROOT.TLatex(0.775,0.912,year)
    Label_year.SetNDC()
    Label_year.SetTextSize(0.04)
    Label_year.SetTextFont(42)
    Label_year.Draw()
    label_SF = "Trigger Scale Factor"
    Label_SF = ROOT.TLatex(0.16, 0.82, label_SF)
    Label_SF.SetNDC()
    Label_SF.SetTextSize(0.04)
    Label_SF.SetTextFont(42)
    Label_SF.Draw()
    label_ch = "ee"
    if ch == 'emu':
       label_ch = "e#mu"
    elif ch == 'mue':
       label_ch = "#mue"
    else:
       label_ch = "#mu#mu"
    Label_ch = ROOT.TLatex(0.16, 0.79, label_ch)
    Label_ch.SetNDC()
    Label_ch.SetTextSize(0.04)
    Label_ch.SetTextFont(42)
    Label_ch.Draw()
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder + '/' + year):
        os.makedirs(folder  + '/' + year)
    canvas.Print(folder + '/' + year + '/' + ch + "_SF2D.pdf")
    del canvas
    gc.collect()


