#define MyAnalysis_cxx

#include "MyAnalysis.h"
#include "PU_reWeighting.h"
#include "lepton_candidate.h"
#include "jet_candidate.h"
#include "event_candidate.h"


void updateProgress(std::atomic<ULong64_t>& progress, float percent, int nThread, int workerID, int nDigit) {

  float digitMin = ((float) nDigit / nThread) * workerID;
  float digitMax = ((float) nDigit / nThread) * (workerID + 1);
  for (int i = 0; i < nDigit; i++) {
    if (i >= digitMin && i < digitMax && i < percent * nDigit) {
      progress = ((1 << i) | progress);
    }
  }
}


void displayProgress(std::atomic<ULong64_t>& progress, std::atomic<ULong64_t>& current, long max, int nDigit) {

  using std::cerr;
  if (max < 500) return;
  if (current % (max / 500) != 0 && current < max - 1) return;
  int barWidth = nDigit;
  cerr << "\x1B[2K"; // Clear line
  cerr << "\x1B[2000D"; // Cursor left
  cerr << '[';
  int bitcounter = 0;
  for (int i = 0; i < barWidth; ++i) { if ((progress >> i) & 1) { cerr << '='; bitcounter++; } else { cerr << ' '; } }
  cerr << ']';
  cerr << " " << Form("%6d/%6d (%4.1f%%)", (int) current, (int) max, 100.0 * current / max);
  cerr.flush();
}


std::stringstream MyAnalysis::Loop(TString fname, TString data, TString dataset, TString year, TString run,
                                   float xs, float lumi, float Nevent, std::atomic<ULong64_t>& progress,
                                   std::atomic<ULong64_t>& counter) {

  std::stringstream summary;
  if (fChain == 0) {
    summary << "TChain is empty.\n";
    return summary;
  }

  auto begin = std::chrono::high_resolution_clock::now();

  std::vector<TString> domains{"Prompt", "FakeTau"}; // Fully prompt, fake e/muon, fake tau.
  if (data == "data"){
    domains[0] = "Data";
  }else if (procname.count(dataset)){
    domains[0] = procname.find(dataset)->second;
  }else{   
    domains[0] = "Others";
  }
  std::vector<TString> charges{"OS", "SS"}; // Same-Sign, Opposite-Sign
  std::vector<TString> channels{"etau", "mutau"};
  std::vector<TString> regions{
    "ll",
    "llB0", //W+Jet
    "llOnZMetl100B0", //DY
    "llBgeq1", //ttbar
    "llJet0",
    "llJet1",
    "llJetgeq2"
  };
  const std::map<TString, std::vector<float>> vars1D = {
    {"lep1Pt",           {0,   25,    40,  100}},
    {"tauPt",            {1,   25,    20,  100}},
    {"TtauPt",           {2,   25,    20,  100}},
    {"lep1Eta",          {3,   25,    0,   2.4}},
    {"tauEta",           {4,   25,    0,   2.4}},
    {"TtauEta",          {5,   25,    0,   2.4}},
    {"njet",             {6,   5,     0,   5}},
    {"nbjet",            {7,   3,     0,   3}},
    {"St",               {8,   25,    60,  200}},
    {"llM",              {9,   25,    20,  120}},
    {"llDr",             {10,  25,    0,   4.5}},
    {"btagSum",          {11,  25,    0,   2.5}},
    {"MET",              {12,  20,    0,   200}},
    {"tM",               {13,  20,    0,   200}},
    {"tauJetPt",         {14,  50,    20,  100}},
    {"tauJetBtag",       {15,  50,    0,   1}},
    {"tauRT",            {16,  6,    -1,  5}}
  };
  const std::map<TString, std::vector<float>> vars2D = {
    {"1ProngTauL",    {0}},
    {"1ProngTauT",    {1}},
    {"3ProngTauL",    {2}},
    {"3ProngTauT",    {3}}
  };

  Double_t tauPtBin[6] = {20, 27, 40, 70, 120, 200};
  Double_t tauJetPtBin[6] = {20, 35, 45, 65, 120, 200};
  Double_t tauEtaBin[3] = {0, 1.5, 2.3};
  Double_t tauJetBtagBin[4] = {0, 0.02, 0.1, 1};
  Double_t tauRTBin[6] = {-1, 0, 1, 2, 3, 5};
  // Creating histograms
  Dim5<TH1F*> Hists1D(Dim5<TH1F*>(domains.size(), Dim4<TH1F*>(charges.size(), Dim3<TH1F*>(channels.size(), Dim2<TH1F*>(regions.size(), Dim1<TH1F*>(vars1D.size()))))));
  Dim5<TH2F*> Hists2D(Dim5<TH2F*>(domains.size(), Dim4<TH2F*>(charges.size(), Dim3<TH2F*>(channels.size(), Dim2<TH2F*>(regions.size(), Dim1<TH2F*>(vars1D.size()))))));
  TH1F *h_test1D;
  TH2F *h_test2D;
  std::stringstream name;
  for (int i = 0; i < (int) domains.size(); ++i) {
    for (int j = 0; j < (int) charges.size(); ++j) {
      for (int k = 0; k < (int) channels.size(); ++k) {
        for (int l = 0; l < (int) regions.size(); ++l) {
          for (auto it = vars1D.cbegin(); it != vars1D.cend(); ++it) {
            name << domains[i] << "_" << charges[j] << "_" << channels[k] << "_" << regions[l] << "_" << it->first << "_" << workerID_; // Adding working ID to avoid mem leak
            if (it->first.Contains("tauPt")){
              h_test1D = new TH1F((name.str()).c_str(), "", 5, tauPtBin);
            }else if (it->first.Contains("tauEta")){
              h_test1D = new TH1F((name.str()).c_str(), "", 2, tauEtaBin);
            }else if (it->first.Contains("tauJetPt")){
              h_test1D = new TH1F((name.str()).c_str(), "", 5, tauJetPtBin);
            }else if (it->first.Contains("tauJetBtag")){
              h_test1D = new TH1F((name.str()).c_str(), "", 3, tauJetBtagBin);
            }else if (it->first.Contains("tauRT")){
              h_test1D = new TH1F((name.str()).c_str(), "", 5, tauRTBin);
            }else{
              h_test1D = new TH1F((name.str()).c_str(), "", it->second.at(1), it->second.at(2), it->second.at(3));
            }
            h_test1D->StatOverflows(kTRUE);
            h_test1D->Sumw2(kTRUE);
            Hists1D[i][j][k][l][it->second.at(0)] = h_test1D;
            name.str("");
          }
          for (auto it = vars2D.cbegin(); it != vars2D.cend(); ++it) {
            name << domains[i] << "_" << charges[j] << "_" << channels[k] << "_" << regions[l] << "_" << it->first << "_" << workerID_; // Adding working ID to avoid mem leak
            if (j==0){
              h_test2D = new TH2F((name.str()).c_str(), "", 5, tauPtBin, 2, tauEtaBin);
            }else{
              h_test2D = new TH2F((name.str()).c_str(), "", 5, tauJetPtBin, 5, tauRTBin);
            }
            h_test2D->StatOverflows(kTRUE);
            h_test2D->Sumw2(kTRUE);
            Hists2D[i][j][k][l][it->second.at(0)] = h_test2D;
            name.str("");
          }
        }
      }
    }
  }

  std::string string_year(year.Data());
  TFile *f_El_RECO = new TFile("data/EGM/RECO/" + year + "egammaEffi_ptAbove20.txt_EGM2D.root");
  TFile *f_El_ID = new TFile("data/EGM/TOPMVASF/v1/MediumCharge/" + year + "egammaEffi.txt_EGM2D.root");
  TFile *f_Mu_RECO = new TFile("data/MUO/RECO/" + year + "Efficiency_muon_generalTracks_trackerMuon.root");
  TFile *f_Mu_ID = new TFile("data/MUO/TOPMVASF/v1/Medium/" + year + "NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt.root");
  // https://github.com/cms-tau-pog/TauIDSFs/tree/master/data
  TFile *f_Ta_ID_e = new TFile("data/TAU/" + year + "TauID_SF_eta_DeepTau2017v2p1VSe.root");
  TFile *f_Ta_ID_mu = new TFile("data/TAU/" + year + "TauID_SF_eta_DeepTau2017v2p1VSmu.root");
  TFile *f_Ta_ID_jet = new TFile("data/TAU/" + year + "TauID_SF_pt_DeepTau2017v2p1VSjet.root");
  TFile *f_Ta_ID_jetFF = new TFile("data/TAU/" + year + "TauID_FF_ptVsEta_DeepTau2017v2p1VSjet.root"); // Depends on charge, channel, region --> maybe remove dependency?
  TFile *f_Ta_ES_jet = new TFile("data/TAU/" + year + "TauES_dm_DeepTau2017v2p1VSjet.root"); // Tau energy scale
  TFile *f_Btag_corr = new TFile("data/BTV/" + year + "BtagCorr.root");
  const TH2F sf_El_RECO = *(TH2F*) f_El_RECO->Get("EGamma_SF2D");
  const TH2F sf_El_ID = *(TH2F*) f_El_ID->Get("EGamma_SF2D");
  const TH2F sf_Mu_RECO = *(TH2F*) f_Mu_RECO->Get("NUM_TrackerMuons_DEN_genTracks");
  const TH2F sf_Mu_ID = *(TH2F*) f_Mu_ID->Get("NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt");
  const TH1F sf_Ta_ID_e = *(TH1F*) f_Ta_ID_e->Get("VVLoose");
  const TH1F sf_Ta_ID_mu = *(TH1F*) f_Ta_ID_mu->Get("Tight");
  const TF1 sf_Ta_ID_jet = *(TF1*) f_Ta_ID_jet->Get("Tight_cent");
  const TH1F sf_Ta_ES_jet = *(TH1F*) f_Ta_ES_jet->Get("tes");
  const TH2F sf_Btag_corr = *(TH2F*) f_Btag_corr->Get("2DBtagShapeCorrection");
  f_El_RECO->Close();
  f_El_ID->Close();
  f_Mu_RECO->Close();
  f_Mu_ID->Close();
  f_Ta_ID_e->Close();
  f_Ta_ID_mu->Close();
  f_Ta_ID_jet->Close();
  // f_Ta_ID_jetFF->Close();
  f_Ta_ES_jet->Close();
  f_Btag_corr->Close();

  std::vector<lepton_candidate*>* TrigObj;
  std::vector<lepton_candidate*>* Leptons;
  std::vector<jet_candidate*>* Jets;
  event_candidate* Event;
  std::vector<int> reg;
  std::vector<float> wgt;
  bool metFilterPass;
  float lep1PtCut = 38;
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
  float weight_Ta_ID_e;
  float weight_Ta_ID_mu;
  float weight_Ta_ID_jet;
  // float weight_Ta_ID_jetFF;
  float weight_Btag_corr; // Correction for btag shape to preserve normalization
  float weight_Event;
  int nAccept = 0;
  PU wPU;

  Long64_t ntr = fChain->GetEntries();
  Long64_t ntrperworker = 1 + ntr / nThread_;
  Long64_t ntrmin = workerID_ * ntrperworker;
  Long64_t ntrmax = (workerID_ + 1) * ntrperworker; // Each worker looks at a subrange of the TChain
  Long64_t ntotal = 0;
  for (Long64_t jentry = ntrmin; jentry < ntrmax; jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    fChain->GetEntry(jentry);
    ntotal++; // Thread-private counter
    {
      std::lock_guard<std::mutex> lock(mtx_); // Locking mutex before accessing atomic variables
      ++counter;
      updateProgress(progress, (float) jentry / ntr, nThread_, workerID_, 32);
      if (!verbose_) displayProgress(progress, counter, ntr, 32);
    }
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
    weight_Ta_ID_e = 1;
    weight_Ta_ID_mu = 1;
    weight_Ta_ID_jet = 1;
    // weight_Ta_ID_jetFF = 1; // Use this if dependency on charge/channel/region removed
    weight_Btag_corr = 1;
    weight_Event = 1;
  
    // MET filters
    if (year == "2017" || year == "2018") {
      if (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter
          && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter
          && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && Flag_BadPFMuonDzFilter)
        metFilterPass = true;
    }
    else if (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter
        && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter
        && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter)
      metFilterPass = true;
    if (!metFilterPass || !myTrig->triggerLogic(dataset)) continue; // Applying general trigger requirement

    // TrigObj selection
    TrigObj = new std::vector<lepton_candidate*>();
    for (UInt_t l = 0; l < nTrigObj; l++) {
      if (l >= 64) break; // Restrict the loop size
      if (TrigObj_id[l]!=11 && TrigObj_id[l]!=13) continue;
      if (TrigObj_id[l]==11 && ((1 << 1) & TrigObj_filterBits[l])) TrigObj->push_back(new lepton_candidate(0, TrigObj_eta[l], TrigObj_phi[l], 0, 0, 0, 0, 0, 0, 0, l, 1, 0, 0));
      if (TrigObj_id[l]==13 && ((1 << 1) & TrigObj_filterBits[l])) TrigObj->push_back(new lepton_candidate(0, TrigObj_eta[l], TrigObj_phi[l], 0, 0, 0, 0, 0, 0, 0, l, 2, 0, 0));
    }
    
    // Lepton selection
    bool TrigMatch;
    Leptons = new std::vector<lepton_candidate*>();
    for (UInt_t l = 0; l < nElectron; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 1) break;

      eleEta = abs(Electron_eta[l] + Electron_deltaEtaSC[l]);
      if (Electron_pt[l] < 20 || abs(Electron_eta[l]) > 2.4 || (eleEta > 1.4442 && eleEta < 1.566)) continue;
      if (Electron_sip3d[l] > 8 || abs(Electron_dxy[l]) > 0.05 || abs(Electron_dz[l]) > 0.1) continue;
      if (Electron_miniPFRelIso_all[l] > 0.4 || (int) Electron_lostHits[l] > 1) continue;
      if (!Electron_convVeto[l] || (int) Electron_tightCharge[l] == 0) continue;
      if (Electron_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_El_RECO = weight_El_RECO * get_factor(&sf_El_RECO, eleEta, Electron_pt[l], "");
        weight_El_ID = weight_El_ID * get_factor(&sf_El_ID, eleEta, Electron_pt[l], "");
      }
      //trigger match
      TrigMatch = false;
      for (int m = 0; m < TrigObj->size(); m++){
          if ((*TrigObj)[m]->flavor_==1 && event_candidate::deltaR(Electron_eta[l], Electron_phi[l], (*TrigObj)[m]->eta_, (*TrigObj)[m]->phi_) < 0.2){
            TrigMatch = true;
            break;
          }
      }
      if (!TrigMatch) continue;
      Leptons->push_back(new lepton_candidate(Electron_pt[l], Electron_eta[l], Electron_phi[l], Electron_dxy[l], Electron_dz[l],
            Electron_charge[l], 0, Electron_topLeptonMVA_v1[l], Electron_topLeptonMVA_v2[l], 0, l, 1,
            data == "mc" ? (int) Electron_genPartFlav[l] : 1, -1));
    }

    for (UInt_t l = 0; l < nMuon; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 1) break;

      if (Muon_pt[l] < 20 || abs(Muon_eta[l]) > 2.4) continue;
      if (!Muon_mediumId[l]) continue;
      if (Muon_sip3d[l] > 8 || abs(Muon_dxy[l]) > 0.05 || abs(Muon_dz[l]) > 0.1) continue;
      if (Muon_miniPFRelIso_all[l] > 0.4) continue;
      if (Muon_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_Mu_RECO = weight_Mu_RECO * get_factor(&sf_Mu_RECO, abs(Muon_eta[l]), Muon_pt[l], "");
        weight_Mu_ID = weight_Mu_ID * get_factor(&sf_Mu_ID, abs(Muon_eta[l]), Muon_pt[l], "");
      }
      //trigger match
      TrigMatch = false;
      for (int m = 0; m < TrigObj->size(); m++){
          if ((*TrigObj)[m]->flavor_==2 && event_candidate::deltaR(Muon_eta[l], Muon_phi[l], (*TrigObj)[m]->eta_, (*TrigObj)[m]->phi_) < 0.2){
            TrigMatch = true;
            break;
          }
      }
      if (!TrigMatch) continue;
      Leptons->push_back(new lepton_candidate(Muon_pt[l], Muon_eta[l], Muon_phi[l], Muon_dxy[l], Muon_dz[l],
        Muon_charge[l], 0, Muon_topLeptonMVA_v1[l], Muon_topLeptonMVA_v2[l], 0, l, 2,
        data == "mc" ? (int) Muon_genPartFlav[l] : 1, -1));
    }

    // Applying flavor-dependent trigger requirement
    if (Leptons->size() != 1 || (*Leptons)[0]->pt_ < lep1PtCut
       || !myTrig->triggerPass((*Leptons)[0]->flavor_-1)) {
      deleteContainter(Leptons);
      deleteContainter(TrigObj);
      continue;
    }

    // Tau selection
    for (UInt_t l = 0; l < nTau; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 2) break;

      tauPt = Tau_pt[l];
      if (data == "mc" && (int) Tau_genPartFlav[l] == 5) tauPt = Tau_pt[l] * sf_Ta_ES_jet.GetBinContent(sf_Ta_ES_jet.GetXaxis()->FindBin(Tau_decayMode[l]));
      if (tauPt < 20 || abs(Tau_eta[l]) > 2.3) continue;
      if (abs(Tau_dxy[l]) > 0.05 || abs(Tau_dz[l]) > 0.1) continue;
      if (Tau_decayMode[l] == 5 || Tau_decayMode[l] == 6) continue;
      if ((int) Tau_idDeepTau2017v2p1VSe[l] < 2 || (int) Tau_idDeepTau2017v2p1VSmu[l] < 8 || (int) Tau_idDeepTau2017v2p1VSjet[l] < 1) continue;

      // Overlap removal
      if (event_candidate::deltaR((*Leptons)[0]->eta_, (*Leptons)[0]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4) continue;

      if (data == "mc") {
        if ((int) Tau_genPartFlav[l] == 5) weight_Ta_ID_jet = weight_Ta_ID_jet * sf_Ta_ID_jet.Eval(tauPt < 140 ? tauPt : 140); // SF measured up to 140GeV
        if ((int) Tau_genPartFlav[l] == 1 || (int) Tau_genPartFlav[l] == 3) weight_Ta_ID_e = weight_Ta_ID_e * sf_Ta_ID_e.GetBinContent(sf_Ta_ID_e.GetXaxis()->FindBin(abs(Tau_eta[l])));
        if ((int) Tau_genPartFlav[l] == 2 || (int) Tau_genPartFlav[l] == 4) weight_Ta_ID_mu = weight_Ta_ID_mu * sf_Ta_ID_mu.GetBinContent(sf_Ta_ID_mu.GetXaxis()->FindBin(abs(Tau_eta[l])));
      }

      Leptons->push_back(new lepton_candidate(tauPt, Tau_eta[l], Tau_phi[l], Tau_dxy[l], Tau_dz[l], Tau_charge[l],
        char_to_int(Tau_idDeepTau2017v2p1VSjet[l]), Tau_rawDeepTau2017v2p1VSjet[l], Tau_jetIdx[l]>=0?Jet_pt_nom[Tau_jetIdx[l]]:tauPt,
        Tau_jetIdx[l]>=0?Jet_btagDeepFlavB[Tau_jetIdx[l]]:0, l, 3, data == "mc" ? (int) Tau_genPartFlav[l] : 5, Tau_decayMode[l]));
    }

    if (Leptons->size() != 2 || abs((*Leptons)[0]->charge_ + (*Leptons)[1]->charge_) > 2) {
      deleteContainter(TrigObj);
      deleteContainter(Leptons);
      continue;
    }
    
    Jets = new std::vector<jet_candidate*>();
    for (UInt_t l = 0; l < nJet; l++) {
      if (l >= 16) break; // Restrict the loop size

      if (Jet_pt_nom[l] < 25 || abs(Jet_eta[l]) > 2.4) continue;
      if ((!((int) Jet_puId[l] & (1 << 1)) && Jet_pt_nom[l] < 50) || !((int)Jet_jetId[l] & (1 << 2))) continue;

      // Overlap removal
      if (event_candidate::deltaR((*Leptons)[0]->eta_, (*Leptons)[0]->phi_, Jet_eta[l], Jet_phi[l]) < 0.4
          || event_candidate::deltaR((*Leptons)[1]->eta_, (*Leptons)[1]->phi_, Jet_eta[l], Jet_phi[l]) < 0.4) continue;
      float JetEnergy;
      TLorentzVector* jet_temp = new TLorentzVector();
      jet_temp->SetPtEtaPhiM(Jet_pt_nom[l], Jet_eta[l], Jet_phi[l], Jet_mass_nom[l]);
      JetEnergy = jet_temp->Energy();
      Jets->push_back(new jet_candidate(Jet_pt_nom[l], Jet_eta[l], Jet_phi[l], JetEnergy, Jet_btagDeepFlavB[l],
        data == "mc" ? Jet_btagSF_deepjet_shape[l] : 1, year, 0));
      delete jet_temp;
    }

    // Reconstruction of heavy particles
    Event = new event_candidate(Leptons, Jets, data == "mc" ? MET_T1Smear_pt : MET_T1_pt, MET_phi, verbose_);

    // MC weights
    if (data == "mc") {
      weight_Lumi = (1000 * xs * lumi * getSign(Generator_weight)) / Nevent; // N.B. Nevent here should be sum of generator weights instead of raw event counts
      weight_PU = wPU.getPUweight(year, int(Pileup_nTrueInt), "nominal");
      weight_L1ECALPreFiring = L1PreFiringWeight_ECAL_Nom;
      weight_L1MuonPreFiring = L1PreFiringWeight_Muon_Nom;
      weight_Btag_corr = get_factor(&sf_Btag_corr, Event->njet(), Event->Ht(), "");
    }

    weight_Event = weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID * weight_Ta_ID_jet * weight_Ta_ID_e * weight_Ta_ID_mu * Event->btagSF() * weight_Btag_corr;

    int rIdx = rInd(regions, "ll");
    reg.push_back(rIdx); // No cuts
    wgt.push_back(weight_Event);
    if (Event->nbjet() == 0){
        rIdx = rInd(regions, "llB0");
        reg.push_back(rIdx);
        wgt.push_back(weight_Event);
        if (Event->OnZ() && Event->MET()->Pt() < 100) { // Z+jets
            rIdx = rInd(regions, "llOnZMetl100B0");
            reg.push_back(rIdx);
            wgt.push_back(weight_Event);
        }
    }else{
      rIdx = rInd(regions, "llBgeq1");
      reg.push_back(rIdx);
      wgt.push_back(weight_Event);
    }
    if (Event->njet() == 0){
      rIdx = rInd(regions, "llJet0");
      reg.push_back(rIdx);
      wgt.push_back(weight_Event);
    }
    if (Event->njet() == 1){
      rIdx = rInd(regions, "llJet1");
      reg.push_back(rIdx);
      wgt.push_back(weight_Event);
    }
    if (Event->njet() >= 2){
      rIdx = rInd(regions, "llJetgeq2");
      reg.push_back(rIdx);
      wgt.push_back(weight_Event);
    }

    int dIdx = 0;
    if (Event->ta1()->truth_>0){
        dIdx = 1;
    }
    if (data == "data"){
        dIdx = 0;
    }
    
    int cIdx = Event->c();
    int chIdx = Event->ch();
    // Filling histograms
    for (int i = 0; i < reg.size(); ++i) {
      float wgt_final = wgt[i];
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "lep1Pt")]->Fill(Event->lep1()->pt_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauPt")]->Fill(Event->ta1()->pt_, wgt_final);
      if (Event->TightTau()) Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "TtauPt")]->Fill(Event->ta1()->pt_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "lep1Eta")]->Fill(abs(Event->lep1()->eta_), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauEta")]->Fill(abs(Event->ta1()->eta_), wgt_final);
      if (Event->TightTau()) Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "TtauEta")]->Fill(abs(Event->ta1()->eta_), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "njet")]->Fill(Event->njet(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "nbjet")]->Fill(Event->nbjet(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "St")]->Fill(Event->St(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "llM")]->Fill(Event->llM(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "llDr")]->Fill(Event->llDr(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "btagSum")]->Fill(Event->btagSum(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "MET")]->Fill(Event->MET()->Pt(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tM")]->Fill(Event->tM(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauJetPt")]->Fill(Event->ta1()->jetpt_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauJetBtag")]->Fill(Event->ta1()->jetbtag_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauRT")]->Fill(Event->ta1()->recoil_/Event->ta1()->pt_, wgt_final);

      if (Event->ta1()->decaymode_<10){
          Hists2D[dIdx][cIdx][chIdx][reg[i]][vInd(vars2D, "1ProngTauL")]->Fill(cIdx==0?Event->ta1()->pt_:Event->ta1()->jetpt_, cIdx==0?abs(Event->ta1()->eta_):Event->ta1()->recoil_/Event->ta1()->pt_, wgt_final);
          if (Event->TightTau()) Hists2D[dIdx][cIdx][chIdx][reg[i]][vInd(vars2D, "1ProngTauT")]->Fill(cIdx==0?Event->ta1()->pt_:Event->ta1()->jetpt_, cIdx==0?abs(Event->ta1()->eta_):Event->ta1()->recoil_/Event->ta1()->pt_, wgt_final);
      }else{
          Hists2D[dIdx][cIdx][chIdx][reg[i]][vInd(vars2D, "3ProngTauL")]->Fill(cIdx==0?Event->ta1()->pt_:Event->ta1()->jetpt_, cIdx==0?abs(Event->ta1()->eta_):Event->ta1()->recoil_/Event->ta1()->pt_, wgt_final);
          if (Event->TightTau()) Hists2D[dIdx][cIdx][chIdx][reg[i]][vInd(vars2D, "3ProngTauT")]->Fill(cIdx==0?Event->ta1()->pt_:Event->ta1()->jetpt_, cIdx==0?abs(Event->ta1()->eta_):Event->ta1()->recoil_/Event->ta1()->pt_, wgt_final);
      }
    }
    
    deleteContainter(TrigObj);
    deleteContainter(Leptons);
    deleteContainter(Jets);
    delete Event;

    nAccept++;
  } // End of event loop

  // Writing output and delete pointers
  TFile file_out (fname, "RECREATE");
  for (int i = 0; i < (int) domains.size(); ++i) {
    for (int j = 0; j < (int) charges.size(); ++j) {
      for (int k = 0; k < (int) channels.size(); ++k) {
        for (int l = 0; l < (int) regions.size(); ++l) {
          for (auto it = vars1D.cbegin(); it != vars1D.cend(); ++it) {
            name << domains[i] << "_" << charges[j] << "_" << channels[k] << "_" << regions[l] << "_" << it->first;
            Hists1D[i][j][k][l][it->second.at(0)]->SetName((name.str()).c_str());
            Hists1D[i][j][k][l][it->second.at(0)]->Write("", TObject::kOverwrite);
            delete Hists1D[i][j][k][l][it->second.at(0)];
            name.str("");
          }
          for (auto it = vars2D.cbegin(); it != vars2D.cend(); ++it) {
            name << domains[i] << "_" << charges[j] << "_" << channels[k] << "_" << regions[l] << "_" << it->first;
            Hists2D[i][j][k][l][it->second.at(0)]->SetName((name.str()).c_str());
            Hists2D[i][j][k][l][it->second.at(0)]->Write("", TObject::kOverwrite);
            delete Hists2D[i][j][k][l][it->second.at(0)];
            name.str("");
          }
        }
      }
    }
  }

  file_out.Close();
  Hists1D.clear();
  Hists2D.clear();

  // Writing summary
  auto end = std::chrono::high_resolution_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
  summary << "Thread " << workerID_ << ": from " << ntotal << " events, " << nAccept << " events are accepted; Time measured: " << ceil(elapsed.count() * 1e-9 * 100) / 100 << " seconds.\n";
  return summary;
}
