#include "lepton_candidate.h"

lepton_candidate::lepton_candidate(float pt_in, float eta_in, float phi_in, float dz_in, int charge_in, float mva1_in, float mva2_in, float mva3_in, int index_in, int flavor_in, int truth_in) {
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  dz_ = dz_in;
  charge_ = charge_in;
  mva1_ = mva1_in;
  mva2_ = mva2_in;
  mva3_ = mva3_in;
  index_ = index_in;
  flavor_ = flavor_in;
  if (flavor_ == 1) {
    p4_.SetPtEtaPhiM(pt_, eta_, phi_, 0.000511);
    if (truth_in == 1 || truth_in == 15) {
      truth_ = 0;
    } else if (truth_in == 4 || truth_in == 5) {
      truth_ = 1;
    } else {
      truth_ = 2;
    }
  }
  if (flavor_ == 2) {
    p4_.SetPtEtaPhiM(pt_, eta_, phi_, 0.10566);
    if (truth_in == 1 || truth_in == 15) {
      truth_ = 0;
    } else if (truth_in == 4 || truth_in == 5) {
      truth_ = 1;
    } else {
      truth_ = 2;
    }
  }
  if (flavor_ == 3) {
    p4_.SetPtEtaPhiM(pt_, eta_, phi_, 1.777);
    if (truth_in == 5) {
      truth_ = 0;
    } else if (truth_in == 0) {
      truth_ = 1;
    } else {
      truth_ = 2;
    }
  }
}

lepton_candidate::~lepton_candidate() {}
