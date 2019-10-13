##############
# VERSION: 1 #
##############

import ROOT
from ROOT import TTree, AddressOf
from ROOTDefs import prepare_event, set_po_tree_parameters
from ROOTClassDefs import Tree
import numpy as np
import sys

# Get argument specifying signal or background
sigOrBack = int(sys.argv[1])

# Define input and output files based on signal/background flag
if sigOrBack == 1:
  file_path = '~/NewTauSamples/dataFiles/sig_ntuple.root'
  f_out_name = 'sig_layers.root'
elif sigOrBack == 0:
  file_path = '~/NewTauSamples/dataFiles/back_ntuple.root'
  f_out_name = 'back_layers.root'
else:
  print 'Must provide argument'
  exit()

# Get input TFile and Tree
f_in = ROOT.TFile(file_path)
print f_in
t_in = Tree(f_in.Get('mytree'))
print t_in
set_po_tree_parameters(t_in)

# Create TFile
f_out = ROOT.TFile(f_out_name, 'recreate')

# Create description TString and store in TFile
t_string = ROOT.TString("""
                         Production script: {}
                         Production scripts version: 1
                         Events source: {}
                         Source production script: formatFullEvent.py
                         Source production script version: 1
                         
                         Cuts:
                         True Tau Visible Pt > 20 GeV
                         |Eta| < 1.4
                         Seed Cell Et > 1 GeV
                         """.format(sys.argv[0], file_path))
f_out.WriteObject(t_string, 'File Details')

# Create output TTree
t_out = TTree('mytree', 'Layer Et only file')

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

for event in t_in(sigOrBack, 1, 0):
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

