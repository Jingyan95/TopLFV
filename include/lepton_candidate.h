#ifndef MY_lepton_candidate
#define MY_lepton_candidate

#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <TLorentzVector.h>

using namespace std;
//using namespace math;
class lepton_candidate {
  
public:
  lepton_candidate(float, float, float, float, int, float, float, float, int, int, int);
  ~lepton_candidate();
  float pt_;
  float eta_;
  float phi_;
  float dz_;
  int charge_;
  float mva1_;
  float mva2_;
  float mva3_;
  int index_;
  int flavor_;
  int truth_;
  TLorentzVector p4_;

private:
  
};

#endif