from math import sqrt

# Calculates background estimates and prints them in LaTeX table format
# TODO: Expand this to have multiple cuts
def BackgroundEstimate(Hists2D, numyear, numsample, numsubsamples, numc, numch, numreg, numvar2D, numsubvar2D,
                       xcut, ycut, cut1, cut2, cut3, cut4, filename):

    # Get particles
    H2 = Hists2D[numyear][numsample][numc][numch][numreg][numvar2D].Clone()

    # Subtract MC particles
    for numsubsample in numsubsamples:
        subH2 = Hists2D[numyear][numsubsample][numc][numch][numreg][numsubvar2D].Clone()
        H2.Add(subH2, -1.0)

    # Do the actual background estimate
    nxBins = H2.GetXaxis().GetNbins()
    nyBins = H2.GetYaxis().GetNbins()
    numA = 0.0
    errA = 0.0
    for xidx in range(1, xcut + 1): # Left
        for yidx in range(ycut + 1, nyBins + 1): # Top
            numA += H2.GetBinContent(xidx, yidx)
            errA += H2.GetBinError(xidx, yidx) * H2.GetBinError(xidx, yidx)
    errA = sqrt(errA)
    numC = 0.0
    errC = 0.0
    for xidx in range(1, xcut + 1): # Left
        for yidx in range(1, ycut + 1): # Bottom
            numC += H2.GetBinContent(xidx, yidx)
            errC += H2.GetBinError(xidx, yidx) * H2.GetBinError(xidx, yidx)
    errC = sqrt(errC)
    numB = 0.0 # Signal
    errB = 0.0
    for xidx in range(xcut + 1, nxBins + 1): # Right
        for yidx in range(ycut + 1, nyBins + 1): # Top
            numB += H2.GetBinContent(xidx, yidx)
            errB += H2.GetBinError(xidx, yidx) * H2.GetBinError(xidx, yidx)
    errB = sqrt(errB)
    numD = 0.0
    errD = 0.0
    for xidx in range(xcut + 1, nxBins + 1): # Right
        for yidx in range(1, ycut + 1): # Bottom
            numD += H2.GetBinContent(xidx, yidx)
            errD += H2.GetBinError(xidx, yidx) * H2.GetBinError(xidx, yidx)
    errD = sqrt(errD)
    fake = numA / numC
    fakeErr = fake * sqrt((errA / numA)**2 + (errC / numC)**2)
    pred = fake * numD
    predErr = pred * sqrt((fakeErr / fake)**2 + (errD / numD)**2)

    # Open and write to output text file
    outFile = open('bkg_estimate_' + filename + '.tex', 'w')

    # Stuff for beginning .tex file
    outFile.write('\\documentclass{beamer}\n')
    outFile.write('\\usepackage[orientation = landscape, size = custom, width = 16, height = 12, scale = 0.5, debug]{beamerposter}\n')
    outFile.write('\\usepackage{colortbl}\n')
    outFile.write('\\usepackage{bm}\n')
    outFile.write('\n')
    outFile.write('\\title{\\textbf{Background Estimate}}\n')
    outFile.write('\\author{Your Name Here}\n')
    outFile.write('\n')
    outFile.write('\\begin{document}\n')
    outFile.write('\n')
    outFile.write('  \\begin{frame}\n')
    outFile.write('    \\maketitle\n')
    outFile.write('  \\end{frame}\n')

    # Slide with background estimates
    outFile.write('\n')
    outFile.write('  \\begin{frame}{\\textbf{' + filename + ' Background Estimate}}\n')
    outFile.write('    \\begin{table}\n')
    outFile.write('      \\begin{tabular}{ c | c | c | }\n')
    outFile.write('        \\hline\n')
    outFile.write('        \\textbf{' + cut1 + '} & \\cellcolor{red!25} %d$\\pm$%d & \\cellcolor{orange!25} %d$\\pm$%d (SR) \\\\\n' % (numA, errA, numB, errB))
    outFile.write('        \\hline\n')
    outFile.write('        \\textbf{' + cut2 + '} & \\cellcolor{blue!25} %d$\\pm$%d & \\cellcolor{green!25} %d$\\pm$%d \\\\\n' % (numC, errC, numD, errD))
    outFile.write('        \\hline\n')
    outFile.write('        & \\textbf{' + cut3 + '} & \\textbf{' + cut4 + '} \\\\\n')
    outFile.write('      \\end{tabular}\n')
    outFile.write('    \\end{table}\n')
    outFile.write('\n')
    outFile.write('    Fake Factor = %.4f$\\pm$%.4f \\\\\n' % (fake, fakeErr))
    outFile.write('    Predicted Count in Signal Region = %d$\\pm$%d \\\\\n' % (pred, predErr))
    outFile.write('    Actual Count in Signal Region = %d$\\pm$%d \\\\\n' % (numB, errB))
    outFile.write('  \\end{frame}\n')

    # Stuff for ending .tex file
    outFile.write('\n')
    outFile.write('\\end{document}\n')

    # Close output text file
    outFile.close()
    print('bkg-estimate-' + filename + '.tex created!')
