import os
import sys
from math import sqrt
from common import *


# Set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--y", dest="YEAR", default="RunII")
parser.add_argument("--p", dest="HISTPATH", default="")
ARGS = parser.parse_args()
YEARS = []
for year in YEARS_RUN2:
    if ARGS.YEAR==year or ARGS.YEAR=="RunII":
        YEARS.append(year)


# Read in histograms
HistAddress = os.path.dirname(sys.path[0])+"/hists"
if len(ARGS.HISTPATH)>0: HistAddress += "/"+ARGS.HISTPATH
files = {} # Keeps from losing "connection" to histograms
H1 = {}
for year in YEARS:
    for sample in SAMPLES:
        fname = HistAddress+"/"+year+"_"+sample+".root"
        print("Opening "+fname)
        files[year+"_"+sample] = ROOT.TFile.Open(fname)
        for region in REGIONS:
            for domain in DOMAINS:
                hname = year+"_"+region+"_"+domain+"_subSR_"+sample
                hSubSR = ROOT.TH1F(hname, "", 18, 0, 18)

                for charge in CHARGES:
                    for channel in CHANNELS:
                        hin = charge+"_"+channel+"_"+region+"_"+domain+"_subSR"
                        h = files[year+"_"+sample].Get(hin).Clone()
                        # Set negative event counts due to NLO low statistics to 0
                        for i in range(1, h.GetNbinsX()+1):
                            if h.GetBinContent(i)<0.0:
                                h.SetBinContent(i, 0.0)
                                h.SetBinError(i, 0.0)
                        # Set sub SR histogram bin contents and errors
                        if (charge=="OS") and (channel=="ee"):
                            hSubSR.SetBinContent(1, h.GetBinContent(1))
                            hSubSR.SetBinError(1, h.GetBinError(1))
                            hSubSR.SetBinContent(2, h.GetBinContent(2))
                            hSubSR.SetBinError(2, h.GetBinError(2))
                        elif (charge=="OS") and (channel=="emu"):
                            hSubSR.SetBinContent(3, h.GetBinContent(3))
                            hSubSR.SetBinError(3, h.GetBinError(3))
                            hSubSR.SetBinContent(4, h.GetBinContent(4))
                            hSubSR.SetBinError(4, h.GetBinError(4))
                            hSubSR.SetBinContent(5, h.GetBinContent(5))
                            hSubSR.SetBinError(5, h.GetBinError(5))
                            hSubSR.SetBinContent(6, h.GetBinContent(6))
                            hSubSR.SetBinError(6, h.GetBinError(6))
                            hSubSR.SetBinContent(7, h.GetBinContent(7))
                            hSubSR.SetBinError(7, h.GetBinError(7))
                            hSubSR.SetBinContent(8, h.GetBinContent(8))
                            hSubSR.SetBinError(8, h.GetBinError(8))
                        elif (charge=="OS") and (channel=="mumu"):
                            hSubSR.SetBinContent(9, h.GetBinContent(9))
                            hSubSR.SetBinError(9, h.GetBinError(9))
                            hSubSR.SetBinContent(10, h.GetBinContent(10))
                            hSubSR.SetBinError(10, h.GetBinError(10))
                        elif (charge=="SS") and (channel=="ee"):
                            hSubSR.SetBinContent(11, h.GetBinContent(11))
                            hSubSR.SetBinError(11, h.GetBinError(11))
                            hSubSR.SetBinContent(12, h.GetBinContent(12))
                            hSubSR.SetBinError(12, h.GetBinError(12))
                        elif (charge=="SS") and (channel=="emu"):
                            hSubSR.SetBinContent(13, h.GetBinContent(13))
                            hSubSR.SetBinError(13, h.GetBinError(13))
                            hSubSR.SetBinContent(14, h.GetBinContent(14))
                            hSubSR.SetBinError(14, h.GetBinError(14))
                            hSubSR.SetBinContent(15, h.GetBinContent(15))
                            hSubSR.SetBinError(15, h.GetBinError(15))
                            hSubSR.SetBinContent(16, h.GetBinContent(16))
                            hSubSR.SetBinError(16, h.GetBinError(16))
                        elif (charge=="SS") and (channel=="mumu"):
                            hSubSR.SetBinContent(17, h.GetBinContent(17))
                            hSubSR.SetBinError(17, h.GetBinError(17))
                            hSubSR.SetBinContent(18, h.GetBinContent(18))
                            hSubSR.SetBinError(18, h.GetBinError(18))
                H1[hname] = hSubSR # Save histogram


# Start LaTeX document
OutAddress = os.path.dirname(sys.path[0])+"/postproc/latex"
fout = open(OutAddress+"/CutFlowTables.tex", "w")
fout.write("\\documentclass{beamer}\n")
fout.write("\\usepackage[orientation = landscape, size = custom, width = 16, height = 12, scale = 0.5]{../latex-beamerposter/beamerposter}\n")
fout.write("\\usepackage{multicol}\n")
fout.write("\\usepackage{lmodern}\n")
fout.write("\n")
fout.write("\\title{\\textbf{Cutflow Tables}}\n")
fout.write("\\author{Author}\n")
fout.write("\n")
fout.write("\\begin{document}\n")
fout.write("\n")
fout.write("  \\begin{frame}\n")
fout.write("    \\maketitle\n")
fout.write("  \\end{frame}\n")
fout.write("\n")
fout.write("  \\begin{frame}{\\textbf{Table of contents}}\n")
fout.write("    \\fontsize{4}{4}\n")
fout.write("    \\begin{multicols}{3}\n")
fout.write("      \\tableofcontents\n")
fout.write("    \\end{multicols}{1}\n")
fout.write("  \\end{frame}\n")
fout.write("\n")

# Get counts
for year in YEARS:
    print("Processing "+year)
    firstOfYear = True
    for r, region in enumerate(REGIONS):
        for d, domain in enumerate(DOMAINS):
            # Initialize containers for cut flow table
            cutFlow = [
                [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], []] # 18
            for arr in cutFlow:
                for i in range(10):
                    arr.append(0.0)
            cutFlowErr = [
                [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], []] # 18
            for arr in cutFlowErr:
                for i in range(9):
                    arr.append(0.0)

            # Calculate cut flow table
            for b in range(H1[hname].GetNbinsX()):
                # Fill from samples
                for s, sample in enumerate(SAMPLES):
                    hname = year+"_"+region+"_"+domain+"_subSR_"+sample
                    cutFlow[b][s] = H1[hname].GetBinContent(b+1)
                    cutFlowErr[b][s] = H1[hname].GetBinError(b+1)
                # Calculate background
                cutFlow[b][7] = cutFlow[b][1] + cutFlow[b][2] + cutFlow[b][3] + cutFlow[b][4]
                cutFlowErr[b][7] = sqrt(
                    cutFlowErr[b][1] * cutFlowErr[b][1] +
                    cutFlowErr[b][2] * cutFlowErr[b][2] +
                    cutFlowErr[b][3] * cutFlowErr[b][3] +
                    cutFlowErr[b][4] * cutFlowErr[b][4])
                # Calculate signal
                cutFlow[b][8] = cutFlow[b][5] + cutFlow[b][6]
                cutFlowErr[b][8] = sqrt(
                    cutFlowErr[b][5] * cutFlowErr[b][5] +
                    cutFlowErr[b][6] * cutFlowErr[b][6])
                # Calculate S/sqrt(B)
                if cutFlow[b][7] != 0:
                    cutFlow[b][9] = cutFlow[b][8] / sqrt(cutFlow[b][7])

            # Writing cutFlow table to LaTeX format
            if firstOfYear:
                fout.write("  \\section{" + year + "}\n")
                fout.write("\n")
                firstOfYear = False
            fout.write("  \\subsection{2$l+\\tau_h$, " + DOMAINS_LATEX[d] + ", " + REGIONS_LATEX[r] + "}\n")
            fout.write("  \\begin{frame}{\\textbf{" + year + "}}\n")
            fout.write("    \\small\n")
            fout.write("    \\begin{itemize}\n")
            fout.write("      \\item 2$l+\\tau_h$, " + DOMAINS_LATEX[d] + ", " + REGIONS_LATEX[r] + "\n")
            fout.write("    \\end{itemize}\n")
            fout.write("    \\makebox[\\textwidth]{\n")
            fout.write("      \\tiny\n")
            fout.write("      \\begin{tabular}{ | l | l | l | l | l | l | l | }\n")
            fout.write("        \\hline\n")
            fout.write("        Mass & OS-$ee$ & OS-$ee$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ \\\\\n")
            fout.write("        Region & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV & $m(e\\mu)<150$GeV & $m(e\\mu)>150$GeV & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV \\\\\n")
            fout.write("        \\hline\n")
            for s in range(len(TABLE_LATEX)):
                if (s == 5) or (s == 6) or (s == 8):
                    fout.write("        " + TABLE_LATEX[s]
                        + " & %.4f$\\pm$%.4f" % (cutFlow[0][s], cutFlowErr[0][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[1][s], cutFlowErr[1][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[2][s], cutFlowErr[2][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[3][s], cutFlowErr[3][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[4][s], cutFlowErr[4][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[5][s], cutFlowErr[5][s])
                        + " \\\\\n")
                else:
                    fout.write("        " + TABLE_LATEX[s]
                        + " & %.2f$\\pm$%.2f" % (cutFlow[0][s], cutFlowErr[0][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[1][s], cutFlowErr[1][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[2][s], cutFlowErr[2][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[3][s], cutFlowErr[3][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[4][s], cutFlowErr[4][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[5][s], cutFlowErr[5][s])
                        + " \\\\\n")
                if (s == 0) or (s == 4) or (s == 6) or (s == 8):
                    fout.write("        \\hline\n")
            fout.write("        $S/\\sqrt{B}$"
                + " & %.4f" % cutFlow[0][9]
                + " & %.4f" % cutFlow[1][9]
                + " & %.4f" % cutFlow[2][9]
                + " & %.4f" % cutFlow[3][9]
                + " & %.4f" % cutFlow[4][9]
                + " & %.4f" % cutFlow[5][9]
                + " \\\\\n")
            fout.write("        \\hline\n")
            fout.write("        \\hline\n")
            fout.write("        Mass & OS-$e\\mu$ & OS-$e\\mu$ & OS-$\\mu\\mu$ & OS-$\\mu\\mu$ & SS-$ee$ & SS-$ee$ \\\\\n")
            fout.write("        Region & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV \\\\\n")
            fout.write("        \\hline\n")
            for s in range(len(TABLE_LATEX)):
                if (s == 5) or (s == 6) or (s == 8):
                    fout.write("        " + TABLE_LATEX[s]
                        + " & %.4f$\\pm$%.4f" % (cutFlow[6][s], cutFlowErr[6][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[7][s], cutFlowErr[7][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[8][s], cutFlowErr[8][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[9][s], cutFlowErr[9][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[10][s], cutFlowErr[10][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[11][s], cutFlowErr[11][s])
                        + " \\\\\n")
                else:
                    fout.write("        " + TABLE_LATEX[s]
                        + " & %.2f$\\pm$%.2f" % (cutFlow[6][s], cutFlowErr[6][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[7][s], cutFlowErr[7][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[8][s], cutFlowErr[8][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[9][s], cutFlowErr[9][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[10][s], cutFlowErr[10][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[11][s], cutFlowErr[11][s])
                        + " \\\\\n")
                if (s == 0) or (s == 4) or (s == 6) or (s == 8):
                    fout.write("        \\hline\n")
            fout.write("        $S/\\sqrt{B}$"
                + " & %.4f" % cutFlow[6][9]
                + " & %.4f" % cutFlow[7][9]
                + " & %.4f" % cutFlow[8][9]
                + " & %.4f" % cutFlow[9][9]
                + " & %.4f" % cutFlow[10][9]
                + " & %.4f" % cutFlow[11][9]
                + " \\\\\n")
            fout.write("        \\hline\n")
            fout.write("        \\hline\n")
            fout.write("        Mass & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$\\mu\\mu$ & SS-$\\mu\\mu$ \\\\\n")
            fout.write("        Region & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV \\\\\n")
            fout.write("        \\hline\n")
            for s in range(len(TABLE_LATEX)):
                if (s == 5) or (s == 6) or (s == 8):
                    fout.write("        " + TABLE_LATEX[s]
                        + " & %.4f$\\pm$%.4f" % (cutFlow[12][s], cutFlowErr[12][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[13][s], cutFlowErr[13][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[14][s], cutFlowErr[14][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[15][s], cutFlowErr[15][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[16][s], cutFlowErr[16][s])
                        + " & %.4f$\\pm$%.4f" % (cutFlow[17][s], cutFlowErr[17][s])
                        + " \\\\\n")
                else:
                    fout.write("        " + TABLE_LATEX[s]
                        + " & %.2f$\\pm$%.2f" % (cutFlow[12][s], cutFlowErr[12][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[13][s], cutFlowErr[13][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[14][s], cutFlowErr[14][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[15][s], cutFlowErr[15][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[16][s], cutFlowErr[16][s])
                        + " & %.2f$\\pm$%.2f" % (cutFlow[17][s], cutFlowErr[17][s])
                        + " \\\\\n")
                if (s == 0) or (s == 4) or (s == 6) or (s == 8):
                    fout.write("        \\hline\n")
            fout.write("        $S/\\sqrt{B}$"
                + " & %.4f" % cutFlow[12][9]
                + " & %.4f" % cutFlow[13][9]
                + " & %.4f" % cutFlow[14][9]
                + " & %.4f" % cutFlow[15][9]
                + " & %.4f" % cutFlow[16][9]
                + " & %.4f" % cutFlow[17][9]
                + " \\\\\n")
            fout.write("        \\hline\n")
            fout.write("      \\end{tabular}\n")
            fout.write("    }\n")
            fout.write("  \\end{frame}\n")
            fout.write("\n")

# End LaTeX document
fout.write("\\end{document}\n")
fout.close()
