import sys
import yaml
import os
import ROOT as R
import time
import array

R.gROOT.SetBatch(True)

# need CROWN env

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

def Add_new_column(input_path, output_path, samples_list, new_column):
    '''
    add a new column, new_column should be a dictionary with key name of 
    new column with value of column value (check what type you need)
    new_column = {column_name: value}
    '''
    f_list = getall_list(input_path)
    for f in f_list:
        # add weight==1 only for data
        if 'SingleMuon' not in f:
            continue
        # loop over each file 
        for n in samples_list:
            if n in f:
                print(f)
                try:
                    df_mc = R.RDataFrame('ntuple', f)
                except:
                    print("no tree named ntuple in this file")
                    continue
                col_names = df_mc.GetColumnNames()
                edited = False
                for c in new_column:    
                    if c not in col_names:    
                        edited = True
                        df_mc = df_mc.Define(c,str(new_column[c]))
                if edited:
                    df_mc.Snapshot('ntuple',  f.replace(input_path, output_path))
                else:
                    print( 'column {} already exists, skip'.format(new_column) )

def post_proc_varial(input_path, output_path, samples_list):
    list_all = getall_list(input_path) 
    for f in list_all:
        if 'SingleMuon' in f:
            continue
        for n in samples_list:
            if n in f:
                # print(n)
                print(f)
                try:
                    df_mc = R.RDataFrame('ntuple', f)
                    col_names = df_mc.GetColumnNames()
                except:
                    print("No Column get in this file {}".format(f))
                    continue
                # print(col_names)
                if 'Xsec'  not in col_names:
                    # if merge e2m and m2m, plz use  gensumw /= 2
                    # if only single channel, e2m or m2m, use gensumw
                    gensumw = R.RDataFrame('conditions', f).Sum('genEventSumw').GetValue()
                    if "Embedding" in f:
                        df_mc = df_mc.Define('Xsec', str(samples_list[n]['xsec']) +'f').Define('genEventSumW', '1.0f') # set gensumw for embedding as 1, since we use genWeight directly
                    else:
                        df_mc = df_mc.Define('Xsec', str(samples_list[n]['xsec']) +'f').Define('genEventSumW', str(gensumw) + 'f')
                    # df_mc = df_mc.Define('Train_weight','Xsec* 139e3 * genWeight / genEventSumW') ## define weight calculated
                    df_mc = df_mc.Define('Train_weight','Xsec* 59.8e3 * genWeight / genEventSumW') ## define weight calculated
                    df_mc.Snapshot('ntuple',  f.replace(input_path, output_path)) # update the file finished
    Add_new_column(input_path, output_path, samples_list, { 'Train_weight': '1.0','genWeight': '1.0f', 'Xsec' : '1.0f', 'genEventSumW': '1.0f', 'puweight': '1.0'})


if __name__ == '__main__':       
    # input_path = '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/input_test_3l'
    # output_path = '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/output_test_3l'
    # draw data vs mc ,use below
    # output_path = '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/output_test_3l_2018'    
    
    # input_path = '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/input_test_4l'
    # output_path = '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/output_test_4l'
    # draw data vs mc ,use below
    # output_path = '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/output_test_4l_2018'
    
    input_path = '/data/pubfs/botaoguo/CROWN/build_test0315/bin/input_test_4l'
    output_path = '/data/pubfs/botaoguo/CROWN/build_test0315/bin/output_test_4l_2018'
    
    # print(input_path)
    # exit(0)
    with open("/data/pubfs/botaoguo/CROWN/sample_database/datasets.yaml" , "r") as file:
        samples_list =  yaml.safe_load(file)
        # print(samples_list)
        post_proc_varial(input_path, output_path, samples_list)
