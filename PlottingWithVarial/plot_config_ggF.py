from samples_HHbbmm import *
from datetime import date
import varial
import ROOT as R
# import wrappers

era = '2023preBPix'
channel = '3l'

input_pattern, stacking_order, sample_colors = get_order_color_vars(era, channel)

####################
# General Settings #
####################

#varial.settings.max_num_processes = 8
varial.settings.rootfile_postfixes += ['.pdf', '.png']
varial.settings.stacking_order = stacking_order
# try to find output on disk and don't run a step if present
enable_reuse_step = True

#################
# Plot Settings #
#################

# name = era+"_"+channel+"_"+str(date.today())+"_001"
name = era+"_"+channel+"_"+str(date.today())+"_nody"+"_001"

if channel == '3l' or channel == 'e2m' or channel == 'm2m':
# 3l e2m mu3's wgt=1, m2m e1's wgt=1
    weight = 'Train_weight*puweight*wz_zz_scale*' +\
             'id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*' +\
             'id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*' +\
             'id_wgt_mu_3*iso_wgt_mu_3*id_wgt_mu_3_below15*iso_wgt_mu_3_below15*' +\
             'id_wgt_ele_loose_1*id_wgt_ele_wp90Iso_1'
elif channel == '4l': 
    weight = 'Train_weight*puweight*' +\
             'id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*' +\
             'id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15*' +\
             'id_wgt_mu_3*iso_wgt_mu_3*id_wgt_mu_3_below15*iso_wgt_mu_3_below15*' +\
             'id_wgt_mu_4*iso_wgt_mu_4*id_wgt_mu_4_below15*iso_wgt_mu_4_below15*' +\
             'id_wgt_ele_loose_1*id_wgt_ele_loose_2*id_wgt_ele_wp90Iso_1*id_wgt_ele_wp90Iso_2'
elif channel == "MET":
    weight = 'Train_weight*puweight*' +\
             'id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*' +\
             'id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15'
elif channel == "fjmm" or channel == "fjmm_cr":
    # weight = 'Train_weight*puweight*' +\
    weight = 'Train_weight*puweight*dy_scale*' +\
             'id_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_1*iso_wgt_mu_2*' +\
             'id_wgt_mu_1_below15*id_wgt_mu_2_below15*iso_wgt_mu_1_below15*iso_wgt_mu_2_below15'

if channel == '3l' or channel == 'e2m' or channel == 'm2m':
    plot_vars = {
        # # WH3l 
        'H_pt' : ('H_pt', ';p_{T}^{H} [GeV];', 15,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu1_fromH_eta)' : ('abs(mu1_fromH_eta)', ';#eta_{#mu1};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu2_fromH_eta)' : ('abs(mu2_fromH_eta)', ';#eta_{#mu2};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mumuH_dR)' : ('abs(mumuH_dR)', ';#Delta R(#mu#mu) [m];', 12,0,6), # (50,0,4.5) overlay or (30,0,6) stack

        'extra_lep_pt' : ('extra_lep_pt', ';p_{T}^{lep} [GeV];', 10,0,200), # (50,20,320) overlay or (20,0,200) stack
        'nelectrons' : ('nelectrons', ';nEles;', 2,0,2),
        'abs(lep_H_dR)' : ('abs(lep_H_dR)', ';#Delta R(lep_H) [m];', 12,0,6), # (50,0,8) overlay or (20,0,6) stack
        'abs(lep_H_deta)' : ('abs(lep_H_deta)', ';#Delta#eta(lep_H);', 10,0,5), # (60,0,6) overlay or (20,0,5) stack

        # lep_muSS_cosThStar -> done
        'abs(lep_muSS_deta)' : ('abs(lep_muSS_deta)', ';#Delta#eta(lep_#mu_{SS});', 10,0,5), # (50,0,5) overlay or (20,0,5) stack
        'lep_muSS_cosThStar' : ('lep_muSS_cosThStar', ';cos(#theta_{lep_#mu_{SS}});', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'abs(lep_muOS_dR)' : ('abs(lep_muOS_dR)', ';#Delta R(lep_#mu_{OS}) [m];', 12,0,6), # (60,0,6) overlay or (20,0,6) stack
        'abs(lep_muOS_deta)' : ('abs(lep_muOS_deta)', ';#Delta#eta(lep_#mu_{OS});', 10,0,5), # (50,0,5) overlay or (20,0,5) stack

        # lep_muOS_cosThStar -> done
        'lep_muOS_cosThStar' : ('lep_muOS_cosThStar', ';cos(#theta_{lep_#mu_{OS}});', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        # 'mt_muSSAndMHT' : ('mt_muSSAndMHT', ';mt(#mu_{SS}_MHT) [GeV];', 30,0,300), # (60,0,600) overlay or (30,0,300) stack
        'mt_muSSAndMHTALL' : ('mt_muSSAndMHTALL', ';mt(#mu_{SS}_MHTALL) [GeV];', 30,0,300), # (60,0,600) overlay or (30,0,300) stack
        # 'mt_lepWAndMHT' : ('mt_lepWAndMHT', ';mt(lep_MHT) [GeV];', 20,0,200), # (60,0,300) overlay or (20,0,200) stack
        'mt_lepWAndMHTALL' : ('mt_lepWAndMHTALL', ';mt(lep_MHTALL) [GeV];', 20,0,200), # (60,0,300) overlay or (20,0,200) stack
        'abs(lep_MHT_dphi)' : ('abs(lep_MHT_dphi)', ';#Delta#phi_{lep}^{MHT};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(lep_MHTALL_dphi)' : ('abs(lep_MHTALL_dphi)', ';#Delta#phi_{MHTALL}^{lep};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(lep_MET_dphi)' : ('abs(lep_MET_dphi)', ';#Delta#phi(lep,MET);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        
        # More 3L Var
        'abs(H_eta)' : ('abs(H_eta)', ';#eta_{H};', 14,0,7), # (50,0,7) overlay or (14,0,7) stack
        'abs(H_phi)' : ('abs(H_phi)', ';|#phi(#mu#mu)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(extra_lep_eta)' : ('abs(extra_lep_eta)', ';#eta_{lep};', 14,0,7), # (50,0,7) overlay or (14,0,7) stack
        'abs(extra_lep_phi)' : ('abs(extra_lep_phi)', ';|#phi(lep)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        
        'abs(lep_H_dphi)' : ('abs(lep_H_dphi)', ';#Delta#phi_{lep}^{H};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(lep_mu1_dphi)' : ('abs(lep_mu1_dphi)', ';#Delta#phi_{lep}^{mu_1};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(lep_mu2_dphi)' : ('abs(lep_mu2_dphi)', ';#Delta#phi_{lep}^{mu_2};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(lep_muSS_dR)' : ('abs(lep_muSS_dR)', ';#Delta R(lep_#mu_{SS}) [m];', 12,0,6), # (60,0,6) overlay or (12,0,6) stack
        
        'met_pt' : ('met_pt', ';MET [GeV];', 15,0,300), # (60,0,300) overlay or (30,0,300) stack
        'abs(met_phi)' : ('abs(met_phi)', ';|#phi(MET)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'mt_W' : ('mt_W', ';M_{t} (W) [GeV];', 15,0,300), # (60,0,300) overlay or (30,0,300) stack
        # 'mt_muOSAndMHT' : ('mt_muOSAndMHT', ';mt(#mu_{OS}_MHT) [GeV];', 30,0,300), # (60,0,600) overlay or (30,0,300) stack
        'mt_muOSAndMHTALL' : ('mt_muOSAndMHTALL', ';mt(#mu_{OS}_MHTALL) [GeV];', 30,0,300), # (60,0,600) overlay or (30,0,300) stack
        
        # 'abs(mu1_MHT_dphi)' : ('abs(mu1_MHT_dphi)', ';#Delta#phi_{mu_1}^{MHT};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu1_MHTALL_dphi)' : ('abs(mu1_MHTALL_dphi)', ';#Delta#phi_{mu_1}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu1_fromH_phi)' : ('abs(mu1_fromH_phi)', ';|#phi(#mu 1)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'mu1_fromH_pt' : ('mu1_fromH_pt', ';Pt(#mu 1) [GeV];', 15,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu1_mu2_dphi)' : ('abs(mu1_mu2_dphi)', ';#Delta#phi_{mu_1}^{mu_2};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        # 'abs(mu2_MHT_dphi)' : ('abs(mu2_MHT_dphi)', ';#Delta#phi_{mu_2}^{MHT};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu2_MHTALL_dphi)' : ('abs(mu2_MHTALL_dphi)', ';#Delta#phi_{mu_2}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu2_fromH_phi)' : ('abs(mu2_fromH_phi)', ';|#phi(#mu 2)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'mu2_fromH_pt' : ('mu2_fromH_pt', ';Pt(#mu 2) [GeV];', 15,0,300), # (60,0,600) overlay or (30,0,300) stack

        # 'abs(mumuH_MHT_dphi)' : ('abs(mumuH_MHT_dphi)', ';#Delta#phi_{H}^{MHT};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mumuH_MHTALL_dphi)' : ('abs(mumuH_MHTALL_dphi)', ';#Delta#phi_{H}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'njets' : ('njets', ';njets;', 12,0,12),
        
        'H_mass' : ('H_mass', ';Mass(#mu#mu) [GeV];', 8,110,150),
        # DNN 3l dnn_score
        # 'dnn_WZTo3LNu_score' : ('dnn_WZTo3LNu_score', 'WZscore', 20,0,1),
        # 'dnn_ZZTo4L_score' : ('dnn_ZZTo4L_score', 'ZZscore', 20,0,1),
        # 'score_51' : ('score_51', 'DNN51score', 20,0,1),
        # 'score_61' : ('score_61', 'DNN61score', 20,0,1),
        # 'score_avg' : ('score_avg', '(Score(WZ)+Score(ZZ))/2', 20,0,1),
        # 'score_times' : ('score_times', 'Score(WZ)*Score(ZZ)', 20,0,1),
        # 'dnn_MET150_score' : ('dnn_MET150_score', 'dnn_MET150_score', 20,0,1),
        # 'dnn_fjmm_score' : ('dnn_fjmm_score', 'dnn_fjmm_score', 20,0,1),
    }
if channel == "4l":
    plot_vars = {
        # ZH4l
        # need leptonID and ZH_cosThStar -> done
        'H_pt' : ('H_pt', ';p_{T}^{H} [GeV];', 10,0,400), # (60,0,600) overlay or (10,0,400) stack
        'abs(H_eta)' : ('abs(H_eta)', ';#eta_{H};', 10,0,6), # (50,0,7) overlay or (10,0,6) stack
        'Z_pt' : ('Z_pt', ';p_{T}^{Z} [GeV];', 10,0,300), # (60,0,600) overlay or (10,0,300) stack
        'abs(mumuH_dphi)' : ('abs(mumuH_dphi)', ';#Delta#phi(#mu#mu);', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        'Z_mass' : ('Z_mass', ';Mass(Z) [GeV];', 10,70,110), # (50,81,101) overlay or (10,70,110)
        'abs(Z_eta)' : ('abs(Z_eta)', ';#eta_{Z};', 10,0,6), # (50,0,7) overlay or (10,0,6) stack
        'abs(llZ_dR)' : ('abs(llZ_dR)', ';#Delta R(ll) [m];', 10,0,5), # (50,0,5) overlay or (10,0,5) stack
        'abs(Z_H_deta)' : ('abs(Z_H_deta)', ';#Delta#eta(ZH);', 10,0,10), # (60,0,9) overlay or (10,0,10)
        'Zlep_ID' : ('Zlep_ID', ';Zlep ID;', 3,11,14),
        'Z_H_cosThStar' : ('Z_H_cosThStar', ';cos(#theta_{Z_H});', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack

        'abs(H_phi)' : ('abs(H_phi)', ';|#phi(#mu#mu)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'Z_H_dphi' : ('Z_H_dphi', ';#Delta#phi_{Z}^{H};', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'abs(Z_phi)' : ('abs(Z_phi)', ';|#phi(Z)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'abs(lep1_fromZ_eta)' : ('abs(lep1_fromZ_eta)', ';#eta_{Zlep_1};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(lep1_fromZ_phi)' : ('abs(lep1_fromZ_phi)', ';|#phi(Zlep_1)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'lep1_fromZ_pt' : ('lep1_fromZ_pt', ';Pt(lep_1) [GeV];', 15,0,300), # (60,0,600) overlay or (20,0,300) stack
        'abs(lep2_fromZ_eta)' : ('abs(lep2_fromZ_eta)', ';#eta_{Zlep_2};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(lep2_fromZ_phi)' : ('abs(lep2_fromZ_phi)', ';|#phi(Zlep_2)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'lep2_fromZ_pt' : ('lep2_fromZ_pt', ';Pt(lep_2) [GeV];', 15,0,300), # (60,0,600) overlay or (20,0,300) stack

        'abs(mu1_fromH_eta)' : ('abs(mu1_fromH_eta)', ';#eta_{#mu1};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu1_fromH_phi)' : ('abs(mu1_fromH_phi)', ';|#phi(#mu 1)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'mu1_fromH_pt' : ('mu1_fromH_pt', ';Pt(#mu 1) [GeV];', 15,0,300), # (60,0,600) overlay or (20,0,300) stack
        'abs(mu2_fromH_eta)' : ('abs(mu2_fromH_eta)', ';#eta_{#mu2};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu2_fromH_phi)' : ('abs(mu2_fromH_phi)', ';|#phi(#mu 2)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'mu2_fromH_pt' : ('mu2_fromH_pt', ';Pt(#mu 2) [GeV];', 15,0,300), # (60,0,600) overlay or (20,0,300) stack
        'met_pt' : ('met_pt', ';MET [GeV];', 15,0,300), # (60,0,300) overlay or (20,0,300) stack
        'abs(met_phi)' : ('abs(met_phi)', ';|#phi(MET)|;', 10,0,3.15), # (50,0,3.15) overlay or (10,0,3.15) stack
        'njets' : ('njets', ';njets;', 12,0,12),
        'abs(mumuH_dR)' : ('abs(mumuH_dR)', ';#Delta R(#mu#mu) [m];', 12,0,6), # (50,0,4.5) overlay or (9,0,4.5) stack
        'H_mass' : ('H_mass', ';Mass(#mu#mu) [GeV];', 8,110,150),
    }
if channel == "MET":
    plot_vars = {
        # MET
        'H_pt' : ('H_pt', ';Pt(#mu#mu) [GeV];', 15,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(H_eta)' : ('abs(H_eta)', ';|#eta(#mu#mu)|;', 16,0,4), # (50,0,7) overlay or (16,0,4) stack
        'abs(H_phi)' : ('abs(H_phi)', ';|#phi(#mu#mu)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack

        'abs(mumuH_dR)' : ('abs(mumuH_dR)', ';#Delta R(#mu#mu) [m];', 12,0,6), # (50,0,5) overlay or (30,0,6) stack
        'abs(mumuH_MHTALL_dphi)' : ('abs(mumuH_MHTALL_dphi)', ';#Delta#phi_{H}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'njets' : ('njets', ';njets;', 12,0,12),

        'mu1_fromH_pt' : ('mu1_fromH_pt', ';Pt(#mu 1) [GeV];', 15,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu1_fromH_eta)' : ('abs(mu1_fromH_eta)', ';|#eta(#mu 1)|;', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu1_fromH_phi)' : ('abs(mu1_fromH_phi)', ';|#phi(#mu 1)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        'mu2_fromH_pt' : ('mu2_fromH_pt', ';Pt(#mu 2) [GeV];', 15,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu2_fromH_eta)' : ('abs(mu2_fromH_eta)', ';|#eta(#mu 2)|;', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu2_fromH_phi)' : ('abs(mu2_fromH_phi)', ';|#phi(#mu 2)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack

        'abs(mu1_mu2_dphi)' : ('abs(mu1_mu2_dphi)', ';#Delta#phi(#mu#mu);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu1_MHTALL_dphi)' : ('abs(mu1_MHTALL_dphi)', ';#Delta#phi_{mu_1}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu2_MHTALL_dphi)' : ('abs(mu2_MHTALL_dphi)', ';#Delta#phi_{mu_2}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        'met_pt' : ('met_pt', ';MET [GeV];', 15,150,450), # (60,0,300) overlay or (15,150,300) stack
        'abs(met_phi)' : ('abs(met_phi)', ';|#phi(MET)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        'abs(met_H_dphi)' : ('abs(met_H_dphi)', ';#Delta#phi(MET_H);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'H_mass' : ('H_mass', ';Mass(#mu#mu) [GeV];', 8,110,150),
    }    
if channel == "fjmm":
    plot_vars = {
        # fjmm
        'fatjet_pt' : ('fatjet_pt', ';p_{T}^{AK8Jet} [GeV];', 15,150,600), # (60,150,750) overlay or (30,150,600) stack
        'abs(fatjet_eta)' : ('abs(fatjet_eta)', ';|#eta_{AK8Jet}|;', 10,0,2.5), # (50,0,2.5) overlay or (10,0,2.5) stack
        'fatjet_eta' : ('fatjet_eta', ';#eta_{AK8Jet};', 20,-2.5,2.5), # (50,0,2.5) overlay or (10,0,2.5) stack
        'abs(fatjet_phi)' : ('abs(fatjet_phi)', ';|#phi(AK8Jet)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        'fatjet_mass' : ('fatjet_mass', ';Mass(AK8Jet) [GeV];', 15,50,200), # (50,50,300) overlay or (30,50,200) stack
        'fatjet_msoftdrop' : ('fatjet_msoftdrop', ';MassSoftDrop(AK8Jet) [GeV];', 15,50,200), # (50,50,300) overlay or (30,50,200) stack
        
        'H_pt' : ('H_pt', ';Pt(#mu#mu) [GeV];', 15,0,450), # (60,0,600) overlay or (30,0,450) stack
        'abs(H_eta)' : ('abs(H_eta)', ';|#eta(#mu#mu)|;', 16,0,4), # (50,0,7) overlay or (16,0,4) stack
        'H_eta' : ('H_eta', ';#eta(#mu#mu);', 16,-4,4), # (50,0,7) overlay or (16,0,4) stack
        'abs(H_phi)' : ('abs(H_phi)', ';|#phi(#mu#mu)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack

        'abs(fatjet_mmH_dR)' : ('abs(fatjet_mmH_dR)', ';#Delta R(AK8 H) [m];', 12,0,6), # (50,0,5) overlay or (30,0,6) stack
        'abs(fatjet_mmH_deta)' : ('abs(fatjet_mmH_deta)', ';#Delta #eta(AK8 H);', 10,0,5), # (50,0,5) overlay or (20,0,5) stack
        'abs(fatjet_mmH_dphi)' : ('abs(fatjet_mmH_dphi)', ';#Delta #phi(AK8 H);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        'abs(fatjet_mu1_dR)' : ('abs(fatjet_mu1_dR)', ';#Delta R(AK8 #mu^1) [m];', 12,0,6), # (50,0,5) overlay or (30,0,6) stack
        'abs(fatjet_mu1_deta)' : ('abs(fatjet_mu1_deta)', ';#Delta #eta(AK8 #mu^1);', 10,0,5), # (50,0,5) overlay or (20,0,5) stack
        'abs(fatjet_mu1_dphi)' : ('abs(fatjet_mu1_dphi)', ';#Delta #phi(AK8 #mu^1);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(fatjet_mu2_dR)' : ('abs(fatjet_mu2_dR)', ';#Delta R(AK8 #mu^2) [m];', 12,0,6), # (50,0,5) overlay or (30,0,6) stack
        'abs(fatjet_mu2_deta)' : ('abs(fatjet_mu2_deta)', ';#Delta #eta(AK8 #mu^2);', 10,0,5), # (50,0,5) overlay or (20,0,5) stack
        'abs(fatjet_mu2_dphi)' : ('abs(fatjet_mu2_dphi)', ';#Delta #phi(AK8 #mu^2);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        'abs(met_H_dphi)' : ('abs(met_H_dphi)', ';|#Delta#phi(MET_H)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        
        # 'abs(mu1_MHT_dphi)' : ('abs(mu1_MHT_dphi)', ';#Delta#phi_{mu_1}^{MHT};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        # 'abs(mu1_MHTALL_dphi)' : ('abs(mu1_MHTALL_dphi)', ';#Delta#phi_{mu_1}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'mu1_fromH_pt' : ('mu1_fromH_pt', ';Pt(#mu 1) [GeV];', 10,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu1_fromH_eta)' : ('abs(mu1_fromH_eta)', ';#eta_{#mu1};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'mu1_fromH_eta' : ('mu1_fromH_eta', ';#eta_{#mu1};', 12,-2.4,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu1_fromH_phi)' : ('abs(mu1_fromH_phi)', ';|#phi(#mu 1)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
            
        'abs(mu1_mu2_dphi)' : ('abs(mu1_mu2_dphi)', ';#Delta#phi_{mu_1}^{mu_2};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        # 'abs(mu2_MHT_dphi)' : ('abs(mu2_MHT_dphi)', ';#Delta#phi_{mu_2}^{MHT};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        # 'abs(mu2_MHTALL_dphi)' : ('abs(mu2_MHTALL_dphi)', ';#Delta#phi_{mu_2}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'mu2_fromH_pt' : ('mu2_fromH_pt', ';Pt(#mu 2) [GeV];', 10,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu2_fromH_eta)' : ('abs(mu2_fromH_eta)', ';|#eta_{#mu2}|;', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'mu2_fromH_eta' : ('mu2_fromH_eta', ';#eta_{#mu2};', 12,-2.4,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu2_fromH_phi)' : ('abs(mu2_fromH_phi)', ';|#phi(#mu 2)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        
        # 'abs(mumuH_MHT_dphi)' : ('abs(mumuH_MHT_dphi)', ';|#Delta#phi_{H}^{MHT}|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        # 'abs(mumuH_MHTALL_dphi)' : ('abs(mumuH_MHTALL_dphi)', ';|#Delta#phi_{H}^{MHTALL}|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mumuH_dR)' : ('abs(mumuH_dR)', ';#Delta R(#mu#mu) [m];', 12,0,6), # (50,0,5) overlay or (30,0,6) stack

        # 'fatjet_PNet_QCD' : ('fatjet_PNet_QCD', ';fatjet_PNet_QCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_QCD' : ('fatjet_PNet_withMass_QCD', ';fatjet_PNet_withMass_QCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_WvsQCD' : ('fatjet_PNet_withMass_WvsQCD', ';fatjet_PNet_withMass_WvsQCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_ZvsQCD' : ('fatjet_PNet_withMass_ZvsQCD', ';fatjet_PNet_withMass_ZvsQCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_TvsQCD' : ('fatjet_PNet_withMass_TvsQCD', ';fatjet_PNet_withMass_TvsQCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'H_mass' : ('H_mass', ';Mass(#mu#mu) [GeV];', 8,110,150),
    }
if channel == "fjmm_cr":
    plot_vars = {
        # fjmm
        'fatjet_pt' : ('fatjet_pt', ';p_{T}^{AK8Jet} [GeV];', 15,150,600), # (60,150,750) overlay or (30,150,600) stack
        'abs(fatjet_eta)' : ('abs(fatjet_eta)', ';|#eta_{AK8Jet}|;', 10,0,2.5), # (50,0,2.5) overlay or (10,0,2.5) stack
        'abs(fatjet_phi)' : ('abs(fatjet_phi)', ';|#phi(AK8Jet)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        'fatjet_mass' : ('fatjet_mass', ';Mass(AK8Jet) [GeV];', 15,50,200), # (50,50,300) overlay or (30,50,200) stack
        'fatjet_msoftdrop' : ('fatjet_msoftdrop', ';MassSoftDrop(AK8Jet) [GeV];', 15,50,200), # (50,50,300) overlay or (30,50,200) stack        

        'dimuonCR_mass' : ('dimuonCR_mass', ';Mass(#mu#mu) [GeV];', 8,70,110),
        'dimuonCR_pt' : ('dimuonCR_pt', ';p_{T}^{#mu#mu} [GeV];', 30,0,600), # (60,0,600) overlay or (30,0,300) stack
        'abs(dimuonCR_eta)' : ('abs(dimuonCR_eta)', ';#eta_{#mu#mu};', 14,0,7), # (50,0,7) overlay or (14,0,7) stack
        'abs(dimuonCR_phi)' : ('abs(dimuonCR_phi)', ';|#phi(#mu#mu)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        'abs(met_mm_fromZCR_dphi)' : ('abs(met_mm_fromZCR_dphi)', ';|#Delta#phi(MET,Z)|;', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'met_pt' : ('met_pt', ';MET [GeV];', 15,0,150),
        'abs(met_phi)' : ('abs(met_phi)', ';|#phi(MET)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack

        'mu1_fromZCR_pt' : ('mu1_fromZCR_pt', ';Pt(#mu1) [GeV];', 20,0,600), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu1_fromZCR_eta)' : ('abs(mu1_fromZCR_eta)', ';#eta_{#mu1};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu1_fromZCR_phi)' : ('abs(mu1_fromZCR_phi)', ';|#phi(#mu1)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack
        'mu2_fromZCR_pt' : ('mu2_fromZCR_pt', ';Pt(#mu2) [GeV];', 10,0,300), # (60,0,600) overlay or (30,0,300) stack
        'abs(mu2_fromZCR_eta)' : ('abs(mu2_fromZCR_eta)', ';#eta_{#mu2};', 12,0,2.4), # (60,0,2.4) overlay or (12,0,2.4) stack
        'abs(mu2_fromZCR_phi)' : ('abs(mu2_fromZCR_phi)', ';|#phi(#mu2)|;', 10,0,4), # (50,0,3.15) overlay or (10,0,4) stack

        'abs(mu1_fromZCR_MHTALL_dphi)' : ('abs(mu1_fromZCR_MHTALL_dphi)', ';#Delta#phi_{mu_1}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(mu2_fromZCR_MHTALL_dphi)' : ('abs(mu2_fromZCR_MHTALL_dphi)', ';#Delta#phi_{mu_2}^{MHTALL};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        'abs(mumuZCR_dR)' : ('abs(mumuZCR_dR)', ';#Delta R(#mu#mu) [m];', 12,0,6), # (50,0,5) overlay or (30,0,6) stack
        'abs(mumuZCR_deta)' : ('abs(mumuZCR_deta)', ';#Delta #eta(#mu#mu);', 10,0,5), # (50,0,5) overlay or (30,0,6) stack
        'abs(mumuZCR_dphi)' : ('abs(mumuZCR_dphi)', ';#Delta #phi(#mu#mu);', 16,0,3.2), # (50,0,5) overlay or (30,0,6) stack
        # same var with mumuZCR_dphi
        # 'abs(mu1_mu2_fromZCR_dphi)' : ('abs(mu1_mu2_fromZCR_dphi)', ';#Delta#phi(#mu#mu);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack

        'fatjet_PNet_withMass_QCD' : ('fatjet_PNet_withMass_QCD', ';fatjet_PNet_withMass_QCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_WvsQCD' : ('fatjet_PNet_withMass_WvsQCD', ';fatjet_PNet_withMass_WvsQCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_ZvsQCD' : ('fatjet_PNet_withMass_ZvsQCD', ';fatjet_PNet_withMass_ZvsQCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
        'fatjet_PNet_withMass_TvsQCD' : ('fatjet_PNet_withMass_TvsQCD', ';fatjet_PNet_withMass_TvsQCD;', 10,0,1), # (50,0,1) overlay or (20,0,1) stack
    }

plot_vars.update({
    'ptmu1_ov_pt2mu' : ('ptmu1_ov_pt2mu', ';p_T(#mu1) / p_T(#mu#mu);', 16,0,4.0), # (50,0,1) overlay or (20,0,1) stack
    'ptmu2_ov_pt2mu' : ('ptmu2_ov_pt2mu', ';p_T(#mu2) / p_T(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack

    'ptmu1_ov_m2mu' : ('ptmu1_ov_m2mu', ';p_T(#mu1) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
    'ptmu2_ov_m2mu' : ('ptmu2_ov_m2mu', ';p_T(#mu2) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
    'pt2mu_ov_m2mu' : ('pt2mu_ov_m2mu', ';p_T(#mu#mu) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
    
})
if channel == "3l":
    plot_vars.update({
        'ptl1_ov_pt2mu' : ('ptl1_ov_pt2mu', ';p_T(lep1) / p_T(#mu#mu);', 30,0,3.0), # (50,0,1) overlay or (20,0,1) stack
        'ptl1_ov_m2mu' : ('ptl1_ov_m2mu', ';p_T(lep1) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
        
        'pz2_nu' : ('pz2_nu', ';pz2(#nu);', 30,-100,500), # (50,0,1) overlay or (20,0,1) stack
        'pz1_nu' : ('pz1_nu', ';pz1(#nu);', 30,-100,500), # (50,0,1) overlay or (20,0,1) stack
        'W_pt' : ('W_pt', ';p_T(W);', 30, 0, 300), # (50,0,1) overlay or (20,0,1) stack
        'abs(W_phi)' : ('abs(W_phi)', ';#phi(W);', 16, 0, 3.2), # (50,0,1) overlay or (20,0,1) stack
        
        'abs(W_H_dphi)' : ('abs(W_H_dphi)', ';#Delta#phi_{W}^{H};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(W_mu1_dphi)' : ('abs(W_mu1_dphi)', ';#Delta#phi_{W}^{mu1};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(W_mu2_dphi)' : ('abs(W_mu2_dphi)', ';#Delta#phi_{W}^{mu2};', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'ptW_ov_pt2mu' : ('ptW_ov_pt2mu', ';p_T(W) / p_T(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
        'W_mass1' : ('W_mass1', ';Mass1(W) [GeV];', 16,60,100),
        'W_mass2' : ('W_mass2', ';Mass2(W) [GeV];', 16,60,100),
        'abs(W_eta1)' : ('abs(W_eta1)', ';#eta1_{W};', 14,0,7), # (50,0,7) overlay or (14,0,7) stack
        'abs(W_eta2)' : ('abs(W_eta2)', ';#eta2_{W};', 14,0,7), # (50,0,7) overlay or (14,0,7) stack

        'lep_muOS_cosThStar_toW1H' : ('lep_muOS_cosThStar_toW1H', ';cos(#theta_{lep_#mu_{OS}}) to W1H;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muOS_cosThStar_toW2H' : ('lep_muOS_cosThStar_toW2H', ';cos(#theta_{lep_#mu_{OS}}) to W2H;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muSS_cosThStar_toW1H' : ('lep_muSS_cosThStar_toW1H', ';cos(#theta_{lep_#mu_{SS}}) to W1H;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muSS_cosThStar_toW2H' : ('lep_muSS_cosThStar_toW2H', ';cos(#theta_{lep_#mu_{SS}}) to W2H;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack

        'lep_muOS_cosThStar_toW1toH' : ('lep_muOS_cosThStar_toW1toH', ';cos(#theta_{lep_#mu_{OS}}) to W1 toH;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muOS_cosThStar_toW2toH' : ('lep_muOS_cosThStar_toW2toH', ';cos(#theta_{lep_#mu_{OS}}) to W2 toH;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muSS_cosThStar_toW1toH' : ('lep_muSS_cosThStar_toW1toH', ';cos(#theta_{lep_#mu_{SS}}) to W1 toH;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muSS_cosThStar_toW2toH' : ('lep_muSS_cosThStar_toW2toH', ';cos(#theta_{lep_#mu_{SS}}) to W2 toH;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack

        'lep_muOS_cosThStar_WH_v2' : ('lep_muOS_cosThStar_WH_v2', ';cos(#theta_{lep_#mu_{OS}}) xunwu;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack
        'lep_muSS_cosThStar_WH_v2' : ('lep_muSS_cosThStar_WH_v2', ';cos(#theta_{lep_#mu_{SS}}) xunwu;', 10,-1,1), # (50,-1,1) overlay or (10,-1,1) stack    
        
        'abs(met_H_dphi)' : ('abs(met_H_dphi)', ';#Delta#phi(MET_H);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(met_mu1_dphi)' : ('abs(met_mu1_dphi)', ';#Delta#phi(MET_mu1);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
        'abs(met_mu2_dphi)' : ('abs(met_mu2_dphi)', ';#Delta#phi(MET_mu2);', 16,0,3.2), # (50,0,3.15) overlay or (16,0,3.2) stack
    })
# if channel == "4l":
#     plot_vars.update({
        
#         'ptmu1_ov_m2mu' : ('ptmu1_ov_m2mu', ';p_T(#mu1) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#         'pt2mu_ov_m2mu' : ('pt2mu_ov_m2mu', ';p_T(#mu#mu) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#     })
# if channel == "MET":
#     plot_vars.update({
#         'met_ov_pt2mu' : ('met_ov_pt2mu', ';MET / p_T(#mu#mu);', 16,0,4.0), # (50,0,1) overlay or (20,0,1) stack
#         'met_ov_m2mu' : ('met_ov_m2mu', ';MET / M(#mu#mu);', 20,0.5,2.5), # (50,0,1) overlay or (20,0,1) stack
        
#         'ptmu1_ov_m2mu' : ('ptmu1_ov_m2mu', ';p_T(#mu1) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#         'pt2mu_ov_m2mu' : ('pt2mu_ov_m2mu', ';p_T(#mu#mu) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#     })
# if channel == "fjmm":
#     plot_vars.update({
#         'ptmu1_ov_m2mu' : ('ptmu1_ov_m2mu', ';p_T(#mu1) / M(#mu#mu);', 12,0,3.0), # (50,0,1) overlay or (20,0,1) stack
#         'pt2mu_ov_m2mu' : ('pt2mu_ov_m2mu', ';p_T(#mu#mu) / M(#mu#mu);', 16,0,4.0), # (50,0,1) overlay or (20,0,1) stack
        
#         'ptfj_ov_pt2mu' : ('ptfj_ov_pt2mu', ';p_T(AK8jet) / p_T(#mu#mu);', 12,0,3.0), # (50,0,1) overlay or (20,0,1) stack
#         'ptfj_ov_m2mu' : ('ptfj_ov_m2mu', ';p_T(AK8jet) / M(#mu#mu);', 12,1.0,4.0), # (50,0,1) overlay or (20,0,1) stack
#         'mfj_ov_m2mu' : ('mfj_ov_m2mu', ';M(AK8jet) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#         'msdfj_ov_m2mu' : ('msdfj_ov_m2mu', ';MSD(AK8jet) / M(#mu#mu);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
        
#         'pnetW_ov_pnetQCD' : ('pnetW_ov_pnetQCD', ';pnet_W(AK8jet) / pnet_QCD(AK8jet);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#         'pnetZ_ov_pnetQCD' : ('pnetZ_ov_pnetQCD', ';pnet_Z(AK8jet) / pnet_QCD(AK8jet);', 20,0,2.0), # (50,0,1) overlay or (20,0,1) stack
#         'pnetW_ov_pnetTWZQCD' : ('pnetW_ov_pnetTWZQCD', ';pnet_W / pnet(T+W+Z+QCD);', 20,0,1.0), # (50,0,1) overlay or (20,0,1) stack
#         'pnetZ_ov_pnetTWZQCD' : ('pnetZ_ov_pnetTWZQCD', ';pnet_Z / pnet(T+W+Z+QCD);', 20,0,1.0), # (50,0,1) overlay or (20,0,1) stack
#     })
#######################################
# Samples, Selections, and Categories #
#######################################

the_samples_dict = get_samples(
    era,
    channel,
    sf_zjb = 1.0,
)

Hmm_win = "(H_mass > 120 && H_mass < 130)"

regions = {
    "{0}_{1}".format(era,channel)                  : '{0}'.format("0 == 0"),
    # "Hmm_win"              : '{0}'.format(Hmm_win),
    # "out_Hmm_win"          : '!{0}'.format(Hmm_win),
}

selections = [
#    'genWeight>-99',
]

the_category_dict = {
    'HHbbmm': [regions, selections, plot_vars],
}

# Blinding the Signal Region
def additional_input_hook(wrps):

    @varial.history.track_history

    def blind_in_HmmWin(w):
        if w.legend == 'Data':
            if 'H_mass' in w.name:
                print('BLINDING Data in %s' % Hmm_win)
                for i in range(3,5): # bin3 for 120, bin5 for 130
                    w.histo.SetBinContent(i, 0.)
                    w.histo.SetBinError(i, 0.)
        return w
        
    wrps = (blind_in_HmmWin(w) for w in wrps)
    return wrps
