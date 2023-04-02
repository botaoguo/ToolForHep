# The name of the TTree in the ntuple.
treename = 'ntuple'

stacking_order = [
    # 3l
    # 'HToMuMu',
    'WHToMuMu',
    # 'ZHToMuMu',
    'WZTo3LNu',
    # 'ZZ+ggZZ',
    # 'top',
    
    # 4l
    # 'ZHToMuMu',
    # 'ZZTo4L',
    # 'ggZZ',
]

sample_colors = {
    # 3l
    # 'HToMuMu' : 632,
    'WHToMuMu' : 880,
    # 'ZHToMuMu' : 624,
    'WZTo3LNu' : 396,
    # 'ZZ+ggZZ' : 4,
    # 'top' : 891,

    # 4l
    # 'ZHToMuMu' : 632,
    # 'ZZTo4L' : 4,
    # 'ggZZ' : 396,
}

# input_pattern = ['/data/pubfs/botaoguo/CROWN/build_addGenW/bin/output_test_3l/%s*.root', \
#                  '/data/pubfs/botaoguo/CROWN/build_addGenW/bin/output_test_4l/%s*.root',]
# for data, use below
input_pattern = ['/data/pubfs/botaoguo/CROWN/build_test0315/bin/output_test_3l_2018/%s*.root', \
                 '/data/pubfs/botaoguo/CROWN/build_test0315/bin/output_test_4l_2018/%s*.root',]

# 16,18 Mu24
# 17 Mu27

def get_samples(channel, signal_overlay=True, **kwargs):
    
    sf_lumi = 1.
    sf_zjb = kwargs.get('sf_zjb', 1.)
    
    ##########################################
    
    samples = {
        # 3l
        'WZTo3LNu': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", sf_zjb*sf_lumi, 'WZTo3LNu', ['WZTo3LNu'],0],
        # 'ZZ+ggZZ': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", sf_zjb*sf_lumi, 'ZZ+ggZZ', ['ZZTo4L','GluGluToContinToZZ'],0],
        # 'top': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", sf_zjb*sf_lumi, 'top', ['TTTT','TTWJetsToLNu','TTZToLLNuNu','tZq_ll'],0],

        # 4l
        # 'ZZTo4L': ["trg_single_mu24==1&&Flag_ZZVeto==1", sf_zjb*sf_lumi, 'ZZTo4L', ['ZZTo4L'],1],
        # 'ggZZ': ["trg_single_mu24==1&&Flag_ZZVeto==1", sf_zjb*sf_lumi, 'ggZZ', ['GluGluToContinToZZ'],1],
        }
    if signal_overlay:
        samples.update({
        # 3l
        # 'HToMuMu': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", 50*sf_zjb*sf_lumi, '(VH3l)*50', ['WminusHToMuMu','WplusHToMuMu','ZHToMuMu'],0],
        'WHToMuMu': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", 1*sf_zjb*sf_lumi, '(WH3l)', ['WminusHToMuMu','WplusHToMuMu'],0],
        # 'ZHToMuMu': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", 50*sf_zjb*sf_lumi, '(ZH3l)*50', ['ZHToMuMu'],0],
        
        # 4l
        # 'ZHToMuMu': ["trg_single_mu24==1&&Flag_ZZVeto==1", 20*sf_zjb*sf_lumi, '(ZH4l)*20', ['ZHToMuMu'],1],       
        })
        
    if channel == 'ggF':
        samples.update({
            # 3l
            # 'Data': ["trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1", sf_zjb*sf_lumi, 'Data', ['SingleMuon'],0],

            # 4l
            # 'Data': ["trg_single_mu24==1&&Flag_ZZVeto==1", sf_zjb*sf_lumi, 'Data', ['SingleMuon'],1],
        })
    
    return samples
