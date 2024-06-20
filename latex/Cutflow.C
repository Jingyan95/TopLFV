#include "TFile.h"
#include "TString.h"
#include "TH1F.h"
#include <fstream>
#include <iostream>

const TString YEARS[1] = {"2016"/*, "2016APV", "2017", "2018"*/};
const std::vector<TString> SAMPLES{"Data", "TX", "VV", "DY", "TT", "LFVStScalarU", "LFVTtScalarU"};
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
  "llStg300OffZbtagl1p3Tight"
};
const std::vector<TString> REGIONS_LATEX{
  "2$l+\\tau_h$, no cuts",
  "2$l+\\tau_h$, Z+jets CR, On Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$",
  "2$l+\\tau_h$, SR, Off Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$",
  "2$l+\\tau_h$, $t\\bar{t}$ + jets CR, Off Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=2$",
  "2$l+\\tau_h$, CR, $S_T<300$ GeV",
  "2$l+\\tau_h$, Z+jets CR, On Z",
  "2$l+\\tau_h$, $t\\bar{t}$ + jets CR, btag $>1.3$",
  "2$l+\\tau_h$, SR(Alt, Loose), btag $<1.3$",
  "2$l+\\tau_h$, SR(Alt, Tight), btag $<1.3$, njet $\\geq 1$ or $S_T>500$ GeV"
};
const std::vector<TString> TABLE_LATEX{"Data", "$t\\bar{t}X$", "VV", "DY",
  "$t\\bar{t}$", "St Scalar U", "Tt Scalar U", "Background", "Signal"};

void Fill(TH1F* h, std::vector<std::vector<Double_t>>& cutflow, 
  std::vector<std::vector<Double_t>>& cutflowErr, Int_t idx);

void Cutflow(TString inputFolder) {

  // Open files and save histograms
  std::map<TString, TH1F*> H{};
  for (TString year : YEARS) {
    for (TString sample : SAMPLES) {

      TString filename = "../hists/" + inputFolder + "/" + year + "_" + sample + ".root";
      TFile* f = TFile::Open(filename);

      for (TString region : REGIONS) {
        TString key = year + "_" + region + "_subSR_" + sample;
        TH1F* hSubSR = new TH1F(key, "", 18, 0, 18);
        for (TString charge : CHARGES) {
          for (TString channel : CHANNELS) {
            TString histname = charge + "_" + channel + "_" + region + "_geqMedLepgeqTightTa_subSR";
            TH1F* h = (TH1F*) f->Get(histname)->Clone();
            if (charge == "OS" && channel == "ee") {
              hSubSR->SetBinContent(1, h->GetBinContent(1));
              hSubSR->SetBinError(1, h->GetBinError(1));
              hSubSR->SetBinContent(2, h->GetBinContent(2));
              hSubSR->SetBinError(2, h->GetBinError(2));
            }
            else if (charge == "OS" && channel == "emu") {
              hSubSR->SetBinContent(3, h->GetBinContent(3));
              hSubSR->SetBinError(3, h->GetBinError(3));
              hSubSR->SetBinContent(4, h->GetBinContent(4));
              hSubSR->SetBinError(4, h->GetBinError(4));
              hSubSR->SetBinContent(5, h->GetBinContent(5));
              hSubSR->SetBinError(5, h->GetBinError(5));
              hSubSR->SetBinContent(6, h->GetBinContent(6));
              hSubSR->SetBinError(6, h->GetBinError(6));
              hSubSR->SetBinContent(7, h->GetBinContent(7));
              hSubSR->SetBinError(7, h->GetBinError(7));
              hSubSR->SetBinContent(8, h->GetBinContent(8));
              hSubSR->SetBinError(8, h->GetBinError(8));
            }
            else if (charge == "OS" && channel == "mumu") {
              hSubSR->SetBinContent(9, h->GetBinContent(9));
              hSubSR->SetBinError(9, h->GetBinError(9));
              hSubSR->SetBinContent(10, h->GetBinContent(10));
              hSubSR->SetBinError(10, h->GetBinError(10));
            }
            else if (charge == "SS" && channel == "ee") {
              hSubSR->SetBinContent(11, h->GetBinContent(11));
              hSubSR->SetBinError(11, h->GetBinError(11));
              hSubSR->SetBinContent(12, h->GetBinContent(12));
              hSubSR->SetBinError(12, h->GetBinError(12));
            }
            else if (charge == "SS" && channel == "emu") {
              hSubSR->SetBinContent(13, h->GetBinContent(13));
              hSubSR->SetBinError(13, h->GetBinError(13));
              hSubSR->SetBinContent(14, h->GetBinContent(14));
              hSubSR->SetBinError(14, h->GetBinError(14));
              hSubSR->SetBinContent(15, h->GetBinContent(15));
              hSubSR->SetBinError(15, h->GetBinError(15));
              hSubSR->SetBinContent(16, h->GetBinContent(16));
              hSubSR->SetBinError(16, h->GetBinError(16));
            }
            else if (charge == "SS" && channel == "mumu") {
              hSubSR->SetBinContent(17, h->GetBinContent(17));
              hSubSR->SetBinError(17, h->GetBinError(17));
              hSubSR->SetBinContent(18, h->GetBinContent(18));
              hSubSR->SetBinError(18, h->GetBinError(18));
            }
          }
        }
        H.emplace(std::make_pair(key, hSubSR));
      }
    }
  }

  // Set negative event counts due to NLO low statistics to 0
  for (auto it = H.cbegin(); it != H.cend(); it++) {
    for (int i = 1; i <= it->second->GetNbinsX(); i++) {
      if (it->second->GetBinContent(i) < 0.0) {
        it->second->SetBinContent(i, 0.0);
      }
    }
  }

  // Start LaTeX document
  char text[1000];
  ofstream fout;
  fout.open("Cutflow_Tables.tex");
  fout << "\\documentclass{beamer}\n";
  fout << "\\usepackage[orientation = landscape, size = custom, width = 16, height = 12, scale = 0.5]{beamerposter}\n";
  fout << "\n";
  fout << "\\title{\\textbf{Cutflow Tables}}\n";
  fout << "\\author{Author}\n";
  fout << "\n";
  fout << "\\begin{document}\n";
  fout << "\n";
  fout << "  \\begin{frame}\n";
  fout << "    \\maketitle\n";
  fout << "  \\end{frame}\n";
  fout << "\n";
  fout << "  \\begin{frame}{\\textbf{Table of contents}}\n";
  fout << "    \\tableofcontents\n";
  fout << "  \\end{frame}\n";
  fout << "\n";

  // Get counts
  for (TString year : YEARS) {
    bool firstOfYear = true;
    for (unsigned int r = 0; r < REGIONS.size(); r++) {

      // Initialize containers for cutflow table
      std::vector<std::vector<Double_t>> cutflow = {
        {}, {}, {}, {}, {}, {}, {}, {}, {},
        {}, {}, {}, {}, {}, {}, {}, {}, {}}; // 18
      for (std::vector<Double_t>& vec : cutflow) {
        for (int i = 0; i < 10; i++) vec.push_back(0.0);
      }
      std::vector<std::vector<Double_t>> cutflowErr = {
        {}, {}, {}, {}, {}, {}, {}, {}, {},
        {}, {}, {}, {}, {}, {}, {}, {}, {}}; // 18
      for (std::vector<Double_t>& vec : cutflowErr) {
        for (int i = 0; i < 9; i++) vec.push_back(0.0);
      }

      // Calculate cutflow table
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[0]), cutflow, cutflowErr, 0);
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[1]), cutflow, cutflowErr, 1);
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[2]), cutflow, cutflowErr, 2);
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[3]), cutflow, cutflowErr, 3);
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[4]), cutflow, cutflowErr, 4);
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[5]), cutflow, cutflowErr, 5);
      Fill(H.at(year + "_" + REGIONS[r] + "_subSR_" + SAMPLES[6]), cutflow, cutflowErr, 6);
      // Calculating background
      for (unsigned int b = 0; b < cutflow.size(); b++) {
        cutflow.at(b).at(7) += cutflow.at(b).at(1) + cutflow.at(b).at(2)
          + cutflow.at(b).at(3) + cutflow.at(b).at(4);
        cutflowErr.at(b).at(7) += sqrt(cutflowErr.at(b).at(1) * cutflowErr.at(b).at(1)
          + cutflowErr.at(b).at(2) * cutflowErr.at(b).at(2)
          + cutflowErr.at(b).at(3) * cutflowErr.at(b).at(3)
          + cutflowErr.at(b).at(4) * cutflowErr.at(b).at(4));
      }
      // Calculating signal
      for (unsigned int b = 0; b < cutflow.size(); b++) {
        cutflow.at(b).at(8) += cutflow.at(b).at(5) + cutflow.at(b).at(6);
        cutflowErr.at(b).at(8) += sqrt(cutflowErr.at(b).at(5) * cutflowErr.at(b).at(5)
          + cutflowErr.at(b).at(6) * cutflowErr.at(b).at(6));
      }
      // Calculating S/sqrt(B)
      for (unsigned int b = 0; b < cutflow.size(); b++) {
        cutflow.at(b).at(9) += cutflow.at(b).at(8) / sqrt(cutflow.at(b).at(7));
      }

      // Writing cutflow table to LaTeX format
      if (firstOfYear) {
        fout << "  \\section{" + year + "}\n";
        fout << "\n";
        firstOfYear = false;
      }
      fout << "  \\subsection{" + REGIONS_LATEX[r] + "}\n";
      fout << "  \\begin{frame}{\\textbf{" + year + "}}\n";
      fout << "    \\begin{itemize}\n";
      fout << "      \\item " + REGIONS_LATEX[r] + "\n";
      fout << "    \\end{itemize}\n";
      fout << "    \\makebox[\\textwidth]{\n";
      fout << "      \\tiny\n";
      fout << "      \\begin{tabular}{ | l | l | l | l | l | l | l | }\n";
      fout << "        \\hline\n";
      fout << "        Mass & OS-$ee$ & OS-$ee$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ & OS-$e\\mu$ \\\\\n";
      fout << "        Region & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV & $m(e\\mu)<150$GeV & $m(e\\mu)>150$GeV & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV \\\\\n";
      fout << "        \\hline\n";
      for (unsigned int s = 0; s < TABLE_LATEX.size(); s++) {
        if (s == 5 || s == 6 || s == 8) {
          snprintf(text, 1000, "        " + TABLE_LATEX[s]
            + " & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f"
            + " & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f \\\\\n",
            cutflow.at(0).at(s), cutflowErr.at(0).at(s),
            cutflow.at(1).at(s), cutflowErr.at(1).at(s),
            cutflow.at(2).at(s), cutflowErr.at(2).at(s),
            cutflow.at(3).at(s), cutflowErr.at(3).at(s),
            cutflow.at(4).at(s), cutflowErr.at(4).at(s),
            cutflow.at(5).at(s), cutflowErr.at(5).at(s));
          fout << text;
        }
        else {
          snprintf(text, 1000, "        " + TABLE_LATEX[s]
            + " & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f"
            + " & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f \\\\\n",
            cutflow.at(0).at(s), cutflowErr.at(0).at(s),
            cutflow.at(1).at(s), cutflowErr.at(1).at(s),
            cutflow.at(2).at(s), cutflowErr.at(2).at(s),
            cutflow.at(3).at(s), cutflowErr.at(3).at(s),
            cutflow.at(4).at(s), cutflowErr.at(4).at(s),
            cutflow.at(5).at(s), cutflowErr.at(5).at(s));
          fout << text;
        }
        if (s == 0 || s == 4 || s == 6 || s == 8) fout << "        \\hline\n";
      }
      snprintf(text, 1000, "        $S/\\sqrt{B}$ & %.4f & %.4f & %.4f & %.4f & %.4f & %.4f \\\\\n",
        cutflow.at(0).at(9), cutflow.at(1).at(9), cutflow.at(2).at(9),
        cutflow.at(3).at(9), cutflow.at(4).at(9), cutflow.at(5).at(9));
      fout << text;
      fout << "        \\hline\n";
      fout << "        \\hline\n";
      fout << "        Mass & OS-$e\\mu$ & OS-$e\\mu$ & OS-$\\mu\\mu$ & OS-$\\mu\\mu$ & SS-$ee$ & SS-$ee$ \\\\\n";
      fout << "        Region & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV \\\\\n";
      fout << "        \\hline\n";
      for (unsigned int s = 0; s < TABLE_LATEX.size(); s++) {
        if (s == 5 || s == 6 || s == 8) {
          snprintf(text, 1000, "        " + TABLE_LATEX[s]
            + " & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f"
            + " & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f \\\\\n",
            cutflow.at(6).at(s), cutflowErr.at(6).at(s),
            cutflow.at(7).at(s), cutflowErr.at(7).at(s),
            cutflow.at(8).at(s), cutflowErr.at(8).at(s),
            cutflow.at(9).at(s), cutflowErr.at(9).at(s),
            cutflow.at(10).at(s), cutflowErr.at(10).at(s),
            cutflow.at(11).at(s), cutflowErr.at(11).at(s));
          fout << text;
        }
        else {
          snprintf(text, 1000, "        " + TABLE_LATEX[s]
            + " & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f"
            + " & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f \\\\\n",
            cutflow.at(6).at(s), cutflowErr.at(6).at(s),
            cutflow.at(7).at(s), cutflowErr.at(7).at(s),
            cutflow.at(8).at(s), cutflowErr.at(8).at(s),
            cutflow.at(9).at(s), cutflowErr.at(9).at(s),
            cutflow.at(10).at(s), cutflowErr.at(10).at(s),
            cutflow.at(11).at(s), cutflowErr.at(11).at(s));
          fout << text;
        }
        if (s == 0 || s == 4 || s == 6 || s == 8) fout << "        \\hline\n";
      }
      snprintf(text, 1000, "        $S/\\sqrt{B}$ & %.4f & %.4f & %.4f & %.4f & %.4f & %.4f \\\\\n",
        cutflow.at(6).at(9), cutflow.at(7).at(9), cutflow.at(8).at(9),
        cutflow.at(9).at(9), cutflow.at(10).at(9), cutflow.at(11).at(9));
      fout << text;
      fout << "        \\hline\n";
      fout << "        \\hline\n";
      fout << "        Mass & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$e\\mu$ & SS-$\\mu\\mu$ & SS-$\\mu\\mu$ \\\\\n";
      fout << "        Region & $m(e\\tau_h)<150$GeV & $m(e\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV & $m(\\mu\\tau_h)<150$GeV & $m(\\mu\\tau_h)>150$GeV \\\\\n";
      fout << "        \\hline\n";
      for (unsigned int s = 0; s < TABLE_LATEX.size(); s++) {
        if (s == 5 || s == 6 || s == 8) {
          snprintf(text, 1000, "        " + TABLE_LATEX[s]
            + " & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f"
            + " & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f & %.4f$\\pm$%.4f \\\\\n",
            cutflow.at(12).at(s), cutflowErr.at(12).at(s),
            cutflow.at(13).at(s), cutflowErr.at(13).at(s),
            cutflow.at(14).at(s), cutflowErr.at(14).at(s),
            cutflow.at(15).at(s), cutflowErr.at(15).at(s),
            cutflow.at(16).at(s), cutflowErr.at(16).at(s),
            cutflow.at(17).at(s), cutflowErr.at(17).at(s));
          fout << text;
        }
        else {
          snprintf(text, 1000, "        " + TABLE_LATEX[s]
            + " & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f"
            + " & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f & %.2f$\\pm$%.2f \\\\\n",
            cutflow.at(12).at(s), cutflowErr.at(12).at(s),
            cutflow.at(13).at(s), cutflowErr.at(13).at(s),
            cutflow.at(14).at(s), cutflowErr.at(14).at(s),
            cutflow.at(15).at(s), cutflowErr.at(15).at(s),
            cutflow.at(16).at(s), cutflowErr.at(16).at(s),
            cutflow.at(17).at(s), cutflowErr.at(17).at(s));
          fout << text;
        }
        if (s == 0 || s == 4 || s == 6 || s == 8) fout << "        \\hline\n";
      }
      snprintf(text, 1000, "        $S/\\sqrt{B}$ & %.4f & %.4f & %.4f & %.4f & %.4f & %.4f \\\\\n",
        cutflow.at(12).at(9), cutflow.at(13).at(9), cutflow.at(14).at(9),
        cutflow.at(15).at(9), cutflow.at(16).at(9), cutflow.at(17).at(9));
      fout << text;
      fout << "        \\hline\n";
      fout << "      \\end{tabular}\n";
      fout << "    }\n";
      fout << "  \\end{frame}\n";
      fout << "\n";
    }
  }

  // End LaTeX document
  fout << "\\end{document}\n";
  fout.close();
}

void Fill(TH1F* h, std::vector<std::vector<Double_t>>& cutflow, 
  std::vector<std::vector<Double_t>>& cutflowErr, Int_t idx) {

  for (int b = 0; b < h->GetNbinsX(); b++) {
    cutflow.at(b).at(idx) += h->GetBinContent(b + 1);
    cutflowErr.at(b).at(idx) += h->GetBinError(b + 1);
  }
}
