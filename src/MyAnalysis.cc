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
  std::vector<TString> regions{"ll","llOnZ","llOffZ","llOffZMetg20Jetgeq1","llOffZMetg20B1","llOffZMetg20B2"};
  std::vector<int>     unBlind{0,1,0,0,0,1};
  const std::map<TString, std::vector<float>> vars =
    {
        {"elMVAv1Prompt",    {0,    50,    0,    1}},
        {"elMVAv1HF",        {1,    50,    0,    1}},
        {"elMVAv1Other",     {2,    50,    0,    1}},
        {"elMVAv2Prompt",    {3,    50,    0,    1}},
        {"elMVAv2HF",        {4,    50,    0,    1}},
        {"elMVAv2Other",     {5,    50,    0,    1}},
        {"elMVAv3Prompt",    {6,    50,    0,    1}},
        {"elMVAv3HF",        {7,    50,    0,    1}},
        {"elMVAv3Other",     {8,    50,    0,    1}},
        {"muMVAv1Prompt",    {9,    50,    0,    1}},
        {"muMVAv1HF",        {10,   50,    0,    1}},
        {"muMVAv1Other",     {11,   50,    0,    1}},
        {"muMVAv2Prompt",    {12,   50,    0,    1}},
        {"muMVAv2HF",        {13,   50,    0,    1}},
        {"muMVAv2Other",     {14,   50,    0,    1}},
        {"muMVAv3Prompt",    {15,   50,    0,    1}},
        {"muMVAv3HF",        {16,   50,    0,    1}},
        {"muMVAv3Other",     {17,   50,    0,    1}},
        {"taMVAv1Had",       {18,   50,    0,    1}},
        {"taMVAv1Fake",      {19,   50,    0,    1}},
        {"taMVAv1Other",     {20,   50,    0,    1}},
        {"taMVAv2Had",       {21,   50,    0,    1}},
        {"taMVAv2Fake",      {22,   50,    0,    1}},
        {"taMVAv2Other",     {23,   50,    0,    1}},
        {"taMVAv3Had",       {24,   50,    0,    1}},
        {"taMVAv3Fake",      {25,   50,    0,    1}},
        {"taMVAv3Other",     {26,   50,    0,    1}},
        {"llM",              {27,   10,    0,    180}},
        {"llDr",             {28,   10,    0,    4.5}},
        {"lep1Pt",           {29,   10,   25,    225}},
        {"lep2Pt",           {30,   10,   20,    180}},
        {"taPt",             {31,   10,   20,    220}},
        {"jet1Pt",           {32,   10,   30,    230}},
        {"njet",             {33,    6,    0,    6}},
        {"nbjet",            {34,    4,    0,    4}},
        {"MET",              {35,   10,    0,    200}},
        {"subSR",            {36,    6,    0,    6}},
        {"LFVemuM",          {37,   10,    0,    300}},
        {"LFVetaM",          {38,   10,    0,    300}},
        {"LFVmutaM",         {39,   10,    0,    300}},
        {"LFVemuDr",         {40,   10,    0,    4.5}},
        {"LFVetaDr",         {41,   10,    0,    4.5}},
        {"LFVmutaDr",        {42,   10,    0,    4.5}},
        {"LFVePt",           {43,   10,   20,    300}},
        {"LFVmuPt",          {44,   10,   20,    300}},
        {"LFVtaPt",          {45,   10,   20,    300}},
        {"BalepPt",          {46,   10,   20,    180}},
        {"Topmass",          {47,   10,    0,    300}}
    };
    
  Double_t llMBin[19] = {0, 20, 40, 60, 76.2, 79.2, 82.2, 85.2, 88.2, 91.2, 94.2, 97.2, 100.2, 103.2, 106.2, 120, 140, 160, 180};
  Dim4 Hists(Dim4(charges.size(),Dim3(channels.size(),Dim2(regions.size(),Dim1(vars.size())))));
  std::stringstream name;
  TH1F *h_test;

  for (int i=0;i<(int)charges.size();++i){
      for (int j=0;j<(int)channels.size();++j){
          for (int k=0;k<(int)regions.size();++k){
              for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
                  name<<charges[i]<<"_"<<channels[j]<<"_"<<regions[k]<<"_"<<it->first;
                  if (it->first.Contains("llM") && i==0 && j!=1){
                  h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),18,llMBin);
                  }else{
                  h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
                  }
                  h_test->StatOverflows(kTRUE);
                  h_test->Sumw2(kTRUE);
                  Hists[i][j][k][it->second.at(0)] = h_test;
                  name.str("");
              }
          }
      }
  }
  //Feature list
//   std::vector<std::string> features_el_v1{"pt", "eta", "jetNDauChargedMVASel", "miniRelIsoCharged", "miniRelIsoNeutral",
//       "jetPtRelv2", "jetPtRatio", "pfRelIso03_all", "jetBTag", "sip3d", "dxy", "dz", "mvaFall17V2noIso"};
//   std::vector<std::string> features_el_v2{"pt", "eta", "jetNDauChargedMVASel", "miniRelIsoCharged", "miniRelIsoNeutral",
//       "jetPtRelv2", "jetPtRatio", "pfRelIso03_all", "jetBTag", "sip3d", "dxy", "dz", "mvaFall17V2noIso", "lostHits"};
//   std::vector<std::string> features_mu{"pt", "eta", "jetNDauChargedMVASel", "miniRelIsoCharged", "miniRelIsoNeutral",
//       "jetPtRelv2", "jetPtRatio", "pfRelIso03_all", "jetBTag", "sip3d", "dxy", "dz", "segmentComp"};
  //Load xgboost model
//   std::string string_year(year.Data());
//   const auto fastForest_el_v1 = fastforest::load_txt("input/el_TOPUL"+string_year+"_XGB.weights.txt",features_el_v1);
//   const auto fastForest_el_v2 = fastforest::load_txt("input/el_TOPv2UL"+string_year+"_XGB.weights.txt",features_el_v2);
//   const auto fastForest_mu_v1 = fastforest::load_txt("input/mu_TOPUL"+string_year+"_XGB.weights.txt",features_mu);
//   const auto fastForest_mu_v2 = fastforest::load_txt("input/mu_TOPv2UL"+string_year+"_XGB.weights.txt",features_mu);
    
  TFile file_out (fname,"RECREATE");
    
  std::vector<lepton_candidate*> *Leptons;
  std::vector<jet_candidate*> *Jets;
  event_candidate *Event;
  std::vector<int> reg;
  std::vector<float> wgt;
  bool metFilterPass;
  float lep1PtCut = 25;
  float eleEta;
  float weight_Lumi;
  int nAccept=0;
    
  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  Long64_t ntr = fChain->GetEntries();
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    displayProgress(jentry, ntr) ;
    InitTrigger();
    metFilterPass = false;
    reg.clear();
    wgt.clear();
    weight_Lumi = 1;
      
    if (verbose_) {
    cout << ".............................................................................................." << endl;
    cout << "event " << jentry << endl;
    }
    //MET filters
    if (year == "2017" || year == "2018"){
        if (Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    } else if (Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    if (!metFilterPass || !myTrig->triggerLogic(dataset)) continue;//Applying general trigger requirement 
    //Lepton selection
    Leptons = new std::vector<lepton_candidate*>();
    for (UInt_t l=0;l<nElectron;l++){
        if (l>=16) break;//Restrict the loop size
        eleEta = abs(Electron_eta[l] + Electron_deltaEtaSC[l]);
        if (Electron_pt[l]<20 || abs(Electron_eta[l]) > 2.4 || (eleEta>1.4442 && eleEta<1.566)) continue;
        if (Electron_sip3d[l]>15) continue;
        if (Electron_sip3d[l]>8 || abs(Electron_dxy[l])>0.05 || abs(Electron_dz[l])>0.1) continue;
        if (Electron_miniPFRelIso_all[l]>0.4 || (int)Electron_lostHits[l]>1) continue;
        if (!Electron_convVeto[l] || (int)Electron_tightCharge[l]==0) continue;
        if (Electron_topLeptonMVA_v1[l]<0.64) continue;
        Leptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],
            Electron_charge[l],Electron_topLeptonMVA_v1[l],Electron_topLeptonMVA_v2[l],0,l,1,data=="mc"?(int)Electron_genPartFlav[l]:1));         
    }
                           
    for (UInt_t l=0;l<nMuon;l++){
        if (l>=16) break;//Restrict the loop size
        if (Muon_pt[l]<20 || abs(Muon_eta[l])>2.4) continue;
        if (Muon_sip3d[l]>15 || (!Muon_mediumId[l])) continue;
        if (Muon_sip3d[l]>8 || abs(Muon_dxy[l])>0.05 || abs(Muon_dz[l])>0.1) continue;
        if (Muon_miniPFRelIso_all[l]>0.4) continue;
        if (Muon_topLeptonMVA_v1[l]<0.64) continue;
        Leptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],
            Muon_charge[l],Muon_topLeptonMVA_v1[l],Muon_topLeptonMVA_v2[l],0,l,2,data=="mc"?(int)Muon_genPartFlav[l]:1));
    }
                           
    if (Leptons->size()!=2 || ((*Leptons)[0]->pt_<lep1PtCut && (*Leptons)[0]->pt_<lep1PtCut)||
        !myTrig->triggerPass((*Leptons)[0]->flavor_+(*Leptons)[1]->flavor_-2)) {//Applying flavor-dependent trigger requirement 
        for (int l=0;l<(int)Leptons->size();l++){
            delete (*Leptons)[l];
        }
        Leptons->clear();
        Leptons->shrink_to_fit();
        delete Leptons;
        continue;
    }
    //Tau selection
    for (UInt_t l=0;l<nTau;l++){
        if (l>=16) break;//Restrict the loop size
        if (Tau_pt[l]<20 || abs(Tau_eta[l])>2.3) continue;
        if (Tau_decayMode[l]==5 || Tau_decayMode[l]==6) continue;
        //The Loosest possible Deep-Tau Working Point
        if ((int)Tau_idDeepTau2017v2p1VSe[l]<1 || (int)Tau_idDeepTau2017v2p1VSmu[l]<1 || (int)Tau_idDeepTau2017v2p1VSjet[l]<32) continue;
        //Overlap removal
        if (event_candidate::deltaR((*Leptons)[0]->eta_,(*Leptons)[0]->phi_,Tau_eta[l],Tau_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[1]->eta_,(*Leptons)[1]->phi_,Tau_eta[l],Tau_phi[l])<0.4) continue;
        Leptons->push_back(new lepton_candidate(Tau_pt[l],Tau_eta[l],Tau_phi[l],Tau_charge[l],Tau_rawDeepTau2017v2p1VSjet[l],
            Tau_rawDeepTau2017v2p1VSe[l],Tau_rawDeepTau2017v2p1VSmu[l],l,3,data=="mc"?(int)Tau_genPartFlav[l]:5));
        //break;//Only look at the leading tau
    }
                           
    if (Leptons->size()!=3 || 
        abs((*Leptons)[0]->charge_+(*Leptons)[1]->charge_+(*Leptons)[2]->charge_)>1) {
        for (int l=0;l<(int)Leptons->size();l++){
            delete (*Leptons)[l];
        }
        Leptons->clear();
        Leptons->shrink_to_fit();
        delete Leptons;
        continue;
    }

    Jets =  new std::vector<jet_candidate*>();
    for (UInt_t l=0;l<nJet;l++){
        if (l>=16) break;//Restrict the loop size
        if (Jet_pt[l]<30 || abs(Jet_eta[l])>2.4) continue;
        if ((!((int)Jet_puId[l]&(1<<1)) && Jet_pt[l]<50) || !((int)Jet_jetId[l]&(1<<2))) continue;
        //Overlap removal
        if (event_candidate::deltaR((*Leptons)[0]->eta_,(*Leptons)[0]->phi_,Jet_eta[l],Jet_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[1]->eta_,(*Leptons)[1]->phi_,Jet_eta[l],Jet_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[2]->eta_,(*Leptons)[2]->phi_,Jet_eta[l],Jet_phi[l])<0.4) continue;
        float JetEnergy;
        TLorentzVector* jet_temp = new TLorentzVector() ;
        jet_temp->SetPtEtaPhiM(Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l]);
        JetEnergy = jet_temp->Energy() ;
        Jets->push_back(new jet_candidate(Jet_pt[l],Jet_eta[l],Jet_phi[l],JetEnergy,Jet_btagDeepFlavB[l],year,0));
        //break;//Only look at the leading tau
    }

    Event = new event_candidate(Leptons,Jets,MET_pt,MET_phi,verbose_);//Reconstruction of heavy particles
    //lumi xs weights
    if (data == "mc") weight_Lumi = (1000*xs*lumi)/Nevent;
      
    reg.push_back(0);
    wgt.push_back(data == "mc"?weight_Lumi:weight_Lumi*unBlind[0]);
    if (Event->OnZ()){
        reg.push_back(1);
        wgt.push_back(data == "mc"?weight_Lumi:weight_Lumi*unBlind[1]);
    }else{
        reg.push_back(2);
        wgt.push_back(data == "mc"?weight_Lumi:weight_Lumi*unBlind[2]);
        if (Event->njet()>0&&Event->MET()->Pt()>20){
            reg.push_back(3);
            wgt.push_back(data == "mc"?weight_Lumi:weight_Lumi*unBlind[3]);
            if (Event->nbjet()==1){
                reg.push_back(4);
                wgt.push_back(data == "mc"?weight_Lumi:weight_Lumi*unBlind[4]);
            }
            if (Event->nbjet()==2){
                reg.push_back(5);
                wgt.push_back(data == "mc"?weight_Lumi:weight_Lumi*unBlind[5]);
            }
        }
    }
    //Start filling histograms
    if (Event->ch()<2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"elMVAv1Prompt")+Event->el1()->truth_, Event->el1()->mva1_, wgt);
    if (Event->ch()<2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"elMVAv2Prompt")+Event->el1()->truth_, Event->el1()->mva2_, wgt);
    if (Event->ch()<2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"elMVAv3Prompt")+Event->el1()->truth_, Event->el1()->mva3_, wgt);
    if (Event->ch()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVAv1Prompt")+Event->mu1()->truth_, Event->mu1()->mva1_, wgt);
    if (Event->ch()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVAv2Prompt")+Event->mu1()->truth_, Event->mu1()->mva2_, wgt);
    if (Event->ch()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"muMVAv3Prompt")+Event->mu1()->truth_, Event->mu1()->mva3_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taMVAv1Had")+Event->ta1()->truth_, Event->ta1()->mva1_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taMVAv2Had")+Event->ta1()->truth_, Event->ta1()->mva2_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taMVAv3Had")+Event->ta1()->truth_, Event->ta1()->mva3_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llM"), Event->llM(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llDr"), Event->llDr(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep1Pt"), Event->lep1()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep2Pt"), Event->lep2()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taPt"), Event->ta1()->pt_, wgt);
    if (Event->njet()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"jet1Pt"), Event->jet1()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"njet"), Event->njet(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"nbjet"), Event->nbjet(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"MET"), Event->MET()->Pt(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"subSR"), Event->LFVllM()>150?1+2*Event->lfvch():2*Event->lfvch(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVemuM")+Event->lfvch(), Event->LFVllM(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVemuDr")+Event->lfvch(), Event->LFVllDr(), wgt);
    if (Event->lfvch()!=2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVePt"), Event->LFVe()->pt_, wgt);
    if (Event->lfvch()!=1) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVmuPt"), Event->LFVmu()->pt_, wgt);
    if (Event->lfvch()!=0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVtaPt"), Event->LFVta()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"BalepPt"), Event->Balep()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"Topmass"), Event->Topmass(), wgt);
    
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