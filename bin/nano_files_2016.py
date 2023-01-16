import sys
import os
import subprocess
import readline
import string

data2016_samples = {}
mc2016_samples = {}
#data2016_samples ['2016_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']

## vector interaction
#mc2016_samples['2016_LFVStVecU'] = [[''], 'mc','LFVStVecU','2016', '','1.902','16.81','1000',1]

## tensor interaction
mc2016_samples['2016_LFVStTensorU'] = [['/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/ST_clequ3_lltu/'], 'mc','LFVStTensorU','2016', '','8.724' ,'16.81','1000',1]

## scalar interaction
mc2016_samples['2016_LFVStScalarU'] = [['/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/ST_clequ1_lltu/'], 'mc','LFVStScalarU','2016', '','0.417' ,'16.81','1000',1]
mc2016_samples['2016_LFVStScalarC'] = [['/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/ST_clequ1_lltc/'], 'mc','LFVStScalarC','2016', '','0.0363' ,'16.81','1000',1]
mc2016_samples['2016_LFVTtScalarU'] = [['/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/TT_clequ1_lltu/'], 'mc','LFVTtScalarU','2016', '','0.012','16.81','1000',1]
