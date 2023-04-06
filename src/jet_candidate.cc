#include "jet_candidate.h"

jet_candidate::jet_candidate(float pt_in, float eta_in, float phi_in, float mass_in, int pdgid_in, int mother_idx_in, int mother_pdgid_in){
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  mass_ = mass_in;
  pdgid_ = pdgid_in;
  mother_idx_ = mother_idx_in;
  mother_pdgid_ = mother_pdgid_in;
  p4_.SetPtEtaPhiM(pt_, eta_, phi_, mass_) ;
}
  
jet_candidate::~jet_candidate(){}


