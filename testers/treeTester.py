from __future__ import print_function
import ROOT
from ROOT import TFile, TTree
from ROOTClassDefs import Tree
from ROOTDefs import prepare_event, set_po_tree_parameters, get_formatted_root_tree
import sys

#back_t, back_f = get_formatted_root_tree('~/NewTauSamples/scripts/production/back_ntuple.root')
#set_po_tree_parameters(back_t)

#sig_t, sig_f = get_formatted_root_tree('~/NewTauSamples/dataFiles/ztt_Output_formatted.root')
sig_t, sig_f = get_formatted_root_tree('/eos/user/n/nicholas/SWAN_projects/NewTauSamples/dataFiles/ztt_Output_formatted.root')
#set_po_tree_parameters(sig_t)

#t_string = back_f.Get('File Details')
#print(t_string)

print(sig_t.entries)

counter = 0
for event in sig_t(1, 1, 0):
  if event.reco_et < 1:
    #print(event.reco_et)
    counter += 1

print(counter)
