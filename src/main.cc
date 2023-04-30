#include "MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events");  //"Events") ;
    ch ->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr29_JEC/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_Apr29_JEC_2016_TTW_UL/230429_193811/0000/tree_6.root");
    MyAnalysis t1(ch,"2016","mc","",false);
    t1.Loop("test.root", "mc", "TTW", "2016", "", 0.235, 16.81, 3322643);
    // ch ->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_Apr29_JEC/2016_G_DoubleMuon/DoubleMuon/crab_Trilep_Inclusive_Apr29_JEC_2016_G_DoubleMuon/230429_192148/0000/tree_4.root");
    // MyAnalysis t1(ch,"2016","data","G",false);
    // t1.Loop("test.root", "data", "DoubleMuon", "2016", "G", 1, 1, 1);
    return 0;
}