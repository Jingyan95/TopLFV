#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,
                                 std::vector<jet_candidate*>* Jets,
                                 bool verbose)
                                    : c_(-1),
                                      ch_(-1),
                                      Leptons_(Leptons),
                                      Jets_(Jets),
                                      verbose_(verbose),
                                      eleMVA_(0),
                                      muMVA_(0),
                                      tauMVA_(0){
    c_ = abs((*Leptons_)[0]->charge_+(*Leptons_)[1]->charge_)/2;
    ch_ = (*Leptons_)[0]->flavor_+(*Leptons_)[1]->flavor_-2;
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


