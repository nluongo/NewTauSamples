import ROOT
from ROOT import TFile, TTree, TVector3
import numpy as np
import os
import sys
from glob import glob
#from helpScripts import createCellLists, eventTruthMatchedTOBs

isSignal = int(sys.argv[1])

print 'Argument: ',sys.argv[1]

if isSignal == 1:
  f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.ZtautauNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574121.ALLTOB._*.root'
else:
  f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.JZ0WNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574138.ALLTOB._*.root'

f_list = glob(f_loc)

t = ROOT.TChain('tobTree')
for f in f_list:
  t.AddFile(f)

events = t.GetEntries()
print 'Total events: ', events

for i, event in enumerate(t):
    for tob in event.efex_AllTOBs:
        print(tob.ppmTauClus())
    exit()
