const TString YEARS[1] = {"2016"/*, "2016APV", "2017", "2018"*/};
const std::vector<TString> SAMPLES{"Data", "TX", "VV", "DY", "TT"};
const TString CHARGES[2] = {"OS", "SS"};
const TString CHANNELS[3] = {"ee", "emu", "mumu"};
const std::vector<TString> REGIONS{"ll", "llStl300", "llbtagg1p3", "llMetg20Jetgeq1B1",
  "llMetg20Jetgeq1B0"/*, "llStg300btagl1p3", "llStg300btagl1p3Tight"*/};
const std::vector<std::vector<TString>> REGIONS_NAME{
  {"", "No cuts", ""},
  {", CR", "S_{T}<300GeV", ""},
  {", t#bar{t}+jets CR", "btag>1.3", ""},
  {", SR", "p_{T}^{miss}>20GeV", "njet#geq1, nbjet=1"},
  {", CR", "p_{T}^{miss}>20GeV", "njet#geq1, nbjet=0"},
  // {", New SR (Loose)", "S_{T}>300GeV", "btag<1.3"},
  // {", New SR (Tight)", "S_{T}>300GeV, btag<1.3", "njet#geq1 or S_{T}>500GeV"}
};
const TString VARS[1] = {"TauIdvsOnZ"};

// Fake factor bins
const std::vector<Double_t> PT_BINS = {20.0, 40.0, 60.0, 100.0, 220.0};
const std::vector<Double_t> ETA_BINS = {-2.3, -1.4, 1.4, 2.3};
const std::vector<Int_t> DM = {0, 1, 10, 11};

// Plot colors
const Int_t COLORS[3] = {4, 2};

// Plot axis labels
const std::vector<TString> ZBinLabels{"On Z", "Off Z"};
const std::vector<TString> WPBinLabels{"VVVLoose", "VVLoose", "VLoose", "Loose",
  "Medium", "Tight", "VTight", "VVTight"};
// const std::vector<TString> DMBinLabels{"0", "1", "10", "11"};

// --------------------------------- //
bool doDetailedPlots = true;
// --------------------------------- //

void Estimate(TH2F* hData, const vector<TH2F*>& hMC, int xCut, int yCut, Double_t results[6],
  bool plotIntermediate = false, TString key = "", TString lumi = "");
void PlotTH1F(TString name, TString xName, TString yName, std::vector<TH1F*> H1,
  std::vector<TString> hNames, Int_t rIdx, TString lumi);
void PlotTH1F(TString name, TString xName, TString yName, std::vector<std::vector<Double_t>> h,
  std::vector<std::vector<Double_t>> hErr, const std::vector<Double_t> binEdges,
  std::vector<TString> hNames, Int_t rIdx, TString lumi);
void PlotTH2F(TH2F* h2, TString xName, TString yName, TString lumi, TString pName,
  const std::vector<TString>& xBinLabels = {}, const std::vector<TString>& yBinLabels = {});
TString GetLumi(TString year);


void FakeFactor() {

  // Open files and save histograms
  std::map<TString, TH2F*> H2{};
  char nameBin[500];
  char nameDM[500];
  for (TString year : YEARS) {
    for (TString sample : SAMPLES) {

      TString fName = "../hists/" + year + "_" + sample + ".root";
      TFile* f = TFile::Open(fName);

      for (TString charge : CHARGES) {
        for (TString channel : CHANNELS) {
          for (TString region : REGIONS) {
            for (TString var : VARS) {

              TString name = charge + "_" + channel + "_" + region + "_" + var;
              TH2F* h = (TH2F*) f->Get<TH2F>(name)->Clone();
              H2.emplace(std::make_pair(year + "_" + name + "_" + sample, h));
              TH2F* hHad = (TH2F*) f->Get<TH2F>(name + "Hadronic")->Clone();
              H2.emplace(std::make_pair(year + "_" + name + "Hadronic_" + sample, hHad));

              // Read in pt binned histograms
              for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {
                snprintf(nameBin, 500, name + "_pt%.1fto%.1f", PT_BINS[pt], PT_BINS[pt + 1]);
                TH2F* hBin = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                H2.emplace(std::make_pair(year + "_" + nameBin + "_" + sample, hBin));
                snprintf(nameBin, 500, name + "Hadronic_pt%.1fto%.1f", PT_BINS[pt], PT_BINS[pt + 1]);
                TH2F* hBinHad = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                H2.emplace(std::make_pair(year + "_" + nameBin + "_" + sample, hBinHad));

                for (Int_t dm : DM) {
                  snprintf(nameDM, 500, name + "_pt%.1fto%.1f_dm%d", PT_BINS[pt], PT_BINS[pt + 1], dm);
                  TH2F* hDM = (TH2F*) f->Get<TH2F>(nameDM)->Clone();
                  H2.emplace(std::make_pair(year + "_" + nameDM + "_" + sample, hDM));
                  snprintf(nameDM, 500, name + "Hadronic_pt%.1fto%.1f_dm%d", PT_BINS[pt], PT_BINS[pt + 1], dm);
                  TH2F* hDMHad = (TH2F*) f->Get<TH2F>(nameDM)->Clone();
                  H2.emplace(std::make_pair(year + "_" + nameDM + "_" + sample, hDMHad));
                }
              }

              // Read in eta binned histograms
              for (Int_t eta = 0; eta < ETA_BINS.size() - 1; eta++) {
                snprintf(nameBin, 500, name + "_eta%.1fto%.1f", ETA_BINS[eta], ETA_BINS[eta + 1]);
                TH2F* hBin = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                H2.emplace(std::make_pair(year + "_" + nameBin + "_" + sample, hBin));
                snprintf(nameBin, 500, name + "Hadronic_eta%.1fto%.1f", ETA_BINS[eta], ETA_BINS[eta + 1]);
                TH2F* hBinHad = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                H2.emplace(std::make_pair(year + "_" + nameBin + "_" + sample, hBinHad));

                for (Int_t dm : DM) {
                  snprintf(nameDM, 500, name + "_eta%.1fto%.1f_dm%d", ETA_BINS[eta], ETA_BINS[eta + 1], dm);
                  TH2F* hDM = (TH2F*) f->Get<TH2F>(nameDM)->Clone();
                  H2.emplace(std::make_pair(year + "_" + nameDM + "_" + sample, hDM));
                  snprintf(nameDM, 500, name + "Hadronic_eta%.1fto%.1f_dm%d", ETA_BINS[eta], ETA_BINS[eta + 1], dm);
                  TH2F* hDMHad = (TH2F*) f->Get<TH2F>(nameDM)->Clone();
                  H2.emplace(std::make_pair(year + "_" + nameDM + "_" + sample, hDMHad));
                }
              }

              // Read in pt and eta binned histograms
              for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {
                for (Int_t eta = 0; eta < ETA_BINS.size() - 1; eta++) {
                  snprintf(nameBin, 500, name + "_pt%.1fto%.1f_eta%.1fto%.1f", PT_BINS[pt], PT_BINS[pt + 1], ETA_BINS[eta], ETA_BINS[eta + 1]);
                  TH2F* hBin = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                  H2.emplace(std::make_pair(year + "_" + nameBin + "_" + sample, hBin));
                  snprintf(nameBin, 500, name + "Hadronic_pt%.1fto%.1f_eta%.1fto%.1f", PT_BINS[pt], PT_BINS[pt + 1], ETA_BINS[eta], ETA_BINS[eta + 1]);
                  TH2F* hBinHad = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                  H2.emplace(std::make_pair(year + "_" + nameBin + "_" + sample, hBinHad));
                }
              }
            }
          }
        }
      }
    }
  }

  // Set negative event counts due to NLO low statistics to 0
  for (auto it = H2.cbegin(); it != H2.cend(); it++) {
    for (int i = 1; i <= it->second->GetNbinsX(); i++) {
      for (int j = 1; j <= it->second->GetNbinsY(); j++) {
        if (it->second->GetBinContent(i, j) < 0.0) {
          it->second->SetBinContent(i, j, 0.0);
          it->second->SetBinError(i, j, 0.0);
        }
      }
    }
  }

  // Set plot style
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);
  gStyle->SetTitleXOffset(1.4);
  gStyle->SetTitleYOffset(1.4);

  // Do fake factor estimation
  char hKey[500];
  TString key, pName;
  Double_t results[6];
  std::vector<TH2F*> hEmpty{};
  for (TString year : YEARS) {
    std::vector<TH1F*> HFakeFactors{};
    std::vector<TH2F*> HFakeFactors2D{};
    for (TString charge : CHARGES) {
      for (TString channel : CHANNELS) {
        for (Int_t r = 0; r < REGIONS.size(); r++) {
          for (TString var : VARS) {

            // Plot some of the 2D histograms
            if (doDetailedPlots) {
              for (TString sample : SAMPLES) {
                key = year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_" + var + "_" + sample;
                pName = "../plot/" + key + ".pdf";
                PlotTH2F(H2.at(key), "All Events", "Tau vs Jets WP", GetLumi(year), pName,
                  ZBinLabels, WPBinLabels);
              }
            }

            pName = charge + "_" + channel + "_" + REGIONS[r] + "_" + var;

            // Do fake factor estimation in pt bins
            std::vector<Double_t> estFF{};
            std::vector<Double_t> estFFErr{};
            // std::vector<std::vector<Double_t>> estPred{{}, {}};
            // std::vector<std::vector<Double_t>> estPredErr{{}, {}};
            for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {
              std::vector<TH2F*> hMC{};
              for (int s = 1; s < SAMPLES.size(); s++) {
                snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                  + var + "Hadronic_pt%.1fto%.1f_" + SAMPLES[s], PT_BINS[pt], PT_BINS[pt + 1]);
                hMC.push_back(H2.at(hKey));
              }
              snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                + var + "_pt%.1fto%.1f_" + SAMPLES[0], PT_BINS[pt], PT_BINS[pt + 1]);
              Estimate(H2.at(hKey), hMC, 1, 5, results, true, hKey, GetLumi(year));
              estFF.push_back(results[0]);
              estFFErr.push_back(results[1]);
              // estPred.at(0).push_back(results[2]);
              // estPredErr.at(0).push_back(results[3]);
              // estPred.at(1).push_back(results[4]);
              // estPredErr.at(1).push_back(results[5]);
            }
            TH1F* hFFPt = new TH1F(pName + "_ptEstFF", "", PT_BINS.size() - 1, PT_BINS.data());
            for (int b = 0; b < estFF.size(); b++) {
              hFFPt->SetBinContent(b + 1, estFF.at(b));
              hFFPt->SetBinError(b + 1, estFFErr.at(b));
            }
            HFakeFactors.push_back(hFFPt);
            if (doDetailedPlots) {
              PlotTH1F(year + "_" + pName + "_ptEstFF", "Tau p_{T}", "Fake Factor", {hFFPt},
                {"Fake Factor"}, r, GetLumi(year));
              // PlotTH1F(year + "_" + pName + "_ptEstComp", "Tau p_{T}", "Background Estimation", estPred,
              //   estPredErr, PT_BINS, {"Fake Taus", "Data Taus"}, r, GetLumi(year));
            }

            // Do fake factor estimation in eta bins
            estFF = {};
            estFFErr = {};
            // estPred = {{}, {}};
            // estPredErr = {{}, {}};
            for (Int_t eta = 0; eta < ETA_BINS.size() - 1; eta++) {
              std::vector<TH2F*> hMC{};
              for (int s = 1; s < SAMPLES.size(); s++) {
                snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                  + var + "Hadronic_eta%.1fto%.1f_" + SAMPLES[s], ETA_BINS[eta], ETA_BINS[eta + 1]);
                hMC.push_back(H2.at(hKey));
              }
              snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                + var + "_eta%.1fto%.1f_" + SAMPLES[0], ETA_BINS[eta], ETA_BINS[eta + 1]);
              Estimate(H2.at(hKey), hMC, 1, 5, results, true, hKey, GetLumi(year));
              estFF.push_back(results[0]);
              estFFErr.push_back(results[1]);
              // estPred.at(0).push_back(results[2]);
              // estPredErr.at(0).push_back(results[3]);
              // estPred.at(1).push_back(results[4]);
              // estPredErr.at(1).push_back(results[5]);
            }
            TH1F* hFFEta = new TH1F(pName + "_etaEstFF", "", ETA_BINS.size() - 1, ETA_BINS.data());
            for (int b = 0; b < estFF.size(); b++) {
              hFFEta->SetBinContent(b + 1, estFF.at(b));
              hFFEta->SetBinError(b + 1, estFFErr.at(b));
            }
            HFakeFactors.push_back(hFFEta);
            if (doDetailedPlots) {
              PlotTH1F(year + "_" + pName + "_etaEstFF", "Tau #eta", "Fake Factor", {hFFEta},
                {"Fake Factor"}, r, GetLumi(year));
              // PlotTH1F(year + "_" + pName + "_etaEstComp", "Tau #eta", "Background Estimation", estPred,
              //   estPredErr, ETA_BINS, {"Fake Taus", "All Taus"}, r, GetLumi(year));
            }

            // Do fake factor estimate in pt and eta bins
            std::vector<std::vector<Double_t>> estFF2D{};
            std::vector<std::vector<Double_t>> estFFErr2D{};
            for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {
              estFF2D.push_back({});
              estFFErr2D.push_back({});
              for (Int_t eta = 0; eta < ETA_BINS.size() - 1; eta++) {
                std::vector<TH2F*> hMC{};
                for (int s = 1; s < SAMPLES.size(); s++) {
                  snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                    + var + "Hadronic_pt%.1fto%.1f_eta%.1fto%.1f_" + SAMPLES[s],
                    PT_BINS[pt], PT_BINS[pt + 1], ETA_BINS[eta], ETA_BINS[eta + 1]);
                  hMC.push_back(H2.at(hKey));
                }
                snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                  + var + "_pt%.1fto%.1f_eta%.1fto%.1f_" + SAMPLES[0],
                  PT_BINS[pt], PT_BINS[pt + 1], ETA_BINS[eta], ETA_BINS[eta + 1]);
                Estimate(H2.at(hKey), hMC, 1, 5, results, true, hKey, GetLumi(year));
                estFF2D.at(pt).push_back(results[0]);
                estFFErr2D.at(pt).push_back(results[1]);
              }
            }
            TH2F* hFF2D = new TH2F(pName + "_ptEtaEstFF", "",
              PT_BINS.size() - 1, PT_BINS.data(), ETA_BINS.size() - 1, ETA_BINS.data());
            for (int bx = 0; bx < estFF2D.size(); bx++) {
              for (int by = 0; by < estFF2D.at(bx).size(); by++) {
                hFF2D->SetBinContent(bx + 1, by + 1, estFF2D.at(bx).at(by));
                hFF2D->SetBinError(bx + 1, by + 1, estFFErr2D.at(bx).at(by));
              }
            }
            HFakeFactors2D.push_back(hFF2D);
            if (doDetailedPlots) {
              PlotTH2F(hFF2D, "Tau p_{T}", "Tau #eta", GetLumi(year),
                "../plot/" + year + "_" + pName + "_ptEtaEstFF.pdf");
            }

            // Validation of fake factor estimation with pt bins
            for (TString sample : SAMPLES) {
              if (sample == "TT" || sample == "DY") {
                std::vector<Double_t> valFF{};
                std::vector<Double_t> valFFErr{};
                std::vector<std::vector<Double_t>> valPred{{}, {}};
                std::vector<std::vector<Double_t>> valPredErr{{}, {}};
                for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {
                  snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                    + var + "_pt%.1fto%.1f_" + sample, PT_BINS[pt], PT_BINS[pt + 1]);
                  Estimate(H2.at(hKey), hEmpty, 1, 5, results);
                  valFF.push_back(results[0]);
                  valFFErr.push_back(results[1]);
                  valPred.at(0).push_back(results[2]);
                  valPredErr.at(0).push_back(results[3]);
                  valPred.at(1).push_back(results[4]);
                  valPredErr.at(1).push_back(results[5]);
                }
                if (doDetailedPlots) {
                  pName = year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_" + var + "_" + sample;
                  PlotTH1F(pName + "_ptValFF", "Tau p_{T}", "Fake Factor", {valFF}, {valFFErr},
                    PT_BINS, {"Fake Factor"}, r, GetLumi(year));
                  PlotTH1F(pName + "_ptValEst", "Tau p_{T}", "Background Estimation", valPred,
                    valPredErr, PT_BINS, {"ABCD method", "MC prediction"}, r, GetLumi(year));
                }
              }
            }

            // Validation of fake factor estimation with eta bins
            for (TString sample : SAMPLES) {
              if (sample == "TT" || sample == "DY") {
                std::vector<Double_t> valFF{};
                std::vector<Double_t> valFFErr{};
                std::vector<std::vector<Double_t>> valPred{{}, {}};
                std::vector<std::vector<Double_t>> valPredErr{{}, {}};
                for (Int_t eta = 0; eta < ETA_BINS.size() - 1; eta++) {
                  snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_"
                    + var + "_eta%.1fto%.1f_" + sample, ETA_BINS[eta], ETA_BINS[eta + 1]);
                  Estimate(H2.at(hKey), hEmpty, 1, 5, results);
                  valFF.push_back(results[0]);
                  valFFErr.push_back(results[1]);
                  valPred.at(0).push_back(results[2]);
                  valPredErr.at(0).push_back(results[3]);
                  valPred.at(1).push_back(results[4]);
                  valPredErr.at(1).push_back(results[5]);
                }
                if (doDetailedPlots) {
                  pName = year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_" + var + "_" + sample;
                  PlotTH1F(pName + "_etaValFF", "Tau #eta", "Fake Factor", {valFF}, {valFFErr},
                    ETA_BINS, {"Fake Factor"}, r, GetLumi(year));
                  PlotTH1F(pName + "_etaValEst", "Tau #eta", "Background Estimation", valPred,
                    valPredErr, ETA_BINS, {"ABCD method", "MC prediction"}, r, GetLumi(year));
                }
              }
            }

            // Validation of fake factor estimation with pt and eta bins
            // TODO
          }
        }
      }
    }

    TString filename = year + "_JetToTauFakeFactors.root";
    TFile fOut (filename, "RECREATE");
    for (TH1F* h : HFakeFactors) h->Write("", TObject::kOverwrite);
    for (TH2F* h2 : HFakeFactors2D) h2->Write("", TObject::kOverwrite);
    fOut.Close();
  }
}


void Estimate(TH2F* hData, const vector<TH2F*>& hMC, int xCut, int yCut, Double_t results[6],
  bool plotIntermediate = false, TString key = "", TString lumi = "") {

  TH2F* hFakeParts = (TH2F*) hData->Clone();
  for (TH2F* hMCTaus : hMC) {
    hFakeParts->Add(hMCTaus, -1.0); // Subtract MC particles
  }

  // Set negative entries to zero
  for (int i = 1; i <= hFakeParts->GetNbinsX(); i++) {
    for (int j = 1; j <= hFakeParts->GetNbinsY(); j++) {
      if (hFakeParts->GetBinContent(i, j) < 0) {
        hFakeParts->SetBinContent(i, j, 0.0);
        hFakeParts->SetBinError(i, j, 0.0);
      }
    }
  }

  if (doDetailedPlots && plotIntermediate) {
    TString pName = "../plot/" + key + "_fakes.pdf";
    PlotTH2F(hFakeParts, "Fake Taus", "Tau vs Jets WP", lumi, pName, ZBinLabels, WPBinLabels);
  }

  // Count the number of fake particles
  Double_t errA, errB, errC, errD;
  Int_t nBinsX = hFakeParts->GetXaxis()->GetNbins();
  Int_t nBinsY = hFakeParts->GetYaxis()->GetNbins();
  Double_t numA = hFakeParts->IntegralAndError(1, xCut, yCut + 1, nBinsY, errA); // Left top
  Double_t numC = hFakeParts->IntegralAndError(1, xCut, 1, yCut, errC); // Left bottom
  Double_t numB = hFakeParts->IntegralAndError(xCut + 1, nBinsX, yCut + 1, nBinsY, errB); // Right top
  Double_t numD = hFakeParts->IntegralAndError(xCut + 1, nBinsX, 1, yCut, errD); // Right bottom

  // Estimate fake factors
  Double_t ff, ffErr;
  if (numC == 0.0) {
    ff = 0.0; // ?
    ffErr = 0.0;
  }
  else {
    ff = numA / numC;
    if (ff == 0.0) ffErr = 0.0; // Case where numA = 0
    else ffErr = ff * sqrt((errA / numA) * (errA / numA) + (errC / numC) * (errC / numC));
  }

  // Estimate # of events prediction in signal region
  Double_t pred, predErr;
  if (ff == 0.0) {
    pred = 0.0; // ?
    predErr = 0.0;
  }
  else {
    pred = ff * numD;
    if (pred == 0.0) predErr = 0.0; // Case where numD = 0
    else predErr = pred * sqrt((ffErr / ff) * (ffErr / ff) + (errD / numD) * (errD / numD));
  }

  results[0] = ff;
  results[1] = ffErr;
  results[2] = pred;
  results[3] = predErr;
  results[4] = numB;
  results[5] = errB;
}


void PlotTH1F(TString name, TString xName, TString yName, std::vector<TH1F*> H1,
  std::vector<TString> hNames, Int_t rIdx, TString lumi) {

  Double_t maxi = -1.0;
  for (int i = 0; i < H1.size(); i++) {
    H1.at(i)->GetXaxis()->SetNoExponent();
    H1.at(i)->GetYaxis()->SetNoExponent();
    H1.at(i)->SetLineWidth(2);
    H1.at(i)->SetLineColor(COLORS[i]);
    H1.at(i)->SetMarkerStyle(20);
    H1.at(i)->SetMarkerSize(1.2);
    H1.at(i)->SetMarkerColor(COLORS[i]);
    maxi = maxi > H1.at(i)->GetMaximum() ? maxi : H1.at(i)->GetMaximum();
  }

  TCanvas* c = new TCanvas("c", "c", 50, 50, 865, 780);
  c->SetBottomMargin(0.12);
  c->SetLeftMargin(0.17);
  c->SetRightMargin(0.07);
  c->cd();

  TLegend* l = new TLegend(0.25, 0.7, 0.5, 0.88);
  l->SetBorderSize(0);
  l->SetTextFont(42);
  l->SetTextSize(0.028);

  H1.at(0)->GetXaxis()->SetTitle(xName);
  H1.at(0)->GetYaxis()->SetTitle(yName);
  H1.at(0)->GetYaxis()->SetRangeUser(0.0, 1.6 * maxi);
  H1.at(0)->Draw("HIST E");
  l->AddEntry(H1.at(0), hNames.at(0), "lep");
  for(int i = 1; i < H1.size(); i++) {
    H1.at(i)->Draw("HIST E SAME");
    l->AddEntry(H1.at(i), hNames.at(i), "lep");
  }

  l->Draw("SAME");

  TLatex* labelReg = new TLatex(0.5, 0.81, "2l+#tau_{h}" + REGIONS_NAME.at(rIdx).at(0));
  labelReg->SetTextSize(0.028);
  labelReg->SetNDC();
  labelReg->SetTextFont(42);
  labelReg->Draw("SAME");
  TLatex* labelCut1 = new TLatex(0.5, 0.73, REGIONS_NAME.at(rIdx).at(1));
  labelCut1->SetTextSize(0.028);
  labelCut1->SetNDC();
  labelCut1->SetTextFont(42);
  labelCut1->Draw("SAME");
  TLatex* labelCut2 = new TLatex(0.5, 0.65, REGIONS_NAME.at(rIdx).at(2));
  labelCut2->SetTextSize(0.028);
  labelCut2->SetNDC();
  labelCut2->SetTextFont(42);
  labelCut2->Draw("SAME");

  TLatex* labelCMS = new TLatex(0.175, 0.92, "CMS");
  labelCMS->SetTextSize(0.04);
  labelCMS->SetNDC();
  labelCMS->SetTextFont(61);
  labelCMS->Draw("SAME");
  TLatex* labelWIP = new TLatex(0.255, 0.92, "Work in Progress");
  labelWIP->SetTextSize(0.028);
  labelWIP->SetNDC();
  labelWIP->SetTextFont(52);
  labelWIP->Draw("SAME");
  // TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
  TLatex* labelLumi = new TLatex(0.74, 0.92, "2016 postVFP");
  labelLumi->SetTextSize(0.035);
  labelLumi->SetNDC();
  labelLumi->SetTextFont(42);
  labelLumi->Draw("SAME");

  c->Print("../plot/" + name + ".pdf");

  delete c;
}


void PlotTH1F(TString name, TString xName, TString yName, std::vector<std::vector<Double_t>> h,
  std::vector<std::vector<Double_t>> hErr, const std::vector<Double_t> binEdges,
  std::vector<TString> hNames, Int_t rIdx, TString lumi) {

  Double_t maxi = -1.0;
  std::vector<TH1F*> hists{};
  for (int i = 0; i < h.size(); i++) {
    TString hName = name + "_";
    hName += std::to_string(i); // Can't add TString and to_string output...
    TH1F* h1 = new TH1F(hName, "", binEdges.size() - 1, binEdges.data());
    for (int j = 0; j < h.at(i).size(); j++) {
      h1->SetBinContent(j + 1, h.at(i).at(j));
      h1->SetBinError(j + 1, hErr.at(i).at(j));
    }
    h1->GetXaxis()->SetNoExponent();
    h1->GetYaxis()->SetNoExponent();
    h1->SetLineWidth(2);
    h1->SetLineColor(COLORS[i]);
    h1->SetMarkerStyle(20);
    h1->SetMarkerSize(1.2);
    h1->SetMarkerColor(COLORS[i]);
    maxi = maxi > h1->GetMaximum() ? maxi : h1->GetMaximum();
    hists.push_back(h1);
  }

  TCanvas* c = new TCanvas("c", "c", 50, 50, 865, 780);
  c->SetBottomMargin(0.12);
  c->SetLeftMargin(0.17);
  c->SetRightMargin(0.07);
  c->cd();

  TLegend* l = new TLegend(0.25, 0.7, 0.5, 0.88);
  l->SetBorderSize(0);
  l->SetTextFont(42);
  l->SetTextSize(0.028);

  hists.at(0)->GetXaxis()->SetTitle(xName);
  hists.at(0)->GetYaxis()->SetTitle(yName);
  hists.at(0)->GetYaxis()->SetRangeUser(0.0, 1.6 * maxi);
  hists.at(0)->Draw("HIST E");
  l->AddEntry(hists.at(0), hNames.at(0), "lep");
  for(int i = 1; i < hists.size(); i++) {
    hists.at(i)->Draw("HIST E SAME");
    l->AddEntry(hists.at(i), hNames.at(i), "lep");
  }

  l->Draw("SAME");

  TLatex* labelReg = new TLatex(0.5, 0.81, "2l+#tau_{h}" + REGIONS_NAME.at(rIdx).at(0));
  labelReg->SetTextSize(0.028);
  labelReg->SetNDC();
  labelReg->SetTextFont(42);
  labelReg->Draw("SAME");
  TLatex* labelCut1 = new TLatex(0.5, 0.73, REGIONS_NAME.at(rIdx).at(1));
  labelCut1->SetTextSize(0.028);
  labelCut1->SetNDC();
  labelCut1->SetTextFont(42);
  labelCut1->Draw("SAME");
  TLatex* labelCut2 = new TLatex(0.5, 0.65, REGIONS_NAME.at(rIdx).at(2));
  labelCut2->SetTextSize(0.028);
  labelCut2->SetNDC();
  labelCut2->SetTextFont(42);
  labelCut2->Draw("SAME");

  TLatex* labelCMS = new TLatex(0.175, 0.92, "CMS");
  labelCMS->SetTextSize(0.04);
  labelCMS->SetNDC();
  labelCMS->SetTextFont(61);
  labelCMS->Draw("SAME");
  TLatex* labelWIP = new TLatex(0.255, 0.92, "Work in Progress");
  labelWIP->SetTextSize(0.028);
  labelWIP->SetNDC();
  labelWIP->SetTextFont(52);
  labelWIP->Draw("SAME");
  // TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
  TLatex* labelLumi = new TLatex(0.74, 0.92, "2016 postVFP");
  labelLumi->SetTextSize(0.035);
  labelLumi->SetNDC();
  labelLumi->SetTextFont(42);
  labelLumi->Draw("SAME");

  c->Print("../plot/" + name + ".pdf");

  delete c;
}


void PlotTH2F(TH2F* h2, TString xName, TString yName, TString lumi, TString pName,
  const std::vector<TString>& xBinLabels = {}, const std::vector<TString>& yBinLabels = {}) {

  h2->GetXaxis()->SetNoExponent();
  h2->GetYaxis()->SetNoExponent();
  // h2->GetZaxis()->SetNoExponent();

  h2->GetXaxis()->SetTitle(xName);
  h2->GetYaxis()->SetTitle(yName);
  h2->GetZaxis()->SetLabelSize(0.03);

  for (int b = 0; b < xBinLabels.size(); b++) {
    h2->GetXaxis()->SetBinLabel(b + 1, xBinLabels.at(b));
  }
  for (int b = 0; b < yBinLabels.size(); b++) {
    h2->GetYaxis()->SetBinLabel(b + 1, yBinLabels.at(b));
  }

  TCanvas* c = new TCanvas("c", "c", 50, 50, 865, 780);
  // c->SetGrid();
  c->SetBottomMargin(0.12);
  c->SetLeftMargin(0.17);
  c->SetRightMargin(0.12);
  c->cd();
  c->SetLogz(kTRUE);

  gStyle->SetPaintTextFormat("4.4f");

  h2->Draw("COLZ TEXT");

  TLatex* labelCMS = new TLatex(0.175, 0.92, "CMS");
  labelCMS->SetTextSize(0.04);
  labelCMS->SetNDC();
  labelCMS->SetTextFont(61);
  labelCMS->Draw();
  TLatex* labelWIP = new TLatex(0.255, 0.92, "Work in Progress");
  labelWIP->SetTextSize(0.028);
  labelWIP->SetNDC();
  labelWIP->SetTextFont(52);
  labelWIP->Draw();
  // TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
  TLatex* labelLumi = new TLatex(0.74, 0.92, "2016 postVFP");
  labelLumi->SetTextSize(0.035);
  labelLumi->SetNDC();
  labelLumi->SetTextFont(42);
  labelLumi->Draw();

  c->Print(pName);

  delete c;
}


TString GetLumi(TString year) {

  if (year == "2016") return "16.8";
  if (year == "2016APV") return "19.5";
  if (year == "2017") return "41.5";
  if (year == "2018") return "59.8";
  return "138";
}
