import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}
##mc2017_samples ['2017_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']
##cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<8 && Electron_miniPFRelIso_all<0.4 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<8 && Muon_mediumId && Muon_miniPFRelIso_all<0.4 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1))>=2)"

##MC
mc2017_samples['2017_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_TTTo2L2Nu/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug25_2017_TTTo2L2Nu/230826_005437/0000/'], 'mc','TTTo2L2Nu','2017', '','88.4','41.48','105859990',2]
mc2017_samples['2017_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_TTW/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug26_2017_TTW/230827_013445/0000/'], 'mc','TTW','2017', '','0.235','41.48','3871055',3]

##Data
data2017_samples['2017_B_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_B_MET/MET/crab_Aug25_2017_B_MET/230826_003841/0000/'], 'data','MET','2017', 'B','1','1','1',43]
data2017_samples['2017_C_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_C_MET/MET/crab_Aug25_2017_C_MET/230826_005159/0000/'], 'data','MET','2017', 'C','1','1','1',53]
data2017_samples['2017_D_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_D_MET/MET/crab_Aug25_2017_D_MET/230826_004544/0000/'], 'data','MET','2017', 'D','1','1','1',15]
data2017_samples['2017_E_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_E_MET/MET/crab_Aug25_2017_E_MET/230826_005345/0000/'], 'data','MET','2017', 'E','1','1','1',48]
data2017_samples['2017_F_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2017_F_MET/MET/crab_Aug25_2017_F_MET/230826_005105/0000/'], 'data','MET','2017', 'F','1','1','1',133]
