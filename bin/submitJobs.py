import sys
import os
import subprocess
import time

start = time.time()

jobruntime = 5400 # 1.5 hr

try:
    file = open('TopLFV.txt')
except Exception as e:
    print('TopLFV.txt not found! Please run makeJobs.py first!')

submit = 'universe = vanilla\n' # Writing .sub file
submit += 'executable = TopLFV.sh\n'
submit += 'should_transfer_files = YES\n'
submit += 'when_to_transfer_output = ON_EXIT\n'
submit += 'transfer_input_files = ../data,../include,CMakeLists.txt,Jobs/$(year)/$(proc)/$(file).C,../build/libTopLFV.so\n'
submit += 'transfer_output_files = $(file).root\n'
submit += 'transfer_output_remaps = "$(file).root = ../hists/$(year)/$(file).root"\n'
submit += 'arguments = $(file)\n'
submit += 'output = Jobs/$(year)/$(proc)/$(file).out\n'
submit += 'error = Jobs/$(year)/$(proc)/$(file).err\n'
submit += 'log = Jobs/$(year)/$(proc)/$(file).log\n'
#submit += 'batch_name = $(proc)\n' #looks like can give only one batch name
submit += 'request_cpus = $(nCPUS)\n'
submit += '+MaxRuntime = ' + str(jobruntime) + '\n' 
submit += 'periodic_hold = (JobStatus == 2) && (time() - EnteredCurrentStatus) > ' + str(int(0.8 * jobruntime)) + '\n'
submit += 'periodic_hold_reason = "Job is getting close to be terminated due to run time"\n'
submit += 'on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)\n'
submit += 'periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 120)\n'
submit += 'queue year,proc,file,nCPUs from TopLFV.txt\n'

open('TopLFV.sub', 'wt').write(submit)
subprocess.call("condor_submit TopLFV.sub", shell=True)

end = time.time()
print('Runtime was %.2f seconds.' % (end - start))
