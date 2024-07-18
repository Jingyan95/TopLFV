import os
import sys
from common import *
from plotFunctions import plot1DStack, plot2D, plotSummary, plot1D


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
    fname = HistAddress+"/"+year+"_Hists1D.root"
    print("Opening "+fname)
    files[year] = ROOT.TFile.Open(fname)
    for sample in SAMPLES:
        for charge in CHARGES:
            for channel in CHANNELS:
                for region in REGIONS:
                    for var in VARS1D:
                        hkey = sample+"_"+charge+"_"+channel+"_"+region+"_"+var
                        hname = year+"_"+hkey
                        H1[hname] = files[year].Get(hkey).Clone()
                        H1[hname].SetBinContent(1, H1[hname].GetBinContent(0)+H1[hname].GetBinContent(1))
                        H1[hname].SetBinContent(H1[hname].GetXaxis().GetNbins(),
                            H1[hname].GetBinContent(H1[hname].GetXaxis().GetNbins())+H1[hname].GetBinContent(H1[hname].GetXaxis().GetNbins()+1))
                        # Set negative event counts due to NLO low statistics to 0
                        for i in range(1, H1[hname].GetNbinsX()+1):
                            if H1[hname].GetBinContent(i)<0.0:
                                H1[hname].SetBinContent(i, 0.0)
                                H1[hname].SetBinError(i, 0.0)

# Create save folders
for year in YEARS:
    for region in REGIONS:
        for charge in CHARGES:
            for channel in CHANNELS:
                if not os.path.exists(ARGS.FOLDER):
                    os.makedirs(ARGS.FOLDER)
                if not os.path.exists(ARGS.FOLDER+"/"+year):
                    os.makedirs(ARGS.FOLDER+"/"+year)
                if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region):
                    os.makedirs(ARGS.FOLDER+"/"+year+"/"+region)
                if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+charge):
                    os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+charge)
                if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel):
                    os.makedirs(ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel)


for year in YEARS:
    for charge in CHARGES:
        for iChannel, channel in enumerate(CHANNELS):
            for iRegion, region in enumerate(REGIONS):
                # Make 1D variable plots
                for iVar, var in enumerate(VARS1D):
                    hists = []
                    for iSample, sample in enumerate(SAMPLES):
                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+var
                        hists.append(H1[hkey])
                    plot1DStack(hists, year, charge, iChannel, iRegion, VARS1D_NAME[iVar], var,
                        charge+", "+CHANNELS_NAME[iChannel],
                        ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel)

# Labels = ["TX", "VV", "DY", "TT", "Overall"]  
# vars = ["lep1Pt", "lep2Pt", "lep3Pt", "lep1Eta", "lep2Eta", "lep3Eta"]  
# varsName = ["Fake leading lepton p_{T} [GeV]",
#             "Fake sub-leading lepton p_{T} [GeV]",
#             "Fake tau lepton p_{T} [GeV]",
#             "Fake leading lepton |#eta|",
#             "Fake sub-leading lepton |#eta|",
#             "Fake tau |#eta|"]                   

# for year in YEARS:
#     for charge in CHARGES:
#         for iChannel, channel in enumerate(CHANNELS):
#             for iRegion, region in enumerate(REGIONS):
#                 for iVar, var in enumerate(vars):
#                     hists = []
#                     histN = []
#                     histD = []
#                     for iSample, sample in enumerate(SAMPLES):
#                         if ('Data' in sample) or ('LFV' in sample):
#                             continue
#                         hkey1 = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+var
#                         hkey2 = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_F"+var
#                         h = H1[hkey2].Clone()
#                         h.Divide(H1[hkey1])
#                         hists.append(h)
#                         if (len(histN)<1):
#                             histN.append(H1[hkey2])
#                             histD.append(H1[hkey1])
#                         else:
#                             histN[0]+=H1[hkey2]
#                             histD[0]+=H1[hkey1]
#                     h = histN[0].Clone()
#                     h.Divide(histD[0])
#                     hists.append(h)
#                     plot1D(year, hists, Labels, varsName[iVar], "Fake rate", Labels, Labels,charge+", "+CHANNELS_NAME[iChannel],False,ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/"+var)

  
