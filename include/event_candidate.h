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
                  float MET_pt,
                  float MET_phi,
                  bool verbose);
  ~event_candidate();

  int c(){return c_;}
  int ch(){return ch_;}
  int lfvch(){return lfvch_;}
  int njet(){return njet_;}
  int nbjet(){return nbjet_;}
  float Topmass(){return Topmass_;}
  float llM(){return llM_;}
  float llDr(){return llDr_;}
  float LFVllM(){return LFVllM_;}
  float LFVllDr(){return LFVllDr_;}
  bool OnZ(){return OnZ_;}
  TLorentzVector* MET(){return MET_;}
  static bool ComparePtJet(jet_candidate *a, jet_candidate *b) { return a->pt_ > b->pt_; }
  static bool CompareBtagJet(jet_candidate *a, jet_candidate *b) { return a->bt_ > b->bt_; }
  lepton_candidate* lep1(){return (*Leptons_)[0]->pt_>(*Leptons_)[1]->pt_?(*Leptons_)[0]:(*Leptons_)[1];}//Leading lepton in pT
  lepton_candidate* lep2(){return (*Leptons_)[0]->pt_>(*Leptons_)[1]->pt_?(*Leptons_)[1]:(*Leptons_)[0];}//Trailing lepton in pT
  jet_candidate* jet1(){return njet_>0?(*Jets_)[0]:nullptr;}//Leading jet in pT
  lepton_candidate* el1(){return ch_<2?(*Leptons_)[0]:nullptr;}
  lepton_candidate* mu1(){return ch_>1?(*Leptons_)[0]:ch_>0?(*Leptons_)[1]:nullptr;}
  lepton_candidate* ta1(){return (*Leptons_)[2];}
  lepton_candidate* LFVe(){return lfvch_!=2?LFVe_:nullptr;}
  lepton_candidate* LFVmu(){return lfvch_!=1?LFVmu_:nullptr;}
  lepton_candidate* LFVta(){return lfvch_!=0?LFVta_:nullptr;}
  lepton_candidate* Balep(){return Balep_;}
        
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

  TLorentzVector solveNeutrinoPz(lepton_candidate *a, TLorentzVector *MET){
      TLorentzVector n;
      TLorentzVector l=a->p4_;
      float pz;
      float plx=l.Px();
      float ply=l.Py();
      float plz=l.Pz();
      float El=l.E();
      float x=mW_*mW_-El*El+plx*plx+ply*ply+plz*plz+2*plx*MET->Px()+2*ply*MET->Py();
      float A=4*(El*El-plz*plz);
      float B=-4*x*plz;
      float C=4*El*El*MET->Pt()*MET->Pt()-x*x;
      float delta=B*B-4*A*C; //quadratic formula
      if(delta<0){
        pz=-B/(2*A); //take the real part of the complex solution
      }
      else{
        float sol1=(-B-sqrt(delta))/(2*A);
        float sol2=(-B+sqrt(delta))/(2*A);
        if(abs(sol1-plz)<abs(sol2-plz)){
          pz=sol1; //pick the one closest to lepton pz
        }
        else{
          pz=sol2;
        }
      }
      n.SetPxPyPzE(MET->Px(),MET->Py(),pz,sqrt(MET->Pt()*MET->Pt()+pz*pz));
      return n;
  }
      
private:
  
  bool verbose_;
  std::vector<lepton_candidate*>* Leptons_;
  std::vector<jet_candidate*>* Jets_;
  TLorentzVector* MET_;
  lepton_candidate* LFVe_;
  lepton_candidate* LFVmu_;
  lepton_candidate* LFVta_;
  lepton_candidate* Balep_;//SM lepton, a.k.a. bachelor lepton 
  jet_candidate* bjet_;//jet with the highest b-tagging score
  int c_;//Charges: 0->Opposite-Sign, 1->Same-Sign
  int ch_;//Channel: 0->ee+tau, 1->emu+ta, 2->mumu+ta
  int lfvch_;//LFV channel: 0->LFV-emu, 1->LFV-eta, 2->LFV-muta
  int njet_;
  int nbjet_;
  float Topmass_;//SM top mass
  float llM_;//Mass of the two leptons (e or mu)
  float llDr_;
  float LFVllM_;//Mass of the LFV lepton pair
  float LFVllDr_;
  bool OnZ_;
      
  float mT_ = 172.5;
  float mZ_ = 91.2;
  float mW_ = 80.2;
};

#endif