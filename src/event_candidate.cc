#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,
                                 std::vector<quark_candidate*>* Quarks,
                                 bool verbose)
                                    : ch_(-1),
                                      Leptons_(Leptons),
                                      Quarks_(Quarks),
                                      llM_(0),
                                      llDr_(0),
                                      verbose_(verbose) {
for (int k=0;k<(int)Leptons_->size();k++){
    if (abs((*Leptons_)[k]->pdgid_)==11) LFVe_ = (*Leptons_)[k]->p4_;
    if (abs((*Leptons_)[k]->pdgid_)==13) LFVmu_ = (*Leptons_)[k]->p4_;
    if (abs((*Leptons_)[k]->pdgid_)==15) LFVtau_ = (*Leptons_)[k]->p4_;
}
if (abs((*Leptons_)[0]->pdgid_)+abs((*Leptons_)[1]->pdgid_)==24) ch_ = 0;//emu
if (abs((*Leptons_)[0]->pdgid_)+abs((*Leptons_)[1]->pdgid_)==26) ch_ = 1;//etau
if (abs((*Leptons_)[0]->pdgid_)+abs((*Leptons_)[1]->pdgid_)==28) ch_ = 2;//mutau
llM_=((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M();
llDr_=deltaR((*Leptons_)[0]->eta_,(*Leptons_)[0]->phi_,(*Leptons_)[1]->eta_,(*Leptons_)[1]->phi_);
}
  
event_candidate::~event_candidate(){}


