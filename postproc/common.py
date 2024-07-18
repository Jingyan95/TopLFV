# ---------------------------------------------------- #
# Everything here should match with src/MyAnalysis.cc  #
# ---------------------------------------------------- #


import argparse
import cmsstyle.src.cmsstyle as CMS
import ROOT


test = False


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018", "All"]
SAMPLES = ["Data", "TX", "VV", "Others", "FakeL", "FakeLTau", "FakeTau", "LFVStScalarU", "LFVTtScalarU"]
SAMPLES_NAME = ["Data", "t#bar{t}+X", "VV(V)", "Others", "Fake e/#mu", "Fake e/#mu + #tau", "Fake #tau",
    "CLFV top production (#mu_{ll'tu}^{scalar} = 0.5)",
    "CLFV top decay (#mu_{ll'tu}^{scalar} = 20)"]
SAMPLES_NAME_SUMMARY = ["Data", "t#bar{t}+X", "VV(V)", "DY/ZZ", "t#bar{t}/WW",
    "CLFV top production", "CLFV top decay"]
TABLE_LATEX = ["Data", "$t\\bar{t}X$", "VV", "DY",
    "$t\\bar{t}$", "St Scalar U", "Tt Scalar U", "Background", "Signal"]
CHARGES = ["OS", "SS"]
CHANNELS = ["ee", "emu", "mumu"]
CHANNELS_NAME = ["ee#tau_{h}", "e#mu#tau_{h}", "#mu#mu#tau_{h}"]
REGIONS = [
    "ll",
    "llOnZMetg20Jetgeq1",
    "llOffZMetg20B1",
    "llOffZMetg20B2",
    "llStl300",
    "llOnZ",
    "llbtagg1p3",
    "llStg300OffZbtagl1p3"
]
REGIONS_NAME = [
    ("No cuts", ""),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ (Z+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1 (SR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2 (t#bar{t}+jets CR)"),
    ("S_{T}<300GeV", "(CR)"),
    ("OnZ", "(Z+jets CR)"),
    ("btag>1.3", "(t#bar{t}+jets CR)"),
    ("S_{T}>300GeV, OffZ", "btag<1.3 (SR(Alt, Loose))")
]
REGIONS_LATEX = [
    "no cuts",
    "Z+jets CR, On Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$",
    "SR, Off Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$",
    "$t\\bar{t}$ + jets CR, Off Z, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=2$",
    "CR, $S_T<300$ GeV",
    "Z+jets CR, On Z",
    "$t\\bar{t}$ + jets CR, btag $>1.3$",
    "SR(Alt, Loose), btag $<1.3$"
]

VARS1D = ["lep1Pt", "lep2Pt", "tauPt", "lep1Eta", "lep2Eta", "tauEta", "Ht", "njet", "nbjet", "St", "tauRT"]
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
               "tau R_{T}"]
VARS2D = ["0J", "1J", "2J"]
VARS2D_NAME = [
    ("#tau p_{T} [GeV]", "#tau #eta"),
    ("Fake #tau p_{T} [GeV]", "Fake #tau #eta")
]

# For fake factor calculation
VARS1DFF = ["taPtFFBin", "taEtaFFBin"]
VARS1DFF_NAME = ["#tau p_{T} [GeV]", "#tau #eta"]
VARS2DFF = ["taPtVsEta"]
VARS2DFF_NAME = [
    ("#tau p_{T} [GeV]", "#tau #eta")
]
FF_LABELS = ["On Z"]
X_CUTS = [ # Regions
    ("llOnZ", "llOffZ")
]
Y_CUTS = [ # Domains
    ("geqMedLepgeqTightTa", "geqMedLeplTightTa")
]

COLORS = [ROOT.kBlack, CMS.p8.kBlue, CMS.p8.kOrange, CMS.p8.kRed, CMS.p8.kPink, CMS.p8.kGreen, CMS.p8.kCyan, CMS.p8.kGray, CMS.p8.kAzure]
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
        ("OnZ", "(Z+jets CR)"),
        ("OffZ", "(Close to SR CR)")
    ]
    REGIONS_LATEX = [
        "Z+jets CR, On Z",
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
