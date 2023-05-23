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
regions = ['ll', 'llOnZMetg20Jetgeq1', 'llOffZMetg20B1', 'llOffZMetg20B2', 'llStl300', 'llOnZ', 'llbtagg1p3', 'llStg300OffZbtagl1p3', 'llStg300OffZbtagl1p3Tight']


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
    outFile = open('cutflow' + yr + '.txt', 'w')
    for reg in regions:
        outFile.write('- - - - - - - - - - ' + reg + ' - - - - - - - - - -\n')

        outFile.write('\\hline\n')
        line = 'Mass & OS-$ee$ & OS-$ee$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ \\\\'
        outFile.write(line + '\n')
        line = 'Region & $m(e\\tau)<150$GeV & $m(e\\tau)>150$GeV & $m(e\\mu)<150$GeV & $m(e\\mu)>150$GeV & $m(e\\tau)<150$GeV & $m(e\\tau)>150$GeV \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')
        for fidx, f in enumerate(Samples):
            line = SamplesName[fidx]
            for b in range(nBins / 3):
                line += ' & ' + str(int(Counts[f][reg][b][0]))
                line += '$\\pm$' + str(int(Counts[f][reg][b][1]))
                if 'Data' not in f: line += '[%.2f\\%%]' % Counts[f][reg][b][2]
            line += ' \\\\'
            outFile.write(line + '\n')
            if f == 'Data.root' or f == 'TT.root': outFile.write('\\hline\n')
        outFile.write('\\hline\n')
        line = 'Background'
        for b in range(nBins / 3):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        line = 'Signal'
        for b in range(nBins / 3):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')
        line = '$S/\\sqrt{B}$'
        for b in range(nBins / 3):
            if SOverB[reg][b] > 0.0:
                line += ' & %.2f' % SOverB[reg][b]
            else:
                line += ' & undefined'
        line += ' \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')

        outFile.write('\\hline\n')
        line = 'Mass & OS-$e\\mu$ & OS-$e\\mu$ & OS-$\\mu\\mu$ & OS-$\\mu\\mu$ & SS-$ee$ & SS-$ee$ \\\\'
        outFile.write(line + '\n')
        line = 'Region & $m(\\mu\\tau)<150$GeV & $m(\\mu\\tau)>150$GeV & $m(\\mu\\tau)<150$GeV & $m(\\mu\\tau)>150$GeV & $m(e\\tau)<150$GeV & $m(e\\tau)>150$GeV \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')
        for fidx, f in enumerate(Samples):
            line = SamplesName[fidx]
            for b in range(nBins / 3, 2 * nBins / 3):
                line += ' & ' + str(int(Counts[f][reg][b][0]))
                line += '$\\pm$' + str(int(Counts[f][reg][b][1]))
                if 'Data' not in f: line += '[%.2f\\%%]' % Counts[f][reg][b][2]
            line += ' \\\\'
            outFile.write(line + '\n')
            if f == 'Data.root' or f == 'TT.root': outFile.write('\\hline\n')
        outFile.write('\\hline\n')
        line = 'Background'
        for b in range(nBins / 3, 2 * nBins / 3):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        line = 'Signal'
        for b in range(nBins / 3, 2 * nBins / 3):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')
        line = '$S/\\sqrt{B}$'
        for b in range(nBins / 3, 2 * nBins / 3):
            if SOverB[reg][b] > 0.0:
                line += ' & %.2f' % SOverB[reg][b]
            else:
                line += ' & undefined'
        line += ' \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')

        outFile.write('\\hline\n')
        line = 'Mass & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$\\mu\\mu$ & SS-$\\mu\\mu$ \\\\'
        outFile.write(line + '\n')
        line = 'Region & $m(e\\tau)<150$GeV & $m(e\\tau)>150$GeV & $m(\\mu\\tau)<150$GeV & $m(\\mu\\tau)>150$GeV & $m(\\mu\\tau)<150$GeV & $m(\\mu\\tau)>150$GeV \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')
        for fidx, f in enumerate(Samples):
            line = SamplesName[fidx]
            for b in range(2 * nBins / 3, nBins):
                line += ' & ' + str(int(Counts[f][reg][b][0]))
                line += '$\\pm$' + str(int(Counts[f][reg][b][1]))
                if 'Data' not in f: line += '[%.2f\\%%]' % Counts[f][reg][b][2]
            line += ' \\\\'
            outFile.write(line + '\n')
            if f == 'Data.root' or f == 'TT.root': outFile.write('\\hline\n')
        outFile.write('\\hline\n')
        line = 'Background'
        for b in range(2 * nBins / 3, nBins):
            line += ' & ' + str(int(Background[reg][b][0]))
            line += '$\\pm$' + str(int(Background[reg][b][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        line = 'Signal'
        for b in range(2 * nBins / 3, nBins):
            line += ' & ' + str(int(Signal[reg][b][0]))
            line += '$\\pm$' + str(int(Signal[reg][b][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')
        line = '$S/\\sqrt{B}$'
        for b in range(2 * nBins / 3, nBins):
            if SOverB[reg][b] > 0.0:
                line += ' & %.2f' % SOverB[reg][b]
            else:
                line += ' & undefined'
        line += ' \\\\'
        outFile.write(line + '\n')
        outFile.write('\\hline\n')

    outFile.close()
    print('cutflow' + yr + '.txt created!')
