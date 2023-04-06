#include "MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events");  //"Events") ;
    ch ->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr6/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_Apr6_2016_TTW_UL/230406_185030/0000/tree_12.root");
    MyAnalysis t1(ch,"2016","mc","",false);
    t1.Loop("test.root", "mc", "TTW", "2016", "", 0.2043, 16.81, 3322643);
    return 0;
}
