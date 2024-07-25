import sys
import os
import subprocess
import readline
import string

data2016APV_samples = {}
mc2016APV_samples = {}
# mc2016APV_samples["2016APV_LFVStVecU"] = ["address", "data/mc", "dataset", "year", "run", "cross section", "lumi", "Neventsraw", "# of files per job"]

# cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<15) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<15 && Muon_mediumId))>=2)"
# cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=1 && Tau_idDeepTau2017v2p1VSmu>=1 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

# Scalar interaction
mc2016APV_samples["2016APV_LFVStScalarU"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_LFVStScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2016APV_LFVStScalarU_UL/230911_225953/0000/"], "mc", "LFVStScalarU", "2016APV", "", "0.097", "19.50", "209000", 209]
mc2016APV_samples["2016APV_LFVTtScalarU"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_LFVTtScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2016APV_LFVTtScalarU_UL/230911_230050/0000/"], "mc", "LFVTtScalarU", "2016APV", "", "0.004", "19.50", "223000", 223]

# Real background samples
mc2016APV_samples["2016APV_TTH"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Aug17_2016APV_TTH_UL/230818_001242/0000/"], "mc", "TTH", "2016APV", "", "0.211", "19.50", "1595435", 14]
mc2016APV_samples["2016APV_TTW"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug17_2016APV_TTW_UL/230818_002405/0000/"], "mc", "TTW", "2016APV", "", "0.235", "19.50", "1543290", 13]
mc2016APV_samples["2016APV_TTZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2016APV_TTZ_UL/230818_002551/0000/"], "mc", "TTZ", "2016APV", "", "0.281", "19.50", "2856626", 8]
mc2016APV_samples["2016APV_WZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug17_2016APV_WZ_UL/230818_000913/0000/"], "mc", "WZ", "2016APV", "", "4.9173", "19.50", "6355769", 32]
mc2016APV_samples["2016APV_ZZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Aug17_2016APV_ZZ_UL/230817_234902/0000/"], "mc", "ZZ", "2016APV", "", "1.256", "19.50", "49189654", 11]
mc2016APV_samples["2016APV_WWW"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2016APV_WWW_UL/230817_235634/0000/"], "mc", "WWW", "2016APV", "", "0.2086", "19.50", "64296", 9]
mc2016APV_samples["2016APV_WWZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2016APV_WWZ_UL/230818_001519/0000/"], "mc", "WWZ", "2016APV", "", "0.1651", "19.50", "73734", 8]
mc2016APV_samples["2016APV_WZZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2016APV_WZZ_UL/230818_000451/0000/"], "mc", "WZZ", "2016APV", "", "0.05565", "19.50", "145164", 8]
mc2016APV_samples["2016APV_ZZZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2016APV_ZZZ_UL/230818_001334/0000/"], "mc", "ZZZ", "2016APV", "", "0.01476", "19.50", "71860", 9]

# Fake background samples
mc2016APV_samples["2016APV_DYM10to50"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Aug17_2016APV_DY10to50_UL/230818_005624/0000/"], "mc", "DYM10to50", "2016APV", "", "15810", "19.50", "25799525", 19]
mc2016APV_samples["2016APV_DYM50"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug17_2016APV_DY50_UL/230818_000821/0000/"], "mc", "DYM50", "2016APV", "", "6077.22", "19.50", "61192713", 11]
mc2016APV_samples["2016APV_TTTo2L2Nu"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2016APV_TTTo2L2Nu_UL/230818_005437/0000/"], "mc", "TTTo2L2Nu", "2016APV", "", "88.4", "19.50", "37202074", 4]
mc2016APV_samples["2016APV_TTToSemiLeptonic"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2016APV_TTToSemiLeptonic_UL/230818_002312/0000/"], "mc", "TTToSemiLeptonic", "2016APV", "", "365.34", "19.50", "131106830", 8]
mc2016APV_samples["2016APV_WWTo2L2Nu"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2016APV_WWTo2L2Nu_UL/230817_234958/0000/"], "mc", "WWTo2L2Nu", "2016APV", "", "12.178", "19.50", "3006596", 12]
mc2016APV_samples["2016APV_ZZTo2L2Nu"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Aug17_2016APV_ZZTo2L2Nu_UL/230818_001006/0000/"], "mc", "ZZTo2L2Nu", "2016APV", "", "0.564", "19.50", "16826232", 25]

# Data
data2016APV_samples["2016APV_Bv1_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv1_MuonEG/MuonEG/crab_Aug17_2016APV_Bv1_MuonEG/230817_235733/0000/"], "data", "MuonEG", "2016APV", "B", "1", "1", "1", 1]
data2016APV_samples["2016APV_Bv2_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv2_MuonEG/MuonEG/crab_Aug17_2016APV_Bv2_MuonEG/230818_005601/0000/"], "data", "MuonEG", "2016APV", "B", "1", "1", "1", 8]
data2016APV_samples["2016APV_C_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_C_MuonEG/MuonEG/crab_Aug17_2016APV_C_MuonEG/230818_000305/0000/"], "data", "MuonEG", "2016APV", "C", "1", "1", "1", 14]
data2016APV_samples["2016APV_D_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_D_MuonEG/MuonEG/crab_Aug17_2016APV_D_MuonEG/230818_000728/0000/"], "data", "MuonEG", "2016APV", "D", "1", "1", "1", 17]
data2016APV_samples["2016APV_E_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_E_MuonEG/MuonEG/crab_Aug17_2016APV_E_MuonEG/230818_005450/0000/"], "data", "MuonEG", "2016APV", "E", "1", "1", "1", 16]
data2016APV_samples["2016APV_F_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_F_MuonEG/MuonEG/crab_Aug17_2016APV_F_MuonEG/230817_235052/0000/"], "data", "MuonEG", "2016APV", "F", "1", "1", "1", 14]

data2016APV_samples["2016APV_Bv1_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv1_DoubleEG/DoubleEG/crab_Aug17_2016APV_Bv1_DoubleEG/230817_233710/0000/"], "data", "DoubleEG", "2016APV", "B", "1", "1", "1", 7]
data2016APV_samples["2016APV_Bv2_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv2_DoubleEG/DoubleEG/crab_Aug17_2016APV_Bv2_DoubleEG/230818_005719/0000/"], "data", "DoubleEG", "2016APV", "B", "1", "1", "1", 10]
data2016APV_samples["2016APV_C_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_C_DoubleEG/DoubleEG/crab_Aug17_2016APV_C_DoubleEG/230817_235148/0000/"], "data", "DoubleEG", "2016APV", "C", "1", "1", "1", 11]
data2016APV_samples["2016APV_D_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_D_DoubleEG/DoubleEG/crab_Aug17_2016APV_D_DoubleEG/230818_001427/0000/"], "data", "DoubleEG", "2016APV", "D", "1", "1", "1", 14]
data2016APV_samples["2016APV_E_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_E_DoubleEG/DoubleEG/crab_Aug17_2016APV_E_DoubleEG/230817_235832/0000/"], "data", "DoubleEG", "2016APV", "E", "1", "1", "1", 7]
data2016APV_samples["2016APV_F_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_F_DoubleEG/DoubleEG/crab_Aug17_2016APV_F_DoubleEG/230818_001152/0000/"], "data", "DoubleEG", "2016APV", "F", "1", "1", "1", 11]

data2016APV_samples["2016APV_Bv1_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv1_DoubleMuon/DoubleMuon/crab_Aug17_2016APV_Bv1_DoubleMuon/230817_235428/0000/"], "data", "DoubleMuon", "2016APV", "B", "1", "1", "1", 3]
data2016APV_samples["2016APV_Bv2_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv2_DoubleMuon/DoubleMuon/crab_Aug17_2016APV_Bv2_DoubleMuon/230818_000026/0000/"], "data", "DoubleMuon", "2016APV", "B", "1", "1", "1", 39]
data2016APV_samples["2016APV_C_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_C_DoubleMuon/DoubleMuon/crab_Aug17_2016APV_C_DoubleMuon/230817_234808/0000/"], "data", "DoubleMuon", "2016APV", "C", "1", "1", "1", 16]
data2016APV_samples["2016APV_D_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_D_DoubleMuon/DoubleMuon/crab_Aug17_2016APV_D_DoubleMuon/230818_000213/0000/"], "data", "DoubleMuon", "2016APV", "D", "1", "1", "1", 22]
data2016APV_samples["2016APV_E_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_E_DoubleMuon/DoubleMuon/crab_Aug17_2016APV_E_DoubleMuon/230818_005510/0000/"], "data", "DoubleMuon", "2016APV", "E", "1", "1", "1", 19]
data2016APV_samples["2016APV_F_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_F_DoubleMuon/DoubleMuon/crab_Aug17_2016APV_F_DoubleMuon/230818_001058/0000/"], "data", "DoubleMuon", "2016APV", "F", "1", "1", "1", 10]

data2016APV_samples["2016APV_Bv1_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv1_SingleElectron/SingleElectron/crab_Aug17_2016APV_Bv1_SingleElectron/230818_005617/0000/"], "data", "SingleElectron", "2016APV", "B", "1", "1", "1", 1]
data2016APV_samples["2016APV_Bv2_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv2_SingleElectron/SingleElectron/crab_Aug17_2016APV_Bv2_SingleElectron/230818_000636/0000/"], "data", "SingleElectron", "2016APV", "B", "1", "1", "1", 22]
data2016APV_samples["2016APV_C_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_C_SingleElectron/SingleElectron/crab_Aug17_2016APV_C_SingleElectron/230818_002643/0000/"], "data", "SingleElectron", "2016APV", "C", "1", "1", "1", 17]
data2016APV_samples["2016APV_D_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_D_SingleElectron/SingleElectron/crab_Aug17_2016APV_D_SingleElectron/230817_235931/0000/"], "data", "SingleElectron", "2016APV", "D", "1", "1", "1", 17]
data2016APV_samples["2016APV_E_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_E_SingleElectron/SingleElectron/crab_Aug17_2016APV_E_SingleElectron/230818_000358/0000/"], "data", "SingleElectron", "2016APV", "E", "1", "1", "1", 19]
data2016APV_samples["2016APV_F_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_F_SingleElectron/SingleElectron/crab_Aug17_2016APV_F_SingleElectron/230818_000121/0000/"], "data", "SingleElectron", "2016APV", "F", "1", "1", "1", 20]

data2016APV_samples["2016APV_Bv1_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv1_SingleMuon/SingleMuon/crab_Aug17_2016APV_Bv1_SingleMuon/230817_235334/0000/"], "data", "SingleMuon", "2016APV", "B", "1", "1", "1", 2]
data2016APV_samples["2016APV_Bv2_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_Bv2_SingleMuon/SingleMuon/crab_Aug17_2016APV_Bv2_SingleMuon/230817_235243/0000/"], "data", "SingleMuon", "2016APV", "B", "1", "1", "1", 35]
data2016APV_samples["2016APV_C_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_C_SingleMuon/SingleMuon/crab_Aug17_2016APV_C_SingleMuon/230818_005459/0000/"], "data", "SingleMuon", "2016APV", "C", "1", "1", "1", 28]
data2016APV_samples["2016APV_D_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_D_SingleMuon/SingleMuon/crab_Aug17_2016APV_D_SingleMuon/230817_235522/0000/"], "data", "SingleMuon", "2016APV", "D", "1", "1", "1", 20]
data2016APV_samples["2016APV_E_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_E_SingleMuon/SingleMuon/crab_Aug17_2016APV_E_SingleMuon/230818_002458/0000/"], "data", "SingleMuon", "2016APV", "E", "1", "1", "1", 24]
data2016APV_samples["2016APV_F_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016APV/2016APV_F_SingleMuon/SingleMuon/crab_Aug17_2016APV_F_SingleMuon/230818_005609/0000/"], "data", "SingleMuon", "2016APV", "F", "1", "1", "1", 43]
