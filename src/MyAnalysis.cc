#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "lepton_candidate.h"
#include "jet_candidate.h"
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
  std::vector<TString> charges{"OS", "SS"};//Same-Sign, Opposite-Sign
  std::vector<TString> channels{"ee", "emu", "mumu"};
  std::vector<TString> regions{"ll","llFakeTau","llHadTau","llOther"};
  const std::map<TString, std::vector<float>> vars =
     {
       {"eleMVA",       {0,    20,    0,    1}},
       {"muMVA",        {1,    20,    0,    1}},
       {"tauMVA",       {2,    20,    0,    1}},
       {"llM",          {3,    20,    0,    180}},
       {"llDr",         {4,    20,    0,    4.5}},
       {"lep1Pt",       {5,    20,    20,   220}},
       {"lep2Pt",       {6,    20,    20,   220}}
  };
    
  Dim4 Hists(Dim4(charges.size(),Dim3(channels.size(),Dim2(regions.size(),Dim1(vars.size())))));
  std::stringstream name;
  TH1F *h_test;

  for (int i=0;i<(int)charges.size();++i){
      for (int j=0;j<(int)channels.size();++j){
          for (int k=0;k<(int)regions.size();++k){
              for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
                  name<<charges[i]<<"_"<<channels[j]<<"_"<<regions[k]<<"_"<<it->first;
                  h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
                  h_test->StatOverflows(kTRUE);
                  h_test->Sumw2(kTRUE);
                  Hists[i][j][k][it->second.at(0)] = h_test;
                  name.str("");
              }
          }
      }
  }
    
  TFile file_out (fname,"RECREATE");
  TTree tree_out("analysis","main analysis") ;
    
  std::vector<lepton_candidate*> *Leptons;
  std::vector<jet_candidate*> *Jets;
  event_candidate *Event;
  std::vector<int> reg;
  std::vector<float> wgt;
  float eleEta;
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
    Jets =  new std::vector<jet_candidate*>();
    for (UInt_t l=0;l<nElectron;l++){
        if (l>=16) continue;//Restrict the loop size
        eleEta = Electron_eta[l] + Electron_deltaEtaSC[l];
        if (Electron_pt[l]<20 || eleEta > 2.4 || (eleEta>1.4442 && eleEta<1.566)) continue;
        if (Electron_sip3d[l]>15) continue;
        Leptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],
                           Electron_phi[l],Electron_charge[l],0,0,0,l,1));
    }
                           
    for (UInt_t l=0;l<nMuon;l++){
        if (l>=16) continue;//Restrict the loop size
        if (Muon_pt[l]<20 || Muon_eta[l]>2.4) continue;
        if (Muon_sip3d[l]>15 || (!Muon_mediumId[l])) continue;
        Leptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],
                           Muon_phi[l],Muon_charge[l],0,0,0,l,2));
    }
                           
    if (Leptons->size()!=2) {
       for (int l=0;l<(int)Leptons->size();l++){
           delete (*Leptons)[l];
       }
       for (int l=0;l<(int)Jets->size();l++){
           delete (*Jets)[l];
       }
       Leptons->clear();
       Leptons->shrink_to_fit();
       delete Leptons;
       Jets->clear();
       Jets->shrink_to_fit();
       delete Jets;
       continue;
    }
    
    int isHadTau = 2;//tau MC truth 1->hadronic tau 0->fake tau(jet) 2->other
    for (UInt_t l=0;l<nTau;l++){
        if (l>=16) continue;//Restrict the loop size
        if (Tau_pt[l]<20 || Tau_eta[l]>2.3) continue;
        if (Tau_decayMode[l]==5 || Tau_decayMode[l]==6) continue;
        //The Loosest possible Deep-Tau Working Point
        if (Tau_idDeepTau2017v2p1VSe[l]<1 || Tau_idDeepTau2017v2p1VSmu[l]<1 || Tau_idDeepTau2017v2p1VSjet[l]<1) continue;
        //Overlap removal
        if (event_candidate::deltaR((*Leptons)[0]->eta_,(*Leptons)[0]->phi_,Tau_eta[l],Tau_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[1]->eta_,(*Leptons)[1]->phi_,Tau_eta[l],Tau_phi[l])<0.4) continue;
        Leptons->push_back(new lepton_candidate(Tau_pt[l],Tau_eta[l],Tau_phi[l],Tau_charge[l],Tau_rawDeepTau2017v2p1VSjet[l],
                                                Tau_rawDeepTau2017v2p1VSe[l],Tau_rawDeepTau2017v2p1VSmu[l],l,3));
        if ((int)Tau_genPartFlav[l]==5) isHadTau = 1;
        if ((int)Tau_genPartFlav[l]==0) isHadTau = 0;
        //break;//Only look at the leading tau
    }
                           
    if (Leptons->size()!=3) {
       for (int l=0;l<(int)Leptons->size();l++){
           delete (*Leptons)[l];
       }
       for (int l=0;l<(int)Jets->size();l++){
           delete (*Jets)[l];
       }
       Leptons->clear();
       Leptons->shrink_to_fit();
       delete Leptons;
       Jets->clear();
       Jets->shrink_to_fit();
       delete Jets;
       continue;
    }
                           
    Event = new event_candidate(Leptons,Jets,verbose_);//Reconstruction of heavy particles
    //lumi xs weights
    if (data == "mc") weight_Lumi = (1000*xs*lumi)/Nevent;
      
    reg.push_back(0);
    wgt.push_back(weight_Lumi);
    reg.push_back(isHadTau+1);
    wgt.push_back(weight_Lumi);

    //Start filling histograms
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"eleMVA"), Event->eleMVA(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVA"), Event->muMVA(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"tauMVA"), Event->tauMVA(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llM"), Event->llM(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llDr"), Event->llDr(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep1Pt"), Event->lep1().Pt(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep2Pt"), Event->lep2().Pt(), wgt);
    
    for (int l=0;l<(int)Leptons->size();l++){
      delete (*Leptons)[l];
    }
    for (int l=0;l<(int)Jets->size();l++){
      delete (*Jets)[l];
    }
      
    Leptons->clear();
    Leptons->shrink_to_fit();
    delete Leptons;
    Jets->clear();
    Jets->shrink_to_fit();
    delete Jets;
    delete Event;
      
    nAccept++;
  } //end of event loop
  cout<<endl<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;

  for (int i=0;i<(int)charges.size();++i){
      for (int j=0;j<(int)channels.size();++j){
          for (int k=0;k<(int)regions.size();++k){
              for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
                  Hists[i][j][k][it->second.at(0)] ->Write("",TObject::kOverwrite);
              }
          }
      }
  }
    
  file_out.Close() ;
  Hists.clear();
}

void MyAnalysis::FillD4Hists(Dim4 H4, int v0, int v1, std::vector<int> v2, int v3, float value, std::vector<float> weight){
  for (int i = 0; i < v2.size(); ++i) {
    H4[v0][v1][v2[i]][v3]->Fill(value, weight[i]);
  }
}
