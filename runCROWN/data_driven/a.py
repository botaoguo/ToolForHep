def load_histogram_from_tree(files, n_bins, x_min, x_max):
    hist = ROOT.TH1F("hist_name", "dimuonCR_mass", 40, 70, 110)
    pre_selection = "({}) && trg_single_mu24==1&&mt_W<60".format(cr_mass_cut)
    for file_name in file_names:
        file = ROOT.TFile.Open(file_name)
        if not file or file.IsZombie():
            print("Failed to open file {}".format(file_name))
            continue
        tree = file.Get("ntuple")
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
        tree.Draw("dimuonCR_mass>>hist_name", "{}".format(weight_calc_sel), "goff")
    return hist