#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,bool verbose)
                                    : verbose_(verbose),
                                      Leptons_(Leptons),
                                      c_(abs((*Leptons_)[0]->charge_+(*Leptons_)[1]->charge_)/2),
                                      ch_(-1){
  sort(Leptons_->begin(), Leptons_->end(), ComparePtLepton);
  if ((*Leptons_)[0]->flavor_+(*Leptons_)[1]->flavor_ == 2){
     ch_ = 0;
  }else if ((*Leptons_)[0]->flavor_+(*Leptons_)[1]->flavor_ == 4){
     ch_ = 3;
  }else if ((*Leptons_)[0]->flavor_==1){
     ch_ = 1;
  }else{
     ch_ = 2;
  }
}
