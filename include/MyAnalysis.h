#ifndef MyAnalysis_h
#define MyAnalysis_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TF1.h>
#include <thread>
#include <mutex>
#include "trigger.h"

using namespace std;
class MyAnalysis {
public :
  TTree          *fChain; //!pointer to the analyzed TTree or TChain
  Int_t          fCurrent; //!current Tree number in a TChain
  TString        year_;
  TString        data_;
  TString        run_;
  bool           verbose_;
  trigger        *myTrig;
  int            nThread_;
  int            workerID_;

  // Fixed size dimensions of array or collections stored in the TTree if any.

  // Branch information: https://swertz.web.cern.ch/swertz/TMG/TopNano/TopNanoV9/doc_topNanoV9-1-1_MC18UL.html#CaloMET
  // Declaration of leaf types
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
  Float_t         Electron_jetRelIso[16];
  Float_t         Electron_jetPtRelv2[16];
  Float_t         Electron_pfRelIso03_all[16];
  Float_t         Electron_sip3d[16];
  Float_t         Electron_dxy[16];
  Float_t         Electron_dz[16];
  Float_t         Electron_mvaFall17V2noIso[16];
  UChar_t         Electron_lostHits[16];
  Int_t           Electron_jetIdx[16];
  UChar_t         Electron_genPartFlav[16];
  Float_t         Electron_topLeptonMVA_v1[16];
  Float_t         Electron_topLeptonMVA_v2[16];
  Bool_t          Electron_convVeto[16];
  Int_t           Electron_tightCharge[16];

  UInt_t          nMuon;
  Int_t           Muon_charge[16];
  Float_t         Muon_mass[16];
  Float_t         Muon_phi[16];
  Float_t         Muon_pt[16];
  Float_t         Muon_eta[16];
  UChar_t         Muon_jetNDauCharged[16];
  Float_t         Muon_miniPFRelIso_chg[16];
  Float_t         Muon_miniPFRelIso_all[16];
  Float_t         Muon_jetRelIso[16];
  Float_t         Muon_jetPtRelv2[16];
  Float_t         Muon_pfRelIso03_all[16];
  Float_t         Muon_sip3d[16];
  Float_t         Muon_dxy[16];
  Float_t         Muon_dz[16];
  Float_t         Muon_segmentComp[16];
  Int_t           Muon_jetIdx[16];
  Bool_t          Muon_mediumId[16];
  UChar_t         Muon_genPartFlav[16];
  Float_t         Muon_topLeptonMVA_v1[16];
  Float_t         Muon_topLeptonMVA_v2[16];

  Bool_t          Flag_goodVertices; 
  Bool_t          Flag_globalSuperTightHalo2016Filter;
  Bool_t          Flag_HBHENoiseFilter;
  Bool_t          Flag_HBHENoiseIsoFilter;
  Bool_t          Flag_EcalDeadCellTriggerPrimitiveFilter;
  Bool_t          Flag_BadPFMuonFilter;
  Bool_t          Flag_eeBadScFilter;
  Bool_t          Flag_ecalBadCalibFilter; 
  Bool_t          Flag_BadPFMuonDzFilter;

  Bool_t          HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL;//2016 APV
  Bool_t          HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL;//2016 APV, 2018
  Bool_t          HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ;//2016, 2017, 2018
  Bool_t          HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;//2016, 2017 

  Bool_t          HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;//2017, 2018
  Bool_t          HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;//2016 APV, 2016
  Bool_t          HLT_DoubleEle33_CaloIdL_MW;//2016APV, 2016, 2017, 2018
  Bool_t          HLT_DoubleEle33_CaloIdL_GsfTrkIdVL;//2016APV, 2016 

  Bool_t          HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL;//2016 APV
  Bool_t          HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;//2016 APV
  Bool_t          HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;//2016
  Bool_t          HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;//2016
  Bool_t          HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8;//2017
  Bool_t          HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8;//2018

  Bool_t          HLT_Ele27_WPTight_Gsf;//2016 APV, 2016
  Bool_t          HLT_Ele32_WPTight_Gsf;//2018
  Bool_t          HLT_Ele35_WPTight_Gsf;//2017
  Bool_t          HLT_IsoMu24;//2016 APV, 2016, 2018
  Bool_t          HLT_IsoTkMu24;//2016 APV, 2016
  Bool_t          HLT_IsoMu27;//2017

  Bool_t          HLT_PFMET300;//2016APV 2016
  Bool_t          HLT_MET200;//2016APV 2016
  Bool_t          HLT_PFHT300_PFMET110;//2016APV 2016
  Bool_t          HLT_PFMET170_HBHECleaned;//2016APV 2016
  Bool_t          HLT_PFMET120_PFMHT120_IDTight;//All
  Bool_t          HLT_PFMETNoMu120_PFMHTNoMu120_IDTight;//All

  Bool_t          HLT_PFMET200_HBHECleaned;//2017 2018
  Bool_t          HLT_PFMET200_HBHE_BeamHaloCleaned;//2017 2018
  Bool_t          HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned;//2017 2018
  Bool_t          HLT_PFMET120_PFMHT120_IDTight_PFHT60;//2017 2018
  Bool_t          HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60;//2017 2018
  Bool_t          HLT_PFHT500_PFMET100_PFMHT100_IDTight;//2017 2018
  Bool_t          HLT_PFHT700_PFMET85_PFMHT85_IDTight;//2017 2018
  Bool_t          HLT_PFHT800_PFMET75_PFMHT75_IDTight;//2017 2018

  Float_t         Generator_weight;//MC generator weight
  Float_t         Pileup_nTrueInt;
  Float_t         L1PreFiringWeight_ECAL_Nom;
  Float_t         L1PreFiringWeight_Muon_Nom;

  // List of branches  
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
  TBranch         *b_Electron_jetRelIso;
  TBranch         *b_Electron_jetPtRelv2;
  TBranch         *b_Electron_pfRelIso03_all;
  TBranch         *b_Electron_sip3d;
  TBranch         *b_Electron_dxy;
  TBranch         *b_Electron_dz;
  TBranch         *b_Electron_mvaFall17V2noIso;
  TBranch         *b_Electron_lostHits;
  TBranch         *b_Electron_jetIdx;
  TBranch         *b_Electron_genPartFlav;
  TBranch         *b_Electron_topLeptonMVA_v1;
  TBranch         *b_Electron_topLeptonMVA_v2;
  TBranch         *b_Electron_convVeto;
  TBranch         *b_Electron_tightCharge;

  TBranch         *b_nMuon;
  TBranch         *b_Muon_charge;
  TBranch         *b_Muon_mass;
  TBranch         *b_Muon_phi;
  TBranch         *b_Muon_pt;
  TBranch         *b_Muon_eta;
  TBranch         *b_Muon_jetNDauCharged;
  TBranch         *b_Muon_miniPFRelIso_chg;
  TBranch         *b_Muon_miniPFRelIso_all;
  TBranch         *b_Muon_jetRelIso;
  TBranch         *b_Muon_jetPtRelv2;
  TBranch         *b_Muon_pfRelIso03_all;
  TBranch         *b_Muon_sip3d;
  TBranch         *b_Muon_dxy;
  TBranch         *b_Muon_dz;
  TBranch         *b_Muon_segmentComp;
  TBranch         *b_Muon_jetIdx;
  TBranch         *b_Muon_mediumId;
  TBranch         *b_Muon_genPartFlav;
  TBranch         *b_Muon_topLeptonMVA_v1;
  TBranch         *b_Muon_topLeptonMVA_v2;

  TBranch         *b_Flag_goodVertices; 
  TBranch         *b_Flag_globalSuperTightHalo2016Filter;
  TBranch         *b_Flag_HBHENoiseFilter;
  TBranch         *b_Flag_HBHENoiseIsoFilter;
  TBranch         *b_Flag_EcalDeadCellTriggerPrimitiveFilter;
  TBranch         *b_Flag_BadPFMuonFilter;
  TBranch         *b_Flag_eeBadScFilter;
  TBranch         *b_Flag_ecalBadCalibFilter; 
  TBranch         *b_Flag_BadPFMuonDzFilter;

  TBranch         *b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL;//2016 APV
  TBranch         *b_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL;//2016 APV, 2018
  TBranch         *b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ;//2016, 2017, 2018
  TBranch         *b_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;//2016, 2017

  TBranch         *b_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;//2017, 2018
  TBranch         *b_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;//2016 APV, 2016
  TBranch         *b_HLT_DoubleEle33_CaloIdL_MW;//2016APV, 2016, 2017, 2018
  TBranch         *b_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL;//2016APV, 2016 

  TBranch         *b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL;//2016 APV
  TBranch         *b_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;//2016 APV
  TBranch         *b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;//2016
  TBranch         *b_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;//2016
  TBranch         *b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8;//2017
  TBranch         *b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8;//2018

  TBranch         *b_HLT_Ele27_WPTight_Gsf;//2016 APV, 2016
  TBranch         *b_HLT_Ele32_WPTight_Gsf;//2018
  TBranch         *b_HLT_Ele35_WPTight_Gsf;//2017
  TBranch         *b_HLT_IsoMu24;//2016 APV, 2016, 2018
  TBranch         *b_HLT_IsoTkMu24;//2016 APV, 2016
  TBranch         *b_HLT_IsoMu27;//2017

  TBranch         *b_HLT_PFMET300;//2016APV 2016
  TBranch         *b_HLT_MET200;//2016APV 2016
  TBranch         *b_HLT_PFHT300_PFMET110;//2016APV 2016
  TBranch         *b_HLT_PFMET170_HBHECleaned;//2016APV 2016
  TBranch         *b_HLT_PFMET120_PFMHT120_IDTight;//All
  TBranch         *b_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight;//All

  TBranch         *b_HLT_PFMET200_HBHECleaned;//2017 2018
  TBranch         *b_HLT_PFMET200_HBHE_BeamHaloCleaned;//2017 2018
  TBranch         *b_HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned;//2017 2018
  TBranch         *b_HLT_PFMET120_PFMHT120_IDTight_PFHT60;//2017 2018
  TBranch         *b_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60;//2017 2018
  TBranch         *b_HLT_PFHT500_PFMET100_PFMHT100_IDTight;//2017 2018
  TBranch         *b_HLT_PFHT700_PFMET85_PFMHT85_IDTight;//2017 2018
  TBranch         *b_HLT_PFHT800_PFMET75_PFMHT75_IDTight;//2017 2018

  TBranch         *b_Generator_weight;
  TBranch         *b_Pileup_nTrueInt;
  TBranch         *b_L1PreFiringWeight_ECAL_Nom;
  TBranch         *b_L1PreFiringWeight_Muon_Nom;

  MyAnalysis(TTree *tree=0, TString year="", TString data="", TString run="", int nThread=8, int workerID=0, bool verbose_=false);
  virtual ~MyAnalysis();
  virtual Int_t    Cut(Long64_t entry);
  virtual void     GetEntry(Long64_t entry);
  virtual Long64_t LoadTree(Long64_t entry);
  virtual void     Init(TTree *tree);
  virtual void     InitTrigger();
  virtual std::stringstream Loop(TString, TString, TString, TString, TString, Float_t,Float_t,Float_t,std::atomic<ULong64_t>&,std::atomic<ULong64_t>&);
  virtual Bool_t   Notify();
  virtual void     Show(Long64_t entry = -1);

  typedef std::vector<TH1F*> Dim1;
  typedef std::vector<Dim1> Dim2;
  typedef std::vector<Dim2> Dim3;
  typedef std::vector<Dim3> Dim4;

  typedef std::vector<TH2F*> D2im1;
  typedef std::vector<D2im1> D2im2;
  typedef std::vector<D2im2> D2im3;
  typedef std::vector<D2im3> D2im4;
  //Utility functions
  int vInd(std::map<TString, std::vector<float>> V, TString name);
  int getSign(const double& x);
  float scale_factor(const TH2F* h, float X, float Y, TString uncert);

private:
  static std::mutex mtx_;//Standard mutex to achieve synchronization
};

#endif

#ifdef MyAnalysis_cxx
MyAnalysis::MyAnalysis(TTree *tree, TString year, TString data, TString run, int nThread, int workerID, bool verbose) : fChain(0), year_(year), data_(data), run_(run), myTrig(new trigger(year_,data_)), nThread_(nThread), workerID_(workerID), verbose_(verbose) {
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

MyAnalysis::~MyAnalysis() {
  if (!fChain) return;
  delete fChain->GetCurrentFile();
  delete myTrig;
}

void MyAnalysis::GetEntry(Long64_t entry) {
  fChain->GetEntry(entry);
}

Long64_t MyAnalysis::LoadTree(Long64_t entry) {
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

void MyAnalysis::Init(TTree *tree) {
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
  fChain->SetBranchAddress("Electron_jetRelIso", &Electron_jetRelIso, &b_Electron_jetRelIso);
  fChain->SetBranchAddress("Electron_jetPtRelv2", &Electron_jetPtRelv2, &b_Electron_jetPtRelv2);
  fChain->SetBranchAddress("Electron_pfRelIso03_all", &Electron_pfRelIso03_all, &b_Electron_pfRelIso03_all);
  fChain->SetBranchAddress("Electron_sip3d", &Electron_sip3d, &b_Electron_sip3d);
  fChain->SetBranchAddress("Electron_dxy", &Electron_dxy, &b_Electron_dxy);
  fChain->SetBranchAddress("Electron_dz", &Electron_dz, &b_Electron_dz);
  fChain->SetBranchAddress("Electron_mvaFall17V2noIso", &Electron_mvaFall17V2noIso, &b_Electron_mvaFall17V2noIso);
  fChain->SetBranchAddress("Electron_lostHits", &Electron_lostHits, &b_Electron_lostHits);
  fChain->SetBranchAddress("Electron_jetIdx", &Electron_jetIdx, &b_Electron_jetIdx);
  if (data_ == "mc") fChain->SetBranchAddress("Electron_genPartFlav", &Electron_genPartFlav, &b_Electron_genPartFlav);
  fChain->SetBranchAddress("Electron_topLeptonMVA_v1", &Electron_topLeptonMVA_v1, &b_Electron_topLeptonMVA_v1);
  fChain->SetBranchAddress("Electron_topLeptonMVA_v2", &Electron_topLeptonMVA_v2, &b_Electron_topLeptonMVA_v2);
  fChain->SetBranchAddress("Electron_convVeto", &Electron_convVeto, &b_Electron_convVeto);
  fChain->SetBranchAddress("Electron_tightCharge", &Electron_tightCharge, &b_Electron_tightCharge);

  fChain->SetBranchAddress("nMuon", &nMuon, &b_nMuon);
  fChain->SetBranchAddress("Muon_charge", &Muon_charge, &b_Muon_charge);
  fChain->SetBranchAddress("Muon_mass", &Muon_mass, &b_Muon_mass);
  fChain->SetBranchAddress("Muon_phi", &Muon_phi, &b_Muon_phi);
  fChain->SetBranchAddress("Muon_pt", &Muon_pt, &b_Muon_pt);
  fChain->SetBranchAddress("Muon_eta", &Muon_eta, &b_Muon_eta);
  fChain->SetBranchAddress("Muon_jetNDauCharged", &Muon_jetNDauCharged, &b_Muon_jetNDauCharged);
  fChain->SetBranchAddress("Muon_miniPFRelIso_chg", &Muon_miniPFRelIso_chg, &b_Muon_miniPFRelIso_chg);
  fChain->SetBranchAddress("Muon_miniPFRelIso_all", &Muon_miniPFRelIso_all, &b_Muon_miniPFRelIso_all);
  fChain->SetBranchAddress("Muon_jetRelIso", &Muon_jetRelIso, &b_Muon_jetRelIso);
  fChain->SetBranchAddress("Muon_jetPtRelv2", &Muon_jetPtRelv2, &b_Muon_jetPtRelv2);
  fChain->SetBranchAddress("Muon_pfRelIso03_all", &Muon_pfRelIso03_all, &b_Muon_pfRelIso03_all);
  fChain->SetBranchAddress("Muon_sip3d", &Muon_sip3d, &b_Muon_sip3d);
  fChain->SetBranchAddress("Muon_dxy", &Muon_dxy, &b_Muon_dxy);
  fChain->SetBranchAddress("Muon_dz", &Muon_dz, &b_Muon_dz);
  fChain->SetBranchAddress("Muon_segmentComp", &Muon_segmentComp, &b_Muon_segmentComp);
  fChain->SetBranchAddress("Muon_jetIdx", &Muon_jetIdx, &b_Muon_jetIdx);
  fChain->SetBranchAddress("Muon_mediumId", &Muon_mediumId, &b_Muon_mediumId);
  if (data_ == "mc") fChain->SetBranchAddress("Muon_genPartFlav", &Muon_genPartFlav, &b_Muon_genPartFlav);
  fChain->SetBranchAddress("Muon_topLeptonMVA_v1", &Muon_topLeptonMVA_v1, &b_Muon_topLeptonMVA_v1);
  fChain->SetBranchAddress("Muon_topLeptonMVA_v2", &Muon_topLeptonMVA_v2, &b_Muon_topLeptonMVA_v2);

  fChain->SetBranchAddress("Flag_goodVertices", &Flag_goodVertices, &b_Flag_goodVertices);
  fChain->SetBranchAddress("Flag_globalSuperTightHalo2016Filter", &Flag_globalSuperTightHalo2016Filter, &b_Flag_globalSuperTightHalo2016Filter);
  fChain->SetBranchAddress("Flag_HBHENoiseFilter", &Flag_HBHENoiseFilter, &b_Flag_HBHENoiseFilter);
  fChain->SetBranchAddress("Flag_HBHENoiseIsoFilter", &Flag_HBHENoiseIsoFilter, &b_Flag_HBHENoiseIsoFilter);
  fChain->SetBranchAddress("Flag_EcalDeadCellTriggerPrimitiveFilter", &Flag_EcalDeadCellTriggerPrimitiveFilter, &b_Flag_EcalDeadCellTriggerPrimitiveFilter);
  fChain->SetBranchAddress("Flag_BadPFMuonFilter", &Flag_BadPFMuonFilter, &b_Flag_BadPFMuonFilter);
  fChain->SetBranchAddress("Flag_eeBadScFilter", &Flag_eeBadScFilter, &b_Flag_eeBadScFilter);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("Flag_ecalBadCalibFilter", &Flag_ecalBadCalibFilter, &b_Flag_ecalBadCalibFilter);
  fChain->SetBranchAddress("Flag_BadPFMuonDzFilter", &Flag_BadPFMuonDzFilter, &b_Flag_BadPFMuonDzFilter);

  if (year_ == "2016APV") fChain->SetBranchAddress("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL", &HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL, &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL);
  if (year_ == "2016APV" || year_ == "2018") fChain->SetBranchAddress("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL", &HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL, &b_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL);
  if (year_ != "2016APV") fChain->SetBranchAddress("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", &HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ);
  if (year_ == "2016" || year_ == "2017") fChain->SetBranchAddress("HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", &HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ, &b_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ);

  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", &HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL, &b_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL);
  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", &HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ, &b_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ);
  fChain->SetBranchAddress("HLT_DoubleEle33_CaloIdL_MW", &HLT_DoubleEle33_CaloIdL_MW, &b_HLT_DoubleEle33_CaloIdL_MW);
  if ((year_ == "2016APV" || year_ == "2016") && run_!="H") fChain->SetBranchAddress("HLT_DoubleEle33_CaloIdL_GsfTrkIdVL", &HLT_DoubleEle33_CaloIdL_GsfTrkIdVL, &b_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL);

  if (year_ == "2016APV") fChain->SetBranchAddress("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL", &HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL, &b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL);
  if (year_ == "2016APV") fChain->SetBranchAddress("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL", &HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL, &b_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL);
  if (year_ == "2016") fChain->SetBranchAddress("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", &HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ, &b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ);
  if (year_ == "2016") fChain->SetBranchAddress("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", &HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ, &b_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ);
  if (year_ == "2017") fChain->SetBranchAddress("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8", &HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8, &b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8);
  if (year_ == "2018") fChain->SetBranchAddress("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8", &HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8, &b_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8);

  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_Ele27_WPTight_Gsf", &HLT_Ele27_WPTight_Gsf, &b_HLT_Ele27_WPTight_Gsf);
  if (year_ == "2018") fChain->SetBranchAddress("HLT_Ele32_WPTight_Gsf", &HLT_Ele32_WPTight_Gsf, &b_HLT_Ele32_WPTight_Gsf);
  if (year_ == "2017") fChain->SetBranchAddress("HLT_Ele35_WPTight_Gsf", &HLT_Ele35_WPTight_Gsf, &b_HLT_Ele35_WPTight_Gsf);
  if (year_ != "2017") fChain->SetBranchAddress("HLT_IsoMu24", &HLT_IsoMu24, &b_HLT_IsoMu24);
  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_IsoTkMu24", &HLT_IsoTkMu24, &b_HLT_IsoTkMu24);
  if (year_ == "2017") fChain->SetBranchAddress("HLT_IsoMu27", &HLT_IsoMu27, &b_HLT_IsoMu27);

  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_PFMET300", &HLT_PFMET300, &b_HLT_PFMET300);
  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_MET200", &HLT_MET200, &b_HLT_MET200);
  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_PFHT300_PFMET110", &HLT_PFHT300_PFMET110, &b_HLT_PFHT300_PFMET110);
  if (year_ == "2016APV" || year_ == "2016") fChain->SetBranchAddress("HLT_PFMET170_HBHECleaned", &HLT_PFMET170_HBHECleaned, &b_HLT_PFMET170_HBHECleaned);
  fChain->SetBranchAddress("HLT_PFMET120_PFMHT120_IDTight", &HLT_PFMET120_PFMHT120_IDTight, &b_HLT_PFMET120_PFMHT120_IDTight);
  fChain->SetBranchAddress("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight", &HLT_PFMETNoMu120_PFMHTNoMu120_IDTight, &b_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFMET200_HBHECleaned", &HLT_PFMET200_HBHECleaned, &b_HLT_PFMET200_HBHECleaned);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFMET200_HBHE_BeamHaloCleaned", &HLT_PFMET200_HBHE_BeamHaloCleaned, &b_HLT_PFMET200_HBHE_BeamHaloCleaned);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned", &HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned, &b_HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFMET120_PFMHT120_IDTight_PFHT60", &HLT_PFMET120_PFMHT120_IDTight_PFHT60, &b_HLT_PFMET120_PFMHT120_IDTight_PFHT60);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60", &HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60, &b_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFHT500_PFMET100_PFMHT100_IDTight", &HLT_PFHT500_PFMET100_PFMHT100_IDTight, &b_HLT_PFHT500_PFMET100_PFMHT100_IDTight);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFHT700_PFMET85_PFMHT85_IDTight", &HLT_PFHT700_PFMET85_PFMHT85_IDTight, &b_HLT_PFHT700_PFMET85_PFMHT85_IDTight);
  if (year_ == "2017" || year_ == "2018") fChain->SetBranchAddress("HLT_PFHT800_PFMET75_PFMHT75_IDTight", &HLT_PFHT800_PFMET75_PFMHT75_IDTight, &b_HLT_PFHT800_PFMET75_PFMHT75_IDTight);

  if (data_ == "mc") fChain->SetBranchAddress("Generator_weight", &Generator_weight, &b_Generator_weight);
  if (data_ == "mc") fChain->SetBranchAddress("Pileup_nTrueInt", &Pileup_nTrueInt, &b_Pileup_nTrueInt);
  fChain->SetBranchAddress("L1PreFiringWeight_ECAL_Nom", &L1PreFiringWeight_ECAL_Nom, &b_L1PreFiringWeight_ECAL_Nom);
  fChain->SetBranchAddress("L1PreFiringWeight_Muon_Nom", &L1PreFiringWeight_Muon_Nom, &b_L1PreFiringWeight_Muon_Nom);

  Notify();
}

void MyAnalysis::InitTrigger() {
  myTrig->Init(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,
    HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,HLT_DoubleEle33_CaloIdL_MW,HLT_DoubleEle33_CaloIdL_GsfTrkIdVL,
    HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8,
    HLT_Ele27_WPTight_Gsf,HLT_Ele32_WPTight_Gsf,HLT_Ele35_WPTight_Gsf,HLT_IsoMu24,HLT_IsoTkMu24,HLT_IsoMu27,HLT_PFMET300,HLT_MET200,HLT_PFHT300_PFMET110,HLT_PFMET170_HBHECleaned,
    HLT_PFMET120_PFMHT120_IDTight,HLT_PFMETNoMu120_PFMHTNoMu120_IDTight,HLT_PFMET200_HBHECleaned,HLT_PFMET200_HBHE_BeamHaloCleaned,HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned,
    HLT_PFMET120_PFMHT120_IDTight_PFHT60,HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60,HLT_PFHT500_PFMET100_PFMHT100_IDTight,HLT_PFHT700_PFMET85_PFMHT85_IDTight,HLT_PFHT800_PFMET75_PFMHT75_IDTight);
}

int MyAnalysis::vInd(std::map<TString, std::vector<float>> V, TString name) {
  return V.find(name)->second.at(0);
}

int MyAnalysis::getSign(const double& x) {
  if (x > 0) return 1;
  if (x < 0) return -1;
  return 0;
}

template <class T>
void deleteContainter(std::vector<T>* v) {
  for (int l=0; l<(int)v->size(); l++) {
    delete (*v)[l];
  }
  v->clear();
  v->shrink_to_fit();
  delete v;
}

float MyAnalysis::scale_factor(const TH2F* h, float X, float Y, TString uncert) {
  int NbinsX = h->GetXaxis()->GetNbins();
  int NbinsY = h->GetYaxis()->GetNbins();
  float x_min = h->GetXaxis()->GetBinLowEdge(1);
  float x_max = h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
  float y_min = h->GetYaxis()->GetBinLowEdge(1);
  float y_max = h->GetYaxis()->GetBinLowEdge(NbinsY)+h->GetYaxis()->GetBinWidth(NbinsY);
  const TAxis *Xaxis = h->GetXaxis();
  const TAxis *Yaxis = h->GetYaxis();
  Int_t binx = 1;
  Int_t biny = 1;
  if (x_min < X && X < x_max) binx = Xaxis->FindBin(X);
  else binx = (X <= x_min) ? 1 : NbinsX ;
  if (y_min < Y && Y < y_max) biny = Yaxis->FindBin(Y);
  else biny = (Y <= y_min) ? 1 : NbinsY ;
  if (uncert == "up") return (h->GetBinContent(binx, biny)+h->GetBinError(binx, biny));
  else if (uncert == "down") return (h->GetBinContent(binx, biny)-h->GetBinError(binx, biny));
  else return h->GetBinContent(binx, biny);
}

Bool_t MyAnalysis::Notify() {
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.
  return kTRUE;
}

void MyAnalysis::Show(Long64_t entry) {
  // Print contents of entry.
  // If entry is not specified, prInt_t current entry
  if (!fChain) return;
  fChain->Show(entry);
}

Int_t MyAnalysis::Cut(Long64_t entry) {
  // This function may be called from Loop.
  // returns  1 if entry is accepted.
  // returns -1 otherwise.
  return 1;
}

#endif // #ifdef MyAnalysis_cxx
