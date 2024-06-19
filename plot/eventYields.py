from math import sqrt, nan
from ctypes import c_double


# calculates event yields and prints them in LaTeX table format
def getEventYields(Hists, samples, samplesName, domains, domainsName, charges, channels, year, regions, regionsName):

    nBins = len(charges)*len(channels) # 0:OS-e, 1:OS-mu, 2:SS-e, 3:SS-mu
    rows = samples.copy()
    rows.append("total")
    rowsName = samplesName.copy()
    rowsName.append("Total")

    # initialize counts, errors, and totals
    counts = {}
    for f in rows:
        for region in regions:
            for domain in domains:
                for b in range(nBins):
                    counts[f+"_"+region+"_"+domain+"_"+str(b)] = [0.0, 0.0, -1.0] # [count, error, %]

    # get counts and errors for each sample & MC total
    for sample in samples:
        for region in regions:
            for domain in domains:
                for iCharge, charge in enumerate(charges):
                    for iChannel, channel in enumerate(channels):
                        hkey = year+"_"+sample+"_"+charge+"_"+channel+"_"+region+"_"+domain+"_taPt" # pick a var that every event will have
                        h = Hists[hkey].Clone()
                        b = len(charges)*iCharge+iChannel
                        error = c_double()
                        integral = h.IntegralAndError(1, h.GetNbinsX(), error)
                        counts[sample+"_"+region+"_"+domain+"_"+str(b)][0] = integral
                        counts[sample+"_"+region+"_"+domain+"_"+str(b)][1] = error.value
                        if "Data" not in sample:
                            counts["total_"+region+"_"+domain+"_"+str(b)][0] += integral
                            counts["total_"+region+"_"+domain+"_"+str(b)][1] += error.value*error.value
    for region in regions:
        for domain in domains:
            for b in range(nBins):
                error = sqrt(counts["total_"+region+"_"+domain+"_"+str(b)][1])
                counts["total_"+region+"_"+domain+"_"+str(b)][1] = error
    for sample in samples:
        for region in regions:
            for domain in domains:
                for b in range(nBins):
                    denominator = counts["total_"+region+"_"+domain+"_"+str(b)][0]
                    if denominator > 0.0:
                        fraction = counts[sample+"_"+region+"_"+domain+"_"+str(b)][0]/denominator
                        counts[sample+"_"+region+"_"+domain+"_"+str(b)][2] = fraction*100.0
                    else:
                        counts[sample+"_"+region+"_"+domain+"_"+str(b)][2] = nan # technically undefined

    # Stuff for beginning .tex file
    tex = ""
    tex += "\\documentclass{beamer}\n"
    tex += "\\usepackage[orientation = landscape, size = custom, width = 16, height = 12, scale = 0.5, debug]{beamerposter}\n"
    tex += "\n"
    tex += "\\title{\\textbf{Event yield tables}}\n"
    tex += "\\author{Your name here}\n"
    tex += "\n"
    tex += "\\begin{document}\n"
    tex += "\n"
    tex += "  \\begin{frame}\n"
    tex += "    \\maketitle\n"
    tex += "  \\end{frame}\n"

    # slide defining all regions
    tex += "\n"
    tex += "  \\begin{frame}{\\textbf{Regions}}\n"
    tex += "    \\begin{enumerate}\n"
    for iRegion, rName in enumerate(regionsName):
        tex += "      \\item (" + str(iRegion + 1) + ") " + rName + "\n"
    tex += "    \\end{enumerate}\n"
    tex += "  \\end{frame}\n"

    # event yield tables -- 1 table per slide
    for iRegion, region in enumerate(regions):
        for iDomain, domain in enumerate(domains):
            tex += "\n"
            tex += "  \\begin{frame}{\\textbf{Event yields}}\n"
            tex += "    \\begin{itemize}\n"
            tex += "      \\item (" + str(iRegion + 1) + ") " + regionsName[iRegion] + ", " + domainsName[iDomain] + "\n"
            tex += "    \\end{itemize}\n"
            tex += "    \\resizebox{0.99\\textwidth}{!}{\n"
            tex += "      \\begin{tabular}{|l|l|l|l|l|}\n"
            tex += "        \\hline\n"
            tex += "        Channel & OS-$e$ & OS-$\\mu$ & SS-$e$ & SS-$\\mu$ \\\\\n"
            tex += "        \\hline\n"
            for iRow, f in enumerate(rows):
                tex += "        " + rowsName[iRow]
                for iCharge, charge in enumerate(charges):
                    for iChannel, channel in enumerate(channels):
                        b = len(charges)*iCharge+iChannel
                        nEvt = counts[f+"_"+region+"_"+domain+"_"+str(b)][0]
                        err = counts[f+"_"+region+"_"+domain+"_"+str(b)][1]
                        if (nEvt > 0) and (nEvt < 10):
                            tex += (" & %.2f" % nEvt)+("$\\pm$%.2f" % err)
                        else:
                            tex += (" & %.0f" % nEvt)+("$\\pm$%.0f" % err)
                        if f != "Data" and f != "total":
                            tex += " [%.2f\\%%]" % counts[f+"_"+region+"_"+domain+"_"+str(b)][2]
                tex += " \\\\\n"
                if f == "Data" or f == "TT":
                    tex += "        \\hline\n"
            tex += "        \\hline\n"
            tex += "      \\end{tabular}\n"
            tex += "    }\n"
            tex += "  \\end{frame}\n"

    # stuff for ending .tex file
    tex += "\n"
    tex += "\\end{document}\n"

    # open, write to, and close output text file
    outFile = open("eventYields" + year + ".tex", "w")
    outFile.write(tex)
    outFile.close()
    print("eventYields" + year + ".tex")
