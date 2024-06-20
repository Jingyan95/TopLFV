#ifndef MY_trigger
#define MY_trigger

#include <cmath>
#include <string>
#include <iostream>
#include <TROOT.h>

using namespace std;
// using namespace math;

class trigger {

public:

  trigger(TString, TString);
  void Init(Bool_t, Bool_t, Bool_t, Bool_t, Bool_t, Bool_t);
  ~trigger();
  Bool_t triggerLogic(TString);
  Bool_t triggerPass(int);

private:

  TString year_;
  TString data_;
  TString dataset_;
  int ch_;

  Bool_t triggerPassE_;
  Bool_t triggerPassMu_;

  // Bool_t triggerPassEE_;
  // Bool_t triggerPassEMu_;
  // Bool_t triggerPassMuMu_;

  // Bool_t Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_; // 2016 APV
  // Bool_t Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_; // 2016 APV, 2017, 2018
  // Bool_t Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_; // 2016, 2017, 2018
  // Bool_t Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_; // 2016

  // Bool_t Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_; // 2017, 2018
  // Bool_t Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_; // 2016 APV, 2016
  // Bool_t DoubleEle33_CaloIdL_MW_; // 2016APV, 2016, 2017, 2018
  // Bool_t DoubleEle33_CaloIdL_GsfTrkIdVL_; // 2016APV, 2016

  // Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_; // 2016 APV
  // Bool_t Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_; // 2016 APV
  // Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_; // 2016
  // Bool_t Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_; // 2016
  // Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_; // 2017
  // Bool_t Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_; // 2018

  Bool_t Ele27_WPTight_Gsf_; // 2016 APV, 2016
  Bool_t Ele32_WPTight_Gsf_; // 2018
  Bool_t Ele35_WPTight_Gsf_; // 2017
  Bool_t IsoMu24_; // 2016 APV, 2016, 2018
  Bool_t IsoTkMu24_; // 2016 APV, 2016
  Bool_t IsoMu27_; // 2017
};

#endif
