import sys
import os
import subprocess
import readline
import string

data2016_samples = {}
mc2016_samples = {}
##mc2016_samples ['2016_LFVStVecU'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw','# of files per job']
##cut = "((Sum$(Electron_pt>18 && abs(Electron_eta)<2.5 && Electron_sip3d<15) + Sum$(Muon_pt>18 && abs(Muon_eta)<2.4 && Muon_sip3d<15 && Muon_mediumId))>=2)"
##cut += " && ((Sum$(Tau_pt>18 && abs(Tau_eta)<2.3 && Tau_idDeepTau2017v2p1VSe>=1 && Tau_idDeepTau2017v2p1VSmu>=1 && Tau_idDeepTau2017v2p1VSjet>=1 && Tau_decayMode!=5 && Tau_decayMode!=6))>=1)"

##Scalar interaction
mc2016_samples['2016_LFVStScalarU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_LFVStScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2016_LFVStScalarU_UL/230911_230400/0000/'], 'mc','LFVStScalarU','2016', '','0.097','16.81','233000',233]
mc2016_samples['2016_LFVTtScalarU'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_LFVTtScalarU_UL/CRAB_UserFiles/crab_Sep11_2_Signal_2016_LFVTtScalarU_UL/230911_230454/0000/'], 'mc','LFVTtScalarU','2016', '','0.004','16.81','237000',237]

##Real background samples
mc2016_samples['2016_TTW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/'], 'mc','TTW','2016', '','0.235' ,'16.81','1800823',6]
mc2016_samples['2016_TTH'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTH_UL/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTH_UL/230501_145738/0000/'], 'mc','TTH','2016', '','0.211' ,'16.81','1622956',8]
mc2016_samples['2016_TTZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTZ_UL/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTZ_UL/230501_145932/0000/'], 'mc','TTZ','2016', '','0.281' ,'16.81','2962856',14]
mc2016_samples['2016_WZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_WZ_UL/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_WZ_UL/230501_145353/0000/'], 'mc','WZ','2016', '','4.9173' ,'16.81','6890010',16]
mc2016_samples['2016_ZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_ZZ_UL/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_ZZ_UL/230501_150529/0000/'], 'mc','ZZ','2016', '','1.256' ,'16.81','51577084',11]
mc2016_samples['2016_WWW'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_WWW_UL/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_WWW_UL/230501_150722/0000/'], 'mc','WWW','2016', '','0.2086' ,'16.81','62442',14]
mc2016_samples['2016_WWZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_WWZ_UL/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_WWZ_UL/230501_145057/0000/'], 'mc','WWZ','2016', '','0.1651' ,'16.81','61060',8]
mc2016_samples['2016_WZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_WZZ_UL/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_WZZ_UL/230501_145835/0000/'], 'mc','WZZ','2016', '','0.05565' ,'16.81','124388',18]
mc2016_samples['2016_ZZZ'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_ZZZ_UL/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_ZZZ_UL/230501_145451/0000/'], 'mc','ZZZ','2016', '','0.01476' ,'16.81','64358',4]

#Fake background samples
mc2016_samples['2016_TTTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTTo2L2Nu_UL/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTTo2L2Nu_UL/230501_150625/0000/'], 'mc','TTTo2L2Nu','2016', '','88.4' ,'16.81','43193956',5]
mc2016_samples['2016_TTToSemiLeptonic'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTToSemiLeptonic_UL/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTToSemiLeptonic_UL/230501_150229/0000/'], 'mc','TTToSemiLeptonic','2016', '','365.34' ,'16.81','143553998',6]
mc2016_samples['2016_DYM50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_DY50_UL/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_DY50_UL/230501_150132/0000/'], 'mc','DYM50','2016', '','6077.22' ,'16.81','48335328',11]
mc2016_samples['2016_DYM10to50'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_DY10to50_UL/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_DY10to50_UL/230501_145201/0000/'], 'mc','DYM10to50','2016', '','15810' ,'16.81','22388550',34]
mc2016_samples['2016_WWTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_WWTo2L2Nu_UL/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_WWTo2L2Nu_UL/230501_150034/0000/'], 'mc','WWTo2L2Nu','2016', '','12.178' ,'16.81','2888924',7]
mc2016_samples['2016_ZZTo2L2Nu'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_ZZTo2L2Nu_UL/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_ZZTo2L2Nu_UL/230501_145643/0000/'], 'mc','ZZTo2L2Nu','2016', '','0.564' ,'16.81','15894442',15]

#Data
data2016_samples['2016_F_MuonEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_F_MuonEG/MuonEG/crab_Trilep_Inclusive_Apr29_JEC_2016_F_MuonEG/230429_193335/0000/'], 'data','MuonEG','2016', 'F','1','1','1',3]
data2016_samples['2016_G_MuonEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_G_MuonEG/MuonEG/crab_Trilep_Inclusive_Apr29_JEC_2016_G_MuonEG/230429_191330/0000/'], 'data','MuonEG','2016', 'G','1','1','1',15]
data2016_samples['2016_H_MuonEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_H_MuonEG/MuonEG/crab_Trilep_Inclusive_Apr29_JEC_2016_H_MuonEG/230429_193004/0000/'], 'data','MuonEG','2016', 'H','1','1','1',10]

data2016_samples['2016_F_DoubleEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_F_DoubleEG/DoubleEG/crab_Trilep_Inclusive_Apr29_JEC_2016_F_DoubleEG/230429_191222/0000/'], 'data','DoubleEG','2016', 'F','1','1','1',5]
data2016_samples['2016_G_DoubleEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_G_DoubleEG/DoubleEG/crab_Trilep_Inclusive_Apr29_JEC_2016_G_DoubleEG/230429_191704/0000/'], 'data','DoubleEG','2016', 'G','1','1','1',8]
data2016_samples['2016_H_DoubleEG'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_H_DoubleEG/DoubleEG/crab_Trilep_Inclusive_Apr29_JEC_2016_H_DoubleEG/230429_192259/0000/'], 'data','DoubleEG','2016', 'H','1','1','1',11]

data2016_samples['2016_F_DoubleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_F_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_F_DoubleMuon/230429_193444/0000/'], 'data','DoubleMuon','2016', 'F','1','1','1',1]
data2016_samples['2016_G_DoubleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_G_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_G_DoubleMuon/230429_192148/0000/'], 'data','DoubleMuon','2016', 'G','1','1','1',29]
data2016_samples['2016_H_DoubleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_H_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_H_DoubleMuon/230429_194355/0000/'], 'data','DoubleMuon','2016', 'H','1','1','1',28]

data2016_samples['2016_F_SingleElectron'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_F_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_F_SingleElectron/230429_190749/0000/'], 'data','SingleElectron','2016', 'F','1','1','1',5]
data2016_samples['2016_G_SingleElectron'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_G_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_G_SingleElectron/230429_193923/0000/'], 'data','SingleElectron','2016', 'G','1','1','1',18]
data2016_samples['2016_H_SingleElectron'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_H_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_H_SingleElectron/230429_193225/0000/'], 'data','SingleElectron','2016', 'H','1','1','1',20]

data2016_samples['2016_F_SingleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_F_SingleMuon/SingleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_F_SingleMuon/230429_191005/0000/'], 'data','SingleMuon','2016', 'F','1','1','1',5]
data2016_samples['2016_G_SingleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_G_SingleMuon/SingleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_G_SingleMuon/230429_191441/0000/'], 'data','SingleMuon','2016', 'G','1','1','1',24]
data2016_samples['2016_H_SingleMuon'] = [['/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_H_SingleMuon/SingleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_H_SingleMuon/230429_194502/0000/'], 'data','SingleMuon','2016', 'H','1','1','1',28]
