import argparse
import os
import sys
import uproot
from commonConfig import *
from plotFunctions import plot1DStack, plotSummary
# from plotFunctions import plot1DStack, plot2D, plotSummary


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="StackHist")
ARGS = parser.parse_args()
YEARS = []
for iYear, year in enumerate(YEARS_RUN2):
    if ARGS.YEAR == year or ARGS.YEAR == "RunII":
        YEARS.append(YEARS_RUN2[iYear])
if len(ARGS.OUTPATH)>0: ARGS.FOLDER = ARGS.OUTPATH+"/"+ARGS.FOLDER


# Read in histograms
HistAddress = os.path.dirname(sys.path[0])+"/hists"
if len(ARGS.HISTPATH)>0: HistAddress += "/"+ARGS.HISTPATH
H1 = {}
# H2 = {}
for year in YEARS:
    for sample in SAMPLES:
        fname = HistAddress+"/"+year+"_"+sample+".root"
        print("Opening "+fname)
        file = uproot.open(fname)
        for charge in CHARGES:
            for channel in CHANNELS:
                for region in REGIONS:
                    for domain in DOMAINS:
                        for var in VARS1D:
                            hname = charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            temp = file[hname].to_pyroot().Clone()
                            # Underflow and overflow
                            temp.SetBinContent(1, temp.GetBinContent(0)+temp.GetBinContent(1))
                            temp.SetBinContent(temp.GetXaxis().GetNbins(),
                                temp.GetBinContent(temp.GetXaxis().GetNbins())+temp.GetBinContent(temp.GetXaxis().GetNbins()+1))
                            # Set negative event counts due to NLO low statistics to 0
                            for i in range(1, temp.GetNbinsX()+1):
                                if temp.GetBinContent(i)<0.0:
                                    temp.SetBinContent(i, 0.0)
                                    temp.SetBinError(i, 0.0)
                            # Save histogram
                            H1[year+"_"+sample+"_"+hname] = temp
        file.close()


# Create save folders
for year in YEARS:
    for region in REGIONS:
        for domain in DOMAINS:
            for charge in CHARGES:
                for channel in CHANNELS:
                    if not os.path.exists(ARGS.FOLDER):
                        os.makedirs(ARGS.FOLDER)
                    if not os.path.exists(ARGS.FOLDER+"/"+year):
                        os.makedirs(ARGS.FOLDER+"/"+year)
                    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region):
                        os.makedirs(ARGS.FOLDER+"/"+year+"/"+region)
                    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+domain):
                        os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+domain)
                    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge):
                        os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge)
                    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge+"/"+channel):
                        os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge+"/"+channel)


# Make 1D variable plots
for year in YEARS:
    for charge in CHARGES:
        for iChannel, channel in enumerate(CHANNELS):
            for iRegion, region in enumerate(REGIONS):
                for iVar, var in enumerate(VARS1D):
                    if var=="subSR": continue
                    for iDomain, domain in enumerate(DOMAINS):
                        hists = []
                        for iSample, sample in enumerate(SAMPLES):
                            hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            hists.append(H1[hkey])
                        plot1DStack(hists, year, charge, iChannel, iRegion, VARS1D_NAME[iVar], var,
                            charge+", "+CHANNELS_NAME[iChannel]+", "+DOMAINS_NAME[iDomain],
                            ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge+"/"+channel)

# Make 2D variable plots
# TODO

# Make summary plots
for year in YEARS:
    for iRegion, region in enumerate(REGIONS):
        for iDomain, domain in enumerate(DOMAINS):
            H = []
            HSignal = []
            for iSample, sample in enumerate(SAMPLES):
                hkey = year+"_"+sample+"_OS_ee_"+region+"_"+domain+"_subSR"
                subSR = H1[hkey].Clone()
                for charge in CHARGES:
                    for channel in CHANNELS:
                        if charge=="OS" and channel=="ee": continue
                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+domain+"_subSR"
                        subSR.Add(H1[hkey].Clone(), 1.0)
                subSR.SetFillColor(COLORS[iSample])
                if "LFV" in sample:
                    subSR.SetLineColor(COLORS[iSample])
                    HSignal.append(subSR)
                else:
                    subSR.SetLineColor(COLORS[0])
                    H.append(subSR)
            plotSummary(H, HSignal, SAMPLES_NAME_SUMMARY, year, iRegion, region, iDomain,
                ARGS.FOLDER+"/"+year+"/"+region+"/"+domain)
