# Top LFV Analysis  

This framework depends on ROOT libraries 

## I. File Lists

<table border="0">
 <tr>
    <td><b style="font-size:30px">Files</b></td>
    <td><b style="font-size:30px">Description</b></td>
 </tr>
  <tr>
    <td>bin/nano_files_2016APV.py</td>
    <td>Python file to store addresses of 2016-preVFP samples</td>
 </tr>
 <tr>
    <td>bin/nano_files_2016.py</td>
    <td>Python file to store addresses of 2016-postVFP samples</td>
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
    <td>Python function for writing condor jobs</td>
 </tr>
 <tr>
    <td>bin/submitJobs.py</td>
    <td>Python function for submitting condor jobs</td>
 </tr>
 <tr>
    <td>bin/Jobs/</td>
    <td>Directory where condor job files live</td>
 </tr>
 <tr>
    <td>helper/</td>
    <td>Directory where utility functions live</td>
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
    <td>input/</td>
    <td>Directory where input files live</td>
 </tr>
 <tr>
    <td>plot/</td>
    <td>Directory where plotting functions live</td>
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
    <td>src/common_details.cc,fastforest_functions,fastforest.cc</td>
    <td>Standalone C++ interface of XGBoost</td>
 </tr>
</table>

## II. To compile & run 

```sh
cmsrel CMSSW_10_6_4
cd CMSSW_10_6_4/src/
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
cmsenv
cd-
git clone https://github.com/jingyan95/TopLFV.git 
cd TopLFV
make all
./RunAll
```

## III. To write & submit jobs 


### makeJobs.py

```sh
cd bin/
python makeJobs.py
```

### submitJobs.py

```sh
python submitJobs.py
```

## IV. To merge files & make plots

```sh
cd ../hists/
python hadd.py
```
Make sure all the necessary output files are there under TopLFV/hists/2016/, otherwise, this function might run into problems. 
We use the function under TopLFV/plot/ to make plots:

```sh
cd ../plot/
python drawHists.py 
```

## IV.a To make cutflow tables

```sh
cd ../helper/
python cutflow.py
```
This script will print out cutflow tables in LaTeX format.
