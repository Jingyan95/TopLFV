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


std::stringstream MyAnalysis::Loop(TString fname, TString data, TString dataset, TString year, TString run, float xs, float lumi,
                                   float Nevent, std::atomic<ULong64_t>& progress, std::atomic<ULong64_t>& counter) {

  std::stringstream summary;
  if (fChain == 0) {
    summary << "TChain is empty.\n";
    return summary;
  }

  auto begin = std::chrono::high_resolution_clock::now();

  std::vector<TString> charges{"OS", "SS"}; // Same-Sign, Opposite-Sign
  std::vector<TString> channels{"ee", "emu", "mumu"};
  std::vector<TString> regions{
    /*0*/ "ll", // No cuts
    /*1*/ "llOffZMetg20Jetgeq1B1", // SR
    /*2*/ "llOffZMetg20Jetgeq1B2", // ttbar + jets CR
    /*3*/ "llOffZStg300btagl1p3", // New SR (Loose)
    /*4*/ "llOffZStg300btagl1p3Tight", // New SR (Tight)
    /*5*/ "llOnZ", // Z + jets CR
    /*6*/ "llOnZMetg20Jetgeq1", // Z + jets CR
    /*7*/ "llbtagg1p3", // ttbar + jets CR
    /*8*/ "llbtagg1p3OffZ", // ttbar + jets CR
    /*9*/ "llStl300", // Generic signal-free region
    /*10*/ "llStl300OffZ", // Generic signal-free region
    /*11*/ "llMetg20Jetgeq1B0", // CR background estimation
    /*12*/ "llMetg20Jetgeq1B0OffZ" // CR background estimation
  };
  std::vector<int> unBlind{0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0};
  std::vector<TString> domains{"geqMedLepgeqTightTa", "geqMedLeplTightTa"};
  const std::map<TString, std::vector<float>> vars = {
    {"llM",              {0,    10,     0,   180}},
    {"llDr",             {1,    10,     0,   4.5}},
    {"lep1Pt",           {2,    10,    30,   230}},
    {"lep2Pt",           {3,    10,    20,   180}},
    {"elLeptonMVAv1",    {4,    50,     0,     1}},
    {"elLeptonMVAv2",    {5,    50,     0,     1}},
    {"muLeptonMVAv1",    {6,    50,     0,     1}},
    {"muLeptonMVAv2",    {7,    50,     0,     1}},
    {"taPt",             {8,    20,    20,   220}},
    {"taEta",            {9,    23,  -2.3,   2.3}},
    {"taVsJetWP",        {10,    8,     0,     8}},
    {"taVsJetMVA",       {11,   50,     0,     1}},
    {"taVsElMVA",        {12,   50,     0,     1}},
    {"taVsMuMVA",        {13,   50,     0,     1}},
    {"taDxy",            {14,   16,  -0.1,   0.1}},
    {"taDz",             {15,   16,  -0.2,   0.2}},
    {"taDecayMode",      {16,   12,     0,    12}},
    {"jet1Pt",           {17,   10,    25,   225}},
    {"jetbtagDeepFlavB", {18,   50,     0,     1}},
    {"njet",             {19,    6,     0,     6}},
    {"nbjet",            {20,    4,     0,     4}},
    {"MET",              {21,   10,     0,   200}},
    {"subSR",            {22,   18,     0,    18}},
    {"LFVemuM",          {23,   10,     0,   300}},
    {"LFVetaM",          {24,   10,     0,   300}},
    {"LFVmutaM",         {25,   10,     0,   300}},
    {"LFVemuDr",         {26,   10,     0,   4.5}},
    {"LFVetaDr",         {27,   10,     0,   4.5}},
    {"LFVmutaDr",        {28,   10,     0,   4.5}},
    {"LFVePt",           {29,   10,    20,   300}},
    {"LFVmuPt",          {30,   10,    20,   300}},
    {"LFVtaPt",          {31,   10,    20,   300}},
    {"balepPt",          {32,   10,    20,   180}},
    {"topmass",          {33,   10,     0,   300}},
    {"Ht",               {34,   10,     0,   300}},
    {"St",               {35,   20,    70,   600}},
    {"btagSum",          {36,   25,     0,   2.5}}
  };
  const std::vector<Double_t> ff_pt_bins = {20.0, 40.0, 60.0, 100.0, 220.0};
  const std::vector<Double_t> ff_eta_bins = {-2.3, -1.4, 1.4, 2.3};

  Double_t llMBin[19] = {0, 20, 39, 58.2, 63.2, 68.2, 73.2, 78.2, 83.2, 88.2, 93.2, 95.2, 98.2, 103.2, 108.2, 126, 144, 162, 180};
  Dim5 Hists(Dim5(charges.size(), Dim4(channels.size(), Dim3(regions.size(), Dim2(domains.size(), Dim1(vars.size()))))));
  TH1F *h_test;
  std::stringstream name;

  // Creating histograms
  for (int i = 0; i < (int) charges.size(); ++i) {
    for (int j = 0; j < (int) channels.size(); ++j) {
      for (int k = 0; k < (int) regions.size(); ++k) {
        for (int m = 0; m < (int) domains.size(); ++m) {
          for (auto it = vars.cbegin(); it != vars.cend(); ++it) {
            name << charges[i] << "_" << channels[j] << "_" << regions[k] << "_" << domains[m] << "_" << it->first << "_" << workerID_; // Adding working ID to avoid mem leak
            if (it->first.Contains("llM") && i == 0 && j != 1) {
              h_test = new TH1F((name.str()).c_str(), "", 18, llMBin);
            } else {
              h_test = new TH1F((name.str()).c_str(), "", it->second.at(1), it->second.at(2), it->second.at(3));
            }
            h_test->StatOverflows(kTRUE);
            h_test->Sumw2(kTRUE);
            Hists[i][j][k][m][it->second.at(0)] = h_test;
            name.str("");
          }
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
  TFile *f_Ta_JetFF = new TFile("data/TAU/" + year + "_JetToTauFakeFactors.root");
  TFile *f_Btag_corr = new TFile("data/BTV/" + year + "BtagCorr.root");
  const auto sf_El_RECO = *(TH2F*) f_El_RECO->Get("EGamma_SF2D");
  const auto sf_El_ID = *(TH2F*) f_El_ID->Get("EGamma_SF2D");
  const auto sf_Mu_RECO = *(TH2F*) f_Mu_RECO->Get("NUM_TrackerMuons_DEN_genTracks");
  const auto sf_Mu_ID = *(TH2F*) f_Mu_ID->Get("NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt");
  const auto sf_Ta_ID_jet = *(TF1*) f_Ta_ID_jet->Get("Tight_cent");
  const auto sf_Ta_ID_e = *(TH1F*) f_Ta_ID_e->Get("VVLoose");
  const auto sf_Ta_ID_mu = *(TH1F*) f_Ta_ID_mu->Get("Tight");
  const auto sf_Ta_ES_jet = *(TH1F*) f_Ta_ES_jet->Get("tes");
  const auto ff_Ta_OS_ee_llMetg20Jetgeq1B0 = *(TH2F*) f_Ta_JetFF->Get("OS_ee_llMetg20Jetgeq1B0_TauIdvsOnZ_ptEtaEstFF");
  const auto ff_Ta_OS_mumu_llMetg20Jetgeq1B0 = *(TH2F*) f_Ta_JetFF->Get("OS_mumu_llMetg20Jetgeq1B0_TauIdvsOnZ_ptEtaEstFF");
  const auto ff_Ta_OS_ee_llStl300 = *(TH2F*) f_Ta_JetFF->Get("OS_ee_llStl300_TauIdvsOnZ_ptEtaEstFF");
  const auto ff_Ta_OS_mumu_llStl300 = *(TH2F*) f_Ta_JetFF->Get("OS_mumu_llStl300_TauIdvsOnZ_ptEtaEstFF");
  const auto ff_Ta_OS_ee_llbtagg1p3 = *(TH2F*) f_Ta_JetFF->Get("OS_ee_llbtagg1p3_TauIdvsOnZ_ptEtaEstFF");
  const auto ff_Ta_OS_mumu_llbtagg1p3 = *(TH2F*) f_Ta_JetFF->Get("OS_mumu_llbtagg1p3_TauIdvsOnZ_ptEtaEstFF");
  const auto sf_Btag_corr = *(TH2F*) f_Btag_corr->Get("2DBtagShapeCorrection");
  f_El_RECO->Close();
  f_El_ID->Close();
  f_Mu_RECO->Close();
  f_Mu_ID->Close();
  f_Ta_ID_jet->Close();
  f_Ta_ID_e->Close();
  f_Ta_ID_mu->Close();
  f_Ta_ES_jet->Close();
  f_Ta_JetFF->Close();
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
  float tauEta;
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
  float weight_Ta_ff_OS_ee_llMetg20Jetgeq1B0;
  float weight_Ta_ff_OS_mumu_llMetg20Jetgeq1B0;
  float weight_Ta_ff_OS_ee_llStl300;
  float weight_Ta_ff_OS_mumu_llStl300;
  float weight_Ta_ff_OS_ee_llbtagg1p3;
  float weight_Ta_ff_OS_mumu_llbtagg1p3;
  float weight_Btag_corr; // Correction for btag shape to preserve normalization
  float weight_Event;
  TString histname;
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
    ++counter;
    updateProgress(progress, (float) jentry / ntr, nThread_, workerID_, 32);
    if (!verbose_) displayProgress(progress, counter, ntr, 32);
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
    weight_Ta_ff_OS_ee_llMetg20Jetgeq1B0 = 1;
    weight_Ta_ff_OS_mumu_llMetg20Jetgeq1B0 = 1;
    weight_Ta_ff_OS_ee_llStl300 = 1;
    weight_Ta_ff_OS_mumu_llStl300 = 1;
    weight_Ta_ff_OS_ee_llbtagg1p3 = 1;
    weight_Ta_ff_OS_mumu_llbtagg1p3 = 1;
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

    // Lepton selection
    Leptons = new std::vector<lepton_candidate*>();
    for (UInt_t l = 0; l < nElectron; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 2) break;

      eleEta = abs(Electron_eta[l] + Electron_deltaEtaSC[l]);
      if (Electron_pt[l] < 20 || abs(Electron_eta[l]) > 2.4 || (eleEta > 1.4442 && eleEta < 1.566)) continue;
      if (Electron_sip3d[l] > 8 || abs(Electron_dxy[l]) > 0.05 || abs(Electron_dz[l]) > 0.1) continue;
      if (Electron_miniPFRelIso_all[l] > 0.4 || (int) Electron_lostHits[l] > 1) continue;
      if (!Electron_convVeto[l] || (int) Electron_tightCharge[l] == 0) continue;
      if (Electron_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_El_RECO = weight_El_RECO * scale_factor(&sf_El_RECO, eleEta, Electron_pt[l], "");
        weight_El_ID = weight_El_ID * scale_factor(&sf_El_ID, eleEta, Electron_pt[l], "");
      }

      Leptons->push_back(new lepton_candidate(Electron_pt[l], Electron_eta[l], Electron_phi[l], Electron_dxy[l], Electron_dz[l],
        Electron_charge[l], 0, Electron_topLeptonMVA_v1[l], Electron_topLeptonMVA_v2[l], 0, l, 1,
        data == "mc" ? (int) Electron_genPartFlav[l] : 1, -1));
    }

    for (UInt_t l = 0; l < nMuon; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 2) break;

      if (Muon_pt[l] < 20 || abs(Muon_eta[l]) > 2.4) continue;
      if (!Muon_mediumId[l]) continue;
      if (Muon_sip3d[l] > 8 || abs(Muon_dxy[l]) > 0.05 || abs(Muon_dz[l]) > 0.1) continue;
      if (Muon_miniPFRelIso_all[l] > 0.4) continue;
      if (Muon_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_Mu_RECO = weight_Mu_RECO * scale_factor(&sf_Mu_RECO, abs(Muon_eta[l]), Muon_pt[l], "");
        weight_Mu_ID = weight_Mu_ID * scale_factor(&sf_Mu_ID, abs(Muon_eta[l]), Muon_pt[l], "");
      }

      Leptons->push_back(new lepton_candidate(Muon_pt[l], Muon_eta[l], Muon_phi[l], Muon_dxy[l], Muon_dz[l],
        Muon_charge[l], 0, Muon_topLeptonMVA_v1[l], Muon_topLeptonMVA_v2[l], 0, l, 2,
        data == "mc" ? (int) Muon_genPartFlav[l] : 1, -1));
    }

    if (Leptons->size() != 2 || ((*Leptons)[0]->pt_ < lep1PtCut && (*Leptons)[1]->pt_ < lep1PtCut)
        || !myTrig->triggerPass((*Leptons)[0]->flavor_ + (*Leptons)[1]->flavor_ - 2)) { // Applying flavor-dependent trigger requirement
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
      if ((int) Tau_idDeepTau2017v2p1VSjet[l] < 1 || (int) Tau_idDeepTau2017v2p1VSe[l] < 2 || (int) Tau_idDeepTau2017v2p1VSmu[l] < 8) continue;

      // Overlap removal
      if (event_candidate::deltaR((*Leptons)[0]->eta_, (*Leptons)[0]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4
          || event_candidate::deltaR((*Leptons)[1]->eta_, (*Leptons)[1]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4) continue;

      if (data == "mc") {
        if ((int) Tau_genPartFlav[l] == 5) weight_Ta_ID_jet = weight_Ta_ID_jet * sf_Ta_ID_jet.Eval(tauPt < 140 ? tauPt : 140); // SF measured up to 140GeV
        if ((int) Tau_genPartFlav[l] == 1 || (int) Tau_genPartFlav[l] == 3) weight_Ta_ID_e = weight_Ta_ID_e * sf_Ta_ID_e.GetBinContent(sf_Ta_ID_e.GetXaxis()->FindBin(abs(Tau_eta[l])));
        if ((int) Tau_genPartFlav[l] == 2 || (int) Tau_genPartFlav[l] == 4) weight_Ta_ID_mu = weight_Ta_ID_mu * sf_Ta_ID_mu.GetBinContent(sf_Ta_ID_mu.GetXaxis()->FindBin(abs(Tau_eta[l])));
      }

      Leptons->push_back(new lepton_candidate(tauPt, Tau_eta[l], Tau_phi[l], Tau_dxy[l], Tau_dz[l], Tau_charge[l],
        char_to_int(Tau_idDeepTau2017v2p1VSjet[l]), Tau_rawDeepTau2017v2p1VSjet[l], Tau_rawDeepTau2017v2p1VSe[l],
        Tau_rawDeepTau2017v2p1VSmu[l], l, 3, data == "mc" ? (int) Tau_genPartFlav[l] : 5, Tau_decayMode[l]));
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

    // Jet to tau fake factor weight calculated here for specific charges/channels
    tauPt = Event->ta1()->pt_;
    tauEta = Event->ta1()->eta_;
    if (!(data == "mc")) { // Apply fake factors to data only
      for (int pt = 0; pt < ff_pt_bins.size() - 1; pt++) {
        if (tauPt > ff_pt_bins[pt] && tauPt < ff_pt_bins[pt + 1]) {
          for (int eta = 0; eta < ff_eta_bins.size() - 1; eta++) {
            if (tauEta > ff_eta_bins[eta] && tauEta < ff_eta_bins[eta + 1]) {
              weight_Ta_ff_OS_ee_llMetg20Jetgeq1B0 = ff_Ta_OS_ee_llMetg20Jetgeq1B0.GetBinContent(pt + 1, eta + 1);
              weight_Ta_ff_OS_mumu_llMetg20Jetgeq1B0 = ff_Ta_OS_mumu_llMetg20Jetgeq1B0.GetBinContent(pt + 1, eta + 1);
              weight_Ta_ff_OS_ee_llStl300 = ff_Ta_OS_ee_llStl300.GetBinContent(pt + 1, eta + 1);
              weight_Ta_ff_OS_mumu_llStl300 = ff_Ta_OS_mumu_llStl300.GetBinContent(pt + 1, eta + 1);
              weight_Ta_ff_OS_ee_llbtagg1p3 = ff_Ta_OS_ee_llbtagg1p3.GetBinContent(pt + 1, eta + 1);
              weight_Ta_ff_OS_mumu_llbtagg1p3 = ff_Ta_OS_mumu_llbtagg1p3.GetBinContent(pt + 1, eta + 1);
              break;
            }
          }
          break;
        }
      }
    }

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

    int rIdx = rInd(regions, "ll"); // No cuts
    reg.push_back(rIdx);
    wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);

    if (!Event->OnZ()) {
      if (Event->MET()->Pt() > 20 && Event->njet() >= 1) {
        if (Event->nbjet() == 1) {
          rIdx = rInd(regions, "llOffZMetg20Jetgeq1B1"); // SR
          reg.push_back(rIdx);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
        }
        if (Event->nbjet() == 2) {
          rIdx = rInd(regions, "llOffZMetg20Jetgeq1B2"); // ttbar + jets CR
          reg.push_back(rIdx);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
        }
      }
      if (Event->St() > 300 && Event->btagSum() < 1.3) {
        rIdx = rInd(regions, "llOffZStg300btagl1p3"); // New SR (Loose)
        reg.push_back(rIdx);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);

        if (Event->SRindex() % 2 == 0 ? Event->njet() > 0 : Event->St() > 500) {
          rIdx = rInd(regions, "llOffZStg300btagl1p3Tight"); // New SR (Tight)
          reg.push_back(rIdx);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
        }
      }
    }
    else if (Event->OnZ()) {
      rIdx = rInd(regions, "llOnZ"); // Z + jets CR
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);

      if (Event->MET()->Pt() > 20 && Event->njet() >= 1) {
        rIdx = rInd(regions, "llOnZMetg20Jetgeq1"); // Z + jets CR
        reg.push_back(rIdx);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
      }
    }
    if (Event->btagSum() > 1.3) {
      rIdx = rInd(regions, "llbtagg1p3"); // ttbar + jets CR
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);

      if (!Event->OnZ()) { // Region D
        if (!Event->TightTau()) {
          if (Event->c() == 0 && Event->ch() == 0) weight_Event *= weight_Ta_ff_OS_ee_llbtagg1p3;
          if (Event->c() == 0 && Event->ch() == 2) weight_Event *= weight_Ta_ff_OS_mumu_llbtagg1p3;
        }
        rIdx = rInd(regions, "llbtagg1p3OffZ"); // ttbar + jets CR
        reg.push_back(rIdx);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
      }
    }
    if (Event->St() < 300) {
      rIdx = rInd(regions, "llStl300"); // Generic signal-free region
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);

      if (!Event->OnZ()) { // Region D
        if (!Event->TightTau()) {
          if (Event->c() == 0 && Event->ch() == 0) weight_Event *= weight_Ta_ff_OS_ee_llStl300;
          if (Event->c() == 0 && Event->ch() == 2) weight_Event *= weight_Ta_ff_OS_mumu_llStl300;
        }
        rIdx = rInd(regions, "llStl300OffZ"); // Generic signal-free region
        reg.push_back(rIdx);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
      }
    }
    if (Event->MET()->Pt() > 20 && Event->njet() >= 1 && Event->nbjet() == 0) {
      rIdx = rInd(regions, "llMetg20Jetgeq1B0"); // CR background estimation
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);

      if (!Event->OnZ()) { // Region D
        if (!Event->TightTau()) {
          if (Event->c() == 0 && Event->ch() == 0) weight_Event *= weight_Ta_ff_OS_ee_llMetg20Jetgeq1B0;
          if (Event->c() == 0 && Event->ch() == 2) weight_Event *= weight_Ta_ff_OS_mumu_llMetg20Jetgeq1B0;
        }
        rIdx = rInd(regions, "llMetg20Jetgeq1B0OffZ"); // CR background estimation
        reg.push_back(rIdx);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
      }
    }

    // Filling histograms
    for (int i = 0; i < reg.size(); ++i) {

      int cIdx = Event->c();
      int chIdx = Event->ch();
      int dIdx = dInd(domains, Event->TightTau());

      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "llM")]->Fill(Event->llM(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "llDr")]->Fill(Event->llDr(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "lep1Pt")]->Fill(Event->lep1()->pt_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "lep2Pt")]->Fill(Event->lep2()->pt_, wgt[i]);
      if (Event->lfvch() != 2) {
        Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "elLeptonMVAv1")]->Fill(Event->el1()->mva1_, wgt[i]);
        Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "elLeptonMVAv2")]->Fill(Event->el1()->mva2_, wgt[i]);
      }
      if (Event->lfvch() != 1) {
        Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "muLeptonMVAv1")]->Fill(Event->mu1()->mva1_, wgt[i]);
        Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "muLeptonMVAv2")]->Fill(Event->mu1()->mva2_, wgt[i]);
      }
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taPt")]->Fill(tauPt, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taEta")]->Fill(tauEta, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taVsJetWP")]->Fill(Event->ta1()->mva1WP_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taVsJetMVA")]->Fill(Event->ta1()->mva1_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taVsElMVA")]->Fill(Event->ta1()->mva2_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taVsMuMVA")]->Fill(Event->ta1()->mva3_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taDxy")]->Fill(Event->ta1()->dxy_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taDz")]->Fill(Event->ta1()->dz_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "taDecayMode")]->Fill(Event->ta1()->decaymode_, wgt[i]);
      if (Event->njet() > 0) Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "jet1Pt")]->Fill(Event->jet1()->pt_, wgt[i]);
      if (Event->njet() > 0) Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "jetbtagDeepFlavB")]->Fill(Event->jet1()->bt_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "njet")]->Fill(Event->njet(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "nbjet")]->Fill(Event->nbjet(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "MET")]->Fill(Event->MET()->Pt(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "subSR")]->Fill(Event->SRindex(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "LFVemuM")+Event->lfvch()]->Fill(Event->LFVllM(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "LFVemuDr")+Event->lfvch()]->Fill(Event->LFVllDr(), wgt[i]);
      if (Event->lfvch() != 2) Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "LFVePt")]->Fill(Event->LFVe()->pt_, wgt[i]);
      if (Event->lfvch() != 1) Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "LFVmuPt")]->Fill(Event->LFVmu()->pt_, wgt[i]);
      if (Event->lfvch() != 0) Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "LFVtaPt")]->Fill(Event->LFVta()->pt_, wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "balepPt")]->Fill(Event->Balep()->pt_, wgt[i]);
      if (Event->njet() > 0) Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "topmass")]->Fill(Event->Topmass(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "Ht")]->Fill(Event->Ht(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "St")]->Fill(Event->St(), wgt[i]);
      Hists[cIdx][chIdx][reg[i]][dIdx][vInd(vars, "btagSum")]->Fill(Event->btagSum(), wgt[i]);
    }

    deleteContainter(Leptons);
    deleteContainter(Jets);
    delete Event;

    nAccept++;
  } // End of event loop

  // Writing output and delete pointers
  TFile file_out (fname, "RECREATE");
  for (int i = 0; i < (int) charges.size(); ++i) {
    for (int j = 0; j < (int) channels.size(); ++j) {
      for (int k = 0; k < (int) regions.size(); ++k) {
        for (int m = 0; m < (int) domains.size(); ++m) {
          for (auto it = vars.cbegin(); it != vars.cend(); ++it) {
            name << charges[i] << "_" << channels[j] << "_" << regions[k] << "_" << domains[m] << "_" << it->first;
            Hists[i][j][k][m][it->second.at(0)]->SetName((name.str()).c_str());
            Hists[i][j][k][m][it->second.at(0)]->Write("", TObject::kOverwrite);
            delete Hists[i][j][k][m][it->second.at(0)];
            name.str("");
          }
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
