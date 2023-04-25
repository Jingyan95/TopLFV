#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,
                                 std::vector<jet_candidate*>* Jets,
                                 float MET_pt,
                                 float MET_phi,
                                 bool verbose)
                                    : verbose_(verbose),
                                      Leptons_(Leptons),
                                      Jets_(Jets),
                                      MET_(new TLorentzVector(MET_pt*cos(MET_phi),MET_pt*sin(MET_phi),0,MET_pt)),
                                      c_(abs((*Leptons_)[0]->charge_+(*Leptons_)[1]->charge_)/2),
                                      ch_((*Leptons_)[0]->flavor_+(*Leptons_)[1]->flavor_-2),
                                      njet_(Jets->size()),
                                      nbjet_(0),
                                      llM_(((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_,(*Leptons_)[0]->phi_,(*Leptons_)[1]->eta_,(*Leptons_)[1]->phi_)),
                                      OnZ_(false){
    if (c_==0 && ch_!=1 && abs(llM_-mZ_)<15) OnZ_ = true;
    if (c_==1 && ch_==0 && abs(llM_-mZ_)<15) OnZ_ = true;
    sort(Jets->begin(), Jets->end(), ComparePtJet);
    for (int l=0;l<(int)Jets->size();l++){
        if((*Jets)[l]->btag_) nbjet_++;
    }
}
  
event_candidate::~event_candidate(){delete MET_;}