#include "TFile.h"
#include "TString.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include <fstream>
#include <iostream>

const TString YEARS[1] = {"2016"/*, "2016APV", "2017", "2018", "All"*/};
const std::vector<TString> SAMPLES{"Data", "TX", "VV", "DY", "TT"};
const std::vector<TString> SAMPLES_NAME{"Data", "TT(X)", "VV(V)", "DY/ZZ", "TT"};
const TString CHARGES[2] = {"OS", "SS"};
const TString CHANNELS[3] = {"ee", "emu", "mumu"};
const std::vector<TString> REGIONS{
  "ll",
  "llOnZMetg20Jetgeq1",
  "llOffZMetg20B1",
  "llOffZMetg20B2",
  "llStl300",
  "llOnZ",
  "llbtagg1p3",
  "llStg300OffZbtagl1p3",
  "llStg300OffZbtagl1p3Tight",
  "llOffZ"
};
const std::vector<std::vector<TString>> REGIONS_NAME{
    {"No cuts", ""},
    {"p_{T}^{miss}>20GeV, njet#geq1", "OnZ (Z+jets CR)"},
    {"p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1 (SR)"},
    {"p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2 (t#bar{t}+jets CR)"},
    {"S_{T}<300GeV", "(CR)"},
    {"OnZ", "(Z+jets CR)"},
    {"btag>1.3", "(t#bar{t}+jets CR)"},
    {"S_{T}>300GeV, OffZ", "btag<1.3 (SR(Alt, Loose))"},
    {"S_{T}>300GeV, OffZ", "btag<1.3, njet#geq1 or S_{T}>500GeV (SR(Alt, Tight))"},
    {"OffZ", "(Close to SR CR)"}
};
const std::vector<TString> DOMAINS{
  "geqMedLepgeqTightTa",
  "geqMedLeplTightTa",
  // "geqMedLepgeqTightTaJetTaFF"
};
const std::vector<TString> DOMAINS_NAME{
  "#geq Tight Tau",
  "< Tight Tau",
  // "#geq Tight #tau, jet#rightarrow#tau FF"
};
const TString VARS1D[2] = {"taPtFFBin", "taEtaFFBin"};
const TString VARS2D[1] = {"taPtVsEta"};
// const TString VARS[4] = {"Ta", "FakeTa", "geqTightTa", "lTightTa"};

// Fake factor bins
// const std::vector<Double_t> PT_BINS = {20.0, 40.0, 60.0, 100.0, 220.0};
// const std::vector<Double_t> ETA_BINS = {0.0, 1.4, 2.3};
// const std::vector<Int_t> DM = {0, 1, 10, 11}; // 2 and 7 are empty

// Plot colors
const Int_t COLORS[2] = {4, 2};

// Plot axis labels
// const std::vector<TString> ZBinLabels{"On Z", "Off Z"};
// const std::vector<TString> WPBinLabels{"VVVLoose", "VVLoose", "VLoose", "Loose",
//   "Medium", "Tight", "VTight", "VVTight"};
// const std::vector<TString> DMBinLabels{"0", "1", "10", "11"};

// --------------------------------- //
bool doDetailedPlots = true;
// --------------------------------- //

// void Estimate(TH2F* hReal, const vector<TH2F*>& hFake, int xCut, int yCut, Double_t results[6],
//   bool doDebugPlots = false, TString key = "", TString lumi = "");
// void PlotTH1F(TString name, TString xName, TString yName,
//   std::vector<TH1F*> H1,
//   std::vector<TString> hNames, Int_t rIdx, TString lumi);
// void PlotTH2F(TH2F* h2, TString xName, TString yName, TString lumi, TString pName,
//   const std::vector<TString>& xBinLabels = {}, const std::vector<TString>& yBinLabels = {});
// TString GetLumi(TString year);

void JetToTauFakeFactors(TString inputFolder) {

  // Open files and save histograms
  std::map<TString, TH1F*> H1{};
  std::map<TString, TH2F*> H2{};
  for (TString year : YEARS) {
    for (TString sample : SAMPLES) {
      TString fName = "../hists/" + inputFolder + "/" + year + "_" + sample + ".root";
      std::cout << "Opening " << fName << std::endl;
      TFile* f = TFile::Open(fName);

      for (TString charge : CHARGES) {
        for (TString channel : CHANNELS) {
          for (TString region : REGIONS) {
            for (TString domain : DOMAINS) {
              for (TString var : VARS1D) {
                TString name = charge + "_" + channel + "_" + region + "_" + domain + "_" + var;
                TH1F* h1 = (TH1F*) f->Get(name)->Clone();
                H1.emplace(make_pair(year + "_" + sample + "_" + name, h1));
              } // End loop over 1D vars
              for (TString var : VARS1D) {
                TString name = charge + "_" + channel + "_" + region + "_" + domain + "_" + var;
                TH2F* h2 = (TH2F*) f->Get(name)->Clone();
                H2.emplace(make_pair(year + "_" + sample + "_" + name, h2));
              } // End loop over 2D vars
            } // End loop over domains
          } // End loop over regions
        } // End loop over channels
      } // End loop over charges
    } // End loop over samples
  } // End loop over years

  // Set negative event counts due to NLO low statistics to 0
  for (auto it = H1.cbegin(); it != H1.cend(); it++) {
    for (int i = 1; i <= it->second->GetNbinsX(); i++) {
      if (it->second->GetBinContent(i) < 0.0) {
        it->second->SetBinContent(i, 0.0);
        it->second->SetBinError(i, 0.0);
      }
    }
  }
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
  // for (TString year : YEARS) {
  //   for (TString charge : CHARGES) {
  //     for (TString channel : CHANNELS) {
  //       for (Int_t r = 0; r < REGIONS.size(); r++) {

  //         // Get data
  //         name = year + "_Data_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsPt";
  //         TH1F* ff = (TH1F*) H1.at(name)->Clone();
  //         name = year + "_Data_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsPt";
  //         TH1F* denom = (TH1F*) H1.at(name)->Clone();

  //         // Subtract "real" taus
  //         name = year + "_TX_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsPt";
  //         ff->Add(H1.at(name), -1.0);
  //         name = year + "_VV_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsPt";
  //         ff->Add(H1.at(name), -1.0);
  //         name = year + "_TX_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsPt";
  //         denom->Add(H1.at(name), -1.0);
  //         name = year + "_VV_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsPt";
  //         denom->Add(H1.at(name), -1.0);

  //         // Set negative entries to zero
  //         for (int i = 1; i <= ff->GetNbinsX(); i++) {
  //           if (ff->GetBinContent(i) < 0) {
  //             ff->SetBinContent(i, 0.0);
  //             ff->SetBinError(i, 0.0);
  //           }
  //         }
  //         for (int i = 1; i <= denom->GetNbinsX(); i++) {
  //           if (denom->GetBinContent(i) < 0) {
  //             denom->SetBinContent(i, 0.0);
  //             denom->SetBinError(i, 0.0);
  //           }
  //         }

  //         // Calculate fake factors
  //         ff->Divide(denom);

  //         PlotTH1F(year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_FFvsPt", "Tau p_{T}", "Fake Factor", {ff}, {"Fake Factor"}, r, GetLumi(year));





  //         // Get data
  //         name = year + "_Data_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsEta";
  //         ff = (TH1F*) H1.at(name)->Clone();
  //         name = year + "_Data_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsEta";
  //         denom = (TH1F*) H1.at(name)->Clone();

  //         // Subtract "real" taus
  //         name = year + "_TX_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsEta";
  //         ff->Add(H1.at(name), -1.0);
  //         name = year + "_VV_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsEta";
  //         ff->Add(H1.at(name), -1.0);
  //         name = year + "_TX_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsEta";
  //         denom->Add(H1.at(name), -1.0);
  //         name = year + "_VV_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsEta";
  //         denom->Add(H1.at(name), -1.0);

  //         // Set negative entries to zero
  //         for (int i = 1; i <= ff->GetNbinsX(); i++) {
  //           if (ff->GetBinContent(i) < 0) {
  //             ff->SetBinContent(i, 0.0);
  //             ff->SetBinError(i, 0.0);
  //           }
  //         }
  //         for (int i = 1; i <= denom->GetNbinsX(); i++) {
  //           if (denom->GetBinContent(i) < 0) {
  //             denom->SetBinContent(i, 0.0);
  //             denom->SetBinError(i, 0.0);
  //           }
  //         }

  //         // Calculate fake factors
  //         ff->Divide(denom);

  //         PlotTH1F(year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_FFvsEta", "Tau |#eta|", "Fake Factor", {ff}, {"Fake Factor"}, r, GetLumi(year));





  //         name = year + "_Data_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsPt_vsEta";
  //         TH2F* ff2 = (TH2F*) H2.at(name)->Clone();
  //         name = year + "_Data_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsPt_vsEta";
  //         TH2F* denom2 = (TH2F*) H2.at(name)->Clone();

  //         // Subtract "real" taus
  //         name = year + "_TX_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsPt_vsEta";
  //         ff2->Add(H2.at(name), -1.0);
  //         name = year + "_VV_" + charge + "_" + channel + "_" + REGIONS[r] + "_geqTightTa_vsPt_vsEta";
  //         ff2->Add(H2.at(name), -1.0);
  //         name = year + "_TX_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsPt_vsEta";
  //         denom2->Add(H2.at(name), -1.0);
  //         name = year + "_VV_" + charge + "_" + channel + "_" + REGIONS[r] + "_lTightTa_vsPt_vsEta";
  //         denom2->Add(H2.at(name), -1.0);

  //         // Set negative entries to zero
  //         for (int i = 1; i <= ff2->GetNbinsX(); i++) {
  //           for (int j = 1; j <= ff2->GetNbinsY(); j++) {
  //             if (ff2->GetBinContent(i, j) < 0) {
  //               ff2->SetBinContent(i, j, 0.0);
  //               ff2->SetBinError(i, j, 0.0);
  //             }
  //           }
  //         }
  //         for (int i = 1; i <= denom2->GetNbinsX(); i++) {
  //           for (int j = 1; j <= denom2->GetNbinsY(); j++) {
  //             if (denom2->GetBinContent(i, j) < 0) {
  //               denom2->SetBinContent(i, j, 0.0);
  //               denom2->SetBinError(i, j, 0.0);
  //             }
  //           }
  //         }

  //         // Calculate fake factors
  //         ff2->Divide(denom2);

  //         PlotTH2F(ff2, "Tau p_{T}", "Tau |#eta|", GetLumi(year), year + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_FFvsPtvsEta");





  //         for (TString sample : SAMPLES) {
  //           if (sample == "Data") continue;
  //           name = year + "_" + sample + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_FakeTa_vsPt_vsEta";
  //           TH2F* fakeTauPurity = (TH2F*) H2.at(name)->Clone();
  //           name = year + "_" + sample + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_Ta_vsPt_vsEta";
  //           TH2F* allTau = (TH2F*) H2.at(name)->Clone();
  //           fakeTauPurity->Divide(allTau);
  //           PlotTH2F(fakeTauPurity, "Tau p_{T}", "Tau |#eta|", GetLumi(year), year + "_" + sample + "_" + charge + "_" + channel + "_" + REGIONS[r] + "_fakeTauPurity");
  //         }
  //       } // End loop over regions
  //     } // End loop over channels
  //   } // End loop over charges
  // } // End loop over years
}


// void Estimate(TH2F* hReal, const vector<TH2F*>& hFake, int xCut, int yCut, Double_t results[6],
//   bool doDebugPlots = false, TString key = "", TString lumi = "") {

//   TH2F* hFakeParts = (TH2F*) hReal->Clone();
//   for (TH2F* hFakeTaus : hFake) {
//     hFakeParts->Add(hFakeTaus, -1.0); // Subtract MC particles
//   }

//   // Set negative entries to zero
//   for (int i = 1; i <= hFakeParts->GetNbinsX(); i++) {
//     for (int j = 1; j <= hFakeParts->GetNbinsY(); j++) {
//       if (hFakeParts->GetBinContent(i, j) < 0) {
//         hFakeParts->SetBinContent(i, j, 0.0);
//         hFakeParts->SetBinError(i, j, 0.0);
//       }
//     }
//   }

//   // if (doDebugPlots) {
//   //   TString pName = "../plot/" + key + "_fakes.pdf";
//   //   PlotTH2F(hFakeParts, "Fake Taus", "Tau vs Jets WP", lumi, pName, ZBinLabels, WPBinLabels);
//   // }

//   // Count the number of fake particles
//   Double_t errA, errB, errC, errD;
//   Int_t nBinsX = hFakeParts->GetXaxis()->GetNbins();
//   Int_t nBinsY = hFakeParts->GetYaxis()->GetNbins();
//   Double_t numA = hFakeParts->IntegralAndError(1, xCut, yCut + 1, nBinsY, errA); // Left top
//   Double_t numC = hFakeParts->IntegralAndError(1, xCut, 1, yCut, errC); // Left bottom
//   Double_t numB = hFakeParts->IntegralAndError(xCut + 1, nBinsX, yCut + 1, nBinsY, errB); // Right top
//   Double_t numD = hFakeParts->IntegralAndError(xCut + 1, nBinsX, 1, yCut, errD); // Right bottom

//   // Estimate fake factors
//   Double_t ff, ffErr;
//   if (numC == 0.0) {
//     ff = 0.0; // ?
//     ffErr = 0.0;
//   }
//   else {
//     ff = numA / numC;
//     if (ff == 0.0) ffErr = 0.0; // Case where numA = 0
//     else ffErr = ff * sqrt((errA / numA) * (errA / numA) + (errC / numC) * (errC / numC));
//   }

//   // Estimate # of events prediction in signal region
//   Double_t pred, predErr;
//   if (ff == 0.0) {
//     pred = 0.0; // ?
//     predErr = 0.0;
//   }
//   else {
//     pred = ff * numD;
//     if (pred == 0.0) predErr = 0.0; // Case where numD = 0
//     else predErr = pred * sqrt((ffErr / ff) * (ffErr / ff) + (errD / numD) * (errD / numD));
//   }

//   results[0] = ff;
//   results[1] = ffErr;
//   results[2] = pred;
//   results[3] = predErr;
//   results[4] = numB;
//   results[5] = errB;
// }


// void PlotTH1F(TString name, TString xName, TString yName, std::vector<TH1F*> H1,
//   std::vector<TString> hNames, Int_t rIdx, TString lumi) {

//   Double_t maxi = -1.0;
//   for (int i = 0; i < H1.size(); i++) {
//     H1.at(i)->GetXaxis()->SetNoExponent();
//     H1.at(i)->GetYaxis()->SetNoExponent();
//     H1.at(i)->SetLineWidth(2);
//     H1.at(i)->SetLineColor(COLORS[i]);
//     H1.at(i)->SetMarkerStyle(20);
//     H1.at(i)->SetMarkerSize(1.2);
//     H1.at(i)->SetMarkerColor(COLORS[i]);
//     maxi = maxi > H1.at(i)->GetMaximum() ? maxi : H1.at(i)->GetMaximum();
//   }

//   TCanvas* c = new TCanvas("c", "c", 50, 50, 865, 780);
//   c->SetBottomMargin(0.12);
//   c->SetLeftMargin(0.17);
//   c->SetRightMargin(0.07);
//   c->cd();

//   TLegend* l = new TLegend(0.25, 0.7, 0.5, 0.88);
//   l->SetBorderSize(0);
//   l->SetTextFont(42);
//   l->SetTextSize(0.028);

//   H1.at(0)->GetXaxis()->SetTitle(xName);
//   H1.at(0)->GetYaxis()->SetTitle(yName);
//   H1.at(0)->GetYaxis()->SetRangeUser(0.0, 1.6 * maxi);
//   H1.at(0)->Draw("HIST E");
//   l->AddEntry(H1.at(0), hNames.at(0), "lep");
//   for(int i = 1; i < H1.size(); i++) {
//     H1.at(i)->Draw("HIST E SAME");
//     l->AddEntry(H1.at(i), hNames.at(i), "lep");
//   }

//   l->Draw("SAME");

//   TLatex* labelReg = new TLatex(0.5, 0.81, "l+#tau_{h}" + REGIONS_NAME.at(rIdx).at(0));
//   labelReg->SetTextSize(0.028);
//   labelReg->SetNDC();
//   labelReg->SetTextFont(42);
//   labelReg->Draw("SAME");
//   TLatex* labelCut1 = new TLatex(0.5, 0.73, REGIONS_NAME.at(rIdx).at(1));
//   labelCut1->SetTextSize(0.028);
//   labelCut1->SetNDC();
//   labelCut1->SetTextFont(42);
//   labelCut1->Draw("SAME");
//   TLatex* labelCut2 = new TLatex(0.5, 0.65, REGIONS_NAME.at(rIdx).at(2));
//   labelCut2->SetTextSize(0.028);
//   labelCut2->SetNDC();
//   labelCut2->SetTextFont(42);
//   labelCut2->Draw("SAME");

//   TLatex* labelCMS = new TLatex(0.175, 0.92, "CMS");
//   labelCMS->SetTextSize(0.04);
//   labelCMS->SetNDC();
//   labelCMS->SetTextFont(61);
//   labelCMS->Draw("SAME");
//   TLatex* labelWIP = new TLatex(0.255, 0.92, "Work in Progress");
//   labelWIP->SetTextSize(0.028);
//   labelWIP->SetNDC();
//   labelWIP->SetTextFont(52);
//   labelWIP->Draw("SAME");
//   // TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
//   TLatex* labelLumi = new TLatex(0.74, 0.92, "2016 postVFP");
//   labelLumi->SetTextSize(0.035);
//   labelLumi->SetNDC();
//   labelLumi->SetTextFont(42);
//   labelLumi->Draw("SAME");

//   c->Print("../plot/" + name + ".pdf");

//   delete c;
// }


// void PlotTH2F(TH2F* h2, TString xName, TString yName, TString lumi, TString pName,
//   const std::vector<TString>& xBinLabels = {}, const std::vector<TString>& yBinLabels = {}) {

//   h2->GetXaxis()->SetNoExponent();
//   h2->GetYaxis()->SetNoExponent();
//   // h2->GetZaxis()->SetNoExponent();

//   h2->GetXaxis()->SetTitle(xName);
//   h2->GetYaxis()->SetTitle(yName);
//   h2->GetZaxis()->SetLabelSize(0.03);

//   for (int b = 0; b < xBinLabels.size(); b++) {
//     h2->GetXaxis()->SetBinLabel(b + 1, xBinLabels.at(b));
//   }
//   for (int b = 0; b < yBinLabels.size(); b++) {
//     h2->GetYaxis()->SetBinLabel(b + 1, yBinLabels.at(b));
//   }

//   TCanvas* c = new TCanvas("c", "c", 50, 50, 865, 780);
//   // c->SetGrid();
//   c->SetBottomMargin(0.12);
//   c->SetLeftMargin(0.17);
//   c->SetRightMargin(0.12);
//   c->cd();
//   c->SetLogz(kTRUE);

//   gStyle->SetPaintTextFormat("4.4f");

//   h2->Draw("COLZ TEXT");

//   TLatex* labelCMS = new TLatex(0.175, 0.92, "CMS");
//   labelCMS->SetTextSize(0.04);
//   labelCMS->SetNDC();
//   labelCMS->SetTextFont(61);
//   labelCMS->Draw();
//   TLatex* labelWIP = new TLatex(0.255, 0.92, "Work in Progress");
//   labelWIP->SetTextSize(0.028);
//   labelWIP->SetNDC();
//   labelWIP->SetTextFont(52);
//   labelWIP->Draw();
//   // TLatex* labelLumi = new TLatex(0.705, 0.92, lumi + " fb^{-1} (13 TeV)");
//   TLatex* labelLumi = new TLatex(0.74, 0.92, "2016 postVFP");
//   labelLumi->SetTextSize(0.035);
//   labelLumi->SetNDC();
//   labelLumi->SetTextFont(42);
//   labelLumi->Draw();

//   c->Print("../plot/" + pName + ".pdf");

//   delete c;
// }


TString GetLumi(TString year) {
  if (year == "2016") return "16.8";
  if (year == "2016APV") return "19.5";
  if (year == "2017") return "41.5";
  if (year == "2018") return "59.8";
  return "138";
}
