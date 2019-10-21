##############
# VERSION: 1 #
##############

import ROOT
import ROOTClassDefs
from ROOT import TFile, TTree, TVector3
from ROOTDefs import resize_root_layer_to_array
import numpy as np
import os
from glob import glob
from helpScripts import createCellLists, po_3x3_cells_to_array, po_12x3_cells_to_array, eventTruthMatchedTOBs, getSeedCell
import sys
import re

# Read in parameter denoting whether to run on signal or background
sigOrBack = int(sys.argv[1])

# Define location of source samples and define output file based on signal or background flag
if sigOrBack == 1:
    f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.ZtautauNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574121.ALLTOB._*.root'
    f_out_name = 'sig_ntuple_turnonrunIII.root'
elif sigOrBack == 0:
    f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.JZ0WNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574138.ALLTOB._*.root' 
    f_out_name = 'back_ntuple_turnonrunIII.root'
else:
    print 'Must provide argument'
    exit()

# Get files and take subset if looking at background  and add them to TChain to be read together
f_list = glob(f_loc)
if sigOrBack == 0:
    f_list = [ f_name for f_name in f_list if re.search("0000[0-1][0-9]",f_name) is not None]

print 'Files included: ',len(f_list)

# Chain all files together in one tree
t = ROOT.TChain("tobTree")
for f_name in f_list:
    t.AddFile(f_name)
entries = t.GetEntries()
print 'Total entries: ',entries

t.seed_region_def = [[4, 7], [1, 1]]
t.adjacent_eta_cells = { 4: -1, 5: 0, 6: 0, 7: 1 }
t.reco_et_def = [[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]]
t.fcore_def = [[3, 2], [12, 3]]
t.reco_et_layer_weights = [1, 1, 1, 1, 1]
#t.reco_et_layer_weights = [1, 1, 1.6, 1.6, 1.4]
t.reco_et_shift = 0

eta_cut = 2.3
seed_et_cut = 1

# Create TFile
f_out = TFile(f_out_name, 'recreate')

# Create description TString and store in TFile
t_string = ROOT.TString("""
                        Production script: {}
                        Production script version: 1
                        Events source: {} 
                        Source production script: https://gitlab.cern.ch/will/L1CaloUpgrade
                        Only files 000001 to 000019 are included
                    
                        Cuts:
                        TOB |Eta| < {}
                        L2 Seed Cell Et > {} GeV

                        Layer Weights:
                        L0+L1: 1
                        L2+L3: 1
                        Had: 1
                        Git commit ID: b5e405823f66e9c1829ddb81bc666d673554354c
                        """.format(sys.argv[0], f_loc, eta_cut, seed_et_cut))
f_out.WriteObject(t_string, 'File Details')

# Create output TTree
t_out = TTree('mytree', 'Full event file')

# Initialize variables to be written to tree
l0_cells = np.array([0]*9, dtype=np.float32)
l1_cells = np.array([0]*36, dtype=np.float32)
l2_cells = np.array([0]*36, dtype=np.float32)
l3_cells = np.array([0]*9, dtype=np.float32)
had_cells = np.array([0]*9, dtype=np.float32)
#tob_eta = np.array([0], dtype=np.float32)
#tob_phi = np.array([0], dtype=np.float32)
run3_et = np.array([0], dtype=np.float32)
#seed_eta = np.array([0], dtype=np.int32)
#seed_phi = np.array([0], dtype=np.int32)

# Connect variables to branches in output tree
#t_out.Branch('L0CellEt', l0_cells, 'L0CellEt[9]/F')
#t_out.Branch('L1CellEt', l1_cells, 'L1CellEt[36]/F')
#t_out.Branch('L2CellEt', l2_cells, 'L2CellEt[36]/F')
#t_out.Branch('L3CellEt', l3_cells, 'L3CellEt[9]/F')
#t_out.Branch('HadCellEt', had_cells, 'HadCellEt[9]/F')
#t_out.Branch('TOBEta', tob_eta, 'TOBEta/F')
#t_out.Branch('TOBPhi', tob_phi, 'TOBPhi/F')
t_out.Branch('Run3Et', run3_et, 'Run3Et/F')
#t_out.Branch('SeedEta', seed_eta, 'SeedEta/I')
#t_out.Branch('SeedPhi', seed_phi, 'SeedPhi/I')

# Define signal-specific variables based on signal/background flag
if sigOrBack == 1:
    true_pt = np.array([0], dtype=np.float32)
    t_out.Branch('TrueTauPt', true_pt, 'TrueTauPt/F')

# Loop over source events and load those that pass cuts into output file
tob_counter = 0
for i, event in enumerate(t):
    if sigOrBack == 1:
        tobList = eventTruthMatchedTOBs(event)
        tobs = [entry[0] for entry in tobList]
        truePts = [entry[1] for entry in tobList]
    else:
        tobs = event.efex_AllTOBs
 
    event_max_et = -float('inf')
    max_et_tob = None
    max_et_tob_num = None
    for tob_num, tob in enumerate(tobs):
        tob_counter += 1

        # Cut on TOB eta
        if abs(tob.eta()) > eta_cut:
            continue

        # Format cells Ets in nTuple-friendly way
        cells = createCellLists(tob)

        po_3x3_cells_to_array(l0_cells, cells[0])
        po_12x3_cells_to_array(l1_cells, cells[1])
        po_12x3_cells_to_array(l2_cells, cells[2])
        po_3x3_cells_to_array(l3_cells, cells[3])
        po_3x3_cells_to_array(had_cells, cells[4])

        l0_array = resize_root_layer_to_array(l0_cells, 3, 3)
        l1_array = resize_root_layer_to_array(l1_cells, 12, 3)
        l2_array = resize_root_layer_to_array(l2_cells, 12, 3)
        l3_array = resize_root_layer_to_array(l3_cells, 3, 3)
        had_array = resize_root_layer_to_array(had_cells, 3, 3)

        l0_layer = ROOTClassDefs.Layer(l0_array, 3, 3, 0)
        l1_layer = ROOTClassDefs.Layer(l1_array, 12, 3, 1)
        l2_layer = ROOTClassDefs.Layer(l2_array, 12, 3, 2)
        l3_layer = ROOTClassDefs.Layer(l3_array, 3, 3, 3)
        had_layer = ROOTClassDefs.Layer(had_array, 3, 3, 4)

        event = ROOTClassDefs.Event(t, l0_layer, l1_layer, l2_layer, l3_layer, had_layer, 0, 1, 0)

        # Find seed cell
        found_seed_eta, found_seed_phi = getSeedCell(event.l2_layer.cell_et)

        # If no seed is found then go to next TOB
        if found_seed_eta is None:
            continue

        # If valid seed found, set it in the Event which recalculate seed_et and reco_et
        event.set_seed_position(found_seed_eta, found_seed_phi)
        
        # Cut on seed Et
        seed_et = event.l2_layer.cell_et[found_seed_eta][found_seed_phi]
        if seed_et < seed_et_cut:
            continue

        if event.reco_et > event_max_et:
            event_max_et = event.reco_et
            max_et_tob = tob
            max_et_tob_num = tob_num

    # Found no valid TOBs, so move to the next event
    if max_et_tob is None:
        continue

    # Found at least one valid TOB, so write it
    run3_et[0] = event_max_et    
    if sigOrBack == 1:
        true_pt[0] = truePts[max_et_tob_num] / 1000.

    t_out.Fill()

    if t_out.GetEntries() % 1000 == 0:
        print 'Entries filled: ',t_out.GetEntries()

print 'TOBs considered: ', tob_counter
print 'TOBs written: ', t_out.GetEntries()

f_out.Write()
f_out.Close()

