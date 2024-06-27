# Top LFV extension analysis
This framework depends on ROOT libraries. The setup has only been texted on lxplus.

## I. Setup
First time:
```
. /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
git clone --recurse-submodules --remote-submodules git@github.com:Jingyan95/TopLFV.git
```
Subsequent setup:
```
source setup.sh
```

## II. To compile & run
```
cd TopLFV/build
cmake ..
make
cd ..
./RunAll
```

## III. To write & submit jobs
```
cd bin/
python makeJobs.py
python submitJobs.py
```

## IV. To merge output ROOT files
```
cd hists/
python hadd.py
```
Make sure all the necessary output files are there under TopLFV/hists/\<year\>/. Otherwise, this function might run into problems.

## V. To make plots
```
cd postproc/
python drawHists.py
```

## VI. To get tables of event yields
```
cd postproc/
python cutFlow.py
```
This script will produce tables of event yields in a LaTeX file. The LaTeX file can be compiled and viewed in pdf format with
```
cd postproc/latex/
pdflatex CutFlowTables.tex
```
To suppress the log output, use
```
pdflatex CutFlowTables.tex > /dev/null
```
The log can still be checked in `CutFlowTables.log`. *The table of contents (TOC) will appear after the second compilation.* LaTeX collects the TOC information in the `.toc` file during the first compilation, and then the TOC is produced during the second compilation.

## To update external git repositories
```
cd TopLFV/
git submodule update --remote
```

## To calculate jet to tau fake factors
```
cd postproc/
python jetToTauFakeFactors.py
```

## File descriptions
<table border="0">
  <tr>
    <td>bin/nano_files_2016APV.py</td>
    <td>Python file to store addresses of 2016preVFP samples</td>
  </tr>
  <tr>
    <td>bin/nano_files_2016.py</td>
    <td>Python file to store addresses of 2016postVFP samples</td>
  </tr>
  <tr>
    <td>bin/nano_files_2017.py</td>
    <td>Python file to store addresses of 2017 samples</td>
  </tr>
  <tr>
    <td>bin/nano_files_2018.py</td>
    <td>Python file to store addresses of 2018 samples</td>
  </tr>
  <tr>
    <td>bin/makeJobs.py</td>
    <td>Python script for writing condor jobs</td>
  </tr>
  <tr>
    <td>bin/submitJobs.py</td>
    <td>Python script for submitting condor jobs</td>
  </tr>
  <tr>
    <td>bin/Jobs/</td>
    <td>Directory where condor job files live</td>
  </tr>
  <tr>
    <td>data/</td>
    <td>Directory where scale factors, efficiencies, and corrections live</td>
  </tr>
  <tr>
    <td>helper/</td>
    <td>Directory where utility scripts live</td>
  </tr>
  <tr>
    <td>helper/Count_Ntotal.py</td>
    <td>Python script for counting the total number of events and number of files</td>
  </tr>
  <tr>
    <td>helper/gen_files_2016.py</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>helper/getSumOfGenWeights.py</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>hists/</td>
    <td>Directory where histograms are saved</td>
  </tr>
  <tr>
    <td>hists/hadd.py</td>
    <td>Utility function for merging root files</td>
  </tr>
  <tr>
    <td>include/</td>
    <td>Directory where header files live</td>
  </tr>
  <tr>
    <td>postproc/</td>
    <td>Directory where post-processing scripts live</td>
  </tr>
  <tr>
    <td>postproc/common.py</td>
    <td>Python script where common variables live</td>
  </tr>
  <tr>
    <td>postproc/plotFunctions.py</td>
    <td>Python script where plotting functions live</td>
  </tr>
  <tr>
    <td>postproc/drawHists.py</td>
    <td>Python script for plotting histograms</td>
  </tr>
  <tr>
    <td>postproc/cutFlow.py</td>
    <td>Python script for creating event yield tables in LaTeX format</td>
  </tr>
  <tr>
    <td>postproc/jetToTauFakeFactors.py</td>
    <td>Python script for calculating jet to tau fake factors</td>
  </tr>
  <tr>
    <td>postproc/cmsstyle/</td>
    <td>External git repository with CMS style files</td>
  </tr>
  <tr>
    <td>postproc/latex/</td>
    <td>Directory where latex files live</td>
  </tr>
  <tr>
    <td>postproc/latex-beamerposter/</td>
    <td>External git repository with beamer style files</td>
  </tr>
  <tr>
    <td>src</td>
    <td>Directory where source files live</td>
  </tr>
  <tr>
    <td>src/MyAnalysis.cc</td>
    <td>Main analysis file</td>
  </tr>
  <tr>
    <td>src/event_candidate.cc</td>
    <td>Object class for events</td>
  </tr>
  <tr>
    <td>src/jet_candidate.cc</td>
    <td>Object class for jets</td>
  </tr>
  <tr>
    <td>src/lepton_candidate.cc</td>
    <td>Object class for leptons</td>
  </tr>
  <tr>
    <td>src/trigger.cc</td>
    <td>HLT trigger logic</td>
  </tr>
  <tr>
    <td>src/main.cc</td>
    <td>Testing file</td>
  </tr>
  <tr>
    <td>src/PU_reWeighting.cc</td>
    <td>Reweight MC pile up distribution</td>
  </tr>
  <tr>
    <td>src/common_details.cc, src/fastforest_functions.cc, src/fastforest.cc</td>
    <td>Standalone C++ interface of XGBoost</td>
  </tr>
</table>

## CMSSW warning
This warning will appear when running `RunAll` if `cmsenv` is not set. So far it can be ignored.
```
TClass::Init:0: RuntimeWarning: no dictionary for class edm::Hash<1> is available
TClass::Init:0: RuntimeWarning: no dictionary for class edm::ProcessHistory is available
TClass::Init:0: RuntimeWarning: no dictionary for class edm::ProcessConfiguration is available
TClass::Init:0: RuntimeWarning: no dictionary for class edm::ParameterSetBlob is available
TClass::Init:0: RuntimeWarning: no dictionary for class pair<edm::Hash<1>,edm::ParameterSetBlob> is available
```
