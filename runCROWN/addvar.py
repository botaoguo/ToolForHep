import argparse
import sys
import yaml
import os
import ROOT as R
import time
import array

R.gROOT.SetBatch(True)
R.gInterpreter.Declare('#include "/data/bond/botaoguo/CROWN/build_run3/bin/new_variables.h"')

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
        
        if channel == "3l" or channel == "cr_c":

            df_mc = df_mc.Define("ptl1_ov_pt2mu", "extra_lep_pt / H_pt")
            df_mc = df_mc.Define("ptl1_ov_m2mu", "extra_lep_pt / H_mass")
            df_mc = df_mc.Define("pz_nu", "calculateNeutrinoPz(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, met_pt, met_phi)")
            # W and Higgs mumu
            df_mc = df_mc.Define("W_H_dphi", "dphi(W_phi, H_phi)")
            df_mc = df_mc.Define("W_mu1_dphi", "dphi(W_phi, mu1_fromH_phi)")
            df_mc = df_mc.Define("W_mu2_dphi", "dphi(W_phi, mu2_fromH_phi)")
            df_mc = df_mc.Define("ptW_ov_pt2mu", "W_pt / H_pt")
            df_mc = df_mc.Define("W_mass","calc_Wmass(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, met_pt, met_phi, pz_nu)")
            df_mc = df_mc.Define("W_eta","calc_Weta(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, met_pt, met_phi, pz_nu)")
            
            # v1, add lep_mass
            df_mc = df_mc.Define("lep_muOS_cosThStar_WH_v1", "calc_CosThetaStar_WH_v1(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, muOS_pt, muOS_eta, muOS_phi, mu2_fromH_mass)" )
            df_mc = df_mc.Define("lep_muSS_cosThStar_WH_v1", "calc_CosThetaStar_WH_v1(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, muSS_pt, muSS_eta, muSS_phi, mu2_fromH_mass)" )
            # v2, xunwu's method
            df_mc = df_mc.Define("lep_muOS_cosThStar_WH_v2", "calc_CosThetaStar_WH_v2(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, muOS_pt, muOS_eta, muOS_phi, mu2_fromH_mass)" )
            df_mc = df_mc.Define("lep_muSS_cosThStar_WH_v2", "calc_CosThetaStar_WH_v2(extra_lep_pt, extra_lep_eta, extra_lep_phi, extra_lep_mass, muSS_pt, muSS_eta, muSS_phi, mu2_fromH_mass)" )
            
            # define kT and antikT
            # df_mc = df_mc.Define("")
            # met and Higgs mumu
            df_mc = df_mc.Define("met_H_dphi", "dphi(met_phi, H_phi)")
            df_mc = df_mc.Define("met_mu1_dphi", "dphi(met_phi, mu1_fromH_phi)")
            df_mc = df_mc.Define("met_mu2_dphi", "dphi(met_phi, mu2_fromH_phi)")
            

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
    elif args.updated == True:
        input_path = current_path + '/' + 'input_cr_c'
        output_path = current_path + '/' + 'output_cr_c'
    os.system("mkdir -p {}".format(output_path))
    
    post_proc_varial(input_path, output_path)
    print("Target path: {}".format(output_path))
    