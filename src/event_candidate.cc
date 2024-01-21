#include "event_candidate.h"

event_candidate::event_candidate(std::vector<lepton_candidate*>* Leptons,
                                 std::vector<jet_candidate*>* Jets,
                                 float MET_pt,
                                 float MET_phi,
                                 bool verbose)
                                    : verbose_(verbose),
                                      Leptons_(Leptons),
                                      Jets_(Jets),
                                      MET_(new TLorentzVector(MET_pt * cos(MET_phi), MET_pt * sin(MET_phi), 0, MET_pt)),
                                      c_(abs((*Leptons_)[0]->charge_ + (*Leptons_)[1]->charge_) / 2),
                                      ch_((*Leptons_)[0]->flavor_ - 1),
                                      njet_(Jets->size()),
                                      nbjet_(0),
                                      btagSF_(1),
                                      btagSum_(0),
                                      Ht_(0),
                                      St_(0),
                                      llM_(((*Leptons_)[0]->p4_ + (*Leptons_)[1]->p4_).M()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_, (*Leptons_)[0]->phi_, (*Leptons_)[1]->eta_, (*Leptons_)[1]->phi_)),
                                      OnZ_(false),
                                      TightTa_((*Leptons_)[1]->mva1WP_ < 5 ? false : true) {
  if (llM_ - mZ_ > -33 && llM_ - mZ_ < 17) OnZ_ = true;
  sort(Jets->begin(), Jets->end(), CompareBtagJet);
  if (Jets->size()) bjet_ = (*Jets_)[0];
  sort(Jets->begin(), Jets->end(), ComparePtJet);
  for (int l = 0; l < (int) Jets->size(); l++) {
    btagSF_ *= (*Jets)[l]->btSF_;
    btagSum_ += (*Jets)[l]->bt_;
    Ht_ += (*Jets)[l]->pt_;
    if ((*Jets)[l]->btag_) nbjet_++;
  }
  St_ = Ht_ + (*Leptons_)[0]->pt_ + (*Leptons_)[1]->pt_ + MET_->Pt();
}

event_candidate::~event_candidate() { delete MET_; }
