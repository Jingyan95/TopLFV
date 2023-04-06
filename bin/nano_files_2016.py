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


##Background samples
mc2016_samples['2016_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr6/2016_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr6_2016_TTTo2L2Nu_UL/230406_184952/0000/'], 'mc','TTTo2L2Nu','2016', '','87.31' ,'16.81','43546000',1]
mc2016_samples['2016_DYM50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr6/2016_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_Inclusive_Apr6_2016_DY50_UL/230406_184913/0000/'], 'mc','DYM50','2016', '','6077.22' ,'16.81','71839442',1]
mc2016_samples['2016_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr6/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_Apr6_2016_TTW_UL/230406_185030/0000/'], 'mc','TTW','2016', '','0.2043' ,'16.81','3322643',1]
mc2016_samples['2016_TTH'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr6/2016_TTH_UL/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr6_2016_TTH_UL/230406_185109/0000/'], 'mc','TTH','2016', '','0.2118' ,'16.81','2240994',1]
