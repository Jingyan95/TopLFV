#ifndef MY_event_candidate
#define MY_event_candidate

#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <TLorentzVector.h>
#include "jet_candidate.h"
#include "lepton_candidate.h"

using namespace std;
//using namespace math;
class event_candidate {
  
public:
  event_candidate(std::vector<lepton_candidate*>* Leptons,
                  std::vector<jet_candidate*>* Jets,
                  bool verbose);
  ~event_candidate();
    
  int c(){return c_;}
  int ch(){return ch_;}
  float eleMVA(){return eleMVA_;}
  float muMVA(){return muMVA_;}
  float tauMVA(){return tauMVA_;}
  TLorentzVector LFVe(){return LFVe_;}
  TLorentzVector LFVmu(){return LFVmu_;}
  TLorentzVector LFVtau(){return LFVtau_;}
        
  Double_t deltaPhi(Double_t phi1, Double_t phi2) {
      Double_t dPhi = phi1 - phi2;
      if (dPhi > TMath::Pi()) dPhi -= 2.*TMath::Pi();
      if (dPhi < -TMath::Pi()) dPhi += 2.*TMath::Pi();
      return dPhi;
  }

  Double_t deltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2) {
      Double_t dEta, dPhi ;
      dEta = eta1 - eta2;
      dPhi = deltaPhi(phi1, phi2);
      return sqrt(dEta*dEta+dPhi*dPhi);
  }
      
private:
  
  int c_;//Charges
  int ch_;//Channel
  std::vector<lepton_candidate*>* Leptons_;
  std::vector<jet_candidate*>* Jets_;
  bool verbose_;
  float eleMVA_;
  float muMVA_;
  float tauMVA_;
  TLorentzVector LFVe_;
  TLorentzVector LFVmu_;
  TLorentzVector LFVtau_;
      
  float mT_ = 172.5;
  float mZ_ = 91.2;
  float mW_ = 80.2;
};

#endif

