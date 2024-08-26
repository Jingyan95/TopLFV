import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}
# mc2017_samples["2017_LFVStVecU"] = ["address", "data/mc", "dataset", "year", "run", "cross section", "lumi", "Neventsraw", "# of files per job"]

# cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<15) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<15 && Muon_mediumId))>=2)"
# cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=1 && Tau_idDeepTau2017v2p1VSmu>=1 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

# Scalar interaction
mc2017_samples["2017_LFVStScalarU"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_LFVStScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2017_LFVStScalarU_UL/230911_230737/0000/"], "mc", "LFVStScalarU", "2017", "", "0.097", "41.48", "229000", 229]
mc2017_samples["2017_LFVTtScalarU"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_LFVTtScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2017_LFVTtScalarU_UL/230911_230643/0000/"], "mc", "LFVTtScalarU", "2017", "", "0.004", "41.48", "237000", 237]

# Real background samples
mc2017_samples["2017_TTH"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Aug17_2017_TTH_UL/230817_235101/0000/"], "mc", "TTH", "2017", "", "0.211", "41.48", "3077771", 6]
mc2017_samples["2017_TTW"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Aug17_2017_TTW_UL/230817_235928/0000/"], "mc", "TTW", "2017", "", "0.235", "41.48", "3871055", 5]
mc2017_samples["2017_TTZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2017_TTZ_UL/230817_235634/0000/"], "mc", "TTZ", "2017", "", "0.281", "41.48", "6911466", 5]
mc2017_samples["2017_WZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug17_2017_WZ_UL/230817_235832/0000/"], "mc", "WZ", "2017", "", "4.9173", "41.48", "6826898", 11]
mc2017_samples["2017_ZZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Aug17_2017_ZZ_UL/230817_235252/0000/"], "mc", "ZZ", "2017", "", "1.256", "41.48", "98378104", 11]
mc2017_samples["2017_WWW"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2017_WWW_UL/230818_000119/0000/"], "mc", "WWW", "2017", "", "0.2086", "41.48", "154830", 16]
mc2017_samples["2017_WWZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2017_WWZ_UL/230817_235538/0000/"], "mc", "WWZ", "2017", "", "0.1651", "41.48", "161398", 5]
mc2017_samples["2017_WZZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2017_WZZ_UL/230817_235348/0000/"], "mc", "WZZ", "2017", "", "0.05565", "41.48", "270316", 2]
mc2017_samples["2017_ZZZ"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Aug17_2017_ZZZ_UL/230818_000023/0000/"], "mc", "ZZZ", "2017", "", "0.01476", "41.48", "158612", 15]

# Fake background samples
mc2017_samples["2017_DYM10to50"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Aug17_2017_DY10to50_UL/230817_235733/0000/"], "mc", "DYM10to50", "2017", "", "15810", "41.48", "68480179", 77]
mc2017_samples["2017_DYM50"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Aug17_2017_DY50_UL/230817_234813/0000/"], "mc", "DYM50", "2017", "", "6077.22", "41.48", "131552424", 14]
mc2017_samples["2017_TTTo2L2Nu"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2017_TTTo2L2Nu_UL/230817_235443/0000/"], "mc", "TTTo2L2Nu", "2017", "", "88.4", "41.48", "105859990", 4]
mc2017_samples["2017_TTToSemiLeptonic"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2017_TTToSemiLeptonic_UL/230817_234910/0000/"], "mc", "TTToSemiLeptonic", "2017", "", "365.34", "41.48", "341194592", 8]
mc2017_samples["2017_WWTo2L2Nu"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Aug17_2017_WWTo2L2Nu_UL/230817_235006/0000/"], "mc", "WWTo2L2Nu", "2017", "", "12.178", "41.48", "7071358", 12]
mc2017_samples["2017_ZZTo2L2Nu"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Aug17_2017_ZZTo2L2Nu_UL/230817_235157/0000/"], "mc", "ZZTo2L2Nu", "2017", "", "0.564", "41.48", "40753260", 6]

mc2017_samples["2017_DYGamma"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2017_DYGamma/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_PhotonConv_2017_DYGamma/240826_005159/0000/"], "mc", "DYGamma", "2017",  "", "55.48", "41.48", "18731142",  23]
mc2017_samples["2017_TTGammaDiL"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2017_TTGammaDiL/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/crab_Trilep_PhotonConv_2017_TTGammaDiL/240826_005056/0000/"], "mc", "TTGammaDiL", "2017",  "", "2.22", "41.48", "10018000",  13]
mc2017_samples["2017_TTGammaSingleL"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2017_TTGammaSingleL/TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/crab_Trilep_PhotonConv_2017_TTGammaSingleL/240826_005405/0000/"], "mc", "TTGammaSingleL", "2017",  "", "7.509", "41.48", "18906000",  20]
mc2017_samples["2017_TTGammaHad"] = [["/eos/cms/store/user/jingyan/LFV_Trilep_PhotonConv/2017_TTGammaHad/TTGamma_Hadronic_TuneCP5_13TeV-madgraph-pythia8/crab_Trilep_PhotonConv_2017_TTGammaHad/240826_005302/0000/"], "mc", "TTGammaHad", "2017",  "", "6.162", "41.48", "10537000",  20]

# Data
data2017_samples["2017_B_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_B_MuonEG/MuonEG/crab_Aug17_2_2017Data_2017_B_MuonEG/230818_013641/0000/"], "data", "MuonEG", "2017", "B", "1", "1", "1", 6]
data2017_samples["2017_C_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_C_MuonEG/MuonEG/crab_Aug17_2_2017Data_2017_C_MuonEG/230818_014012/0000/"], "data", "MuonEG", "2017", "C", "1", "1", "1", 17]
data2017_samples["2017_D_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_D_MuonEG/MuonEG/crab_Aug17_2_2017Data_2017_D_MuonEG/230818_015510/0000/"], "data", "MuonEG", "2017", "D", "1", "1", "1", 13]
data2017_samples["2017_E_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_E_MuonEG/MuonEG/crab_Aug17_2_2017Data_2017_E_MuonEG/230818_014529/0000/"], "data", "MuonEG", "2017", "E", "1", "1", "1", 8]
data2017_samples["2017_F_MuonEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_F_MuonEG/MuonEG/crab_Aug17_2_2017Data_2017_F_MuonEG/230818_014715/0000/"], "data", "MuonEG", "2017", "F", "1", "1", "1", 8]

data2017_samples["2017_B_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_B_DoubleEG/DoubleEG/crab_Aug17_2_2017Data_2017_B_DoubleEG/230818_013734/0000/"], "data", "DoubleEG", "2017", "B", "1", "1", "1", 8]
data2017_samples["2017_C_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_C_DoubleEG/DoubleEG/crab_Aug17_2_2017Data_2017_C_DoubleEG/230818_014901/0000/"], "data", "DoubleEG", "2017", "C", "1", "1", "1", 9]
data2017_samples["2017_D_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_D_DoubleEG/DoubleEG/crab_Aug17_2_2017Data_2017_D_DoubleEG/230818_015047/0000/"], "data", "DoubleEG", "2017", "D", "1", "1", "1", 7]
data2017_samples["2017_E_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_E_DoubleEG/DoubleEG/crab_Aug17_2_2017Data_2017_E_DoubleEG/230818_014436/0000/"], "data", "DoubleEG", "2017", "E", "1", "1", "1", 8]
data2017_samples["2017_F_DoubleEG"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_F_DoubleEG/DoubleEG/crab_Aug17_2_2017Data_2017_F_DoubleEG/230818_014250/0000/"], "data", "DoubleEG", "2017", "F", "1", "1", "1", 10]

data2017_samples["2017_B_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_B_DoubleMuon/DoubleMuon/crab_Aug17_2_2017Data_2017_B_DoubleMuon/230818_015232/0000/"], "data", "DoubleMuon", "2017", "B", "1", "1", "1", 8]
data2017_samples["2017_C_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_C_DoubleMuon/DoubleMuon/crab_Aug17_2_2017Data_2017_C_DoubleMuon/230818_015325/0000/"], "data", "DoubleMuon", "2017", "C", "1", "1", "1", 15]
data2017_samples["2017_D_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_D_DoubleMuon/DoubleMuon/crab_Aug17_2_2017Data_2017_D_DoubleMuon/230818_013827/0000/"], "data", "DoubleMuon", "2017", "D", "1", "1", "1", 16]
data2017_samples["2017_E_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_E_DoubleMuon/DoubleMuon/crab_Aug17_2_2017Data_2017_E_DoubleMuon/230818_014622/0000/"], "data", "DoubleMuon", "2017", "E", "1", "1", "1", 17]
data2017_samples["2017_F_DoubleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_F_DoubleMuon/DoubleMuon/crab_Aug17_2_2017Data_2017_F_DoubleMuon/230818_013547/0000/"], "data", "DoubleMuon", "2017", "F", "1", "1", "1", 15]

data2017_samples["2017_B_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_B_SingleElectron/SingleElectron/crab_Aug17_2_2017Data_2017_B_SingleElectron/230818_013402/0000/"], "data", "SingleElectron", "2017", "B", "1", "1", "1", 16]
data2017_samples["2017_C_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_C_SingleElectron/SingleElectron/crab_Aug17_2_2017Data_2017_C_SingleElectron/230818_014954/0000/"], "data", "SingleElectron", "2017", "C", "1", "1", "1", 20]
data2017_samples["2017_D_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_D_SingleElectron/SingleElectron/crab_Aug17_2_2017Data_2017_D_SingleElectron/230818_015417/0000/"], "data", "SingleElectron", "2017", "D", "1", "1", "1", 18]
data2017_samples["2017_E_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_E_SingleElectron/SingleElectron/crab_Aug17_2_2017Data_2017_E_SingleElectron/230818_015139/0000/"], "data", "SingleElectron", "2017", "E", "1", "1", "1", 17]
data2017_samples["2017_F_SingleElectron"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_F_SingleElectron/SingleElectron/crab_Aug17_2_2017Data_2017_F_SingleElectron/230818_013455/0000/"], "data", "SingleElectron", "2017", "F", "1", "1", "1", 17]

data2017_samples["2017_B_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_B_SingleMuon/SingleMuon/crab_Aug17_2_2017Data_2017_B_SingleMuon/230818_014158/0000/"], "data", "SingleMuon", "2017", "B", "1", "1", "1", 13]
data2017_samples["2017_C_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_C_SingleMuon/SingleMuon/crab_Aug17_2_2017Data_2017_C_SingleMuon/230818_014343/0000/"], "data", "SingleMuon", "2017", "C", "1", "1", "1", 16]
data2017_samples["2017_D_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_D_SingleMuon/SingleMuon/crab_Aug17_2_2017Data_2017_D_SingleMuon/230818_013920/0000/"], "data", "SingleMuon", "2017", "D", "1", "1", "1", 20]
data2017_samples["2017_E_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_E_SingleMuon/SingleMuon/crab_Aug17_2_2017Data_2017_E_SingleMuon/230818_014808/0000/"], "data", "SingleMuon", "2017", "E", "1", "1", "1", 14]
data2017_samples["2017_F_SingleMuon"] = [["/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2017/2017_F_SingleMuon/SingleMuon/crab_Aug17_2_2017Data_2017_F_SingleMuon/230818_014105/0000/"], "data", "SingleMuon", "2017", "F", "1", "1", "1", 18]