#ifndef MyAnalysis_h
#define MyAnalysis_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>

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

// Fixed size dimensions of array or collections stored in the TTree if any.

// Branch information: https://swertz.web.cern.ch/swertz/TMG/TopNano/TopNanoV9/doc_topNanoV9-1-1_MC18UL.html#CaloMET
// Declaration of leaf types
   ULong64_t       event;
   UInt_t          run;
   UInt_t          luminosityBlock;

   Int_t           nGenPart;
   Float_t         GenPart_mass[64];
   Float_t         GenPart_phi[64];
   Float_t         GenPart_pt[64];
   Float_t         GenPart_eta[64];
   Int_t           GenPart_genPartIdxMother[64];
   Int_t           GenPart_pdgId[64];
   Int_t           GenPart_status[64];

   // List of branches
   TBranch        *b_event;
   TBranch        *b_run;
   TBranch        *b_luminosityBlock;
    
   TBranch        *b_nGenPart;
   TBranch        *b_GenPart_mass;
   TBranch        *b_GenPart_phi;
   TBranch        *b_GenPart_pt;
   TBranch        *b_GenPart_eta;
   TBranch        *b_GenPart_genPartIdxMother;
   TBranch        *b_GenPart_pdgId;
   TBranch        *b_GenPart_status;

   MyAnalysis(TTree *tree=0, TString year="", TString data="", TString run="", bool verbose_=false);
   virtual ~MyAnalysis();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString, TString, TString, TString, TString, Float_t,Float_t,Float_t);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
    
   typedef vector<TH1F*> Dim1;
   typedef vector<Dim1> Dim2;
   typedef vector<Dim2> Dim3;
    
   void FillD3Hists(Dim3 H3, int v0, std::vector<int> v1, int v2, float value, std::vector<float> weight);
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
   Init(tree);
}

MyAnalysis::~MyAnalysis()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t MyAnalysis::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t MyAnalysis::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void MyAnalysis::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // poInt_ters of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object poInt_ter

   // Set branch addresses and branch poInt_ters
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("luminosityBlock", &luminosityBlock, &b_luminosityBlock);

   if (data_ == "mc"){
   fChain->SetBranchAddress("nGenPart", &nGenPart, &b_nGenPart);
   fChain->SetBranchAddress("GenPart_mass", &GenPart_mass, &b_GenPart_mass);
   fChain->SetBranchAddress("GenPart_phi", &GenPart_phi, &b_GenPart_phi);
   fChain->SetBranchAddress("GenPart_pt", &GenPart_pt, &b_GenPart_pt);
   fChain->SetBranchAddress("GenPart_eta", &GenPart_eta, &b_GenPart_eta);
   fChain->SetBranchAddress("GenPart_pdgId", &GenPart_pdgId, &b_GenPart_pdgId);
   fChain->SetBranchAddress("GenPart_status", &GenPart_status, &b_GenPart_status);
   fChain->SetBranchAddress("GenPart_genPartIdxMother", &GenPart_genPartIdxMother, &b_GenPart_genPartIdxMother);
   }

   Notify();
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
