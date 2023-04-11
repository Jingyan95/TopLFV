#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "lepton_candidate.h"
#include "jet_candidate.h"
#include "event_candidate.h"
#include "fastforest.h"
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <time.h>
#include <iostream>
#include <algorithm>
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
  std::vector<TString> regions{"ll","llOnZ","llOffZ"};
  const std::map<TString, std::vector<float>> vars =
     {
       {"llM",              {0,    20,    0,    180}},
       {"llDr",             {1,    20,    0,    4.5}},
       {"lep1Pt",           {2,    20,    20,   220}},
       {"lep2Pt",           {3,    20,    20,   220}},
       {"elMVAv1Prompt",    {4,    50,    0,    1}},
       {"elMVAv1HF",        {5,    50,    0,    1}},
       {"elMVAv1Other",     {6,    50,    0,    1}},
       {"elMVAv2Prompt",    {7,    50,    0,    1}},
       {"elMVAv2HF",        {8,    50,    0,    1}},
       {"elMVAv2Other",     {9,    50,    0,    1}},
       {"elMVAv3Prompt",    {10,   50,    0,    1}},
       {"elMVAv3HF",        {11,   50,    0,    1}},
       {"elMVAv3Other",     {12,   50,    0,    1}},
       {"muMVAv1Prompt",    {13,   50,    0,    1}},
       {"muMVAv1HF",        {14,   50,    0,    1}},
       {"muMVAv1Other",     {15,   50,    0,    1}},
       {"muMVAv2Prompt",    {16,   50,    0,    1}},
       {"muMVAv2HF",        {17,   50,    0,    1}},
       {"muMVAv2Other",     {18,   50,    0,    1}},
       {"muMVAv3Prompt",    {19,   50,    0,    1}},
       {"muMVAv3HF",        {20,   50,    0,    1}},
       {"muMVAv3Other",     {21,   50,    0,    1}},
       {"taMVAv1Had",       {22,   50,    0,    1}},
       {"taMVAv1Fake",      {23,   50,    0,    1}},
       {"taMVAv1Other",     {24,   50,    0,    1}},
       {"taMVAv2Had",       {25,   50,    0,    1}},
       {"taMVAv2Fake",      {26,   50,    0,    1}},
       {"taMVAv2Other",     {27,   50,    0,    1}},
       {"taMVAv3Had",       {28,   50,    0,    1}},
       {"taMVAv3Fake",      {29,   50,    0,    1}},
       {"taMVAv3Other",     {30,   50,    0,    1}}
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

  std::vector<std::string> features_el_v1{"pt", "eta", "jetNDauChargedMVASel", "miniRelIsoCharged", "miniRelIsoNeutral",
      "jetPtRelv2", "jetPtRatio", "pfRelIso03_all", "jetBTag", "sip3d", "dxy", "dz", "mvaFall17V2noIso"};
  std::vector<std::string> features_el_v2{"pt", "eta", "jetNDauChargedMVASel", "miniRelIsoCharged", "miniRelIsoNeutral",
      "jetPtRelv2", "jetPtRatio", "pfRelIso03_all", "jetBTag", "sip3d", "dxy", "dz", "mvaFall17V2noIso", "lostHits"};
  std::vector<std::string> features_mu{"pt", "eta", "jetNDauChargedMVASel", "miniRelIsoCharged", "miniRelIsoNeutral",
      "jetPtRelv2", "jetPtRatio", "pfRelIso03_all", "jetBTag", "sip3d", "dxy", "dz", "segmentComp"};

  const auto fastForest_el_v1 = fastforest::load_txt("input/el_TOPUL16_XGB.weights.txt",features_el_v1);
  const auto fastForest_el_v2 = fastforest::load_txt("input/el_TOPv2UL16_XGB.weights.txt",features_el_v2);
  const auto fastForest_mu_v1 = fastforest::load_txt("input/mu_TOPUL16_XGB.weights.txt",features_mu);
  const auto fastForest_mu_v2 = fastforest::load_txt("input/mu_TOPv2UL16_XGB.weights.txt",features_mu);
    
  TFile file_out (fname,"RECREATE");
    
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
        if (l>=16) break;//Restrict the loop size
        eleEta = Electron_eta[l] + Electron_deltaEtaSC[l];
        if (Electron_pt[l]<20 || eleEta > 2.4 || (eleEta>1.4442 && eleEta<1.566)) continue;
        if (Electron_sip3d[l]>15) continue;
        bool electron_jet = (Electron_jetIdx[l]>=0 && Electron_jetIdx[l]<(int)nJet)?true:false;
        float ptRatio = electron_jet?std::min(1. / (Electron_jetRelIso[l] + 1.), 1.5):1. / (Electron_jetRelIso[l] + 1.);
        float btag = (electron_jet && Jet_btagDeepFlavB[Electron_jetIdx[l]]>=0)?Jet_btagDeepFlavB[Electron_jetIdx[l]]:0;
        float dxy = abs(Electron_dxy[l])>0?log(abs(Electron_dxy[l])):0;
        float dz = abs(Electron_dz[l])>0?log(abs(Electron_dz[l])):0;
        std::vector<float> input_el_v1{Electron_pt[l],abs(Electron_eta[l]),(float)Electron_jetNDauCharged[l],
                                      Electron_miniPFRelIso_chg[l],Electron_miniPFRelIso_all[l]-Electron_miniPFRelIso_chg[l],
                                      Electron_jetPtRelv2[l],ptRatio,btag,Electron_sip3d[l],dxy,dz,Electron_mvaFall17V2noIso[l]};
        std::vector<float> input_el_v2{Electron_pt[l],abs(Electron_eta[l]),(float)Electron_jetNDauCharged[l],
                                      Electron_miniPFRelIso_chg[l],Electron_miniPFRelIso_all[l]-Electron_miniPFRelIso_chg[l],
                                      Electron_jetPtRelv2[l],ptRatio,btag,Electron_sip3d[l],dxy,dz,Electron_mvaFall17V2noIso[l],(float)Electron_lostHits[l]};
        float mva1 = 1./(1. + std::exp(-fastForest_el_v1(input_el_v1.data())));
        float mva2 = 1./(1. + std::exp(-fastForest_el_v2(input_el_v2.data())));
        Leptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],
           Electron_phi[l],Electron_charge[l],mva1,mva2,0,l,1,(int)Electron_genPartFlav[l]));
            
    }
                           
    for (UInt_t l=0;l<nMuon;l++){
        if (l>=16) break;//Restrict the loop size
        if (Muon_pt[l]<20 || Muon_eta[l]>2.4) continue;
        if (Muon_sip3d[l]>15 || (!Muon_mediumId[l])) continue;
        bool muon_jet = (Muon_jetIdx[l]>=0 && Muon_jetIdx[l]<(int)nJet)?true:false;
        float ptRatio = muon_jet?std::min(1. / (Muon_jetRelIso[l] + 1.), 1.5):1. / (Muon_jetRelIso[l] + 1.);
        float btag = (muon_jet && Jet_btagDeepFlavB[Muon_jetIdx[l]]>=0)?Jet_btagDeepFlavB[Muon_jetIdx[l]]:0;
        float dxy = abs(Muon_dxy[l])>0?log(abs(Muon_dxy[l])):0;
        float dz = abs(Muon_dz[l])>0?log(abs(Muon_dz[l])):0;
        std::vector<float> input_mu{Muon_pt[l],abs(Muon_eta[l]),(float)Muon_jetNDauCharged[l],
                                    Muon_miniPFRelIso_chg[l],Muon_miniPFRelIso_all[l]-Muon_miniPFRelIso_chg[l],
                                    Muon_jetPtRelv2[l],ptRatio,btag,Muon_sip3d[l],dxy,dz,Muon_segmentComp[l]};
        float mva1 = 1./(1. + std::exp(-fastForest_mu_v1(input_mu.data())));
        float mva2 = 1./(1. + std::exp(-fastForest_mu_v2(input_mu.data())));
        Leptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],
            Muon_phi[l],Muon_charge[l],mva1,mva2,0,l,2,(int)Muon_genPartFlav[l]));
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

    for (UInt_t l=0;l<nTau;l++){
        if (l>=16) break;//Restrict the loop size
        if (Tau_pt[l]<20 || Tau_eta[l]>2.3) continue;
        if (Tau_decayMode[l]==5 || Tau_decayMode[l]==6) continue;
        //The Loosest possible Deep-Tau Working Point
        if ((int)Tau_idDeepTau2017v2p1VSe[l]<1 || (int)Tau_idDeepTau2017v2p1VSmu[l]<1 || (int)Tau_idDeepTau2017v2p1VSjet[l]<1) continue;
        //Overlap removal
        if (event_candidate::deltaR((*Leptons)[0]->eta_,(*Leptons)[0]->phi_,Tau_eta[l],Tau_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[1]->eta_,(*Leptons)[1]->phi_,Tau_eta[l],Tau_phi[l])<0.4) continue;
        Leptons->push_back(new lepton_candidate(Tau_pt[l],Tau_eta[l],Tau_phi[l],Tau_charge[l],Tau_rawDeepTau2017v2p1VSjet[l],
            Tau_rawDeepTau2017v2p1VSe[l],Tau_rawDeepTau2017v2p1VSmu[l],l,3,(int)Tau_genPartFlav[l]));
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
    if (Event->OnZ()){
       reg.push_back(1);
       wgt.push_back(weight_Lumi);
    }else{
       reg.push_back(2);
       wgt.push_back(weight_Lumi);
    }

    //Start filling histograms
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llM"), Event->llM(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llDr"), Event->llDr(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep1Pt"), Event->lep1()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep2Pt"), Event->lep2()->pt_, wgt);
    if (Event->ch()<2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"elMVAv1Prompt")+Event->el1()->truth_, Event->el1()->mva1_, wgt);
    if (Event->ch()<2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"elMVAv2Prompt")+Event->el1()->truth_, Event->el1()->mva2_, wgt);
    if (Event->ch()<2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"elMVAv3Prompt")+Event->el1()->truth_, Event->el1()->mva3_, wgt);
    if (Event->ch()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVAv1Prompt")+Event->mu1()->truth_, Event->mu1()->mva1_, wgt);
    if (Event->ch()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVAv2Prompt")+Event->mu1()->truth_, Event->mu1()->mva2_, wgt);
    if (Event->ch()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVAv3Prompt")+Event->mu1()->truth_, Event->mu1()->mva3_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taMVAv1Had")+Event->ta1()->truth_, Event->ta1()->mva1_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taMVAv2Had")+Event->ta1()->truth_, Event->ta1()->mva2_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taMVAv3Had")+Event->ta1()->truth_, Event->ta1()->mva3_, wgt);
    
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
