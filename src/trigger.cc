#include "trigger.h"

trigger::trigger(TString year, TString data)
               :year_(year), data_(data), dataset_(0), ch_(-1),
                triggerPassEE_(false), triggerPassEMu_(false), triggerPassMuMu_(false),
                Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_(false),
                Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_(false),
                Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_(false),
                Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_(false),
                Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_(false),
                Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_(false),
                DoubleEle33_CaloIdL_MW_(false),
                DoubleEle33_CaloIdL_GsfTrkIdVL_(false),
                Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_(false),
                Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_(false),
                Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_(false),
                Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_(false),
                Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_(false),
                Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_(false),
                Ele27_WPTight_Gsf_(false),
                Ele32_WPTight_Gsf_(false),
                Ele35_WPTight_Gsf_(false),
                IsoMu24_(false),
                IsoTkMu24_(false),
                IsoMu27_(false){}

void trigger::Init(Bool_t Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL,
                   Bool_t Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,
                   Bool_t Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,
                   Bool_t Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,
                   Bool_t Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,
                   Bool_t Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,
                   Bool_t DoubleEle33_CaloIdL_MW,
                   Bool_t DoubleEle33_CaloIdL_GsfTrkIdVL,
                   Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL,
                   Bool_t Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,
                   Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,
                   Bool_t Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,
                   Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8,
                   Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8,
                   Bool_t Ele27_WPTight_Gsf,
                   Bool_t Ele32_WPTight_Gsf,
                   Bool_t Ele35_WPTight_Gsf,
                   Bool_t IsoMu24,
                   Bool_t IsoTkMu24,
                   Bool_t IsoMu27){
                   Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_ = Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL;
                   Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ = Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL;
                   Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ = Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ;
                   Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ = Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
                   Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ = Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
                   Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ = Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
                   DoubleEle33_CaloIdL_MW_ = DoubleEle33_CaloIdL_MW;
                   DoubleEle33_CaloIdL_GsfTrkIdVL_ = DoubleEle33_CaloIdL_GsfTrkIdVL;
                   Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_ = Mu17_TrkIsoVVL_Mu8_TrkIsoVVL;
                   Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_ = Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
                   Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_ = Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
                   Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_ = Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
                   Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_ = Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8;
                   Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_ = Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8;
                   Ele27_WPTight_Gsf_ = Ele27_WPTight_Gsf;
                   Ele32_WPTight_Gsf_ = Ele32_WPTight_Gsf;
                   Ele35_WPTight_Gsf_ = Ele35_WPTight_Gsf;
                   IsoMu24_ = IsoMu24;
                   IsoTkMu24_ = IsoTkMu24;
                   IsoMu27_ = IsoMu27;               
}

Bool_t trigger::triggerLogic(TString dataset){
    dataset_ = dataset;
    triggerPassEE_ = false;
    triggerPassEMu_ = false;
    triggerPassMuMu_ = false;
    //MC
    if (data_ == "mc"){
        if (year_ == "2016APV"){
            if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_ || Ele27_WPTight_Gsf_) triggerPassEE_ = true;
            if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele27_WPTight_Gsf_ || IsoMu24_ || IsoTkMu24_) triggerPassEMu_ = true;
            if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_ || IsoMu24_ || IsoTkMu24_) triggerPassMuMu_ = true;
        }
        if (year_ == "2016"){
            if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_ || Ele27_WPTight_Gsf_) triggerPassEE_ = true;
            if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || Ele27_WPTight_Gsf_ || IsoMu24_ || IsoTkMu24_) triggerPassEMu_ = true;
            if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_ || IsoMu24_ || IsoTkMu24_) triggerPassMuMu_ = true;
        }
        if (year_ == "2017"){
            if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_ || Ele35_WPTight_Gsf_) triggerPassEE_ = true;
            if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele35_WPTight_Gsf_ || IsoMu27_) triggerPassEMu_ = true;
            if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_ || IsoMu27_) triggerPassMuMu_ =true;
        }
        if (year_ == "2018"){
            if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_ || Ele32_WPTight_Gsf_) triggerPassEE_ = true;
            if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele32_WPTight_Gsf_ || IsoMu24_) triggerPassEMu_ = true;
            if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_ || IsoMu24_) triggerPassMuMu_ = true;
        } 
    }else{
        if (year_ == "2016APV"){
            if (dataset_=="MuonEG"){
                if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleElectron"){
                if (!(Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_) && Ele27_WPTight_Gsf_) triggerPassEE_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_) && Ele27_WPTight_Gsf_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleMuon"){
                if (!(Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_) && (IsoMu24_ || IsoTkMu24_)) triggerPassMuMu_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele27_WPTight_Gsf_) && (IsoMu24_ || IsoTkMu24_)) triggerPassEMu_ = true; 
            }
            if (dataset_=="DoubleEG"){
                if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_) triggerPassEE_ = true;
            }
            if (dataset_=="DoubleMuon"){
                if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_) triggerPassMuMu_ = true;
            }
        }
        if (year_ == "2016"){
            if (dataset_=="MuonEG"){
                if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleElectron"){
                if (!(Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_) && Ele27_WPTight_Gsf_) triggerPassEE_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_) && Ele27_WPTight_Gsf_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleMuon"){
                if (!(Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_) && (IsoMu24_ || IsoTkMu24_)) triggerPassMuMu_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || Ele27_WPTight_Gsf_) && (IsoMu24_ || IsoTkMu24_)) triggerPassEMu_ = true; 
            }
            if (dataset_=="DoubleEG"){
                if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_) triggerPassEE_ = true;
            }
            if (dataset_=="DoubleMuon"){
                if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_) triggerPassMuMu_ = true;
            }
        }
        if (year_ == "2017"){
            if (dataset_=="MuonEG"){
                if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleElectron"){
                if (!(Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_ ) && Ele35_WPTight_Gsf_) triggerPassEE_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_) && Ele35_WPTight_Gsf_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleMuon"){
                if (!(Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_) && IsoMu27_) triggerPassMuMu_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele35_WPTight_Gsf_) && IsoMu27_) triggerPassEMu_ = true; 
            }
            if (dataset_=="DoubleEG"){
                if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_) triggerPassEE_ = true;
            }
            if (dataset_=="DoubleMuon"){
                if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_) triggerPassMuMu_ = true;
            }
        }
        if (year_ == "2018"){
            if (dataset_=="MuonEG"){
                if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_) triggerPassEMu_ = true;
            }
            if (dataset_=="SingleMuon"){
                if (!(Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_) && IsoMu24_) triggerPassMuMu_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele32_WPTight_Gsf_) && IsoMu24_) triggerPassEMu_ = true; 
            }
            if (dataset_=="EGamma"){
                if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_ || Ele32_WPTight_Gsf_) triggerPassEE_ = true;
                if (!(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_) && Ele32_WPTight_Gsf_) triggerPassEMu_ = true;
            }
            if (dataset_=="DoubleMuon"){
                if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_) triggerPassMuMu_ = true;
            }
        }
    }
    return (triggerPassEE_||triggerPassEMu_||triggerPassMuMu_);
}

Bool_t trigger::triggerPass(int ch){
    ch_ = ch;
    if (ch_ == 0) return triggerPassEE_;
    if (ch_ == 1) return triggerPassEMu_;
    if (ch_ == 2) return triggerPassMuMu_;
    assert(0);
}

trigger::~trigger(){}