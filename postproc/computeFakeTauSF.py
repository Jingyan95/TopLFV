import os
import sys
from common import *
from plotFunctions import plot1DStack, plot2D, plotSummary, plot1D


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="FakeTauSF")
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
H2 = {}
for year in YEARS:
    fname = HistAddress+"/"+year+"_Hists1D.root"
    print("Opening "+fname)
    files[year] = ROOT.TFile.Open(fname)
    for sample in SAMPLES:
        for charge in CHARGES:
            for channel in CHANNELS:
                for region in REGIONS:
                    for var in VARS2D:
                        hkey = sample+"_"+charge+"_"+channel+"_"+region+"_"+var
                        hname = year+"_"+hkey
                        H2[hname] = files[year].Get(hkey).Clone()
                        # Overflow
                        for i in range(1, H2[hname].GetNbinsY()+1):
                            H2[hname].SetBinContent(H2[hname].GetNbinsX(), i,
                                H2[hname].GetBinContent(H2[hname].GetNbinsX(), i)+H2[hname].GetBinContent(H2[hname].GetNbinsX()+1, i))
                            H2[hname].SetBinContent(1, i,
                                H2[hname].GetBinContent(1, i)+H2[hname].GetBinContent(0, i))
                        for i in range(1, H2[hname].GetNbinsX()+1):
                            H2[hname].SetBinContent(i, H2[hname].GetNbinsY(),
                                H2[hname].GetBinContent(i, H2[hname].GetNbinsY())+H2[hname].GetBinContent(i, H2[hname].GetNbinsY()+1))
                            H2[hname].SetBinContent(i, 1,
                                H2[hname].GetBinContent(i, 1)+H2[hname].GetBinContent(i, 0))
            
# Create save folders
for year in YEARS:
    if not os.path.exists(ARGS.FOLDER):
        os.makedirs(ARGS.FOLDER)
    if not os.path.exists(ARGS.FOLDER+"/"+year):
        os.makedirs(ARGS.FOLDER+"/"+year)
            
for year in YEARS:   
    fileout = ROOT.TFile(year + 'FakeTauSF.root','recreate')
    for var in VARS2D:        
        ee_data_N = H2[year+"_Data_OS_ee_llOnZ_"+var].Clone()
        ee_data_N.Add(H2[year+"_TX_OS_ee_llOnZ_"+var],-1)
        ee_data_N.Add(H2[year+"_VV_OS_ee_llOnZ_"+var],-1)
        ee_data_N.Add(H2[year+"_Others_OS_ee_llOnZ_"+var],-1)
        ee_data_N.Add(H2[year+"_FakeL_OS_ee_llOnZ_"+var],-1)

        mumu_data_N = H2[year+"_Data_OS_mumu_llOnZ_"+var].Clone()
        mumu_data_N.Add(H2[year+"_TX_OS_mumu_llOnZ_"+var],-1)
        mumu_data_N.Add(H2[year+"_VV_OS_mumu_llOnZ_"+var],-1)
        mumu_data_N.Add(H2[year+"_Others_OS_mumu_llOnZ_"+var],-1)
        mumu_data_N.Add(H2[year+"_FakeL_OS_mumu_llOnZ_"+var],-1)

        ee_data_D = H2[year+"_FakeTau_OS_ee_llOnZ_"+var].Clone()
        mumu_data_D = H2[year+"_FakeTau_OS_mumu_llOnZ_"+var].Clone()
        
        ee_data_N.Add(mumu_data_N)
        ee_data_D.Add(mumu_data_D)

        ee_data_N.Divide(ee_data_D)  

        plot2D(ee_data_N, year, "tau p_{T} [GeV]", "tau |#eta|", "Tau fake efficiency SF", False, ARGS.FOLDER+"/"+year+"/"+var)
        ee_data_N.SetName("FakeEff_SF_AbsEtaVsPt_"+var)
        ee_data_N.Write()
    fileout.Close()

