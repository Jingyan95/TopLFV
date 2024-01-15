import math
import gc
import ROOT
import os
import array
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetEndErrorSize(0)
from array import array
from ROOT import TGaxis
import gc
TGaxis.SetMaxDigits(2)


def StackHist(hists, SignalHists, Fnames, c = "charge", ch = "channel", reg = "region",
              regName = ["region", ""], dom = "domain", domName = "domain name",
              year = '2016', var = "sample", varname = "v"):

    folder = 'StackHist'
    hs = ROOT.THStack("hs", "")
    for num in range(1, len(hists)):
        hs.Add(hists[num])

    binwidth = array('d')
    bincenter = array('d')
    yvalue = array('d')
    yerrup = array('d')
    yerrdown = array('d')
    T = hists[0].Clone()
    for b in range(T.GetNbinsX()):
        if T.GetBinContent(b + 1) > 0:
            binwidth.append(0)
            bincenter.append(T.GetBinCenter(b + 1))
            yvalue.append(T.GetBinContent(b + 1))
            yerrup.append(T.GetBinError(b + 1))
            yerrdown.append(T.GetBinError(b + 1))
    if len(bincenter) > 0:
        dummy = ROOT.TGraphAsymmErrors(len(bincenter), bincenter, yvalue, binwidth, binwidth, yerrdown, yerrup)
    else:
        dummy = ROOT.TGraphAsymmErrors()

    canvas = ROOT.TCanvas(year + c + ch + reg + dom + var, year + c + ch + reg + dom + var, 50, 50, 865, 780)
    canvas.SetGrid()
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    ROOT.gStyle.SetErrorX(0)

    legend = ROOT.TLegend(0.62, 0.69, 0.77, 0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend2 = ROOT.TLegend(0.77, 0.69, 0.92, 0.88)
    legend2.SetBorderSize(0)
    legend2.SetFillStyle(0)
    legend2.SetTextFont(42)
    legend2.SetTextSize(0.05)
    legend3 = ROOT.TLegend(0.442, 0.56, 0.78, 0.683)
    legend3.SetBorderSize(0)
    legend3.SetFillStyle(0)
    legend3.SetTextFont(42)
    legend3.SetTextSize(0.05)

    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99, 0) # Used for the hist plot
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.305, 0) # Used for the ratio plot
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
        if H > 0:
            SignalHists[H].Scale(20)
        else:
            SignalHists[H].Scale(0.5)

    y_max = 2000 * hists[0].GetMaximum()
    if y_max < 2000 * hs.GetStack().Last().GetMaximum():
        y_max = 2000 * hs.GetStack().Last().GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetLineWidth(2)
    x_min = hists[0].GetXaxis().GetBinLowEdge(1)
    x_max = hists[0].GetXaxis().GetBinLowEdge(hists[0].GetXaxis().GetNbins()) + hists[0].GetXaxis().GetBinWidth(hists[0].GetXaxis().GetNbins())

    frame = pad1.DrawFrame(x_min, 0.01, x_max, y_max)
    frame.SetTitle("")
    frame.GetYaxis().SetTitle('Events')
    frame.GetXaxis().SetLabelSize(0)
    frame.GetYaxis().SetTitleOffset(0.87)
    frame.GetYaxis().SetTitleSize(0.07)
    frame.GetYaxis().SetLabelSize(0.05)
    # frame.GetYaxis().SetNoExponent()
    pad1.Update()
    dummy.Draw("P")
    hs.Draw("histSAME")
    for H in range(len(SignalHists)):
        SignalHists[H].SetLineWidth(3)
        SignalHists[H].SetFillColor(0)
        SignalHists[H].SetLineStyle(H + 1)
        SignalHists[H].Draw("histSAME")
    dummy.Draw("PSAME")
    frame.Draw("AXISSAMEY+")
    frame.Draw("AXISSAMEX+")
    pad1.Update()

    SumofMC = hs.GetStack().Last()
    binwidth = array('d')
    bincenter = array('d')
    yvalue = array('d')
    yerrup = array('d')
    yerrdown = array('d')
    yvalueRatio = array('d')
    yerrupRatio = array('d')
    yerrdownRatio = array('d')
    for b in range(SumofMC.GetNbinsX()):
        if SumofMC.GetBinContent(b + 1) > 0:
            binwidth.append(SumofMC.GetBinWidth(b + 1) / 2)
            bincenter.append(SumofMC.GetBinCenter(b + 1))
            yvalue.append(SumofMC.GetBinContent(b + 1))
            yerrup.append(SumofMC.GetBinError(b + 1))
            yerrdown.append(SumofMC.GetBinError(b + 1))
            yvalueRatio.append(1)
            yerrupRatio.append(SumofMC.GetBinError(b + 1) / SumofMC.GetBinContent(b + 1))
            yerrdownRatio.append(SumofMC.GetBinError(b + 1) / SumofMC.GetBinContent(b + 1))
    if len(bincenter) > 0:
        error = ROOT.TGraphAsymmErrors(len(bincenter), bincenter, yvalue, binwidth, binwidth, yerrdown, yerrup)
        errorRatio = ROOT.TGraphAsymmErrors(len(bincenter), bincenter, yvalueRatio, binwidth, binwidth, yerrdownRatio, yerrupRatio)
    else:
        error = ROOT.TGraphAsymmErrors()
        errorRatio = ROOT.TGraphAsymmErrors()
    error.SetFillColor(13)
    error.SetLineColor(13)
    error.SetFillStyle(3154)
    error.SetLineWidth(4)
    error.Draw("2")

    Lumi = getLumi(year)
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
       Label_lumi = ROOT.TLatex(0.625, 0.92, Lumi + " fb^{-1} (13 TeV)")
    else:
       Label_lumi = ROOT.TLatex(0.673, 0.92, Lumi + " fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.SetTextSize(0.063)
    Label_lumi.Draw("same")
    ch_plot = ch
    if 'ee' in ch:
        if 'SS' in c:
            ch_plot = 'ee#tau_{h}'
        else:
            ch_plot = 'e#bar{e}#tau_{h}'
    if 'emu' in ch:
        if 'SS' in c:
            ch_plot = 'e#mu#tau_{h}'
        else:
            ch_plot = 'e#bar{#mu}#tau_{h}'
    if 'mumu' in ch:
        if 'SS' in c:
            ch_plot = '#mu#mu#tau_{h}'
        else:
            ch_plot = '#mu#bar{#mu}#tau_{h}'
    Label_channel = ROOT.TLatex(0.17, 0.78, ch_plot + regName[1])
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.SetTextSize(0.058)
    Label_channel.Draw("same")
    Label_region = ROOT.TLatex(0.17, 0.7, regName[0])
    Label_region.SetNDC()
    Label_region.SetTextFont(42)
    Label_region.SetTextSize(0.058)
    Label_region.Draw("same")
    Label_region2 = ROOT.TLatex(0.17, 0.62, domName)
    Label_region2.SetNDC()
    Label_region2.SetTextFont(42)
    Label_region2.SetTextSize(0.058)
    Label_region2.Draw("same")

    legend.AddEntry(dummy, Fnames[0], 'ep')
    for num in range(1, len(hists)):
        if num < (len(hists) - 2):
            legend.AddEntry(hists[num], Fnames[num], 'F')
        else:
            legend2.AddEntry(hists[num], Fnames[num], 'F')
    error.SetLineWidth(1)
    legend2.AddEntry(error, 'Stat. only', 'F')
    for H in range(len(SignalHists)):
        if H == 0:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists) + H] + " (#mu_{#scale[0.8]{ll`tu}}^{#scale[0.8]{scalar}} = 0.5)", 'L')
        else:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists) + H] + " (#mu_{#scale[0.8]{ll`tu}}^{#scale[0.8]{scalar}} = 20)", 'L')
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
    # dummy_ratio.GetXaxis().CenterTitle()
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()
    dummy_ratio.GetYaxis().SetNoExponent()
    dummy_ratio.GetXaxis().SetTitleSize(0.05 / 0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.05 / 0.3)
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
    dummy_ratio.GetYaxis().SetRangeUser(0.2, 1.8)
    if ('njet' in var):
        dummy_ratio.GetXaxis().SetNdivisions(6)
    if ('nbjet' in var):
        dummy_ratio.GetXaxis().SetNdivisions(4)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('#frac{Data}{Pred.}')
    dummy_ratio.Draw('E1')
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    errorRatio.SetFillColor(13)
    errorRatio.SetLineColor(13)
    errorRatio.SetFillStyle(3154)
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
    if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch + '/' + reg):
        os.makedirs(folder + '/' + year + '/' + c + '/' + ch + '/' + reg)
    if len(dom) > 0:
        if not os.path.exists(folder + '/' + year + '/' + c + '/' + ch + '/' + reg + '/' + dom):
            os.makedirs(folder + '/' + year + '/' + c + '/' + ch + '/' + reg + '/' + dom)
        canvas.Print(folder + '/' + year + '/' + c + '/' + ch + '/' + reg + '/' + dom + '/' + var + ".pdf")
    else:
        canvas.Print(folder + '/' + year + '/' + c + '/' + ch + '/' + reg + '/' + var + ".pdf")
    del canvas
    gc.collect()


def getLumi(year):

    if (year == '2016APV'):
        return '19.5'
    elif (year == '2016'):
        return '16.8'
    elif (year == '2017'):
        return '41.5'
    elif (year == '2018'):
        return '59.8'
    return '138'
