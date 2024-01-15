#include "trigger.h"

trigger::trigger(TString year, TString data) :
                year_(year), data_(data), dataset_(0), ch_(-1),
                triggerPassE_(false), triggerPassMu_(false),
                Ele27_WPTight_Gsf_(false),
                Ele32_WPTight_Gsf_(false),
                Ele35_WPTight_Gsf_(false),
                IsoMu24_(false),
                IsoTkMu24_(false),
                IsoMu27_(false) {}

void trigger::Init(
                Bool_t Ele27_WPTight_Gsf,
                Bool_t Ele32_WPTight_Gsf,
                Bool_t Ele35_WPTight_Gsf,
                Bool_t IsoMu24,
                Bool_t IsoTkMu24,
                Bool_t IsoMu27) {
  Ele27_WPTight_Gsf_ = Ele27_WPTight_Gsf;
  Ele32_WPTight_Gsf_ = Ele32_WPTight_Gsf;
  Ele35_WPTight_Gsf_ = Ele35_WPTight_Gsf;
  IsoMu24_ = IsoMu24;
  IsoTkMu24_ = IsoTkMu24;
  IsoMu27_ = IsoMu27;
}

Bool_t trigger::triggerLogic(TString dataset) {
  dataset_ = dataset;
  triggerPassE_ = false;
  triggerPassMu_ = false;

  // MC
  if (data_ == "mc") {
    if (year_ == "2016APV") {
      if (Ele27_WPTight_Gsf_) triggerPassE_ = true;
      if (IsoMu24_ || IsoTkMu24_) triggerPassMu_ = true;
    }
    if (year_ == "2016") {
      if (Ele27_WPTight_Gsf_) triggerPassE_ = true;
      if (IsoMu24_ || IsoTkMu24_) triggerPassMu_ = true;
    }
    if (year_ == "2017") {
      if (Ele35_WPTight_Gsf_) triggerPassE_ = true;
      if (IsoMu27_) triggerPassMu_ = true;
    }
    if (year_ == "2018") {
      if (Ele32_WPTight_Gsf_) triggerPassE_ = true;
      if (IsoMu24_) triggerPassMu_ = true;
    }
  }
  // Data
  else {
    if (year_ == "2016APV") {
      // if (dataset_ == "MuonEG") {}
      if (dataset_ == "SingleElectron") {
        if (Ele27_WPTight_Gsf_) triggerPassE_ = true;
      }
      if (dataset_ == "SingleMuon") {
        if (IsoMu24_ || IsoTkMu24_) triggerPassMu_ = true;
      }
      // if (dataset_ == "DoubleEG") {}
      // if (dataset_ == "DoubleMuon") {}
    }
    if (year_ == "2016") {
      // if (dataset_ == "MuonEG") {}
      if (dataset_ == "SingleElectron") {
        if (Ele27_WPTight_Gsf_) triggerPassE_ = true;
      }
      if (dataset_ == "SingleMuon") {
        if (IsoMu24_ || IsoTkMu24_) triggerPassMu_ = true;
      }
      // if (dataset_ == "DoubleEG") {}
      // if (dataset_ == "DoubleMuon") {}
    }
    if (year_ == "2017"){
      // if (dataset_ == "MuonEG"){}
      if (dataset_ == "SingleElectron") {
        if (Ele35_WPTight_Gsf_) triggerPassE_ = true;
      }
      if (dataset_ == "SingleMuon") {
        if (IsoMu27_) triggerPassMu_ = true;
      }
      // if (dataset_ == "DoubleEG") {}
      // if (dataset_ == "DoubleMuon") {}
    }
    if (year_ == "2018"){
      // if (dataset_ == "MuonEG") {}
      if (dataset_ == "SingleMuon") {
        if (IsoMu24_) triggerPassMu_ = true;
      }
      if (dataset_ == "EGamma") {
        if (Ele32_WPTight_Gsf_) triggerPassE_ = true;
      }
      // if (dataset_ == "DoubleMuon") {}
    }
  }
  return (triggerPassE_ || triggerPassMu_);
}

Bool_t trigger::triggerPass(int ch) {
  ch_ = ch;
  if (ch_ == 0) return triggerPassE_;
  if (ch_ == 1) return triggerPassMu_;
  assert(0);
}

trigger::~trigger() {}
