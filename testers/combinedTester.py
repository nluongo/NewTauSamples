from __future__ import print_function
import ROOT
from ROOTClassDefs import Tree
from ROOTDefs import get_formatted_root_tree, set_po_tree_parameters

event_t, event_f = get_formatted_root_tree('~/NewTauSamples/dataFiles/sig_ntuple.root')
set_po_tree_parameters(event_t)

layer_f = ROOT.TFile('~/NewTauSamples/scripts/sig_layers.root')
layer_t = layer_f.Get('mytree')

for event in event_t:
  print(event.had_layer.cell_et)
  print(event.seed_eta)
  break

layer_t.GetEntry(0)
print(layer_t.HadEt)

