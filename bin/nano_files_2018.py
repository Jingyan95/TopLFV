import sys
import os
import subprocess
import readline
import string

data2018_samples = {}
mc2018_samples = {}
# mc2018_samples["2018_LFVStVecU"] = ["address", "data/mc", "dataset", "year", "run", "cross section", "lumi", "Neventsraw", "# of files per job"]

# cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<15) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<15 && Muon_mediumId))>=2)"
# cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=1 && Tau_idDeepTau2017v2p1VSmu>=1 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

# Scalar interaction
mc2018_samples["2018_LFVStScalarU"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_LFVStScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2018_LFVStScalarU_UL/230911_230932/0000/"], "mc", "LFVStScalarU", "2018", "", "0.097", "59.83", "227000", 229]
mc2018_samples["2018_LFVTtScalarU"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_LFVTtScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2018_LFVTtScalarU_UL/230911_231026/0000/"], "mc", "LFVTtScalarU", "2018", "", "0.004", "59.83", "229000", 229]

# Real background samples
mc2018_samples["2018_TTH"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Aug17_2018_TTH_UL/230817_233525/0000/"], "mc", "TTH", "2018", "", "0.211", "59.83", "3235099", 17]
mc2018_samples["2018_TTW"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug17_2018_TTW_UL/230817_235640/0000/"], "mc", "TTW", "2018", "", "0.235", "59.83", "5666428", 4]
mc2018_samples["2018_TTZ"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2018_TTZ_UL/230817_234834/0000/"], "mc", "TTZ", "2018", "", "0.281", "59.83", "9651834", 4]
mc2018_samples["2018_WZ"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug17_2018_WZ_UL/230817_235454/0000/"], "mc", "WZ", "2018", "", "4.9173", "59.83", "6482815", 18]
mc2018_samples["2018_ZZ"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Aug17_2018_ZZ_UL/230817_235835/0000/"], "mc", "ZZ", "2018", "", "1.256", "59.83", "56239302", 16]
mc2018_samples["2018_WWW"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2018_WWW_UL/230817_232746/0000/"], "mc", "WWW", "2018", "", "0.2086", "59.83", "216852", 5]
mc2018_samples["2018_WWZ"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug19_2018_WWZ_UL/230819_160328/0000/"], "mc", "WWZ", "2018", "", "0.1651", "59.83", "224734", 5]
mc2018_samples["2018_WZZ"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2018_WZZ_UL/230817_235021/0000/"], "mc", "WZZ", "2018", "", "0.05565", "59.83", "271866", 15]
mc2018_samples["2018_ZZZ"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2018_ZZZ_UL/230817_235933/0000/"], "mc", "ZZZ", "2018", "", "0.01476", "59.83", "222716", 14]

# Fake background samples
mc2018_samples["2018_DYM10to50"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Aug17_2018_DY10to50_UL/230817_235400/0000/"], "mc", "DYM10to50", "2018", "", "15810", "59.83", "94452816", 84]
mc2018_samples["2018_DYM50"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug17_2018_DY50_UL/230817_234927/0000/"], "mc", "DYM50", "2018", "", "6077.22", "59.83", "131572454", 19]
mc2018_samples["2018_TTTo2L2Nu"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2018_TTTo2L2Nu_UL/230817_235305/0000/"], "mc", "TTTo2L2Nu", "2018", "", "88.4", "59.83", "143848848", 4]
mc2018_samples["2018_TTToSemiLeptonic"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2018_TTToSemiLeptonic_UL/230817_235210/0000/"], "mc", "TTToSemiLeptonic", "2018", "", "365.34", "59.83", "472557630", 8]
mc2018_samples["2018_WWTo2L2Nu"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2018_WWTo2L2Nu_UL/230817_235549/0000/"], "mc", "WWTo2L2Nu", "2018", "", "12.178", "59.83", "9956710", 19]
mc2018_samples["2018_ZZTo2L2Nu"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Aug17_2018_ZZTo2L2Nu_UL/230817_235116/0000/"], "mc", "ZZTo2L2Nu", "2018", "", "0.564", "59.83", "97491908", 11]

mc2018_samples["2018_DYGamma"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2018_DYGamma/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_PhotonConv_2018_DYGamma/240826_012031/0000/"], "mc", "DYGamma", "2018",  "", "55.48", "59.83", "18750664", 19]
mc2018_samples["2018_TTGammaDiL"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2018_TTGammaDiL/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/crab_Trilep_PhotonConv_2018_TTGammaDiL/240826_012135/0000/"], "mc", "TTGammaDiL", "2018",  "", "2.22", "59.83", "14694000", 15]
mc2018_samples["2018_TTGammaSingleL"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2018_TTGammaSingleL/TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/crab_Trilep_PhotonConv_2018_TTGammaSingleL/240826_012239/0000/"], "mc", "TTGammaSingleL", "2018",  "", "7.509", "59.83", "27731999", 31]
mc2018_samples["2018_TTGammaHad"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2018_TTGammaHad/TTGamma_Hadronic_TuneCP5_13TeV-madgraph-pythia8/crab_Trilep_PhotonConv_2018_TTGammaHad/240826_011927/0000/"], "mc", "TTGammaHad", "2018",  "", "6.162", "59.83", "14763000",  26]

# Data
data2018_samples["2018_A_MuonEG"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_A_MuonEG/MuonEG/crab_Aug17_2018Data_2018_A_MuonEG/230818_010753/0000/"], "data", "MuonEG", "2018", "A", "1", "1", "1", 11]
data2018_samples["2018_B_MuonEG"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_B_MuonEG/MuonEG/crab_Aug17_2018Data_2018_B_MuonEG/230818_012008/0000/"], "data", "MuonEG", "2018", "B", "1", "1", "1", 6]
data2018_samples["2018_C_MuonEG"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_C_MuonEG/MuonEG/crab_Aug17_2018Data_2018_C_MuonEG/230818_011237/0000/"], "data", "MuonEG", "2018", "C", "1", "1", "1", 7]
data2018_samples["2018_D_MuonEG"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_D_MuonEG/MuonEG/crab_Aug17_2018Data_2018_D_MuonEG/230818_011622/0000/"], "data", "MuonEG", "2018", "D", "1", "1", "1", 10]

data2018_samples["2018_A_EGamma"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_A_EGamma/EGamma/crab_Aug17_2018Data_2018_A_EGamma/230818_010656/0000/"], "data", "EGamma", "2018", "A", "1", "1", "1", 12]
data2018_samples["2018_B_EGamma"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_B_EGamma/EGamma/crab_Aug17_2018Data_2018_B_EGamma/230818_010947/0000/"], "data", "EGamma", "2018", "B", "1", "1", "1", 9]
data2018_samples["2018_C_EGamma"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_C_EGamma/EGamma/crab_Aug17_2018Data_2018_C_EGamma/230818_011912/0000/"], "data", "EGamma", "2018", "C", "1", "1", "1", 12]
data2018_samples["2018_D_EGamma"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_D_EGamma/EGamma/crab_Aug17_2018Data_2018_D_EGamma/230818_011815/0000/"], "data", "EGamma", "2018", "D", "1", "1", "1", 12]

data2018_samples["2018_A_DoubleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_A_DoubleMuon/DoubleMuon/crab_Aug17_2018Data_2018_A_DoubleMuon/230818_011429/0000/"], "data", "DoubleMuon", "2018", "A", "1", "1", "1", 13]
data2018_samples["2018_B_DoubleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_B_DoubleMuon/DoubleMuon/crab_Aug17_2018Data_2018_B_DoubleMuon/230818_011526/0000/"], "data", "DoubleMuon", "2018", "B", "1", "1", "1", 18]
data2018_samples["2018_C_DoubleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_C_DoubleMuon/DoubleMuon/crab_Aug17_2018Data_2018_C_DoubleMuon/230818_011045/0000/"], "data", "DoubleMuon", "2018", "C", "1", "1", "1", 16]
data2018_samples["2018_D_DoubleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_D_DoubleMuon/DoubleMuon/crab_Aug17_2018Data_2018_D_DoubleMuon/230818_012105/0000/"], "data", "DoubleMuon", "2018", "D", "1", "1", "1", 22]

data2018_samples["2018_A_SingleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_A_SingleMuon/SingleMuon/crab_Aug19_2018_A_SingleMuon/230819_160218/0000/"], "data", "SingleMuon", "2018", "A", "1", "1", "1", 12]
data2018_samples["2018_B_SingleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_B_SingleMuon/SingleMuon/crab_Aug17_2018Data_2018_B_SingleMuon/230818_011719/0000/"], "data", "SingleMuon", "2018", "B", "1", "1", "1", 13]
data2018_samples["2018_C_SingleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_C_SingleMuon/SingleMuon/crab_Aug17_2018Data_2018_C_SingleMuon/230818_010850/0000/"], "data", "SingleMuon", "2018", "C", "1", "1", "1", 17]
data2018_samples["2018_D_SingleMuon"] = [["/eos/user/j/jingyan/TopLFV/LFV_Trilep_Inclusive/2018/2018_D_SingleMuon/SingleMuon/crab_Aug17_2018Data_2018_D_SingleMuon/230818_011140/0000/"], "data", "SingleMuon", "2018", "D", "1", "1", "1", 13]