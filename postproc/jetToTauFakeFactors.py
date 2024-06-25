import argparse
import os
import sys
from common import *
from plotFunctions import plot1D, plot2D


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="FakeFactors")
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
                        for var in VARS1DFF:
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
                        for var in VARS2DFF:
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
    for cut in X_CUTS:
        if not os.path.exists(ARGS.FOLDER):
            os.makedirs(ARGS.FOLDER)
        if not os.path.exists(ARGS.FOLDER+"/"+year):
            os.makedirs(ARGS.FOLDER+"/"+year)
        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+cut[0]):
            os.makedirs(ARGS.FOLDER+"/"+year+"/"+cut[0])

# Open output ROOT files
DataAddress = os.path.dirname(sys.path[0])+"/data/TAU"
fout = {}
for year in YEARS:
    if year=="All": continue
    # fout[year+"_taPtFFBin"] = ROOT.TFile.Open(DataAddress+"/"+year+"TauID_FF_pt_DeepTau2017v2p1VSjet.root", "RECREATE")
    # fout[year+"_taEtaFFBin"] = ROOT.TFile.Open(DataAddress+"/"+year+"TauID_FF_eta_DeepTau2017v2p1VSjet.root", "RECREATE")
    fout[year+"_taPtVsEta"] = ROOT.TFile.Open(DataAddress+"/"+year+"TauID_FF_ptVsEta_DeepTau2017v2p1VSjet.root", "RECREATE")


# Do fake factor estimation
# ABCD regions defined in slide 17 here:
# https://indico.cern.ch/event/1298853/contributions/5519537/subcontributions/437004/attachments/2694688/4676531/2023.8.4%20—%20NEU%20CMS%20Meeting%20Top%20LFV.pdf
for year in YEARS:
    for iCut in range(len(FF_LABELS)):
        x1 = X_CUTS[iCut][0]
        x2 = X_CUTS[iCut][1] # Signal
        y1 = Y_CUTS[iCut][0] # Signal
        y2 = Y_CUTS[iCut][1]

        for iVar, var in enumerate(VARS1DFF):
            hists = []
            labels = []
            # fout[year+"_"+var].cd()
            for charge in CHARGES:
                for channel in CHANNELS:
                    # Get data and subtract "real" taus
                    regA = charge+"_"+channel+"_"+x1+"_"+y1+"_"+var
                    ff = H1[year+"_Data_"+regA].Clone()
                    ff.Add(H1[year+"_TX_"+regA].Clone(), -1.0)
                    ff.Add(H1[year+"_VV_"+regA].Clone(), -1.0)
                    for i in range(1, ff.GetNbinsX()+1):
                        if ff.GetBinContent(i)<0.0:
                            ff.SetBinContent(i, 0.0)
                            ff.SetBinError(i, 0.0)
                    regC = charge+"_"+channel+"_"+x1+"_"+y2+"_"+var
                    denom = H1[year+"_Data_"+regC].Clone()
                    denom.Add(H1[year+"_TX_"+regC].Clone(), -1.0)
                    denom.Add(H1[year+"_VV_"+regC].Clone(), -1.0)
                    for i in range(1, denom.GetNbinsX()+1):
                        if denom.GetBinContent(i)<0.0:
                            denom.SetBinContent(i, 0.0)
                            denom.SetBinError(i, 0.0)
                    hname = charge+"_"+channel+"_"+var+"_ff_"+x1
                    ff.Divide(denom) # Calculate fake factors
                    ff.SetName(hname)
                    # ff.Write() # Write to ROOT file
                    hists.append(ff) # Add histogram to plot
                    labels.append(charge+"-"+channel)
            plot1D(year, hists, labels, VARS1DFF_NAME[iVar], "Fake Factor", "", "",
                "2l+#tau, "+FF_LABELS[iCut], False, ARGS.FOLDER+"/"+year+"/"+x1+"/"+var)

        for iVar, var in enumerate(VARS2DFF):
            if year!="All": fout[year+"_"+var].cd()
            for charge in CHARGES:
                for channel in CHANNELS:
                    hname = charge+"_"+channel+"_"+var+"_ff_"+x1
                    # Get data and subtract "real" taus
                    regA = charge+"_"+channel+"_"+x1+"_"+y1+"_"+var
                    ff = H2[year+"_Data_"+regA].Clone()
                    ff.Add(H2[year+"_TX_"+regA].Clone(), -1.0)
                    ff.Add(H2[year+"_VV_"+regA].Clone(), -1.0)
                    ff.SetName(hname)
                    if ff.GetEntries()==0:
                        ff.Write()
                        continue
                    for i in range(1, ff.GetNbinsX()+1):
                        for j in range(1, ff.GetNbinsY()+1):
                            if ff.GetBinContent(i, j)<0.0:
                                ff.SetBinContent(i, j, 0.0)
                                ff.SetBinError(i, j, 0.0)
                    regC = charge+"_"+channel+"_"+x1+"_"+y2+"_"+var
                    denom = H2[year+"_Data_"+regC].Clone()
                    denom.Add(H2[year+"_TX_"+regC].Clone(), -1.0)
                    denom.Add(H2[year+"_VV_"+regC].Clone(), -1.0)
                    for i in range(1, denom.GetNbinsX()+1):
                        for j in range(1, denom.GetNbinsY()+1):
                            if denom.GetBinContent(i, j)<0.0:
                                denom.SetBinContent(i, j, 0.0)
                                denom.SetBinError(i, j, 0.0)
                    ff.Divide(denom) # Calculate fake factors
                    if year!="All": ff.Write() # Write to ROOT file
                    plot2D(ff, VARS2DFF_NAME[iVar][0], VARS2DFF_NAME[iVar][1], "Fake Factor", False,
                        ARGS.FOLDER+"/"+year+"/"+x1+"/"+charge+"_"+channel+"_"+var)
