# ----------------------------------------------------------- #
# Everything here should be some subset of src/MyAnalysis.cc  #
# ----------------------------------------------------------- #


import argparse
import cmsstyle.src.cmsstyle as CMS
import ROOT


test = False
draw = False
fake = True


YEARS_RUN2 = ["2016APV", "2016", "2017", "2018", "All"]
SAMPLES = ["Data", "TX", "VV", "DY", "TT", "LFVStScalarU", "LFVTtScalarU"]
SAMPLES_NAME = ["Data", "t#bar{t}+X", "VV(V)", "DY/ZZ", "t#bar{t}/WW",
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
    # "Generic" regions
    "ll",
    "llMetg20Jetgeq1OffZB1", # SR
    "llMetg20Jetgeq1OnZ", # Z+jets CR
    "llMetg20Jetgeq1OffZB2", # ttbar+jets CR
    # St(l/g)300 regions
    "llStg300",
    "llStl300", # fake
    "llMetg20Jetgeq1Stg300",
    "llMetg20Jetgeq1Stl300", # fake
    "llMetg20Jetgeq1OffZB1Stg300",
    "llMetg20Jetgeq1OffZB1Stl300", # fake
    # DY (Z) regions
    "llMetg20Jetgeq1OffZBneq1", # validation
    "llMetg20Jetgeq1OnZBneq1", # validation, fake
    "llMetg20Jetgeq1OffZ", # signal
    "llMetg20Jetgeq1OnZ", # signal, fake (see above!!)
    # ttbar regions
    "llMetg20Jetgeq1B1Stl300", # validation
    "llMetg20Jetgeq1B2Stl300", # validation, fake
    "llMetg20Jetgeq1B1", # signal
    "llMetg20Jetgeq1B2" # signal, fake
]
REGIONS_NAME = [
    ("No cuts", ""),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1 (SR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ (Z+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2 (t#bar{t}+jets CR)"),
    ("S_{T}>300GeV", "(Loose Alt. SR)"),
    ("S_{T}<300GeV", "(CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "S_{T}>300GeV (Medium Alt. SR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "S_{T}<300GeV (CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1, OffZ", "nbjet=1, S_{T}>300GeV (Tight Alt. SR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1, OffZ", "nbjet=1, S_{T}<300GeV (CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet#neq1 (Z+jets VR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ, nbjet#neq1 (Z+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ (Z+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ (Z+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "nbjet=1, S_{T}<300GeV (t#bar{t}+jets VR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "nbjet=2, S_{T}<300GeV (t#bar{t}+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "nbjet=1 (t#bar{t}+jets CR)"),
    ("p_{T}^{miss}>20GeV, njet#geq1", "nbjet=2 (t#bar{t}+jets CR)")
]
REGIONS_LATEX = [
    "No cuts",
    "SR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=1$",
    "Z+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, On Z",
    "$t\\bar{t}$+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=2$",
    "Loose Alt. SR: $S_T>300$",
    "CR: $S_T<300$",
    "Medium Alt. SR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, $S_T>300$",
    "CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, $S_T<300$",
    "Tight Alt. SR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=1$, $S_T>300$",
    "CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=1$, $S_T<300$",
    "Z+jets VR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $\\neq 1",
    "Z+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, On Z, nbjet $\\neq 1",
    "Z+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z",
    "Z+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, On Z",
    "$t\\bar{t}$+jets VR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$, $S_T<300$",
    "$t\\bar{t}$+jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=2, $S_T<300$",
    "$t\\bar{t}$+jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$",
    "$t\\bar{t}$+jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=2"
]
DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa"]
DOMAINS_NAME = ["#geq Tight Tau", "< Tight Tau"]
# DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa", "geqMedLepgeqTightTaJetTaFF"]
# DOMAINS_NAME = ["#geq Tight Tau", "< Tight Tau", "#geq Tight Tau"]
DOMAINS_LATEX = [
    "$\\geq$ Tight $\\tau$",
    "$<$ Tight $\\tau$",
    # "$\\geq$ Tight $\\tau$, jet$\\rightarrow\\tau$ FF"
]
VARS1D = [
    "llM", "llDr", "lep1Pt", "lep2Pt", "elLeptonMVAv1", "elLeptonMVAv2", "muLeptonMVAv1", "muLeptonMVAv2",
    "taPt", "taPtFFBin", "taPtFFBinFake", "taEta", "taEtaFFBin", "taEtaFFBinFake", "taVsJetWP", "taVsJetMVA",
    "taVsElMVA", "taVsMuMVA", "taDxy", "taDz", "taDecayMode", "jet1Pt", "jetbtagDeepFlavB", "njet",
    "nbjet", "MET", "subSR", "LFVemuM", "LFVetaM", "LFVmutaM", "LFVemuDr", "LFVetaDr", "LFVmutaDr",
    "LFVePt", "LFVmuPt", "LFVtaPt", "balepPt", "topmass", "Ht", "St", "btagSum"]
VARS1D_NAME = [
    "m(l#bar{l}) [GeV]", "#DeltaR(l#bar{l})", "Leading lepton p_{T} [GeV]", "Sub-leading lepton p_{T} [GeV]",
    "Electron Top Lepton MVA (v1)", "Electron Top Lepton MVA (v2)", "Muon Top Lepton MVA (v1)",
    "Muon Top Lepton MVA (v2)", "#tau p_{T} [GeV]", "#tau p_{T} [GeV]", "Fake #tau p_{T} [GeV]", "#tau #eta",
    "#tau #eta", "Fake #tau #eta", "#tau vs Jet WP", "#tau vs Jet MVA", "#tau vs Electron MVA",
    "#tau vs Muon MVA", "#tau d_{xy} [cm]", "#tau d_{z} [cm]", "#tau Decay Mode", "Leading jet p_{T} [GeV]",
    "btag", "njet", "nbjet (Loose WP)", "MET [GeV]", "SR subdivided", "m(e#bar{#mu}) [GeV]",
    "m(e#bar{#tau}) [GeV]", "m(#mu#bar{#tau}) [GeV]", "#DeltaR(e,#bar{#mu}) [GeV]", "#DeltaR(e,#bar{#tau}) [GeV]",
    "#DeltaR(#mu,#bar{#tau}) [GeV]", "LFV electron p_{T} [GeV]", "LFV muon p_{T} [GeV]", "LFV tau p_{T} [GeV]",
    "Bachelor lepton p_{T} [GeV]", "m(top) [GeV]", "H_{T} [GeV]", "S_{T} [GeV]", "Sum of btagging scores"]
VARS2D = ["taPtVsEta", "taPtVsEtaFake"]
VARS2D_NAME = [
    ("#tau p_{T} [GeV]", "#tau #eta"),
    ("Fake #tau p_{T} [GeV]", "Fake #tau #eta")
]

# For fake factor calculation
# VARS1DFF = ["taPtFFBin", "taEtaFFBin"]
VARS1DFF = ["taPtFFBin", "taPtFFBinFake", "taEtaFFBin", "taEtaFFBinFake"]
# VARS1DFF_NAME = ["#tau p_{T} [GeV]", "#tau #eta"]
VARS1DFF_NAME = ["Tau p_{T} [GeV]", "Fake tau p_{T} [GeV]", "Tau #eta", "Fake tau #eta"]
VARS2DFF = ["taPtVsEta", "taPtVsEtaFake"]
VARS2DFF_NAME = [
    ("#tau p_{T} [GeV]", "#tau #eta"),
    ("Fake #tau p_{T} [GeV]", "Fake #tau #eta")
]
X_CUTS = [ # Regions
    ("llMetg20Jetgeq1OffZB1Stl300", "llMetg20Jetgeq1OffZB1Stg300"),
    ("llMetg20Jetgeq1OnZBneq1", "llMetg20Jetgeq1OffZBneq1"),
    ("llMetg20Jetgeq1B2Stl300", "llMetg20Jetgeq1B1Stl300")
]
Y_CUTS = [ # Domains
    ("geqMedLepgeqTightTa", "geqMedLeplTightTa"),
    ("geqMedLepgeqTightTa", "geqMedLeplTightTa"),
    ("geqMedLepgeqTightTa", "geqMedLeplTightTa")
]
X_CUT_LABELS = [
    ("S_{T}<300GeV", "S_{T}>300GeV"),
    ("On Z", "Off Z"),
    ("nbjet=2", "nbjet=1")
]
Y_CUT_LABELS = [
    ("#geq Tight Tau", "< Tight Tau"),
    ("#geq Tight Tau", "< Tight Tau"),
    ("#geq Tight Tau", "< Tight Tau")
]

COLORS = [ROOT.kBlack, CMS.p6.kBlue, CMS.p6.kYellow, CMS.p6.kRed, CMS.p6.kGrape, CMS.p6.kGray, CMS.p6.kViolet]
SQUARE = CMS.kSquare
PLOT_LABEL = "Work in Progress"

def getLumi(year):
    if year=="2016APV": return "19.5"
    elif year=="2016": return "16.8"
    elif year=="2017": return "41.5"
    elif year=="2018": return "59.8"
    return "138"


# ----------------------- Small sets ----------------------- #
if draw:
    # YEARS_RUN2 = ["2016APV"]
    # CHARGES = ["OS"]
    # CHANNELS = ["emu"]
    # CHANNELS_NAME = ["ee#tau_{h}"]
    REGIONS = [
        "ll",
        "llMetg20Jetgeq1OffZB1", # SR
        "llMetg20Jetgeq1OnZ", # Z+jets CR
        "llMetg20Jetgeq1OffZB2" # ttbar+jets CR
    ]
    REGIONS_NAME = [
        ("No cuts", ""),
        ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=1 (SR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ (Z+jets CR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet=2 (t#bar{t}+jets CR)")
    ]
    REGIONS_LATEX = [
        "No cuts",
        "SR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=1$",
        "Z+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, On Z",
        "$t\\bar{t}$+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=2$"
    ]
    # DOMAINS = ["geqMedLepgeqTightTa", "geqMedLeplTightTa"]
    # DOMAINS_NAME = ["#geq Tight Tau", "< Tight Tau"]
    # DOMAINS_LATEX = [
    #     "$\\geq$ Tight $\\tau$",
    #     "$<$ Tight $\\tau$"
    # ]
    # VARS1D = ["taPtFFBin", "taEtaFFBin", "subSR"]
    # VARS1D_NAME = ["#tau p_{T} [GeV]", "#tau #eta", "SR subdivided"]

if fake:
    REGIONS = [
        # St(l/g)300 regions
        "llMetg20Jetgeq1OffZB1Stg300",
        "llMetg20Jetgeq1OffZB1Stl300", # fake
        # DY (Z) regions
        "llMetg20Jetgeq1OffZBneq1", # validation
        "llMetg20Jetgeq1OnZBneq1", # validation, fake
        # ttbar regions
        "llMetg20Jetgeq1B1Stl300", # validation
        "llMetg20Jetgeq1B2Stl300" # validation, fake
    ]
    REGIONS_NAME = [
        ("p_{T}^{miss}>20GeV, njet#geq1, OffZ", "nbjet=1, S_{T}>300GeV (Tight Alt. SR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1, OffZ", "nbjet=1, S_{T}<300GeV (CR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1", "OffZ, nbjet#neq1 (Z+jets VR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1", "OnZ, nbjet#neq1 (Z+jets CR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1", "nbjet=1, S_{T}<300GeV (t#bar{t}+jets VR)"),
        ("p_{T}^{miss}>20GeV, njet#geq1", "nbjet=2, S_{T}<300GeV (t#bar{t}+jets CR)")
    ]
    REGIONS_LATEX = [
        "Tight Alt. SR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=1$, $S_T>300$",
        "CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $=1$, $S_T<300$",
        "Z+jets VR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, Off Z, nbjet $\\neq 1",
        "Z+jets CR: $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, On Z, nbjet $\\neq 1",
        "$t\\bar{t}$+jets VR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=1$, $S_T<300$",
        "$t\\bar{t}$+jets CR, $p_T^\\text{miss}>20$ GeV, njet $\\geq 1$, nbjet $=2, $S_T<300$"
    ]
