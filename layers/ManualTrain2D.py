#import ROOT
#from ROOT import TCanvas, TH1F, TLegend
#from NNDefs import build_and_train_class_nn
from LayersDefs import get_signal_and_background_frames, calculate_derived_et_columns, roc_cuts, background_eff_at_target_signal_eff
#from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

#random.seed(7)
#np.random.seed(7)

total_steps = 101

ninety_percent_efficiencies = np.ones([total_steps, total_steps])

signal_frame, background_frame = get_signal_and_background_frames()

print(signal_frame, background_frame)

calculate_derived_et_columns(signal_frame, background_frame)

# Don't do this unless actually training a network!
# Sample from background frame so there are the same number of signal and background events

for i in range(total_steps):
    for j in range(total_steps):
        print('i = {0}  j = {1}'.format(i, j))
        l2l3_weight = 0.1 * i
        had_weight = 0.1 * j

        calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1], column_names=['L0Et', 'L1Et'],
                                     output_column_name='L0+L1Et')
        calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1], column_names=['L2Et', 'L3Et'],
                                     output_column_name='L2+L3Et')
        calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, l2l3_weight, had_weight], column_names=['L0+L1Et', 'L2+L3Et', 'HadEt'],
                                     output_column_name='TotalEt')

        end_background_efficiency = background_eff_at_target_signal_eff(signal_frame, background_frame, 'TotalEt')

        ninety_percent_efficiencies[i][j] = end_background_efficiency

print(ninety_percent_efficiencies)

min_eff = float('inf')
min_l2l3_weight = 0
min_had_weight = 0
for i in range(total_steps):
    for j in range(total_steps):
        if ninety_percent_efficiencies[i][j] == 0:
            continue
        if ninety_percent_efficiencies[i][j] < min_eff:
            min_eff = ninety_percent_efficiencies[i][j]
            min_l2l3_weight = 0.1 * i
            min_had_weight = 0.1 * j

print('Min eff:  ',min_eff)
print('Min L2L3 Weight: ', min_l2l3_weight)
print('Min Hadronic Weight: ',min_had_weight)



