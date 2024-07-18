#ifndef MY_matrix_method
#define MY_matrix_method

#include "TMatrixD.h"
#include "TVectorD.h"

using namespace std;

class matrix_method {

public:

  matrix_method(float, float, float, float, float, float, int);
  std::vector<float> getWeights(){return Weights;}
  ~matrix_method();
  
private:

  TMatrixD M;
  TVectorD V;
  std::vector<float> Weights;

};

#endif
