import argparse
import os
import sys
import uproot
from commonConfig import *
from plotFunctions import plot1D
# from plotFunctions import plot1D, plot2D


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="FakeFactors")
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
                        for var in VARS1DFF:
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
    for ff in FF:
        if not os.path.exists(ARGS.FOLDER):
            os.makedirs(ARGS.FOLDER)
        if not os.path.exists(ARGS.FOLDER+"/"+year):
            os.makedirs(ARGS.FOLDER+"/"+year)
        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+ff):
            os.makedirs(ARGS.FOLDER+"/"+year+"/"+ff)


# Do fake factor estimation
for year in YEARS:
    for iCut in range(len(FF)):
        for iVar, var in enumerate(VARS1DFF):
            hists = []
            labels = []
            for charge in CHARGES:
                for channel in CHANNELS:
                    x1 = X_CUTS[iCut][0]
                    x2 = X_CUTS[iCut][1] # Signal
                    y1 = Y_CUTS[iCut][0] # Signal
                    y2 = Y_CUTS[iCut][1]

                    # ABCD regions defined in slide 17 here:
                    # https://indico.cern.ch/event/1298853/contributions/5519537/subcontributions/437004/attachments/2694688/4676531/2023.8.4%20—%20NEU%20CMS%20Meeting%20Top%20LFV.pdf

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

                    # Calculate fake factors
                    ff.Divide(denom);
                    ff.SetName(year+"_"+charge+"_"+channel+"_"+var+"_ff")

                    hists.append(ff)
                    labels.append(charge+"-"+channel)

            plot1D(year, hists, labels, VARS1DFF_NAME[iVar], "Fake Factor", "", "",
                "2#ell+#tau, "+FF_LABELS[iCut], False, ARGS.FOLDER+"/"+year+"/"+FF[iCut]+"/"+var)

        # for iVar, var in enumerate(VARS2DFF):
        #     TODO
