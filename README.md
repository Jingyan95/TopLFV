# Top LFV Analysis
This framework depends on ROOT libraries. The setup has only been texted on lxplus.

## I. Setup
```
. /cvmfs/sft.cern.ch/lcg/views/LCG_104c/x86_64-el9-gcc13-opt/setup.sh
```

## II. To compile & run
```
git clone https://github.com/jingyan95/TopLFV.git
cd TopLFV
make all
./RunAll
```

## III. To write & submit jobs
```
cd bin/
python3 makeJobs.py
python3 submitJobs.py
```

## IV. To merge output ROOT files
```
cd hists/
python3 hadd.py
```
Make sure all the necessary output files are there under TopLFV/hists/\<year\>/. Otherwise, this function might run into problems.

## V. To make plots
```
cd plot/
python3 drawHists.py
```

## VI. To get event yields
```
cd latex/
root -l -b -q 'Cutflow.cc+("<folder where histograms are stored>")'
```
This script will produce tables of event yields in a LaTeX file. The LaTeX file can be compiled and viewed in pdf format with
```
pdflatex Cutflow_Tables.tex
```
*NOTE: for some reason the table of contents only shows up after compiling twice with pdflatex.*

## File descriptions
<table border="0">
  <tr>
    <td>bin/nano_files_2016APV.py</td>
    <td>Python file to store addresses of 2016preVFP samples with trilepton events</td>
  </tr>
  <tr>
    <td>bin/nano_files_2016.py</td>
    <td>Python file to store addresses of 2016postVFP samples with trilepton events</td>
  </tr>
  <tr>
    <td>bin/nano_files_2017.py</td>
    <td>Python file to store addresses of 2017 samples with trilepton events</td>
  </tr>
  <tr>
    <td>bin/nano_files_2018.py</td>
    <td>Python file to store addresses of 2018 samples with trilepton events</td>
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
    <td>latex/</td>
    <td>Directory where latex files live</td>
  </tr>
  <tr>
    <td>latex/Cutflow.cc</td>
    <td>Utility file for creating event yield tables in LaTeX format</td>
  </tr>
  <tr>
    <td>latex/beamerposter.sty</td>
    <td>Beamer style file for compiling LaTeX event yield tables</td>
  </tr>
  <tr>
    <td>plot/</td>
    <td>Directory where plots are saved</td>
  </tr>
  <tr>
    <td>plot/drawHists.py</td>
    <td>Python script for plotting histograms</td>
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
