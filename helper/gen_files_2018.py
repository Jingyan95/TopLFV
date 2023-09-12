import sys
import os
import subprocess
import readline
import string

mc2018_samples = {}

#Scalar interaction
mc2018_samples['2018_LFVStScalarU'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_LFVStScalarU_UL/CRAB_UserFiles/crab_Set11_2_GenWieght_2018_LFVStScalarU_UL/230911_230940/0000/']]
mc2018_samples['2018_LFVTtScalarU'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_LFVTtScalarU_UL/CRAB_UserFiles/crab_Set11_2_GenWieght_2018_LFVTtScalarU_UL/230911_231034/0000/']]

##Fake background samples
mc2018_samples['2018_TTTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2018_TTTo2L2Nu_UL/230819_021927/0000/']]
mc2018_samples['2018_TTToSemiLeptonic'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2018_TTToSemiLeptonic_UL/230819_021830/0000/']]
mc2018_samples['2018_DYM50'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug18_2018_DY50_UL/230819_021453/0000/']]
mc2018_samples['2018_DYM10to50'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Aug18_2018_DY10to50_UL/230819_022024/0000/']]
mc2018_samples['2018_WWTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2018_WWTo2L2Nu_UL/230819_022220/0000/']]
mc2018_samples['2018_ZZTo2L2Nu'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Aug18_2018_ZZ_UL/230819_022517/0000/']]

##Real background samples
mc2018_samples['2018_TTW'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug18_2018_TTW_UL/230819_022320/0000/']]
mc2018_samples['2018_TTH'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Aug18_2018_TTH_UL/230819_021546/0000/']]
mc2018_samples['2018_TTZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2018_TTZ_UL/230819_021401/0000/']]
mc2018_samples['2018_WZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug18_2018_WZ_UL/230819_022122/0000/']]
mc2018_samples['2018_ZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Aug18_2018_ZZTo2L2Nu_UL/230819_021735/0000/']]
mc2018_samples['2018_WWW'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2018_WWW_UL/230819_021309/0000/']]
mc2018_samples['2018_WWZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2018_WWZ_UL/230819_022418/0000/']]
mc2018_samples['2018_WZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2018_WZZ_UL/230819_021640/0000/']]
mc2018_samples['2018_ZZZ'] = [['/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive_SumOfGenWeights/2018/2018_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2018_ZZZ_UL/230819_022615/0000/']]
