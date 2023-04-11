#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,
                                 std::vector<jet_candidate*>* Jets,
                                 bool verbose)
                                    : verbose_(verbose),
                                      Leptons_(Leptons),
                                      Jets_(Jets),
                                      c_(abs((*Leptons_)[0]->charge_+(*Leptons_)[1]->charge_)/2),
                                      ch_((*Leptons_)[0]->flavor_+(*Leptons_)[1]->flavor_-2),
                                      llM_(((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_,(*Leptons_)[0]->phi_,(*Leptons_)[1]->eta_,(*Leptons_)[1]->phi_)),
                                      OnZ_(false){
    if (c_==0 && ch_!=1 && abs(llM_-mZ_)<15) OnZ_ = true;
}
  
event_candidate::~event_candidate(){}




