import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}
# mc2017_samples["2017_LFVStVecU"] = ["address", "data/mc", "dataset", "year", "run", "cross section", "lumi", "Neventsraw", "# of files per job"]

# cut = "((Sum$(Electron_pt>20 && abs(Electron_eta)<2.4 && Electron_sip3d<8 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1 && Electron_miniPFRelIso_all<0.4 && Electron_lostHits<2 && Electron_convVeto && Electron_tightCharge>0)"
# cut += " + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_mediumId && Muon_sip3d<8 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1 && Muon_miniPFRelIso_all<0.4))>=1)"
# cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=2 && Tau_idDeepTau2017v2p1VSmu>=8 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

# Real background samples
mc2017_samples["2017_TTH"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_2017LFVSignalAndData_v2_2017_TTH_UL/231104_235646/0000/"], "mc", "TTH", "2017", "", "0.211", "41.48", "3077771", 6]
mc2017_samples["2017_TTW"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017LFVSignalAndData_v1_2017_TTW_UL/231103_212458/0000/"], "mc", "TTW", "2017", "", "0.235", "41.48", "3871055", 5]
mc2017_samples["2017_TTZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_2017LFVSignalAndData_v1_2017_TTZ_UL/231103_215519/0000/"], "mc", "TTZ", "2017", "", "0.281", "41.48", "6911466", 5]
mc2017_samples["2017_WZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2017LFVSignalAndData_v1_2017_WZ_UL/231103_214347/0000/"], "mc", "WZ", "2017", "", "4.9173", "41.48", "6826898", 31]
mc2017_samples["2017_ZZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_2017LFVSignalAndData_v2_2017_ZZ_UL/231104_235918/0000/"], "mc", "ZZ", "2017", "", "1.256", "41.48", "98378104", 11]
mc2017_samples["2017_WWW"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_2017LFVSignalAndData_v1_2017_WWW_UL/231103_213142/0000/"], "mc", "WWW", "2017", "", "0.2086", "41.48", "154830", 16]
mc2017_samples["2017_WWZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_2017LFVSignalAndData_v1_2017_WWZ_UL/231103_212134/0000/"], "mc", "WWZ", "2017", "", "0.1651", "41.48", "161398", 5]
mc2017_samples["2017_WZZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_2017LFVSignalAndData_v1_2017_WZZ_UL/231103_214238/0000/"], "mc", "WZZ", "2017", "", "0.05565", "41.48", "270316", 2]
mc2017_samples["2017_ZZZ"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_2017LFVSignalAndData_v1_2017_ZZZ_UL/231103_212605/0000/"], "mc", "ZZZ", "2017", "", "0.01476", "41.48", "158612", 15]
mc2017_samples["2017_TTTo2L2Nu"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_2017LFVSignalAndData_v1_2017_TTTo2L2Nu_UL/231103_213741/0000/"], "mc", "TTTo2L2Nu", "2017", "", "88.4", "41.48", "105859990", 4]
mc2017_samples["2017_WWTo2L2Nu"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_2017LFVSignalAndData_v1_2017_WWTo2L2Nu_UL/231103_213621/0000/"], "mc", "WWTo2L2Nu", "2017", "", "12.178", "41.48", "7071358", 46]

# Fake background samples
mc2017_samples["2017_DYM10to50"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017LFVSignalAndData_v2_2017_DY10to50_UL/231105_000153/0000/"], "mc", "DYM10to50", "2017", "", "15810", "41.48", "68480179", 77]
mc2017_samples["2017_DYM50"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2017LFVSignalAndData_v1_2017_DY50_UL/231103_213400/0000/"], "mc", "DYM50", "2017", "", "6077.22", "41.48", "131552424", 14]
mc2017_samples["2017_TTToSemiLeptonic"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_2017LFVSignalAndData_v2_2017_TTToSemiLeptonic_UL/231104_235505/0000/"], "mc", "TTToSemiLeptonic", "2017", "", "365.34", "41.48", "341194592", 8]
mc2017_samples["2017_ZZTo2L2Nu"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_2017LFVSignalAndData_v2_2017_ZZTo2L2Nu_UL/231104_235737/0000/"], "mc", "ZZTo2L2Nu", "2017", "", "0.564", "41.48", "40753260", 15]
mc2017_samples["2017_WJets"] = [["/eos/cms/store/user/jingyan/LFV_WJets/2017_WJets_UL/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_WJets_2017_WJets_UL/240710_234847/0000/"], "mc", "WJets", "2017", "", "61526.7", "41.48", "78307186", 10]

# Data
data2017_samples["2017_B_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_B_MuonEG/MuonEG/crab_2017LFVSignalAndData_v1_2017_B_MuonEG/231103_211701/0000/"], "data", "MuonEG", "2017", "B", "1", "1", "1", 6]
data2017_samples["2017_C_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_C_MuonEG/MuonEG/crab_2017LFVSignalAndData_v1_2017_C_MuonEG/231103_212925/0000/"], "data", "MuonEG", "2017", "C", "1", "1", "1", 17]
data2017_samples["2017_D_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_D_MuonEG/MuonEG/crab_2017LFVSignalAndData_v1_2017_D_MuonEG/231103_215848/0000/"], "data", "MuonEG", "2017", "D", "1", "1", "1", 13]
data2017_samples["2017_E_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_E_MuonEG/MuonEG/crab_2017LFVSignalAndData_v1_2017_E_MuonEG/231103_214457/0000/"], "data", "MuonEG", "2017", "E", "1", "1", "1", 8]
data2017_samples["2017_F_MuonEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_F_MuonEG/MuonEG/crab_2017LFVSignalAndData_v1_2017_F_MuonEG/231103_214719/0000/"], "data", "MuonEG", "2017", "F", "1", "1", "1", 8]

data2017_samples["2017_B_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_B_DoubleEG/DoubleEG/crab_2017LFVSignalAndData_v1_2017_B_DoubleEG/231103_213511/0000/"], "data", "DoubleEG", "2017", "B", "1", "1", "1", 8]
data2017_samples["2017_C_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_C_DoubleEG/DoubleEG/crab_2017LFVSignalAndData_v1_2017_C_DoubleEG/231103_214934/0000/"], "data", "DoubleEG", "2017", "C", "1", "1", "1", 9]
data2017_samples["2017_D_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_D_DoubleEG/DoubleEG/crab_2017LFVSignalAndData_v1_2017_D_DoubleEG/231103_211446/0000/"], "data", "DoubleEG", "2017", "D", "1", "1", "1", 7]
data2017_samples["2017_E_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_E_DoubleEG/DoubleEG/crab_2017LFVSignalAndData_v1_2017_E_DoubleEG/231103_215408/0000/"], "data", "DoubleEG", "2017", "E", "1", "1", "1", 8]
data2017_samples["2017_F_DoubleEG"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_F_DoubleEG/DoubleEG/crab_2017LFVSignalAndData_v2_2017_F_DoubleEG/231104_235556/0000/"], "data", "DoubleEG", "2017", "F", "1", "1", "1", 10]

data2017_samples["2017_B_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_B_DoubleMuon/DoubleMuon/crab_2017LFVSignalAndData_v1_2017_B_DoubleMuon/231103_215628/0000/"], "data", "DoubleMuon", "2017", "B", "1", "1", "1", 8]
data2017_samples["2017_C_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_C_DoubleMuon/DoubleMuon/crab_2017LFVSignalAndData_v1_2017_C_DoubleMuon/231103_212240/0000/"], "data", "DoubleMuon", "2017", "C", "1", "1", "1", 15]
data2017_samples["2017_D_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_D_DoubleMuon/DoubleMuon/crab_2017LFVSignalAndData_v1_2017_D_DoubleMuon/231103_215958/0000/"], "data", "DoubleMuon", "2017", "D", "1", "1", "1", 16]
data2017_samples["2017_E_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_E_DoubleMuon/DoubleMuon/crab_2017LFVSignalAndData_v1_2017_E_DoubleMuon/231103_214610/0000/"], "data", "DoubleMuon", "2017", "E", "1", "1", "1", 17]
data2017_samples["2017_F_DoubleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_F_DoubleMuon/DoubleMuon/crab_2017LFVSignalAndData_v2_2017_F_DoubleMuon/231105_000010/0000/"], "data", "DoubleMuon", "2017", "F", "1", "1", "1", 30]

data2017_samples["2017_B_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_B_SingleElectron/SingleElectron/crab_2017LFVSignalAndData_v1_2017_B_SingleElectron/231103_211339/0000/"], "data", "SingleElectron", "2017", "B", "1", "1", "1", 16]
data2017_samples["2017_C_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_C_SingleElectron/SingleElectron/crab_2017LFVSignalAndData_v1_2017_C_SingleElectron/231103_215043/0000/"], "data", "SingleElectron", "2017", "C", "1", "1", "1", 20]
data2017_samples["2017_D_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_D_SingleElectron/SingleElectron/crab_2017LFVSignalAndData_v1_2017_D_SingleElectron/231103_215737/0000/"], "data", "SingleElectron", "2017", "D", "1", "1", "1", 18]
data2017_samples["2017_E_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_E_SingleElectron/SingleElectron/crab_2017LFVSignalAndData_v1_2017_E_SingleElectron/231103_215259/0000/"], "data", "SingleElectron", "2017", "E", "1", "1", "1", 17]
data2017_samples["2017_F_SingleElectron"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_F_SingleElectron/SingleElectron/crab_2017LFVSignalAndData_v2_2017_F_SingleElectron/231105_000243/0000/"], "data", "SingleElectron", "2017", "F", "1", "1", "1", 17]

data2017_samples["2017_B_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_B_SingleMuon/SingleMuon/crab_2017LFVSignalAndData_v3_2017_B_SingleMuon/231105_094040/0000/"], "data", "SingleMuon", "2017", "B", "1", "1", "1", 52]
data2017_samples["2017_C_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_C_SingleMuon/SingleMuon/crab_2017LFVSignalAndData_v2_2017_C_SingleMuon/231104_235826/0000/"], "data", "SingleMuon", "2017", "C", "1", "1", "1", 32]
data2017_samples["2017_D_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_D_SingleMuon/SingleMuon/crab_2017LFVSignalAndData_v2_2017_D_SingleMuon/231105_000333/0000/"], "data", "SingleMuon", "2017", "D", "1", "1", "1", 40]
data2017_samples["2017_E_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_E_SingleMuon/SingleMuon/crab_2017LFVSignalAndData_v2_2017_E_SingleMuon/231105_000102/0000/"], "data", "SingleMuon", "2017", "E", "1", "1", "1", 28]
data2017_samples["2017_F_SingleMuon"] = [["/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_F_SingleMuon/SingleMuon/crab_2017LFVSignalAndData_v2_2017_F_SingleMuon/231105_000426/0000/"], "data", "SingleMuon", "2017", "F", "1", "1", "1", 35]
