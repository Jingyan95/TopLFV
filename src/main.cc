#include "MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events");  //"Events") ;
//    ch ->Add("/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/TT_clequ1_lltu/0000.root");
    ch ->Add("/eos/cms/store/user/jingyan/LFV_Inclusive_Trilep/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Inclusive_Trilep_2016_TTW_UL/230331_081630/0000/tree_11.root");
    MyAnalysis t1(ch,"2016","mc","",false);
    t1.Loop("test.root", "mc", "LFVTtScalarU", "2016", "", 0.012, 16.81, 1000);
    return 0;
}
