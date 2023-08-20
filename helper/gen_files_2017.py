import sys
import os
import subprocess
import readline
import string

mc2017_samples = {}

##Fake background samples
mc2017_samples['2017_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2017_TTTo2L2Nu_UL/230819_021926/0000/']]
mc2017_samples['2017_TTToSemiLeptonic'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2017_TTToSemiLeptonic_UL/230819_021350/0000/']]
mc2017_samples['2017_DYM50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug18_2017_DY50_UL/230819_021254/0000/']]
mc2017_samples['2017_DYM10to50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Aug18_2017_DY10to50_UL/230819_022220/0000/']]
mc2017_samples['2017_WWTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug18_2017_WWTo2L2Nu_UL/230819_021443/0000/']]
mc2017_samples['2017_ZZTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Aug18_2017_ZZTo2L2Nu_UL/230819_021635/0000/']]

##Real background samples
mc2017_samples['2017_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug18_2017_TTW_UL/230819_022418/0000/']]
mc2017_samples['2017_TTH'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Aug18_2017_TTH_UL/230819_021537/0000/']]
mc2017_samples['2017_TTZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2017_TTZ_UL/230819_022122/0000/']]
mc2017_samples['2017_WZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug18_2017_WZ_UL/230819_022320/0000/']]
mc2017_samples['2017_ZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Aug18_2017_ZZ_UL/230819_021731/0000/']]
mc2017_samples['2017_WWW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2017_WWW_UL/230819_022615/0000/']]
mc2017_samples['2017_WWZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2017_WWZ_UL/230819_022023/0000/']]
mc2017_samples['2017_WZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2017_WZZ_UL/230819_021828/0000/']]
mc2017_samples['2017_ZZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_SumOfGenWeights/2017/2017_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug18_2017_ZZZ_UL/230819_022517/0000/']]
