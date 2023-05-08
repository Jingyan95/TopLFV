#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "lepton_candidate.h"
#include "quark_candidate.h"
#include "event_candidate.h"
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <time.h>
#include <iostream>
#include <cmath>
#include <chrono>
#include "ROOT/TTreeProcessorMT.hxx"

void displayProgress(long current, long max){
  using std::cerr;
  if (max<500) return;
  if (current%(max/500)!=0 && current<max-1) return;

  int width = 52; // Hope the terminal is at least that wide.
  int barWidth = width - 2;
  cerr << "\x1B[2K"; // Clear line
  cerr << "\x1B[2000D"; // Cursor left
  cerr << '[';
  for(int i=0 ; i<barWidth ; ++i){ if(i<barWidth*current/max){ cerr << '=' ; }else{ cerr << ' ' ; } }
  cerr << ']';
  cerr << " " << Form("%8d/%8d (%5.2f%%)", (int)current, (int)max, 100.0*current/max) ;
  cerr.flush();
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset, TString year, TString run, float xs, float lumi, float Nevent)
{
  auto begin = std::chrono::high_resolution_clock::now();
  // ROOT::TThreadedObject<TH1F>* h_test;

  // TH1F* h_ele_pt_max;
  // TH1F* h_mu_pt_max;
  // TH1F* h_ta_pt_max;
  // TH1F* h_jet_pt_max;
  // h_ele_pt_max = new TH1F("ele_pt_max","ele_pt_max",20, 0, 100);
  // h_mu_pt_max = new TH1F("mu_pt_max","mu_pt_max",20, 0, 100);
  // h_ta_pt_max = new TH1F("ta_pt_max","ta_pt_max",20, 0, 100);
  // h_jet_pt_max = new TH1F("jet_pt_max","jet_pt_max",20, 0, 100);

  ROOT::TThreadedObject<TH1F>* h_ele_pt_max;
  ROOT::TThreadedObject<TH1F>* h_mu_pt_max;
  ROOT::TThreadedObject<TH1F>* h_ta_pt_max;
  ROOT::TThreadedObject<TH1F>* h_jet_pt_max;
  h_ele_pt_max = new ROOT::TThreadedObject<TH1F>("ele_pt_max","ele_pt_max",20, 0, 100);
  h_mu_pt_max = new ROOT::TThreadedObject<TH1F>("mu_pt_max","mu_pt_max",20, 0, 100);
  h_ta_pt_max = new ROOT::TThreadedObject<TH1F>("ta_pt_max","ta_pt_max",20, 0, 100);
  h_jet_pt_max = new ROOT::TThreadedObject<TH1F>("jet_pt_max","jet_pt_max",20, 0, 100);
    
  TFile file_out (fname,"RECREATE");

  int nthreads = 1;
  ROOT::EnableImplicitMT(nthreads);

  ROOT::EnableThreadSafety();
    
  ROOT::TTreeProcessorMT tp(*fChain);

  auto myFunction = [&](TTreeReader &myReader) {
      TTreeReaderValue<UInt_t> nElectron(myReader, "nElectron");
      TTreeReaderArray<Float_t> Electron_pt(myReader, "Electron_pt");
      TTreeReaderValue<UInt_t> nMuon(myReader, "nMuon");
      TTreeReaderArray<Float_t> Muon_pt(myReader, "Muon_pt");
      TTreeReaderValue<UInt_t> nTau(myReader, "nTau");
      TTreeReaderArray<Float_t> Tau_pt(myReader, "Tau_pt");
      TTreeReaderValue<UInt_t> nJet(myReader, "nJet");
      TTreeReaderArray<Float_t> Jet_pt(myReader, "Jet_pt");
      auto h_ele = h_ele_pt_max->Get();
      auto h_mu = h_mu_pt_max->Get();
      auto h_ta = h_ta_pt_max->Get();
      auto h_jet = h_jet_pt_max->Get();
      while (myReader.Next()) {    
        float ele_pt_max=0;
        float mu_pt_max=0;
        float ta_pt_max=0;
        float jet_pt_max=0;
        //Electron
        for (UInt_t l=0;l<*nElectron;l++){
            if (l>=64) continue;//Restrict the loop size
            if (Electron_pt[l]>ele_pt_max) ele_pt_max = Electron_pt[l];
        }
        //Muon
        for (UInt_t l=0;l<*nMuon;l++){
            if (l>=64) continue;//Restrict the loop size
            if (Muon_pt[l]>mu_pt_max) mu_pt_max = Muon_pt[l];
        }
        //Tau
        for (UInt_t l=0;l<*nTau;l++){
            if (l>=64) continue;//Restrict the loop size
            if (Tau_pt[l]>ta_pt_max) ta_pt_max = Tau_pt[l];
        }
        //Jet
        for (UInt_t l=0;l<*nJet;l++){
            if (l>=64) continue;//Restrict the loop size
            if (Jet_pt[l]>jet_pt_max) jet_pt_max = Jet_pt[l];
        }
        h_ele->Fill(ele_pt_max);
        h_mu->Fill(mu_pt_max);
        h_ta->Fill(ta_pt_max);
        h_jet->Fill(mu_pt_max);
      } //end of event loop
  };
  // TTreeReader myReader(fChain);
  // myFunction(myReader);
  tp.Process(myFunction);
  // h_ele_pt_max->Write();
  // h_mu_pt_max->Write();
  // h_ta_pt_max->Write();
  // h_jet_pt_max->Write();  
  // delete h_ele_pt_max;
  // delete h_mu_pt_max;
  // delete h_ta_pt_max;
  // delete h_jet_pt_max;
  auto H_ele = h_ele_pt_max->Merge();
  auto H_mu = h_mu_pt_max->Merge();
  auto H_ta = h_ta_pt_max->Merge();
  auto H_jet = h_jet_pt_max->Merge();  
  H_ele->Write();
  H_mu->Write();
  H_ta->Write();
  H_jet->Write();
  file_out.Close() ;
  auto end = std::chrono::high_resolution_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
  printf("Time measured: %.3f seconds.\n", elapsed.count() * 1e-9);
}

