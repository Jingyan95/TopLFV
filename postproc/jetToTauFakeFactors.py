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
    for xcut in X_CUTS:
        for region in xcut:
            for ycut in Y_CUTS:
                for domain in ycut:
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
    for iCut in range(len(X_CUTS)):
        x1 = X_CUTS[iCut][0]
        x2 = X_CUTS[iCut][1] # Signal
        y1 = Y_CUTS[iCut][0] # Signal
        y2 = Y_CUTS[iCut][1]
        regA = x1+"_"+y1
        regC = x1+"_"+y2
        regD = x2+"_"+y2
        regB = x2+"_"+y1

        for iVar, var in enumerate(VARS1DFF):
            if "Fake" in var: continue

            # Plot fake tau purity
            for charge in CHARGES:
                for channel in CHANNELS:
                    histsA = []
                    histsC = []
                    histsD = []
                    histsB = []
                    labels = []
                    for iSample, sample in enumerate(SAMPLES):
                        if sample=="Data" or sample=="LFVStScalarU" or sample=="LFVTtScalarU": continue

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regA+"_"+var
                        purA = H1[hkey+"Fake"].Clone()
                        denA = H1[hkey].Clone()
                        purA.Divide(denA)
                        histsA.append(purA)

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regC+"_"+var
                        purC = H1[hkey+"Fake"].Clone()
                        denC = H1[hkey].Clone()
                        purC.Divide(denC)
                        histsC.append(purC)

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regD+"_"+var
                        purD = H1[hkey+"Fake"].Clone()
                        denD = H1[hkey].Clone()
                        purD.Divide(denD)
                        histsD.append(purD)

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regB+"_"+var
                        purB = H1[hkey+"Fake"].Clone()
                        denB = H1[hkey].Clone()
                        purB.Divide(denB)
                        histsB.append(purB)

                        labels.append(SAMPLES_NAME[iSample])
                    plot1D(year, histsA, labels, VARS1DFF_NAME[iVar], "Fake tau purity",
                        "2l+#tau, "+X_CUT_LABELS[iCut][0]+", "+Y_CUT_LABELS[iCut][0], False,
                        ARGS.FOLDER+"/"+year+"/"+x1+"/"+y1+"/"+charge+"/"+channel+"/"+var+"_purity")
                    plot1D(year, histsC, labels, VARS1DFF_NAME[iVar], "Fake tau purity",
                        "2l+#tau, "+X_CUT_LABELS[iCut][0]+", "+Y_CUT_LABELS[iCut][1], False,
                        ARGS.FOLDER+"/"+year+"/"+x1+"/"+y2+"/"+charge+"/"+channel+"/"+var+"_purity")
                    plot1D(year, histsD, labels, VARS1DFF_NAME[iVar], "Fake tau purity",
                        "2l+#tau, "+X_CUT_LABELS[iCut][1]+", "+Y_CUT_LABELS[iCut][1], False,
                        ARGS.FOLDER+"/"+year+"/"+x2+"/"+y2+"/"+charge+"/"+channel+"/"+var+"_purity")
                    plot1D(year, histsB, labels, VARS1DFF_NAME[iVar], "Fake tau purity",
                        "2l+#tau, "+X_CUT_LABELS[iCut][1]+", "+Y_CUT_LABELS[iCut][0], False,
                        ARGS.FOLDER+"/"+year+"/"+x2+"/"+y1+"/"+charge+"/"+channel+"/"+var+"_purity")

            hists = []
            labels = []
            lstyles = []
            # fout[year+"_"+var].cd()
            for charge in CHARGES:
                for channel in CHANNELS:
                    hname = charge+"_"+channel+"_"+var+"_ff_"+x1
                    # Get data and subtract "real" taus
                    hkey = charge+"_"+channel+"_"+regA+"_"+var
                    ff = H1[year+"_Data_"+hkey].Clone()
                    ff.Add(H1[year+"_TX_"+hkey].Clone(), -1.0)
                    ff.Add(H1[year+"_VV_"+hkey].Clone(), -1.0)
                    for i in range(1, ff.GetNbinsX()+1):
                        if ff.GetBinContent(i)<0.0:
                            ff.SetBinContent(i, 0.0)
                            ff.SetBinError(i, 0.0)
                    hkey = charge+"_"+channel+"_"+regC+"_"+var
                    denom = H1[year+"_Data_"+hkey].Clone()
                    denom.Add(H1[year+"_TX_"+hkey].Clone(), -1.0)
                    denom.Add(H1[year+"_VV_"+hkey].Clone(), -1.0)
                    for i in range(1, denom.GetNbinsX()+1):
                        if denom.GetBinContent(i)<0.0:
                            denom.SetBinContent(i, 0.0)
                            denom.SetBinError(i, 0.0)
                    ff.Divide(denom) # Calculate fake factors
                    ff.SetName(hname)
                    # ff.Write() # Write to ROOT file
                    hists.append(ff) # Add histogram to plot
                    labels.append(charge+"-"+channel)
                    if charge=="OS":
                        lstyles.append(ROOT.kSolid)
                    elif charge=="SS":
                        lstyles.append(ROOT.kDashed)
            plot1D(year, hists, labels, VARS1DFF_NAME[iVar], "Fake factor",
                "2l+#tau, "+X_CUT_LABELS[iCut][0], False, ARGS.FOLDER+"/"+year+"/"+x1+"/"+var+"_ff", lstyles)

            avgFF = hists[0].Clone() # OS-ee
            avgFF.Add(hists[2].Clone()) # OS-mumu
            avgFF.Scale(1.0/2.0) # Averaged
            for charge in CHARGES:
                closure = []
                closure_labels = []
                closure_styles = []
                closure_colors = []
                incr = 1
                if charge=="SS": incr += 3
                for iCh, channel in enumerate(CHANNELS):
                    hkey = charge+"_"+channel+"_"+regD+"_"+var
                    predicted = H1[year+"_Data_"+hkey].Clone()
                    predicted.Add(H1[year+"_TX_"+hkey].Clone(), -1.0)
                    predicted.Add(H1[year+"_VV_"+hkey].Clone(), -1.0)
                    predicted.Multiply(avgFF)
                    hkey = charge+"_"+channel+"_"+regB+"_"+var
                    actual = H1[year+"_Data_"+hkey].Clone()
                    closure.append(predicted)
                    closure_labels.append("OS-"+channel+" Pred.")
                    closure_styles.append(ROOT.kDashed)
                    closure_colors.append(COLORS[iCh+incr])
                    closure.append(actual)
                    closure_labels.append("OS-"+channel+" Actual")
                    closure_styles.append(ROOT.kSolid)
                    closure_colors.append(COLORS[iCh+incr])
                plot1D(year, closure, closure_labels, VARS1DFF_NAME[iVar], "Events",
                    "2l+#tau, "+X_CUT_LABELS[iCut][1], True, ARGS.FOLDER+"/"+year+"/"+x2+"/"+charge+"_"+var+"_closure",
                    closure_styles, closure_colors)

        for iVar, var in enumerate(VARS2DFF):
            if "Fake" in var: continue

            # # Plot fake tau purity
            for charge in CHARGES:
                for channel in CHANNELS:
                    for iSample, sample in enumerate(SAMPLES):
                        if sample=="Data" or sample=="LFVStScalarU" or sample=="LFVTtScalarU": continue

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regA+"_"+var
                        purA = H2[hkey+"Fake"].Clone()
                        denA = H2[hkey].Clone()
                        purA.Divide(denA)
                        if purA.GetEntries()>0:
                            plot2D(purA, VARS2DFF_NAME[iVar][0], VARS2DFF_NAME[iVar][1], "Fake tau purity", False,
                                ARGS.FOLDER+"/"+year+"/"+x1+"/"+y1+"/"+charge+"/"+channel+"/"+var+"_"+sample+"_purity",
                                [0.0, 1.1])

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regC+"_"+var
                        purC = H2[hkey+"Fake"].Clone()
                        denC = H2[hkey].Clone()
                        purC.Divide(denC)
                        if purC.GetEntries()>0:
                            plot2D(purC, VARS2DFF_NAME[iVar][0], VARS2DFF_NAME[iVar][1], "Fake tau purity", False,
                                ARGS.FOLDER+"/"+year+"/"+x1+"/"+y2+"/"+charge+"/"+channel+"/"+var+"_"+sample+"_purity",
                                [0.0, 1.1])

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regD+"_"+var
                        purD = H2[hkey+"Fake"].Clone()
                        denD = H2[hkey].Clone()
                        purD.Divide(denD)
                        if purD.GetEntries()>0:
                            plot2D(purD, VARS2DFF_NAME[iVar][1], VARS2DFF_NAME[iVar][1], "Fake tau purity", False,
                                ARGS.FOLDER+"/"+year+"/"+x2+"/"+y2+"/"+charge+"/"+channel+"/"+var+"_"+sample+"_purity",
                                [0.0, 1.1])

                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+regB+"_"+var
                        purB = H2[hkey+"Fake"].Clone()
                        denB = H2[hkey].Clone()
                        purB.Divide(denB)
                        if purB.GetEntries()>0:
                            plot2D(purB, VARS2DFF_NAME[iVar][1], VARS2DFF_NAME[iVar][0], "Fake tau purity", False,
                                ARGS.FOLDER+"/"+year+"/"+x2+"/"+y1+"/"+charge+"/"+channel+"/"+var+"_"+sample+"_purity",
                                [0.0, 1.1])

            if year!="All": fout[year+"_"+var].cd()
            for charge in CHARGES:
                for channel in CHANNELS:
                    hname = charge+"_"+channel+"_"+var+"_ff_"+x1
                    # Get data and subtract "real" taus
                    hkey = charge+"_"+channel+"_"+regA+"_"+var
                    ff = H2[year+"_Data_"+hkey].Clone()
                    ff.Add(H2[year+"_TX_"+hkey].Clone(), -1.0)
                    ff.Add(H2[year+"_VV_"+hkey].Clone(), -1.0)
                    ff.SetName(hname)
                    if ff.GetEntries()==0.0:
                        if year!="All": ff.Write()
                        continue
                    for i in range(1, ff.GetNbinsX()+1):
                        for j in range(1, ff.GetNbinsY()+1):
                            if ff.GetBinContent(i, j)<0.0:
                                ff.SetBinContent(i, j, 0.0)
                                ff.SetBinError(i, j, 0.0)
                    hkey = charge+"_"+channel+"_"+regC+"_"+var
                    denom = H2[year+"_Data_"+hkey].Clone()
                    denom.Add(H2[year+"_TX_"+hkey].Clone(), -1.0)
                    denom.Add(H2[year+"_VV_"+hkey].Clone(), -1.0)
                    for i in range(1, denom.GetNbinsX()+1):
                        for j in range(1, denom.GetNbinsY()+1):
                            if denom.GetBinContent(i, j)<0.0:
                                denom.SetBinContent(i, j, 0.0)
                                denom.SetBinError(i, j, 0.0)
                    ff.Divide(denom) # Calculate fake factors
                    if ff.GetEntries()==0.0:
                        if year!="All": ff.Write()
                        continue
                    if year!="All": ff.Write() # Write to ROOT file
                    plot2D(ff, VARS2DFF_NAME[iVar][0], VARS2DFF_NAME[iVar][1], "Fake factor", False,
                        ARGS.FOLDER+"/"+year+"/"+x1+"/"+charge+"_"+channel+"_"+var+"_ff")
