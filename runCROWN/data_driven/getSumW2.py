import ROOT
import os
import sys
import math
import numpy as np

# Define the file names and pre-selection criteria
file_names = sys.argv[1:]
apply_wz_scale = True
scale_dict = {
    "2022m2m": 1.0791680279940155,
    "2022e2m": 1.060103425086457,
    "2023m2m": 1.1323487753530297,
    "2023e2m": 1.043860425226919,
}

pre_selection = "( (dimuonCR_mass>=85 && dimuonCR_mass<=95) && trg_single_mu24==1&&mt_W<60)*(2*is_data - 1)*(1-is_dyjets)"

weight_calc_sel = "Train_weight*puweight*" + "(" + pre_selection + ")"
print(weight_calc_sel)

print("Pre_selection: {}".format(pre_selection))
print("******************************************")
if "2022" in file_names[0] and "e2m" in file_names[0]:
    print("2022 e2m")
elif "2022" in file_names[0] and "m2m" in file_names[0]:
    print("2022 m2m")
elif "2023" in file_names[0] and "e2m" in file_names[0]:
    print("2023 e2m")
elif "2023" in file_names[0] and "m2m" in file_names[0]:
    print("2023 m2m")

# print(file_names[0])
# exit(0)
toterr1 = 0
toterr2 = 0
toterr3 = 0
toterr4 = 0
toterr5 = 0
toterr6 = 0
toterr7 = 0
toterr8 = 0
tot1 = 0
tot2 = 0
tot3 = 0
tot4 = 0
tot5 = 0
tot6 = 0
tot7 = 0
tot8 = 0
Integral = 0
tot_sum_a_err = 0
sumw2byhand = 0
data_yield = 0
data_err = 0

for file_name in file_names:
    file = ROOT.TFile.Open(file_name)
    tree = file.Get("ntuple")
    # Apply the pre-selection and get the number of entries
    try:
        tree.SetEstimate(tree.GetEntries())
        n_entries = tree.Draw(">>entry_list", pre_selection, "entrylist")
        entry_list = ROOT.gDirectory.Get("entry_list")
    except:
        print("Failed to apply pre-selection or get number of entries from file {}".format(file_name))
        continue

    # deal with the sfs
    if "m2m" in file_name and "Muon" not in file_name:
        weight_calc_sel = "Train_weight*puweight*" +\
                          "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                          "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                          "id_wgt_mu_3*iso_wgt_mu_3*id_wgt_mu_3_below15*iso_wgt_mu_3_below15*" +\
                          "(" + pre_selection + ")"
    elif "e2m" in file_name and "Muon" not in file_name:
        weight_calc_sel = "Train_weight*puweight*" +\
                          "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                          "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                          "id_wgt_ele_loose_1*id_wgt_ele_wp90Iso_1*" +\
                          "(" + pre_selection + ")"
    else:
        weight_calc_sel = "Train_weight*puweight*" + "(" + pre_selection + ")"

    
    h0 = ROOT.TH1F("h0", "dimuonCR_mass", 1, 70, 110)
    h1 = ROOT.TH1F("h1", "Train_weight", 200, -10, 10)
    h0.Sumw2()
    h1.Sumw2()
    tree.Draw("dimuonCR_mass>>h0", "{}".format(weight_calc_sel), "goff")
    tree.Draw("Train_weight>>h1", "{}".format(weight_calc_sel), "goff")
    weight_mean = h1.GetMean()
    # print("{}'s mean_weight is {}, entries is {}, sqrt(Nw^2) is {}".format(file_name, weight_mean, n_entries, weight_mean*math.sqrt(n_entries)))
    sumw2byhand += weight_mean*math.sqrt(n_entries)
    # total data - non DY mc
    # print("Integral: {}".format(h0.Integral()))
    a = h0.GetSumw2()
    
    if "Muon" in file_name:
        data_yield += n_entries
        data_err += weight_mean*math.sqrt(n_entries)
    if apply_wz_scale and ("WZto" in file_name or "ZZto" in file_name):
        if "m2m" in file_name and "2022" in file_name:
            Integral += h0.Integral()*scale_dict["2022m2m"]
        elif "e2m" in file_name and "2022" in file_name:
            Integral += h0.Integral()*scale_dict["2022e2m"]
        elif "m2m" in file_name and "2023" in file_name:
            Integral += h0.Integral()*scale_dict["2023m2m"]
        elif "e2m" in file_name and "2023" in file_name:
            Integral += h0.Integral()*scale_dict["2023e2m"]
            
    else:
        # total data - non DY mc
        Integral += h0.Integral()
    # Integral += h0.Integral()

    # for i in range(len(a)):
        # print("GetSumw2's {} element: {}".format(i,a[i]))
        # pass
    # sum_a_err = math.sqrt(sum(a))
    # print("toterr sum(a): {}".format(sum_a_err))
    # tot_sum_a_err += sum(a)
    
    err1 = h0.GetBinError(1)
    # err2 = h0.GetBinError(2)
    # err3 = h0.GetBinError(3)
    # err4 = h0.GetBinError(4)
    # err5 = h0.GetBinError(5)
    # err6 = h0.GetBinError(6)
    # err7 = h0.GetBinError(7)
    # err8 = h0.GetBinError(8)
    toterr1 += err1
    # toterr2 += err2
    # toterr3 += err3
    # toterr4 += err4
    # toterr5 += err5
    # toterr6 += err6
    # toterr7 += err7
    # toterr8 += err8

    yield1 = h0.GetBinContent(1)
    # yield2 = h0.GetBinContent(2)
    # yield3 = h0.GetBinContent(3)
    # yield4 = h0.GetBinContent(4)
    # yield5 = h0.GetBinContent(5)
    # yield6 = h0.GetBinContent(6)
    # yield7 = h0.GetBinContent(7)
    # yield8 = h0.GetBinContent(8)
    tot1 += yield1
    # tot2 += yield2
    # tot3 += yield3
    # tot4 += yield4
    # tot5 += yield5
    # tot6 += yield6
    # tot7 += yield7
    # tot8 += yield8

    
    # print("the first bin's err: {}".format(err1))
# print("TOT sqrt toterr sum of sum(a): {}".format(math.sqrt(tot_sum_a_err)))
# print("Yield {} toterr1 using GetBinError: {}".format(tot1,toterr1))
# print("Yield {} toterr2 using GetBinError: {}".format(tot2,toterr2))
# print("Yield {} toterr3 using GetBinError: {}".format(tot3,toterr3))
# print("Yield {} toterr4 using GetBinError: {}".format(tot4,toterr4))
# print("Yield {} toterr5 using GetBinError: {}".format(tot5,toterr5))
# print("Yield {} toterr6 using GetBinError: {}".format(tot6,toterr6))
# print("Yield {} toterr7 using GetBinError: {}".format(tot7,toterr7))
# print("Yield {} toterr8 using GetBinError: {}".format(tot8,toterr8))
toterr = toterr1
# toterr = math.sqrt(toterr1**2+toterr2**2+toterr3**2+toterr4**2+toterr5**2+toterr6**2+toterr7**2+toterr8**2)
print("toterr: {}".format(toterr))
print("total data: {}, err: {}".format(data_yield, data_err))
# print("toterr using sqrt(sumof toterr1-8): {}".format(toterr))
print("total data - non DY mc: {}".format(Integral))
# print("sumw2 by hand: {}".format(sumw2byhand))