import sys
import os
import subprocess
import readline
import string

data2018_samples = {}
mc2018_samples = {}
# mc2018_samples["2018_LFVStVecU"] = ["address", "data/mc", "dataset", "year", "run", "cross section", "lumi", "Neventsraw", "# of files per job"]

# cut = "((Sum$(Electron_pt>20 && abs(Electron_eta)<2.4 && Electron_sip3d<8 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1 && Electron_miniPFRelIso_all<0.4 && Electron_lostHits<2 && Electron_convVeto && Electron_tightCharge>0)"
# cut += " + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_mediumId && Muon_sip3d<8 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1 && Muon_miniPFRelIso_all<0.4))>=1)"
# cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=2 && Tau_idDeepTau2017v2p1VSmu>=8 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

# Real background samples
mc2018_samples["2018_TTH"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_2018LFVSignalAndData_v1_2018_TTH_UL/231103_211648/0000/"], "mc", "TTH", "2018", "", "0.211", "59.83", "3235099", 17]
mc2018_samples["2018_TTW"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2018LFVSignalAndData_v1_2018_TTW_UL/231103_214322/0000/"], "mc", "TTW", "2018", "", "0.235", "59.83", "5666428", 4]
mc2018_samples["2018_TTZ"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_2018LFVSignalAndData_v1_2018_TTZ_UL/231103_211550/0000/"], "mc", "TTZ", "2018", "", "0.281", "59.83", "9651834", 4]
mc2018_samples["2018_WZ"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2018LFVSignalAndData_v2_2018_WZ_UL/231104_231332/0000/"], "mc", "WZ", "2018", "", "4.9173", "59.83", "6482815", 18]
mc2018_samples["2018_ZZ"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_2018LFVSignalAndData_v2_2018_ZZ_UL/231104_232248/0000/"], "mc", "ZZ", "2018", "", "1.256", "59.83", "56239302", 16]
mc2018_samples["2018_WWW"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_2018LFVSignalAndData_v1_2018_WWW_UL/231103_211454/0000/"], "mc", "WWW", "2018", "", "0.2086", "59.83", "216852", 5]
mc2018_samples["2018_WWZ"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_2018LFVSignalAndData_v1_2018_WWZ_UL/231103_212847/0000/"], "mc", "WWZ", "2018", "", "0.1651", "59.83", "224734", 5]
mc2018_samples["2018_WZZ"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_2018LFVSignalAndData_v1_2018_WZZ_UL/231103_213842/0000/"], "mc", "WZZ", "2018", "", "0.05565", "59.83", "271866", 15]
mc2018_samples["2018_ZZZ"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_2018LFVSignalAndData_v2_2018_ZZZ_UL/231104_232014/0000/"], "mc", "ZZZ", "2018", "", "0.01476", "59.83", "222716", 14]
mc2018_samples["2018_TTTo2L2Nu"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_2018LFVSignalAndData_v1_2018_TTTo2L2Nu_UL/231103_213656/0000/"], "mc", "TTTo2L2Nu", "2018", "", "88.4", "59.83", "143848848", 4]
mc2018_samples["2018_WWTo2L2Nu"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_2018LFVSignalAndData_v1_2018_WWTo2L2Nu_UL/231103_214131/0000/"], "mc", "WWTo2L2Nu", "2018", "", "12.178", "59.83", "9956710", 37]

# Fake background samples
mc2018_samples["2018_DYM10to50"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2018LFVSignalAndData_v1_2018_DY10to50_UL/231103_212422/0000/"], "mc", "DYM10to50", "2018", "", "15810", "59.83", "94452816", 84]
mc2018_samples["2018_DYM50"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2018LFVSignalAndData_v2_2018_DY50_UL/231104_231242/0000/"], "mc", "DYM50", "2018", "", "6077.22", "59.83", "131572454", 19]
mc2018_samples["2018_TTToSemiLeptonic"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_2018LFVSignalAndData_v2_2018_TTToSemiLeptonic_UL/231104_231655/0000/"], "mc", "TTToSemiLeptonic", "2018", "", "365.34", "59.83", "472557630", 8]
mc2018_samples["2018_ZZTo2L2Nu"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_2018LFVSignalAndData_v2_2018_ZZTo2L2Nu_UL/231104_231602/0000/"], "mc", "ZZTo2L2Nu", "2018", "", "0.564", "59.83", "97491908", 22]
mc2018_samples["2018_WJets_0J"] = [["/eos/cms/store/user/jingyan/LFV_Wjets/2018_WJets_0J_UL/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Wjets_2018_WJets_0J_UL/240710_205324/0000/"], "mc", "WJets_0J", "2018", "", "49397", "59.83", "138080546", 10]
mc2018_samples["2018_WJets_1J"] = [["/eos/cms/store/user/jingyan/LFV_Wjets/2018_WJets_1J_UL/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Wjets_2018_WJets_1J_UL/240710_205415/0000/"], "mc", "WJets_1J", "2018", "", "8087", "59.83", "89044378", 10]
mc2018_samples["2018_WJets_2J"] = [["/eos/cms/store/user/jingyan/LFV_Wjets/2018_WJets_2J_UL/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Wjets_2018_WJets_2J_UL/240710_205505/0000/"], "mc", "WJets_2J", "2018", "", "3176", "59.83", "29631923", 10]

# Data
data2018_samples["2018_A_MuonEG"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_A_MuonEG/MuonEG/crab_2018LFVSignalAndData_v1_2018_A_MuonEG/231103_211754/0000/"], "data", "MuonEG", "2018", "A", "1", "1", "1", 11]
data2018_samples["2018_B_MuonEG"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_B_MuonEG/MuonEG/crab_2018LFVSignalAndData_v1_2018_B_MuonEG/231103_213749/0000/"], "data", "MuonEG", "2018", "B", "1", "1", "1", 6]
data2018_samples["2018_C_MuonEG"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_C_MuonEG/MuonEG/crab_2018LFVSignalAndData_v2_2018_C_MuonEG/231104_231924/0000/"], "data", "MuonEG", "2018", "C", "1", "1", "1", 7]
data2018_samples["2018_D_MuonEG"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_D_MuonEG/MuonEG/crab_2018LFVSignalAndData_v2_2018_D_MuonEG/231104_231422/0000/"], "data", "MuonEG", "2018", "D", "1", "1", "1", 10]

data2018_samples["2018_A_EGamma"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_A_EGamma/EGamma/crab_2018LFVSignalAndData_v2_2018_A_EGamma/231104_231152/0000/"], "data", "EGamma", "2018", "A", "1", "1", "1", 12]
data2018_samples["2018_B_EGamma"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_B_EGamma/EGamma/crab_2018LFVSignalAndData_v1_2018_B_EGamma/231103_212050/0000/"], "data", "EGamma", "2018", "B", "1", "1", "1", 9]
data2018_samples["2018_C_EGamma"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_C_EGamma/EGamma/crab_2018LFVSignalAndData_v2_2018_C_EGamma/231104_231834/0000/"], "data", "EGamma", "2018", "C", "1", "1", "1", 12]
data2018_samples["2018_D_EGamma"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_D_EGamma/EGamma/crab_2018LFVSignalAndData_v2_2018_D_EGamma/231104_231745/0000/"], "data", "EGamma", "2018", "D", "1", "1", "1", 12]

data2018_samples["2018_A_DoubleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_A_DoubleMuon/DoubleMuon/crab_2018LFVSignalAndData_v1_2018_A_DoubleMuon/231103_212942/0000/"], "data", "DoubleMuon", "2018", "A", "1", "1", "1", 25]
data2018_samples["2018_B_DoubleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_B_DoubleMuon/DoubleMuon/crab_2018LFVSignalAndData_v1_2018_B_DoubleMuon/231103_212610/0000/"], "data", "DoubleMuon", "2018", "B", "1", "1", "1", 18]
data2018_samples["2018_C_DoubleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_C_DoubleMuon/DoubleMuon/crab_2018LFVSignalAndData_v2_2018_C_DoubleMuon/231104_231512/0000/"], "data", "DoubleMuon", "2018", "C", "1", "1", "1", 31]
data2018_samples["2018_D_DoubleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_D_DoubleMuon/DoubleMuon/crab_2018LFVSignalAndData_v1_2018_D_DoubleMuon/231103_214034/0000/"], "data", "DoubleMuon", "2018", "D", "1", "1", "1", 22]

data2018_samples["2018_A_SingleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_A_SingleMuon/SingleMuon/crab_2018LFVSignalAndData_v2_2018_A_SingleMuon/231104_232158/0000/"], "data", "SingleMuon", "2018", "A", "1", "1", "1", 24]
data2018_samples["2018_B_SingleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_B_SingleMuon/SingleMuon/crab_2018LFVSignalAndData_v1_2018_B_SingleMuon/231103_213508/0000/"], "data", "SingleMuon", "2018", "B", "1", "1", "1", 26]
data2018_samples["2018_C_SingleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_C_SingleMuon/SingleMuon/crab_2018LFVSignalAndData_v1_2018_C_SingleMuon/231103_211851/0000/"], "data", "SingleMuon", "2018", "C", "1", "1", "1", 34]
data2018_samples["2018_D_SingleMuon"] = [["/eos/cms/store/user/etsai/LFV_Dilepton/2018/2018_D_SingleMuon/SingleMuon/crab_2018LFVSignalAndData_v2_2018_D_SingleMuon/231104_232104/0000/"], "data", "SingleMuon", "2018", "D", "1", "1", "1", 26]
