import ROOT
from ROOTDefs import apply_tree_cut, set_po_tree_parameters, multi_print
from ROOTClassDefs import Tree
from ROOTPlotDefs import reco_et_tree_histogram
from ROCCurveDefs import et_roc_curve
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, THStack, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange, kTRUE
import numpy as np
import os
import math

ROOT.gROOT.SetBatch(kTRUE)

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

# Load signal and background samples
fsig_path = os.path.join(os.path.expanduser('~'), 'NewTauSamples', 'dataFiles', 'sig_ntuple.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))
set_po_tree_parameters(tsig)

fback_path = os.path.join(os.path.expanduser('~'), 'NewTauSamples', 'dataFiles', 'back_ntuple_abr.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
set_po_tree_parameters(tback)

old_fsig_path = os.path.join(os.path.expanduser('~'), 'NewTauSamples', 'dataFiles', 'ztt_Output_formatted.root')
old_fsig = ROOT.TFile(old_fsig_path)
old_tsig = Tree(old_fsig.Get('mytree'))
set_po_tree_parameters(old_tsig)

old_fback_path = os.path.join(os.path.expanduser('~'), 'NewTauSamples', 'dataFiles', 'output_MB80_formatted.root')
old_fback = ROOT.TFile(old_fback_path)
old_tback = Tree(old_fback.Get('mytree'))

# Set (1x1, 1x1, 1x1, 1x1, 1x1) reconstructed Et algorithm
tsig.set_reco_et_def([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])
tback.set_reco_et_def([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])
old_tsig.set_reco_et_def([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])
old_tback.set_reco_et_def([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])

# Make ROC curves
gr0 = et_roc_curve(tsig, tback, 100, 0, 100)
gr10 = et_roc_curve(old_tsig, old_tback, 100, 0, 100)
#gr4 = et_roc_curve(tsig, old_tback, 100, 0, 100)
#h0_0 = reco_et_tree_histogram(tsig, 100, 0, 100)
#h0_0.Scale(1/h0_0.Integral())
#h0_1 = reco_et_tree_histogram(tback, 100, 0, 100)
#h0_1.Scale(1/h0_1.Integral())
#h0_2 = reco_et_tree_histogram(old_tback, 100, 0, 100)
#h0_2.Scale(1/h0_2.Integral())

# Set (1x2, 3x2, 3x2, 1x2, 1x2) reconstructed Et algorithm
tsig.set_reco_et_def([[1, 2], [3, 2], [3, 2], [1, 2], [1, 2]])
tback.set_reco_et_def([[1, 2], [3, 2], [3, 2], [1, 2], [1, 2]])
old_tsig.set_reco_et_def([[1, 2], [3, 2], [3, 2], [1, 2], [1, 2]])
old_tback.set_reco_et_def([[1, 2], [3, 2], [3, 2], [1, 2], [1, 2]]) 

# Make ROC curves
gr1 = et_roc_curve(tsig, tback, 100, 0, 100)
gr11 = et_roc_curve(old_tsig, old_tback, 100, 0, 100)
#gr5 = et_roc_curve(tsig, old_tback, 100, 0, 100)
#h1_0 = reco_et_tree_histogram(tsig, 100, 0, 100)
#h1_0.Scale(1/h1_0.Integral('width'))
#h1_1 = reco_et_tree_histogram(tback, 100, 0, 100)
#h1_1.Scale(1/h1_1.Integral('width'))
#h1_2 = reco_et_tree_histogram(old_tback, 100, 0, 100)
#h1_2.Scale(1/h1_2.Integral('width'))

# Set (1x2, 5x2, 5x2, 3x2, 3x2) reconstructed Et algorithm
tsig.set_reco_et_def([[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]])
tback.set_reco_et_def([[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]])
old_tsig.set_reco_et_def([[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]])
old_tback.set_reco_et_def([[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]])

# Make ROC curves
gr2 = et_roc_curve(tsig, tback, 100, 0, 100)
gr12 = et_roc_curve(old_tsig, old_tback, 100, 0, 100)
#h2_0 = reco_et_tree_histogram(tsig, 100, 0, 100)
#h2_0.Scale(1/h2_0.Integral('width'))
#h2_1 = reco_et_tree_histogram(tback, 100, 0, 100)
#h2_1.Scale(1/h2_1.Integral('width'))
#h2_2 = reco_et_tree_histogram(old_tback, 100, 0, 100)
#h2_2.Scale(1/h2_2.Integral('width'))

# Set (3x3, 9x3, 9x3, 3x3, 3x3) reconstructed Et algorithm
tsig.set_reco_et_def([[3, 3], [9, 3], [9, 3], [3, 3], [3, 3]])
tback.set_reco_et_def([[3, 3], [9, 3], [9, 3], [3, 3], [3, 3]])
old_tsig.set_reco_et_def([[3, 3], [9, 3], [9, 3], [3, 3], [3, 3]])
old_tback.set_reco_et_def([[3, 3], [9, 3], [9, 3], [3, 3], [3, 3]])

# Make ROC curves
gr3 = et_roc_curve(tsig, tback, 100, 0, 100)
gr13 = et_roc_curve(old_tsig, old_tback, 100, 0, 100)
#gr7 = et_roc_curve(tsig, old_tback, 100, 0, 100)
#h3_0 = reco_et_tree_histogram(tsig, 100, 0, 100)
#h3_0.Scale(1/h3_0.Integral('width'))
#h3_1 = reco_et_tree_histogram(tback, 100, 0, 100)
#h3_1.Scale(1/h3_1.Integral('width'))
#h3_2 = reco_et_tree_histogram(old_tback, 100, 0, 100)
#h3_2.Scale(1/h3_2.Integral('width'))

afs_name = '../plots/AllNewRocCurves.pdf' 
eos_name = '/eos/user/n/nicholas/SWAN_projects/NewTauSamples/plots/AllNewRocCurves.pdf'

plot_names = [afs_name, eos_name]

gr0.Draw()
gr0.SetLineColor(kRed)
gr0.SetTitle('New Samples Reconstructed Et ROC Curves')
gr0.GetXaxis().SetTitle("Background Eff")
gr0.GetYaxis().SetTitle("Signal Eff")
gr1.Draw('same')
gr1.SetLineColor(kBlue)

gr2.Draw('same')
gr2.SetLineColor(kGreen)
gr3.Draw('same')
gr3.SetLineColor(kMagenta)

leg1 = TLegend(0.6, 0.1, 0.9, 0.3)
leg1.AddEntry(gr0, '(1x1, 1x1, 1x1, 1x1, 1x1)', 'l')
leg1.AddEntry(gr1, '(1x2, 3x2, 3x2, 1x2, 1x2)', 'l')
leg1.AddEntry(gr2, '(1x2, 5x2, 5x2, 3x2, 3x2)', 'l')
leg1.AddEntry(gr3, '(3x3, 9x3, 9x3, 3x3, 3x3)', 'l')
leg1.SetHeader('Reconstructed Et Definitions')
leg1.Draw()

multi_print(plot_names, c1, '(')

c1.Clear()

gr10.Draw()
gr10.SetLineColor(kRed)
gr10.SetTitle('Old Samples Reconstructed Et ROC Curves')
gr10.GetXaxis().SetTitle("Background Eff")
gr10.GetYaxis().SetTitle("Signal Eff")
gr11.Draw('same')
gr11.SetLineColor(kBlue)

gr12.Draw('same')
gr12.SetLineColor(kGreen)
gr13.Draw('same')
gr13.SetLineColor(kMagenta)

leg2 = TLegend(0.6, 0.1, 0.9, 0.3)
leg2.AddEntry(gr0, '(1x1, 1x1, 1x1, 1x1, 1x1)', 'l')
leg2.AddEntry(gr1, '(1x2, 3x2, 3x2, 1x2, 1x2)', 'l')
leg2.AddEntry(gr2, '(1x2, 5x2, 5x2, 3x2, 3x2)', 'l')
leg2.AddEntry(gr3, '(3x3, 9x3, 9x3, 3x3, 3x3)', 'l')
leg2.SetHeader('Reconstructed Et Definitions')
leg2.Draw()

multi_print(plot_names, c1, '(')

c1.Clear()
'''
gr4.Draw()
gr4.SetLineColor(kRed)
gr4.SetTitle('Old Background Reco Et ROC Curves (True Tau Pt > 20 GeV)')
gr4.GetXaxis().SetTitle("Background Eff")
gr4.GetYaxis().SetTitle("Signal Eff")
gr5.Draw('same')
gr5.SetLineColor(kBlue)
gr6.Draw('same')
gr6.SetLineColor(kGreen)
gr7.Draw('same')
gr7.SetLineColor(kMagenta)

leg2 = TLegend(0.6, 0.1, 0.9, 0.3)
leg2.AddEntry(gr4, '(1x1, 1x1, 1x1, 1x1, 1x1)', 'l')
leg2.AddEntry(gr5, '(1x2, 3x2, 3x2, 1x2, 1x2)', 'l')
leg2.AddEntry(gr6, '(1x2, 5x2, 5x2, 3x2, 3x2)', 'l')
leg2.AddEntry(gr7, '(3x3, 9x3, 9x3, 3x3, 3x3)', 'l')
leg2.SetHeader('Reconstructed Et Definitions')
leg2.Draw()

multi_print(plot_names, c1, ')')

c1.Clear()
'''
gr2.Draw()

gr2.SetLineColor(kRed)
gr2.SetTitle('Old vs New Reco Et ROC Curves')
gr2.GetXaxis().SetTitle('Background Eff')
gr2.GetYaxis().SetTitle('Signal Eff')
gr12.Draw('same')
gr12.SetLineColor(kBlue)

leg3 = TLegend(0.65, 0.1, 0.9, 0.25)
leg3.AddEntry(gr2, 'New (1x2, 5x2, 5x2, 3x2, 3x2)', 'l')
leg3.AddEntry(gr12, 'Old (1x2, 5x2, 5x2, 3x2, 3x2)', 'l')
leg3.SetHeader('Samples')
leg3.Draw()

multi_print(plot_names, c1, ')')
'''
th0 = THStack('th0', 'Reconstructed Et (1x1, 1x1, 1x1, 1x1, 1x1)')
h0_0.SetLineColor(kRed)
th0.Add(h0_0)
h0_1.SetLineColor(kBlue)
th0.Add(h0_1)
h0_2.SetLineColor(kGreen)
th0.Add(h0_2)
th0.Draw('hist nostack')

leg4 = TLegend(0.65, 0.7, 0.9, 0.9)
leg4.AddEntry(h0_0, 'Signal', 'l')
leg4.AddEntry(h0_1, 'New Background', 'l')
leg4.AddEntry(h0_2, 'Old Background', 'l')
leg4.SetHeader('Background Sample')
leg4.Draw()

multi_print(plot_names, c1)

th1 = THStack('th1', 'Reconstructed Et (1x2, 3x2, 3x2, 1x2, 1x2)')
h1_0.SetLineColor(kRed)
th1.Add(h1_0)
h1_1.SetLineColor(kBlue)
th1.Add(h1_1)
h1_2.SetLineColor(kGreen)
th1.Add(h1_2)
th1.Draw('hist nostack')
leg4.Draw()

multi_print(plot_names, c1)

th2 = THStack('th2', 'Reconstructed Et (1x2, 5x2, 5x2, 3x2, 3x2)')
h2_0.SetLineColor(kRed)
th2.Add(h2_0)
h2_1.SetLineColor(kBlue)
th2.Add(h2_1)
h2_2.SetLineColor(kGreen)
th2.Add(h2_2)
th2.Draw('hist nostack')
leg4.Draw()

multi_print(plot_names, c1)

th3 = THStack('th3', 'Reconstructed Et (3x3, 9x3, 9x3, 3x3, 3x3)')
h3_0.SetLineColor(kRed)
th3.Add(h3_0)
h3_1.SetLineColor(kBlue)
th3.Add(h3_1)
h3_2.SetLineColor(kGreen)
th3.Add(h3_2)
th3.Draw('hist nostack')

leg4.Draw()

multi_print(plot_names, c1, ')')
'''

