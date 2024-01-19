import argparse
import os
import sys
import uproot
import numpy as np
import cmsstyle as CMS
import ROOT
import gc


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018"]
SAMPLES = ["Data", "TX", "VV", "DY", "TT", "LFVStScalarU", "LFVTtScalarU"]
SAMPLES_NAME = ["Data", r"t\bar{t}+X", "VV(V)", "DY/ZZ", r"t\bar{t}/WW",
    r"CLFV top production (\mu_{ll'tu}^{scalar} = 0.5)",
    r"CLFV top decay (\mu_{ll'tu}^{scalar} = 20)"]
CHARGES = ["OS", "SS"]
CHANNELS = ["ee", "emu", "mumu"]
CHANNELS_NAME = [r"ee\tau_{h}", r"e\mu\tau_{h}", r"\mu\mu\tau_{h}"]
REGIONS = ["ll", "llStl300", "llMetg20Jetgeq1B0"]
REGIONS_NAME = [
    ("No cuts", ""),
    (r"S_{T} < 300 GeV (CR)", ""),
    (r"p_{T}^{miss} > 20 GeV, njet #geq 1,", "nbjet = 0 (CR)")]
DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa"]
DOMAINS_NAME = [r"#geq Tight Tau", r"< Tight Tau"]
VARS = [
    "llM", "llDr", "lep1Pt", "lep2Pt", "elLeptonMVAv1", "elLeptonMVAv2", "muLeptonMVAv1", "muLeptonMVAv2",
    "taPt", "taPtFake", "taEta", "taEtaFake", "taVsJetWP", "taVsJetMVA", "taVsElMVA", "taVsMuMVA", "taDxy",
    "taDz", "taDecayMode", "jet1Pt", "jetbtagDeepFlavB", "njet", "nbjet", "MET", "subSR", "LFVemuM",
    "LFVetaM", "LFVmutaM", "LFVemuDr", "LFVetaDr", "LFVmutaDr", "LFVePt", "LFVmuPt", "LFVtaPt", "balepPt",
    "topmass", "Ht", "St", "btagSum"]
VARS_NAME = [
    "m(l#bar{l}) [GeV]", "#DeltaR(l#bar{l})", "Leading lepton p_{T} [GeV]", "Sub-leading lepton p_{T} [GeV]",
    "Electron Top Lepton MVA (v1)", "Electron Top Lepton MVA (v2)", "Muon Top Lepton MVA (v1)",
    "Muon Top Lepton MVA (v2)", "#tau p_{T} [GeV]", "Fake #tau p_{T} [GeV]", "#tau #eta", "Fake #tau #eta",
    "#tau vs Jet WP", "#tau vs Jet MVA", "#tau vs Electron MVA", "#tau vs Muon MVA", "#tau d_{xy} [cm]",
    "#tau d_{z} [cm]", "#tau Decay Mode", "Leading jet p_{T} [GeV]", "btag", "njet", "nbjet (Loose WP)",
    "MET [GeV]", "SR subdivided", "m(e#bar{#mu}) [GeV]", "m(e#bar{#tau}) [GeV]", "m(#mu#bar{#tau}) [GeV]",
    "#DeltaR(e,#bar{#mu}) [GeV]", "#DeltaR(e,#bar{#tau}) [GeV]", "#DeltaR(#mu,#bar{#tau}) [GeV]",
    "LFV electron p_{T} [GeV]", "LFV muon p_{T} [GeV]", "LFV tau p_{T} [GeV]", "Bachelor lepton p_{T} [GeV]",
    "m(top) [GeV]", "H_{T} [GeV]", "S_{T} [GeV]", "Sum of btagging scores"]
COLORS = [ROOT.kBlack, ROOT.kRed - 4, ROOT.kOrange - 3, ROOT.kGreen, ROOT.kYellow, ROOT.kViolet + 1, ROOT.kGray]

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
                    for domain in DOMAINS:
                        for var in VARS:
                            hname = charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            temp = file[hname].to_pyroot().Clone()
                            # underflow and overflow
                            temp.SetBinContent(1, temp.GetBinContent(0)+temp.GetBinContent(1))
                            temp.SetBinContent(temp.GetXaxis().GetNbins(),
                                temp.GetBinContent(temp.GetXaxis().GetNbins())+temp.GetBinContent(temp.GetXaxis().GetNbins()+1))
                            h[year+"_"+sample+"_"+hname] = temp
        file.close()


def makePlot(hists, year, charge, iChannel, channel, iRegion, region, iVar, var, iDomain=-1, domain=""):
    CMS.SetLumi(getLumi(year))
    CMS.SetEnergy("13") # Run 2

    # make MC and signal histograms
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

    # calculate data/pred. ratio
    ratioHist = hists[0].Clone()
    ratioHist.Divide(MCHists[-1].Clone())

    # get error on MC and ratio
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

    # get x_min and x_max
    x_min = hists[0].GetBinLowEdge(1)
    x_max = hists[0].GetBinLowEdge(hists[0].GetNbinsX())+hists[0].GetBinWidth(hists[0].GetNbinsX())
    # get y_min and y_max
    y_max = hists[0].GetMaximum()
    true_y_min = 1e10
    for hist in hists:
        true_y_min = min(true_y_min, hist.GetMinimum(0.0))
    y_min = true_y_min/2.0
    y_max = 2000*max(y_max, MCHists[-1].GetMaximum())

    dicanv = CMS.cmsDiCanvas(var,
        x_min, x_max, y_min, y_max, 0.2, 1.8,
        VARS_NAME[iVar], "Events", "Data/Pred.",
        square=square, extraSpace=0.1, iPos=0)
    dicanv.cd(1).SetLogy(True)

    # draw histograms
    for iHist, loopHist in enumerate(reversed(MCHists)):
        CMS.cmsDraw(loopHist, "hist", fcolor=COLORS[1+iHist])
    CMS.cmsDraw(MCErrorHist, "E2", fstyle=3004, fcolor=COLORS[0])
    CMS.cmsDraw(hists[0], "P EX0", fcolor=COLORS[0], lwidth=2)
    for iHist, loopHist in enumerate(SigHists):
        CMS.cmsDraw(loopHist, "hist", lcolor=COLORS[1+len(MCHists)+iHist], fcolor=0, lwidth=3, lstyle=iHist+1)

    # draw legend
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

    # add charge, channel, region labels
    if square:
        legLabelTop = CMS.cmsLeg(0.18, 0.83, 0.5, 0.89, textSize=0.04)
        legLabelMiddle = CMS.cmsLeg(0.18, 0.77, 0.5, 0.83, textSize=0.04)
        legLabelBottom = CMS.cmsLeg(0.18, 0.71, 0.5, 0.77, textSize=0.04)
    else:
        legLabelTop = CMS.cmsLeg(0.15, 0.82, 0.5, 0.88, textSize=0.05)
        legLabelMiddle = CMS.cmsLeg(0.15, 0.76, 0.5, 0.82, textSize=0.05)
        legLabelBottom = CMS.cmsLeg(0.15, 0.7, 0.5, 0.76, textSize=0.05)
    CMS.cmsHeader(legLabelTop, charge+", "+CHANNELS_NAME[iChannel]+", "+DOMAINS_NAME[iDomain], textSize=0.04)
    CMS.cmsHeader(legLabelMiddle, REGIONS_NAME[iRegion][0], textSize=0.04)
    CMS.cmsHeader(legLabelBottom, REGIONS_NAME[iRegion][1], textSize=0.04)

    # draw MC relative error and ratio plot + reference lines
    dicanv.cd(2)
    CMS.cmsDraw(MCRelError, "E2", fstyle=3004, fcolor=COLORS[0])
    CMS.cmsDraw(ratioHist, "P EX0", fcolor=COLORS[0], lwidth=2)
    upLine = ROOT.TLine(x_min, 1.5, x_max, 1.5)
    midLine = ROOT.TLine(x_min, 1, x_max, 1)
    downLine = ROOT.TLine(x_min, 0.5, x_max, 0.5)
    CMS.cmsDrawLine(upLine, lcolor=COLORS[0], lstyle=ROOT.kDotted)
    CMS.cmsDrawLine(midLine, lcolor=COLORS[0], lstyle=ROOT.kDotted)
    CMS.cmsDrawLine(downLine, lcolor=COLORS[0], lstyle=ROOT.kDotted)

    if not os.path.exists(ARGS.FOLDER):
        os.makedirs(ARGS.FOLDER)
    if not os.path.exists(ARGS.FOLDER+"/"+year):
        os.makedirs(ARGS.FOLDER+"/"+year)
    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+charge):
        os.makedirs(ARGS.FOLDER+"/"+year+"/"+charge)
    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel):
        os.makedirs(ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel)
    if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel+"/"+region):
        os.makedirs(ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel+"/"+region)
    if iDomain>=0:
        if not os.path.exists(ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel+"/"+region+"/"+domain):
            os.makedirs(ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel+"/"+region+"/"+domain)
        CMS.SaveCanvas(dicanv, ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel+"/"+region+"/"+domain+"/"+var+".pdf")
    else:
        CMS.SaveCanvas(dicanv, ARGS.FOLDER+"/"+year+"/"+charge+"/"+channel+"/"+region+"/"+var+".pdf")
    del dicanv
    gc.collect()


for year in YEARS:
    for charge in CHARGES:
        for iChannel, channel in enumerate(CHANNELS):
            for iRegion, region in enumerate(REGIONS):
                for iVar, var in enumerate(VARS):
                    for iDomain, domain in enumerate(DOMAINS):
                        hists = []
                        for iSample, sample in enumerate(SAMPLES):
                            hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+domain+"_"+var
                            hists.append(h[hkey])
                        makePlot(hists, year, charge, iChannel, channel, iRegion, region, iVar, var, iDomain, domain)
