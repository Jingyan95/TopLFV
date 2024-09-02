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
                                      ch_((*Leptons_)[0]->flavor_ + (*Leptons_)[1]->flavor_ - 2),
                                      lfvch_(-1),
                                      SRindex_(-1),
                                      njet_(Jets->size()),
                                      nbjet_(0),
                                      btagSF_(1),
                                      btagSum_(0),
                                      Ht_(0),
                                      St_(0),
                                      Topmass_(0),
                                      llM_(((*Leptons_)[0]->p4_ + (*Leptons_)[1]->p4_).M()),
                                      llPt_(((*Leptons_)[0]->p4_ + (*Leptons_)[1]->p4_).Pt()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_, (*Leptons_)[0]->phi_, (*Leptons_)[1]->eta_, (*Leptons_)[1]->phi_)),
                                      OnZ_(false),
                                      SideBand_(false),
                                      OffZ_(false),
                                      TightLep1_(this->lep1()->mva1_ < 0.64 ? 0 : 1),
                                      TightLep2_(this->lep2()->mva1_ < 0.64 ? 0 : 1),
                                      TightTa_(this->ta1()->mva1WP_ < 5 ? 0 : 1),
                                      typeIndex_(7 - (TightLep1_<<2) - (TightLep2_<<1) - TightTa_) {                             
  if (c_ == 0 && ch_ != 1 && abs(llM_ - mZ_) < 15) OnZ_ = true;
  if (c_ == 1 && ch_ == 0 && abs(llM_ - mZ_) < 15) OnZ_ = true; // Same-Sign ee
  if (c_ == 0 && ch_ != 1 && abs(llM_ - mZ_) > 15 && abs(llM_ - mZ_) < 40) SideBand_ = true;
  if (!OnZ_ && !SideBand_) OffZ_ = true;

  sort(Jets->begin(), Jets->end(), CompareBtagJet);
  if (Jets->size()) bjet_ = (*Jets_)[0];
  sort(Jets->begin(), Jets->end(), ComparePtJet);
  float px_ = MET_pt * cos(MET_phi);
  float py_ = MET_pt * sin(MET_phi);
  for (int l = 0; l < (int) Jets->size(); l++) {
    btagSF_ *= (*Jets)[l]->btSF_;
    btagSum_ += (*Jets)[l]->bt_;
    Ht_ += (*Jets)[l]->pt_;
    if ((*Jets)[l]->btag_) nbjet_++;
    px_ += (*Jets)[l]->pt_ * cos((*Jets)[l]->phi_);
    py_ += (*Jets)[l]->pt_ * sin((*Jets)[l]->phi_);
  }
  St_ = Ht_ + (*Leptons_)[0]->pt_ + (*Leptons_)[1]->pt_ + (*Leptons_)[2]->pt_ + MET_->Pt();
  float px1_ = px_+ (*Leptons_)[1]->pt_ * cos((*Leptons_)[1]->phi_);
  float py1_ = py_+ (*Leptons_)[1]->pt_ * sin((*Leptons_)[1]->phi_);
  px1_ += (*Leptons_)[2]->pt_ * cos((*Leptons_)[2]->phi_);
  py1_ += (*Leptons_)[2]->pt_ * sin((*Leptons_)[2]->phi_);

  float px2_ = px_+ (*Leptons_)[0]->pt_ * cos((*Leptons_)[0]->phi_);
  float py2_ = py_+ (*Leptons_)[0]->pt_ * sin((*Leptons_)[0]->phi_);
  px2_ += (*Leptons_)[2]->pt_ * cos((*Leptons_)[2]->phi_);
  py2_ += (*Leptons_)[2]->pt_ * sin((*Leptons_)[2]->phi_);

  float px3_ = px_+ (*Leptons_)[0]->pt_ * cos((*Leptons_)[0]->phi_);
  float py3_ = py_+ (*Leptons_)[0]->pt_ * sin((*Leptons_)[0]->phi_);
  px3_ += (*Leptons_)[1]->pt_ * cos((*Leptons_)[1]->phi_);
  py3_ += (*Leptons_)[1]->pt_ * sin((*Leptons_)[1]->phi_);

  nonlep_ = new TLorentzVector(px1_, py1_, 0, sqrt(px1_ * px1_ + py1_ * py1_));
  (*Leptons_)[0]->setRecoil(-1 * nonlep_->Pt() * cos(deltaPhi(nonlep_->Phi(), (*Leptons_)[0]->phi_)));
  nonlep_ = new TLorentzVector(px2_, py2_, 0, sqrt(px2_ * px2_ + py2_ * py2_));
  (*Leptons_)[1]->setRecoil(-1 * nonlep_->Pt() * cos(deltaPhi(nonlep_->Phi(), (*Leptons_)[1]->phi_)));
  nonlep_ = new TLorentzVector(px3_, py3_, 0, sqrt(px3_ * px3_ + py3_ * py3_));
  (*Leptons_)[2]->setRecoil(-1 * nonlep_->Pt() * cos(deltaPhi(nonlep_->Phi(), (*Leptons_)[2]->phi_)));

  if (c_ == 0) { // Looking at Opposite-Sign first
    if (ch_ == 0) { // ee
      lfvch_ = 1;
      LFVta_ = (*Leptons_)[2];
      if ((*Leptons_)[0]->charge_ + (*Leptons_)[2]->charge_ == 0) { // Electron and tau must have opposite sign to form LFV pair
        LFVe_ = (*Leptons_)[0];
        Balep_ = (*Leptons_)[1];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 0 : 1;
        if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[1], MET_) + (*Leptons_)[1]->p4_ + bjet_->p4_).M();
      }
      else {
        LFVe_ = (*Leptons_)[1];
        Balep_ = (*Leptons_)[0];
        SRindex_ = ((*Leptons_)[1]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 0 : 1;
        if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[0], MET_) + (*Leptons_)[0]->p4_ + bjet_->p4_).M();
      }
    }
    if (ch_ == 1){ // emu
      float topmass0 = 0;
      float topmass1 = 0;
      float obs0 = (*Leptons_)[2]->pt_; // Assuming lepton with lower pT is the SM lepton when top quark can not be reconstructed
      int ba = abs((*Leptons_)[1]->charge_ + (*Leptons_)[2]->charge_) / 2;
      float obs1 = (*Leptons_)[ba]->pt_;
      if (Jets_->size()) { // Top quark can only be reconstructed when there is at least one jet
        topmass0 = (solveNeutrinoPz((*Leptons_)[2], MET_) + (*Leptons_)[2]->p4_ + bjet_->p4_).M();
        topmass1 = (solveNeutrinoPz((*Leptons_)[ba], MET_) + (*Leptons_)[ba]->p4_ + bjet_->p4_).M();
        obs0 = abs(topmass0 - mT_);
        obs1 = abs(topmass1 - mT_);
      }
      // if (TightTa_ && (*Leptons_)[ba]->mva1_ < 0.64) obs1 = -1;
      // if (!TightTa_ && (*Leptons_)[ba]->mva1_ > 0.64) obs0 = -1;
      if (obs0<obs1) {
        Topmass_ = topmass0;
        lfvch_ = 0;
        Balep_ = (*Leptons_)[2];
        LFVe_ = (*Leptons_)[0];
        LFVmu_ = (*Leptons_)[1];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[1]->p4_).M() < lfvmCut_ ? 2 : 3;
      }
      else if (ba) {
        Topmass_ = topmass1;
        lfvch_ = 1;
        Balep_ = (*Leptons_)[1];
        LFVe_ = (*Leptons_)[0];
        LFVta_ = (*Leptons_)[2];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 4 : 5;
      }
      else {
        Topmass_ = topmass1;
        lfvch_ = 2;
        Balep_ = (*Leptons_)[0];
        LFVmu_ = (*Leptons_)[1];
        LFVta_ = (*Leptons_)[2];
        SRindex_ = ((*Leptons_)[1]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 6 : 7;
      }
    }
    if (ch_ == 2) { // mumu
      lfvch_ = 2;
      LFVta_ = (*Leptons_)[2];
      if ((*Leptons_)[0]->charge_ + (*Leptons_)[2]->charge_ == 0) {
        LFVmu_ = (*Leptons_)[0];
        Balep_ = (*Leptons_)[1];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 8 : 9;
        if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[1], MET_) + (*Leptons_)[1]->p4_ + bjet_->p4_).M();
      }
      else {
        LFVmu_ = (*Leptons_)[1];
        Balep_ = (*Leptons_)[0];
        SRindex_ = ((*Leptons_)[1]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 8 : 9;
        if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[0], MET_) + (*Leptons_)[0]->p4_ + bjet_->p4_).M();
      }
    }
  }
  else { // Same-Sign
    LFVta_ = (*Leptons_)[2];
    float topmass0 = 0;
    float topmass1 = 0;
    float obs0 = (*Leptons_)[0]->pt_;
    float obs1 = (*Leptons_)[1]->pt_;
    if (Jets_->size()) {
      topmass0 = (solveNeutrinoPz((*Leptons_)[0], MET_) + (*Leptons_)[0]->p4_ + bjet_->p4_).M();
      topmass1 = (solveNeutrinoPz((*Leptons_)[1], MET_) + (*Leptons_)[1]->p4_ + bjet_->p4_).M();
      obs0 = abs(topmass0 - mT_);
      obs1 = abs(topmass1 - mT_);
    }
    if ((*Leptons_)[0]->mva1_ > 0.64 && (*Leptons_)[1]->mva1_ < 0.64) obs1 = -1;
    if ((*Leptons_)[0]->mva1_ < 0.64 && (*Leptons_)[1]->mva1_ > 0.64) obs0 = -1;
    if (ch_ == 0) { // ee
      lfvch_ = 1;
      if (obs0 < obs1) {
        Topmass_ = topmass0;
        Balep_ = (*Leptons_)[0];
        LFVe_ = (*Leptons_)[1];
        SRindex_ = ((*Leptons_)[1]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 10 : 11;
      }
      else {
        Topmass_ = topmass1;
        Balep_ = (*Leptons_)[1];
        LFVe_ = (*Leptons_)[0];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 10 : 11;
      }
    }
    if (ch_ == 1) { // emu
      if (obs0 < obs1) {
        lfvch_ = 2;
        Topmass_ = topmass0;
        Balep_ = (*Leptons_)[0];
        LFVmu_ = (*Leptons_)[1];
        SRindex_ = ((*Leptons_)[1]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 14 : 15;
      }
      else {
        lfvch_ = 1;
        Topmass_ = topmass1;
        Balep_ = (*Leptons_)[1];
        LFVe_ = (*Leptons_)[0];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 12 : 13;
      }
    }
    if (ch_ == 2) { // mumu
      lfvch_ = 2;
      if (obs0 < obs1) {
        Topmass_ = topmass0;
        Balep_ = (*Leptons_)[0];
        LFVmu_ = (*Leptons_)[1];
        SRindex_ = ((*Leptons_)[1]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 16 : 17;
      }
      else {
        Topmass_ = topmass1;
        Balep_ = (*Leptons_)[1];
        LFVmu_ = (*Leptons_)[0];
        SRindex_ = ((*Leptons_)[0]->p4_ + (*Leptons_)[2]->p4_).M() < lfvmCut_ ? 16 : 17;
      }
    }
  }
  if (lfvch_ == 0) {
    LFVllM_ = (LFVe_->p4_ + LFVmu_->p4_).M();
    LFVllDr_ = deltaR(LFVe_->eta_, LFVe_->phi_, LFVmu_->eta_, LFVmu_->phi_);
  }
  if (lfvch_ == 1) {
    LFVllM_ = (LFVe_->p4_ + LFVta_->p4_).M();
    LFVllDr_ = deltaR(LFVe_->eta_, LFVe_->phi_, LFVta_->eta_, LFVta_->phi_);
  }
  if (lfvch_ == 2) {
    LFVllM_ = (LFVmu_->p4_ + LFVta_->p4_).M();
    LFVllDr_ = deltaR(LFVmu_->eta_, LFVmu_->phi_, LFVta_->eta_, LFVta_->phi_);
  }
}

event_candidate::~event_candidate() { delete MET_; delete nonlep_;}
