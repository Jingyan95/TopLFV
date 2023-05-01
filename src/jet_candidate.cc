#include "jet_candidate.h"

jet_candidate::jet_candidate(float pt_in, float eta_in, float phi_in, float E_in, float btag_in, float btagSF_in, TString year, int ind_in){
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  btag_ = isb(btag_in,year);
  p4_.SetPtEtaPhiE(pt_, eta_, phi_, E_in) ;
  flavor_ = ind_in;
  bt_=btag_in;
  btSF_=btagSF_in;
  isbajet = 0;
}


int jet_candidate::isb(float btag_in , TString year){
  int R = 0;
  //DeepJet UL medium WP https://btv-wiki.docs.cern.ch/ScaleFactors/#useful-tools
  // if (year == "2016APV" && btag_in > 0.2598) R=1;
  // if (year == "2016" && btag_in > 0.2489) R=1;
  // if (year == "2017" && btag_in > 0.3040) R=1;
  // if (year == "2018" && btag_in > 0.2783) R=1;
  //DeepJet UL loose WP
  if (year == "2016APV" && btag_in > 0.0508) R=1;
  if (year == "2016" && btag_in > 0.0480) R=1;
  if (year == "2017" && btag_in > 0.0532) R=1;
  if (year == "2018" && btag_in > 0.0490) R=1;
  return R;
}
  
jet_candidate::~jet_candidate(){}