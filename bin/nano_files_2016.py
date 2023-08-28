import sys
import os
import subprocess
import readline
import string

data2016_samples = {}
mc2016_samples = {}
##mc2016_samples ['2016_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']
##cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<8 && Electron_miniPFRelIso_all<0.4 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<8 && Muon_mediumId && Muon_miniPFRelIso_all<0.4 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1))>=2)"

##MC
mc2016_samples['2016_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016_TTTo2L2Nu/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug25_2016_TTTo2L2Nu/230826_005011/0000/'], 'mc','TTTo2L2Nu','2016', '','88.4' ,'16.81','43193956',2]
mc2016_samples['2016_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016_TTW/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug26_2016_TTW/230827_013541/0000/'], 'mc','TTW','2016', '','0.235' ,'16.81','1800823',6]

##Data
data2016_samples['2016_F_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016_F_MET/MET/crab_Aug25_2016_F_MET/230826_004731/0000/'], 'data','MET','2016', 'F','1','1','1',3]
data2016_samples['2016_G_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016_G_MET/MET/crab_Aug25_2016_G_MET/230826_004120/0000/'], 'data','MET','2016', 'G','1','1','1',17]
data2016_samples['2016_H_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016_H_MET/MET/crab_Aug25_2016_H_MET/230826_004824/0000/'], 'data','MET','2016', 'H','1','1','1',32]
