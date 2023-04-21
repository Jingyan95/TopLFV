#include "MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events");  //"Events") ;
    ch ->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr19/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilepton_Inclusive_Apr19_2016_TTW_UL/230419_121349/0000/tree_6.root");
    MyAnalysis t1(ch,"2016","mc","",false);
    t1.Loop("test.root", "mc", "TTW", "2016", "", 0.235, 16.81, 3322643);
    return 0;
}
