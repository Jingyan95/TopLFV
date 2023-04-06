#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,
                                 std::vector<jet_candidate*>* Jets,
                                 bool verbose)
                                    : verbose_(verbose),
                                      Leptons_(Leptons),
                                      Jets_(Jets),
                                      c_(abs((*Leptons_)[0]->charge_+(*Leptons_)[1]->charge_)/2),
                                      ch_((*Leptons_)[0]->flavor_+(*Leptons_)[1]->flavor_-2),
                                      eleMVA_(0),
                                      muMVA_(0),
                                      tauMVA_(0),
                                      llM_(((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_,(*Leptons_)[0]->phi_,(*Leptons_)[1]->eta_,(*Leptons_)[1]->phi_)),
                                      lep1_((*Leptons_)[0]->p4_),
                                      lep2_((*Leptons_)[1]->p4_){
    if (ch_==0){
        eleMVA_ = (*Leptons_)[0]->mva1_;
    }else if (ch_==1){
        eleMVA_ = (*Leptons_)[0]->mva1_;
        muMVA_ = (*Leptons_)[1]->mva1_;
    }else{
        muMVA_ = (*Leptons_)[0]->mva1_;
    }
    tauMVA_ = (*Leptons_)[2]->mva1_;
}
  
event_candidate::~event_candidate(){}




