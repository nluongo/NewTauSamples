##############
# VERSION: 1 #
##############

import ROOT
from ROOT import TFile, TTree, TVector3
from ROOTDefs import resize_root_layer_to_array
import ROOTClassDefs
import numpy as np
import os
from glob import glob
from NewTauDefs import createCellLists, po_3x3_cells_to_array, po_12x3_cells_to_array, eventTruthMatchedTOBs, getSeedCell, event_from_tob, isCentralTowerSeed
import sys
import re
from myHelpers_New import bigCluster

# Read in parameter denoting whether to run on signal or background
sigOrBack = int(sys.argv[1])

# Define location of source samples and define output file based on signal or background flag
if sigOrBack == 1:
    f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.ZtautauNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574121.ALLTOB._*.root'
    f_out_name = 'sig_ntuple_turnonbigcluster.root'
elif sigOrBack == 0:
    f_loc = '/afs/cern.ch/work/b/barak/public/L1CALO/phase1/user.viveiros.JZ0WNtuple.NTUP_r9700_ALLTOB/user.viveiros.15574138.ALLTOB._*.root' 
    f_out_name = 'back_ntuple_turnonbigcluster.root'
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
t.reco_et_shift = 0

my_tree = ROOTClassDefs.Tree(t)

eta_cut = 2.3
train_max = 20
git_commit_id = 'dad39d542e01ec6cc0dd6de0bdb7db8b2684bb9b'

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
                            distanceFromFrontOfTrain < {}

                            Git commit ID: {} 
                            """.format(sys.argv[0], f_loc, eta_cut, train_max, git_commit_id))
elif sigOrBack == 1:
    t_string = ROOT.TString("""
                            Production script: {}
                            Production script version: 1
                            Events source: {} 
                            Source production script: https://gitlab.cern.ch/will/L1CaloUpgrade
    
                            Truth-matching truth -> reco with dR = 0.3 and reco -> TOB with dR = 0.3
                            Truth that do not find a match in reco are filtered out

                            Cuts:
                            Reco Tau |Eta| < {} (applied to recos after matching to truth)
                            distanceFromFrontOfTrain < {}

                            Git commit ID: {} 
                            """.format(sys.argv[0], f_loc, eta_cut, train_max, git_commit_id))

# Create output TTree
t_out = TTree('mytree', 'Full event file')

# Initialize variables to be written to tree
bigcluster_et = np.array([0], dtype=np.float32)

# Connect variables to branches in output tree
t_out.Branch('BigClusterEt', bigcluster_et, 'BigClusterEt/F')

# Define signal-specific variables based on signal/background flag
if sigOrBack == 1:
    true_pt = np.array([0], dtype=np.float32)
    true_eta = np.array([0], dtype=np.float32)
    reco_pt = np.array([0], dtype=np.float32)
    reco_eta = np.array([0], dtype=np.float32)
    
    t_out.Branch('TrueTauPt', true_pt, 'TrueTauPt/F')
    t_out.Branch('TrueTauEta', true_eta, 'TrueTauEta/F')
    t_out.Branch('RecoTauPt', reco_pt, 'RecoTauPt/F')
    t_out.Branch('TrueTauPt', true_pt, 'TrueTauPt/F')

# Loop over source events and load those that pass cuts into output file
tob_counter = 0
for i, event in enumerate(t):
    if event.distanceFromFrontOfTrain < train_max:
        continue

    if sigOrBack == 1:
        tobList = eventTruthMatchedTOBs(event, my_tree)
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

        #For signal, fill all matched taus that survive eta and seed
        if sigOrBack == 1:
            # If truth didn't match to reco then throw it away
            if recoPts[tob_num] == -1:
                continue

            # If we do find one, then apply cut to reco tau eta
            if abs(recoEta[tob_num]) > eta_cut:
                continue

            bigcluster_et[0] = bigCluster(tob)[0] if tob != -1 else -1
            true_pt[0] = truePts[tob_num] / 1000.
            true_eta[0] = trueEta[tob_num]
            reco_pt[0] = recoPts[tob_num] / 1000. if recoPts != -1 else -1
            reco_eta[0] = recoEta[tob_num]

            t_out.Fill()
            continue

        # For background, fill only highest-Et in event
        else:
            tob_event = event_from_tob(my_tree, tob)

            # Cut on TOB eta
            #if abs(tob.eta()) > eta_cut:
            #    continue

            if not isCentralTowerSeed(tob_event):
                continue

            event_et = bigCluster(tob)[0]

            if event_et > event_max_et:
                event_max_et = event_et
                max_et_tob = tob
                max_et_tob_num = tob_num

    # Found no valid TOBs, so move to the next event
    if max_et_tob is None:
        continue

    # Found at least one valid TOB, so write it
    bigcluster_et[0] = event_max_et

    t_out.Fill()

    if t_out.GetEntries() % 1000 == 0:
        print 'Entries filled: ',t_out.GetEntries()

print 'TOBs considered: ', tob_counter
print 'TOBs written: ', t_out.GetEntries()

f_out.Write()
f_out.Close()






