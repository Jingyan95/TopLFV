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

for yr in year:
    Counts = {}
    Counts[yr] = {}
    for f in Samples:
        Counts[yr][f] = {}
        file = ROOT.TFile.Open(HistAddress + yr + '_' + f)
        for reg in regions:
            Counts[yr][f][reg] = {}
            total = 0.0
            for c in charges:
                Counts[yr][f][reg][c] = {}
                for ch in channels:
                    h = file.Get(c + '_' + ch + '_' + reg + '_llM')
                    nbinsX = h.GetXaxis().GetNbins()
                    err = ROOT.Double()
                    integral = h.IntegralAndError(1, nbinsX, err)
                    Counts[yr][f][reg][c][ch] = [integral, err, -1.0] # [integral, error, %]
                    total += integral
            for c in charges:
                for ch in channels:
                    if total == 0.0:
                        Counts[yr][f][reg][c][ch][2] = 0.0
                    else:
                        Counts[yr][f][reg][c][ch][2] = Counts[yr][f][reg][c][ch][0] / total * 100.0

    Background = {}
    Background[yr] = {}
    Signal = {}
    Signal[yr] = {}
    SOverB = {}
    SOverB[yr] = {}
    for reg in regions:
        Signal[yr][reg] = {}
        Background[yr][reg] = {}
        SOverB[yr][reg] = {}
        for c in charges:
            Signal[yr][reg][c] = {}
            Background[yr][reg][c] = {}
            SOverB[yr][reg][c] = {}
            for ch in channels:
                sig = Counts[yr]['LFVStScalarU.root'][reg][c][ch][0] + Counts[yr]['LFVTtScalarU.root'][reg][c][ch][0]
                sig_err = sqrt(Counts[yr]['LFVStScalarU.root'][reg][c][ch][1]**2 + Counts[yr]['LFVTtScalarU.root'][reg][c][ch][1]**2)
                Signal[yr][reg][c][ch] = [sig, sig_err]

                bkg = Counts[yr]['TX.root'][reg][c][ch][0] + Counts[yr]['VV.root'][reg][c][ch][0] + Counts[yr]['DY.root'][reg][c][ch][0] + Counts[yr]['TT.root'][reg][c][ch][0]
                bkg_err = sqrt(Counts[yr]['TX.root'][reg][c][ch][1]**2 + Counts[yr]['VV.root'][reg][c][ch][1]**2 + Counts[yr]['DY.root'][reg][c][ch][1]**2 + Counts[yr]['TT.root'][reg][c][ch][1]**2)
                Background[yr][reg][c][ch] = [bkg, bkg_err]

                if bkg == 0.0:
                    SOverB[yr][reg][c][ch] = -1.0
                else:
                    SOverB[yr][reg][c][ch] = sig / sqrt(bkg)

    # open and write to output text file
    outFile = open('cutflow' + yr + '.txt', 'w')
    for reg in regions:
        outFile.write('- - - - - - - - - - ' + reg + ' - - - - - - - - - -\n')

        outFile.write('\\hline\n')
        line = 'Samples'
        for c in charges:
            for ch in channels:
                line += ' & ' + c + '\\_' + ch
        line += ' \\\\'
        outFile.write(line + '\n')

        outFile.write('\\hline\n')
        for fidx, f in enumerate(Samples):
            line = SamplesName[fidx]
            for c in charges:
                for ch in channels:
                    line += ' & ' + str(int(Counts[yr][f][reg][c][ch][0]))
                    line += '$\\pm$' + str(int(Counts[yr][f][reg][c][ch][1]))
                    line += '[%.2f\\%%]' % Counts[yr][f][reg][c][ch][2]
            line += ' \\\\'
            outFile.write(line + '\n')
            if f == 'Data.root' or f == 'TT.root': outFile.write('\\hline\n')

        outFile.write('\\hline\n')
        line = 'Background'
        for c in charges:
            for ch in channels:
                line += ' & ' + str(int(Background[yr][reg][c][ch][0]))
                line += '$\\pm$' + str(int(Background[yr][reg][c][ch][1]))
        line += ' \\\\'
        outFile.write(line + '\n')
        line = 'Signal'
        for c in charges:
            for ch in channels:
                line += ' & ' + str(int(Signal[yr][reg][c][ch][0]))
                line += '$\\pm$' + str(int(Signal[yr][reg][c][ch][1]))
        line += ' \\\\'
        outFile.write(line + '\n')

        outFile.write('\\hline\n')
        line = '$S/\\sqrt{B}$'
        for c in charges:
            for ch in channels:
                if SOverB[yr][reg][c][ch] > 0.0:
                    line += ' & %.2f' % SOverB[yr][reg][c][ch]
                else:
                    line += ' & undefined'
        line += ' \\\\'
        outFile.write(line + '\n')

        outFile.write('\\hline\n')

    outFile.close()
    print('cutflow' + yr + '.txt created!')
