import sys
import os
import subprocess
import readline
import string

mc2016APV_samples = {}

#Scalar interaction
mc2016APV_samples['2016APV_LFVStScalarU'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_LFVStScalarU_UL/CRAB_UserFiles/crab_Set11_2_GenWieght_2016APV_LFVStScalarU_UL/230911_225954/0000/']]
mc2016APV_samples['2016APV_LFVTtScalarU'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_LFVTtScalarU_UL/CRAB_UserFiles/crab_Set11_2_GenWieght_2016APV_LFVTtScalarU_UL/230911_230050/0000/']]

##Fake background samples
mc2016APV_samples['2016APV_TTTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2016APV_TTTo2L2Nu_UL/230819_021537/0000/']]
mc2016APV_samples['2016APV_TTToSemiLeptonic'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2016APV_TTToSemiLeptonic_UL/230819_022023/0000/']]
mc2016APV_samples['2016APV_DYM50'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug18_2016APV_DY50_UL/230819_022122/0000/']]
mc2016APV_samples['2016APV_DYM10to50'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Aug18_2016APV_DY10to50_UL/230819_021635/0000/']]
mc2016APV_samples['2016APV_WWTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2016APV_WWTo2L2Nu_UL/230819_022615/0000/']]
mc2016APV_samples['2016APV_ZZTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Aug18_2016APV_ZZTo2L2Nu_UL/230819_022220/0000/']]

##Real background samples
mc2016APV_samples['2016APV_TTW'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug18_2016APV_TTW_UL/230819_021349/0000/']]
mc2016APV_samples['2016APV_TTH'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Aug18_2016APV_TTH_UL/230819_021731/0000/']]
mc2016APV_samples['2016APV_TTZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2016APV_TTZ_UL/230819_022320/0000/']]
mc2016APV_samples['2016APV_WZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug18_2016APV_WZ_UL/230819_021442/0000/']]
mc2016APV_samples['2016APV_ZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Aug18_2016APV_ZZ_UL/230819_021254/0000/']]
mc2016APV_samples['2016APV_WWW'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2016APV_WWW_UL/230819_021926/0000/']]
mc2016APV_samples['2016APV_WWZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2016APV_WWZ_UL/230819_022418/0000/']]
mc2016APV_samples['2016APV_WZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2016APV_WZZ_UL/230819_021828/0000/']]
mc2016APV_samples['2016APV_ZZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2016APV/2016APV_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2016APV_ZZZ_UL/230819_022517/0000/']]
