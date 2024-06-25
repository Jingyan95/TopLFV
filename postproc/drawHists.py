import os
import sys
from common import *
from plotFunctions import plot1DStack, plot2D, plotSummary


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="StackHist")
ARGS = parser.parse_args()
YEARS = []
for year in YEARS_RUN2:
    if ARGS.YEAR==year or ARGS.YEAR=="RunII":
        YEARS.append(year)
if len(ARGS.OUTPATH)>0: ARGS.FOLDER = ARGS.OUTPATH+"/"+ARGS.FOLDER


# Read in histograms
HistAddress = os.path.dirname(sys.path[0])+"/hists"
if len(ARGS.HISTPATH)>0: HistAddress += "/"+ARGS.HISTPATH
files = {} # Keeps from losing "connection" to histograms
H1 = {}
H2 = {}
for year in YEARS:
    for sample in SAMPLES:
        fname = HistAddress+"/"+year+"_"+sample+".root"
        print("Opening "+fname)
        files[year+"_"+sample] = ROOT.TFile.Open(fname)
        for charge in CHARGES:
            for channel in CHANNELS:
                for region in REGIONS:
                    for domain in DOMAINS:
                        for var in VARS1D:
                            hkey = charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            hname = year+"_"+sample+"_"+hkey
                            H1[hname] = files[year+"_"+sample].Get(hkey).Clone()
                            H1[hname].SetBinContent(1, H1[hname].GetBinContent(0)+H1[hname].GetBinContent(1))
                            H1[hname].SetBinContent(H1[hname].GetXaxis().GetNbins(),
                                H1[hname].GetBinContent(H1[hname].GetXaxis().GetNbins())+H1[hname].GetBinContent(H1[hname].GetXaxis().GetNbins()+1))
                            # Set negative event counts due to NLO low statistics to 0
                            for i in range(1, H1[hname].GetNbinsX()+1):
                                if H1[hname].GetBinContent(i)<0.0:
                                    H1[hname].SetBinContent(i, 0.0)
                                    H1[hname].SetBinError(i, 0.0)
                        for var in VARS2D:
                            hkey = charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            hname = year+"_"+sample+"_"+hkey
                            H2[hname] = files[year+"_"+sample].Get(hkey).Clone()
                            # Underflow and overflow
                            for i in range(1, H2[hname].GetNbinsX()+1):
                                H2[hname].SetBinContent(i, 1, H2[hname].GetBinContent(i, 0)+H2[hname].GetBinContent(i, 1))
                                H2[hname].SetBinContent(i, H2[hname].GetNbinsY(),
                                    H2[hname].GetBinContent(i, H2[hname].GetNbinsY())+H2[hname].GetBinContent(i, H2[hname].GetNbinsY()+1))
                            for i in range(1, H2[hname].GetNbinsY()+1):
                                H2[hname].SetBinContent(1, i, H2[hname].GetBinContent(0, i)+H2[hname].GetBinContent(1, i))
                                H2[hname].SetBinContent(H2[hname].GetNbinsX(), i,
                                    H2[hname].GetBinContent(H2[hname].GetNbinsX(), i)+H2[hname].GetBinContent(H2[hname].GetNbinsX()+1, i))
                            # Set negative event counts due to NLO low statistics to 0
                            for i in range(1, H2[hname].GetNbinsX()+1):
                                for j in range(1, H2[hname].GetNbinsY()+1):
                                    if H2[hname].GetBinContent(i, j)<0.0:
                                        H2[hname].SetBinContent(i, j, 0.0)
                                        H2[hname].SetBinError(i, j, 0.0)


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


for year in YEARS:
    for charge in CHARGES:
        for iChannel, channel in enumerate(CHANNELS):
            for iRegion, region in enumerate(REGIONS):
                # Make 1D variable plots
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
                for iVar, var in enumerate(VARS2D):
                    for iDomain, domain in enumerate(DOMAINS):
                        for iSample, sample in enumerate(SAMPLES):
                            hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            plot2D(H2[hkey], VARS2D_NAME[iVar][0], VARS2D_NAME[iVar][1], "Events", True,
                                ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge+"/"+channel+"/"+var+"_"+sample)

# Make summary plots
for year in YEARS:
    for iRegion, region in enumerate(REGIONS):
        for iDomain, domain in enumerate(DOMAINS):
            H = []
            HSignal = []
            for iSample, sample in enumerate(SAMPLES):
                hkey = year+"_"+sample+"_OS_emu_"+region+"_"+domain+"_subSR"
                subSR = H1[hkey].Clone()
                for charge in CHARGES:
                    for channel in CHANNELS:
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
