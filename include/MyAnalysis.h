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
    
   UInt_t          nElectron;
   Int_t           Electron_charge[16];
   Float_t         Electron_deltaEtaSC[16];
   Float_t         Electron_mass[16];
   Float_t         Electron_phi[16];
   Float_t         Electron_pt[16];
   Float_t         Electron_eta[16];
   UChar_t         Electron_jetNDauCharged[16];
   Float_t         Electron_miniPFRelIso_chg[16];
   Float_t         Electron_miniPFRelIso_all[16];
   Float_t         Electron_jetPtRelv2[16];
   Float_t         Electron_pfRelIso03_all[16];
   Float_t         Electron_sip3d[16];
   Float_t         Electron_dxy[16];
   Float_t         Electron_dz[16];
   Float_t         Electron_mvaFall17V2noIso[16];
   UChar_t         Electron_lostHits[16];
   Int_t           Electron_jetIdx[16];
       
   UInt_t          nMuon;
   Int_t           Muon_charge[16];
   Float_t         Muon_mass[16];
   Float_t         Muon_phi[16];
   Float_t         Muon_pt[16];
   Float_t         Muon_eta[16];
   UChar_t         Muon_jetNDauCharged[16];
   Float_t         Muon_miniPFRelIso_chg[16];
   Float_t         Muon_miniPFRelIso_all[16];
   Float_t         Muon_jetPtRelv2[16];
   Float_t         Muon_pfRelIso03_all[16];
   Float_t         Muon_sip3d[16];
   Float_t         Muon_dxy[16];
   Float_t         Muon_dz[16];
   Float_t         Muon_segmentComp[16];
   Int_t           Muon_jetIdx[16];
   Bool_t          Muon_mediumId[16];
    
   UInt_t          nTau;
   Int_t           Tau_charge[16];
   Float_t         Tau_pt[16];
   Float_t         Tau_eta[16];
   Float_t         Tau_phi[16];
   Float_t         Tau_mass[16];
   UChar_t         Tau_genPartFlav[16];
   Int_t           Tau_decayMode[16];
   Float_t         Tau_rawDeepTau2017v2p1VSe[16];
   Float_t         Tau_rawDeepTau2017v2p1VSmu[16];
   Float_t         Tau_rawDeepTau2017v2p1VSjet[16];
   UChar_t         Tau_idDeepTau2017v2p1VSe[16];
   UChar_t         Tau_idDeepTau2017v2p1VSmu[16];
   UChar_t         Tau_idDeepTau2017v2p1VSjet[16];
    
   UInt_t          nJet;
   Float_t         Jet_btagDeepFlavB[16];
    
   // List of branches
   TBranch         *b_event;
   TBranch         *b_run;
   TBranch         *b_luminosityBlock;
    
   TBranch         *b_nElectron;
   TBranch         *b_Electron_charge;
   TBranch         *b_Electron_deltaEtaSC;
   TBranch         *b_Electron_mass;
   TBranch         *b_Electron_phi;
   TBranch         *b_Electron_pt;
   TBranch         *b_Electron_eta;
   TBranch         *b_Electron_jetNDauCharged;
   TBranch         *b_Electron_miniPFRelIso_chg;
   TBranch         *b_Electron_miniPFRelIso_all;
   TBranch         *b_Electron_jetPtRelv2;
   TBranch         *b_Electron_pfRelIso03_all;
   TBranch         *b_Electron_sip3d;
   TBranch         *b_Electron_dxy;
   TBranch         *b_Electron_dz;
   TBranch         *b_Electron_mvaFall17V2noIso;
   TBranch         *b_Electron_lostHits;
   TBranch         *b_Electron_jetIdx;
        
   TBranch         *b_nMuon;
   TBranch         *b_Muon_charge;
   TBranch         *b_Muon_mass;
   TBranch         *b_Muon_phi;
   TBranch         *b_Muon_pt;
   TBranch         *b_Muon_eta;
   TBranch         *b_Muon_jetNDauCharged;
   TBranch         *b_Muon_miniPFRelIso_chg;
   TBranch         *b_Muon_miniPFRelIso_all;
   TBranch         *b_Muon_jetPtRelv2;
   TBranch         *b_Muon_pfRelIso03_all;
   TBranch         *b_Muon_sip3d;
   TBranch         *b_Muon_dxy;
   TBranch         *b_Muon_dz;
   TBranch         *b_Muon_segmentComp;
   TBranch         *b_Muon_jetIdx;
   TBranch         *b_Muon_mediumId;
    
   TBranch         *b_nTau;
   TBranch         *b_Tau_charge;
   TBranch         *b_Tau_pt;
   TBranch         *b_Tau_eta;
   TBranch         *b_Tau_phi;
   TBranch         *b_Tau_mass;
   TBranch         *b_Tau_genPartFlav;
   TBranch         *b_Tau_decayMode;
   TBranch         *b_Tau_rawDeepTau2017v2p1VSe;
   TBranch         *b_Tau_rawDeepTau2017v2p1VSmu;
   TBranch         *b_Tau_rawDeepTau2017v2p1VSjet;
   TBranch         *b_Tau_idDeepTau2017v2p1VSe;
   TBranch         *b_Tau_idDeepTau2017v2p1VSmu;
   TBranch         *b_Tau_idDeepTau2017v2p1VSjet;
    
   TBranch         *b_nJet;
   TBranch         *b_Jet_btagDeepFlavB;
    
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
   typedef vector<Dim3> Dim4;
    
   void FillD4Hists(Dim4 H4, int v0, int v1, std::vector<int> v2, int v3, float value, std::vector<float> weight);
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
    
   fChain->SetBranchAddress("nElectron", &nElectron, &b_nElectron);
   fChain->SetBranchAddress("Electron_charge", &Electron_charge, &b_Electron_charge);
   fChain->SetBranchAddress("Electron_deltaEtaSC", &Electron_deltaEtaSC, &b_Electron_deltaEtaSC);
   fChain->SetBranchAddress("Electron_mass", &Electron_mass, &b_Electron_mass);
   fChain->SetBranchAddress("Electron_phi", &Electron_phi, &b_Electron_phi);
   fChain->SetBranchAddress("Electron_pt", &Electron_pt, &b_Electron_pt);
   fChain->SetBranchAddress("Electron_eta", &Electron_eta, &b_Electron_eta);
   fChain->SetBranchAddress("Electron_jetNDauCharged", &Electron_jetNDauCharged, &b_Electron_jetNDauCharged);
   fChain->SetBranchAddress("Electron_miniPFRelIso_chg", &Electron_miniPFRelIso_chg, &b_Electron_miniPFRelIso_chg);
   fChain->SetBranchAddress("Electron_miniPFRelIso_all", &Electron_miniPFRelIso_all, &b_Electron_miniPFRelIso_all);
   fChain->SetBranchAddress("Electron_jetPtRelv2", &Electron_jetPtRelv2, &b_Electron_jetPtRelv2);
   fChain->SetBranchAddress("Electron_pfRelIso03_all", &Electron_pfRelIso03_all, &b_Electron_pfRelIso03_all);
   fChain->SetBranchAddress("Electron_sip3d", &Electron_sip3d, &b_Electron_sip3d);
   fChain->SetBranchAddress("Electron_dxy", &Electron_dxy, &b_Electron_dxy);
   fChain->SetBranchAddress("Electron_dz", &Electron_dz, &b_Electron_dz);
   fChain->SetBranchAddress("Electron_mvaFall17V2noIso", &Electron_mvaFall17V2noIso, &b_Electron_mvaFall17V2noIso);
   fChain->SetBranchAddress("Electron_lostHits", &Electron_lostHits, &b_Electron_lostHits);
   fChain->SetBranchAddress("Electron_jetIdx", &Electron_jetIdx, &b_Electron_jetIdx);
    
   fChain->SetBranchAddress("nMuon", &nMuon, &b_nMuon);
   fChain->SetBranchAddress("Muon_charge", &Muon_charge, &b_Muon_charge);
   fChain->SetBranchAddress("Muon_mass", &Muon_mass, &b_Muon_mass);
   fChain->SetBranchAddress("Muon_phi", &Muon_phi, &b_Muon_phi);
   fChain->SetBranchAddress("Muon_pt", &Muon_pt, &b_Muon_pt);
   fChain->SetBranchAddress("Muon_eta", &Muon_eta, &b_Muon_eta);
   fChain->SetBranchAddress("Muon_jetNDauCharged", &Muon_jetNDauCharged, &b_Muon_jetNDauCharged);
   fChain->SetBranchAddress("Muon_miniPFRelIso_chg", &Muon_miniPFRelIso_chg, &b_Muon_miniPFRelIso_chg);
   fChain->SetBranchAddress("Muon_miniPFRelIso_all", &Muon_miniPFRelIso_all, &b_Muon_miniPFRelIso_all);
   fChain->SetBranchAddress("Muon_jetPtRelv2", &Muon_jetPtRelv2, &b_Muon_jetPtRelv2);
   fChain->SetBranchAddress("Muon_pfRelIso03_all", &Muon_pfRelIso03_all, &b_Muon_pfRelIso03_all);
   fChain->SetBranchAddress("Muon_sip3d", &Muon_sip3d, &b_Muon_sip3d);
   fChain->SetBranchAddress("Muon_dxy", &Muon_dxy, &b_Muon_dxy);
   fChain->SetBranchAddress("Muon_dz", &Muon_dz, &b_Muon_dz);
   fChain->SetBranchAddress("Muon_segmentComp", &Muon_segmentComp, &b_Muon_segmentComp);
   fChain->SetBranchAddress("Muon_jetIdx", &Muon_jetIdx, &b_Muon_jetIdx);
   fChain->SetBranchAddress("Muon_mediumId", &Muon_mediumId, &b_Muon_mediumId);
    
   fChain->SetBranchAddress("nTau", &nTau, &b_nTau);
   fChain->SetBranchAddress("Tau_charge", &Tau_charge, &b_Tau_charge);
   fChain->SetBranchAddress("Tau_pt", &Tau_pt, &b_Tau_pt);
   fChain->SetBranchAddress("Tau_eta", &Tau_eta, &b_Tau_eta);
   fChain->SetBranchAddress("Tau_phi", &Tau_phi, &b_Tau_phi);
   fChain->SetBranchAddress("Tau_mass", &Tau_mass, &b_Tau_mass);
   fChain->SetBranchAddress("Tau_genPartFlav", &Tau_genPartFlav, &b_Tau_genPartFlav);
   fChain->SetBranchAddress("Tau_decayMode", &Tau_decayMode, &b_Tau_decayMode);
   fChain->SetBranchAddress("Tau_rawDeepTau2017v2p1VSe", &Tau_rawDeepTau2017v2p1VSe, &b_Tau_rawDeepTau2017v2p1VSe);
   fChain->SetBranchAddress("Tau_rawDeepTau2017v2p1VSmu", &Tau_rawDeepTau2017v2p1VSmu, &b_Tau_rawDeepTau2017v2p1VSmu);
   fChain->SetBranchAddress("Tau_rawDeepTau2017v2p1VSjet", &Tau_rawDeepTau2017v2p1VSjet, &b_Tau_rawDeepTau2017v2p1VSjet);
   fChain->SetBranchAddress("Tau_idDeepTau2017v2p1VSe", &Tau_idDeepTau2017v2p1VSe, &b_Tau_idDeepTau2017v2p1VSe);
   fChain->SetBranchAddress("Tau_idDeepTau2017v2p1VSmu", &Tau_idDeepTau2017v2p1VSmu, &b_Tau_idDeepTau2017v2p1VSmu);
   fChain->SetBranchAddress("Tau_idDeepTau2017v2p1VSjet", &Tau_idDeepTau2017v2p1VSjet, &b_Tau_idDeepTau2017v2p1VSjet);
    
   fChain->SetBranchAddress("nJet", &nJet, &b_nJet);
   fChain->SetBranchAddress("Jet_btagDeepFlavB", &Jet_btagDeepFlavB, &b_Jet_btagDeepFlavB);
    
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
