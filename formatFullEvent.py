##############
# VERSION: 1 #
##############

import ROOT
from ROOT import TFile, TTree, TVector3
import numpy as np
import os
from glob import glob
from helpScripts import createCellLists, po_3x3_cells_to_array, po_12x3_cells_to_array, eventTruthMatchedTOBs, getSeedCell
import sys

# Read in parameter denoting whether to run on signal or background
sigOrBack = int(sys.argv[1])

# Define location of source samples and define output file based on signal or background flag
if sigOrBack == 1:
  f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.ZtautauNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574121.ALLTOB._*.root'
  f_out_name = 'sig_ntuple.root'
elif sigOrBack == 0:
  f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.JZ0WNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574138.ALLTOB._*.root'
  f_out_name = 'back_ntuple_abr.root'
else:
  print 'Must provide argument'
  exit()

# Get all valid files and add them to TChain to be read together
f_list = glob(f_loc)
print 'Files found: ',len(f_list)
t = ROOT.TChain("tobTree")
for f_name in f_list:
  t.AddFile(f_name)
entries = t.GetEntries()
print 'Total entries: ',entries

# Create TFile
f_out = TFile(f_out_name, 'recreate')

# Create description TString and store in TFile
t_string = ROOT.TString("""
                        Production script: {}
                        Production script version: 1
                        Events source: {} 
                        Source production script: https://gitlab.cern.ch/will/L1CaloUpgrade
                        """.format(sys.argv[0], f_loc))
f_out.WriteObject(t_string, 'File Details')

# Create output TTree
t_out = TTree('mytree', 'Full event file')

# Initialize variables to be written to tree
l0_cells = np.array([0]*9, dtype=np.float32)
l1_cells = np.array([0]*36, dtype=np.float32)
l2_cells = np.array([0]*36, dtype=np.float32)
l3_cells = np.array([0]*9, dtype=np.float32)
had_cells = np.array([0]*9, dtype=np.float32)
tob_eta = np.array([0], dtype=np.float32)
tob_phi = np.array([0], dtype=np.float32)
seed_eta = np.array([0], dtype=np.int32)
seed_phi = np.array([0], dtype=np.int32)

# Connect variables to branches in output tree
t_out.Branch('L0CellEt', l0_cells, 'L0CellEt[9]/F')
t_out.Branch('L1CellEt', l1_cells, 'L1CellEt[36]/F')
t_out.Branch('L2CellEt', l2_cells, 'L2CellEt[36]/F')
t_out.Branch('L3CellEt', l3_cells, 'L3CellEt[9]/F')
t_out.Branch('HadCellEt', had_cells, 'HadCellEt[9]/F')
t_out.Branch('TOBEta', tob_eta, 'TOBEta/F')
t_out.Branch('TOBPhi', tob_phi, 'TOBPhi/F')
t_out.Branch('SeedEta', seed_eta, 'SeedEta/I')
t_out.Branch('SeedPhi', seed_phi, 'SeedPhi/I')

# Define signal-specific variables based on signal/background flag
if sigOrBack == 1:
  true_pt = np.array([0], dtype=np.float32)
  t_out.Branch('TrueTauPt', true_pt, 'TrueTauPt/F')

# Loop over source events and load those that pass cuts into output file
tob_counter = 0
event_break = 0
for counter, event in enumerate(t):
  if event_break == 1:
    break

  if sigOrBack == 1:
    tobList = eventTruthMatchedTOBs(event)
    tobs = [entry[0] for entry in tobList]
    truePts = [entry[1] for entry in tobList]
  else:
    tobs = event.efex_AllTOBs
  
  for tob_num, tob in enumerate(tobs):
    tob_counter += 1
    
    # If signal, cut on true Pt and if surviving convert to GeV
    if sigOrBack == 1:
      if truePts[tob_num] < 20000.:
        continue
      true_pt[0] = truePts[tob_num] / 1000.
    
    # Cut on TOB eta
    if abs(tob.eta()) > 1.4:
      continue
    
    # Format cells Ets in nTuple-friendly way
    cells = createCellLists(tob)

    po_3x3_cells_to_array(l0_cells, cells[0])
    po_12x3_cells_to_array(l1_cells, cells[1])
    po_12x3_cells_to_array(l2_cells, cells[2])
    po_3x3_cells_to_array(l3_cells, cells[3])
    po_3x3_cells_to_array(had_cells, cells[4])
    
    tob_eta[0] = tob.eta()
    tob_phi[0] = tob.phi()

    # Get layer 2 cells in format getSeedCell understands
    formatted_l2_cells = np.asarray(list(l2_cells))
    formatted_l2_cells = np.resize(formatted_l2_cells, (12, 3))

    # Find seed cell
    found_seed_eta, found_seed_phi = getSeedCell(formatted_l2_cells)
    
    # If no seed is found then go to next TOB
    if found_seed_eta is None:
      continue
    
    # Cut on seed Et
    if formatted_l2_cells[found_seed_eta][found_seed_phi] < 1:
      continue

    seed_eta[0] = found_seed_eta
    seed_phi[0] = found_seed_phi

    t_out.Fill()

    if t_out.GetEntries() % 1000 == 0:
      print 'Entries filled: ',t_out.GetEntries()

    if t_out.GetEntries() == 100000:
      event_break = 1
      break

print 'TOBs considered: ', tob_counter
print 'TOBs written: ', t_out.GetEntries()

f_out.Write()
f_out.Close()






