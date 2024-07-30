import numpy as np
import gc
from math import sqrt
from array import array
from common import *


ROOT.gROOT.SetBatch(1)


def plot1D(year, hists, labels, xlabel, ylabel, ylabelNorm, ylabelRatio, legHeader, log, saveName):
    CMS.SetLumi(getLumi(year))
    CMS.SetEnergy("13") # Run 2
    CMS.SetExtraText(PLOT_LABEL)

    left = hists[0].GetBinLowEdge(1)
    right = hists[0].GetBinLowEdge(hists[0].GetNbinsX() + 1)
    maxi = -1.0
    for hist in hists:
        maxi = max(maxi, hist.GetMaximum())

    canv = CMS.cmsCanvas(saveName,
        left,
        right,
        0.8 if log else 0,
        50 * maxi if log else 1.1 * maxi,
        xlabel, ylabel, square=CMS.kRectangular, extraSpace=0.01, iPos=0)
    canv.SetLogy(log)
    leg = CMS.cmsLeg(0.55, 0.89 - 0.04 * 8, 0.89, 0.89, textSize=0.04)
    if legHeader: CMS.cmsHeader(leg, legHeader, textSize=0.04)

    for iHist, hist in enumerate(hists):
        CMS.cmsDraw(hist, "hist", mcolor=COLORS[iHist+1], fstyle=0, lwidth=3)
        label = labels[iHist]
        leg.AddEntry(hist, label, "L")

    CMS.GetcmsCanvasHist(canv).GetXaxis().SetTitleOffset(1.2)
    CMS.GetcmsCanvasHist(canv).GetXaxis().SetLabelSize(0.04)
    CMS.GetcmsCanvasHist(canv).GetXaxis().SetTitleSize(0.05)
    CMS.GetcmsCanvasHist(canv).GetYaxis().SetTitleOffset(1.1)
    CMS.GetcmsCanvasHist(canv).GetYaxis().SetLabelSize(0.04)
    CMS.GetcmsCanvasHist(canv).GetYaxis().SetTitleSize(0.05)
    CMS.GetcmsCanvasHist(canv).GetYaxis().SetMaxDigits(2)
    CMS.GetcmsCanvasHist(canv).GetYaxis().SetNoExponent()

    CMS.SaveCanvas(canv, saveName + ".png", close=False)
    CMS.SaveCanvas(canv, saveName + ".pdf")


def plot1DStack(hists, year, charge, iChannel, iRegion, varName, var, topLabel, saveDir):
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
    y_min = 0.6
    y_max = 5000*max(y_max, MCHists[-1].GetMaximum(),y_min)

    dicanv = CMS.cmsDiCanvas(var,
        x_min, x_max, y_min, y_max, 0.2, 1.8,
        varName, "Events", "Data/Pred.",
        square=SQUARE, extraSpace=0.1, iPos=0)
    dicanv.cd(1).SetLogy(True)

    # Draw histograms
    for iHist, loopHist in enumerate(reversed(MCHists)):
        CMS.cmsDraw(loopHist, "hist", fcolor=COLORS[1+iHist])
    CMS.cmsDraw(MCErrorHist, "E2", fstyle=3004, fcolor=COLORS[0])
    CMS.cmsDraw(hists[0], "P EX0", fcolor=COLORS[0], lwidth=2)
    for iHist, loopHist in enumerate(SigHists):
        CMS.cmsDraw(loopHist, "hist", lcolor=COLORS[1+len(MCHists)+iHist], fcolor=0, lwidth=3, lstyle=iHist+1)
    ROOT.gPad.RedrawAxis()

    # Draw legend
    if SQUARE:
        legData = CMS.cmsLeg(0.41, 0.83, 0.56, 0.89, textSize=0.04)
        legLeft = CMS.cmsLeg(0.56, 0.65, 0.71, 0.89, textSize=0.04)
        legRight = CMS.cmsLeg(0.71, 0.65, 0.86, 0.89, textSize=0.04)
        legBottom = CMS.cmsLeg(0.37, 0.53, 0.89, 0.65, textSize=0.04)
    else:
        legData = CMS.cmsLeg(0.45, 0.64, 0.60, 0.88, textSize=0.04)
        legLeft = CMS.cmsLeg(0.60, 0.64, 0.75, 0.88, textSize=0.05)
        legRight = CMS.cmsLeg(0.75, 0.64, 0.87, 0.88, textSize=0.05)
        legBottom = CMS.cmsLeg(0.43, 0.52, 0.9, 0.64, textSize=0.05)
    legData.AddEntry(hists[0], SAMPLES_NAME[0], "P EX0")
    for iHist, loopHist in enumerate(MCHists):
        if iHist < (len(MCHists)/2):
            legLeft.AddEntry(loopHist, SAMPLES_NAME[1+iHist], "f")
        else:
            legRight.AddEntry(loopHist, SAMPLES_NAME[1+iHist], "f")
    for iHist, loopHist in enumerate(SigHists):
        legBottom.AddEntry(loopHist, SAMPLES_NAME[1+len(MCHists)+iHist], "l")

    # Add charge, channel, region labels
    if SQUARE:
        legLabelTop = CMS.cmsLeg(0.18, 0.83, 0.5, 0.89, textSize=0.04)
        legLabelMiddle = CMS.cmsLeg(0.18, 0.77, 0.5, 0.83, textSize=0.04)
        legLabelBottom = CMS.cmsLeg(0.18, 0.71, 0.5, 0.77, textSize=0.04)
    else:
        legLabelTop = CMS.cmsLeg(0.15, 0.82, 0.5, 0.88, textSize=0.05)
        legLabelMiddle = CMS.cmsLeg(0.15, 0.76, 0.5, 0.82, textSize=0.05)
        legLabelBottom = CMS.cmsLeg(0.15, 0.7, 0.5, 0.76, textSize=0.05)
    CMS.cmsHeader(legLabelTop, topLabel, textSize=0.04)
    CMS.cmsHeader(legLabelMiddle, REGIONS_NAME[iRegion][0], textSize=0.04)
    regName = REGIONS_NAME[iRegion][1]
    if ('OnZ' in REGIONS_NAME[iRegion][1] and 'SS' in charge): regName = 'ChargMisID CR'
    CMS.cmsHeader(legLabelBottom, regName, textSize=0.04)

    # Draw MC relative error and ratio plot + reference lines
    dicanv.cd(2)
    legRatio = CMS.cmsLeg(0.2, 0.75, 0.35, 0.87, textSize=0.06)
    legRatio.AddEntry(MCErrorHist, "Stat. only", "f")
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


def plot2D(hist, year, xlabel, ylabel, zlabel, logz, saveName):
    CMS.SetLumi(getLumi(year))

    xmin = hist.GetXaxis().GetBinLowEdge(1)
    xmax = hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX() + 1)
    ymin = hist.GetYaxis().GetBinLowEdge(1)
    ymax = hist.GetYaxis().GetBinLowEdge(hist.GetNbinsY() + 1)

    canv = CMS.cmsCanvas(saveName, xmin, xmax, ymin, ymax, xlabel, ylabel,
        square=CMS.kSquare, extraSpace=0.01, iPos=0, with_z_axis=True, scaleLumi=0.8)

    hist.GetZaxis().SetTitle(zlabel)
    hist.GetZaxis().SetTitleOffset(1.4)
    hist.Draw("same colz text45 e")
    hist.SetMarkerColor(ROOT.kRed)
    ROOT.gStyle.SetPaintTextFormat("4.3f");
    if logz: canv.SetLogz()

    CMS.SetCMSPalette()
    CMS.UpdatePalettePosition(hist, canv) # Adjust palette position

    CMS.SaveCanvas(canv, saveName + ".png", close=False)
    CMS.SaveCanvas(canv, saveName + ".pdf")


def plotSummary(hists, SignalHists, Fnames, year, iRegion, region, saveDir):
    ROOT.gStyle.SetErrorX(0) # No horizontal error bar
    ROOT.gStyle.SetEndErrorSize(0)
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

    legend0 = ROOT.TLegend(0.38, 0.68, 0.45, 0.87)
    legend0.SetBorderSize(0)
    legend0.SetFillStyle(0)
    legend0.SetTextFont(42)
    legend0.SetTextSize(0.05)
    legend1 = ROOT.TLegend(0.48, 0.68, 0.55, 0.87)
    legend1.SetBorderSize(0)
    legend1.SetFillStyle(0)
    legend1.SetTextFont(42)
    legend1.SetTextSize(0.05)
    legend2 = ROOT.TLegend(0.58, 0.68, 0.65, 0.87)
    legend2.SetBorderSize(0)
    legend2.SetFillStyle(0)
    legend2.SetTextFont(42)
    legend2.SetTextSize(0.05)
    legend3 = ROOT.TLegend(0.68, 0.75, 0.90, 0.87)
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
            SignalHists[H].Scale(20)
        else:
            SignalHists[H].Scale(0.5)

    y_max = hists[0].GetMaximum()
    if y_max < hs.GetStack().Last().GetMaximum():
        y_max = hs.GetStack().Last().GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetLineWidth(1)
    x_min = hists[0].GetXaxis().GetBinLowEdge(1)
    x_max = hists[0].GetXaxis().GetBinLowEdge(hists[0].GetXaxis().GetNbins())+hists[0].GetXaxis().GetBinWidth(hists[0].GetXaxis().GetNbins())

    frame = pad1.DrawFrame(x_min, 0.6, x_max, 6000*y_max)
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
    error.SetFillStyle(3154)
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
    Label_channel = ROOT.TLatex(0.1, 0.81, "2l+#tau_{h}")
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

    legend0.AddEntry(dummy, Fnames[0], "ep")
    for num in range(1, len(hists)):
        if num<3:
            legend0.AddEntry(hists[num], Fnames[num], "F")
        elif num<6:
            legend1.AddEntry(hists[num], Fnames[num], "F")
        else: legend2.AddEntry(hists[num], Fnames[num], "F")
    error.SetLineWidth(1)
    for H in range(len(SignalHists)):
        if H==0:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H], "L")
        else:
            legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H], "L")
    legend0.Draw("same")
    legend1.Draw("same")
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
    errorRatio.SetFillStyle(3154)
    errorRatio.SetLineWidth(4)
    errorRatio.Draw("2")
    errorRatio.SetLineWidth(1)
    legend5 = ROOT.TLegend(0.1, 0.735, 0.17, 0.875)
    legend5.SetBorderSize(0)
    legend5.SetFillStyle(0)
    legend5.SetTextColor(1)
    legend5.SetTextFont(42)
    legend5.SetTextSize(0.11)
    legend5.AddEntry(errorRatio, "Stat. Only", "F")
    legend5.Draw("same")
    canvas.Print(saveDir+"/Summary_"+region+".png")
    canvas.Print(saveDir+"/Summary_"+region+".pdf")
    del canvas
    gc.collect()
