#include "MyAnalysis.h"
#include "ROOT/TSeq.hxx"
#include <thread>
int main(){
    ROOT::EnableThreadSafety();
    UInt_t nThread = 6;
    auto workerIDs = ROOT::TSeqI(nThread);
    auto workItem = [=](UInt_t workerID) {
        TChain* ch = new TChain("Events");  
        ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_May1_BtagSF/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_5.root");
        ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_May1_BtagSF/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_6.root");
        ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_May1_BtagSF/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_7.root");
        ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive_May1_BtagSF/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_10.root");
        MyAnalysis t1(ch,"2016","mc","",nThread,workerID,false);
        t1.Loop(Form("test_%u.root",workerID), "mc", "TTW", "2016", "", 0.235, 16.81, 3322643);
    };
    std::vector<std::thread> workers;
    for (auto workerID : workerIDs) {
        workers.emplace_back(workItem, workerID);
    }
    for (auto&& worker : workers) worker.join();
    return 0;
}