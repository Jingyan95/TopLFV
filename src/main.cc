#include "MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events");  //"Events") ;
    ch ->Add("/eos/cms/store/user/jingyan/LFV_Inclusive_Trilep/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Inclusive_Trilep_2016_TTW_UL/230331_081630/0000/tree_11.root");
    MyAnalysis t1(ch,"2016","mc","",false);
    t1.Loop("test.root", "mc", "TTW", "2016", "", 0.2043, 16.81, 3322643);
    return 0;
}
