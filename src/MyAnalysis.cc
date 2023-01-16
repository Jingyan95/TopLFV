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
#include <vector>

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

int vInd(std::map<TString, std::vector<float>> V, TString name){
  return V.find(name)->second.at(0);
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset, TString year, TString run, float xs, float lumi, float Nevent)
{
  std::vector<TString> channels{"emu", "etau", "mutau", "All"};
  std::vector<TString> regions{"ll", "llMl150", "llMg150"};
  const std::map<TString, std::vector<float>> vars =
     {
       {"LFVePt",       {0,    10,    0,    200}},
       {"LFVmuPt",      {1,    10,    0,    200}},
       {"LFVtauPt",     {2,    10,    0,    200}},
       {"llM",          {3,    10,    0,    400}},
       {"llDr",         {4,    10,    0,    4.5}}
  };
    
  Dim3 Hists(Dim3(channels.size(),Dim2(regions.size(),Dim1(vars.size()))));
  std::stringstream name;
  TH1F *h_test;

  for (int i=0;i<(int)channels.size();++i){
      for (int j=0;j<(int)regions.size();++j){
          for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
              name<<channels[i]<<"_"<<regions[j]<<"_"<<it->first;
              h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
              h_test->StatOverflows(kTRUE);
              h_test->Sumw2(kTRUE);
              Hists[i][j][it->second.at(0)] = h_test;
              name.str("");
          }
      }
  }
    
  TFile file_out (fname,"RECREATE");
  TTree tree_out("analysis","main analysis") ;
    
  std::vector<lepton_candidate*> *Leptons;
  std::vector<quark_candidate*> *Quarks;
  event_candidate *Event;
  std::vector<int> reg;
  std::vector<float> wgt;
  float weight_Lumi;
  int nAccept=0;
    
  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  Long64_t ntr = fChain->GetEntries ();
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    displayProgress(jentry, ntr) ;

    reg.clear();
    wgt.clear();
    weight_Lumi = 1;
      
    if (verbose_) {
    cout << ".............................................................................................." << endl;
    cout << "event " << jentry << endl;
    }
      
    //Lepton selection
    Leptons = new std::vector<lepton_candidate*>();
    Quarks =  new std::vector<quark_candidate*>();
    for (UInt_t l=0;l<nGenPart;l++){
        if (l>=32) continue;//Restrict the loop size
        if (abs(GenPart_pdgId[l])==11||abs(GenPart_pdgId[l])==13||abs(GenPart_pdgId[l])==15){//Only interested in charged leptons
            if (GenPart_genPartIdxMother[l]==0||abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==6){//Charged leptons from top production || decay
               if (Leptons->size()<2) Leptons->push_back(new lepton_candidate(GenPart_pt[l],GenPart_eta[l],GenPart_phi[l],
                                      GenPart_pdgId[l],GenPart_genPartIdxMother[l],GenPart_pdgId[GenPart_genPartIdxMother[l]]));
            }
        }
        if (abs(GenPart_pdgId[l])>=1&&abs(GenPart_pdgId[l])<=8){//Dummy quark container
            Quarks->push_back(new quark_candidate(GenPart_pt[l],GenPart_eta[l],GenPart_phi[l],GenPart_mass[l],
                                GenPart_pdgId[l],GenPart_genPartIdxMother[l],GenPart_pdgId[GenPart_genPartIdxMother[l]]));
        }
    }
      
    if(Leptons->size()!=2) {
      for (int l=0;l<(int)Leptons->size();l++){
          delete (*Leptons)[l];
      }
      for (int l=0;l<(int)Quarks->size();l++){
          delete (*Quarks)[l];
      }
      Leptons->clear();
      Leptons->shrink_to_fit();
      delete Leptons;
      Quarks->clear();
      Quarks->shrink_to_fit();
      delete Quarks;
      continue;
    }
    Event = new event_candidate(Leptons,Quarks,verbose_);//Reconstruction of heavy particles
    //lumi xs weights
    //if (data == "mc") weight_Lumi = (1000*xs*lumi)/Nevent;
      
    if (Event->ch()>=0){
        reg.push_back(0);
        wgt.push_back(weight_Lumi);
        if (Event->llM()<150){
            reg.push_back(1);
            wgt.push_back(weight_Lumi);
        }else{
            reg.push_back(2);
            wgt.push_back(weight_Lumi);
        }
    }
    //Start filling histograms
    if (Event->ch()!=2) FillD3Hists(Hists, Event->ch(), reg, vInd(vars,"LFVePt"), Event->LFVe().Pt(), wgt);
    if (Event->ch()!=1) FillD3Hists(Hists, Event->ch(), reg, vInd(vars,"LFVmuPt"), Event->LFVmu().Pt(), wgt);
    if (Event->ch()!=0) FillD3Hists(Hists, Event->ch(), reg, vInd(vars,"LFVtauPt"), Event->LFVtau().Pt(), wgt);
    FillD3Hists(Hists, Event->ch(), reg, vInd(vars,"llM"), Event->llM(), wgt);
    FillD3Hists(Hists, Event->ch(), reg, vInd(vars,"llDr"), Event->llDr(), wgt);
    //Filling the inclusive ll` channel
    if (Event->ch()!=2) FillD3Hists(Hists, 3, reg, vInd(vars,"LFVePt"), Event->LFVe().Pt(), wgt);
    if (Event->ch()!=1) FillD3Hists(Hists, 3, reg, vInd(vars,"LFVmuPt"), Event->LFVmu().Pt(), wgt);
    if (Event->ch()!=0) FillD3Hists(Hists, 3, reg, vInd(vars,"LFVtauPt"), Event->LFVtau().Pt(), wgt);
    FillD3Hists(Hists, 3, reg, vInd(vars,"llM"), Event->llM(), wgt);
    FillD3Hists(Hists, 3, reg, vInd(vars,"llDr"), Event->llDr(), wgt);
    
    for (int l=0;l<(int)Leptons->size();l++){
      delete (*Leptons)[l];
    }
    for (int l=0;l<(int)Quarks->size();l++){
      delete (*Quarks)[l];
    }
      
    Leptons->clear();
    Leptons->shrink_to_fit();
    delete Leptons;
    Quarks->clear();
    Quarks->shrink_to_fit();
    delete Quarks;
    delete Event;
      
    nAccept++;
  } //end of event loop
  cout<<endl<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;

  for (int j=0;j<(int)channels.size();++j){
      for (int k=0;k<(int)regions.size();++k){
          for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
              Hists[j][k][it->second.at(0)] ->Write("",TObject::kOverwrite);
          }
      }
  }
    
  file_out.Close() ;
  Hists.clear();
}

void MyAnalysis::FillD3Hists(Dim3 H3, int v0, std::vector<int> v1, int v2, float value, std::vector<float> weight){
  for (int i = 0; i < v1.size(); ++i) {
    H3[v0][v1[i]][v2]->Fill(value, weight[i]);
  }
}
