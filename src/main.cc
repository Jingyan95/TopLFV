#include "MyAnalysis.h"
#include "ROOT/TSeq.hxx"
#include <thread>
#include <atomic>

std::mutex MyAnalysis::mtx_;

int main() {
  system("rm -f test*.root");
  ROOT::EnableThreadSafety();
  UInt_t nThread = 6;
  std::stringstream Summary;
  Summary << "\nNumber of threads requested " << nThread << ".\n";
  auto workerIDs = ROOT::TSeqI(nThread);
  std::atomic<ULong64_t> progress(0);
  std::atomic<ULong64_t> counter(0);
  auto workItem = [&](UInt_t workerID) {
    TChain* ch = new TChain("Events");  
    ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_5.root");
    ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_6.root");
    ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_7.root");
    ch->Add("/eos/cms/store/user/jingyan/LFV_Trilep_Inclusive/2016/2016_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_Trilep_Inclusive_May1_BtagSF_2016_TTW_UL/230501_150430/0000/tree_10.root");
    MyAnalysis t1(ch, "2016", "mc", "", nThread, workerID, false);
    auto workerSummary = t1.Loop(Form("test_%u.root", workerID), "mc", "TTW", "2016", "", 0.235, 16.81, 1800823, std::ref(progress), std::ref(counter));
    Summary << workerSummary.str();
  };
  std::vector<std::thread> workers;
  for (auto workerID : workerIDs) {
    workers.emplace_back(workItem, workerID);
  }
  for (auto&& worker : workers) worker.join();
  std::cout << Summary.str();
  system("hadd test.root test_*.root");
  system("rm -f test_*.root");
  return 0;
}
