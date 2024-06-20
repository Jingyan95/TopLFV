#ifndef MY_lepton_candidate
#define MY_lepton_candidate

#include <cmath>
#include <string>
#include <iostream>
#include <vector>
#include <complex>
#include <TLorentzVector.h>

using namespace std;

class lepton_candidate {

public:
  lepton_candidate(float, float, float, float, float, int, int, float, float, float, int, int, int, int);
  ~lepton_candidate();
  float pt_;
  float eta_;
  float phi_;
  float dxy_;
  float dz_;
  int charge_;
  int mva1WP_; // Currently only used for Tau vs Jet WP
  float mva1_;
  float mva2_;
  float mva3_;
  int index_;
  int flavor_;
  int truth_;
  int decaymode_;
  TLorentzVector p4_;

private:

};

#endif
