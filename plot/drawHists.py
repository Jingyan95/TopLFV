import argparse
import os
import sys
import uproot
import numpy as np
import cmsstyle as CMS
import ROOT
import gc
from math import sqrt
from array import array


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018", "All"]
SAMPLES = ["Data", "TX", "VV", "DY", "TT", "LFVStScalarU", "LFVTtScalarU"]
SAMPLES_NAME = ["Data", "t#bar{t}+X", "VV(V)", "DY/ZZ", "t#bar{t}/WW",
    "CLFV top production (#mu_{ll'tu}^{scalar} = 0.5)",
    "CLFV top decay (#mu_{ll'tu}^{scalar} = 20)"]
SAMPLES_NAME_SUMMARY = ["Data", "t#bar{t}+X", "VV(V)", "DY/ZZ", "t#bar{t}/WW",
    "CLFV top production", "CLFV top decay"]
CHARGES = ["OS", "SS"]
CHANNELS = ["ee", "emu", "mumu"]
CHANNELS_NAME = ["ee#tau_{h}", "e#mu#tau_{h}", "#mu#mu#tau_{h}"]
REGIONS = [
    "ll",
    "llOnZMetg20Jetgeq1",
    "llOffZMetg20B1",
    "llOffZMetg20B2",
    "llStl300",
    "llOnZ",
    "llbtagg1p3",
    "llStg300OffZbtagl1p3",
    "llStg300OffZbtagl1p3Tight",
    "llOffZ"
]
REGIONS_NAME = [
    ("No cuts", ""),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ (Z+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1 (SR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2 (t#bar{t}+jets CR)"),
    ("S_{T}<300GeV", "(CR)"),
    ("OnZ", "(Z+jets CR)"),
    ("btag>1.3", "(t#bar{t}+jets CR)"),
    ("S_{T}>300GeV, OffZ", "btag<1.3 (SR(Alt, Loose))"),
    ("S_{T}>300GeV, OffZ", "btag<1.3, njet#geq1 or S_{T}>500GeV (SR(Alt, Tight))"),
    ("OffZ", "(Close to SR CR)")
]
DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa"]
DOMAINS_NAME = ["#geq Tight Tau", "< Tight Tau"]
# DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa", "geqMedLepgeqTightTaJetTaFF"]
# DOMAINS_NAME = ["#geq Tight Tau", "< Tight Tau", "#geq Tight Tau"]
VARS1D = [
    "llM", "llDr", "lep1Pt", "lep2Pt", "elLeptonMVAv1", "elLeptonMVAv2", "muLeptonMVAv1", "muLeptonMVAv2",
    "taPt", "taPtFFBin", "taPtFake", "taEta", "taEtaFFBin", "taEtaFake", "taVsJetWP", "taVsJetMVA",
    "taVsElMVA", "taVsMuMVA", "taDxy", "taDz", "taDecayMode", "jet1Pt", "jetbtagDeepFlavB", "njet",
    "nbjet", "MET", "subSR", "LFVemuM", "LFVetaM", "LFVmutaM", "LFVemuDr", "LFVetaDr", "LFVmutaDr",
    "LFVePt", "LFVmuPt", "LFVtaPt", "balepPt", "topmass", "Ht", "St", "btagSum"]
VARS1D_NAME = [
    "m(l#bar{l}) [GeV]", "#DeltaR(l#bar{l})", "Leading lepton p_{T} [GeV]", "Sub-leading lepton p_{T} [GeV]",
    "Electron Top Lepton MVA (v1)", "Electron Top Lepton MVA (v2)", "Muon Top Lepton MVA (v1)",
    "Muon Top Lepton MVA (v2)", "#tau p_{T} [GeV]", "#tau p_{T} [GeV]", "Fake #tau p_{T} [GeV]", "#tau #eta",
    "#tau #eta", "Fake #tau #eta", "#tau vs Jet WP", "#tau vs Jet MVA", "#tau vs Electron MVA",
    "#tau vs Muon MVA", "#tau d_{xy} [cm]", "#tau d_{z} [cm]", "#tau Decay Mode", "Leading jet p_{T} [GeV]",
    "btag", "njet", "nbjet (Loose WP)", "MET [GeV]", "SR subdivided", "m(e#bar{#mu}) [GeV]",
    "m(e#bar{#tau}) [GeV]", "m(#mu#bar{#tau}) [GeV]", "#DeltaR(e,#bar{#mu}) [GeV]", "#DeltaR(e,#bar{#tau}) [GeV]",
    "#DeltaR(#mu,#bar{#tau}) [GeV]", "LFV electron p_{T} [GeV]", "LFV muon p_{T} [GeV]", "LFV tau p_{T} [GeV]",
    "Bachelor lepton p_{T} [GeV]", "m(top) [GeV]", "H_{T} [GeV]", "S_{T} [GeV]", "Sum of btagging scores"]
VARS2D = ["taPtVsEta", "taPtVsEtaFake"]
VARS2D_NAME = [("#tau p_{T} [GeV]", "#tau #eta"), ("Fake #tau p_{T} [GeV]", "Fake #tau #eta")]
COLORS = [ROOT.kBlack, ROOT.kRed - 4, ROOT.kOrange - 3, ROOT.kGreen, ROOT.kYellow, ROOT.kViolet + 1, ROOT.kGray]
PLOT_LABEL = "Work in Progress"

def getLumi(year):
    if year=="2016APV": return "19.5"
    elif year=="2016": return "16.8"
    elif year=="2017": return "41.5"
    elif year=="2018": return "59.8"
    return "138"


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
parser.add_argument("--s", dest="SQUARE", default=True)
parser.add_argument("--o", dest="OUTPATH", default="")
parser.add_argument("--f", dest="FOLDER", default="StackHist")
ARGS = parser.parse_args()
YEARS = []
for iYear, year in enumerate(YEARS_RUN2):
    if ARGS.YEAR == year or ARGS.YEAR == "RunII":
        YEARS.append(YEARS_RUN2[iYear])
square = CMS.kSquare
if not ARGS.SQUARE: square = CMS.kRectangular
if len(ARGS.OUTPATH)>0: ARGS.FOLDER = ARGS.OUTPATH+"/"+ARGS.FOLDER


# TODO: add 2D plots
# TODO: add tau purity plots (1D and 2D)

# Read in histograms
HistAddress = os.path.dirname(sys.path[0])+"/hists"
if len(ARGS.HISTPATH)>0: HistAddress += "/"+ARGS.HISTPATH
h = {}
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
                            h[year+"_"+sample+"_"+hname] = temp
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


def makePlot(hists, year, charge, iChannel, iRegion, varName, var, topLabel, saveDir):
    CMS.SetLumi(getLumi(year))
    CMS.SetEnergy("13") # Run 2
    CMS.SetExtraText(PLOT_LABEL)

    # Make MC and signal histograms
    MCHists = []
    SigHists = []
    for iSample, sample in enumerate(SAMPLES):
        if sample=="Data": continue
        if "LFV" not in sample: # MC
            if len(MCHists)>0:
                loopHist = MCHists[-1].Clone()
                loopHist.Add(hists[iSample].Clone())
                MCHists.append(loopHist)
            else:
                MCHists.append(hists[iSample].Clone())
        else:
            loopHist = hists[iSample].Clone()
            if sample=="LFVStScalarU": loopHist.Scale(0.5)
            elif sample=="LFVTtScalarU": loopHist.Scale(20)
            loopHist.SetFillColor(0)
            SigHists.append(loopHist)

    # Calculate data/pred. ratio
    ratioHist = hists[0].Clone()
    ratioHist.Divide(MCHists[-1].Clone())

    # Get error on MC and ratio
    xpos = []
    xerr = []
    ypos = []
    yerrup = []
    yerrdown = []
    yRel = []
    yerrupRel = []
    yerrdownRel = []
    for iBin in range(1, MCHists[-1].GetNbinsX()+1):
        if MCHists[-1].GetBinContent(iBin) > 0.0:
            xpos.append(MCHists[-1].GetBinCenter(iBin))
            xerr.append(MCHists[-1].GetBinWidth(iBin)/2)
            ypos.append(MCHists[-1].GetBinContent(iBin))
            yerrup.append(MCHists[-1].GetBinError(iBin))
            yerrdown.append(MCHists[-1].GetBinError(iBin))
            yRel.append(1.0)
            yerrupRel.append(MCHists[-1].GetBinError(iBin)/MCHists[-1].GetBinContent(iBin))
            yerrdownRel.append(MCHists[-1].GetBinError(iBin)/MCHists[-1].GetBinContent(iBin))
    if len(xpos)>0:
        MCErrorHist = ROOT.TGraphAsymmErrors(len(xpos), np.array(xpos), np.array(ypos),
            np.array(xerr), np.array(xerr), np.array(yerrdown), np.array(yerrup))
        MCRelError = ROOT.TGraphAsymmErrors(len(xpos), np.array(xpos), np.array(yRel),
            np.array(xerr), np.array(xerr), np.array(yerrdownRel), np.array(yerrupRel))
    else:
        MCErrorHist = ROOT.TGraphAsymmErrors()
        MCRelError = ROOT.TGraphAsymmErrors()

    # Get x_min and x_max
    x_min = hists[0].GetBinLowEdge(1)
    x_max = hists[0].GetBinLowEdge(hists[0].GetNbinsX())+hists[0].GetBinWidth(hists[0].GetNbinsX())
    # Get y_min and y_max
    y_max = hists[0].GetMaximum()
    true_y_min = 1e10
    for hist in hists:
        true_y_min = min(true_y_min, hist.GetMinimum(0.0))
    y_min = true_y_min/2.0
    y_max = 2000*max(y_max, MCHists[-1].GetMaximum())

    dicanv = CMS.cmsDiCanvas(var,
        x_min, x_max, y_min, y_max, 0.2, 1.8,
        varName, "Events", "Data/Pred.",
        square=square, extraSpace=0.1, iPos=0)
    dicanv.cd(1).SetLogy(True)

    # Draw histograms
    for iHist, loopHist in enumerate(reversed(MCHists)):
        CMS.cmsDraw(loopHist, "hist", fcolor=COLORS[1+iHist])
    CMS.cmsDraw(MCErrorHist, "E2", fstyle=3004, fcolor=COLORS[0])
    CMS.cmsDraw(hists[0], "P EX0", fcolor=COLORS[0], lwidth=2)
    for iHist, loopHist in enumerate(SigHists):
        CMS.cmsDraw(loopHist, "hist", lcolor=COLORS[1+len(MCHists)+iHist], fcolor=0, lwidth=3, lstyle=iHist+1)

    # Draw legend
    if square:
        legLeft = CMS.cmsLeg(0.59, 0.71, 0.74, 0.89, textSize=0.04)
        legRight = CMS.cmsLeg(0.74, 0.71, 0.89, 0.89, textSize=0.04)
        legBottom = CMS.cmsLeg(0.37, 0.59, 0.89, 0.71, textSize=0.04)
    else:
        legLeft = CMS.cmsLeg(0.66, 0.7, 0.78, 0.88, textSize=0.05)
        legRight = CMS.cmsLeg(0.78, 0.7, 0.9, 0.88, textSize=0.05)
        legBottom = CMS.cmsLeg(0.43, 0.58, 0.9, 0.7, textSize=0.05)
    legLeft.AddEntry(hists[0], SAMPLES_NAME[0], "P EX0")
    for iHist, loopHist in enumerate(reversed(MCHists)):
        if iHist < len(MCHists)/2:
            legLeft.AddEntry(loopHist, SAMPLES_NAME[1+iHist], "f")
        else:
            legRight.AddEntry(loopHist, SAMPLES_NAME[1+iHist], "f")
    legRight.AddEntry(MCErrorHist, "Stat. only", "f")
    for iHist, loopHist in enumerate(SigHists):
        legBottom.AddEntry(loopHist, SAMPLES_NAME[1+len(MCHists)+iHist], "l")

    # Add charge, channel, region labels
    if square:
        legLabelTop = CMS.cmsLeg(0.18, 0.83, 0.5, 0.89, textSize=0.04)
        legLabelMiddle = CMS.cmsLeg(0.18, 0.77, 0.5, 0.83, textSize=0.04)
        legLabelBottom = CMS.cmsLeg(0.18, 0.71, 0.5, 0.77, textSize=0.04)
    else:
        legLabelTop = CMS.cmsLeg(0.15, 0.82, 0.5, 0.88, textSize=0.05)
        legLabelMiddle = CMS.cmsLeg(0.15, 0.76, 0.5, 0.82, textSize=0.05)
        legLabelBottom = CMS.cmsLeg(0.15, 0.7, 0.5, 0.76, textSize=0.05)
    CMS.cmsHeader(legLabelTop, topLabel, textSize=0.04)
    CMS.cmsHeader(legLabelMiddle, REGIONS_NAME[iRegion][0], textSize=0.04)
    CMS.cmsHeader(legLabelBottom, REGIONS_NAME[iRegion][1], textSize=0.04)

    # Draw MC relative error and ratio plot + reference lines
    dicanv.cd(2)
    CMS.cmsDraw(MCRelError, "E2", fstyle=3004, fcolor=COLORS[0])
    CMS.cmsDraw(ratioHist, "P EX0", fcolor=COLORS[0], lwidth=2)
    upLine = ROOT.TLine(x_min, 1.5, x_max, 1.5)
    midLine = ROOT.TLine(x_min, 1, x_max, 1)
    downLine = ROOT.TLine(x_min, 0.5, x_max, 0.5)
    CMS.cmsDrawLine(upLine, lcolor=COLORS[0], lstyle=ROOT.kDotted)
    CMS.cmsDrawLine(midLine, lcolor=COLORS[0], lstyle=ROOT.kDotted)
    CMS.cmsDrawLine(downLine, lcolor=COLORS[0], lstyle=ROOT.kDotted)

    CMS.SaveCanvas(dicanv, saveDir+"/"+var+".png", close=False)
    CMS.SaveCanvas(dicanv, saveDir+"/"+var+".pdf")
    del dicanv
    gc.collect()


def SummaryPlot(hists, SignalHists, Fnames, year, iRegion, region, iDomain, saveDir):
    ROOT.gStyle.SetErrorX(0) # No horizontal error bar
    hs = ROOT.THStack("hs", "")
    for num in range(1, len(hists)):
        hs.Add(hists[num])

    binwidth = array("d")
    bincenter = array("d")
    yvalue = array("d")
    yerrup = array("d")
    yerrdown = array("d")
    T = hists[0].Clone()
    for b in range(T.GetNbinsX()):
        if T.GetBinContent(b+1)>0:
            binwidth.append(0)
            bincenter.append(T.GetBinCenter(b+1))
            yvalue.append(T.GetBinContent(b+1))
            yerrup.append(T.GetBinError(b+1))
            yerrdown.append(T.GetBinError(b+1))
    if len(bincenter)>0:
        dummy = ROOT.TGraphAsymmErrors(len(bincenter), bincenter, yvalue, binwidth, binwidth, yerrdown, yerrup)
    else:
        dummy = ROOT.TGraphAsymmErrors()

    canvas = ROOT.TCanvas(year+region, year+region, 50, 50, 1865, 780)
    canvas.SetGrid()
    canvas.SetBottomMargin(0.17)
    canvas.cd()
    # Calculating S/sqrt(B)
    Label_sig = ROOT.TLatex(0.051, 0.29, r"#frac{S}{#sqrt{B}}")
    Label_sig.SetNDC()
    Label_sig.SetTextFont(42)
    Label_sig.SetTextSize(0.03)
    Label_sig.Draw("")
    sig = []
    for b in range(SignalHists[0].GetNbinsX()):
        if hs.GetStack().Last().GetBinContent(b+1)>0:
            Sig = ROOT.TLatex(0.085+b*0.0495, 0.29,
                str(round((SignalHists[0]+SignalHists[1]).GetBinContent(b+1)/sqrt(hs.GetStack().Last().GetBinContent(b+1)), 2)))
            Sig.SetNDC()
            Sig.SetTextFont(42)
            Sig.SetTextSize(0.03)
            Sig.Draw("")
            sig.append(Sig)

    legend = ROOT.TLegend(0.56, 0.68, 0.63, 0.87)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend2 = ROOT.TLegend(0.63, 0.68, 0.7, 0.87)
    legend2.SetBorderSize(0)
    legend2.SetFillStyle(0)
    legend2.SetTextFont(42)
    legend2.SetTextSize(0.05)
    legend3 = ROOT.TLegend(0.7, 0.75, 0.85, 0.87)
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
    pad1.SetLeftMargin(0.07)
    pad1.SetRightMargin(0.035)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetLeftMargin(0.07)
    pad2.SetRightMargin(0.035)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kTRUE)

    for H in range(len(SignalHists)):
        if H > 0:
            SignalHists[H].Scale(100)
        else:
            SignalHists[H].Scale(1)

    y_max = hists[0].GetMaximum()
    if y_max < hs.GetStack().Last().GetMaximum():
        y_max = hs.GetStack().Last().GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetLineWidth(1)
    x_min = hists[0].GetXaxis().GetBinLowEdge(1)
    x_max = hists[0].GetXaxis().GetBinLowEdge(hists[0].GetXaxis().GetNbins())+hists[0].GetXaxis().GetBinWidth(hists[0].GetXaxis().GetNbins())

    frame = pad1.DrawFrame(x_min, 0.2, x_max, 6000*y_max)
    frame.SetTitle("")
    frame.GetYaxis().SetTitle('Events')
    frame.GetXaxis().SetLabelSize(0)
    frame.GetYaxis().SetTitleOffset(0.4)
    frame.GetYaxis().SetTitleSize(0.07)
    frame.GetYaxis().SetLabelOffset(0.0006)
    frame.GetYaxis().SetLabelSize(0.05)
    pad1.Update()

    dummy.Draw("P")
    hs.Draw("histSAME")
    for H in range(len(SignalHists)):
        SignalHists[H].SetLineWidth(2)
        SignalHists[H].SetFillColor(0)
        SignalHists[H].SetLineStyle(H+1)
        SignalHists[H].Draw("histSAME")
    dummy.Draw("PSAME")
    frame.Draw("AXISSAMEY+")
    frame.Draw("AXISSAMEX+")
    pad1.Update()
    # Sub-SR boundries and legends
    line = ROOT.TLine(2, 0, 2, y_max*15)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    line.Draw("")
    line1 = ROOT.TLine(8, 0, 8, y_max*15)
    line1.SetLineColor(ROOT.kBlack)
    line1.SetLineWidth(1)
    line1.SetLineStyle(2)
    line1.Draw("")
    line2 = ROOT.TLine(10, 0, 10, y_max*15)
    line2.SetLineColor(ROOT.kBlack)
    line2.SetLineWidth(1)
    line2.SetLineStyle(2)
    line2.Draw("")
    line3 = ROOT.TLine(12, 0, 12, y_max*15)
    line3.SetLineColor(ROOT.kBlack)
    line3.SetLineWidth(1)
    line3.SetLineStyle(2)
    line3.Draw("")
    line4 = ROOT.TLine(16, 0, 16, y_max*15)
    line4.SetLineColor(ROOT.kBlack)
    line4.SetLineWidth(1)
    line4.SetLineStyle(2)
    line4.Draw("")
    Label_SRblock1 = ROOT.TLatex(0.099, 0.57, "OS-ee")
    Label_SRblock1.SetNDC()
    Label_SRblock1.SetTextFont(42)
    Label_SRblock1.SetTextSize(0.058)
    Label_SRblock1.Draw("same")
    Label_SRblock2 = ROOT.TLatex(0.298, 0.57, "OS-e#mu")
    Label_SRblock2.SetNDC()
    Label_SRblock2.SetTextFont(42)
    Label_SRblock2.SetTextSize(0.058)
    Label_SRblock2.Draw("same")
    Label_SRblock3 = ROOT.TLatex(0.498, 0.57, "OS-#mu#mu")
    Label_SRblock3.SetNDC()
    Label_SRblock3.SetTextFont(42)
    Label_SRblock3.SetTextSize(0.058)
    Label_SRblock3.Draw("same")
    Label_SRblock4 = ROOT.TLatex(0.598, 0.57, "SS-ee")
    Label_SRblock4.SetNDC()
    Label_SRblock4.SetTextFont(42)
    Label_SRblock4.SetTextSize(0.058)
    Label_SRblock4.Draw("same")
    Label_SRblock5 = ROOT.TLatex(0.748, 0.57, "SS-e#mu")
    Label_SRblock5.SetNDC()
    Label_SRblock5.SetTextFont(42)
    Label_SRblock5.SetTextSize(0.058)
    Label_SRblock5.Draw("same")
    Label_SRblock6 = ROOT.TLatex(0.898, 0.57, "SS-#mu#mu")
    Label_SRblock6.SetNDC()
    Label_SRblock6.SetTextFont(42)
    Label_SRblock6.SetTextSize(0.058)
    Label_SRblock6.Draw("same")

    SumofMC = hs.GetStack().Last()
    binwidth = array("d")
    bincenter = array("d")
    yvalue = array("d")
    yerrup = array("d")
    yerrdown = array("d")
    yvalueRatio = array("d")
    yerrupRatio = array("d")
    yerrdownRatio = array("d")
    for b in range(SumofMC.GetNbinsX()):
        if SumofMC.GetBinContent(b+1) > 0:
            binwidth.append(SumofMC.GetBinWidth(b+1)/2)
            bincenter.append(SumofMC.GetBinCenter(b+1))
            yvalue.append(SumofMC.GetBinContent(b+1))
            yerrup.append(SumofMC.GetBinError(b+1))
            yerrdown.append(SumofMC.GetBinError(b+1))
            yvalueRatio.append(1)
            yerrupRatio.append(SumofMC.GetBinError(b+1)/SumofMC.GetBinContent(b+1))
            yerrdownRatio.append(SumofMC.GetBinError(b+1)/SumofMC.GetBinContent(b+1))
    if len(bincenter)>0:
        error = ROOT.TGraphAsymmErrors(len(bincenter), bincenter, yvalue, binwidth, binwidth, yerrdown, yerrup)
        errorRatio = ROOT.TGraphAsymmErrors(len(bincenter), bincenter, yvalueRatio, binwidth, binwidth, yerrdownRatio, yerrupRatio)
    else:
        error = ROOT.TGraphAsymmErrors()
        errorRatio = ROOT.TGraphAsymmErrors()
    error.SetFillColor(13)
    error.SetLineColor(13)
    error.SetFillStyle(3004)
    error.SetLineWidth(4)
    error.Draw("2")

    label_cms = "CMS"
    Label_cms = ROOT.TLatex(0.08, 0.92, label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.SetTextSize(0.081)
    Label_cms.Draw()
    Label_cms1 = ROOT.TLatex(0.128, 0.92, PLOT_LABEL)
    Label_cms1.SetNDC()
    Label_cms1.SetTextSize(0.063)
    Label_cms1.SetTextFont(52)
    Label_cms1.Draw()
    Label_lumi = ROOT.TLatex(0.8314, 0.92, getLumi(year)+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.SetTextSize(0.063)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.1, 0.81, "2l+#tau_{h}, "+DOMAINS_NAME[iDomain])
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.SetTextSize(0.058)
    Label_channel.Draw("same")
    Label_region = ROOT.TLatex(0.1, 0.73, REGIONS_NAME[iRegion][0])
    Label_region.SetNDC()
    Label_region.SetTextFont(42)
    Label_region.SetTextSize(0.058)
    Label_region.Draw("same")
    Label_region2 = ROOT.TLatex(0.1, 0.65, REGIONS_NAME[iRegion][1])
    Label_region2.SetNDC()
    Label_region2.SetTextFont(42)
    Label_region2.SetTextSize(0.058)
    Label_region2.Draw("same")

    legend.AddEntry(dummy, Fnames[0], "ep")
    for num in range(1, len(hists)):
        if num<(len(hists)-2):
            legend.AddEntry(hists[num], Fnames[num], "F")
        else:
            legend2.AddEntry(hists[num], Fnames[num], "F")
    error.SetLineWidth(1)
    legend2.AddEntry(error, "Stat. only", "F")
    for H in range(len(SignalHists)):
        if H==0:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H]+" (#mu_{#scale[0.8]{ll`tu}}^{#scale[0.8]{scalar}} = 1)", "L")
        else:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H]+" (#mu_{#scale[0.8]{ll`tu}}^{#scale[0.8]{scalar}} = 100)", "L")
    legend.Draw("same")
    legend2.Draw("same")
    legend3.Draw("same")

    pad1.Update()

    pad2.cd()
    dummy_ratio = hists[0].Clone()
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetTitle("")
    dummy_ratio.SetMarkerStyle(20)
    dummy_ratio.SetMarkerSize(1.2)
    dummy_ratio.SetLineWidth(1)
    dummy_ratio.GetXaxis().SetTitle('')
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()
    dummy_ratio.GetYaxis().SetNoExponent()
    dummy_ratio.GetXaxis().SetTitleSize(0.05/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.05/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.115)
    dummy_ratio.GetYaxis().SetLabelSize(0.1125)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.004)
    dummy_ratio.GetYaxis().SetTitleOffset(0.17)
    dummy_ratio.GetXaxis().SetTitleOffset(0.9)
    dummy_ratio.GetYaxis().SetNdivisions(504)
    dummy_ratio.GetYaxis().SetRangeUser(0.2, 1.8)
    dummy_ratio.GetXaxis().SetBinLabel(1, "m(e#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(2, "m(e#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(3, "m(e#mu)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(4, "m(e#mu)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(5, "m(e#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(6, "m(e#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(7, "m(#mu#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(8, "m(#mu#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(9, "m(#mu#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(10, "m(#mu#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(11, "m(e#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(12, "m(e#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(13, "m(e#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(14, "m(e#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(15, "m(#mu#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(16, "m(#mu#tau)>150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(17, "m(#mu#tau)<150GeV")
    dummy_ratio.GetXaxis().SetBinLabel(18, "m(#mu#tau)>150GeV")
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle(r"#frac{Data}{Pred.}")
    dummy_ratio.Draw("E1")
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    errorRatio.SetFillColor(13)
    errorRatio.SetLineColor(13)
    errorRatio.SetFillStyle(3004)
    errorRatio.SetLineWidth(4)
    errorRatio.Draw("2")
    canvas.Print(saveDir+"/subSR.png")
    canvas.Print(saveDir+"/subSR.pdf")
    del canvas
    gc.collect()


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
                            hists.append(h[hkey])
                        makePlot(hists, year, charge, iChannel, iRegion, VARS1D_NAME[iVar], var,
                            charge+", "+CHANNELS_NAME[iChannel]+", "+DOMAINS_NAME[iDomain],
                            ARGS.FOLDER+"/"+year+"/"+region+"/"+domain+"/"+charge+"/"+channel)

# Make summary plots
for year in YEARS:
    for iRegion, region in enumerate(REGIONS):
        for iDomain, domain in enumerate(DOMAINS):
            H = []
            HSignal = []
            for iSample, sample in enumerate(SAMPLES):
                hkey = year+"_"+sample+"_OS_ee_"+region+"_"+domain+"_subSR"
                subSR = h[hkey].Clone()
                for charge in CHARGES:
                    for channel in CHANNELS:
                        if charge=="OS" and channel=="ee": continue
                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+domain+"_subSR"
                        subSR.Add(h[hkey].Clone(), 1.0)
                subSR.SetFillColor(COLORS[iSample])
                if "LFV" in sample:
                    subSR.SetLineColor(COLORS[iSample])
                    HSignal.append(subSR)
                else:
                    subSR.SetLineColor(COLORS[0])
                    H.append(subSR)
            SummaryPlot(H, HSignal, SAMPLES_NAME_SUMMARY, year, iRegion, region, iDomain,
                ARGS.FOLDER+"/"+year+"/"+region+"/"+domain)
