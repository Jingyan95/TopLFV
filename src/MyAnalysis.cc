#define MyAnalysis_cxx

#include "MyAnalysis.h"
#include "PU_reWeighting.h"
#include "lepton_candidate.h"
#include "jet_candidate.h"
#include "event_candidate.h"
#include "matrix_method.h"

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

  std::vector<TString> domains{"Prompt", "FakeL", "FakeLTau", "FakeTau"}; // Fully prompt, fake e/muon, fake e/muon + fake tau, fake tau.
  if (data == "data"){
    domains[0] = "Data";
  }else if (procname.count(dataset)){
    domains[0] = procname.find(dataset)->second;
  }else{   
    domains[0] = "Others";
  }
  std::vector<TString> charges{"OS", "SS"}; // Same-Sign, Opposite-Sign
  std::vector<TString> channels{"ee", "emu", "mumu"};
  std::vector<TString> regions{
    "ll",
    "llOnZMetg20Jetgeq1",
    "llOffZMetg20B1",
    "llOffZMetg20B2",
    "llStl300",
    "llOnZ",
    "llbtagg1p3",
    "llStg300OffZbtagl1p3"
  };
  std::vector<int> unBlind{0, 1, 0, 1, 1, 1, 1, 0};
  const std::map<TString, std::vector<float>> vars1D = {
    {"lep1Pt",           {0,   10,    30,  100}},
    {"lep2Pt",           {1,   10,    20,  100}},
    {"tauPt",            {2,   10,    20,  100}},
    {"lep1Eta",          {3,   3,     0,   2.4}},
    {"lep2Eta",          {4,   3,     0,   2.4}},
    {"tauEta",           {5,   3,     0,   2.3}},
    {"Ht",               {6,   10,    0,   200}},
    {"njet",             {7,   4,     0,   4}},
    {"nbjet",            {8,   3,     0,   3}},
    {"St",               {9,   10,    70,  300}},
    {"tauRT",            {10,  12,    -1,  5}}
  };
  
  // Creating histograms
  Dim5<TH1F*> Hists1D(Dim5<TH1F*>(domains.size(), Dim4<TH1F*>(charges.size(), Dim3<TH1F*>(channels.size(), Dim2<TH1F*>(regions.size(), Dim1<TH1F*>(vars1D.size()))))));
  TH1F *h_test1D;
  std::stringstream name;
  for (int i = 0; i < (int) domains.size(); ++i) {
    for (int j = 0; j < (int) charges.size(); ++j) {
      for (int k = 0; k < (int) channels.size(); ++k) {
        for (int l = 0; l < (int) regions.size(); ++l) {
          for (auto it = vars1D.cbegin(); it != vars1D.cend(); ++it) {
            name << domains[i] << "_" << charges[j] << "_" << channels[k] << "_" << regions[l] << "_" << it->first << "_" << workerID_; // Adding working ID to avoid mem leak
            h_test1D = new TH1F((name.str()).c_str(), "", it->second.at(1), it->second.at(2), it->second.at(3));
            h_test1D->StatOverflows(kTRUE);
            h_test1D->Sumw2(kTRUE);
            Hists1D[i][j][k][l][it->second.at(0)] = h_test1D;
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
  TFile *f_Ta_MM = new TFile("data/MatrixMethod/" + year + "FakeTauMatrixMethod.root"); // tau lepton
  TFile *f_Ta_MM_SF = new TFile("data/MatrixMethod/" + year + "FakeTauSF.root "); // tau lepton
  TFile *f_L_MM = new TFile("data/MatrixMethod/" + year + "FakeLMatrixMethod.root"); // light lepton
  TFile *f_TRG = new TFile("data/TRG/" + year + "TriggerSF.root");
  TFile *f_Btag_corr = new TFile("data/BTV/" + year + "BtagCorr.root");

  const TH2F sf_El_RECO = *(TH2F*) f_El_RECO->Get("EGamma_SF2D");
  const TH2F sf_El_ID = *(TH2F*) f_El_ID->Get("EGamma_SF2D");
  const TH2F sf_Mu_RECO = *(TH2F*) f_Mu_RECO->Get("NUM_TrackerMuons_DEN_genTracks");
  const TH2F sf_Mu_ID = *(TH2F*) f_Mu_ID->Get("NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt");
  const TH1F sf_Ta_ID_e = *(TH1F*) f_Ta_ID_e->Get("VVLoose");
  const TH1F sf_Ta_ID_mu = *(TH1F*) f_Ta_ID_mu->Get("Tight");
  const TF1 sf_Ta_ID_jet = *(TF1*) f_Ta_ID_jet->Get("Tight_cent");
  const TH2F rEff_1Prong = *(TH2F*) f_Ta_MM->Get("RealEff_AbsEtaVsPt_1Prong");
  const TH2F rEff_3Prong = *(TH2F*) f_Ta_MM->Get("RealEff_AbsEtaVsPt_3Prong");
  const TH2F fEff_1Prong = *(TH2F*) f_Ta_MM->Get("FakeEff_RtVsPt_1Prong");
  const TH2F fEff_3Prong = *(TH2F*) f_Ta_MM->Get("FakeEff_RtVsPt_3Prong");
  const TH2F fEff_SF_0J = *(TH2F*) f_Ta_MM_SF->Get("FakeEff_SF_AbsEtaVsPt_0J");
  const TH2F fEff_SF_1J = *(TH2F*) f_Ta_MM_SF->Get("FakeEff_SF_AbsEtaVsPt_1J");
  const TH2F fEff_SF_2J = *(TH2F*) f_Ta_MM_SF->Get("FakeEff_SF_AbsEtaVsPt_2J");
  const TH2F rEff_e = *(TH2F*) f_L_MM->Get("e_RealEff_AbsEtaVsPt");
  const TH2F rEff_mu = *(TH2F*) f_L_MM->Get("mu_RealEff_AbsEtaVsPt");
  const TH2F fEff_e = *(TH2F*) f_L_MM->Get("e_FakeEff_AbsEtaVsPt");
  const TH2F fEff_mu = *(TH2F*) f_L_MM->Get("mu_FakeEff_AbsEtaVsPt");
  const TH1F sf_Ta_ES_jet = *(TH1F*) f_Ta_ES_jet->Get("tes");
  const auto sf_TRG_ee = *(TH2F*)f_TRG->Get("ee");
  const auto sf_TRG_emu = *(TH2F*)f_TRG->Get("emu");
  const auto sf_TRG_mue = *(TH2F*)f_TRG->Get("mue");
  const auto sf_TRG_mumu = *(TH2F*)f_TRG->Get("mumu");
  const TH2F sf_Btag_corr = *(TH2F*) f_Btag_corr->Get("2DBtagShapeCorrection");

  f_El_RECO->Close();
  f_El_ID->Close();
  f_Mu_RECO->Close();
  f_Mu_ID->Close();
  f_Ta_ID_e->Close();
  f_Ta_ID_mu->Close();
  f_Ta_ID_jet->Close();
  f_Ta_ES_jet->Close();
  f_Ta_MM->Close();
  f_Ta_MM_SF->Close();
  f_L_MM->Close();
  f_TRG->Close();
  f_Btag_corr->Close();

  std::vector<lepton_candidate*>* Leptons;
  std::vector<jet_candidate*>* Jets;
  event_candidate* Event;
  matrix_method* MM;
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
  float weight_Ta_ID_e;
  float weight_Ta_ID_mu;
  float weight_Ta_ID_jet;
  float weight_TRG = 1;
  float weight_Btag_corr; // Correction for btag shape to preserve normalization
  float weight_Event;
  float r1, r2, r3, f1, f2, f3;
  std::vector<float> weight_MM; // matrix method weight for fake tau
  weight_MM.reserve(4);
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
      if (Electron_topLeptonMVA_v1[l] < 0.05) continue;

      if (data == "mc") {
        weight_El_RECO = weight_El_RECO * get_factor(&sf_El_RECO, eleEta, Electron_pt[l], "");
        weight_El_ID = weight_El_ID * get_factor(&sf_El_ID, eleEta, Electron_pt[l], "");
      }

      Leptons->push_back(new lepton_candidate(Electron_pt[l], Electron_eta[l], Electron_phi[l], Electron_dxy[l], Electron_dz[l],
        Electron_charge[l], 0, Electron_topLeptonMVA_v1[l], Electron_jetIdx[l]>=0?Jet_pt_nom[Electron_jetIdx[l]]:Electron_pt[l], 0, l, 1,
        data == "mc" ? (int) Electron_genPartFlav[l] : 1, -1));
    }

    for (UInt_t l = 0; l < nMuon; l++) {
      if (l >= 16) break; // Restrict the loop size
      if (Leptons->size() > 2) break;

      if (Muon_pt[l] < 20 || abs(Muon_eta[l]) > 2.4) continue;
      if (!Muon_mediumId[l]) continue;
      if (Muon_sip3d[l] > 8 || abs(Muon_dxy[l]) > 0.05 || abs(Muon_dz[l]) > 0.1) continue;
      if (Muon_miniPFRelIso_all[l] > 0.4) continue;
      // if (Muon_topLeptonMVA_v1[l] < 0.64) continue;

      if (data == "mc") {
        weight_Mu_RECO = weight_Mu_RECO * get_factor(&sf_Mu_RECO, abs(Muon_eta[l]), Muon_pt[l], "");
        weight_Mu_ID = weight_Mu_ID * get_factor(&sf_Mu_ID, abs(Muon_eta[l]), Muon_pt[l], "");
      }

      Leptons->push_back(new lepton_candidate(Muon_pt[l], Muon_eta[l], Muon_phi[l], Muon_dxy[l], Muon_dz[l],
        Muon_charge[l], 0, Muon_topLeptonMVA_v1[l], Muon_jetIdx[l]>=0?Jet_pt_nom[Muon_jetIdx[l]]:Muon_pt[l], 0, l, 2,
        data == "mc" ? (int) Muon_genPartFlav[l] : 1, -1));
    }

    // Applying flavor-dependent trigger requirement
    if (Leptons->size() != 2 || ((*Leptons)[0]->pt_ < lep1PtCut && (*Leptons)[1]->pt_ < lep1PtCut)
        || !myTrig->triggerPass((*Leptons)[0]->flavor_ + (*Leptons)[1]->flavor_ - 2)) {
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
      // "Tight" tau is defined as having Tau_idDeepTau2017v2p1VSjet >= 5
      // "Loose" tau is defined as having Tau_idDeepTau2017v2p1VSjet < 5
      // See line 26 in src/event_candidate.cc
      if ((int) Tau_idDeepTau2017v2p1VSe[l] < 2 || (int) Tau_idDeepTau2017v2p1VSmu[l] < 8 || (int) Tau_idDeepTau2017v2p1VSjet[l] < 1) continue;

      // Overlap removal
      if (event_candidate::deltaR((*Leptons)[0]->eta_, (*Leptons)[0]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4
          || event_candidate::deltaR((*Leptons)[1]->eta_, (*Leptons)[1]->phi_, Tau_eta[l], Tau_phi[l]) < 0.4) continue;

      if (data == "mc") {
        if ((int) Tau_genPartFlav[l] == 5) weight_Ta_ID_jet = weight_Ta_ID_jet * sf_Ta_ID_jet.Eval(tauPt < 140 ? tauPt : 140); // SF measured up to 140GeV
        if ((int) Tau_genPartFlav[l] == 1 || (int) Tau_genPartFlav[l] == 3) weight_Ta_ID_e = weight_Ta_ID_e * sf_Ta_ID_e.GetBinContent(sf_Ta_ID_e.GetXaxis()->FindBin(abs(Tau_eta[l])));
        if ((int) Tau_genPartFlav[l] == 2 || (int) Tau_genPartFlav[l] == 4) weight_Ta_ID_mu = weight_Ta_ID_mu * sf_Ta_ID_mu.GetBinContent(sf_Ta_ID_mu.GetXaxis()->FindBin(abs(Tau_eta[l])));
      }

      Leptons->push_back(new lepton_candidate(tauPt, Tau_eta[l], Tau_phi[l], Tau_dxy[l], Tau_dz[l], Tau_charge[l],
        char_to_int(Tau_idDeepTau2017v2p1VSjet[l]), Tau_rawDeepTau2017v2p1VSjet[l], Tau_jetIdx[l]>=0?Jet_pt_nom[Tau_jetIdx[l]]:tauPt,
        Tau_jetIdx[l]>=0?Jet_btagDeepFlavB[Tau_jetIdx[l]]:0, l, 3, data == "mc" ? (int) Tau_genPartFlav[l] : 5, Tau_decayMode[l]));
    }

    if (Leptons->size() != 3 || abs((*Leptons)[0]->charge_ + (*Leptons)[1]->charge_ + (*Leptons)[2]->charge_) > 1) {
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
      if (Event->ch()==0){
        weight_TRG = get_factor(&sf_TRG_ee, Event->lep1()->pt_, Event->lep2()->pt_, "");
      }else if (Event->ch()==2){
        weight_TRG = get_factor(&sf_TRG_mumu, Event->lep1()->pt_, Event->lep2()->pt_, "");
      }else if (Event->lep1()->flavor_==1){
        weight_TRG = get_factor(&sf_TRG_emu, Event->lep1()->pt_, Event->lep2()->pt_, "");
      }else{
        weight_TRG = get_factor(&sf_TRG_mue, Event->lep1()->pt_, Event->lep2()->pt_, "");
      }
        weight_Btag_corr = get_factor(&sf_Btag_corr, Event->njet(), Event->Ht(), "");
    }

    weight_Event = Event->typeIndex()==0?weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID * weight_Ta_ID_jet * weight_Ta_ID_e * weight_Ta_ID_mu * weight_TRG * Event->btagSF() * weight_Btag_corr:0;

    int dIdx = 0;
    if ((Event->lep1()->truth_>0 || Event->lep2()->truth_>0) && Event->ta1()->truth_==0){
        dIdx = 1;
        weight_Event = 0;// turn off MC fake estimate
    }
    if ((Event->lep1()->truth_>0 || Event->lep2()->truth_>0) && Event->ta1()->truth_>0){
        dIdx = 2;
        weight_Event = 0;// turn off MC fake estimate
    }
    if (Event->lep1()->truth_==0 && Event->lep2()->truth_==0 && Event->ta1()->truth_>0){
        dIdx = 3;
        weight_Event = 0;// turn off MC fake estimate
    }
    if (data == "data" || dataset.Contains("LFV")){
        dIdx = 0;
    }
    int rIdx = rInd(regions, "ll");
    reg.push_back(rIdx); // No cuts
    wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
    if (Event->MET()->Pt() > 20 && Event->njet() > 0) {
      if (Event->OnZ()) { // Z+jets CR
        rIdx = rInd(regions, "llOnZMetg20Jetgeq1");
        reg.push_back(rIdx);
        wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
      } else {
        if (Event->nbjet() == 1) { // SR
          rIdx = rInd(regions, "llOffZMetg20B1");
          reg.push_back(rIdx);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
        }
        if (Event->nbjet() == 2) { // ttbar+jets CR
          rIdx = rInd(regions, "llOffZMetg20B2");
          reg.push_back(rIdx);
          wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
        }
      }
    }
    if (Event->St() < 300) { // Generic signal-free region
      rIdx = rInd(regions, "llStl300");
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
    }
    if (Event->OnZ()) { // Z+jets CR
      rIdx = rInd(regions, "llOnZ");
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
    }
    if (Event->btagSum() > 1.3) { // ttbar+jets CR
      rIdx = rInd(regions, "llbtagg1p3");
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
    }
    if (Event->St() > 300 && !Event->OnZ() && Event->btagSum() < 1.3) { // New SR
      rIdx = rInd(regions, "llStg300OffZbtagl1p3");
      reg.push_back(rIdx);
      wgt.push_back(data == "mc" ? weight_Event : weight_Event * unBlind[rIdx]);
    }
  
    int cIdx = Event->c();
    int chIdx = Event->ch();
    // Filling histograms
    for (int i = 0; i < reg.size(); ++i) {
      float wgt_final = wgt[i];
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "lep1Pt")]->Fill(Event->lep1()->pt_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "lep2Pt")]->Fill(Event->lep2()->pt_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauPt")]->Fill(Event->ta1()->pt_, wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "lep1Eta")]->Fill(abs(Event->lep1()->eta_), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "lep2Eta")]->Fill(abs(Event->lep2()->eta_), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauEta")]->Fill(abs(Event->ta1()->eta_), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "Ht")]->Fill(Event->Ht(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "njet")]->Fill(Event->njet(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "nbjet")]->Fill(Event->nbjet(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "St")]->Fill(Event->St(), wgt_final);
      Hists1D[dIdx][cIdx][chIdx][reg[i]][vInd(vars1D, "tauRT")]->Fill(Event->ta1()->recoil_/Event->ta1()->pt_, wgt_final);
    }
    if (Event->lep1()->flavor_==0){
       r1 = get_factor(&rEff_e,Event->lep1()->pt_, abs(Event->lep1()->eta_), ""); 
       f1 = get_factor(&fEff_e,Event->lep1()->jetpt_, abs(Event->lep1()->eta_), ""); 
    }else{
       r1 = get_factor(&rEff_mu,Event->lep1()->pt_, abs(Event->lep1()->eta_), ""); 
       f1 = get_factor(&fEff_mu,Event->lep1()->jetpt_, abs(Event->lep1()->eta_), ""); 
    }
    if (Event->lep2()->flavor_==0){
       r2 = get_factor(&rEff_e,Event->lep2()->pt_, abs(Event->lep2()->eta_), ""); 
       f2 = get_factor(&fEff_e,Event->lep2()->jetpt_, abs(Event->lep2()->eta_), ""); 
    }else{
       r2 = get_factor(&rEff_mu,Event->lep2()->pt_, abs(Event->lep2()->eta_), ""); 
       f2 = get_factor(&fEff_mu,Event->lep2()->jetpt_, abs(Event->lep2()->eta_), ""); 
    }
    if (Event->ta1()->decaymode_<10){
       r3 = get_factor(&rEff_1Prong,Event->ta1()->pt_, abs(Event->ta1()->eta_), ""); 
       f3 = get_factor(&fEff_1Prong,Event->ta1()->jetpt_, Event->ta1()->recoil_/Event->ta1()->pt_, ""); 
    }else{
       r3 = get_factor(&rEff_3Prong,Event->ta1()->pt_, abs(Event->ta1()->eta_), ""); 
       f3 = get_factor(&fEff_3Prong,Event->ta1()->jetpt_, Event->ta1()->recoil_/Event->ta1()->pt_, ""); 
    }
    if (Event->njet()==0) f3*=get_factor(&fEff_SF_0J, Event->ta1()->pt_, Event->llPt(), "");
    if (Event->njet()==1) f3*=get_factor(&fEff_SF_1J, Event->ta1()->pt_, Event->llPt(), "");
    if (Event->njet()>=2) f3*=get_factor(&fEff_SF_2J, Event->ta1()->pt_, Event->llPt(), "");
    MM = new matrix_method(r1, r2, r3, f1, f2, f3, Event->typeIndex());
    weight_MM = MM->getWeights();
    if (data == "mc") std::fill(weight_MM.begin(), weight_MM.end(), 0);
    for (int i = 0; i < reg.size(); ++i) {
        for (int j = 1; j < domains.size(); ++j){
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "lep1Pt")]->Fill(Event->lep1()->pt_, weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "lep2Pt")]->Fill(Event->lep2()->pt_, weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "tauPt")]->Fill(Event->ta1()->pt_, weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "lep1Eta")]->Fill(abs(Event->lep1()->eta_), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "lep2Eta")]->Fill(abs(Event->lep2()->eta_), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "tauEta")]->Fill(abs(Event->ta1()->eta_), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "Ht")]->Fill(Event->Ht(), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "njet")]->Fill(Event->njet(), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "nbjet")]->Fill(Event->nbjet(), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "St")]->Fill(Event->St(), weight_MM[j]);
            Hists1D[j][cIdx][chIdx][reg[i]][vInd(vars1D, "tauRT")]->Fill(Event->ta1()->recoil_/Event->ta1()->pt_, weight_MM[j]);
        }
    }

    deleteContainter(Leptons);
    deleteContainter(Jets);
    delete Event;
    delete MM;

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
        }
      }
    }
  }

  file_out.Close();
  Hists1D.clear();
  weight_MM.clear();

  // Writing summary
  auto end = std::chrono::high_resolution_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
  summary << "Thread " << workerID_ << ": from " << ntotal << " events, " << nAccept << " events are accepted; Time measured: " << ceil(elapsed.count() * 1e-9 * 100) / 100 << " seconds.\n";
  return summary;
}
