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
mc2016_samples['2016_LFVStTensorU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_LFVStTensorU_UL/CRAB_UserFiles/crab_Trilepton_Inclusive_Apr19_2016_LFVStTensorU_UL/230419_120540/0000/'], 'mc','LFVStTensorU','2016', '','8.724' ,'16.81','1000',1]

## scalar interaction
mc2016_samples['2016_LFVStScalarU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_LFVStScalarU_UL/CRAB_UserFiles/crab_Trilepton_Inclusive_Apr19_2016_LFVStScalarU_UL/230419_121019/0000/'], 'mc','LFVStScalarU','2016', '','0.417' ,'16.81','1000',1]
mc2016_samples['2016_LFVStScalarC'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_LFVStScalarC_UL/CRAB_UserFiles/crab_Trilepton_Inclusive_Apr19_2016_LFVStScalarC_UL/230419_120909/0000/'], 'mc','LFVStScalarC','2016', '','0.0363' ,'16.81','1000',1]
mc2016_samples['2016_LFVTtScalarU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_LFVTtScalarU_UL/CRAB_UserFiles/crab_Trilepton_Inclusive_Apr19_2016_LFVTtScalarU_UL/230419_121128/0000/'], 'mc','LFVTtScalarU','2016', '','0.012','16.81','1000',1]

##Fake background samples
mc2016_samples['2016_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTTo2L2Nu_UL/230419_121459/0000/'], 'mc','TTTo2L2Nu','2016', '','88.4' ,'16.81','43546000',1]
mc2016_samples['2016_DYM50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilepton_Inclusive_Apr19_2016_DY50_UL/230419_120428/0000/'], 'mc','DYM50','2016', '','6077.22' ,'16.81','71839442',2]

##Real background samples
mc2016_samples['2016_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTW_UL/230419_121349/0000/'], 'mc','TTW','2016', '','0.235' ,'16.81','3322643',2]
mc2016_samples['2016_TTH'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTH_UL/230419_121721/0000/'], 'mc','TTH','2016', '','0.211' ,'16.81','4941250',2]
mc2016_samples['2016_TTZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTZ_UL/230419_121829/0000/'], 'mc','TTZ','2016', '','0.281' ,'16.81','6017000',4]
mc2016_samples['2016_WZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WZ_UL/230419_120800/0000/'], 'mc','WZ','2016', '','4.9173' ,'16.81','10441724',4]
mc2016_samples['2016_ZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Trilepton_Inclusive_Apr19_2016_ZZ/230419_122046/0000/'], 'mc','ZZ','2016', '','1.256' ,'16.81','52104000',2]
mc2016_samples['2016_WWW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WWW/230419_121238/0000/'], 'mc','WWW','2016', '','0.2086' ,'16.81','69000',14]
mc2016_samples['2016_WWZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WWZ/230419_121938/0000/'], 'mc','WWZ','2016', '','0.1651' ,'16.81','67000',8]
mc2016_samples['2016_WZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WZZ/230419_120650/0000/'], 'mc','WZZ','2016', '','0.05565' ,'16.81','137000',18]
mc2016_samples['2016_ZZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_ZZZ/230419_122859/0000/'], 'mc','ZZZ','2016', '','0.01476' ,'16.81','72000',4]
