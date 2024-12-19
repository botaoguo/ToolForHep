# The name of the TTree in the ntuple.
treename = 'ntuple'

# need a function to return stacking_order, color and plot_vars?

def get_order_color_vars(era, channel):
    if era == '2023preBPix':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/output_test_2l_2023preBPix/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/output_test_2l_2023preBPix/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3/bin/2023preBPix/output/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/output_test_4l_2023preBPix/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3/bin/2023preBPix/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/output_test_3l_2023preBPix/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/output_test_3l_2023preBPix/%s*m2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023preBPix/output_test_cr_fjmm_2023preBPix/%s*fjmm_cr.root'
        ]
    if era == '2023postBPix':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_2l_2023postBPix/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_2l_2023postBPix/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_2l_2023postBPix/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_4l_2023postBPix/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_3l_2023postBPix/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_3l_2023postBPix/%s*m2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023postBPix/output_test_cr_fjmm_2023postBPix/%s*fjmm_cr.root'
        ]
    if era == '2022postEE':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_2l_2022postEE/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_2l_2022postEE/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_3l_2022postEE/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_4l_2022postEE/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_3l_2022postEE/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_3l_2022postEE/%s*m2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022postEE/output_test_cr_fjmm_2022postEE/%s*fjmm_cr.root'
        ]
    if era == '2022preEE':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_2l_2022preEE/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_2l_2022preEE/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_3l_2022preEE/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_4l_2022preEE/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_3l_2022preEE/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_3l_2022preEE/%s*m2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022preEE/output_test_cr_fjmm_2022preEE/%s*fjmm_cr.root'
        ]
    if era == '2022merged':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_2l_2022p*EE/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_2l_2022p*EE/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_3l_2022p*EE/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_4l_2022p*EE/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_3l_2022p*EE/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_3l_2022p*EE/%s*m2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2022p*EE/output_test_cr_fjmm_2022p*EE/%s*fjmm_cr.root'
        ]
    if era == '2023merged':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_2l_2023p*BPix/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_2l_2023p*BPix/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_3l_2023p*BPix/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_4l_2023p*BPix/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_3l_2023p*BPix/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_3l_2023p*BPix/%s*m2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/2023p*BPix/output_test_cr_fjmm_2023p*BPix/%s*fjmm_cr.root'
        ]
    if era == '2022_2023':
        # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        input_pattern = [
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/new_var_2l_202*/%s*_fjmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/new_var_2l_202*/%s*_nnmm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/new_var_3l_202*/%s*2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/new_var_4l_202*/%s*mm.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/%s*e2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/%s*m2m_regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/%s*regionc.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/new_var_3l_202*/%s*e2m.root', \
            '/data/bond/botaoguo/CROWN/build_run3_allsys/bin/202*/new_var_3l_202*/%s*m2m.root', \
            '1'
        ]
    # if era == '2022_2023':
    #     # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
    #     input_pattern = [
    #         '/data/bond/botaoguo/CROWN/linkforRun3/output_test_2l*/%s*_fjmm.root', \
    #         '/data/bond/botaoguo/CROWN/linkforRun3/output_test_2l*/%s*_nnmm.root', \
    #         '/data/bond/botaoguo/CROWN/linkforRun3/output_test_3l*/%s*2m.root', \
    #         '/data/bond/botaoguo/CROWN/linkforRun3/output_test_4l*/%s*mm.root', \
    #         '1', \
    #         '1', \
    #         '/data/bond/botaoguo/CROWN/linkforRun3/%s*regionc.root', \
    #         '1', \
    #         '1', \
    #         '1'
    #     ]
    if channel == '4l':
        stacking_order = [
            # 4l
            'ZHToMuMu',
            'ZZTo4L',
            'other',
        ]
        sample_colors = {
            # 4l
            'ZHToMuMu' : 632,
            'ZZTo4L' : 416,
            'other' : 13, # 891
        }
    else:
        sample_colors = {
            # 3l
            'VHToMuMu' : 632,
            'TTHToMuMu' : 610,
            'WZ' : 396,
            'ZZ' : 416,
            'DYJets' : 4,
            'TTTo2L2Nu' : 870,
            'SingleTop' : 800,
            'triboson' : 891,
            'WW' : 880,            
        }
        if channel == "3l":
            stacking_order = [
                # 3l
                'VHToMuMu',
                'TTHToMuMu',
                'WZ',
                'ZZ',
                'DYJets',
                'TTTo2L2Nu',
                'SingleTop',
                'triboson',
                'WW',
            ]
        elif channel == "MET":
            stacking_order = [
                # 3l
                'VHToMuMu',
                'TTHToMuMu',
                'TTTo2L2Nu',
                'WW',
                'SingleTop',
                'DYJets',
                'WZ',
                'ZZ',
                'triboson',
            ]
        elif channel == "fjmm" or channel == "fjmm_cr":
            stacking_order = [
                # 3l
                'VHToMuMu',
                'TTHToMuMu',
                'DYJets',
                'TTTo2L2Nu',
                'WZ',
                'ZZ',
                'SingleTop',
                'triboson',
                'WW',
            ]            
    return input_pattern, stacking_order, sample_colors

def get_samples(era, channel, **kwargs):
    sf_lumi = 1.
    sf_zjb = kwargs.get('sf_zjb', 1.)
    ##########################################
    if channel == '3l' or channel == 'e2m' or channel == 'm2m':
        loc_num_3l = 2 # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l
        DY_num = 6
        # selection_driven = "(Flag_dimuon_Zmass_veto==1&&trg_single_mu24==1)*(2*is_data - 1)"
        selection_3l = "Flag_dimuon_Zmass_veto==1&&trg_single_mu24==1&&nbjets_loose<=1&&nbjets_medium<=0"
        # selection_3l = "Flag_dimuon_Zmass_veto==1&&trg_single_mu24==1&&nbjets_loose<=1&&nbjets_medium<=0"
        samples = {
            # 3l
            'Data': [selection_3l, sf_zjb*sf_lumi, 'Data', ['Muon'],loc_num_3l],
            'VHToMuMu': [selection_3l, 50*sf_zjb*sf_lumi, '(VH)*50', ['WminusH','WplusH','ZH'],loc_num_3l],
            'TTHToMuMu': [selection_3l, 50*sf_zjb*sf_lumi, '(TTH)*50', ['TTH'],loc_num_3l],
            'WZ': [selection_3l, sf_zjb*sf_lumi, 'WZ', ['WZto'],loc_num_3l],
            'ZZ': [selection_3l, sf_zjb*sf_lumi, 'ZZ', ['ZZto'],loc_num_3l],
            # DYJets using Data driven,
            # 'DYJets': [selection_3l, sf_zjb*sf_lumi, 'DYJets', ['zmerged'],DY_num],
            'TTTo2L2Nu': [selection_3l, sf_zjb*sf_lumi, 'TTTo2L2Nu', ['TTto2L2Nu'],loc_num_3l],
            'SingleTop': [selection_3l, sf_zjb*sf_lumi, 'SingleTop', ['TbarWplusto','TWminusto'],loc_num_3l],
            'triboson': [selection_3l, sf_zjb*sf_lumi, 'triboson', ['WWW','WWZ','WZZ','ZZZ'],loc_num_3l],
            'WW': [selection_3l, sf_zjb*sf_lumi, 'WW', ['WWto'],loc_num_3l],
        }
    if channel == '4l':
        loc_num_4l = 3 # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l
        selection_4l = "trg_single_mu24==1&&Flag_ZZVeto==1&&nbjets_loose<=1&&nbjets_medium<=0&&JetFlag_pass_veto_map==1"
        # selection_4l = "trg_single_mu24==1&&Flag_ZZVeto==1&&nbjets_loose<=1&&nbjets_medium<=0"
        samples = {
            # 4l
            'Data': [selection_4l, sf_zjb*sf_lumi, 'Data', ['Muon'],loc_num_4l],
            'ZHToMuMu': [selection_4l, 20*sf_zjb*sf_lumi, '(ZH4l)*20', ['ZH'],loc_num_4l],
            'ZZTo4L': [selection_4l, sf_zjb*sf_lumi, 'ZZTo4L', ['ZZto4L'],loc_num_4l],
            'other': [selection_4l, sf_zjb*sf_lumi, 'other', ['WWW','WWZ','WZto','WZZ','ZZZ','TTto','WWto','DY'],loc_num_4l],
        }
    if channel == 'MET':
        loc_num_met = 1 # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l
        selection_MET = "trg_single_mu24==1&&nbjets_loose<=1&&nbjets_medium<=0&&JetFlag_pass_veto_map==1"
        # selection_MET = "trg_single_mu24==1&&nbjets_loose<=1&&nbjets_medium<=0"
        samples = {
            # MET
            'Data': [selection_MET, sf_zjb*sf_lumi, 'Data', ['Muon'],loc_num_met],
            'VHToMuMu': [selection_MET, 500*sf_zjb*sf_lumi, '(VH)*500', ['WminusH','WplusH','ZH'],loc_num_met],
            'TTHToMuMu': [selection_MET, 500*sf_zjb*sf_lumi, '(TTH)*500', ['TTH'],loc_num_met],
            'TTTo2L2Nu': [selection_MET, sf_zjb*sf_lumi, 'TTTo2L2Nu', ['TTto2L2Nu'],loc_num_met],
            'WW': [selection_MET, sf_zjb*sf_lumi, 'WW', ['WWto2L2Nu'],loc_num_met],
            'SingleTop': [selection_MET, sf_zjb*sf_lumi, 'SingleTop', ['TbarWplusto','TWminusto'],loc_num_met],
            'DYJets': [selection_MET, sf_zjb*sf_lumi, 'DYJets', ['DYto2'],loc_num_met],
            'WZ': [selection_MET, sf_zjb*sf_lumi, 'WZ', ['WZto'],loc_num_met],
            'ZZ': [selection_MET, sf_zjb*sf_lumi, 'ZZ', ['ZZto'],loc_num_met],
            'triboson': [selection_MET, sf_zjb*sf_lumi, 'triboson', ['WWW','WWZ','WZZ','ZZZ'],loc_num_met],            
        }
    if channel == 'fjmm' or channel == 'fjmm_cr':
        if "cr" in channel:
            loc_num_fjmm = 9
        else:
            loc_num_fjmm = 0 # 0 fjmm, 1 met, 2 3l, 3 4l, 6 DY3l, 9 fjmm_cr
        selection_fjmm = "trg_single_mu24==1&&nbjets_loose<=1&&nbjets_medium<=0&&JetFlag_pass_veto_map==1"
        # selection_fjmm = "trg_single_mu24==1&&nbjets_loose<=1&&nbjets_medium<=0"
        samples = {                        
            # fjmm
            'Data': [selection_fjmm, sf_zjb*sf_lumi, 'Data', ['Muon'],loc_num_fjmm],
            'DYJets': [selection_fjmm, sf_zjb*sf_lumi, 'DYJets', ['DYto2L-2Jets_MLL-50_PTLL'],loc_num_fjmm],
            'TTTo2L2Nu': [selection_fjmm, sf_zjb*sf_lumi, 'TTTo2L2Nu', ['TTto'],loc_num_fjmm],
            'WZ': [selection_fjmm, sf_zjb*sf_lumi, 'WZ', ['WZto'],loc_num_fjmm],
            'WW': [selection_fjmm, sf_zjb*sf_lumi, 'WW', ['WWto'],loc_num_fjmm],
            'ZZ': [selection_fjmm, sf_zjb*sf_lumi, 'ZZ', ['ZZto'],loc_num_fjmm],
            'SingleTop': [selection_fjmm, sf_zjb*sf_lumi, 'SingleTop', ['TbarWplusto','TWminusto'],loc_num_fjmm],
            'triboson': [selection_fjmm, sf_zjb*sf_lumi, 'triboson', ['WWW','WWZ','WZZ','ZZZ'],loc_num_fjmm],
        }
        if channel == 'fjmm':
            samples.update({
                'VHToMuMu': [selection_fjmm, 500*sf_zjb*sf_lumi, '(VH)*500', ['WplusH','WminusH','ZH'],loc_num_fjmm],
                'TTHToMuMu': [selection_fjmm, 500*sf_zjb*sf_lumi, '(TTH)*500', ['TTH'],loc_num_fjmm],
            })
    if channel == 'ggF':
        samples.update({
        # add sth or not
    })
    return samples
