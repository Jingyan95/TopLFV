# ---------------------------------------------------- #
# Everything here should match with src/MyAnalysis.cc  #
# ---------------------------------------------------- #


import argparse
import cmsstyle.src.cmsstyle as CMS
import ROOT


test = False


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018", "All"]
SAMPLES = ["Data", "tt", "DY", "Others", "FakeTau"]
SAMPLES_NAME = ["Data", "t#bar{t}", "DY", "Others", "Fake #tau"]
SAMPLES_NAME_SUMMARY = ["Data", "t#bar{t}+X", "VV(V)", "DY/ZZ", "t#bar{t}/WW",
    "CLFV top production", "CLFV top decay"]
TABLE_LATEX = ["Data", "$t\\bar{t}X$", "VV", "DY",
    "$t\\bar{t}$", "St Scalar U", "Tt Scalar U", "Background", "Signal"]
CHARGES = ["OS", "SS"]
CHANNELS = ["etau", "mutau"]
CHANNELS_NAME = ["e#tau_{h}", "#mu#tau_{h}"]
REGIONS = [
    "ll",
    "llB0", 
    "llOnZMetl100B0",
    "llBgeq1",
    "llJet0",
    "llJet1",
    "llJetgeq2"
]
REGIONS_NAME = [
    ("No cuts", ""),
    ("B0", "(W+jets)"),
    ("OnZ, MET<100, B0", "(Z+jets)"),
    ("Bgeq1", "(t#bar{t})"),
    ("Jet0", "Jet CR"),
    ("Jet1", "Jet CR"),
    ("Jetgeq2", "Jet CR")
]
REGIONS_LATEX = [
    "no cuts",
    "W+jets, B0",
    "Z+jets, On Z, Met < 100, B0",
    "t#{t}, Bgeq1",
    "Jet CR, Jet0",
    "Jet CR, Jet1",
    "Jet CR, Jetgeq2"
]

VARS1D = ["lep1Pt", "tauPt", "TtauPt", "lep1Eta", "tauEta", "TtauEta", "njet", "nbjet", "St", "llM", "llDr", "btagSum", "MET", "tM", "tauJetPt", "tauJetBtag", "tauRT"]
VARS1D_NAME = ["Leading lepton p_{T} [GeV]",
               "tau lepton p_{T} [GeV]", 
               "Tight tau lepton p_{T} [GeV]", 
               "Leading lepton |#eta|", 
               "tau lepton |#eta|",
               "Tight tau lepton |#eta|",
               "njet",
               "nbjet",
               "S_{T} [GeV]",
               "m(ll) [GeV]",
               "#DeltaR(ll)",
               "Sum of btagging scores",
               "MET [GeV]",
               "M_{T} [GeV]",
               "tau mother jet p_{T} [GeV]",
               "tau mother jet b tagging",
               "tau RT"]
               
VARS2D = ["1ProngTauL", "1ProngTauT", "3ProngTauL", "3ProngTauT"]
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

COLORS = [ROOT.kBlack, CMS.p8.kBlue, CMS.p8.kOrange, CMS.p8.kRed, CMS.p8.kPink, CMS.p8.kCyan, CMS.p8.kGray, CMS.p8.kAzure]
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
