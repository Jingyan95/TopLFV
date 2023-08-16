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
  for (int i = 0; i < barWidth; ++i) { if (((progress >> i) & 1)) { cerr << '='; bitcounter++; } else { cerr << ' '; } }
  cerr << ']';
  cerr << " " << Form("%6d/%6d (%4.1f%%)", (int) current, (int) max, 100.0 * current / max);
  cerr.flush();
}

std::stringstream MyAnalysis::Loop(TString fname, TString data, TString dataset, TString year, TString run, float xs, float lumi, float Nevent, std::atomic<ULong64_t>& progress, std::atomic<ULong64_t>& counter) {

  std::stringstream summary;
  if (fChain == 0) { summary << "TChain is empty.\n"; return summary; }
  auto begin = std::chrono::high_resolution_clock::now();
  std::vector<TString> charges{"OS", "SS"}; // Same-Sign, Opposite-Sign
  std::vector<TString> channels{"ee", "emu", "mumu"};
  std::vector<TString> regions{"ll", "llOnZMetg20Jetgeq1", "llOffZMetg20B1", "llOffZMetg20B2", "llStl300", "llOnZ", "llbtagg1p3", "llStg300OffZbtagl1p3", "llStg300OffZbtagl1p3Tight"};
  std::vector<int> unBlind{0, 1, 0, 1, 1, 1, 1, 0, 0};
  const std::map<TString, std::vector<float>> vars =
  {
    {"llM",              {0,   10,     0,   180}},
    {"llDr",             {1,   10,     0,   4.5}},
    {"lep1Pt",           {2,   10,    30,   230}},
    {"lep2Pt",           {3,   10,    20,   180}},
    {"taPt",             {4,   10,    20,   220}},
    {"taDxy",            {5,   16,  -0.1,   0.1}},
    {"taDz",             {6,   16,  -0.2,   0.2}},
    {"jet1Pt",           {7,   10,    25,   225}},
    {"njet",             {8,    6,     0,     6}},
    {"nbjet",            {9,    4,     0,     4}},
    {"MET",              {10,  10,     0,   200}},
    {"subSR",            {11,  18,     0,    18}},
    {"LFVemuM",          {12,  10,     0,   300}},
    {"LFVetaM",          {13,  10,     0,   300}},
    {"LFVmutaM",         {14,  10,     0,   300}},
    {"LFVemuDr",         {15,  10,     0,   4.5}},
    {"LFVetaDr",         {16,  10,     0,   4.5}},
    {"LFVmutaDr",        {17,  10,     0,   4.5}},
    {"LFVePt",           {18,  10,    20,   300}},
    {"LFVmuPt",          {19,  10,    20,   300}},
    {"LFVtaPt",          {20,  10,    20,   300}},
    {"BalepPt",          {21,  10,    20,   180}},
    {"Topmass",          {22,  10,     0,   300}},
    {"Ht",               {23,  10,     0,   300}},
    {"St",               {24,  20,    70,   600}},
    {"btagSum",          {25,  25,     0,   2.5}}
  };

  Double_t llMBin[19] = {0, 20, 39, 58.2, 63.2, 68.2, 73.2, 78.2, 83.2, 88.2, 93.2, 95.2, 98.2, 103.2, 108.2, 126, 144, 162, 180};
  Dim4 Hists(Dim4(charges.size(),Dim3(channels.size(),Dim2(regions.size(),Dim1(vars.size())))));
  std::stringstream name;
  TH1F *h_test;

  for (int i = 0; i < (int) charges.size(); ++i) {
    for (int j = 0; j < (int) channels.size(); ++j) {
      for (int k = 0; k < (int) regions.size(); ++k) {
        for (auto it = vars.cbegin(); it != vars.cend(); ++it) {
          name << charges[i] << "_" << channels[j] << "_" << regions[k] << "_" << it->first << "_" << workerID_; // adding working ID to avoid mem leak
          if (it->first.Contains("llM") && i == 0 && j != 1) {
            h_test = new TH1F((name.str()).c_str(), "", 18, llMBin);
          } else {
            h_test = new TH1F((name.str()).c_str(), "", it->second.at(1), it->second.at(2), it->second.at(3));
          }
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          Hists[i][j][k][it->second.at(0)] = h_test;
          name.str("");
        }
      }
    }
  }

  // TH2F *h_2D_wBtagSF;
  // TH2F *h_2D_woBtagSF;
  // Double_t HtBin[6] = {0, 30, 60, 100, 160, 250};
  // Double_t njetBin[6] = {0, 1, 2, 3, 4, 5};
  // h_2D_wBtagSF = new TH2F("2D_wBtagSF", "2D_wBtagSF", 5, njetBin, 5, HtBin);
  // h_2D_woBtagSF = new TH2F("2D_woBtagSF", "2D_woBtagSF", 5, njetBin, 5, HtBin);

  std::string string_year(year.Data());
  TFile *f_El_RECO = new TFile("data/EGM/RECO/" + year + "egammaEffi_ptAbove20.txt_EGM2D.root");
  TFile *f_El_ID = new TFile("data/EGM/TOPMVASF/v1/MediumCharge/" + year + "egammaEffi.txt_EGM2D.root");
  TFile *f_Mu_RECO = new TFile("data/MUO/RECO/" + year + "Efficiency_muon_generalTracks_trackerMuon.root");
  TFile *f_Mu_ID = new TFile("data/MUO/TOPMVASF/v1/Medium/" + year + "NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt.root");
  TFile *f_Ta_ID_jet = new TFile("data/TAU/" + year + "TauID_SF_pt_DeepTau2017v2p1VSjet.root"); // https://github.com/cms-tau-pog/TauIDSFs/tree/master/data
  TFile *f_Ta_ID_e = new TFile("data/TAU/" + year + "TauID_SF_eta_DeepTau2017v2p1VSe.root");
  TFile *f_Ta_ID_mu = new TFile("data/TAU/" + year + "TauID_SF_eta_DeepTau2017v2p1VSmu.root");
  TFile *f_Ta_ES_jet = new TFile("data/TAU/" + year + "TauES_dm_DeepTau2017v2p1VSjet.root"); // Tau energy scale
  TFile *f_Btag_corr = new TFile("data/BTV/" + year + "BtagCorr.root");
  const auto sf_El_RECO = *(TH2F*)f_El_RECO->Get("EGamma_SF2D");
  const auto sf_El_ID = *(TH2F*)f_El_ID->Get("EGamma_SF2D");
  const auto sf_Mu_RECO = *(TH2F*)f_Mu_RECO->Get("NUM_TrackerMuons_DEN_genTracks");
  const auto sf_Mu_ID = *(TH2F*)f_Mu_ID->Get("NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt");
  const auto sf_Ta_ID_jet = *(TF1*)f_Ta_ID_jet->Get("Tight_cent");
  const auto sf_Ta_ID_e = *(TH1F*)f_Ta_ID_e->Get("VVLoose");
  const auto sf_Ta_ID_mu = *(TH1F*)f_Ta_ID_mu->Get("Tight");
  const auto sf_Ta_ES_jet = *(TH1F*)f_Ta_ES_jet->Get("tes");
  const auto sf_Btag_corr = *(TH2F*)f_Btag_corr->Get("2DBtagShapeCorrection");
  f_El_RECO->Close();
  f_El_ID->Close();
  f_Mu_RECO->Close();
  f_Mu_ID->Close();
  f_Ta_ID_jet->Close();
  f_Ta_ID_e->Close();
  f_Ta_ID_mu->Close();
  f_Ta_ES_jet->Close();
  f_Btag_corr->Close();

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
  float weight_Btag_corr; // correction for btag shape to preserve normalization 
  float weight_Event;
  int nAccept=0;
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
    ntotal++; // thread-private counter
    std::lock_guard<std::mutex> lock(mtx_); // locking mutex before accessing atomic variables
    ++counter; // shared-counter 
    updateProgress(progress, (float) jentry / ntr, nThread_, workerID_, 32);
    if (!verbose_) displayProgress(progress, counter, ntr, 32);
    mtx_.unlock(); // releasing mutex
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

    // MET filters
    if (year == "2017" || year == "2018") {
      if (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter
          &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter
          && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && Flag_BadPFMuonDzFilter)
        metFilterPass = true;
    } else if (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter
        && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter
        && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter)
      metFilterPass = true;
    if (!metFilterPass || !myTrig->triggerLogic(dataset)) continue; // Applying general trigger requirement

    //Lepton selection
    Leptons = new std::vector<lepton_candidate*>();
    for (UInt_t l = 0; l < nElectron; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 2) break;

      eleEta = abs(Electron_eta[l] + Electron_deltaEtaSC[l]);
      if (Electron_pt[l] < 20 || abs(Electron_eta[l]) > 2.4 || (eleEta > 1.4442 && eleEta < 1.566)) continue;
      // if (Electron_sip3d[l] > 15) continue;
      if (Electron_sip3d[l] > 8 || abs(Electron_dxy[l]) > 0.05 || abs(Electron_dz[l]) > 0.1) continue;
      if (Electron_miniPFRelIso_all[l] > 0.4 || (int) Electron_lostHits[l] > 1) continue;
      if (!Electron_convVeto[l] || (int) Electron_tightCharge[l] == 0) continue;
      if (Electron_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_El_RECO = weight_El_RECO * scale_factor(&sf_El_RECO, eleEta, Electron_pt[l], "");
        weight_El_ID = weight_El_ID * scale_factor(&sf_El_ID, eleEta, Electron_pt[l], "");
      }

      Leptons->push_back(new lepton_candidate(Electron_pt[l], Electron_eta[l], Electron_phi[l], Electron_dxy[l], Electron_dz[l],
        Electron_charge[l], Electron_topLeptonMVA_v1[l], Electron_topLeptonMVA_v2[l], 0, l, 1,
        data == "mc" ? (int) Electron_genPartFlav[l] : 1));
    }

    for (UInt_t l = 0; l < nMuon; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 2) break;

      if (Muon_pt[l] < 20 || abs(Muon_eta[l]) > 2.4) continue;
      // if (Muon_sip3d[l] > 15) continue;
      if (!Muon_mediumId[l]) continue;
      if (Muon_sip3d[l] > 8 || abs(Muon_dxy[l]) > 0.05 || abs(Muon_dz[l]) > 0.1) continue;
      if (Muon_miniPFRelIso_all[l] > 0.4) continue;
      if (Muon_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_Mu_RECO = weight_Mu_RECO * scale_factor(&sf_Mu_RECO, abs(Muon_eta[l]), Muon_pt[l], "");
        weight_Mu_ID = weight_Mu_ID * scale_factor(&sf_Mu_ID, abs(Muon_eta[l]), Muon_pt[l], "");
      }

      Leptons->push_back(new lepton_candidate(Muon_pt[l], Muon_eta[l], Muon_phi[l], Muon_dxy[l], Muon_dz[l],
        Muon_charge[l], Muon_topLeptonMVA_v1[l], Muon_topLeptonMVA_v2[l], 0, l, 2,
        data == "mc" ? (int) Muon_genPartFlav[l] : 1));
    }

    if (Leptons->size() != 2 || ((*Leptons)[0]->pt_ < lep1PtCut && (*Leptons)[1]->pt_ < lep1PtCut)
        || !myTrig->triggerPass((*Leptons)[0]->flavor_ + (*Leptons)[1]->flavor_-2)) { // Applying flavor-dependent trigger requirement
      deleteContainter(Leptons);
      continue;
    }

    // Tau selection
    for (UInt_t l = 0; l < nTau; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 3) break;

      tauPt = Tau_pt[l];
      if (data == "mc" && (int) Tau_genPartFlav[l] == 5) tauPt = Tau_pt[l] * sf_Ta_ES_jet.GetBinContent(sf_Ta_ES_jet.GetXaxis()->FindBin(Tau_decayMode[l]));
      if (tauPt < 20 || abs(Tau_eta[l]) > 2.3) continue;
      if (abs(Tau_dxy[l]) > 0.05 || abs(Tau_dz[l]) > 0.1) continue;
      if (Tau_decayMode[l] == 5 || Tau_decayMode[l] == 6) continue;
      if ((int) Tau_idDeepTau2017v2p1VSe[l] < 2 || (int) Tau_idDeepTau2017v2p1VSmu[l] < 8 || (int) Tau_idDeepTau2017v2p1VSjet[l] < 32) continue;
      // Overlap removal
      if (event_candidate::deltaR((*Leptons)[0]->eta_, (*Leptons)[0]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4
          || event_candidate::deltaR((*Leptons)[1]->eta_, (*Leptons)[1]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4) continue;

      if (data == "mc") {
        if ((int) Tau_genPartFlav[l] == 5) weight_Ta_ID_jet = weight_Ta_ID_jet * sf_Ta_ID_jet.Eval(tauPt < 140 ? tauPt : 140); // SF measured up to 140GeV
        if ((int) Tau_genPartFlav[l] == 1 || (int) Tau_genPartFlav[l] == 3) weight_Ta_ID_e = weight_Ta_ID_e * sf_Ta_ID_e.GetBinContent(sf_Ta_ID_e.GetXaxis()->FindBin(abs(Tau_eta[l])));
        if ((int) Tau_genPartFlav[l] == 2 || (int) Tau_genPartFlav[l] == 4) weight_Ta_ID_mu = weight_Ta_ID_mu * sf_Ta_ID_mu.GetBinContent(sf_Ta_ID_mu.GetXaxis()->FindBin(abs(Tau_eta[l])));
      }

      Leptons->push_back(new lepton_candidate(tauPt, Tau_eta[l], Tau_phi[l], Tau_dxy[l], Tau_dz[l],
        Tau_charge[l], Tau_rawDeepTau2017v2p1VSjet[l], Tau_rawDeepTau2017v2p1VSe[l], Tau_rawDeepTau2017v2p1VSmu[l], l, 3,
        data == "mc" ? (int) Tau_genPartFlav[l] : 5));
    }

    if (Leptons->size() != 3
        || abs((*Leptons)[0]->charge_ + (*Leptons)[1]->charge_ + (*Leptons)[2]->charge_) > 1) {
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
          || event_candidate::deltaR((*Leptons)[1]->eta_, (*Leptons)[1]->phi_, Jet_eta[l], Jet_phi[l]) < 0.4
          || event_candidate::deltaR((*Leptons)[2]->eta_, (*Leptons)[2]->phi_, Jet_eta[l], Jet_phi[l]) < 0.4) continue;
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
      weight_Btag_corr = scale_factor(&sf_Btag_corr, Event->njet(), Event->Ht(), "");
    }
    weight_Event = weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID * weight_Ta_ID_jet * weight_Ta_ID_e * weight_Ta_ID_mu * Event->btagSF() * weight_Btag_corr;
    // h_2D_woBtagSF->Fill(Event->njet() > 4 ? 4 : Event->njet(), Event->Ht() > 250 ? 249 : Event->Ht(), weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID * weight_Ta_ID_jet * weight_Ta_ID_e * weight_Ta_ID_mu);
    // h_2D_wBtagSF->Fill(Event->njet() > 4 ? 4 : Event->njet(), Event->Ht() > 250 ? 249 : Event->Ht(), weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID * weight_Ta_ID_jet * weight_Ta_ID_e * weight_Ta_ID_mu * Event->btagSF());

    reg.push_back(0);
    wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[0]);
    if (Event->MET()->Pt() > 20 && Event->njet() > 0) {
      if (Event->OnZ()) { // Z+jets CR
        reg.push_back(1);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[1]);
      }
      else {
        if (Event->nbjet() == 1) { // SR
          reg.push_back(2);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[2]);
        }
        if (Event->nbjet() == 2) { // ttbar+jets CR
          reg.push_back(3);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[3]);
        }
      }
    }
    if (Event->St() < 300) { // Generic signal-free region
      reg.push_back(4);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[4]);
    }
    if (Event->OnZ()) { // Z+jets CR
      reg.push_back(5);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[5]);
    }
    if (Event->btagSum() > 1.3) { // ttbar+jets CR
      reg.push_back(6);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[6]);
    }
    if (Event->St() > 300 && !Event->OnZ() && Event->btagSum() < 1.3) { // New SR
      reg.push_back(7);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[7]);
      if(Event->SRindex() % 2 == 0 ? Event->njet() > 0 : Event->St() > 500) { // New SR (Tight)
        reg.push_back(8);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[8]);
      }
    }
    // Filling histograms
    for (int i = 0; i < reg.size(); ++i) {
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "llM")]->Fill(Event->llM(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "llDr")]->Fill(Event->llDr(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "lep1Pt")]->Fill(Event->lep1()->pt_, wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "lep2Pt")]->Fill(Event->lep2()->pt_, wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "taPt")]->Fill(Event->ta1()->pt_, wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "taDxy")]->Fill(Event->ta1()->dxy_, wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "taDz")]->Fill(Event->ta1()->dz_, wgt[i]);
      if (Event->njet() > 0) Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "jet1Pt")]->Fill(Event->jet1()->pt_, wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "njet")]->Fill(Event->njet(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "nbjet")]->Fill(Event->nbjet(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "MET")]->Fill(Event->MET()->Pt(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "subSR")]->Fill(Event->SRindex(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "LFVemuM")+Event->lfvch()]->Fill(Event->LFVllM(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "LFVemuDr")+Event->lfvch()]->Fill(Event->LFVllDr(), wgt[i]);
      if (Event->lfvch() != 2) Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "LFVePt")]->Fill(Event->LFVe()->pt_, wgt[i]);
      if (Event->lfvch() != 1) Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "LFVmuPt")]->Fill(Event->LFVmu()->pt_, wgt[i]);
      if (Event->lfvch() != 0) Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "LFVtaPt")]->Fill(Event->LFVta()->pt_, wgt[i]);
      Hists[Event->c()][Event->ch()][i][vInd(vars, "BalepPt")]->Fill(Event->Balep()->pt_, wgt[i]);
      if (Event->njet() > 0) Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "Topmass")]->Fill(Event->Topmass(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "Ht")]->Fill(Event->Ht(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "St")]->Fill(Event->St(), wgt[i]);
      Hists[Event->c()][Event->ch()][reg[i]][vInd(vars, "btagSum")]->Fill(Event->btagSum(), wgt[i]);
    }

    deleteContainter(Leptons);
    deleteContainter(Jets);
    delete Event;

    nAccept++;
  } // end of event loop

  // Writing output and delete pointers
  TFile file_out (fname, "RECREATE");
  for (int i = 0; i < (int) charges.size(); ++i) {
    for (int j = 0; j < (int) channels.size(); ++j) {
      for (int k = 0; k < (int) regions.size(); ++k) {
        for (auto it = vars.cbegin(); it != vars.cend(); ++it) {
          name << charges[i] << "_" << channels[j] << "_" << regions[k] << "_" << it->first;
          Hists[i][j][k][it->second.at(0)]->SetName((name.str()).c_str());
          Hists[i][j][k][it->second.at(0)]->Write("", TObject::kOverwrite);
          delete Hists[i][j][k][it->second.at(0)];
          name.str("");
        }
      }
    }
  }
  // h_2D_woBtagSF->Write("", TObject::kOverwrite);
  // h_2D_wBtagSF->Write("", TObject::kOverwrite);
  file_out.Close();
  Hists.clear();

  // Writing summary
  auto end = std::chrono::high_resolution_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
  summary << "Thread " << workerID_ << ": from " << ntotal << " events, " << nAccept << " events are accepted; Time measured: " << ceil(elapsed.count() * 1e-9 * 100) / 100 << " seconds.\n";
  return summary;
}
