# prints out cutflows in LaTeX table format

import argparse
import ROOT
import sys
import os
from math import sqrt


year_RunII = ['2016APV', '2016', '2017', '2018', 'All']
year = []
Samples = ['Data.root', 'TX.root', 'VV.root', 'DY.root', 'TT.root', 'LFVStScalarU.root', 'LFVTtScalarU.root']
SamplesName = ['Data', '$t\\bar{t}X$', 'VV', 'DY', '$t\\bar{t}$', 'St Scalar U', 'Tt Scalar U']
charges = ['OS', 'SS']
channels = ['ee', 'emu', 'mumu']
regions = ['ll']
regions = ['ll', 'llOnZMetg20Jetgeq1', 'llOffZMetg20B1', 'llOffZMetg20B2', 'llStl300', 'llOnZ', 'llbtagg1p3', 'llStg300OffZbtagl1p3', 'llStg300OffZbtagl1p3Tight']
regionsName = ['2$l+\\tau_h$, no cuts',
    '2$l+\\tau_h$, Z + jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, on Z',
    '2$l+\\tau_h$, SR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, off Z, nbjet $=1$',
    '2$l+\\tau_h$, $t\\bar{t}$ + jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, off Z, nbjet $=2$',
    '2$l+\\tau_h$, CR, $S_T<300$ GeV',
    '2$l+\\tau_h$, Z + jets CR, on Z',
    '2$l+\\tau_h$, $t\\bar{t}$ + jets CR, btag $>1.3$',
    '2$l+\\tau_h$, SR (Alt, Loose), $S_T>300$ GeV, off Z, btag $>1.3$',
    '2$l+\\tau_h$, SR (Alt, Tight), $S_T>300$ GeV, off Z, btag $>1.3$, njet $\\geq 1$ or $S_T>500$ GeV']


# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--n', dest = 'NAMETAG', default = '2016')
ARGS = parser.parse_args()
name = ARGS.NAMETAG

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'bin'))
loc = os.path.dirname(sys.path[0]) + '/'
HistAddress = loc + 'hists/'


for numyear, nameyear in enumerate(year_RunII):
    if name == nameyear or name == 'RunII':
        year.append(year_RunII[numyear])

nBins = 18
for yr in year:
    Counts = {}
    Totals = {}

    for reg in regions:
        Totals[reg] = []
        for b in range(nBins):
            Totals[reg].append(0.0)

    for f in Samples:
        Counts[f] = {}
        file = ROOT.TFile.Open(HistAddress + yr + '_' + f)
        for reg in regions:
            Counts[f][reg] = {}
            for b in range(nBins):
                Counts[f][reg][b] = [0.0, 0.0, -1.0]

            for c in charges:
                for ch in channels:
                    h = file.Get(c + '_' + ch + '_' + reg + '_subSR')
                    for b in range(nBins):
                        Counts[f][reg][b][0] += h.GetBinContent(b + 1)
                        Counts[f][reg][b][1] += h.GetBinError(b + 1)
                        if 'Data' not in f: Totals[reg][b] += h.GetBinContent(b + 1)

    for f in Samples:
        for reg in regions:
            for b in range(nBins):
                if Totals[reg][b] == 0.0:
                    Counts[f][reg][b][2] = 0.0
                else:
                    Counts[f][reg][b][2] = Counts[f][reg][b][0] / Totals[reg][b] * 100.0

    Background = {}
    Signal = {}
    SOverB = {}
    for reg in regions:
        Signal[reg] = {}
        Background[reg] = {}
        SOverB[reg] = {}
        for b in range(nBins):
            sig = Counts['LFVStScalarU.root'][reg][b][0] + Counts['LFVTtScalarU.root'][reg][b][0]
            sig_err = sqrt(Counts['LFVStScalarU.root'][reg][b][1]**2 + Counts['LFVTtScalarU.root'][reg][b][1]**2)
            Signal[reg][b] = [sig, sig_err]

            bkg = Counts['TX.root'][reg][b][0] + Counts['VV.root'][reg][b][0] + Counts['DY.root'][reg][b][0] + Counts['TT.root'][reg][b][0]
            bkg_err = sqrt(Counts['TX.root'][reg][b][1]**2 + Counts['VV.root'][reg][b][1]**2 + Counts['DY.root'][reg][b][1]**2 + Counts['TT.root'][reg][b][1]**2)
            Background[reg][b] = [bkg, bkg_err]

            if bkg == 0.0:
                SOverB[reg][b] = -1.0
            else:
                SOverB[reg][b] = sig / sqrt(bkg)

    # open and write to output text file
    outFile = open('cutflow' + yr + '.tex', 'w')

    # stuff for beginning .tex file
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

    # slide listing all cuts
    outFile.write('\n')
    outFile.write('  \\begin{frame}{\\textbf{Cutflow}}\n')
    outFile.write('    \\begin{enumerate}\n')
    for regName in regionsName:
        outFile.write('      \\item ' + regName + '\n')
    outFile.write('    \\end{enumerate}\n')
    outFile.write('  \\end{frame}\n')

    # cutflow table slides, 1 per region
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
            for b in range(nBins / 3):
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
        for b in range(nBins / 3):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        line = '        Signal'
        for b in range(nBins / 3):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        line = '        $S/\\sqrt{B}$'
        for b in range(nBins / 3):
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
            for b in range(nBins / 3, 2 * nBins / 3):
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
        for b in range(nBins / 3, 2 * nBins / 3):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        line = '        Signal'
        for b in range(nBins / 3, 2 * nBins / 3):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        line = '        $S/\\sqrt{B}$'
        for b in range(nBins / 3, 2 * nBins / 3):
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
            for b in range(2 * nBins / 3, nBins):
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
        for b in range(2 * nBins / 3, nBins):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        line = '        Signal'
        for b in range(2 * nBins / 3, nBins):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\\n'
        outFile.write(line)
        outFile.write('        \\hline\n')
        line = '        $S/\\sqrt{B}$'
        for b in range(2 * nBins / 3, nBins):
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

    # stuff for ending .tex file
    outFile.write('\n')
    outFile.write('\\end{document}\n')

    outFile.close()
    print('cutflow' + yr + '.tex created!')
