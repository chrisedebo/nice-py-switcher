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
  print(("settings: Power Limit {} watts").format(watts))
  nvidiasmi="sudo nvidia-smi -i {} -pl {}"
  if type(watts) is int:
    nvsmi=nvidiasmi.format(gpu_no,watts)
    subprocess.call((nvsmi).split(" "))

def nvclocksettings(oc_mhz,oc_tag,gpu_no):
  os.environ["DISPLAY"]=":0"
  print(("settings: {} {}mhz").format(oc_tag,oc_mhz))
  nvsettings=("nvidia-settings -a [gpu:{}]/{}[{}]={}").format(gpu_no,oc_tag,"{}",oc_mhz)
  print(nvsettings.format("1"))
  subprocess.call((nvsettings.format("2")).split(" "))
  subprocess.call((nvsettings.format("3")).split(" "))

cards=int(subprocess.check_output("nvidia-smi --query-gpu=count --format=csv,noheader,nounits".split(" ")).split("\n")[-2])
for i in range(0, cards):
  print(i)   
  #power limit
  powerlimit(power_limit,str(i))

  #gpu clock
  nvclocksettings(gpu_oc,gco,str(i))
  
  #mem clock
  nvclocksettings(mem_oc,mtro,str(i))


subprocess.call(("nvidia-settings --assign GPULogoBrightness=0").split(" "))

