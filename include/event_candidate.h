#ifndef MY_event_candidate
#define MY_event_candidate

#include <cmath>
#include <string>
#include <iostream>
#include <vector>
#include <complex>
#include <algorithm>
#include <TLorentzVector.h>
#include "jet_candidate.h"
#include "lepton_candidate.h"

using namespace std;

class event_candidate {

public:

  event_candidate(std::vector<lepton_candidate*>* Leptons,
                  std::vector<jet_candidate*>* Jets,
                  float MET_pt,
                  float MET_phi,
                  bool verbose);
  ~event_candidate();

  int c() { return c_; }
  int ch() { return ch_; }
  int njet() { return njet_; }
  int nbjet() { return nbjet_; }
  float btagSF() { return btagSF_; }
  float btagSum() { return btagSum_; }
  float Ht() { return Ht_; }
  float St() { return St_; }
  float llM() { return llM_; }
  float llDr() { return llDr_; }
  bool OnZ() { return OnZ_; }
  bool TightTau() { return TightTa_; }
  TLorentzVector* MET() { return MET_; }

  static bool ComparePtJet(jet_candidate *a, jet_candidate *b) { return a->pt_ > b->pt_; }
  static bool CompareBtagJet(jet_candidate *a, jet_candidate *b) { return a->bt_ > b->bt_; }

  lepton_candidate* lep1() { return (*Leptons_)[0]; }
  jet_candidate* jet1() { return njet_ > 0 ? (*Jets_)[0] : nullptr; } // Leading jet in pT
  lepton_candidate* el1() { return ch_ == 0 ? (*Leptons_)[0] : nullptr; }
  lepton_candidate* mu1() { return ch_ == 1 ? (*Leptons_)[0] : nullptr; }
  lepton_candidate* ta1() { return (*Leptons_)[1]; }

  static Double_t deltaPhi(Double_t phi1, Double_t phi2) {
    Double_t dPhi = phi1 - phi2;
    if (dPhi > TMath::Pi()) dPhi -= 2.0 * TMath::Pi();
    if (dPhi < -TMath::Pi()) dPhi += 2.0 * TMath::Pi();
    return dPhi;
  }

  static Double_t deltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2) {
    Double_t dEta, dPhi ;
    dEta = eta1 - eta2;
    dPhi = deltaPhi(phi1, phi2);
    return sqrt(dEta * dEta + dPhi * dPhi);
  }

private:

  bool verbose_;
  std::vector<lepton_candidate*>* Leptons_;
  std::vector<jet_candidate*>* Jets_;
  TLorentzVector* MET_;
  jet_candidate* bjet_; // Jet with the highest b-tagging score
  int c_; // Charges: 0->Opposite-Sign, 1->Same-Sign
  int ch_; // Channel: 0->e+tau, 1->mu+ta
  int njet_;
  int nbjet_;
  float btagSF_;
  float btagSum_; // Sum of btagging score
  float Ht_;
  float St_;
  float llM_; // Mass of the two leptons
  float llDr_;
  bool OnZ_; // Events close to Z peak (incl. Same-Sign ee due to charge flip) (should be sensitive to leptonic tau?)
  bool TightTa_; // Events with tau passing Tight tau vs. jets WP

  float mZ_ = 91.2;
};

#endif
