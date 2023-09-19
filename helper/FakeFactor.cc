const TString YEARS[1] = {"2016"/*, "2016APV", "2017", "2018"*/};
const TString SAMPLES[5] = {"Data", "TX", "VV", "DY", "TT"};
// include these from MyAnalysis.cc?
const TString CHARGES[1] = {"OS"/*, "SS"*/};
const TString CHANNELS[2] = {"ee", /*"emu", */"mumu"};
const TString REGIONS[5] = {"ll", "llStl300", "llbtagg1p3", "llMetg20Jetgeq1B1",
  "llMetg20Jetgeq1B0"/*, "llStg300btagl1p3", "llStg300btagl1p3Tight"*/};
const TString VARS[1] = {"TauIdvsOnZ"};

// Fake factor bins
// include these from MyAnalysis.cc?
const Int_t N_PT = 5;
// const TString PT_BINS[N_PT] = {"20.0", "40.0", "60.0", "100.0", "220.0"};
const TString PT_BINS[N_PT] = {"20", "40", "60", "100", "220"};
const Int_t N_ETA = 4;
const TString ETA_BINS[N_ETA] = {"-2.3", "-1.4", "1.4", "2.3"};
const TString DM[4] = {"0", "1", "10", "11"};

// Plot axis labels
const std::vector<TString> xBinLabels{"On Z", "Off Z"};
const std::vector<TString> yBinLabels{"VVVLoose", "VVLoose", "VLoose", "Loose",
  "Medium", "Tight", "VTight", "VVTight"};


void Calculate(TH2F* hData, const vector<TH2F*>& hMC, int xCut, int yCut, Double_t results[6]);
void PlotTH2F(TH2F* h2, TString xName, TString yName,
  const std::vector<TString>& xBinLabels, const std::vector<TString>& yBinLabels,
  TString lumi, TString pName);
TString GetLumi(TString year);


void FakeFactor() {

  // Open and save histograms
  std::map<TString, TH2F*> H2{};

  // TString fName, hName, hNameNew, pName;
  // std::vector<TH2F*> hEmpty{};

  for (TString sample : SAMPLES) {
    for (TString year : YEARS) {

      TString fName = "../hists/" + year + "_" + sample + ".root";
      TFile* f = TFile::Open(fName);

      for (TString charge : CHARGES) {
        for (TString channel : CHANNELS) {
          for (TString region : REGIONS) {
            for (TString var : VARS) {
              TString name = charge + "_" + channel + "_" + region + "_" + var;
              TString key = year + "_" + name + "_" + sample;
              TH2F* h = (TH2F*) f->Get<TH2F>(name)->Clone();
              H2.emplace(std::make_pair(key, h));
              // std::cout << h->GetBinContent(1, 1) << std::endl;
              // H2[key] = h;
              // std::cout << "map size: " << H2.size() << std::endl;

              for (Int_t pt = 0; pt < N_PT - 1; pt++) {
                TString nameBin = name + "_pt" + PT_BINS[pt] + "to" + PT_BINS[pt + 1];
                TString keyBin = year + "_" + nameBin + "_" + sample;
                TH2F* hBin = (TH2F*) f->Get<TH2F>(nameBin)->Clone();
                H2.emplace(std::make_pair(keyBin, hBin));

                for (TString dm : DM) {
                  TString nameDM = nameBin + "_dm" + dm;
                  TString keyDM = year + "_" + nameDM + "_" + sample;
                  // std::cout << keyDM << std::endl;
                  TH2F* hDM = (TH2F*) f->Get<TH2F>(nameDM)->Clone();
                  H2.emplace(std::make_pair(keyDM, hDM));
                }
              }

              // std::cout << H2.at("2016_OS_ee_ll_TauIdvsOnZ_pt20to40_dm0_Data")->GetBinContent(1, 1) << std::endl;

              // hName = charge + "_" + channel + "_" + region + "_TauIdvsOnZ";

              // fName = "../hists/" + year + "_Data.root";
              // TFile* fData = TFile::Open(fName);
              // TH2F* hData = (TH2F*) fData->Get<TH2F>(hName)->Clone();
              // pName = "../plot/" + year + "_" + hName + "_Data.pdf";
              // // PlotTH2F(hData, "All Events", "Tau vs Jets WP",
              // //   xBinLabels, yBinLabels, GetLumi(year), pName);

              // std::vector<TH2F*> hMC{};
              // for (TString mc : MC_SAMPLES) {
              //   fName = "../hists/" + year + "_" + mc + ".root";
              //   TFile* f = TFile::Open(fName);
              //   TH2F* hist = (TH2F*) f->Get<TH2F>(hName)->Clone();
              //   hMC.push_back(hist);
              //   pName = "../plot/" + year + "_" + hName + "_" + mc + ".pdf";
              //   // PlotTH2F(hist, "All Events", "Tau vs Jets WP",
              //   //   xBinLabels, yBinLabels, GetLumi(year), pName);
              // }

              // std::vector<Double_t> {};
              // for (Int_t pt = 0; pt < N_PT; pt++) {

              //   hNameNew = 

              //   fName = "../hists/" + year + "_Data.root";
              //   TFile* fData = TFile::Open(fName);
              //   TH2F* hData = (TH2F*) fData->Get<TH2F>(hName)->Clone();
              //   pName = "../plot/" + year + "_" + hName + "_Data.pdf";
              //   // PlotTH2F(hData, "All Events", "Tau vs Jets WP",
              //   //   xBinLabels, yBinLabels, GetLumi(year), pName);

              //   std::vector<TH2F*> hMC{};
              //   for (TString mc : MC_SAMPLES) {
              //     fName = "../hists/" + year + "_" + mc + ".root";
              //     TFile* f = TFile::Open(fName);
              //     TH2F* hist = (TH2F*) f->Get<TH2F>(hName)->Clone();
              //     hMC.push_back(hist);
              //     pName = "../plot/" + year + "_" + hName + "_" + mc + ".pdf";
              //     // PlotTH2F(hist, "All Events", "Tau vs Jets WP",
              //     //   xBinLabels, yBinLabels, GetLumi(year), pName);
              //   }
              // }



              // Validation plots


              // std::cout << hName << std::endl;
              // Double_t results[6];
              // Calculate(hData, hMC, 1, 5, results);
              // Calculate(hMC.at(3), hEmpty, 1, 5, results); // Validation
              // for (Double_t n : results) {
              //   std::cout << n << " ";
              // }
              // std::cout << std::endl;
            }
          }
        }
      }

      // f->Close();
    }
  }

  TString hKey, pName;
  for (TString sample : SAMPLES) {
    for (TString year : YEARS) {
      for (TString charge : CHARGES) {
        for (TString channel : CHANNELS) {
          for (TString region : REGIONS) {
            for (TString var : VARS) {
              hKey = year + "_" + charge + "_" + channel + "_" + region + "_" + var + "_" + sample;
              pName = "../plot/" + hKey + ".pdf";
              PlotTH2F(H2.at(hKey), "All Events", "Tau vs Jets WP",
                xBinLabels, yBinLabels, GetLumi(year), pName);
            }
          }
        }
      }
    }
  }



  // Add LaTeX output functionality
}


void Calculate(TH2F* hData, const vector<TH2F*>& hMC, int xCut, int yCut, Double_t results[6]) {

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

  // Set negative event counts due to NLO low statistics to 0
  if (numA < 0.0) {
    numA = 0.0;
    errA = 0.0;
  }
  if (numB < 0.0) {
    numB = 0.0;
    errB = 0.0;
  }
  if (numC < 0.0) {
    numC = 0.0;
    errC = 0.0;
  }
  if (numD < 0.0) {
    numD = 0.0;
    errD = 0.0;
  }

  // Calculate fake factors
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

  // Calculate # of events prediction in signal region
  Double_t pred, predErr;
  if (ff < 0.0/* || numD == 0.0*/) {
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


TString GetLumi(TString year) {

  if (year == "2016") return "16.8";
  if (year == "2016APV") return "19.5";
  if (year == "2017") return "41.5";
  if (year == "2018") return "59.8";
  return "138";
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

  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);

  c->Print(pName);

  delete c;
}
