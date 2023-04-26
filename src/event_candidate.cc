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
                                      njet_(Jets->size()),
                                      nbjet_(0),
                                      Topmass_(0),
                                      llM_(((*Leptons_)[0]->p4_+(*Leptons_)[1]->p4_).M()),
                                      llDr_(deltaR((*Leptons_)[0]->eta_,(*Leptons_)[0]->phi_,(*Leptons_)[1]->eta_,(*Leptons_)[1]->phi_)),
                                      OnZ_(false){
    if (c_==0 && ch_!=1 && abs(llM_-mZ_)<15) OnZ_ = true;
    if (c_==1 && ch_==0 && abs(llM_-mZ_)<15) OnZ_ = true;//Same-Sign ee 
    sort(Jets->begin(), Jets->end(), CompareBtagJet);
    if (Jets->size()) bjet_ = (*Jets_)[0];
    sort(Jets->begin(), Jets->end(), ComparePtJet);
    for (int l=0;l<(int)Jets->size();l++){
        if((*Jets)[l]->btag_) nbjet_++;
    }
    if (c_==0){
        if (ch_==0){
            lfvch_ = 1;
            LFVta_ = (*Leptons_)[2];
            if ((*Leptons_)[0]->charge_+(*Leptons_)[2]->charge_==0){
                LFVe_ = (*Leptons_)[0];
                Balep_ = (*Leptons_)[1];
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[1],MET_)+(*Leptons_)[1]->p4_+bjet_->p4_).M();
            }
            else{
                LFVe_ = (*Leptons_)[1];
                Balep_ = (*Leptons_)[0];
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[0],MET_)+(*Leptons_)[0]->p4_+bjet_->p4_).M();
            }
        }
        if (ch_==1){
            float topmass0 = 0;
            float topmass1 = 0;
            float obs0 = (*Leptons_)[2]->pt_;
            int ba = abs((*Leptons_)[1]->charge_+(*Leptons_)[2]->charge_)/2;
            float obs1 = (*Leptons_)[ba]->pt_;
            if (Jets_->size()){
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
            }else if (ba){
                Topmass_ = topmass1;
                lfvch_ = 1;
                Balep_ = (*Leptons_)[1];
                LFVe_ = (*Leptons_)[0];
                LFVta_ = (*Leptons_)[2];
            }else{
                Topmass_ = topmass1;
                lfvch_ = 2;
                Balep_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
                LFVta_ = (*Leptons_)[2];
            }
        }
        if (ch_==2){
            lfvch_ = 2;
            LFVta_ = (*Leptons_)[2];
            if ((*Leptons_)[0]->charge_+(*Leptons_)[2]->charge_==0){
                LFVmu_ = (*Leptons_)[0];
                Balep_ = (*Leptons_)[1];
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[1],MET_)+(*Leptons_)[1]->p4_+bjet_->p4_).M();
            }
            else{
                LFVmu_ = (*Leptons_)[1];
                Balep_ = (*Leptons_)[0];
                if (Jets->size()) Topmass_ = (solveNeutrinoPz((*Leptons_)[0],MET_)+(*Leptons_)[0]->p4_+bjet_->p4_).M();
            }
        }
    }else{
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
        if (ch_==0){
            lfvch_ = 1;
            if (obs0<obs1){
                Topmass_ = topmass0;
                Balep_ = (*Leptons_)[0];
                LFVe_ = (*Leptons_)[1];
            }else{
                Topmass_ = topmass1;
                Balep_ = (*Leptons_)[1];
                LFVe_ = (*Leptons_)[0];
            }
        }
        if (ch_==1){
            if (obs0<obs1){
                lfvch_ = 2;
                Topmass_ = topmass0;
                Balep_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
            }else{
                lfvch_ = 1;
                Topmass_ = topmass1;
                Balep_ = (*Leptons_)[1];
                LFVe_ = (*Leptons_)[0];
            }
        }
        if (ch_==2){
            lfvch_ = 2;
            if (obs0<obs1){
                Topmass_ = topmass0;
                Balep_ = (*Leptons_)[0];
                LFVmu_ = (*Leptons_)[1];
            }else{
                Topmass_ = topmass1;
                Balep_ = (*Leptons_)[1];
                LFVmu_ = (*Leptons_)[0];
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