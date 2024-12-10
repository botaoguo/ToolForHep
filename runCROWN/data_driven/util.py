import ROOT
import os
import sys
 
# python getNpass.py *e2m*regionb*root
def calc_data_minus_nondy(cr_mass_cut, file_names):
    
    apply_wz_scale = True
    pre_selection = "({}) && trg_single_mu24==1&&mt_W<60".format(cr_mass_cut)

    print("Pre_selection: {}".format(pre_selection))
    print("******************************************")
    Bkg_Yield = []
    Sig_Yield = []
    Data_Yield = []
    DY_Yield = []

    TotBkg_Yield = 0
    TotSig_Yield = 0
    TotData = 0
    TotDY_Yield = 0

    sig_entries = 0
    bkg_entries = 0
    data_entries = 0
    dy_entries = 0
    # Loop over the files
    for file_name in file_names:
        # if 'SingleMuon' in file_name or 'Muon' in file_name:
        #     continue
        # Open the file and get the tree
        file = ROOT.TFile.Open(file_name)
        if not file or file.IsZombie():
            print("Failed to open file {}".format(file_name))
            continue
        tree = file.Get("ntuple")
        if not tree:
            print("Failed to get tree from file {}".format(file_name))
            continue

        # Apply the pre-selection and get the number of entries
        try:
            tree.SetEstimate(tree.GetEntries())
            n_entries = tree.Draw(">>entry_list", pre_selection, "entrylist")
            entry_list = ROOT.gDirectory.Get("entry_list")
        except:
            print("Failed to apply pre-selection or get number of entries from file {}".format(file_name))
            continue

        # Print the number of entries
        # print("NOTICE ************&&&&&&&&&&&&$$$$$$$$########!!!!!!!")
        # print("File {0} has {1} entries passing the pre-selection.".format(file_name,n_entries))

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

        # Integral
        # h0 = ROOT.TH1F("h0", "weight distribution", 200, -10, 10)
        # tree.Draw("Train_weight>>h0", "{}".format(weight_calc_sel), "goff")
        h0 = ROOT.TH1F("h0", "dimuonCR_mass", 1, 70, 110)
        tree.Draw("dimuonCR_mass>>h0", "{}".format(weight_calc_sel), "goff")
        Integral = h0.Integral()
        # print("Integral: {}".format(Integral))
        # calculate event yield
        fileprefix = os.path.splitext(file_name)[0]
        if apply_wz_scale and ("WZto" in fileprefix or "ZZto" in fileprefix):
            if "m2m" in fileprefix:
                # print("m2m Integral before: {}".format(Integral))
                Integral = Integral*1.0898572889149147
                # print("m2m Integral after: {}".format(Integral))
            elif "e2m" in fileprefix:
                # print("e2m Integral before: {}".format(Integral))
                Integral = Integral*1.0266938449768972
                # print("e2m Integral after: {}".format(Integral))
        # print(fileprefix)
        # Weight = (Xsec_dict[fileprefix]*1e3*Lumi) / (Ntot_dict[fileprefix])
        # Yield = (Xsec_dict[fileprefix]*1e3*Lumi*n_entries) / (Ntot_dict[fileprefix])
        
        # print("File {0} 's weight: {1}, Event Yield: {2}".format(file_name,Weight,Yield))
        if 'Hto2Mu' in fileprefix : 
            TotSig_Yield += Integral
            sig_entries += n_entries
            Sig_Yield.append((fileprefix,int(n_entries),Integral))
        elif 'DYto2L' in fileprefix : 
            TotDY_Yield += Integral
            dy_entries += n_entries
            DY_Yield.append((fileprefix,int(n_entries),Integral))
        elif 'Muon' in fileprefix:
            TotData += Integral
            data_entries += n_entries
            Data_Yield.append((fileprefix,int(n_entries),Integral))
        else : 
            TotBkg_Yield += Integral
            bkg_entries += n_entries
            Bkg_Yield.append((fileprefix,int(n_entries),Integral))
        
        # Cleanup
        del entry_list
        file.Close()

    print("Data - nonDY_bkg: {}".format(TotData- TotBkg_Yield))
    return (TotData- TotBkg_Yield)