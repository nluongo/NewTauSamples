from __future__ import print_function
import ROOT
from ROOT import TFile, TTree
from ROOTClassDefs import Tree
from ROOTDefs import prepare_event, set_po_tree_parameters, get_formatted_root_tree
import sys

back_t, back_f = get_formatted_root_tree('~/NewTauSamples/dataFiles/back_ntuple_abr.root')
set_po_tree_parameters(back_t)

sig_t, sig_f = get_formatted_root_tree('~/NewTauSamples/dataFiles/sig_ntuple.root')
set_po_tree_parameters(sig_t)

print('Background entries: ',back_t.entries)
print('Signal entries: ',sig_t.entries)

back_ets = set()
for counter, event in enumerate(back_t):
  back_ets.add(event.had_layer.cell_et[1][1])
  #back_ets.add(event.had_layer.cell_et[1][1])

sig_ets = set()
for counter, event in enumerate(sig_t):
  sig_ets.add(event.had_layer.cell_et[1][1])
  #sig_ets.add(event.had_layer.cell_et[1][1])

#print(sig_ets)
#print(back_ets)

#print(list(sig_ets))
#print(list(back_ets))

print('Signal values:')
print(sorted(list(sig_ets))[0:10])
print('Background values:')
print(sorted(list(back_ets))[0:10])
