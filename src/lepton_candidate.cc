#include "lepton_candidate.h"

lepton_candidate::lepton_candidate(float pt_in, float eta_in, float phi_in, int charge_in, float mva1_in, float mva2_in, float mva3_in, int index_in, int flavor_in){
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  charge_ = charge_in;
  mva1_ = mva1_in;
  mva2_ = mva2_in;
  mva3_ = mva3_in;
  index_ = index_in;
  flavor_ = flavor_in;
  if (flavor_==1) p4_.SetPtEtaPhiM(pt_, eta_, phi_, 0.000511) ;
  if (flavor_==2) p4_.SetPtEtaPhiM(pt_, eta_, phi_, 0.10566) ;
  if (flavor_==3) p4_.SetPtEtaPhiM(pt_, eta_, phi_, 1.777) ;
}

lepton_candidate::~lepton_candidate(){}


