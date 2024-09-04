#include "MyAnalysis.h"
#include "ROOT/TSeq.hxx"
#include <thread>
#include <atomic>

std::mutex MyAnalysis::mtx_;

int main() {
  int Sys = system("rm -f test*.root");
  if (Sys<0) {std::cout<<"No files named test*.root"<<std::endl;}
  ROOT::EnableThreadSafety();
  UInt_t nThread = 2;
  std::stringstream Summary;
  Summary << "\nNumber of threads requested " << nThread << ".\n";
  auto workerIDs = ROOT::TSeqI(nThread);
  std::atomic<ULong64_t> progress(0);
  std::atomic<ULong64_t> counter(0);
  auto workItem = [&](UInt_t workerID) {
    TChain* ch = new TChain("Events");
    ch->Add("/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016/2016_H_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_H_SingleElectron/230429_193225/0000/tree_1.root");
    ch->Add("/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016/2016_H_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_H_SingleElectron/230429_193225/0000/tree_10.root");
    ch->Add("/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016/2016_H_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_H_SingleElectron/230429_193225/0000/tree_11.root");
    ch->Add("/eos/user/s/skinnari/TopLFV/LFV_Trilep_Inclusive/2016/2016_H_SingleElectron/SingleElectron/crab_Trilep_Inclusive_Apr29_JEC_2016_H_SingleElectron/230429_193225/0000/tree_12.root");
    MyAnalysis t1(ch, "2016" , "data" , "H", nThread, workerID, false, false);
    auto workerSummary = t1.Loop(Form("test_%u.root",workerID), "data" , "SingleElectron" , "2016" , "H" , 1 , 1 , 1, std::ref(progress), std::ref(counter));
    Summary << workerSummary.str();
  };
  std::vector<std::thread> workers;
  for (auto workerID : workerIDs) {
    workers.emplace_back(workItem, workerID);
  }
  for (auto&& worker : workers) worker.join();
  std::cout << Summary.str();
  if (counter>0){//Rerun jobs if they fail to open root files 
    Sys = system("hadd test.root test_*.root");
    if (Sys<0) {std::cout<<"Filed to hadd test.root"<<std::endl;}
    Sys = system("rm -f test_*.root");
    if (Sys<0) {std::cout<<"No files named test*.root"<<std::endl;}
  }
  return 0;
}
