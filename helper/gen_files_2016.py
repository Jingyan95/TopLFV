import sys
import os
import subprocess
import readline
import string

mc2016_samples = {}
# #Scalar interaction
mc2016_samples['2016_LFVStScalarU'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_LFVStScalarU_UL/CRAB_UserFiles/crab_Sep11_3_GenWeight_2016_LFVStScalarU_UL/230912_023936/0000/']]
mc2016_samples['2016_LFVTtScalarU'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_LFVTtScalarU_UL/CRAB_UserFiles/crab_Sep11_3_GenWeight_2016_LFVTtScalarU_UL/230912_024033/0000/']]

##Fake background samples
mc2016_samples['2016_TTTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_TTTo2L2Nu_UL/230430_083326/0000/']]
mc2016_samples['2016_TTToSemiLeptonic'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_TTToSemiLeptonic_UL/230430_082939/0000/']]
mc2016_samples['2016_TTToHadronic'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_TTToHadronic_UL/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_TTToHadronic_UL/230430_081711/0000/']]
mc2016_samples['2016_DYM50'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_DY50_UL/230430_082820/0000/']]
mc2016_samples['2016_DYM10to50'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_DY10to50_UL/230430_081556/0000/']]
mc2016_samples['2016_WWTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_WWTo2L2Nu_UL/230430_082703/0000/']]
mc2016_samples['2016_ZZTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_ZZTo2L2Nu_UL/230430_082206/0000/']]

##Real background samples
mc2016_samples['2016_TTW'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_TTW_UL/230430_083055/0000/']]
mc2016_samples['2016_TTH'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_TTH_UL/230430_082320/0000/']]
mc2016_samples['2016_TTZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_TTZ_UL/230430_082547/0000/']]
mc2016_samples['2016_WZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_WZ_UL/230430_081824/0000/']]
mc2016_samples['2016_ZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_ZZ_UL/230430_083211/0000/']]
mc2016_samples['2016_WWW'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_WWW_UL/230430_083441/0000/']]
mc2016_samples['2016_WWZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_WWZ_UL/230430_081444/0000/']]
mc2016_samples['2016_WZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_WZZ_UL/230430_082434/0000/']]
mc2016_samples['2016_ZZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016/2016_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_Apr30_SumOfGenWeights_2016_ZZZ_UL/230430_081938/0000/']]
