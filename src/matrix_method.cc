#include "matrix_method.h"

matrix_method::matrix_method(float r1, float r2 , float r3, float f1, float f2, float f3, int type):
                             M(8,8),
                             V(8),
                             Weights(0) {
  M(0,0)=r1*r2*r3;
  M(0,1)=r1*r2*f3;
  M(0,2)=r1*f2*r3;
  M(0,3)=r1*f2*f3;
  M(0,4)=f1*r2*r3;
  M(0,5)=f1*r2*f3;
  M(0,6)=f1*f2*r3;
  M(0,7)=f1*f2*f3;
    
  M(1,0)=r1*r2*(1-r3);
  M(1,1)=r1*r2*(1-f3);
  M(1,2)=r1*f2*(1-r3);
  M(1,3)=r1*f2*(1-f3);
  M(1,4)=f1*r2*(1-r3);
  M(1,5)=f1*r2*(1-f3);
  M(1,6)=f1*f2*(1-r3);
  M(1,7)=f1*f2*(1-f3);
    
  M(2,0)=r1*(1-r2)*r3;
  M(2,1)=r1*(1-r2)*f3;
  M(2,2)=r1*(1-f2)*r3;
  M(2,3)=r1*(1-f2)*f3;
  M(2,4)=f1*(1-r2)*r3;
  M(2,5)=f1*(1-r2)*f3;
  M(2,6)=f1*(1-f2)*r3;
  M(2,7)=f1*(1-f2)*f3;
    
  M(3,0)=r1*(1-r2)*(1-r3);
  M(3,1)=r1*(1-r2)*(1-f3);
  M(3,2)=r1*(1-f2)*(1-r3);
  M(3,3)=r1*(1-f2)*(1-f3);
  M(3,4)=f1*(1-r2)*(1-r3);
  M(3,5)=f1*(1-r2)*(1-f3);
  M(3,6)=f1*(1-f2)*(1-r3);
  M(3,7)=f1*(1-f2)*(1-f3);

  M(4,0)=(1-r1)*r2*r3;
  M(4,1)=(1-r1)*r2*f3;
  M(4,2)=(1-r1)*f2*r3;
  M(4,3)=(1-r1)*f2*f3;
  M(4,4)=(1-f1)*r2*r3;
  M(4,5)=(1-f1)*r2*f3;
  M(4,6)=(1-f1)*f2*r3;
  M(4,7)=(1-f1)*f2*f3;

  M(5,0)=(1-r1)*r2*(1-r3);
  M(5,1)=(1-r1)*r2*(1-f3);
  M(5,2)=(1-r1)*f2*(1-r3);
  M(5,3)=(1-r1)*f2*(1-f3);
  M(5,4)=(1-f1)*r2*(1-r3);
  M(5,5)=(1-f1)*r2*(1-f3);
  M(5,6)=(1-f1)*f2*(1-r3);
  M(5,7)=(1-f1)*f2*(1-f3);

  M(6,0)=(1-r1)*(1-r2)*r3;
  M(6,1)=(1-r1)*(1-r2)*f3;
  M(6,2)=(1-r1)*(1-f2)*r3;
  M(6,3)=(1-r1)*(1-f2)*f3;
  M(6,4)=(1-f1)*(1-r2)*r3;
  M(6,5)=(1-f1)*(1-r2)*f3;
  M(6,6)=(1-f1)*(1-f2)*r3;
  M(6,7)=(1-f1)*(1-f2)*f3;

  M(7,0)=(1-r1)*(1-r2)*(1-r3);
  M(7,1)=(1-r1)*(1-r2)*(1-f3);
  M(7,2)=(1-r1)*(1-f2)*(1-r3);
  M(7,3)=(1-r1)*(1-f2)*(1-f3);
  M(7,4)=(1-f1)*(1-r2)*(1-r3);
  M(7,5)=(1-f1)*(1-r2)*(1-f3);
  M(7,6)=(1-f1)*(1-f2)*(1-r3);
  M(7,7)=(1-f1)*(1-f2)*(1-f3);
    
  V(0)=0;
  V(1)=0;
  V(2)=0;
  V(3)=0;
  V(4)=0;
  V(5)=0;
  V(6)=0;
  V(7)=0;
  V(type)=1;
  
  auto R = M.Invert() * V;
  Weights.push_back(R[0]*r1*r2*r3); //fully prompt 
  Weights.push_back(R[2]*r1*f2*r3+R[4]*f1*r2*r3+R[6]*f1*f2*r3); //fake e/mu
  Weights.push_back(R[3]*r1*f2*f3+R[5]*f1*r2*f3+R[7]*f1*f2*f3); //fake e/mu + fake tau
  Weights.push_back(R[1]*r1*r2*f3); //fake tau
}

matrix_method::~matrix_method() {}
