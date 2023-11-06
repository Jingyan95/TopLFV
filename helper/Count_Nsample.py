import os
import ROOT
import argparse

# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--d', dest='DIRECTORY')
ARGS = parser.parse_args()
dir = ARGS.DIRECTORY # directory where root files are stored

print('-----------------------')
print(dir)
nEventsraw = 0
nFiles = 0
filenames = os.listdir(dir)
for fname in filenames:
    filename = dir + '/' + fname
    if 'fail' in fname:
        continue
    if 'log' in fname:
        continue
    f = ROOT.TFile.Open(filename)
    if not f:
        continue
    tree_events = f.Get('Events')
    nEventsraw += tree_events.GetEntries()
    nFiles += 1
    f.Close()
print('nEventsraw = %d' % nEventsraw)
print('nFiles = %d' % nFiles)
