import ROOT
from ROOT import TGraph, TCanvas, TFile, TLegend, TH1F, kRed, kBlue, kGreen
from ROOTDefs import prepare_event, set_po_tree_parameters, multi_print
from ROOTPlotDefs import reco_et_tree_histogram
from ROOTClassDefs import Tree


c1 = TCanvas('c1', 'Graph Draw Options', 200, 10, 600, 400)

new_sig_f = TFile('../dataFiles/sig_ntuple.root')
new_sig_t = Tree(new_sig_f.Get('mytree'))
set_po_tree_parameters(new_sig_t)

new_back_f = TFile('../dataFiles/back_ntuple_abr.root')
new_back_t = Tree(new_back_f.Get('mytree'))
set_po_tree_parameters(new_back_t)

old_back_f = TFile('../dataFiles/output_MB80_formatted.root')
old_back_t = Tree(old_back_f.Get('mytree'))

old_sig_f = TFile('../dataFiles/ztt_Output_formatted.root')
old_sig_t = Tree(old_sig_f.Get('mytree'))
set_po_tree_parameters(old_sig_t)

print 'New signal entries'
print new_sig_t.entries
print 'Old signal entries'
print old_sig_t.entries
print 'New background entries'
print old_back_t.entries

new_sig_had_hist = TH1F('hist', 'New Signal Hadronic Layer Energy', 100, 0, 20)
old_sig_had_hist = TH1F('hist', 'Old Signal Hadronic Layer Energy', 100, 0, 20)
new_back_had_hist = TH1F('hist', 'New Background Hadronic Layer Energy', 100, 0, 20)
old_back_had_hist = TH1F('hist', 'Old Background Hadronic Layer Energy', 100, 0, 20)

zero_new_sig_had = 0
zero_old_sig_had = 0
zero_new_back_had = 0
zero_old_back_had = 0

# Load Had info for new signal
for event in new_sig_t:
  new_sig_had_hist.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_new_sig_had += 1

# Load Had info for old signal
for event in old_sig_t:
  old_sig_had_hist.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_old_sig_had += 1

# Load Had info for new background
for event in new_back_t:
  new_back_had_hist.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_new_back_had += 1

# Load Had info for old background
for event in old_back_t:
  old_back_had_hist.Fill(event.had_layer.reco_et)
  if event.had_layer.reco_et == 0:
    zero_old_back_had += 1

print 'Percentage of new signal entries with zero hadronic energy'
print float(zero_new_sig_had) / new_sig_t.entries

print 'Percentage of old signal entries with zero hadronic energy'
print float(zero_old_sig_had) / old_sig_t.entries

print 'Percentage of new background entries with zero hadronic energy'
print float(zero_new_back_had) / new_back_t.entries

print 'Percentage of old background entries with zero hadronic energy'
print float(zero_old_back_had) / old_back_t.entries

new_sig_hist = reco_et_tree_histogram(new_sig_t, 100, 0, 50)
new_sig_hist.SetTitle('New Signal Event Reconstructed Et')

old_sig_hist = reco_et_tree_histogram(old_sig_t, 100, 0, 50)
old_sig_hist.SetTitle('Old Signal Event Reconstructed Et')

new_back_hist = reco_et_tree_histogram(new_back_t, 100, 0, 50)
new_back_hist.SetTitle('New Background Event Reconstructed Et')

old_back_hist = reco_et_tree_histogram(old_back_t, 100, 0, 50)
old_back_hist.SetTitle('Old Background Event Reconstructed Et')

afs_name = '../plots/RecoEtHists.pdf'
eos_name = '/eos/user/n/nicholas/SWAN_projects/NewTauSamples/plots/RecoEtHists.pdf'

plot_names = [afs_name, eos_name]

# Total reconstructed Et plots
new_sig_hist.Draw()
multi_print(plot_names, c1, '(')

old_sig_hist.Draw()
multi_print(plot_names, c1)

new_back_hist.Draw()
multi_print(plot_names, c1)

old_back_hist.Draw()
multi_print(plot_names, c1)

# Had reconstructed Et plots
c1.SetLogy()

new_sig_had_hist.Draw()
new_sig_had_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
new_sig_had_hist.GetYaxis().SetTitle('Entries')
multi_print(plot_names, c1)

old_sig_had_hist.Draw()
old_sig_had_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
old_sig_had_hist.GetYaxis().SetTitle('Entries')
multi_print(plot_names, c1)

new_back_had_hist.Draw()
new_back_had_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
new_back_had_hist.GetYaxis().SetTitle('Entries')
multi_print(plot_names, c1)

old_back_had_hist.Draw()
old_back_had_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
old_back_had_hist.GetYaxis().SetTitle('Entries')
multi_print(plot_names, c1)

c1.SetLogy(0)

new_sig_hist.Draw('hist')
new_sig_hist.Scale(1/new_sig_hist.Integral())
new_sig_hist.SetTitle('Signal Reconstructed Et')
new_sig_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
new_sig_hist.GetYaxis().SetTitle('Entries')
new_sig_hist.SetStats(0)
new_sig_hist.SetLineColor(kRed)

old_sig_hist.Draw('hist same')
old_sig_hist.Scale(1/old_sig_hist.Integral())
old_sig_hist.SetLineColor(kBlue)

leg1 = TLegend(0.7, 0.8, 0.9, 0.9)
leg1.AddEntry(new_sig_hist, 'New Sample')
leg1.AddEntry(old_sig_hist, 'Old Sample')
leg1.Draw()

multi_print(plot_names, c1)

new_back_hist.Draw('hist')
new_back_hist.Scale(1/new_back_hist.Integral())
new_back_hist.SetTitle('Background Reconstructed Et')
new_back_hist.GetXaxis().SetTitle('Reconstructed Et (GeV)')
new_back_hist.GetYaxis().SetTitle('Entries')
new_back_hist.SetStats(0)
new_back_hist.SetLineColor(kRed)

old_back_hist.Draw('hist same')
old_back_hist.Scale(1/old_back_hist.Integral())
old_back_hist.SetLineColor(kBlue)

leg2 = TLegend(0.7, 0.8, 0.9, 0.9)
leg2.AddEntry(new_back_hist, 'New Sample')
leg2.AddEntry(old_back_hist, 'Old Sample')
leg2.Draw()

multi_print(plot_names, c1, ')')

new_sig_hist.Scale(1/new_sig_hist.Integral())
