# ---------------------------------------------------- #
# Everything here should match with src/MyAnalysis.cc  #
# ---------------------------------------------------- #


import argparse
import cmsstyle.src.cmsstyle as CMS
import ROOT


test = False


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018", "All"]
SAMPLES = ["Data", "TX", "VV", "Others", "FakeL", "FakeLTau", "DYFakeTau", "ttFakeTau", "ChargeMisId", "LFVStScalarU", "LFVTtScalarU"]
SAMPLES_NAME = ["Data", "t#bar{t}+X", "VV(V)", "Others", "Fake e/#mu", "Fake e/#mu + #tau", "DY + fake #tau", "t#bar{t} + fake #tau",
                "ChargeMisID", "CLFV top production (#mu_{ll'tu}^{scalar} = 0.5)", "CLFV top decay (#mu_{ll'tu}^{scalar} = 20)"]
TABLE_LATEX = ["Data", "$t\\bar{t}$+X", "VV(V)", "Others", "Fake e/$\\mu$", "Fake e/$\\mu$ + $\\tau_h$", "DY + fake $\\tau_h$", "$t\\bar{t}$ + fake $\\tau_h$",
                "ChargeMisID", "St Scalar U", "Tt Scalar U", "Background", "Signal"]
CHARGES = ["OS", "SS"]
CHANNELS = ["ee", "emu", "mumu"]
CHANNELS_NAME = ["ee#tau_{h}", "e#mu#tau_{h}", "#mu#mu#tau_{h}"]
REGIONS = [
    "ll",
    "llOnZB0",
    "llSideBand",
    "llOffZMetg20B1",
    "llOffZMetg20B2",
    "llStl300",
    "llStg300OffZ"
]
REGIONS_NAME = [
    ("No cuts", ""),
    ("OnZ", "DY+jets CR"),
    ("Side Band", "Z Side Band"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1 (SR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2 (t#bar{t}+jets CR)"),
    ("S_{T}<300GeV", "Generic CR"),
    ("S_{T}>300GeV, OffZ", " SR (New)")
]
REGIONS_LATEX = [
    "no cuts",
    "DY+jets CR, On Z",
    "Z Side Band",
    "SR, Off Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$",
    "$t\\bar{t}$ + jets CR, Off Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=2$",
    "Generic CR, $S_T<300$ GeV",
    "SR (New), Off Z, $S_{T}>300$ GeV"
]

VARS1D = ["lep1Pt", "lep2Pt", "tauPt", "lep1Eta", "lep2Eta", "tauEta", "Ht", "njet", "nbjet", "St", "tauRt", "lep1Rt", "lep2Rt", "llM", "llDr", "llPt", "subSR"]
VARS1D_NAME = ["Leading lepton p_{T} [GeV]",
               "Sub-leading lepton p_{T} [GeV]", 
               "tau lepton p_{T} [GeV]", 
               "Leading lepton |#eta|", 
               "Sub-leading lepton |#eta|", 
               "tau lepton |#eta|",
               "H_{T} [GeV]",
               "njet",
               "nbjet",
               "S_{T} [GeV]",
               "tau R_{T}",
               "Leading lepton R_{T}",
               "Sub-leading lepton R_{T}",
               "m(ll) [GeV]",
               "#DeltaR(l,l)",
               "p_{T}(ll)",
               "Bin index"]

# For fake factor calculation
VARS1DFF = ["taPtFFBin", "taEtaFFBin"]
VARS1DFF_NAME = ["#tau p_{T} [GeV]", "#tau #eta"]
FF_LABELS = ["On Z"]
X_CUTS = [ # Regions
    ("llOnZ", "llOffZ")
]
Y_CUTS = [ # Domains
    ("geqMedLepgeqTightTa", "geqMedLeplTightTa")
]

COLORS = [ROOT.kBlack, CMS.p10.kBlue, CMS.p10.kYellow, CMS.p10.kRed, CMS.p10.kGray, CMS.p10.kViolet, CMS.p10.kBrown, CMS.p10.kOrange, CMS.p10.kGreen, CMS.p10.kAsh, CMS.p10.kCyan]
SQUARE = CMS.kSquare
PLOT_LABEL = "Work in Progress"

def getLumi(year):
    if year=="2016APV": return "19.5"
    elif year=="2016": return "16.8"
    elif year=="2017": return "41.5"
    elif year=="2018": return "59.8"
    return "138"


# ----------------------- Test set ----------------------- #
if test:
    YEARS_RUN2 = ["2016APV"]
    CHARGES = ["OS"]
    CHANNELS = ["emu"]
    CHANNELS_NAME = ["ee#tau_{h}"]
    REGIONS = [
        "llOnZ",
        "llOffZ"
    ]
    REGIONS_NAME = [
        ("OnZ", "(DY+jets CR)"),
        ("OffZ", "(Close to SR CR)")
    ]
    REGIONS_LATEX = [
        "DY+jets CR, On Z",
        "Close to SR CR, Off Z"
    ]
    DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa"]
    DOMAINS_NAME = ["#geq Tight Tau", "< Tight Tau"]
    DOMAINS_LATEX = [
        "$\\geq$ Tight $\\tau$",
        "$<$ Tight $\\tau$"
    ]
    VARS1D = ["taPtFFBin", "taEtaFFBin", "subSR"]
    VARS1D_NAME = ["#tau p_{T} [GeV]", "#tau #eta", "SR subdivided"]
