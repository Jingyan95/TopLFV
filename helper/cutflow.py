from math import sqrt

nBins = 18 # Number of bins in subSR histogram


# Calculates cutflow tables and prints them in LaTeX table format
def CutflowTables(Hists, numyear, nameyear, regions, regionsName, charges, channels, Samples, SamplesName):

    # Initialize counts and totals
    Counts = {}
    for f in Samples:
        Counts[f] = {}
        for reg in regions:
            Counts[f][reg] = {}
            for b in range(nBins):
                Counts[f][reg][b] = [0.0, 0.0, -1.0] # [count, error, %]
    Totals = {}
    for reg in regions:
        Totals[reg] = []
        for b in range(nBins):
            Totals[reg].append(0.0)

    # Get counts for each sample
    for numf, namef in enumerate(Samples):
        for numreg, namereg in enumerate(regions):
            for c in range(len(charges)):
                for ch in range(len(channels)):
                    h = Hists[numyear][numf][c][ch][numreg][15].Clone()
                    for b in range(nBins):
                        Counts[namef][namereg][b][0] += h.GetBinContent(b + 1)
                        Counts[namef][namereg][b][1] += h.GetBinError(b + 1)
                        if 'Data' not in f: Totals[namereg][b] += h.GetBinContent(b + 1)
    for f in Samples:
        for reg in regions:
            for b in range(nBins):
                if Totals[reg][b] == 0.0:
                    Counts[f][reg][b][2] = 0.0 # Technically undefined
                else:
                    Counts[f][reg][b][2] = Counts[f][reg][b][0] / Totals[reg][b] * 100.0

    # Get counts for signal and background
    Background = {}
    Signal = {}
    SOverB = {}
    for reg in regions:
        Signal[reg] = {}
        Background[reg] = {}
        SOverB[reg] = {}
        for b in range(nBins):
            sig = Counts[Samples[5]][reg][b][0] + Counts[Samples[6]][reg][b][0]
            sig_err = sqrt(Counts[Samples[5]][reg][b][1]**2 + Counts[Samples[6]][reg][b][1]**2)
            Signal[reg][b] = [sig, sig_err]

            bkg = Counts[Samples[1]][reg][b][0] + Counts[Samples[2]][reg][b][0] + Counts[Samples[3]][reg][b][0] + Counts[Samples[4]][reg][b][0]
            bkg_err = sqrt(Counts[Samples[1]][reg][b][1]**2 + Counts[Samples[2]][reg][b][1]**2 + Counts[Samples[3]][reg][b][1]**2 + Counts[Samples[4]][reg][b][1]**2)
            Background[reg][b] = [bkg, bkg_err]

            if bkg == 0.0:
                SOverB[reg][b] = -1.0
            else:
                SOverB[reg][b] = sig / sqrt(bkg)

    # Open and write to output text file
    outFile = open('cutflow' + nameyear + '.tex', 'w')

    # Stuff for beginning .tex file
    outFile.write('\\documentclass{beamer}\n')
    outFile.write('\\usepackage[orientation = landscape, size = custom, width = 16, height = 12, scale = 0.5, debug]{beamerposter}\n')
    outFile.write('\n')
    outFile.write('\\title{\\textbf{Cutflow Tables}}\n')
    outFile.write('\\author{Your Name Here}\n')
    outFile.write('\n')
    outFile.write('\\begin{document}\n')
    outFile.write('\n')
    outFile.write('  \\begin{frame}\n')
    outFile.write('    \\maketitle\n')
    outFile.write('  \\end{frame}\n')

    # Slide listing all cuts
    outFile.write('\n')
    outFile.write('  \\begin{frame}{\\textbf{Cutflow}}\n')
    outFile.write('    \\begin{enumerate}\n')
    for regName in regionsName:
        outFile.write('      \\item ' + regName + '\n')
    outFile.write('    \\end{enumerate}\n')
    outFile.write('  \\end{frame}\n')

    # Cutflow table slides, 1 per region
    for ridx, reg in enumerate(regions):
        outFile.write('\n')
        outFile.write('  \\begin{frame}{\\textbf{Cutflow}}\n')
        outFile.write('    \\begin{itemize}\n')
        outFile.write('      \\item (' + str(ridx + 1) + ') ' + regionsName[ridx] + '\n')
        outFile.write('    \\end{itemize}\n')
        outFile.write('    \\makebox[\\textwidth]{\n')
        outFile.write('      \\tiny\n')
        outFile.write('      \\begin{tabular}{ | l | l | l | l | l | l | l | }\n')
        outFile.write('        \\hline\n')
        line = '        Mass & OS-$ee$ & OS-$ee$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ \\\\\n'
        outFile.write(line)
        line = '        Region & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV & $m(e\\mu)<150$GeV & $m(e\\mu)>150$GeV & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        for fidx, f in enumerate(Samples):
            line = '        ' + SamplesName[fidx]
            for b in range(nBins // 3):
                if f == 'LFVStScalarU.root' or f == 'LFVTtScalarU.root': line += ' & %.2f' % Counts[f][reg][b][0]
                else: line += ' & ' + str(int(Counts[f][reg][b][0]))
                if f == 'LFVStScalarU.root' or f == 'LFVTtScalarU.root': line += '$\\pm$%.2f' % Counts[f][reg][b][1]
                else: line += '$\\pm$' + str(int(Counts[f][reg][b][1]))
                if 'Data' not in f: line += '[%.2f\\%%]' % Counts[f][reg][b][2]
            line += ' \\\\\n'
            outFile.write(line)
            if f == 'Data.root' or f == 'TT.root': outFile.write('        \\hline\n')
        outFile.write('        \\hline\n')
        line = '        Background'
        for b in range(nBins // 3):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        line = '        Signal'
        for b in range(nBins // 3):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        line = '        $S/\\sqrt{B}$'
        for b in range(nBins // 3):
            if SOverB[reg][b] > 0.0:
                line += ' & %.2f' % SOverB[reg][b]
            else:
                line += ' & undefined'
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')

        outFile.write('        \\hline\n')
        line = '        Mass & OS-$e\\mu$ & OS-$e\\mu$ & OS-$\\mu\\mu$ & OS-$\\mu\\mu$ & SS-$ee$ & SS-$ee$ \\\\\n'
        outFile.write(line)
        line = '        Region & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        for fidx, f in enumerate(Samples):
            line = '        ' + SamplesName[fidx]
            for b in range(nBins // 3, 2 * nBins // 3):
                if f == 'LFVStScalarU.root' or f == 'LFVTtScalarU.root': line += ' & %.2f' % Counts[f][reg][b][0]
                else: line += ' & ' + str(int(Counts[f][reg][b][0]))
                if f == 'LFVStScalarU.root' or f == 'LFVTtScalarU.root': line += '$\\pm$%.2f' % Counts[f][reg][b][1]
                else: line += '$\\pm$' + str(int(Counts[f][reg][b][1]))
                if 'Data' not in f: line += '[%.2f\\%%]' % Counts[f][reg][b][2]
            line += ' \\\\\n'
            outFile.write(line)
            if f == 'Data.root' or f == 'TT.root': outFile.write('        \\hline\n')
        outFile.write('        \\hline\n')
        line = '        Background'
        for b in range(nBins // 3, 2 * nBins // 3):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        line = '        Signal'
        for b in range(nBins // 3, 2 * nBins // 3):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        line = '        $S/\\sqrt{B}$'
        for b in range(nBins // 3, 2 * nBins // 3):
            if SOverB[reg][b] > 0.0:
                line += ' & %.2f' % SOverB[reg][b]
            else:
                line += ' & undefined'
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')

        outFile.write('        \\hline\n')
        line = '        Mass & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$\\mu\\mu$ & SS-$\\mu\\mu$ \\\\\n'
        outFile.write(line)
        line = '        Region & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        for fidx, f in enumerate(Samples):
            line = '        ' + SamplesName[fidx]
            for b in range(2 * nBins // 3, nBins):
                if f == 'LFVStScalarU.root' or f == 'LFVTtScalarU.root': line += ' & %.2f' % Counts[f][reg][b][0]
                else: line += ' & ' + str(int(Counts[f][reg][b][0]))
                if f == 'LFVStScalarU.root' or f == 'LFVTtScalarU.root': line += '$\\pm$%.2f' % Counts[f][reg][b][1]
                else: line += '$\\pm$' + str(int(Counts[f][reg][b][1]))
                if 'Data' not in f: line += '[%.2f\\%%]' % Counts[f][reg][b][2]
            line += ' \\\\\n'
            outFile.write(line)
            if f == 'Data.root' or f == 'TT.root': outFile.write('        \\hline\n')
        outFile.write('        \\hline\n')
        line = '        Background'
        for b in range(2 * nBins // 3, nBins):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        line = '        Signal'
        for b in range(2 * nBins // 3, nBins):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        line = '        $S/\\sqrt{B}$'
        for b in range(2 * nBins // 3, nBins):
            if SOverB[reg][b] > 0.0:
                line += ' & %.2f' % SOverB[reg][b]
            else:
                line += ' & undefined'
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        outFile.write('      \\end{tabular}\n')
        outFile.write('    }\n')
        outFile.write('  \\end{frame}\n')

    # Stuff for ending .tex file
    outFile.write('\n')
    outFile.write('\\end{document}\n')

    # Close output file
    outFile.close()
    print('cutflow' + nameyear + '.tex created')
