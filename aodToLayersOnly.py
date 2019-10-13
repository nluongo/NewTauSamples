##############
# VERSION: 1 #
##############

import ROOT
from ROOT import TTree, AddressOf
from ROOTDefs import prepare_event, set_po_tree_parameters
from ROOTClassDefs import Tree
import numpy as np
import sys

'''
Take formatted PO signal file and ET background file and format such that only the total Et of each layer is stored
Default algorithm for determining layer Et is used
For background (ET)
- layer_dim_keys = {0 : [3, 3], 1 : [13, 3], 2 : [13, 3], 3 : [3, 3], 4 : [3, 3]}
- reco_et_def = [[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]]
- seed_region_def = [[4, 8], [1, 1]]
- adjacent_eta_cells = { 4: -1, 5: 0, 6: 0, 7: 0, 8: 1 }
For signal (PO)
- layer_dim_keys = {0 : [3, 3], 1 : [12, 3], 2 : [12, 3], 3 : [3, 3], 4 : [3, 3]}
- reco_et_def = [[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]]
- seed_region_def = [[4, 7], [1, 1]]
- adjacent_eta_cells = { 4: -1, 5: 0, 6: 0, 7: 0, 8: 1 }
'''
# Get argument specifying signal or background
sigOrBack = int(sys.argv[1])

# Define input file
if sigOrBack == 1:
  file_path = '~/NewTauSamples/dataFiles/sig_ntuple.root'
elif sigOrBack == 0:
  file_path = '~/NewTauSamples/dataFiles/back_ntuple_abr.root'
else:
  print 'Must provide argument'
  exit()

# Get input TFile and Tree
f_in = ROOT.TFile(file_path)
print f_in
t_in = Tree(f_in.Get('mytree'))
print t_in
set_po_tree_parameters(t_in)

# Define ouput file dependent on signal or background
if sigOrBack == 1:
  f_out = ROOT.TFile('sig_layers.root', 'recreate')
  t_out = ROOT.TTree('mytree', 'Layers only xAOD-derived file')
else:
  f_out = ROOT.TFile('back_layers_abr.root', 'recreate')
  t_out = ROOT.TTree('mytree', 'Layers only xAOD-derived file')

t_string = ROOT.TString('Test string info')

# Initialize variables to be written to tree
l0_layer_et = np.array([0], dtype=np.float32)
l1_layer_et = np.array([0], dtype=np.float32)
l2_layer_et = np.array([0], dtype=np.float32)
l3_layer_et = np.array([0], dtype=np.float32)
had_layer_et = np.array([0], dtype=np.float32)

# Connect variables to branches in output tree
t_out.Branch('L0Et', l0_layer_et, 'L0Et/F')
t_out.Branch('L1Et', l1_layer_et, 'L1Et/F')
t_out.Branch('L2Et', l2_layer_et, 'L2Et/F')
t_out.Branch('L3Et', l3_layer_et, 'L3Et/F')
t_out.Branch('HadEt', had_layer_et, 'HadEt/F')

if sigOrBack == 1:
  true_tau_pt = np.array([0], dtype=np.float32)
  t_out.Branch('TruePt', true_tau_pt, 'TruePt/F')

for event in t_in:
  l0_layer_et[0] = event.l0_layer.reco_et
  l1_layer_et[0] = event.l1_layer.reco_et
  l2_layer_et[0] = event.l2_layer.reco_et
  l3_layer_et[0] = event.l3_layer.reco_et
  had_layer_et[0] = event.had_layer.reco_et
  
  if sigOrBack == 1:
    true_tau_pt[0] = event.true_tau_pt

  t_out.Fill()

f_out.Write()
f_out.Close()

