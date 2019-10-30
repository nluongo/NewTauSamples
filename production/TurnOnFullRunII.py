##############
# VERSION: 1 #
##############

import ROOT
from ROOT import TFile, TTree, TVector3
import numpy as np
import os
from glob import glob
from NewTauDefs import createCellLists, po_3x3_cells_to_array, po_12x3_cells_to_array, eventTruthMatchedTOBs, getSeedCell
import sys
import re

# Read in parameter denoting whether to run on signal or background
sigOrBack = int(sys.argv[1])

# Define location of source samples and define output file based on signal or background flag
if sigOrBack == 1:
    f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.ZtautauNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574121.ALLTOB._*.root'
    f_out_name = 'sig_ntuple_turnonrunII.root'
elif sigOrBack == 0:
    f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.JZ0WNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574138.ALLTOB._*.root' 
    f_out_name = 'back_ntuple_turnonrunII.root'
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

eta_cut = 2.3

# Create TFile
f_out = TFile(f_out_name, 'recreate')

# Create description TString and store in TFile
if sigOrBack == 0:
    t_string = ROOT.TString("""
                            Production script: {}
                            Production script version: 1
                            Events source: {} 
                            Source production script: https://gitlab.cern.ch/will/L1CaloUpgrade
                            Only files 000001 to 000019 are included
                            
                            Only the highest Et of each event is filled
                            
                            Cuts:
                            TOB |Eta| < {}
                            ppmIsMaxCore(3.99) = True
    
                            Git commit ID: 119a4a292a48519763b0d594e6df3478768f500d
                            """.format(sys.argv[0], f_loc, eta_cut))
elif sigOrBack == 1:
    t_string = ROOT.TString("""
                            Production script: {}
                            Production script version: 1
                            Events source: {} 
                            Source production script: https://gitlab.cern.ch/will/L1CaloUpgrade
    
                            Truth-matching truth -> reco with dR = 0.3 and reco -> TOB with dR = 0.3

                            Cuts:
                            Reco Tau |Eta| < {}
                            ppmIsMaxCore(3.99) = True
    
                            Git commit ID: 119a4a292a48519763b0d594e6df3478768f500d
                            """.format(sys.argv[0], f_loc, eta_cut))

f_out.WriteObject(t_string, 'File Details')

# Create output TTree
t_out = TTree('mytree', 'Full event file')

# Initialize variables to be written to tree
#l0_cells = np.array([0]*9, dtype=np.float32)
#l1_cells = np.array([0]*36, dtype=np.float32)
#l2_cells = np.array([0]*36, dtype=np.float32)
#l3_cells = np.array([0]*9, dtype=np.float32)
#had_cells = np.array([0]*9, dtype=np.float32)
#tob_eta = np.array([0], dtype=np.float32)
#tob_phi = np.array([0], dtype=np.float32)
run2_et = np.array([0], dtype=np.float32)
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
t_out.Branch('Run2Et', run2_et, 'Run2Et/F')
#t_out.Branch('SeedEta', seed_eta, 'SeedEta/I')
#t_out.Branch('SeedPhi', seed_phi, 'SeedPhi/I')

# Define signal-specific variables based on signal/background flag
if sigOrBack == 1:
    true_pt = np.array([0], dtype=np.float32)
    true_eta = np.array([0], dtype=np.float32)
    reco_pt = np.array([0], dtype=np.float32)
    reco_eta = np.array([0], dtype=np.float32)
    
    t_out.Branch('TrueTauPt', true_pt, 'TrueTauPt/F')
    t_out.Branch('TrueTauEta', true_eta, 'TrueTauEta/F')
    t_out.Branch('RecoTauPt', reco_pt, 'RecoTauPt/F')
    t_out.Branch('RecoTauEta', reco_eta, 'RecoTauEta/F')

# Loop over source events and load those that pass cuts into output file
tob_counter = 0
event_break = 0
for i, event in enumerate(t):
    if event_break == 1:
        break

    if sigOrBack == 1:
        tobList = eventTruthMatchedTOBs(event)
        tobs = [entry[0] for entry in tobList]
        truePts = [entry[1] for entry in tobList]
        trueEta = [entry[2] for entry in tobList]
        recoPts = [entry[3] for entry in tobList]
        recoEta = [entry[4] for entry in tobList]
    else:
        tobs = event.efex_AllTOBs
 
    event_max_et = -float('inf')
    max_et_tob = None
    max_et_tob_num = None
    for tob_num, tob in enumerate(tobs):
        tob_counter += 1
        
        # For signal, fill all matched taus that survive eta and seed
        if sigOrBack == 1:
            # If not truth-matched cut on true tau eta
            if tob == -1 and abs(trueEta[tob_num]) > eta_cut:
                continue
            # If truth-matched cut on reconstructed tau eta
            if tob != -1 and abs(recoEta[tob_num]) > eta_cut:
                continue

            run2_et[0] = tob.ppmTauClus() if tob != -1 else -1
            true_pt[0] = truePts[tob_num] / 1000.
            true_eta[0] = trueEta[tob_num]
            reco_pt[0] = recoPts[tob_num] / 1000. if recoPts != -1 else -1
            reco_eta[0] = recoEta[tob_num]

            t_out.Fill()
            continue

        # For background, fill only highest-Et in event
        else:
            # Cut on TOB eta
            if abs(tob.eta()) > eta_cut:
                continue

            # Only consider those that pass Run2 seed cut
            if not tob.ppmIsMaxCore(3.99):
                continue

            if tob.ppmTauClus() > event_max_et:
                event_max_et = tob.ppmTauClus()
                max_et_tob = tob
                max_et_tob_num = tob_num

    # Found no valid TOBs, so move to the next event
    if max_et_tob is None:
        continue

    # Found at least one valid TOB, so write it
    run2_et[0] = event_max_et
    
    t_out.Fill()

    if t_out.GetEntries() % 1000 == 0:
        print 'Entries filled: ',t_out.GetEntries()

print 'TOBs considered: ', tob_counter
print 'TOBs written: ', t_out.GetEntries()

f_out.Write()
f_out.Close()
