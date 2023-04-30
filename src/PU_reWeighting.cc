#include "PU_reWeighting.h"

PU::PU(){}
PU::~PU(){}

double PU::PU_2016preVFP(int NumTrueInteraction, TString type_str){
if (NumTrueInteraction < 0 || NumTrueInteraction > 73 ) {return 1;}
else {
	if (type_str == "nominal") {return puUL2016preVFP_nominal[NumTrueInteraction];}
	else if (type_str == "up") {return puUL2016preVFP_up[NumTrueInteraction];}
	else if (type_str == "down") {return puUL2016preVFP_down[NumTrueInteraction];}
	else {std::cout<<"Error pu string!"<<std::endl; return 1.0;}
}
}

double PU::PU_2016postVFP(int NumTrueInteraction, TString type_str){
if (NumTrueInteraction < 0 || NumTrueInteraction > 73 ) {return 1;}
else {
        if (type_str == "nominal") {return puUL2016postVFP_nominal[NumTrueInteraction];}
        else if (type_str == "up") {return puUL2016postVFP_up[NumTrueInteraction];}
        else if (type_str == "down") {return puUL2016postVFP_down[NumTrueInteraction];}
        else {std::cout<<"Error pu string!"<<std::endl; return 1.0;}
}
}
		
double PU::PU_2017(int NumTrueInteraction, TString type_str){
if (NumTrueInteraction < 0 || NumTrueInteraction > 73 ) {return 1;}
else {
        if (type_str == "nominal") {return puUL2017_nominal[NumTrueInteraction];}
        else if (type_str == "up") {return puUL2017_up[NumTrueInteraction];}
        else if (type_str == "down") {return puUL2017_down[NumTrueInteraction];}
	else {std::cout<<"Error pu string!"<<std::endl; return 1.0;}
}
}
		
double PU::PU_2018(int NumTrueInteraction, TString type_str){
if (NumTrueInteraction < 0 || NumTrueInteraction > 73 ) {return 1;}
else {
        if (type_str == "nominal") {return puUL2018_nominal[NumTrueInteraction];}
        else if (type_str == "up") {return puUL2018_up[NumTrueInteraction];}
        else if (type_str == "down") {return puUL2018_down[NumTrueInteraction];}
	else {std::cout<<"Error pu string!"<<std::endl; return 1.0;}
}
}
				
