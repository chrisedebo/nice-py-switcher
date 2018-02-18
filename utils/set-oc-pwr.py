#!/usr/bin/env python2.7
import sys
import subprocess
import os

power_limit=int(sys.argv[1])
gpu_oc=int(sys.argv[2])
mem_oc=int(sys.argv[3])

gco="GPUGraphicsClockOffset"
mtro="GPUMemoryTransferRateOffset"

def powerlimit(watts,gpu_no):
  nvidiasmi="sudo nvidia-smi -i {} -pl {}"
  if type(watts) is int:
    nvsmi=nvidiasmi.format(gpu_no,watts)
    subprocess.call((nvsmi).split(" "))

def nvclocksettings(oc_mhz,oc_tag,gpu_no):
  os.environ["DISPLAY"]=(":{}").format(gpu_no)
  nvsettings=("nvidia-settings -a [gpu:{}]/{}[{}]={}").format(0,oc_tag,"{}",oc_mhz)
  #print(nvsettings.format("1"))
  subprocess.call((nvsettings.format("2")).split(" "))
  subprocess.call((nvsettings.format("3")).split(" "))

cards=int(subprocess.check_output("nvidia-smi --query-gpu=count --format=csv,noheader,nounits".split(" ")).split("\n")[-2])
for i in range(0, cards):
  #power limit
  powerlimit(power_limit,str(i))

  #gpu clock
  nvclocksettings(gpu_oc,gco,str(i))
  
  #mem clock
  nvclocksettings(mem_oc,mtro,str(i))


print(("settings: gpu offset:{}mhz mem offset:{}mhz power limit:{} Watts").format(gpu_oc,mem_oc,power_limit))
