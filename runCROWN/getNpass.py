import ROOT
import os
import sys
import argparse

# usage 
# python getNpass.py 3l *.root ../../../build_2022postEE_v2_allsys/bin/output_test_3l_2022postEE/*.root
# python getNpass.py 2l *fjmm.root ../../../build_2022postEE_v2_allsys/bin/output_test_2l_2022postEE/*fjmm.root
# 
scale_dict = {
    "2022m2m": 1.1387360512110984,
    "2022e2m": 1.139853578151835,
    "2023m2m": 1.1408969060901353,
    "2023e2m": 1.0683926064012228,
}

def run_pass(channel, file_names, do_wzscale):
    apply_wz_scale = False
    # Define the file names and pre-selection criteria
    if channel == "2l" or channel == "cr_fjmm":
        pre_selection = "trg_single_mu24==1"
    elif channel == "3l" or channel == "cr_c":
        pre_selection = "Flag_dimuon_Zmass_veto==1&&trg_single_mu24==1"
        apply_wz_scale = True
        print("apply wz scale now")
    elif channel == "4l":
        pre_selection = "Flag_ZZVeto==1&&trg_single_mu24==1"
    elif channel == "cr_bd":
        if do_wzscale is True:
            pre_selection = "trg_single_mu24==1&&mt_W>60"
            # calculate scale now
            apply_wz_scale = False
        elif do_wzscale is False:
            pre_selection = "(dimuonCR_mass>=85 && dimuonCR_mass<=95)&&trg_single_mu24==1&&mt_W<60"
            # pre_selection = "(dimuonCR_mass>=85 && dimuonCR_mass<=95)&&trg_single_mu24==1"
            print("apply wz scale now")
            apply_wz_scale = True
    else:
        raise RuntimeError("Input the correct category, only support 2l, 3l and 4l")

    # exit(0)
    #
    pre_selection += "&&nbjets_loose<=1&&nbjets_medium<=0"
    print("Pre_selection: {}".format(pre_selection))
    print("******************************************")
    Bkg_Yield = []
    Sig_Yield = []
    Data_Yield = []
    DY_Yield = []
    WZ_Yield = []
    ZZ_Yield = []
    TT_Yield = []
    TTH_Yield = []
    ggH_Yield = []
    VBFH_Yield = []

    TotBkg_Yield = 0
    TotSig_Yield = 0
    TotData = 0
    TotDY_Yield = 0
    TotWZ_Yield = 0
    TotZZ_Yield = 0
    TotTT_Yield = 0
    TotTTH_Yield = 0
    TotggH_Yield = 0
    TotVBFH_Yield = 0

    sig_entries = 0
    bkg_entries = 0
    data_entries = 0
    dy_entries = 0
    wz_entries = 0
    zz_entries = 0
    tt_entries = 0
    tth_entries = 0
    ggh_entries = 0
    vbfh_entries = 0
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
            weight_calc_sel = "Train_weight*puweight*trg_wgt_single_mu24*" +\
                            "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                            "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                            "id_wgt_mu_3*iso_wgt_mu_3*id_wgt_mu_3_below15*iso_wgt_mu_3_below15*" +\
                            "(" + pre_selection + ")"
        elif "e2m" in file_name and "Muon" not in file_name:
            weight_calc_sel = "Train_weight*puweight*trg_wgt_single_mu24*" +\
                            "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                            "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                            "id_wgt_ele_loose_1*id_wgt_ele_wp90Iso_1*reco_wgt_ele_1*" +\
                            "(" + pre_selection + ")"
        elif "fjmm" in file_name and "Muon" not in file_name:
            weight_calc_sel = "Train_weight*puweight*trg_wgt_single_mu24*dy_scale*" +\
                              "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                              "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                              "(" + pre_selection + ")"
        elif "Muon" not in file_name:
            weight_calc_sel = "Train_weight*puweight*trg_wgt_single_mu24*" +\
                            "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                            "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                            "(" + pre_selection + ")"
        else:
            weight_calc_sel = "Train_weight*puweight*" +\
                            "id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*" +\
                            "id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*" +\
                            "(" + pre_selection + ")"
        # Integral
        # h0 = ROOT.TH1F("h0", "weight distribution", 200, -10, 10)
        # tree.Draw("Train_weight>>h0", "{}".format(weight_calc_sel), "goff")
        if "cr" in channel and channel != "cr_c":
            h0 = ROOT.TH1F("h0", "dimuonCR_mass", 1, 70, 110)
            tree.Draw("dimuonCR_mass>>h0", "{}".format(weight_calc_sel), "goff")
        else:
            h0 = ROOT.TH1F("h0", "H_mass", 1, 110, 150)
            tree.Draw("H_mass>>h0", "{}".format(weight_calc_sel), "goff")
        Integral = h0.Integral()
        # print("Integral: {}".format(Integral))
        # calculate event yield
        fileprefix = os.path.splitext(file_name)[0]
        if apply_wz_scale and ("WZto" in fileprefix or "ZZto" in fileprefix):
            if "m2m" in fileprefix and "2022" in fileprefix:
                Integral = Integral*scale_dict["2022m2m"]
            elif "e2m" in fileprefix and "2022" in fileprefix:
                Integral = Integral*scale_dict["2022e2m"]
            elif "m2m" in fileprefix and "2023" in fileprefix:
                Integral = Integral*scale_dict["2023m2m"]
            elif "e2m" in fileprefix and "2023" in fileprefix:
                Integral = Integral*scale_dict["2023e2m"]
        # print(fileprefix)
        # Weight = (Xsec_dict[fileprefix]*1e3*Lumi) / (Ntot_dict[fileprefix])
        # Yield = (Xsec_dict[fileprefix]*1e3*Lumi*n_entries) / (Ntot_dict[fileprefix])
        
        # print("File {0} 's weight: {1}, Event Yield: {2}".format(file_name,Weight,Yield))
        # if 'Hto2Mu' in fileprefix : 
        if 'WminusH' in fileprefix or 'WplusH' in fileprefix or 'ZH' in fileprefix : 
            TotSig_Yield += Integral
            sig_entries += n_entries
            Sig_Yield.append((fileprefix,int(n_entries),Integral))
        elif 'TTH_Hto2Mu' in fileprefix:
            TotTTH_Yield += Integral
            tth_entries += n_entries
            TTH_Yield.append((fileprefix,int(n_entries),Integral))
        elif 'GluGluHto2Mu' in fileprefix:
            TotggH_Yield += Integral
            ggh_entries += n_entries
            ggH_Yield.append((fileprefix,int(n_entries),Integral))
        elif 'VBFHto2Mu' in fileprefix:
            TotVBFH_Yield += Integral
            vbfh_entries += n_entries
            VBFH_Yield.append((fileprefix,int(n_entries),Integral))
        elif 'Muon' in fileprefix:
            TotData += Integral
            data_entries += n_entries
            Data_Yield.append((fileprefix,int(n_entries),Integral))
        else : 
            TotBkg_Yield += Integral
            bkg_entries += n_entries
            Bkg_Yield.append((fileprefix,int(n_entries),Integral))
        
        if 'DYto2L' in fileprefix : 
            TotDY_Yield += Integral
            dy_entries += n_entries
            DY_Yield.append((fileprefix,int(n_entries),Integral))
        if 'WZto' in fileprefix:
            TotWZ_Yield += Integral
            wz_entries += n_entries
            WZ_Yield.append((fileprefix,int(n_entries),Integral))
        if 'ZZto' in fileprefix:
            TotZZ_Yield += Integral
            zz_entries += n_entries
            ZZ_Yield.append((fileprefix,int(n_entries),Integral))
        if 'TTto' in fileprefix:
            TotTT_Yield += Integral
            tt_entries += n_entries
            TT_Yield.append((fileprefix,int(n_entries),Integral))

        # Cleanup
        del entry_list
        file.Close()

    if channel == "cr_fjmm" or ( channel == "cr_bd" and do_wzscale is False ):
        print("Total (non DY) Background Yield: {}".format(TotBkg_Yield - TotDY_Yield))
        print("Total Data: {}".format(TotData))
        print("Total DY: {}".format(TotDY_Yield))
        print("DY in bkg: {}%".format(100*TotDY_Yield/(TotBkg_Yield)))
        print("****************************")
        print("Data - nonDY_bkg: {}".format(TotData- (TotBkg_Yield - TotDY_Yield)))
        if channel == "cr_fjmm":
            print("(Data - nonDY_bkg) / DY: {}".format( (TotData- (TotBkg_Yield - TotDY_Yield)) / TotDY_Yield ))
        print("****************************")
        print("Total signal entries: {}".format(sig_entries))
        print("Total background entries: {}".format(bkg_entries))
        print("Total Data entries: {}".format(data_entries))
        print("Total DY entries: {}".format(dy_entries))
    elif channel == "cr_bd" and do_wzscale is True:
        print("Total (nonWZ_ZZ) Background Yield: {}".format( TotBkg_Yield - (TotWZ_Yield + TotZZ_Yield) ))
        print("Total Data: {}".format(TotData))
        print("Total DY: {}".format(TotDY_Yield))
        print("Total WZ: {}".format(TotWZ_Yield))
        print("Total ZZ: {}".format(TotZZ_Yield))
        print("Total WZ+ZZ: {}".format(TotWZ_Yield + TotZZ_Yield))
        print("****************************")
        print("(Data - nonWZ,ZZ_mc)is {}".format(TotData - (TotBkg_Yield - (TotWZ_Yield + TotZZ_Yield)) ))
        print("(Data - nonWZ,ZZ_mc) / (WZ+ZZ) is {}".format( (TotData - (TotBkg_Yield - (TotWZ_Yield + TotZZ_Yield)) ) / (TotWZ_Yield + TotZZ_Yield) ))
        print("****************************")
        print("Total signal entries: {}".format(sig_entries))
        print("Total background entries: {}".format(bkg_entries))
        print("Total Data entries: {}".format(data_entries))
        print("Total DY entries: {}".format(dy_entries))
        print("Total WZ entries: {}".format(wz_entries))
        print("Total ZZ entries: {}".format(zz_entries))
    else:
        print("Total Signal Yield (VH): {}".format(TotSig_Yield))
        print("Total TTH: {}".format(TotTTH_Yield))
        print("Total ggH: {}".format(TotggH_Yield))
        print("Total VBFH: {}".format(TotVBFH_Yield))
        print("Total Signal: {}".format(TotSig_Yield + TotggH_Yield + TotVBFH_Yield + TotTTH_Yield))

        print("Total Background Yield: {}".format(TotBkg_Yield))
        print("Total Data: {}".format(TotData))
        print("Total WZ: {}".format(TotWZ_Yield))
        print("Total ZZ: {}".format(TotZZ_Yield))
        print("Total DY: {}".format(TotDY_Yield))
        print("Total TT: {}".format(TotTT_Yield))

        print("Total signal entries: {}".format(sig_entries))
        print("Total tth entries: {}".format(tth_entries))
        print("Total Data entries: {}".format(data_entries))
        print("Total WZ entries: {}".format(wz_entries))
        print("Total ZZ entries: {}".format(zz_entries))
        print("Total DY entries: {}".format(dy_entries))
        print("Total TT entries: {}".format(tt_entries))

if __name__ == '__main__':       
    
    parser = argparse.ArgumentParser(description='post-process for hmm')
    parser.add_argument('--ch', required=True, type=str, help="2l,3l,4l,cr_bd,cr_c,cr_fjmm")
    parser.add_argument('--input', required=True, type=str, nargs='+', help="input files")
    parser.add_argument('--wzscale', required=False, default=False, type=bool, help="do wz scale")
    args = parser.parse_args()
    # print(args)
    
    channel = args.ch
    file_names = args.input
    do_wzscale = args.wzscale
    # print(do_wzscale)
    # exit(0)
    # print(file_names)
    run_pass(channel, file_names, do_wzscale)
    print("Done!")
