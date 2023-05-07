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
                                      lfvch_(-1),
                                      SRindex_(-1),
                                      njet_(Jets->size()),
                                      nbjet_(0),
                                      btagSF_(1),
                                      btagSum_(0),
                                      Ht_(0),
                                      St_(0),
                                      Topmass_(0),
                                      llM_(((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_,(*Leptons_)[0]->phi_,(*Leptons_)[1]->eta_,(*Leptons_)[1]->phi_)),
                                      OnZ_(false){
    if (c_==0 && ch_!=1 && llM_-mZ_>-33 && llM_-mZ_<17) OnZ_ = true;
    if (c_==1 && ch_==0 && llM_-mZ_>-33 && llM_-mZ_<17) OnZ_ = true;//Same-Sign ee 
    sort(Jets->begin(), Jets->end(), CompareBtagJet);
    if (Jets->size()) bjet_ = (*Jets_)[0];
    sort(Jets->begin(), Jets->end(), ComparePtJet);
    for (int l=0;l<(int)Jets->size();l++){
        btagSF_ *= (*Jets)[l]->btSF_;
        btagSum_ += (*Jets)[l]->bt_;
        Ht_+=(*Jets)[l]->pt_;
        if((*Jets)[l]->btag_) nbjet_++;
    }
    St_=Ht_+(*Leptons_)[0]->pt_+(*Leptons_)[1]->pt_+(*Leptons_)[2]->pt_+MET_->Pt();
    if (c_==0){//Looking at Opposite-Sign first
        if (ch_==0){//ee
            lfvch_ = 1;
            LFVta_ = (*Leptons_)[2];
            if ((*Leptons_)[0]->charge_+(*Leptons_)[2]->charge_==0){//Electron and tau must have opposite sign to form LFV pair 
                LFVe_ = (*Leptons_)[0];
                Balep_ = (*Leptons_)[1];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?0:1;
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[1],MET_)+(*Leptons_)[1]->p4_+bjet_->p4_).M();
            }
            else{
                LFVe_ = (*Leptons_)[1];
                Balep_ = (*Leptons_)[0];
                SRindex_ = ((*Leptons_)[1]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?0:1;
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[0],MET_)+(*Leptons_)[0]->p4_+bjet_->p4_).M();
            }
        }
        if (ch_==1){//emu
            float topmass0 = 0;
            float topmass1 = 0;
            float obs0 = (*Leptons_)[2]->pt_;//Assuming lepton with lower pT is the SM lepton when top quark can not be reconstructed
            int ba = abs((*Leptons_)[1]->charge_+(*Leptons_)[2]->charge_)/2;
            float obs1 = (*Leptons_)[ba]->pt_;
            if (Jets_->size()){//Top quark can only be reconstructed when there is at least one jet
                topmass0 = (solveNeutrinoPz((*Leptons_)[2],MET_)+(*Leptons_)[2]->p4_+bjet_->p4_).M();
                topmass1 = (solveNeutrinoPz((*Leptons_)[ba],MET_)+(*Leptons_)[ba]->p4_+bjet_->p4_).M();
                obs0 = abs(topmass0-mT_);
                obs1 = abs(topmass1-mT_);
            }
            if (obs0<obs1){
                Topmass_ = topmass0;
                lfvch_ = 0;
                Balep_ = (*Leptons_)[2];
                LFVe_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M()<lfvmCut_?2:3;
            }else if (ba){
                Topmass_ = topmass1;
                lfvch_ = 1;
                Balep_ = (*Leptons_)[1];
                LFVe_ = (*Leptons_)[0];
                LFVta_ = (*Leptons_)[2];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?4:5;
            }else{
                Topmass_ = topmass1;
                lfvch_ = 2;
                Balep_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
                LFVta_ = (*Leptons_)[2];
                SRindex_ = ((*Leptons_)[1]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?6:7;
            }
        }
        if (ch_==2){//mumu
            lfvch_ = 2;
            LFVta_ = (*Leptons_)[2];
            if ((*Leptons_)[0]->charge_+(*Leptons_)[2]->charge_==0){
                LFVmu_ = (*Leptons_)[0];
                Balep_ = (*Leptons_)[1];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?8:9;
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[1],MET_)+(*Leptons_)[1]->p4_+bjet_->p4_).M();
            }
            else{
                LFVmu_ = (*Leptons_)[1];
                Balep_ = (*Leptons_)[0];
                SRindex_ = ((*Leptons_)[1]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?8:9;
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[0],MET_)+(*Leptons_)[0]->p4_+bjet_->p4_).M();
            }
        }
    }else{//Same-Sign
        LFVta_ = (*Leptons_)[2];
        float topmass0 = 0;
        float topmass1 = 0;
        float obs0 = (*Leptons_)[0]->pt_;
        float obs1 = (*Leptons_)[1]->pt_;
        if (Jets_->size()){
        topmass0 = (solveNeutrinoPz((*Leptons_)[0],MET_)+(*Leptons_)[0]->p4_+bjet_->p4_).M();
        topmass1 = (solveNeutrinoPz((*Leptons_)[1],MET_)+(*Leptons_)[1]->p4_+bjet_->p4_).M();
        obs0 = abs(topmass0-mT_);
        obs1 = abs(topmass1-mT_);
        }
        if (ch_==0){//ee
            lfvch_ = 1;
            if (obs0<obs1){
                Topmass_ = topmass0;
                Balep_ = (*Leptons_)[0];
                LFVe_ = (*Leptons_)[1];
                SRindex_ = ((*Leptons_)[1]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?10:11;
            }else{
                Topmass_ = topmass1;
                Balep_ = (*Leptons_)[1];
                LFVe_ = (*Leptons_)[0];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?10:11;
            }
        }
        if (ch_==1){//emu
            if (obs0<obs1){
                lfvch_ = 2;
                Topmass_ = topmass0;
                Balep_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
                SRindex_ = ((*Leptons_)[1]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?14:15;
            }else{
                lfvch_ = 1;
                Topmass_ = topmass1;
                Balep_ = (*Leptons_)[1];
                LFVe_ = (*Leptons_)[0];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?12:13;
            }
        }
        if (ch_==2){//mumu
            lfvch_ = 2;
            if (obs0<obs1){
                Topmass_ = topmass0;
                Balep_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
                SRindex_ = ((*Leptons_)[1]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?16:17;
            }else{
                Topmass_ = topmass1;
                Balep_ = (*Leptons_)[1];
                LFVmu_ = (*Leptons_)[0];
                SRindex_ = ((*Leptons_)[0]->p4_+(*Leptons_)[2]->p4_).M()<lfvmCut_?16:17;
            }
        }
    }
    if (lfvch_==0){
        LFVllM_ = (LFVe_->p4_+LFVmu_->p4_).M();
        LFVllDr_ = deltaR(LFVe_->eta_,LFVe_->phi_,LFVmu_->eta_,LFVmu_->phi_);
    }
    if (lfvch_==1){
        LFVllM_ = (LFVe_->p4_+LFVta_->p4_).M();
        LFVllDr_ = deltaR(LFVe_->eta_,LFVe_->phi_,LFVta_->eta_,LFVta_->phi_);
    }
    if (lfvch_==2){
        LFVllM_ = (LFVmu_->p4_+LFVta_->p4_).M();
        LFVllDr_ = deltaR(LFVmu_->eta_,LFVmu_->phi_,LFVta_->eta_,LFVta_->phi_);
    }
}
  
event_candidate::~event_candidate(){delete MET_;}