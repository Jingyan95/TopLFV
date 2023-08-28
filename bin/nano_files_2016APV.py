import sys
import os
import subprocess
import readline
import string

data2016APV_samples = {}
mc2016APV_samples = {}
##mc2016APV_samples ['2016APV_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']
##cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<8 && Electron_miniPFRelIso_all<0.4 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<8 && Muon_mediumId && Muon_miniPFRelIso_all<0.4 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1))>=2)"

##MC
mc2016APV_samples['2016APV_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_TTTo2L2Nu/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug25_2016APV_TTTo2L2Nu/230826_005624/0000/'], 'mc','TTTo2L2Nu','2016APV', '','88.4','19.50','37202074',2]
mc2016APV_samples['2016APV_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_TTW/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug26_2016APV_TTW/230827_013743/0000/'], 'mc','TTW','2016APV', '','0.235','19.50','1543290',26]

##Data
data2016APV_samples['2016APV_Bv1_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_Bv1_MET/MET/crab_Aug25_2016APV_Bv1_MET/230826_005252/0000/'], 'data','MET','2016APV', 'B','1','1','1',1]
data2016APV_samples['2016APV_Bv2_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_Bv2_MET/MET/crab_Aug25_2016APV_Bv2_MET/230826_004359/0000/'], 'data','MET','2016APV', 'B','1','1','1',26]
data2016APV_samples['2016APV_C_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_C_MET/MET/crab_Aug25_2016APV_C_MET/230826_004451/0000/'], 'data','MET','2016APV', 'C','1','1','1',24]
data2016APV_samples['2016APV_D_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_D_MET/MET/crab_Aug25_2016APV_D_MET/230826_005716/0000/'], 'data','MET','2016APV', 'D','1','1','1',24]
data2016APV_samples['2016APV_E_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_E_MET/MET/crab_Aug25_2016APV_E_MET/230826_005531/0000/'], 'data','MET','2016APV', 'E','1','1','1',24]
data2016APV_samples['2016APV_F_MET'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Trigger/2016APV_F_MET/MET/crab_Aug25_2016APV_F_MET/230826_004637/0000/'], 'data','MET','2016APV', 'F','1','1','1',18]


