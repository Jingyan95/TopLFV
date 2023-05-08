#ifndef MyAnalysis_h
#define MyAnalysis_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "ROOT/TThreadedObject.hxx"

// Header file for the classes stored in the TTree if any.
#include "vector"

using namespace std;
class MyAnalysis {
public :TTree          *fChain;   //!poInt_ter to the analyzed TTree or TChain
   Int_t          fCurrent; //!current Tree number in a TChain
   TString        year_;
   TString        data_;
   TString        run_;
   bool           verbose_;

   MyAnalysis(TTree *tree=0, TString year="", TString data="", TString run="", bool verbose_=false);
   virtual ~MyAnalysis();
   virtual Int_t    Cut(Long64_t entry);
   // virtual void     Init(TTreeReader& myReader);
   virtual void     Loop(TString, TString, TString, TString, TString, Float_t,Float_t,Float_t);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef MyAnalysis_cxx
MyAnalysis::MyAnalysis(TTree *tree, TString year, TString data, TString run, bool verbose) : fChain(0), year_(year), data_(data), run_(run), verbose_(verbose)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/ST_clequ1_lltu/0000.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/afs/cern.ch/work/j/jingyan/public/SMEFTfr_LFV_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM/ST_clequ1_lltu/0000.root");
      }
      f->GetObject("Events",tree);

   }
   fChain = tree;
}

MyAnalysis::~MyAnalysis()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Bool_t MyAnalysis::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.
   return kTRUE;
}

void MyAnalysis::Show(Long64_t entry)
{
// PrInt_t contents of entry.
// If entry is not specified, prInt_t current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t MyAnalysis::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef MyAnalysis_cxx
