const TString YEARS[1] = {"2016"/*, "2016APV", "2017", "2018"*/};
const std::vector<TString> SAMPLES{"Data", "TX", "VV", "DY", "TT"};
const TString CHARGES[1] = {"OS"/*, "SS"*/};
const TString CHANNELS[2] = {"ee", /*"emu", */"mumu"};
const TString REGIONS[5] = {"ll", "llStl300", "llbtagg1p3", "llMetg20Jetgeq1B1",
  "llMetg20Jetgeq1B0"/*, "llStg300btagl1p3", "llStg300btagl1p3Tight"*/};
const TString VARS[1] = {"TauIdvsOnZ"};

// Fake factor bins
const std::vector<Double_t> PT_BINS = {20.0, 40.0, 60.0, 100.0, 220.0};
const std::vector<Double_t> ETA_BINS = {-2.3, -1.4, 1.4, 2.3};
const std::vector<Int_t> DM = {0, 1, 10, 11};

// Plot colors
const Int_t COLORS[3] = {4, 2};

// Plot axis labels
const std::vector<TString> xBinLabels{"On Z", "Off Z"};
const std::vector<TString> yBinLabels{"VVVLoose", "VVLoose", "VLoose", "Loose",
  "Medium", "Tight", "VTight", "VVTight"};


void Estimate(TH2F* hData, const vector<TH2F*>& hMC, int xCut, int yCut, Double_t results[6]);
void PlotTH1F(TString name, TString xName, TString yName, std::vector<std::vector<Double_t>> h,
  std::vector<std::vector<Double_t>> hErr, const std::vector<Double_t> binEdges,
  std::vector<TString> hNames, TString lumi);
void PlotTH2F(TH2F* h2, TString xName, TString yName,
  const std::vector<TString>& xBinLabels, const std::vector<TString>& yBinLabels,
  TString lumi, TString pName);
TString GetLumi(TString year);


void FakeFactor() {

  // Open and save histograms
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
              TString key = year + "_" + name + "_" + sample;
              TH2F* h = (TH2F*) f->Get<TH2F>(name)->Clone();
              // Set negative event counts due to NLO low statistics to 0
              for (int i = 1; i <= h->GetNbinsX(); i++) {
                for (int j = 1; j <= h->GetNbinsY(); j++) {
                  if (h->GetBinContent(i, j) < 0) {
                    h->SetBinContent(i, j, 0.0);
                    h->SetBinError(i, j, 0.0);
                  }
                }
              }
              H2.emplace(std::make_pair(key, h));

              for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {

                // snprintf(nameBin, 500, name + "_pt%.1fto%.1f", PT_BINS[pt], PT_BINS[pt + 1]);
                snprintf(nameBin, 500, name + "_pt%.0fto%.0f", PT_BINS[pt], PT_BINS[pt + 1]);
                TString keyBin = year + "_" + nameBin + "_" + sample;
                TH2F* hBin = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                // Set negative event counts due to NLO low statistics to 0
                for (int i = 1; i <= hBin->GetNbinsX(); i++) {
                  for (int j = 1; j <= hBin->GetNbinsY(); j++) {
                    if (hBin->GetBinContent(i, j) < 0) {
                      hBin->SetBinContent(i, j, 0.0);
                      hBin->SetBinError(i, j, 0.0);
                    }
                  }
                }
                H2.emplace(std::make_pair(keyBin, hBin));

                for (Int_t dm : DM) {

                  // snprintf(nameDM, 500, name + "_pt%.1fto%.1f_dm%d", PT_BINS[pt], PT_BINS[pt + 1], dm);
                  snprintf(nameDM, 500, name + "_pt%.0fto%.0f_dm%d", PT_BINS[pt], PT_BINS[pt + 1], dm);
                  TString keyDM = year + "_" + nameDM + "_" + sample;
                  TH2F* hDM = (TH2F*) f->Get<TH2F>(nameDM)->Clone();
                  // Set negative event counts due to NLO low statistics to 0
                  for (int i = 1; i <= hDM->GetNbinsX(); i++) {
                    for (int j = 1; j <= hDM->GetNbinsY(); j++) {
                      if (hDM->GetBinContent(i, j) < 0) {
                        hDM->SetBinContent(i, j, 0.0);
                        hDM->SetBinError(i, j, 0.0);
                      }
                    }
                  }
                  H2.emplace(std::make_pair(keyDM, hDM));
                }
              }
            }
          }
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
    for (TString charge : CHARGES) {
      for (TString channel : CHANNELS) {
        for (TString region : REGIONS) {
          for (TString var : VARS) {

            // Do fake factor estimation
            std::vector<std::vector<Double_t>> resEstFF{{}};
            std::vector<std::vector<Double_t>> resEstFFErr{{}};
            std::vector<std::vector<Double_t>> resEstPred{{}, {}};
            std::vector<std::vector<Double_t>> resEstPredErr{{}, {}};

            for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {
              std::vector<TH2F*> hMC{};
              for (int s = 1; s < SAMPLES.size(); s++) {
                // snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + region + "_"
                //   + var + "_pt%.1fto%.1f_" + SAMPLES[s], PT_BINS[pt], PT_BINS[pt + 1]);
                snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + region + "_"
                  + var + "_pt%.0fto%.0f_" + SAMPLES[s], PT_BINS[pt], PT_BINS[pt + 1]);
                hMC.push_back(H2.at(hKey));
              }
              // snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + region + "_"
              //   + var + "_pt%.1fto%.1f_Data", PT_BINS[pt], PT_BINS[pt + 1]);
              snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + region + "_"
                + var + "_pt%.0fto%.0f_Data", PT_BINS[pt], PT_BINS[pt + 1]);
              // std::cout << hKey << std::endl;
              Estimate(H2.at(hKey), hMC, 1, 5, results);
              resEstFF.at(0).push_back(results[0]);
              resEstFFErr.at(0).push_back(results[1]);
              resEstPred.at(0).push_back(results[2]);
              resEstPredErr.at(0).push_back(results[3]);
              resEstPred.at(1).push_back(results[4]);
              resEstPredErr.at(1).push_back(results[5]);

              for (TString dm : DM) {
                //
              }
            }

            pName = year + "_" + charge + "_" + channel + "_" + region + "_" + var;
            PlotTH1F(pName + "_ptEstFF", "Tau p_{T}", "Fake Factor", resEstFF, resEstFFErr,
              PT_BINS, {"Fake Factor"}, GetLumi(year));
            // PlotTH1F(pName + "_ptValEst", "Tau p_{T}", "Background Estimation", resEstPred,
            //   resEstPredErr, PT_BINS, {"Estimation", "Actual"}, GetLumi(year));

            // Plot some of the 2D histograms
            // for (TString sample : SAMPLES) {
            //   key = year + "_" + charge + "_" + channel + "_" + region + "_" + var + "_" + sample;
            //   pName = "../plot/" + key + ".pdf";
            //   PlotTH2F(H2.at(key), "All Events", "Tau vs Jets WP", xBinLabels, yBinLabels,
            //     GetLumi(year), pName);
            // }

            // Do validation of fake factor estimation
            for (TString sample : SAMPLES) {
              if (sample == "TT" || sample == "DY") {

                std::vector<std::vector<Double_t>> resValFF{{}};
                std::vector<std::vector<Double_t>> resValFFErr{{}};
                std::vector<std::vector<Double_t>> resValPred{{}, {}};
                std::vector<std::vector<Double_t>> resValPredErr{{}, {}};

                for (Int_t pt = 0; pt < PT_BINS.size() - 1; pt++) {

                  snprintf(hKey, 500, year + "_" + charge + "_" + channel + "_" + region + "_"
                    + var + "_pt%.0fto%.0f_" + sample, PT_BINS[pt], PT_BINS[pt + 1]);
                  // Double_t results[6];

                  Estimate(H2.at(hKey), hEmpty, 1, 5, results);
                  resValFF.at(0).push_back(results[0]);
                  resValFFErr.at(0).push_back(results[1]);
                  resValPred.at(0).push_back(results[2]);
                  resValPredErr.at(0).push_back(results[3]);
                  resValPred.at(1).push_back(results[4]);
                  resValPredErr.at(1).push_back(results[5]);
                }

                pName = year + "_" + charge + "_" + channel + "_" + region + "_" + var + "_" + sample;
                PlotTH1F(pName + "_ptValFF", "Tau p_{T}", "Fake Factor", resValFF, resValFFErr,
                  PT_BINS, {"Fake Factor"}, GetLumi(year));
                PlotTH1F(pName + "_ptValEst", "Tau p_{T}", "Background Estimation", resValPred,
                  resValPredErr, PT_BINS, {"Estimation", "Actual"}, GetLumi(year));
              }
            }
          }
        }
      }
    }
  }



  // Add LaTeX output functionality
}


void Estimate(TH2F* hData, const vector<TH2F*>& hMC, int xCut, int yCut, Double_t results[6]) {

  TH2F* hFakeParts = (TH2F*) hData->Clone();
  for (TH2F* hMCTaus : hMC) {
    hFakeParts->Add(hMCTaus, -1.0); // Subtract MC particles
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
    ff = -100.0;
    ffErr = 0.0;
  }
  else {
    ff = numA / numC;
    if (ff == 0.0) ffErr = 0.0; // Case where numA = 0
    else ffErr = ff * sqrt((errA / numA) * (errA / numA) + (errC / numC) * (errC / numC));
  }

  // Estimate # of events prediction in signal region
  Double_t pred, predErr;
  if (ff < 0.0) {
    pred = -100.0;
    predErr = 0.0;
  }
  else {
    pred = ff * numD;
    if (pred == 0.0) predErr = 0.0; // Case where ff = 0 or numD = 0
    else predErr = pred * sqrt((ffErr / ff) * (ffErr / ff) + (errD / numD) * (errD / numD));
  }

  results[0] = ff;
  results[1] = ffErr;
  results[2] = pred;
  results[3] = predErr;
  results[4] = numB;
  results[5] = errB;
}


void PlotTH1F(TString name, TString xName, TString yName, std::vector<std::vector<Double_t>> h,
  std::vector<std::vector<Double_t>> hErr, const std::vector<Double_t> binEdges,
  std::vector<TString> hNames, TString lumi) {

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
  TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
  labelLumi->SetTextSize(0.035);
  labelLumi->SetNDC();
  labelLumi->SetTextFont(42);
  labelLumi->Draw();

  c->Print("../plot/" + name + ".pdf");

  delete c;
}


void PlotTH2F(TH2F* h2, TString xName, TString yName,
  const std::vector<TString>& xBinLabels, const std::vector<TString>& yBinLabels,
  TString lumi, TString pName) {

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
  c->SetGrid();
  c->SetBottomMargin(0.12);
  c->SetLeftMargin(0.17);
  c->SetRightMargin(0.12);
  c->cd();
  c->SetLogz(kTRUE);

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
  TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
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
