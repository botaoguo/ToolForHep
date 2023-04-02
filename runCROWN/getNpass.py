import ROOT
import os
import sys
# from Sample import *

# usage 
# python getNpass.py 3l *.root
# 

# Define the file names and pre-selection criteria
file_names = sys.argv[2:]

if sys.argv[1] == "2l":
    pre_selection = "trg_single_mu24==1"
elif sys.argv[1] == "3l":
    pre_selection = "Flag_dimuon_Zmass_veto==1&&trg_single_mu24==1"
elif sys.argv[1] == "4l":
    pre_selection = "Flag_ZZVeto==1&&trg_single_mu24==1"
else:
    raise RuntimeError("Input the correct category, only support 2l, 3l and 4l")

weight_calc_sel = "Train_weight*" + "(" + pre_selection + ")"
print(weight_calc_sel)
# exit(0)
#
print("Pre_selection: {}".format(pre_selection))
print("******************************************")
Bkg_Yield = []
Sig_Yield = []

TotBkg_Yield = 0
TotSig_Yield = 0
Top_Yield = 0
# Loop over the files
for file_name in file_names:
    if 'SingleMuon' in file_name:
        continue
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
    print("NOTICE ************&&&&&&&&&&&&$$$$$$$$########!!!!!!!")
    print("File {0} has {1} entries passing the pre-selection.".format(file_name,n_entries))

    # Integral
    h0 = ROOT.TH1F("h0", "weight distribution", 200, -10, 10)
    tree.Draw("Train_weight>>h0", "{}".format(weight_calc_sel), "goff")
    Integral = h0.Integral()
    print("Integral: {}".format(Integral))
    # calculate event yield
    fileprefix = os.path.splitext(file_name)[0]
    # Weight = (Xsec_dict[fileprefix]*1e3*Lumi) / (Ntot_dict[fileprefix])
    # Yield = (Xsec_dict[fileprefix]*1e3*Lumi*n_entries) / (Ntot_dict[fileprefix])
    
    # print("File {0} 's weight: {1}, Event Yield: {2}".format(file_name,Weight,Yield))
    if 'HToMuMu' in fileprefix : 
        TotSig_Yield += Integral
        Sig_Yield.append((fileprefix,Integral))
    else : 
        TotBkg_Yield += Integral
        Bkg_Yield.append((fileprefix,Integral))
    # if 'TT' in fileprefix or 'ST' in fileprefix or 'tZq' in fileprefix:
    #     Top_Yield += Yield
    # print(fileprefix)
    # print(Yield)
    # exit(0)
    
    # Cleanup
    del entry_list
    file.Close()

print("Total Signal Yield (VH): {}".format(TotSig_Yield))
print("Total Background Yield: {}".format(TotBkg_Yield))
Sig_Yield.sort(key=lambda x: x[1],reverse=True)
Bkg_Yield.sort(key=lambda x: x[1],reverse=True)
for i in Sig_Yield:
    print(i)
for i in Bkg_Yield:
    print(i)
# print("Top Yield: {}".format(Top_Yield))