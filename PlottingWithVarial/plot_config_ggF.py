from samples_HHbbmm import *
import varial
import ROOT as R
# import wrappers

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

name = '3l_test-0329_001'

weight = 'Train_weight'

plot_vars = {
    # WH3l 
    'dimuon_p4_Higgs.fCoordinates.fPt' : ('dimuon_p4_Higgs.fCoordinates.fPt', ';p_{T}^{H} [GeV];', 60,0,600),
    'abs(muon_leadingp4_H.fCoordinates.fEta)' : ('abs(muon_leadingp4_H.fCoordinates.fEta)', ';#eta_{#mu1};', 60,0,2.4),
    'abs(muon_subleadingp4_H.fCoordinates.fEta)' : ('abs(muon_subleadingp4_H.fCoordinates.fEta)', ';#eta_{#mu2};', 60,0,2.4),
    'mumuH_dR' : ('mumuH_dR', ';#Delta R(#mu#mu) [m];', 50,0,4.5),

    'extra_lep_p4.fCoordinates.fPt' : ('extra_lep_p4.fCoordinates.fPt', ';p_{T}^{lep} [GeV];', 50,20,320),
    'nelectrons' : ('nelectrons', ';nEles;', 2,0,2),
    'lep_H_dR' : ('lep_H_dR', ';#Delta R(lep_H) [m];', 50,0,8),
    'lep_H_deta' : ('lep_H_deta', ';#Delta#eta(lep_H);', 60,0,6),

    # lep_muSS_cosThStar -> done
    'lep_muSS_deta' : ('lep_muSS_deta', ';#Delta#eta(lep_#mu_{SS});', 50,0,5),
    'lep_muSS_cosThStar' : ('lep_muSS_cosThStar', ';cos(#theta_{lep_#mu_{SS}});', 50,-1,1),
    'lep_muOS_dR' : ('lep_muOS_dR', ';#Delta R(lep_#mu_{OS}) [m];', 60,0,6),
    'lep_muOS_deta' : ('lep_muOS_deta', ';#Delta#eta(lep_#mu_{OS});', 50,0,5),

    # lep_muOS_cosThStar -> done
    'lep_muOS_cosThStar' : ('lep_muOS_cosThStar', ';cos(#theta_{lep_#mu_{OS}});', 50,-1,1),
    'mt_muSSAndMHT' : ('mt_muSSAndMHT', ';mt(#mu_{SS}_MHT) [GeV];', 60,0,600),
    'mt_lepWAndMHT' : ('mt_lepWAndMHT', ';mt(lep_MHT) [GeV];', 60,0,300),
    'lep_MHT_dphi' : ('lep_MHT_dphi', ';#Delta#phi_{lep}^{MHT};', 50,0,3.15),
    
    # ZH4l
    # need leptonID and ZH_cosThStar -> done
    # 'dimuon_p4_Higgs.fCoordinates.fPt' : ('dimuon_p4_Higgs.fCoordinates.fPt', ';p_{T}^{H} [GeV];', 60,0,600),
    # 'dimuon_p4_Higgs.fCoordinates.fEta' : ('dimuon_p4_Higgs.fCoordinates.fEta', ';#eta_{H};', 50,0,7),
    # 'dilepton_p4_Z.fCoordinates.fPt' : ('dilepton_p4_Z.fCoordinates.fPt', ';p_{T}^{Z} [GeV];', 60,0,600),
    # 'mumuH_dphi' : ('mumuH_dphi', ';#Delta#phi(#mu#mu);', 50,0,3.15),   
    # 'dilepton_p4_Z.fCoordinates.fM' : ('dilepton_p4_Z.fCoordinates.fM', ';Mass(Z) [GeV];', 50,81,101),
    # 'dilepton_p4_Z.fCoordinates.fEta' : ('dilepton_p4_Z.fCoordinates.fEta', ';#eta_{Z};', 50,0,7),
    # 'llZ_dR' : ('llZ_dR', ';#Delta R(ll) [m];', 50,0,5),
    # 'Z_H_deta' : ('Z_H_deta', ';#Delta#eta(ZH);', 60,0,9),
    # 'Zlep_ID' : ('Zlep_ID', ';Zlep ID;', 3,11,14),
    # 'Z_H_cosThStar' : ('Z_H_cosThStar', ';cos(#Theta_{Z_H});', 50,-1,1),
    
    # M(mm)
    'dimuon_p4_Higgs.fCoordinates.fM' : ('dimuon_p4_Higgs.fCoordinates.fM', ';Mass(#mu#mu) [GeV];', 8,110,150),

}

# from Muon
plot_vars.update({
#     'mt_1'       :    ('mt_1',       ';mt_1 [GeV];', 28,0,140),
#     'mu0_pt'           :           ('mu0_pt',             ';p_{T}_Mu1 [GeV];',  25,     0,      600),
#     'm_2mu'           :            ('m_2mu',              ';Mass_H(mm) [GeV];', 25,     50,     200),
})

#######################################
# Samples, Selections, and Categories #
#######################################

the_samples_dict = get_samples(
    channel='ggF',
    
    signal_overlay=True,
    
    sf_zjb = 1.0,
)

Hmm_win = "(lep_MHT_dphi>=3)"

regions = {
    "ALL"                  : '{0}'.format("0 == 0"),
#    "Hmm_win"              : '{0}'.format(Hmm_win),
#     "out_Hmm_win"          : '!{0}'.format(Hmm_win),
}

selections = [
#    'genWeight>-99',
#    'weight>-99','weight>-199',
]

the_category_dict = {
    'HHbbmm': [regions, selections, plot_vars],
}

# Blinding the Signal Region
def additional_input_hook(wrps):

    @varial.history.track_history

    def blind_in_HmmWin(w):
        if w.legend == 'Data' and w.in_file_path.startswith('Hmm_win'):
            if 'pt' or 'mu' in w.name:
                print('BLINDING Data in %s' % w.in_file_path)
                for i in xrange(w.histo.GetNbinsX() + 1):
                    w.histo.SetBinContent(i, 0.)
                    w.histo.SetBinError(i, 0.)
        return w
        
    wrps = (blind_in_HmmWin(w) for w in wrps)
    return wrps
