#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "PU_reWeighting.h"
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
#include <ctime>
#include <vector>

void displayProgress(long current, long max){
  using std::cerr;
  if (max<500) return;
  if (current%(max/500)!=0 && current<max-1) return;

  int width = 45; // Hope the terminal is at least that wide.
  int barWidth = width - 2;
  cerr << "\x1B[2K"; // Clear line
  cerr << "\x1B[2000D"; // Cursor left
  cerr << '[';
  for(int i=0 ; i<barWidth ; ++i){ if(i<barWidth*current/max){ cerr << '=' ; }else{ cerr << ' ' ; } }
  cerr << ']';
  cerr << " " << Form("%8d/%8d (%5.2f%%)", (int)current, (int)max, 100.0*current/max);
  cerr.flush();
}

int vInd(std::map<TString, std::vector<float>> V, TString name){
  return V.find(name)->second.at(0);
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset, TString year, TString run, float xs, float lumi, float Nevent)
{
  std::vector<TString> charges{"OS", "SS"};//Same-Sign, Opposite-Sign
  std::vector<TString> channels{"ee", "emu", "mumu"};
  std::vector<TString> regions{"ll","llOnZMetg20Jetgeq1","llOffZMetg20B1","llOffZMetg20B2","llStl300","llOnZ","llStg300OffZbtagg1p3","llStg300OffZbtagl1p3","llStg300OffZbtagl1p3Tight"};
  std::vector<int>     unBlind{0,1,0,1,1,1,1,0,0};
  const std::map<TString, std::vector<float>> vars =
    {
        {"llM",              {0,   10,    0,    180}},
        {"llDr",             {1,   10,    0,    4.5}},
        {"lep1Pt",           {2,   10,    25,   225}},
        {"lep2Pt",           {3,   10,    20,   180}},
        {"taPt",             {4,   10,    25,   225}},
        {"jet1Pt",           {5,   10,    30,   230}},
        {"njet",             {6,   6,     0,    6}},
        {"nbjet",            {7,   4,     0,    4}},
        {"MET",              {8,   10,    0,    200}},
        {"subSR",            {9,   18,    0,    18}},
        {"LFVemuM",          {10,  10,    0,    300}},
        {"LFVetaM",          {11,  10,    0,    300}},
        {"LFVmutaM",         {12,  10,    0,    300}},
        {"LFVemuDr",         {13,  10,    0,    4.5}},
        {"LFVetaDr",         {14,  10,    0,    4.5}},
        {"LFVmutaDr",        {15,  10,    0,    4.5}},
        {"LFVePt",           {16,  10,    20,   300}},
        {"LFVmuPt",          {17,  10,    20,   300}},
        {"LFVtaPt",          {18,  10,    20,   300}},
        {"BalepPt",          {19,  10,    20,   180}},
        {"Topmass",          {20,  10,    0,    300}},
        {"Ht",               {21,  10,    0,    300}},
        {"St",               {22,  20,    70,   600}},
        {"btagSum",          {23,  25,    0,    2.5}}
    };
    
  Double_t llMBin[19] = {0, 20, 39, 58.2, 63.2, 68.2, 73.2, 78.2, 83.2, 88.2, 93.2, 95.2, 98.2, 103.2, 108.2, 126, 144, 162, 180};
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

//   TH2F *h_2D_wBtagSF;
//   TH2F *h_2D_woBtagSF;
//   Double_t HtBin[6] = {0, 30, 60, 100, 160, 250};
//   Double_t njetBin[6] = {0, 1, 2, 3, 4, 5};
//   h_2D_wBtagSF = new TH2F("2D_wBtagSF","2D_wBtagSF",5,njetBin,5,HtBin);
//   h_2D_woBtagSF = new TH2F("2D_woBtagSF","2D_woBtagSF",5,njetBin,5,HtBin);

  std::string string_year(year.Data());
  TFile *f_El_RECO = new TFile("data/EGM/RECO/"+year+"egammaEffi_ptAbove20.txt_EGM2D.root");
  TFile *f_El_ID = new TFile("data/EGM/TOPMVASF/v1/MediumCharge/"+year+"egammaEffi.txt_EGM2D.root");
  TFile *f_Mu_RECO = new TFile("data/MUO/RECO/"+year+"Efficiency_muon_generalTracks_trackerMuon.root");
  TFile *f_Mu_ID = new TFile("data/MUO/TOPMVASF/v1/Medium/"+year+"NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt.root");
  TFile *f_Ta_ID_jet = new TFile("data/TAU/"+year+"TauID_SF_pt_DeepTau2017v2p1VSjet.root");//https://github.com/cms-tau-pog/TauIDSFs/tree/master/data
  TFile *f_Ta_ID_e = new TFile("data/TAU/"+year+"TauID_SF_eta_DeepTau2017v2p1VSe.root");
  TFile *f_Ta_ID_mu = new TFile("data/TAU/"+year+"TauID_SF_eta_DeepTau2017v2p1VSmu.root");
  TFile *f_Ta_ES_jet = new TFile("data/TAU/"+year+"TauES_dm_DeepTau2017v2p1VSjet.root");//Tau energy scale
  TFile *f_Btag_corr = new TFile("data/BTV/"+year+"BtagCorr.root");
  auto sf_El_RECO = *(TH2F*)f_El_RECO->Get("EGamma_SF2D");
  auto sf_El_ID = *(TH2F*)f_El_ID->Get("EGamma_SF2D");
  auto sf_Mu_RECO = *(TH2F*)f_Mu_RECO->Get("NUM_TrackerMuons_DEN_genTracks");
  auto sf_Mu_ID = *(TH2F*)f_Mu_ID->Get("NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt");
  auto sf_Ta_ID_jet = *(TF1*)f_Ta_ID_jet->Get("Tight_cent");
  auto sf_Ta_ID_e = *(TH1F*)f_Ta_ID_e->Get("VVLoose");
  auto sf_Ta_ID_mu = *(TH1F*)f_Ta_ID_mu->Get("Tight");
  auto sf_Ta_ES_jet = *(TH1F*)f_Ta_ES_jet->Get("tes");
  auto sf_Btag_corr = *(TH2F*)f_Btag_corr->Get("2DBtagShapeCorrection");
  f_El_RECO->Close();
  f_El_ID->Close();
  f_Mu_RECO->Close();
  f_Mu_ID->Close();
  f_Ta_ID_jet->Close();
  f_Ta_ID_e->Close();
  f_Ta_ID_mu->Close();
  f_Ta_ES_jet->Close();
  f_Btag_corr->Close();
    
  TFile file_out (fname,"RECREATE");
    
  std::vector<lepton_candidate*> *Leptons;
  std::vector<jet_candidate*> *Jets;
  event_candidate *Event;
  std::vector<int> reg;
  std::vector<float> wgt;
  bool metFilterPass;
  float lep1PtCut = 30;
  float eleEta;
  float tauPt;
  float weight_Lumi;
  float weight_PU;
  float weight_L1ECALPreFiring;
  float weight_L1MuonPreFiring;
  float weight_El_RECO;
  float weight_El_ID;
  float weight_Mu_RECO;
  float weight_Mu_ID;
  float weight_Ta_ID_jet;
  float weight_Ta_ID_e;
  float weight_Ta_ID_mu;
  float weight_Btag_corr;//correction for btag shape to preserve normalization 
  float weight_Event;
  int nAccept=0;
  PU wPU;
    
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
    weight_PU = 1;
    weight_L1ECALPreFiring = 1;
    weight_L1MuonPreFiring = 1;
    weight_El_RECO = 1;
    weight_El_ID = 1;
    weight_Mu_RECO = 1;
    weight_Mu_ID = 1;
    weight_Ta_ID_jet = 1;
    weight_Ta_ID_e = 1;
    weight_Ta_ID_mu = 1;
    weight_Btag_corr = 1;
    weight_Event = 1;
      
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
        if (data == "mc") {
            weight_El_RECO = weight_El_RECO * scale_factor(&sf_El_RECO, eleEta, Electron_pt[l],"");
            weight_El_ID = weight_El_ID * scale_factor(&sf_El_ID, eleEta, Electron_pt[l],"");
        }
        Leptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_dz[l],
            Electron_charge[l],Electron_topLeptonMVA_v1[l],Electron_topLeptonMVA_v2[l],0,l,1,data=="mc"?(int)Electron_genPartFlav[l]:1));         
    }
                           
    for (UInt_t l=0;l<nMuon;l++){
        if (l>=16) break;//Restrict the loop size
        if (Muon_pt[l]<20 || abs(Muon_eta[l])>2.4) continue;
        if (Muon_sip3d[l]>15 || (!Muon_mediumId[l])) continue;
        if (Muon_sip3d[l]>8 || abs(Muon_dxy[l])>0.05 || abs(Muon_dz[l])>0.1) continue;
        if (Muon_miniPFRelIso_all[l]>0.4) continue;
        if (Muon_topLeptonMVA_v1[l]<0.64) continue;
        if (data == "mc") {
            weight_Mu_RECO = weight_Mu_RECO * scale_factor(&sf_Mu_RECO, abs(Muon_eta[l]), Muon_pt[l],"");
            weight_Mu_ID = weight_Mu_ID * scale_factor(&sf_Mu_ID, abs(Muon_eta[l]), Muon_pt[l],"");
        }
        Leptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_dz[l],
            Muon_charge[l],Muon_topLeptonMVA_v1[l],Muon_topLeptonMVA_v2[l],0,l,2,data=="mc"?(int)Muon_genPartFlav[l]:1));
    }
                           
    if (Leptons->size()!=2 || ((*Leptons)[0]->pt_<lep1PtCut && (*Leptons)[1]->pt_<lep1PtCut)||
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
        tauPt = Tau_pt[l];
        if (data=="mc" && (int)Tau_genPartFlav[l]==5) tauPt = Tau_pt[l] * sf_Ta_ES_jet.GetBinContent(sf_Ta_ES_jet.GetXaxis()->FindBin(Tau_decayMode[l]));
        if (tauPt<20 || abs(Tau_eta[l])>2.3 || abs(Tau_dxy[l])>0.05 || abs(Tau_dz[l])>0.1) continue;
        if (Tau_decayMode[l]==5 || Tau_decayMode[l]==6) continue;
        //The Loosest possible Deep-Tau Working Point
        if ((int)Tau_idDeepTau2017v2p1VSe[l]<2 || (int)Tau_idDeepTau2017v2p1VSmu[l]<8 || (int)Tau_idDeepTau2017v2p1VSjet[l]<32) continue;
        //Overlap removal
        if (event_candidate::deltaR((*Leptons)[0]->eta_,(*Leptons)[0]->phi_,Tau_eta[l],Tau_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[1]->eta_,(*Leptons)[1]->phi_,Tau_eta[l],Tau_phi[l])<0.4) continue;
        if (data=="mc") {
            if ((int)Tau_genPartFlav[l]==5) weight_Ta_ID_jet = weight_Ta_ID_jet * sf_Ta_ID_jet.Eval(tauPt<140?tauPt:140);//SF measured up to 140GeV
            if ((int)Tau_genPartFlav[l]==1||(int)Tau_genPartFlav[l]==3) weight_Ta_ID_e = weight_Ta_ID_e * sf_Ta_ID_e.GetBinContent(sf_Ta_ID_e.GetXaxis()->FindBin(abs(Tau_eta[l])));
            if ((int)Tau_genPartFlav[l]==2||(int)Tau_genPartFlav[l]==4) weight_Ta_ID_mu = weight_Ta_ID_mu * sf_Ta_ID_mu.GetBinContent(sf_Ta_ID_mu.GetXaxis()->FindBin(abs(Tau_eta[l])));
        }
        Leptons->push_back(new lepton_candidate(tauPt,Tau_eta[l],Tau_phi[l],Tau_dz[l],Tau_charge[l],Tau_rawDeepTau2017v2p1VSjet[l],
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
        if (Jet_pt_nom[l]<25 || abs(Jet_eta[l])>2.4) continue;
        if ((!((int)Jet_puId[l]&(1<<1)) && Jet_pt_nom[l]<50) || !((int)Jet_jetId[l]&(1<<2))) continue;
        //Overlap removal
        if (event_candidate::deltaR((*Leptons)[0]->eta_,(*Leptons)[0]->phi_,Jet_eta[l],Jet_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[1]->eta_,(*Leptons)[1]->phi_,Jet_eta[l],Jet_phi[l])<0.4 ||
            event_candidate::deltaR((*Leptons)[2]->eta_,(*Leptons)[2]->phi_,Jet_eta[l],Jet_phi[l])<0.4) continue;
        float JetEnergy;
        TLorentzVector* jet_temp = new TLorentzVector() ;
        jet_temp->SetPtEtaPhiM(Jet_pt_nom[l],Jet_eta[l],Jet_phi[l],Jet_mass_nom[l]);
        JetEnergy = jet_temp->Energy() ;
        Jets->push_back(new jet_candidate(Jet_pt_nom[l],Jet_eta[l],Jet_phi[l],JetEnergy,Jet_btagDeepFlavB[l],data=="mc"?Jet_btagSF_deepjet_shape[l]:1,year,0));
        //break;//Only look at the leading tau
    }

    Event = new event_candidate(Leptons,Jets,data=="mc"?MET_T1Smear_pt:MET_T1_pt,MET_phi,verbose_);//Reconstruction of heavy particles
    //lumi xs weights
    if (data == "mc") {
    weight_Lumi = (1000*xs*lumi*getSign(Generator_weight))/Nevent;
    weight_PU = wPU.getPUweight(year,int(Pileup_nTrueInt),"nominal");
    weight_L1ECALPreFiring = L1PreFiringWeight_ECAL_Nom;
    weight_L1MuonPreFiring = L1PreFiringWeight_Muon_Nom;
    weight_Btag_corr = scale_factor(&sf_Btag_corr, Event->njet(), Event->Ht(),"");
    }
    weight_Event = weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID * weight_Ta_ID_jet * weight_Ta_ID_e * weight_Ta_ID_mu * Event->btagSF() * weight_Btag_corr;
    // h_2D_woBtagSF->Fill(Event->njet()>4?4:Event->njet(),Event->Ht()>250?249:Event->Ht(),weight_Event);
    // h_2D_wBtagSF->Fill(Event->njet()>4?4:Event->njet(),Event->Ht()>250?249:Event->Ht(),weight_Event*Event->btagSF());

    reg.push_back(0);
    wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[0]);
    if (Event->MET()->Pt()>20&&Event->njet()>0){
        if (Event->OnZ()){
        reg.push_back(1);
        wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[1]);
        }
        else{
            if (Event->nbjet()==1){
                reg.push_back(2);
                wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[2]);
            }
            if (Event->nbjet()==2){
                reg.push_back(3);
                wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[3]);
            }
        }
    }
    if (Event->St()<300){
        reg.push_back(4);
        wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[4]);
    }
    if (Event->OnZ()){
        reg.push_back(5);
        wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[5]);
    }
    if (Event->St()>300&&!Event->OnZ()){
        if (Event->btagSum()>1.3){
            reg.push_back(6);
            wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[6]);
        }
        else{
            reg.push_back(7);
            wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[7]);
            if(Event->SRindex()%2==0?Event->njet()>0:Event->St()>350){
                reg.push_back(8);
                wgt.push_back(data == "mc"?weight_Event:weight_Event*unBlind[8]);
            }
        }
    }
    //Start filling histograms
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llM"), Event->llM(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"llDr"), Event->llDr(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep1Pt"), Event->lep1()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"lep2Pt"), Event->lep2()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"taPt"), Event->ta1()->pt_, wgt);
    if (Event->njet()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"jet1Pt"), Event->jet1()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"njet"), Event->njet(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"nbjet"), Event->nbjet(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"MET"), Event->MET()->Pt(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"subSR"), Event->SRindex(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVemuM")+Event->lfvch(), Event->LFVllM(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVemuDr")+Event->lfvch(), Event->LFVllDr(), wgt);
    if (Event->lfvch()!=2) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVePt"), Event->LFVe()->pt_, wgt);
    if (Event->lfvch()!=1) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVmuPt"), Event->LFVmu()->pt_, wgt);
    if (Event->lfvch()!=0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"LFVtaPt"), Event->LFVta()->pt_, wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"BalepPt"), Event->Balep()->pt_, wgt);
    if (Event->njet()>0) FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"Topmass"), Event->Topmass(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"Ht"), Event->Ht(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"St"), Event->St(), wgt);
    FillD4Hists(Hists, Event->c(), Event->ch(), reg, vInd(vars,"btagSum"), Event->btagSum(), wgt);
    
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

//   h_2D_woBtagSF->Write("",TObject::kOverwrite);
//   h_2D_wBtagSF->Write("",TObject::kOverwrite);
    
  file_out.Close() ;
  Hists.clear();
}