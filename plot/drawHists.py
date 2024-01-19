import argparse
import os
import sys
import uproot
import numpy as np
import cmsstyle as CMS
import ROOT
import gc


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018"]
SAMPLES = ["Data", "TX", "VV", "DY", "TT"]
SAMPLES_NAME = ["Data", r"t\bar{t}+X", "VV(V)", "DY/ZZ", r"t\bar{t}/WW"]
CHARGES = ["OS", "SS"]
CHANNELS = ["ee", "emu", "mumu"]
CHANNELS_NAME = [r"ee\tau_{h}", r"e\mu\tau_{h}", r"\mu\mu\tau_{h}"]
REGIONS = ["ll", "llStl300", "llMetg20Jetgeq1B0"]
REGIONS_NAME = [
    ("No cuts", ""),
    (r"S_{T} < 300 GeV (CR)", ""),
    (r"p_{T}^{miss} > 20 GeV, njet #geq 1,", "nbjet = 0 (CR)")]
VARS = ["geqTightTa", "geqTightFakeTa", "lTightTa", "lTightFakeTa"]
VARS_NAME = [r"\geq Tight Tau", r"\geq Tight Tau", r"< Tight Tau", r"< Tight Tau"]
DIFFS = ["vsPt", "vsEta", "vsPt_vsEta"]
DIFFS_NAME_1D = [r"Tau p_{T}", r"Tau \eta"]
DIFFS_NAME_2D = [(r"Tau p_{T}", r"Tau \eta")]
MARKERS = [8, 23, 22, 21, 34, 33]
COLORS = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kViolet, ROOT.kOrange+3]
PLOT_LABEL = "Work in Progress"

def getLumi(year):
    if year=="2016APV": return "19.5"
    elif year=="2016": return "16.8"
    elif year=="2017": return "41.5"
    elif year=="2018": return "59.8"
    return "138"


# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="2016")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--s", dest="SQUARE", default=True)
parser.add_argument("--f", dest="FOLDER", default="StackHist")
ARGS = parser.parse_args()
YEARS = []
for iYear, year in enumerate(YEARS_RUN2):
    if ARGS.YEAR == year or ARGS.YEAR == "RunII":
        YEARS.append(YEARS_RUN2[iYear])
square = CMS.kSquare
if not ARGS.SQUARE: square = CMS.kRectangular


# read in histograms
HistAddress = os.path.dirname(sys.path[0])+"/hists"
if len(ARGS.HISTPATH)>0: HistAddress += "/"+ARGS.HISTPATH
h = {}
for year in YEARS:
    for sample in SAMPLES:
        fname = HistAddress + "/" + year + "_" + sample + ".root"
        print("Opening " + fname)
        file = uproot.open(fname)
        for charge in CHARGES:
            for channel in CHANNELS:
                for region in REGIONS:
                    for var in VARS:
                        for diff in DIFFS:
                            hname = charge+"_"+channel+"_"+region+"_"+var+"_"+diff
                            temp = file[hname].to_pyroot().Clone() # TODO: what to do about overflow bin?
                            # Set negative event counts due to NLO low statistics to 0 in 1D histograms
                            if diff!="vsPt_vsEta":
                                for i in range(1, temp.GetNbinsX()+1):
                                    if temp.GetBinContent(i)<0.0:
                                        temp.SetBinContent(i, 0.0)
                                        temp.SetBinError(i, 0.0)
                            # Set negative event counts due to NLO low statistics to 0 in 2D histograms
                            else:
                                for i in range(1, temp.GetNbinsX()+1):
                                    for j in range(1, temp.GetNbinsY()+1):
                                        if temp.GetBinContent(i, j)<0.0:
                                            temp.SetBinContent(i, j, 0.0)
                                            temp.SetBinError(i, j, 0.0)
                            h[year+"_"+sample+"_"+hname] = temp
        file.close()


# create save folders
for year in YEARS:
    for region in REGIONS:
        for diff in DIFFS:
            for charge in CHARGES:
                for channel in CHANNELS:
                    for iVar in range(0, len(VARS), 2):
                        if not os.path.exists(ARGS.FOLDER):
                                os.makedirs(ARGS.FOLDER)
                        if not os.path.exists(ARGS.FOLDER+"/"+year):
                            os.makedirs(ARGS.FOLDER+"/"+year)
                        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region):
                            os.makedirs(ARGS.FOLDER+"/"+year+"/"+region)
                        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff):
                            os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff)
                        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge):
                            os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge)
                        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel):
                            os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel)
                        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel+"/"+VARS[iVar]):
                            os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel+"/"+VARS[iVar])


def make1DPlot(hists, histLabels, pname, yLabel, year, iRegion, iDiff, saveDir, iVar=-1, yMax=0.0):
    CMS.SetLumi(getLumi(year))
    CMS.SetEnergy("13") # Run 2
    CMS.SetExtraText(PLOT_LABEL)

    # set negative event counts due to NLO low statistics to 0
    for iHist in range(len(hists)):
        for xBin in range(1, hists[iHist].GetNbinsX()+1):
            if hists[iHist].GetBinContent(xBin)<0.0:
                hists[iHist].SetBinContent(xBin, 0.0)
                hists[iHist].SetBinError(xBin, 0.0)

    # get x_min and x_max
    x_min = hists[0].GetBinLowEdge(1)
    x_max = hists[0].GetBinLowEdge(hists[0].GetNbinsX())+hists[0].GetBinWidth(hists[0].GetNbinsX())
    # get y_min and y_max
    y_min = 0.0
    if yMax>0.0:
        y_max = yMax
    else:
        y_max = -1.0
        for hist in hists:
            y_max = max(y_max, hist.GetMaximum())
        y_max = 1.6*y_max

    canv = CMS.cmsCanvas(pname,
        x_min, x_max, y_min, y_max, DIFFS_NAME_1D[iDiff], yLabel,
        square=square, iPos=0)

    for iHist, hist in enumerate(hists):
        CMS.cmsDraw(hist, "HIST E", marker=MARKERS[iHist], mcolor=COLORS[iHist],
            lwidth=2, lcolor=COLORS[iHist], fcolor=0)

    # draw legend
    if square:
        leg = CMS.cmsLeg(0.59, 0.71, 0.74, 0.89, textSize=0.04)
    else:
        leg = CMS.cmsLeg(0.66, 0.7, 0.78, 0.88, textSize=0.05)
    for iHist, hist in enumerate(hists):
        leg.AddEntry(hist, histLabels[iHist], "PL")

    # add region (+domain) labels
    if square:
        legLabelTop = CMS.cmsLeg(0.18, 0.83, 0.5, 0.89, textSize=0.04)
        legLabelMiddle = CMS.cmsLeg(0.18, 0.77, 0.5, 0.83, textSize=0.04)
        legLabelBottom = CMS.cmsLeg(0.18, 0.71, 0.5, 0.77, textSize=0.04)
    else:
        legLabelTop = CMS.cmsLeg(0.15, 0.82, 0.5, 0.88, textSize=0.05)
        legLabelMiddle = CMS.cmsLeg(0.15, 0.76, 0.5, 0.82, textSize=0.05)
        legLabelBottom = CMS.cmsLeg(0.15, 0.7, 0.5, 0.76, textSize=0.05)
    if iVar>=0: CMS.cmsHeader(legLabelTop, VARS_NAME[iVar], textSize=0.04)
    CMS.cmsHeader(legLabelMiddle, REGIONS_NAME[iRegion][0], textSize=0.04)
    CMS.cmsHeader(legLabelBottom, REGIONS_NAME[iRegion][1], textSize=0.04)

    CMS.SaveCanvas(canv, saveDir+"/"+pname+".pdf")
    del canv
    gc.collect()


def make2DPlot(hist, pname, year, iDiff, saveDir):
    CMS.SetLumi(getLumi(year))
    CMS.SetEnergy("13") # Run 2
    CMS.SetExtraText(PLOT_LABEL)

    # set negative event counts due to NLO low statistics to 0
    for xBin in range(1, hist.GetNbinsX()+1):
        for yBin in range(1, hist.GetNbinsY()+1):
            if hist.GetBinContent(xBin, yBin)<0.0:
                hist.SetBinContent(xBin, yBin, 0.0)
                hist.SetBinError(xBin, yBin, 0.0)

    # get min and max
    x_min = hist.GetXaxis().GetBinLowEdge(1)
    x_max = hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX())+hist.GetXaxis().GetBinWidth(hist.GetNbinsX())
    y_min = hist.GetYaxis().GetBinLowEdge(1)
    y_max = hist.GetYaxis().GetBinLowEdge(hist.GetNbinsY())+hist.GetYaxis().GetBinWidth(hist.GetNbinsY())

    canv = CMS.cmsCanvas(pname,
        x_min, x_max, y_min, y_max, DIFFS_NAME_2D[iDiff][0], DIFFS_NAME_2D[iDiff][1],
        square=square, iPos=0)

    CMS.cmsDraw(hist, "COLZ TEXT45 E")

    CMS.SaveCanvas(canv, saveDir+"/"+pname+".pdf")
    del canv
    gc.collect()


# fake factors
for year in YEARS:
    for iRegion, region in enumerate(REGIONS):
        if region=="ll": continue # this region is blinded
        for iDiff, diff in enumerate(DIFFS):
            if diff!="vsPt_vsEta": # 1D
                hists = []
                labels = []
                for charge in CHARGES:
                    for iChannel, channel in enumerate(CHANNELS):
                        hname = year + "_Data_" + charge + "_" + channel + "_" + region + "_geqTightTa_" + diff
                        fakeFactor = h[hname].Clone()
                        hname = year + "_TX_" + charge + "_" + channel + "_" + region + "_geqTightTa_" + diff
                        fakeFactor.Add(h[hname].Clone(), -1.0)
                        hname = year + "_VV_" + charge + "_" + channel + "_" + region + "_geqTightTa_" + diff
                        fakeFactor.Add(h[hname].Clone(), -1.0)
                        for i in range(1, fakeFactor.GetNbinsX() + 1): # Set negative event counts to 0
                            if fakeFactor.GetBinContent(i) < 0.0:
                                fakeFactor.SetBinContent(i, 0.0)
                                fakeFactor.SetBinError(i, 0.0)
                        hname = year + "_Data_" + charge + "_" + channel + "_" + region + "_lTightTa_" + diff
                        denominator = h[hname].Clone()
                        hname = year + "_TX_" + charge + "_" + channel + "_" + region + "_lTightTa_" + diff
                        denominator.Add(h[hname].Clone(), -1.0)
                        hname = year + "_VV_" + charge + "_" + channel + "_" + region + "_lTightTa_" + diff
                        denominator.Add(h[hname].Clone(), -1.0)
                        for i in range(1, denominator.GetNbinsX() + 1): # Set negative event counts to 0
                            if denominator.GetBinContent(i) < 0.0:
                                denominator.SetBinContent(i, 0.0)
                                denominator.SetBinError(i, 0.0)
                        fakeFactor.Divide(denominator)
                        hists.append(fakeFactor)
                        labels.append(charge+", "+CHANNELS_NAME[iChannel])
                make1DPlot(hists, labels, "1DFakeFactors", "Fake Factors", year, iRegion, iDiff,
                    ARGS.FOLDER+"/"+year+"/"+region+"/"+diff)
            else: # 2D
                for charge in CHARGES:
                    for iChannel, channel in enumerate(CHANNELS):
                        hname = year + "_Data_" + charge + "_" + channel + "_" + region + "_geqTightTa_" + diff
                        fakeFactor = h[hname].Clone()
                        hname = year + "_TX_" + charge + "_" + channel + "_" + region + "_geqTightTa_" + diff
                        fakeFactor.Add(h[hname].Clone(), -1.0)
                        hname = year + "_VV_" + charge + "_" + channel + "_" + region + "_geqTightTa_" + diff
                        fakeFactor.Add(h[hname].Clone(), -1.0)
                        for i in range(1, fakeFactor.GetNbinsX()+1):
                            for j in range(1, fakeFactor.GetNbinsY()+1):
                                if fakeFactor.GetBinContent(i, j)<0.0:
                                    fakeFactor.SetBinContent(i, j, 0.0)
                                    fakeFactor.SetBinError(i, j, 0.0)
                        hname = year + "_Data_" + charge + "_" + channel + "_" + region + "_lTightTa_" + diff
                        denominator = h[hname].Clone()
                        hname = year + "_TX_" + charge + "_" + channel + "_" + region + "_lTightTa_" + diff
                        denominator.Add(h[hname].Clone(), -1.0)
                        hname = year + "_VV_" + charge + "_" + channel + "_" + region + "_lTightTa_" + diff
                        denominator.Add(h[hname].Clone(), -1.0)
                        for i in range(1, denominator.GetNbinsX()+1):
                            for j in range(1, denominator.GetNbinsY()+1):
                                if denominator.GetBinContent(i, j)<0.0:
                                    denominator.SetBinContent(i, j, 0.0)
                                    denominator.SetBinError(i, j, 0.0)
                        fakeFactor.Divide(denominator)
                        make2DPlot(fakeFactor, "2DFakeFactors", year, iDiff-len(DIFFS_NAME_1D),
                            ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel)

# fake tau purity
for iYear, year in enumerate(YEARS):
    for iDiff, diff in enumerate(DIFFS):
        for iRegion, region in enumerate(REGIONS):
            for charge in CHARGES:
                for iChannel, channel in enumerate(CHANNELS):
                    for iVar in range(0, len(VARS), 2):
                        if diff!="vsPt_vsEta": # 1D
                            hists = []
                            labels = []
                            for iSample, sample in enumerate(SAMPLES):
                                if sample=="Data": continue
                                hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+VARS[iVar+1]+"_"+diff
                                purity = h[hkey].Clone()
                                hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+VARS[iVar]+"_"+diff
                                denominator = h[hkey].Clone()
                                purity.Divide(denominator)
                                hists.append(purity)
                                labels.append(SAMPLES_NAME[iSample]+", "+charge+", "+CHANNELS_NAME[iChannel])
                            make1DPlot(hists, labels, "1DPurity", "Fake Tau Purity", year, iRegion, iDiff,
                                ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel+"/"+VARS[iVar], iVar, 1.6)
                        else: # 2D
                            for iSample, sample in enumerate(SAMPLES):
                                if sample=="Data": continue
                                hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+VARS[iVar+1]+"_"+diff
                                purity = h[hkey].Clone()
                                hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+VARS[iVar]+"_"+diff
                                denominator = h[hkey].Clone()
                                purity.Divide(denominator)
                                make2DPlot(purity, "2DPurity"+sample, year, iDiff-len(DIFFS_NAME_1D),
                                    ARGS.FOLDER+"/"+year+"/"+region+"/"+diff+"/"+charge+"/"+channel+"/"+VARS[iVar])
