import ROOT
from ROOTDefs import set_po_tree_parameters, multi_print, prepare_event
from ROOTClassDefs import Tree

c1 = ROOT.TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

file_path = '~/NewTauSamples/dataFiles/sig_ntuple.root'
f = ROOT.TFile(file_path)
t = Tree(f.Get('mytree'))
set_po_tree_parameters(t)

afs_name = '~/NewTauSamples/plots/sanityCheck.pdf'
eos_name = '/eos/user/n/nicholas/NewTauSamples/plots/sanityCheck.pdf'

plot_names = [afs_name, eos_name]

h0 = ROOT.TH1F('hist', 'New Signal True Tau Pt', 100, 0, 100)
h1 = ROOT.TH1F('hist', 'New Signal Seed Et', 100, 0, 20)
h2 = ROOT.TH1F('hist', 'New Signal Eta', 50, -5, 5)

for i in range(t.root_ttree.GetEntries()):
  t.root_ttree.GetEntry(i)
  event = prepare_event(t, i)
  h0.Fill(t.root_ttree.TrueTauPt)
  h1.Fill(event.l2_layer.cell_et[t.root_ttree.SeedEta][t.root_ttree.SeedPhi])
  h2.Fill(t.root_ttree.TOBEta)

h0.Draw('hist')
multi_print(plot_names, c1, '(')

h1.Draw('hist')
multi_print(plot_names, c1)

h2.Draw('hist')
multi_print(plot_names, c1, ')')
