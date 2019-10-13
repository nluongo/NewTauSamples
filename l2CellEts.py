import ROOT
from ROOT import TFile, TTree, TH1F, TCanvas
from ROOTClassDefs import Tree
from ROOTDefs import prepare_event, set_po_tree_parameters

c1 = TCanvas('c1', 'Graph Draw Options', 200, 10, 600, 400)

f_old = ROOT.TFile('../dataFiles/output_MB80_formatted.root')
t_old = Tree(f_old.Get('mytree'))

f_new = ROOT.TFile('../dataFiles/back_xAOD_formatted_abr.root')
t_new = Tree(f_new.Get('mytree'))
set_po_tree_parameters(t_new)

f_sig = ROOT.TFile('../dataFiles/ztt_Output_formatted.root')
t_sig = Tree(f_sig.Get('mytree'))
set_po_tree_parameters(t_sig)

print 'Old entries: ', t_old.entries
print 'New entries: ', t_new.entries
print 'Sig entries: ', t_sig.entries

bins = 120
min_bin = -1
max_bin = 2

old_seed_histo = TH1F('hist', 'Old Background Seed Supercell Energy', 200, 0, 5)
new_seed_histo = TH1F('hist', 'New Background Seed Supercell Energy', 200, 0, 5)
sig_seed_histo = TH1F('hist', 'Signal Seed Supercell Energy', 200, 0, 5)

old_cell_histo = TH1F('hist', 'Old Background L2 Supercell Energy (Constant eta/phi)', bins, min_bin, max_bin)
new_cell_histo = TH1F('hist', 'New Background L2 Supercell Energy (Constant eta/phi)', bins, min_bin, max_bin)
sig_cell_histo = TH1F('hist', 'Signal L2 Supercell Energy (Constant eta/phi)', bins, min_bin, max_bin)

old_off_histo = TH1F('hist', 'Old Background L2 Supercell Energy (Seed eta - 2)', bins, min_bin, max_bin)
new_off_histo = TH1F('hist', 'New Background L2 Supercell Energy (Seed eta - 2)', bins, min_bin, max_bin)
sig_off_histo = TH1F('hist', 'Signal L2 Supercell Energy (Seed eta - 2)', bins, min_bin, max_bin)

for i in range(t_old.entries):
  event = prepare_event(t_old, i)
  old_seed_histo.Fill(event.seed_et)
  old_cell_histo.Fill(event.l2_layer.cell_et[3][1])
  old_off_histo.Fill(event.l2_layer.cell_et[event.seed_eta - 2][event.seed_phi])

for i in range(t_new.entries):
  event = prepare_event(t_new, i)
  new_seed_histo.Fill(event.seed_et)
  new_cell_histo.Fill(event.l2_layer.cell_et[3][1])
  new_off_histo.Fill(event.l2_layer.cell_et[event.seed_eta - 2][event.seed_phi])

for i in range(t_sig.entries):
  event = prepare_event(t_sig, i)
  sig_seed_histo.Fill(event.seed_et)
  sig_cell_histo.Fill(event.l2_layer.cell_et[3][1])
  sig_off_histo.Fill(event.l2_layer.cell_et[event.seed_eta - 2][event.seed_phi])

out_name = '../plots/l2CellEts.pdf'

old_seed_histo.Draw()
c1.Print(out_name+'(')

new_seed_histo.Draw()
c1.Print(out_name)

sig_seed_histo.Draw()
c1.Print(out_name)

old_cell_histo.Draw()
c1.Print(out_name)

new_cell_histo.Draw()
c1.Print(out_name)

sig_cell_histo.Draw()
c1.Print(out_name)

old_off_histo.Draw()
c1.Print(out_name)

new_off_histo.Draw()
c1.Print(out_name)

sig_off_histo.Draw()
c1.Print(out_name+')')

