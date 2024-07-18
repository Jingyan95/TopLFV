#include "MyAnalysis.h"
#include "ROOT/TSeq.hxx"
#include <thread>
#include <atomic>

std::mutex MyAnalysis::mtx_;

int main() {
  int Sys = system("rm -f test*.root");
  if (Sys<0) {std::cout<<"No files named test*.root"<<std::endl;}
  ROOT::EnableThreadSafety();
  UInt_t nThread = 6;
  std::stringstream Summary;
  Summary << "\nNumber of threads requested " << nThread << ".\n";
  auto workerIDs = ROOT::TSeqI(nThread);
  std::atomic<ULong64_t> progress(0);
  std::atomic<ULong64_t> counter(0);
  auto workItem = [&](UInt_t workerID) {
    TChain* ch = new TChain("Events");
    ch->Add("/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017LFVSignalAndData_v1_2017_TTW_UL/231103_212458/0000/tree_1.root");
    ch->Add("/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017LFVSignalAndData_v1_2017_TTW_UL/231103_212458/0000/tree_2.root");
    ch->Add("/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017LFVSignalAndData_v1_2017_TTW_UL/231103_212458/0000/tree_3.root");
    ch->Add("/eos/user/e/etsai/public/LFV_Dilepton/2017/2017_TTW_UL/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017LFVSignalAndData_v1_2017_TTW_UL/231103_212458/0000/tree_4.root");
    MyAnalysis t1(ch, "2017", "mc", "", nThread, workerID, false);
    auto workerSummary = t1.Loop(Form("test_%u.root", workerID), "mc", "TTW", "2017", "", 0.235, 41.48, 3871055, std::ref(progress), std::ref(counter));
    Summary << workerSummary.str();
  };
  std::vector<std::thread> workers;
  for (auto workerID : workerIDs) {
    workers.emplace_back(workItem, workerID);
  }
  for (auto&& worker : workers) worker.join();
  std::cout << Summary.str();
  Sys = system("hadd test.root test_*.root");
  if (Sys<0) {std::cout<<"Filed to hadd test.root"<<std::endl;}
  Sys = system("rm -f test_*.root");
  if (Sys<0) {std::cout<<"No files named test*.root"<<std::endl;}
  return 0;
}
