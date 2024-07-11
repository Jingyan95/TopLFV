import sys
import os
import subprocess
import readline
import string

data2016_samples = {}
mc2016_samples = {}
# mc2016_samples["2016_LFVStVecU"] = ["address", "data/mc", "dataset", "year", "run", "cross section", "lumi", "Neventsraw", "# of files per job"]

# cut = "((Sum$(Electron_pt>20 && abs(Electron_eta)<2.4 && Electron_sip3d<8 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1 && Electron_miniPFRelIso_all<0.4 && Electron_lostHits<2 && Electron_convVeto && Electron_tightCharge>0)"
# cut += " + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_mediumId && Muon_sip3d<8 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1 && Muon_miniPFRelIso_all<0.4))>=1)"
# cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=2 && Tau_idDeepTau2017v2p1VSmu>=8 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

# Real background samples
mc2016_samples["2016_TTW"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2016LFVSignalAndData_v5_2016_TTW_UL/231103_181048/0000/"], "mc", "TTW", "2016", "", "0.235", "16.81", "1800823", 6]
mc2016_samples["2016_TTH"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_2016LFVSignalAndData_v5_2016_TTH_UL/231103_180906/0000/"], "mc", "TTH", "2016", "", "0.211", "16.81", "1622956", 8]
mc2016_samples["2016_TTZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_2016LFVSignalAndData_v3_2016_TTZ_UL/231102_130059/0000/"], "mc", "TTZ", "2016", "", "0.281", "16.81", "2962856", 14]
mc2016_samples["2016_WZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2016LFVSignalAndData_v3_2016_WZ_UL/231102_125152/0000/"], "mc", "WZ", "2016", "", "4.9173", "16.81", "6890010", 16]
mc2016_samples["2016_ZZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_2016LFVSignalAndData_v5_2016_ZZ_UL/231103_180956/0000/"], "mc", "ZZ", "2016", "", "1.256", "16.81", "51577084", 11]
mc2016_samples["2016_WWW"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_2016LFVSignalAndData_v3_2016_WWW_UL/231102_125945/0000/"], "mc", "WWW", "2016", "", "0.2086", "16.81", "62442", 14]
mc2016_samples["2016_WWZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_2016LFVSignalAndData_v3_2016_WWZ_UL/231102_124841/0000/"], "mc", "WWZ", "2016", "", "0.1651", "16.81", "61060", 8]
mc2016_samples["2016_WZZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_2016LFVSignalAndData_v3_2016_WZZ_UL/231102_125806/0000/"], "mc", "WZZ", "2016", "", "0.05565", "16.81", "124388", 18]
mc2016_samples["2016_ZZZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_2016LFVSignalAndData_v3_2016_ZZZ_UL/231102_130312/0000/"], "mc", "ZZZ", "2016", "", "0.01476", "16.81", "64358", 4]
mc2016_samples["2016_TTTo2L2Nu"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_2016LFVSignalAndData_v5_2016_TTTo2L2Nu_UL/231103_181142/0000/"], "mc", "TTTo2L2Nu", "2016", "", "88.4", "16.81", "43193956", 5]
mc2016_samples["2016_WWTo2L2Nu"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_2016LFVSignalAndData_v3_2016_WWTo2L2Nu_UL/231102_130205/0000/"], "mc", "WWTo2L2Nu", "2016", "", "12.178", "16.81", "2888924", 7]

# Fake background samples
mc2016_samples["2016_DYM10to50"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2016LFVSignalAndData_v5_2016_DY10to50_UL/231103_180815/0000/"], "mc", "DYM10to50", "2016", "", "15810", "16.81", "22388550", 34]
mc2016_samples["2016_DYM50"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2016LFVSignalAndData_v5_2016_DY50_UL/231103_180636/0000/"], "mc", "DYM50", "2016", "", "6077.22", "16.81", "48335328", 11]
mc2016_samples["2016_TTToSemiLeptonic"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_2016LFVSignalAndData_v5_2016_TTToSemiLeptonic_UL/231103_181232/0000/"], "mc", "TTToSemiLeptonic", "2016", "", "365.34", "16.81", "143553998", 6]
mc2016_samples["2016_ZZTo2L2Nu"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_2016LFVSignalAndData_v3_2016_ZZTo2L2Nu_UL/231102_125502/0000/"], "mc", "ZZTo2L2Nu", "2016", "", "0.564", "16.81", "15894442", 15]
mc2016_samples["2016_WJets"] = [["/eos/cms/store/user/jingyan/LFV_WJets/2016_WJets_UL/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_WJets_2016_WJets_UL/240710_234739/0000/"], "mc", "WJets", "2016", "", "61526.7", "16.81", "80958227", 10]

# Data
data2016_samples["2016_F_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_F_MuonEG/MuonEG/crab_2016LFVSignalAndData_2016_F_MuonEG/231101_094952/0000/"], "data", "MuonEG", "2016", "F", "1", "1", "1", 3]
data2016_samples["2016_G_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_G_MuonEG/MuonEG/crab_2016LFVSignalAndData_v6_2016_G_MuonEG/231109_130946/0000/"], "data", "MuonEG", "2016", "G", "1", "1", "1", 15]
data2016_samples["2016_H_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_H_MuonEG/MuonEG/crab_2016LFVSignalAndData_v6_2016_H_MuonEG/231109_131059/0000/"], "data", "MuonEG", "2016", "H", "1", "1", "1", 10]

data2016_samples["2016_F_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_F_DoubleEG/DoubleEG/crab_2016LFVSignalAndData_2016_F_DoubleEG/231101_094047/0000/"], "data", "DoubleEG", "2016", "F", "1", "1", "1", 5]
data2016_samples["2016_G_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_G_DoubleEG/DoubleEG/crab_Dilepton2016Data_2016_G_DoubleEG/231101_163437/0000/"], "data", "DoubleEG", "2016", "G", "1", "1", "1", 8]
data2016_samples["2016_H_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_H_DoubleEG/DoubleEG/crab_Dilepton2016Data_2016_H_DoubleEG/231101_163534/0000/"], "data", "DoubleEG", "2016", "H", "1", "1", "1", 11]

data2016_samples["2016_F_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_F_DoubleMuon/DoubleMuon/crab_2016LFVSignalAndData_2016_F_DoubleMuon/231101_095323/0000/"], "data", "DoubleMuon", "2016", "F", "1", "1", "1", 1]
data2016_samples["2016_G_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_G_DoubleMuon/DoubleMuon/crab_2016LFVSignalAndData_v6_2016_G_DoubleMuon/231109_131202/0000/"], "data", "DoubleMuon", "2016", "G", "1", "1", "1", 29]
data2016_samples["2016_H_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_H_DoubleMuon/DoubleMuon/crab_2016LFVSignalAndData_2016_H_DoubleMuon/231101_095415/0000/"], "data", "DoubleMuon", "2016", "H", "1", "1", "1", 28]

data2016_samples["2016_F_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_F_SingleElectron/SingleElectron/crab_2016LFVSignalAndData_2016_F_SingleElectron/231101_093953/0000/"], "data", "SingleElectron", "2016", "F", "1", "1", "1", 5]
data2016_samples["2016_G_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_G_SingleElectron/SingleElectron/crab_2016LFVSignalAndData_2016_G_SingleElectron/231101_095046/0000/"], "data", "SingleElectron", "2016", "G", "1", "1", "1", 18]
data2016_samples["2016_H_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_H_SingleElectron/SingleElectron/crab_2016LFVSignalAndData_v5_2016_H_SingleElectron/231103_180726/0000/"], "data", "SingleElectron", "2016", "H", "1", "1", "1", 20]

data2016_samples["2016_F_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_F_SingleMuon/SingleMuon/crab_2016LFVSignalAndData_2016_F_SingleMuon/231101_094234/0000/"], "data", "SingleMuon", "2016", "F", "1", "1", "1", 5]
data2016_samples["2016_G_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_G_SingleMuon/SingleMuon/crab_2016LFVSignalAndData_2016_G_SingleMuon/231101_095232/0000/"], "data", "SingleMuon", "2016", "G", "1", "1", "1", 24]
data2016_samples["2016_H_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2016/2016_H_SingleMuon/SingleMuon/crab_2016LFVSignalAndData_2016_H_SingleMuon/231101_094716/0000/"], "data", "SingleMuon", "2016", "H", "1", "1", "1", 28]
