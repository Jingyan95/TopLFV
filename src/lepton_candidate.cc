#include "lepton_candidate.h"

lepton_candidate::lepton_candidate(float pt_in, float eta_in, float phi_in, int pdgid_in, int mother_idx_in, int mother_pdgid_in){
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  pdgid_ = pdgid_in;
  charge_ = -abs(pdgid_in);
  mother_idx_ = mother_idx_in;
  mother_pdgid_ = mother_pdgid_in;
  if (abs(pdgid_)==11) p4_.SetPtEtaPhiM(pt_, eta_, phi_, 0.000511) ;
  if (abs(pdgid_)==13) p4_.SetPtEtaPhiM(pt_, eta_, phi_, 0.10566) ;
  if (abs(pdgid_)==15) p4_.SetPtEtaPhiM(pt_, eta_, phi_, 1.777) ;
}

lepton_candidate::~lepton_candidate(){}


