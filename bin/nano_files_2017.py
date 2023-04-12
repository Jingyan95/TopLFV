import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}
#data2017_samples ['DYM10to50'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']

#preUL branch name can be found at https://swertz.web.cern.ch/swertz/TMG/TopNano/TopNanoV6p1/doc_topNanoV6p1.html
#Top Lepton MVA ID is named "Electron_mvaTOP/Muon_mvaTOP"
#Pre-UL ntuples are pre-selected with cut = "((Sum$(Electron_pt>20 && abs(Electron_eta)<2.4 && Electron_sip3d<8 && Electron_miniPFRelIso_all<0.4 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1 && Electron_lostHits<2) + Sum$(Muon_pt>20 && abs(Muon_eta)<2.4 && Muon_sip3d<8 && Muon_mediumId && Muon_miniPFRelIso_all<0.4 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1))>=2)"
#Please apply event selection that is no looser than the pre-selection
#Code at reco branch needs modification in order to work with preUL ntuples,
##namely the requirement of tau lepton needs to be removed, UL ID C++ interface should not be called because preUL ntuples don't have all the branches needed 
mc2017_samples['2017_TTTo2L2Nu_preUL'] = [['/eos/cms/store/user/jingyan/LFV_Dilepton_TopLeptonMVAStudy/2017_TTTo2L2Nu_preUL/CRAB_UserFiles/crab_Dilepton_TopLeptonMVAStudy_preUL_2017_TTTo2L2Nu/230412_063803/0000/'], 'mc', 'TTTo2L2Nu', '2017', '', '87.31', '41.53', '8705576', 1]

#UL ntuples are pre-selected with cut = "((Sum$(Electron_pt>20 && abs(Electron_eta)<2.4 && Electron_sip3d<15) + Sum$(Muon_pt>20 && abs(Muon_eta)<2.4 && Muon_sip3d<15 && Muon_mediumId))>=2)"
#Please apply event selection that is no looser than the pre-selection
mc2017_samples['2017_TTTo2L2Nu_UL'] = [['/eos/cms/store/user/jingyan/LFV_Dilepton_TopLeptonMVAStudy/2017_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Dilepton_TopLeptonMVAStudy_UL_2017_TTTo2L2Nu/230411_165319/0000/'], 'mc', 'TTTo2L2Nu', '2017', '', '87.31', '41.53', '106724000', 1]


