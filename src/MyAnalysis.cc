#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "PU_reWeighting.h"
#include "lepton_candidate.h"
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
  std::vector<TString> charges{"OS", "SS"};
  std::vector<TString> channels{"ee", "emu", "mue", "mumu"};
  std::vector<TString> pass{"All", "Pass"};
  const std::map<TString, std::vector<float>> vars =
  {
    {"lep1Pt",           {0,   3}},
    {"lep2Pt",           {1,   3}},
    {"lep1Eta",          {2,   4}},
    {"lep2Eta",          {3,   4}}
  };

  const std::map<TString, std::vector<float>> varsD2 =
  {
    {"lepPt",            {0,   3,   3}},
    {"lepEta",           {1,   4,   4}}
  };

  Double_t lep1PtBin[4] = {30, 75, 120, 200};
  Double_t lep2PtBin[4] = {20, 75, 120, 200};
  // Double_t lep1PtBin[8] = {30, 45, 75, 95, 120, 150, 200, 500};
  // Double_t lep2PtBin[8] = {20, 45, 75, 95, 120, 150, 200, 500};

  Double_t lep1EtaBin[5] = {-2.4, -1.4,  0,  1.4, 2.4};
  Double_t lep2EtaBin[5] = {-2.4, -1.4,  0,  1.4, 2.4};
  // Double_t lep1EtaBin[7] = {-2.4, -1.4, -0.7, 0,  0.7, 1.4, 2.4};
  // Double_t lep2EtaBin[7] = {-2.4, -1.4, -0.7, 0,  0.7, 1.4, 2.4};

  Dim4 Hists(Dim4(charges.size(),Dim3(channels.size(),Dim2(pass.size(),Dim1(vars.size())))));
  D2im4 HistsD2(D2im4(charges.size(),D2im3(channels.size(),D2im2(pass.size(),D2im1(varsD2.size())))));
  std::stringstream name;
  TH1F *h_test;
  TH2F *h2_test;

  for (int i = 0; i < (int) charges.size(); ++i) {
    for (int j = 0; j < (int) channels.size(); ++j) {
      for (int k = 0; k < (int) pass.size(); ++k) {
        for (auto it = vars.cbegin(); it != vars.cend(); ++it) {
          name << charges[i] << "_" << channels[j] << "_" << pass[k] << "_" << it->first << "_" << workerID_; // adding working ID to avoid mem leak
          if (it->first.Contains("lep1Pt")) {
            h_test = new TH1F((name.str()).c_str(), "", it->second.at(1), lep1PtBin);
          } else if (it->first.Contains("lep2Pt")) {
            h_test = new TH1F((name.str()).c_str(), "", it->second.at(1), lep2PtBin);
          } else if (it->first.Contains("lep1Eta")) {
            h_test = new TH1F((name.str()).c_str(), "", it->second.at(1), lep1EtaBin);
          } else if (it->first.Contains("lep2Eta")) {
            h_test = new TH1F((name.str()).c_str(), "", it->second.at(1), lep2EtaBin);
          }
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          Hists[i][j][k][it->second.at(0)] = h_test;
          name.str("");
        }
        for (auto it = varsD2.cbegin(); it != varsD2.cend(); ++it) {
          name << charges[i] << "_" << channels[j] << "_" << pass[k] << "_" << it->first << "_" << workerID_; // adding working ID to avoid mem leak
          if (it->first.Contains("lepPt")) {
            h2_test = new TH2F((name.str()).c_str(), "", it->second.at(1), lep1PtBin, it->second.at(2), lep2PtBin);
          } else if (it->first.Contains("lepEta")) {
            h2_test = new TH2F((name.str()).c_str(), "", it->second.at(1), lep1EtaBin, it->second.at(2), lep2EtaBin);
          } 
          h2_test->StatOverflows(kTRUE);
          h2_test->Sumw2(kTRUE);
          HistsD2[i][j][k][it->second.at(0)] = h2_test;
          name.str("");
        }
      }
    }
  }

  std::string string_year(year.Data());
  TFile *f_El_RECO = new TFile("data/EGM/RECO/" + year + "egammaEffi_ptAbove20.txt_EGM2D.root"); // https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis
  TFile *f_El_ID = new TFile("data/EGM/TOPMVASF/v1/MediumCharge/" + year + "egammaEffi.txt_EGM2D.root"); // Jack To-Do: TopMVA ID SF 2016APV,2017,2018
  TFile *f_Mu_RECO = new TFile("data/MUO/RECO/" + year + "Efficiency_muon_generalTracks_trackerMuon.root"); // https://gitlab.cern.ch/cms-muonPOG/muonefficiencies/-/tree/master/Run2/UL
  TFile *f_Mu_ID = new TFile("data/MUO/TOPMVASF/v1/Medium/" + year + "NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt.root");
  const auto sf_El_RECO = *(TH2F*)f_El_RECO->Get("EGamma_SF2D");
  const auto sf_El_ID = *(TH2F*)f_El_ID->Get("EGamma_SF2D");
  const auto sf_Mu_RECO = *(TH2F*)f_Mu_RECO->Get("NUM_TrackerMuons_DEN_genTracks");
  const auto sf_Mu_ID = *(TH2F*)f_Mu_ID->Get("NUM_LeptonMvaMedium_DEN_TrackerMuons_abseta_pt");
  f_El_RECO->Close();
  f_El_ID->Close();
  f_Mu_RECO->Close();
  f_Mu_ID->Close();

  std::vector<lepton_candidate*> *Leptons;
  event_candidate *Event;
  bool metFilterPass;
  float lep1PtCut = 30;
  float eleEta;
  float weight_Lumi;
  float weight_PU;
  float weight_L1ECALPreFiring;
  float weight_L1MuonPreFiring;
  float weight_El_RECO;
  float weight_El_ID;
  float weight_Mu_RECO;
  float weight_Mu_ID;
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
    weight_Lumi = 1;
    weight_PU = 1;
    weight_L1ECALPreFiring = 1;
    weight_L1MuonPreFiring = 1;
    weight_El_RECO = 1;
    weight_El_ID = 1;
    weight_Mu_RECO = 1;
    weight_Mu_ID = 1;
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
    if (!metFilterPass||!myTrig->triggerLogic()) continue; 

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

      Leptons->push_back(new lepton_candidate(Electron_pt[l]>200?199:Electron_pt[l], Electron_eta[l], Electron_phi[l], Electron_dxy[l], Electron_dz[l],
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

      Leptons->push_back(new lepton_candidate(Muon_pt[l]>200?199:Muon_pt[l], Muon_eta[l], Muon_phi[l], Muon_dxy[l], Muon_dz[l],
        Muon_charge[l], Muon_topLeptonMVA_v1[l], Muon_topLeptonMVA_v2[l], 0, l, 2,
        data == "mc" ? (int) Muon_genPartFlav[l] : 1));
    }

    if (Leptons->size() != 2 || ((*Leptons)[0]->pt_ < lep1PtCut && (*Leptons)[1]->pt_ < lep1PtCut)) { 
      deleteContainter(Leptons);
      continue;
    }

    // Reconstruction of heavy particles
    Event = new event_candidate(Leptons, verbose_);

    // MC weights
    if (data == "mc") {
      weight_Lumi = (1000 * xs * lumi * getSign(Generator_weight)) / Nevent; // N.B. Nevent here should be sum of generator weights instead of raw event counts
      weight_PU = wPU.getPUweight(year, int(Pileup_nTrueInt), "nominal");
      weight_L1ECALPreFiring = L1PreFiringWeight_ECAL_Nom;
      weight_L1MuonPreFiring = L1PreFiringWeight_Muon_Nom;
    }
    weight_Event = weight_Lumi * weight_PU * weight_L1ECALPreFiring * weight_L1MuonPreFiring * weight_El_RECO * weight_El_ID * weight_Mu_RECO * weight_Mu_ID;
    
    Hists[Event->c()][Event->ch()][0][vInd(vars, "lep1Pt")]->Fill(Event->lep1()->pt_, weight_Event);
    Hists[Event->c()][Event->ch()][0][vInd(vars, "lep2Pt")]->Fill(Event->lep2()->pt_, weight_Event);
    Hists[Event->c()][Event->ch()][0][vInd(vars, "lep1Eta")]->Fill(Event->lep1()->eta_, weight_Event);
    Hists[Event->c()][Event->ch()][0][vInd(vars, "lep2Eta")]->Fill(Event->lep2()->eta_, weight_Event);
    HistsD2[Event->c()][Event->ch()][0][vInd(varsD2, "lepPt")]->Fill(Event->lep1()->pt_, Event->lep2()->pt_, weight_Event);
    HistsD2[Event->c()][Event->ch()][0][vInd(varsD2, "lepEta")]->Fill(Event->lep1()->eta_, Event->lep2()->eta_, weight_Event);
    if (myTrig->triggerPass(Event->ch())){
      Hists[Event->c()][Event->ch()][1][vInd(vars, "lep1Pt")]->Fill(Event->lep1()->pt_, weight_Event);
      Hists[Event->c()][Event->ch()][1][vInd(vars, "lep2Pt")]->Fill(Event->lep2()->pt_, weight_Event);
      Hists[Event->c()][Event->ch()][1][vInd(vars, "lep1Eta")]->Fill(Event->lep1()->eta_, weight_Event);
      Hists[Event->c()][Event->ch()][1][vInd(vars, "lep2Eta")]->Fill(Event->lep2()->eta_, weight_Event);
      HistsD2[Event->c()][Event->ch()][1][vInd(varsD2, "lepPt")]->Fill(Event->lep1()->pt_, Event->lep2()->pt_, weight_Event);
      HistsD2[Event->c()][Event->ch()][1][vInd(varsD2, "lepEta")]->Fill(Event->lep1()->eta_, Event->lep2()->eta_, weight_Event);
    }
      
    deleteContainter(Leptons);
    delete Event;

    nAccept++;
  } // end of event loop

  // Writing output and delete pointers
  TFile file_out (fname, "RECREATE");
  for (int i = 0; i < (int) charges.size(); ++i) {
    for (int j = 0; j < (int) channels.size(); ++j) {
      for (int k = 0; k < (int) pass.size(); ++k) {
        for (auto it = vars.cbegin(); it != vars.cend(); ++it) {
          name << charges[i] << "_" << channels[j] << "_" << pass[k] << "_" << it->first;
          Hists[i][j][k][it->second.at(0)]->SetName((name.str()).c_str());
          Hists[i][j][k][it->second.at(0)]->Write("", TObject::kOverwrite);
          delete Hists[i][j][k][it->second.at(0)];
          name.str("");
        }
        for (auto it = varsD2.cbegin(); it != varsD2.cend(); ++it) {
          name << charges[i] << "_" << channels[j] << "_" << pass[k] << "_" << it->first;
          HistsD2[i][j][k][it->second.at(0)]->SetName((name.str()).c_str());
          HistsD2[i][j][k][it->second.at(0)]->Write("", TObject::kOverwrite);
          delete HistsD2[i][j][k][it->second.at(0)];
          name.str("");
        }
      }
    }
  }

  file_out.Close();
  Hists.clear();
  HistsD2.clear();

  // Writing summary
  auto end = std::chrono::high_resolution_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
  summary << "Thread " << workerID_ << ": from " << ntotal << " events, " << nAccept << " events are accepted; Time measured: " << ceil(elapsed.count() * 1e-9 * 100) / 100 << " seconds.\n";
  return summary;
}
