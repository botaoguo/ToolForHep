import argparse
import sys
import yaml
import os
import ROOT as R
import time
import array

R.gROOT.SetBatch(True)

def getall_list(input_path):
    '''
    get a list of all files in input_path
    '''
    inputfile = []
    for fname in os.listdir(input_path):
        if '.root' not in fname or 'FakeFactor' in fname or 'output' in fname or 'input' in fname or 'Fakes' in fname or 'FF' in fname:
            continue
        _file = R.TFile.Open(input_path + '/' + fname)
        if _file.GetListOfKeys().Contains("ntuple"):
            inputfile.append(input_path + '/' + fname)
    # print(inputfile)
    # exit(0)
    return inputfile

def post_proc_varial(input_path, output_path):
    list_all = getall_list(input_path) 
    for f in list_all:
        print(f)
        try:
            df_mc = R.RDataFrame('ntuple', f)
            col_names = df_mc.GetColumnNames()
        except:
            print("No Column get in this file {}".format(f))
            continue
        # define new variable
        
        # for common channel, 3l, 4l, nnmm, fjmm
        df_mc = df_mc.Define("ptmu1_ov_pt2mu", "mu1_fromH_pt / H_pt")
        df_mc = df_mc.Define("ptmu2_ov_pt2mu", "mu2_fromH_pt / H_pt")

        df_mc = df_mc.Define("ptmu1_ov_m2mu", "mu1_fromH_pt / H_mass")
        df_mc = df_mc.Define("ptmu2_ov_m2mu", "mu2_fromH_pt / H_mass")
        df_mc = df_mc.Define("pt2mu_ov_m2mu", "H_pt / H_mass")
        
        if channel == "3l":
            df_mc = df_mc.Define("ptl1_ov_pt2mu", "extra_lep_pt / H_pt")
            df_mc = df_mc.Define("ptl1_ov_m2mu", "extra_lep_pt / H_mass")
        if channel == "4l":
            df_mc = df_mc.Define("pt2l_ov_pt2mu", "Z_pt / H_pt")
            df_mc = df_mc.Define("m2l_ov_pt2mu", "Z_mass / H_pt")
            
            df_mc = df_mc.Define("pt2l_ov_m2mu", "Z_pt / H_mass")
            df_mc = df_mc.Define("m2l_ov_m2mu", "Z_mass / H_mass")
                                
            df_mc = df_mc.Define("ptl1_ov_pt2l", "lep1_fromZ_pt / Z_pt")
            df_mc = df_mc.Define("ptl2_ov_pt2l", "lep2_fromZ_pt / Z_pt")
            df_mc = df_mc.Define("ptmu1_ov_pt2l", "mu1_fromH_pt / Z_pt")
            df_mc = df_mc.Define("ptmu2_ov_pt2l", "mu2_fromH_pt / Z_pt")
                            
            df_mc = df_mc.Define("ptl1_ov_m2l", "lep1_fromZ_pt / Z_mass")
            df_mc = df_mc.Define("ptl2_ov_m2l", "lep2_fromZ_pt / Z_mass")
            df_mc = df_mc.Define("ptmu1_ov_m2l", "mu1_fromH_pt / Z_mass")
            df_mc = df_mc.Define("ptmu2_ov_m2l", "mu2_fromH_pt / Z_mass")
            
            df_mc = df_mc.Define("ptl1_ov_pt2mu", "lep1_fromZ_pt / H_pt")
            df_mc = df_mc.Define("ptl2_ov_pt2mu", "lep2_fromZ_pt / H_pt")
            df_mc = df_mc.Define("ptl1_ov_m2mu", "lep1_fromZ_pt / H_mass")
            df_mc = df_mc.Define("ptl2_ov_m2mu", "lep2_fromZ_pt / H_mass")
        if channel == "MET":
            df_mc = df_mc.Define("met_ov_pt2mu", "met_pt / H_pt")
            df_mc = df_mc.Define("met_ov_m2mu", "met_pt / H_mass")
        if channel == "fjmm":
            df_mc = df_mc.Define("ptfj_ov_pt2mu", "fatjet_pt / H_pt")
            df_mc = df_mc.Define("ptfj_ov_m2mu", "fatjet_pt / H_mass")
            df_mc = df_mc.Define("mfj_ov_m2mu", "fatjet_mass / H_mass")
            df_mc = df_mc.Define("msdfj_ov_m2mu", "fatjet_msoftdrop / H_mass")

            df_mc = df_mc.Define("pnetW_ov_pnetQCD", "fatjet_PNet_withMass_WvsQCD / fatjet_PNet_withMass_QCD")
            df_mc = df_mc.Define("pnetZ_ov_pnetQCD", "fatjet_PNet_withMass_ZvsQCD / fatjet_PNet_withMass_QCD")
            df_mc = df_mc.Define("pnetW_ov_pnetTWZQCD", "fatjet_PNet_withMass_WvsQCD / (fatjet_PNet_withMass_TvsQCD + fatjet_PNet_withMass_WvsQCD + fatjet_PNet_withMass_ZvsQCD+ fatjet_PNet_withMass_QCD)")
            df_mc = df_mc.Define("pnetZ_ov_pnetTWZQCD", "fatjet_PNet_withMass_ZvsQCD / (fatjet_PNet_withMass_TvsQCD + fatjet_PNet_withMass_WvsQCD + fatjet_PNet_withMass_ZvsQCD+ fatjet_PNet_withMass_QCD)")
        
        df_mc.Snapshot('ntuple',  f.replace(input_path, output_path)) # update the file finished

if __name__ == '__main__':       
    
    parser = argparse.ArgumentParser(description='post-process for hmm')
    parser.add_argument('--era', required=True, type=str, help="2022preEE, 2022postEE, 2023preBPix, 2023postBPix")
    parser.add_argument('--ch', required=True, type=str, help="2l,3l,4l,cr_bd,cr_c,cr_fjmm")
    parser.add_argument('--updated', required=False, type=bool, default=False, help="update the factor on CR")
    args = parser.parse_args()
    
    year = args.era
    channel = args.ch
    
    current_path = os.getcwd()
    if args.updated == False:
        input_path = current_path + '/' + 'input'
        output_path = current_path + '/' + 'output'
        # input_path = current_path + '/' + 'output_test_{0}_{1}'.format(channel,year)
        # output_path = current_path + '/' + 'new_var_{0}_{1}'.format(channel,year)
    elif args.updated == True:
        input_path = current_path + '/' + 'output_test_{0}_{1}_updated'.format(channel,year)
        output_path = current_path + '/' + 'new_var_{0}_{1}_updated'.format(channel,year)
    os.system("mkdir -p {}".format(output_path))
    
    post_proc_varial(input_path, output_path)
    print("Target path: {}".format(output_path))
    