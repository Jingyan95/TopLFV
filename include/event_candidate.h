#ifndef MY_event_candidate
#define MY_event_candidate

#include <cmath>
#include <string>
#include <iostream>
#include <vector>
#include <complex>
#include <algorithm>
#include <TLorentzVector.h>
#include "jet_candidate.h"
#include "lepton_candidate.h"

using namespace std;
//using namespace math;
class event_candidate {

public:
  event_candidate(std::vector<lepton_candidate*>* Leptons, bool verbose);
  // ~event_candidate();

  int c() { return c_; }
  int ch() { return ch_; }
  
  static bool ComparePtLepton(lepton_candidate *a, lepton_candidate *b) { return a->pt_ > b->pt_; }

  lepton_candidate* lep1() { return (*Leptons_)[0]; } // Leading lepton in pT
  lepton_candidate* lep2() { return (*Leptons_)[1]; } // Sub-leading lepton in pT

private:

  bool verbose_;
  std::vector<lepton_candidate*>* Leptons_;
  int c_; // Charges: 0->Opposite-Sign, 1->Same-Sign
  int ch_; // Channel: 0->ee+tau, 1->emu+ta, 2->mumu+ta
};

#endif
