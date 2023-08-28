#include "trigger.h"

trigger::trigger(TString year, TString data)
              : year_(year), data_(data), ch_(-1),
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
                IsoMu27_(false),
                PFMET300_(false),
                MET200_(false),
                PFHT300_PFMET110_(false),
                PFMET170_HBHECleaned_(false),
                PFMET120_PFMHT120_IDTight_(false),
                PFMETNoMu120_PFMHTNoMu120_IDTight_(false),
                PFMET200_HBHECleaned_(false),
                PFMET200_HBHE_BeamHaloCleaned_(false),
                PFMETTypeOne200_HBHE_BeamHaloCleaned_(false),
                PFMET120_PFMHT120_IDTight_PFHT60_(false),
                PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_(false),
                PFHT500_PFMET100_PFMHT100_IDTight_(false),
                PFHT700_PFMET85_PFMHT85_IDTight_(false),
                PFHT800_PFMET75_PFMHT75_IDTight_(false){}

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
                   Bool_t IsoMu27,
                   Bool_t PFMET300,
                   Bool_t MET200,
                   Bool_t PFHT300_PFMET110,
                   Bool_t PFMET170_HBHECleaned,
                   Bool_t PFMET120_PFMHT120_IDTight,
                   Bool_t PFMETNoMu120_PFMHTNoMu120_IDTight,
                   Bool_t PFMET200_HBHECleaned,
                   Bool_t PFMET200_HBHE_BeamHaloCleaned,
                   Bool_t PFMETTypeOne200_HBHE_BeamHaloCleaned,
                   Bool_t PFMET120_PFMHT120_IDTight_PFHT60,
                   Bool_t PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60,
                   Bool_t PFHT500_PFMET100_PFMHT100_IDTight,
                   Bool_t PFHT700_PFMET85_PFMHT85_IDTight,
                   Bool_t PFHT800_PFMET75_PFMHT75_IDTight) {
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
  PFMET300_ = PFMET300;
  MET200_ = MET200;
  PFHT300_PFMET110_ = PFHT300_PFMET110;
  PFMET170_HBHECleaned_ = PFMET170_HBHECleaned;
  PFMET120_PFMHT120_IDTight_ = PFMET120_PFMHT120_IDTight;
  PFMETNoMu120_PFMHTNoMu120_IDTight_ = PFMETNoMu120_PFMHTNoMu120_IDTight;
  PFMET200_HBHECleaned_ = PFMET200_HBHECleaned;
  PFMET200_HBHE_BeamHaloCleaned_ = PFMET200_HBHE_BeamHaloCleaned;
  PFMETTypeOne200_HBHE_BeamHaloCleaned_ = PFMETTypeOne200_HBHE_BeamHaloCleaned;
  PFMET120_PFMHT120_IDTight_PFHT60_ = PFMET120_PFMHT120_IDTight_PFHT60;
  PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_ = PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60;
  PFHT500_PFMET100_PFMHT100_IDTight_ = PFHT500_PFMET100_PFMHT100_IDTight;
  PFHT700_PFMET85_PFMHT85_IDTight_ = PFHT700_PFMET85_PFMHT85_IDTight;
  PFHT800_PFMET75_PFMHT75_IDTight_ = PFHT800_PFMET75_PFMHT75_IDTight;
}

Bool_t trigger::triggerLogic() {
  triggerPassMET_ = false;
  triggerPassEE_ = false;
  triggerPassEMu_ = false;
  triggerPassMuMu_ = false;

  if (year_ == "2016APV") {
    if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_ || Ele27_WPTight_Gsf_) triggerPassEE_ = true;
    if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele27_WPTight_Gsf_ || IsoMu24_ || IsoTkMu24_) triggerPassEMu_ = true;
    if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_ || IsoMu24_ || IsoTkMu24_) triggerPassMuMu_ = true;
  }
  if (year_ == "2016") {
    if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || DoubleEle33_CaloIdL_MW_ || DoubleEle33_CaloIdL_GsfTrkIdVL_ || Ele27_WPTight_Gsf_) triggerPassEE_ = true;
    if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || Ele27_WPTight_Gsf_ || IsoMu24_ || IsoTkMu24_) triggerPassEMu_ = true;
    if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_ || Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_ || IsoMu24_ || IsoTkMu24_) triggerPassMuMu_ = true;
  }
  if (year_ == "2017") {
    if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_ || Ele35_WPTight_Gsf_) triggerPassEE_ = true;
    if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_ || Ele35_WPTight_Gsf_ || IsoMu27_) triggerPassEMu_ = true;
    if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_ || IsoMu27_) triggerPassMuMu_ = true;
  }
  if (year_ == "2018") {
    if (Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_ || DoubleEle33_CaloIdL_MW_ || Ele32_WPTight_Gsf_) triggerPassEE_ = true;
    if (Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_ || Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_ || Ele32_WPTight_Gsf_ || IsoMu24_) triggerPassEMu_ = true;
    if (Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_ || IsoMu24_) triggerPassMuMu_ = true;
  }

  // MC
  if (data_ == "mc") {
    triggerPassMET_ = true;
  } else {// Data
    if (year_ == "2016APV") {
      if (PFMET300_ || MET200_ || PFHT300_PFMET110_ || PFMET170_HBHECleaned_ || PFMET120_PFMHT120_IDTight_ || PFMETNoMu120_PFMHTNoMu120_IDTight_) triggerPassMET_ = true;
    }
    if (year_ == "2016") {
      if (PFMET300_ || MET200_ || PFHT300_PFMET110_ || PFMET170_HBHECleaned_ || PFMET120_PFMHT120_IDTight_ || PFMETNoMu120_PFMHTNoMu120_IDTight_) triggerPassMET_ = true;
    }
    if (year_ == "2017"){   
      if (PFMET200_HBHECleaned_ || PFMET200_HBHE_BeamHaloCleaned_ || PFMETTypeOne200_HBHE_BeamHaloCleaned_ || PFMET120_PFMHT120_IDTight_PFHT60_ || PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_ || PFHT500_PFMET100_PFMHT100_IDTight_ || PFHT700_PFMET85_PFMHT85_IDTight_ || PFHT800_PFMET75_PFMHT75_IDTight_) triggerPassMET_ = true;
    }
    if (year_ == "2018"){
      if (PFMET200_HBHECleaned_ || PFMET200_HBHE_BeamHaloCleaned_ || PFMETTypeOne200_HBHE_BeamHaloCleaned_ || PFMET120_PFMHT120_IDTight_PFHT60_ || PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_ || PFHT500_PFMET100_PFMHT100_IDTight_ || PFHT700_PFMET85_PFMHT85_IDTight_ || PFHT800_PFMET75_PFMHT75_IDTight_) triggerPassMET_ = true;
    }
  }
  return triggerPassMET_;
}

Bool_t trigger::triggerPass(int ch) {
  ch_ = ch;
  if (ch_ == 0) return triggerPassEE_;
  if (ch_ == 1 || ch_ == 2) return triggerPassEMu_;
  if (ch_ == 3) return triggerPassMuMu_;
  assert(0);
}

trigger::~trigger() {}
