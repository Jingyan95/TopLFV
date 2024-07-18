import os
import sys
from common import *
from plotFunctions import plot1DStack, plot2D, plotSummary, plot1D


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="MatrixMethod")
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
                
tmp = []
tmp1 = files["2016"].Get("Data_OS_etau_ll_TtauPt").Clone()                                  
tmp1.Reset("ICESM") 
tmp2 = files["2016"].Get("Data_SS_etau_ll_tauJetPt").Clone()
tmp2.Reset("ICESM") 
tmp.append(tmp1)
tmp.append(tmp2)

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

H1Rate = {}
H2Rate = {}
for year in YEARS:
    for charge in CHARGES:
        for iChannel, channel in enumerate(CHANNELS):
            for iRegion, region in enumerate(REGIONS):
                if ('SS' in charge) and ('OnZ' in region):
                    continue
                #Real Rate
                r_1Prong_tt_N = H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_1ProngTauT"].Clone()
                r_1Prong_tt_D = H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_1ProngTauL"].Clone()
                r_3Prong_tt_N = H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_3ProngTauT"].Clone()
                r_3Prong_tt_D = H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_3ProngTauL"].Clone()

                r_1Prong_DY_N = H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_1ProngTauT"].Clone()
                r_1Prong_DY_D = H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_1ProngTauL"].Clone()
                r_3Prong_DY_N = H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_3ProngTauT"].Clone()
                r_3Prong_DY_D = H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_3ProngTauL"].Clone()
                
                r_1Prong_tt_N.Divide(r_1Prong_tt_D)
                plot2D(r_1Prong_tt_N, year, "tau p_{T} [GeV]", "|#eta|", "Real Efficiency", False, ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/r_1Prong_tt")
                H2Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_1Prong_tt"] = r_1Prong_tt_N.Clone()
                r_3Prong_tt_N.Divide(r_3Prong_tt_D)
                plot2D(r_3Prong_tt_N, year, "tau p_{T} [GeV]", "|#eta|", "Real Efficiency", False, ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/r_3Prong_tt")
                H2Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_3Prong_tt"] = r_3Prong_tt_N.Clone()

                r_1Prong_DY_N.Divide(r_1Prong_DY_D)
                plot2D(r_1Prong_DY_N, year, "tau p_{T} [GeV]", "|#eta|", "Real Efficiency", False, ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/r_1Prong_DY")
                H2Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_1Prong_DY"] = r_1Prong_DY_N.Clone()
                r_3Prong_DY_N.Divide(r_3Prong_DY_D)
                plot2D(r_3Prong_DY_N, year, "tau p_{T} [GeV]", "|#eta|", "Real Efficiency", False, ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/r_3Prong_DY")
                H2Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_3Prong_DY"] = r_3Prong_DY_N.Clone()

                r_1Prong_tt_Barrel = tmp[0].Clone()
                r_1Prong_tt_Endcap = tmp[0].Clone()
                r_3Prong_tt_Barrel = tmp[0].Clone()
                r_3Prong_tt_Endcap = tmp[0].Clone()

                r_1Prong_DY_Barrel = tmp[0].Clone()
                r_1Prong_DY_Endcap = tmp[0].Clone()
                r_3Prong_DY_Barrel = tmp[0].Clone()
                r_3Prong_DY_Endcap = tmp[0].Clone()

                for b in range(tmp[0].GetNbinsX()):
                    r_1Prong_tt_Barrel.SetBinContent(b+1,r_1Prong_tt_N.GetBinContent(b+1,1))
                    r_1Prong_tt_Barrel.SetBinError(b+1,r_1Prong_tt_N.GetBinError(b+1,1))
                    r_1Prong_tt_Endcap.SetBinContent(b+1,r_1Prong_tt_N.GetBinContent(b+1,2))
                    r_1Prong_tt_Endcap.SetBinError(b+1,r_1Prong_tt_N.GetBinError(b+1,2))

                    r_3Prong_tt_Barrel.SetBinContent(b+1,r_3Prong_tt_N.GetBinContent(b+1,1))
                    r_3Prong_tt_Barrel.SetBinError(b+1,r_3Prong_tt_N.GetBinError(b+1,1))
                    r_3Prong_tt_Endcap.SetBinContent(b+1,r_3Prong_tt_N.GetBinContent(b+1,2))
                    r_3Prong_tt_Endcap.SetBinError(b+1,r_3Prong_tt_N.GetBinError(b+1,2))

                    r_1Prong_DY_Barrel.SetBinContent(b+1,r_1Prong_DY_N.GetBinContent(b+1,1))
                    r_1Prong_DY_Barrel.SetBinError(b+1,r_1Prong_DY_N.GetBinError(b+1,1))
                    r_1Prong_DY_Endcap.SetBinContent(b+1,r_1Prong_DY_N.GetBinContent(b+1,2))
                    r_1Prong_DY_Endcap.SetBinError(b+1,r_1Prong_DY_N.GetBinError(b+1,2))

                    r_3Prong_DY_Barrel.SetBinContent(b+1,r_3Prong_DY_N.GetBinContent(b+1,1))
                    r_3Prong_DY_Barrel.SetBinError(b+1,r_3Prong_DY_N.GetBinError(b+1,1))
                    r_3Prong_DY_Endcap.SetBinContent(b+1,r_3Prong_DY_N.GetBinContent(b+1,2))
                    r_3Prong_DY_Endcap.SetBinError(b+1,r_3Prong_DY_N.GetBinError(b+1,2))

                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_1Prong_tt_Barrel"] = r_1Prong_tt_Barrel
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_1Prong_tt_Endcap"] = r_1Prong_tt_Endcap
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_3Prong_tt_Barrel"] = r_3Prong_tt_Barrel
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_3Prong_tt_Endcap"] = r_3Prong_tt_Endcap
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_1Prong_DY_Barrel"] = r_1Prong_DY_Barrel
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_1Prong_DY_Endcap"] = r_1Prong_DY_Endcap
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_3Prong_DY_Barrel"] = r_3Prong_DY_Barrel
                H1Rate[year+"_R_"+charge+"_"+channel+"_"+region+"_3Prong_DY_Endcap"] = r_3Prong_DY_Endcap
                #Fake Rate
                f_1Prong_data_N = H2[year+"_Data_"+charge+"_"+channel+"_"+region+"_1ProngTauT"].Clone()
                f_1Prong_data_N.Add(H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_1ProngTauT"],-1)
                f_1Prong_data_N.Add(H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_1ProngTauT"],-1)
                f_1Prong_data_N.Add(H2[year+"_Others_"+charge+"_"+channel+"_"+region+"_1ProngTauT"],-1)

                f_1Prong_data_D = H2[year+"_Data_"+charge+"_"+channel+"_"+region+"_1ProngTauL"].Clone()
                f_1Prong_data_D.Add(H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_1ProngTauL"],-1)
                f_1Prong_data_D.Add(H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_1ProngTauL"],-1)
                f_1Prong_data_D.Add(H2[year+"_Others_"+charge+"_"+channel+"_"+region+"_1ProngTauL"],-1)

                f_3Prong_data_N = H2[year+"_Data_"+charge+"_"+channel+"_"+region+"_3ProngTauT"].Clone()
                f_3Prong_data_N.Add(H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_3ProngTauT"],-1)
                f_3Prong_data_N.Add(H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_3ProngTauT"],-1)
                f_3Prong_data_N.Add(H2[year+"_Others_"+charge+"_"+channel+"_"+region+"_3ProngTauT"],-1)

                f_3Prong_data_D = H2[year+"_Data_"+charge+"_"+channel+"_"+region+"_3ProngTauL"].Clone()
                f_3Prong_data_D.Add(H2[year+"_tt_"+charge+"_"+channel+"_"+region+"_3ProngTauL"],-1)
                f_3Prong_data_D.Add(H2[year+"_DY_"+charge+"_"+channel+"_"+region+"_3ProngTauL"],-1)
                f_3Prong_data_D.Add(H2[year+"_Others_"+charge+"_"+channel+"_"+region+"_3ProngTauL"],-1)

                f_1Prong_data_N.Divide(f_1Prong_data_D)  
                plot2D(f_1Prong_data_N, year, "Mother jet p_{T} [GeV]", "tau R_{T}", "Fake Efficiency", False, ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/f_1Prong_data")
                H2Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_1Prong_Data"] = f_1Prong_data_N.Clone()
                f_3Prong_data_N.Divide(f_3Prong_data_D)
                plot2D(f_3Prong_data_N, year,"Mother jet p_{T} [GeV]", "tau R_{T}", "Fake Efficiency", False, ARGS.FOLDER+"/"+year+"/"+region+"/"+charge+"/"+channel+"/f_3Prong_data")    
                H2Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_3Prong_Data"] = f_3Prong_data_N.Clone() 

                f_1Prong_Data_LBtag = tmp[1].Clone()
                f_1Prong_Data_MBtag = tmp[1].Clone()
                f_1Prong_Data_HBtag = tmp[1].Clone()
                f_3Prong_Data_LBtag = tmp[1].Clone()
                f_3Prong_Data_MBtag = tmp[1].Clone()
                f_3Prong_Data_HBtag = tmp[1].Clone()

                for b in range(tmp[1].GetNbinsX()):
                    f_1Prong_Data_LBtag.SetBinContent(b+1,f_1Prong_data_N.GetBinContent(b+1,1))
                    f_1Prong_Data_LBtag.SetBinError(b+1,f_1Prong_data_N.GetBinError(b+1,1))
                    f_1Prong_Data_MBtag.SetBinContent(b+1,f_1Prong_data_N.GetBinContent(b+1,2))
                    f_1Prong_Data_MBtag.SetBinError(b+1,f_1Prong_data_N.GetBinError(b+1,2))
                    f_1Prong_Data_HBtag.SetBinContent(b+1,f_1Prong_data_N.GetBinContent(b+1,3))
                    f_1Prong_Data_HBtag.SetBinError(b+1,f_1Prong_data_N.GetBinError(b+1,3))

                    f_3Prong_Data_LBtag.SetBinContent(b+1,f_3Prong_data_N.GetBinContent(b+1,1))
                    f_3Prong_Data_LBtag.SetBinError(b+1,f_3Prong_data_N.GetBinError(b+1,1))
                    f_3Prong_Data_MBtag.SetBinContent(b+1,f_3Prong_data_N.GetBinContent(b+1,2))
                    f_3Prong_Data_MBtag.SetBinError(b+1,f_3Prong_data_N.GetBinError(b+1,2))
                    f_3Prong_Data_HBtag.SetBinContent(b+1,f_3Prong_data_N.GetBinContent(b+1,3))
                    f_3Prong_Data_HBtag.SetBinError(b+1,f_3Prong_data_N.GetBinError(b+1,3))

                H1Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_1Prong_Data_LBtag"] = f_1Prong_Data_LBtag
                H1Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_1Prong_Data_MBtag"] = f_1Prong_Data_MBtag
                H1Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_1Prong_Data_HBtag"] = f_1Prong_Data_HBtag
                H1Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_3Prong_Data_LBtag"] = f_3Prong_Data_LBtag
                H1Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_3Prong_Data_MBtag"] = f_3Prong_Data_MBtag
                H1Rate[year+"_F_"+charge+"_"+channel+"_"+region+"_3Prong_Data_HBtag"] = f_3Prong_Data_HBtag

# Create save folders
for year in YEARS:
    for region in REGIONS:
        for channel in CHANNELS:
            if not os.path.exists("1DRate"):
                os.makedirs("1DRate")
            if not os.path.exists("1DRate"+"/"+year):
                os.makedirs("1DRate"+"/"+year)
            if not os.path.exists("1DRate"+"/"+year+"/"+region):
                os.makedirs("1DRate"+"/"+year+"/"+region)
            if not os.path.exists("1DRate"+"/"+year+"/"+region+"/"+channel):
                os.makedirs("1DRate"+"/"+year+"/"+region+"/"+channel)

Labels_R = ["1Prong, |#eta|<1.5", "1Prong, 1.5<|#eta|<2.3", "3Prong, |#eta|<1.5", "3Prong, 1.5<|#eta|<2.3"] 
Labels_F = ["1Prong, btag<0.02", "1Prong, 0.02<btag<0.1", "1Prong, 0.1<btag<1", "3Prong, btag<0.02", "3Prong, 0.02<btag<0.1", "3Prong, 0.1<btag<1"] 
for year in YEARS:
    for iChannel, channel in enumerate(CHANNELS):
            for iRegion, region in enumerate(REGIONS):
                R_tt = []
                R_DY = []
                R_tt.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_1Prong_tt_Barrel"])
                R_tt.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_1Prong_tt_Endcap"])
                R_tt.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_3Prong_tt_Barrel"])
                R_tt.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_3Prong_tt_Endcap"])
                plot1D(year, R_tt, Labels_R, "tau p_{T} [GeV]", "Real Efficiency in t#bar{t}", Labels_R, Labels_R,CHANNELS_NAME[iChannel],False,"1DRate/"+year+"/"+region+"/"+channel+"/R_tt_tauPt")
                R_DY.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_1Prong_DY_Barrel"])
                R_DY.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_1Prong_DY_Endcap"])
                R_DY.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_3Prong_DY_Barrel"])
                R_DY.append(H1Rate[year+"_R_OS_"+channel+"_"+region+"_3Prong_DY_Endcap"])
                plot1D(year, R_DY, Labels_R, "tau p_{T} [GeV]", "Real Efficiency in DY", Labels_R, Labels_R,CHANNELS_NAME[iChannel],False,"1DRate/"+year+"/"+region+"/"+channel+"/R_DY_tauPt")
                if ('OnZ' in region):
                    continue
                F_Data = []
                F_Data.append(H1Rate[year+"_F_SS_"+channel+"_"+region+"_1Prong_Data_LBtag"])
                F_Data.append(H1Rate[year+"_F_SS_"+channel+"_"+region+"_1Prong_Data_MBtag"])
                F_Data.append(H1Rate[year+"_F_SS_"+channel+"_"+region+"_1Prong_Data_HBtag"])
                F_Data.append(H1Rate[year+"_F_SS_"+channel+"_"+region+"_3Prong_Data_LBtag"])
                F_Data.append(H1Rate[year+"_F_SS_"+channel+"_"+region+"_3Prong_Data_MBtag"])
                F_Data.append(H1Rate[year+"_F_SS_"+channel+"_"+region+"_3Prong_Data_HBtag"])
                plot1D(year, F_Data, Labels_F, "Mother jet p_{T} [GeV]", "Fake Efficiency in Data", Labels_F, Labels_F,CHANNELS_NAME[iChannel],False,"1DRate/"+year+"/"+region+"/"+channel+"/F_Data_tauPt")

for year in YEARS:
    fileout = ROOT.TFile(year + 'FakeTauMatrixMethod.root','recreate')
    h2 = H2Rate[year+"_R_OS_mutau_llBgeq1_1Prong_tt"].Clone()
    h2.SetName("RealEff_AbsEtaVsPt_1Prong")
    h2.Write()
    h2 = H2Rate[year+"_R_OS_mutau_llBgeq1_3Prong_tt"].Clone()
    h2.SetName("RealEff_AbsEtaVsPt_3Prong")
    h2.Write()
    h2 = H2Rate[year+"_F_SS_mutau_ll_1Prong_Data"].Clone()
    h2.SetName("FakeEff_RtVsPt_1Prong")
    h2.Write()
    h2 = H2Rate[year+"_F_SS_mutau_ll_3Prong_Data"].Clone()
    h2.SetName("FakeEff_RtVsPt_3Prong")
    h2.Write()
    fileout.Close()
