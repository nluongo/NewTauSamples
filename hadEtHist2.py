import ROOT
from ROOT import TGraph, TCanvas, TFile, TLegend, TH1F, kRed, kBlue, kGreen
from ROOTDefs import prepare_event, set_po_tree_parameters
from ROOTPlotDefs import reco_et_tree_histogram
from ROOTClassDefs import Tree


c1 = TCanvas('c1', 'Graph Draw Options', 200, 10, 600, 400)

new_f = TFile('../dataFiles/back_xAOD_formatted.root')
new_t = Tree(new_f.Get('mytree'))
set_po_tree_parameters(new_t)

new_05_f = TFile('../dataFiles/back_xAOD_formatted_0.5L2.root')
new_05_t = Tree(new_05_f.Get('mytree'))
set_po_tree_parameters(new_05_t)

old_f = TFile('../dataFiles/output_MB80_formatted.root')
old_t = Tree(old_f.Get('mytree'))

sig_f = TFile('../dataFiles/ztt_Output_formatted.root')
sig_t = Tree(sig_f.Get('mytree'))
set_po_tree_parameters(sig_t)

print 'New entries'
print new_t.entries
print 'Old entries'
print old_t.entries

new_had_histo = TH1F('histo', 'New Hadronic Energy', 100, 0, 20)
new_05_had_histo = TH1F('histo', 'New 0.5 GeV Hadronic Energy', 100, 0, 20)
old_had_histo = TH1F('histo', 'Old Hadronic Energy', 100, 0, 20)

zero_new = 0
zero_05_new = 0
zero_old = 0
for i in range(new_t.entries):
  event = prepare_event(new_t, i)
  new_had_histo.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_new += 1

for i in range(new_05_t.entries):
  event = prepare_event(new_05_t, i)
  new_05_had_histo.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_05_new += 1

for i in range(old_t.entries):
  event = prepare_event(old_t, i)
  old_had_histo.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_old += 1

print 'Percentage of new entries with zero hadronic energy'
print float(zero_new) / new_t.entries
print 'Percentage of new 0.5 GeV entries with zero hadronic energy'
print float(zero_05_new) / new_05_t.entries
print 'Percentage of old entries with zero hadronic energy'
print float(zero_old) / old_t.entries

new_hist = reco_et_tree_histogram(new_t, 100, 0, 50)
new_hist.SetTitle('New Background Event Reconstructed Et')
new_05_hist = reco_et_tree_histogram(new_05_t, 100, 0, 50)
new_05_hist.SetTitle('New Background 0.5 GeV Event Reconstructed Et')
old_hist = reco_et_tree_histogram(old_t, 100, 0, 50)
old_hist.SetTitle('Old Background Event Reconstructed Et')
sig_hist = reco_et_tree_histogram(sig_t, 100, 0, 50)
sig_hist.SetTitle('Signal Event Reconstructed Et')

new_had_histo.SetTitle('New Background Hadronic Reconstructed Et')
new_05_had_histo.SetTitle('New Background 0.5 GeV Hadronic Reconstructed Et')
old_had_histo.SetTitle('Old Background Hadronic Reconstructed Et')

plot_name = '../plots/RecoEtHists2.pdf'
'''
new_hist.Draw()
c1.Print(plot_name+'(')
new_05_hist.Draw()
c1.Print(plot_name)
old_hist.Draw()
c1.Print(plot_name)
new_had_histo.Draw()
c1.SetLogy()
c1.Print(plot_name)
new_05_had_histo.Draw()
c1.Print(plot_name)
old_had_histo.Draw()
c1.Print(plot_name)
c1.SetLogy(0)
'''
#new_hist.Draw('hist')
#new_hist.Scale(1/new_hist.GetEntries())
#new_hist.SetTitle('Reconstructed Et')
#new_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
#new_hist.GetYaxis().SetTitle('Entries')
#new_hist.SetStats(0)
#new_hist.SetLineColor(kRed)
sig_hist.Draw('hist')
#sig_hist.Scale(1/sig_hist.GetEntries())
sig_hist.SetLineColor(kBlue)
#old_hist.Draw('hist same')
#old_hist.Scale(1/old_hist.GetEntries())
#old_hist.SetLineColor(kGreen)
#leg1 = TLegend(0.7, 0.8, 0.9, 0.9)
#leg1.AddEntry(sig_hist, 'Signal')
#leg1.AddEntry(new_hist, 'New Background')
#leg1.AddEntry(old_hist, 'Old Background')
#leg1.Draw()

c1.Print(plot_name)


