import sys
import os
import subprocess
import readline
import string

data2018_samples = {}
mc2018_samples = {}
##mc2018_samples ['2018_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']
##cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<8 && Electron_miniPFRelIso_all<0.4 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<8 && Muon_mediumId && Muon_miniPFRelIso_all<0.4 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1))>=2)"

##MC
mc2018_samples['2018_TTTo2L2Nu'] = [['/eos/cms/store/user/etsai/LFV_Trilepton_Inclusive_Trigger/2018_TTTo2L2Nu/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug25_2018_TTTo2L2Nu/230826_004305/0000/'], 'mc','TTTo2L2Nu','2018', '','88.4','59.83','143848848',2]
mc2018_samples['2018_TTW'] = [['/eos/cms/store/user/etsai/LFV_Trilepton_Inclusive_Trigger/2018_TTW/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug26_2018_TTW_UL/230827_013639/0000/'], 'mc','TTW','2018', '','0.235','59.83','5666428',3]

##Data
data2018_samples['2018_A_MET'] = [['/eos/cms/store/user/etsai/LFV_Trilepton_Inclusive_Trigger/2018_A_MET/MET/crab_Aug25_2018_A_MET/230826_004918/0000/'], 'data','MET','2018', 'A','1','1','1',43]
data2018_samples['2018_B_MET'] = [['/eos/cms/store/user/etsai/LFV_Trilepton_Inclusive_Trigger/2018_B_MET/MET/crab_Aug25_2018_B_MET/230826_004212/0000/'], 'data','MET','2018', 'B','1','1','1',19]
data2018_samples['2018_C_MET'] = [['/eos/cms/store/user/etsai/LFV_Trilepton_Inclusive_Trigger/2018_C_MET/MET/crab_Aug25_2018_C_MET/230826_004027/0000/'], 'data','MET','2018', 'C','1','1','1',27]
data2018_samples['2018_D_MET'] = [['/eos/cms/store/user/etsai/LFV_Trilepton_Inclusive_Trigger/2018_D_MET/MET/crab_Aug25_2018_D_MET/230826_003935/0000/'], 'data','MET','2018', 'D','1','1','1',76]
