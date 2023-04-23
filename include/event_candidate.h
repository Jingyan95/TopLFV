#ifndef MY_event_candidate
#define MY_event_candidate

#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <algorithm>
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
  int njet(){return njet_;}
  int nbjet(){return nbjet_;}
  float llM(){return llM_;}
  float llDr(){return llDr_;}
  bool OnZ(){return OnZ_;}
  static bool ComparePtJet(jet_candidate *a, jet_candidate *b) { return a->pt_ > b->pt_; }
  lepton_candidate* lep1(){return (*Leptons_)[0];}
  lepton_candidate* lep2(){return (*Leptons_)[1];}
  lepton_candidate* lep3(){return (*Leptons_)[2];}//Tau
  jet_candidate* jet1(){return njet_>0?(*Jets_)[0]:nullptr;}//Leading jet in pT
  lepton_candidate* el1(){return ch_<2?(*Leptons_)[0]:nullptr;}
  lepton_candidate* mu1(){return ch_>1?(*Leptons_)[0]:ch_>0?(*Leptons_)[1]:nullptr;}
  lepton_candidate* ta1(){return (*Leptons_)[2];}
        
  static Double_t deltaPhi(Double_t phi1, Double_t phi2) {
      Double_t dPhi = phi1 - phi2;
      if (dPhi > TMath::Pi()) dPhi -= 2.*TMath::Pi();
      if (dPhi < -TMath::Pi()) dPhi += 2.*TMath::Pi();
      return dPhi;
  }

  static Double_t deltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2) {
      Double_t dEta, dPhi ;
      dEta = eta1 - eta2;
      dPhi = deltaPhi(phi1, phi2);
      return sqrt(dEta*dEta+dPhi*dPhi);
  }
      
private:
  
  bool verbose_;
  std::vector<lepton_candidate*>* Leptons_;
  std::vector<jet_candidate*>* Jets_;
  int c_;//Charges
  int ch_;//Channel
  int njet_;
  int nbjet_;
  float llM_;
  float llDr_;
  bool OnZ_;
      
  float mT_ = 172.5;
  float mZ_ = 91.2;
  float mW_ = 80.2;
};

#endif