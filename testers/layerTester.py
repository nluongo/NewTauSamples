import ROOT
import pandas as pd

#f = uproot.open('back_xAOD_layers.root')
#t = f['mytree']

#frame = t.arrays(['L0Et', 'L1Et', 'L2Et', 'L3Et', 'HadEt'], outputtype=pd.DataFrame)
#print frame

f = ROOT.TFile('~/NewTauSamples/dataFiles/back_layers.root')
t = f.Get('mytree')
t_string = f.Get('Tester')
print t_string

print t.GetEntries()

t.GetEntry(0)

print t.L0Et
print t.L1Et
print t.L2Et
print t.L3Et
print t.HadEt
#print t.TruePt
