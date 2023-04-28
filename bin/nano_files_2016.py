import sys
import os
import subprocess
import readline
import string

data2016_samples = {}
mc2016_samples = {}
##data2016_samples ['2016_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']
##cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<15) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<15 && Muon_mediumId))>=2)"
##cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=1 && Tau_idDeepTau2017v2p1VSmu>=1 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

##Scalar interaction
mc2016_samples['2016_LFVStScalarU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_LFVStScalarU_UL/CRAB_UserFiles/crab_Trilep_Inclusive_Apr21_2016_LFVStScalarU_UL/230421_214648/0000/'], 'mc','LFVStScalarU','2016', '','0.417' ,'16.81','100000',100]
mc2016_samples['2016_LFVTtScalarU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_LFVTtScalarU_UL/CRAB_UserFiles/crab_Trilep_Inclusive_Apr21_2016_LFVTtScalarU_UL/230421_214750/0000/'], 'mc','LFVTtScalarU','2016', '','0.012','16.81','100000',100]

##Fake background samples
mc2016_samples['2016_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTTo2L2Nu_UL/230419_121459/0000/'], 'mc','TTTo2L2Nu','2016', '','88.4' ,'16.81','43546000',7]
mc2016_samples['2016_TTToSemiLeptonic'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr27_2016_TTToSemiLeptonic_UL/230427_155453/0000/'], 'mc','TTToSemiLeptonic','2016', '','365.34' ,'16.81','144722000',20]
mc2016_samples['2016_TTToHadronic'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTToHadronic_UL/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_Apr27_2016_TTToHadronic_UL/230427_155250/0000/'], 'mc','TTToHadronic','2016', '','377.96' ,'16.81','107067000',73]
mc2016_samples['2016_DYM50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilepton_Inclusive_Apr19_2016_DY50_UL/230419_120428/0000/'], 'mc','DYM50','2016', '','6077.22' ,'16.81','71839442',14]
mc2016_samples['2016_DYM10to50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Trilep_Inclusive_Apr27_2016_DY10to50_UL/230427_155352/0000/'], 'mc','DYM50','2016', '','15810' ,'16.81','22388550',34]

##Real background samples
mc2016_samples['2016_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTW_UL/230419_121349/0000/'], 'mc','TTW','2016', '','0.235' ,'16.81','3322643',6]
mc2016_samples['2016_TTH'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTH_UL/230419_121721/0000/'], 'mc','TTH','2016', '','0.211' ,'16.81','4941250',8]
mc2016_samples['2016_TTZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTZ_UL/230419_121829/0000/'], 'mc','TTZ','2016', '','0.281' ,'16.81','6017000',14]
mc2016_samples['2016_WZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WZ_UL/230419_120800/0000/'], 'mc','WZ','2016', '','4.9173' ,'16.81','10441724',16]
mc2016_samples['2016_ZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Trilepton_Inclusive_Apr19_2016_ZZ/230419_122046/0000/'], 'mc','ZZ','2016', '','1.256' ,'16.81','52104000',11]
mc2016_samples['2016_WWW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WWW/230419_121238/0000/'], 'mc','WWW','2016', '','0.2086' ,'16.81','69000',14]
mc2016_samples['2016_WWZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WWZ/230419_121938/0000/'], 'mc','WWZ','2016', '','0.1651' ,'16.81','67000',8]
mc2016_samples['2016_WZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_WZZ/230419_120650/0000/'], 'mc','WZZ','2016', '','0.05565' ,'16.81','137000',18]
mc2016_samples['2016_ZZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilepton_Inclusive_Apr19_2016_ZZZ/230419_122859/0000/'], 'mc','ZZZ','2016', '','0.01476' ,'16.81','72000',4]

##Data
data2016_samples['2016_F_MuonEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_F_MuonEG/MuonEG/crab_Trilep_Inclusive_Apr24_2_2016_F_MuonEG/230424_160032/0000/'], 'data','MuonEG','2016', 'F','1','1','1',3]
data2016_samples['2016_G_MuonEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_G_MuonEG/MuonEG/crab_Trilep_Inclusive_Apr24_2_2016_G_MuonEG/230424_155424/0000/'], 'data','MuonEG','2016', 'G','1','1','1',29]
data2016_samples['2016_H_MuonEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_H_MuonEG/MuonEG/crab_Trilep_Inclusive_Apr24_2_2016_H_MuonEG/230424_160534/0000/'], 'data','MuonEG','2016', 'H','1','1','1',19]

data2016_samples['2016_F_DoubleEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_F_DoubleEG/DoubleEG/crab_Trilep_Inclusive_Apr24_2_2016_F_DoubleEG/230424_155312/0000/'], 'data','DoubleEG','2016', 'F','1','1','1',5]
data2016_samples['2016_G_DoubleEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_G_DoubleEG/DoubleEG/crab_Trilep_Inclusive_Apr24_2_2016_G_DoubleEG/230424_155651/0000/'], 'data','DoubleEG','2016', 'G','1','1','1',16]
data2016_samples['2016_H_DoubleEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_H_DoubleEG/DoubleEG/crab_Trilep_Inclusive_Apr24_2_2016_H_DoubleEG/230424_155805/0000/'], 'data','DoubleEG','2016', 'H','1','1','1',29]

data2016_samples['2016_F_DoubleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_F_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr24_2_2016_F_DoubleMuon/230424_160648/0000/'], 'data','DoubleMuon','2016', 'F','1','1','1',1]
data2016_samples['2016_G_DoubleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_G_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr24_2_2016_G_DoubleMuon/230424_165016/0000/'], 'data','DoubleMuon','2016', 'G','1','1','1',29]
data2016_samples['2016_H_DoubleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_H_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr24_2_2016_H_DoubleMuon/230424_160801/0000/'], 'data','DoubleMuon','2016', 'H','1','1','1',28]

data2016_samples['2016_F_SingleElectron'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_F_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr24_2_2016_F_SingleElectron/230424_155050/0000/'], 'data','SingleElectron','2016', 'F','1','1','1',5]
data2016_samples['2016_G_SingleElectron'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_G_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr24_2_2016_G_SingleElectron/230424_155919/0000/'], 'data','SingleElectron','2016', 'G','1','1','1',36]
data2016_samples['2016_H_SingleElectron'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_H_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr24_2_2016_H_SingleElectron/230424_155202/0000/'], 'data','SingleElectron','2016', 'H','1','1','1',40]

data2016_samples['2016_F_SingleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_F_SingleMuon/SingleMuon/crab_Trilep_Inclusive_Apr24_2_2016_F_SingleMuon/230424_155537/0000/'], 'data','SingleMuon','2016', 'F','1','1','1',5]
data2016_samples['2016_G_SingleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_G_SingleMuon/SingleMuon/crab_Trilep_Inclusive_Apr24_2_2016_G_SingleMuon/230424_160300/0000/'], 'data','SingleMuon','2016', 'G','1','1','1',70]
data2016_samples['2016_H_SingleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_H_SingleMuon/SingleMuon/crab_Trilep_Inclusive_Apr24_2_2016_H_SingleMuon/230424_160417/0000/'], 'data','SingleMuon','2016', 'H','1','1','1',82]
