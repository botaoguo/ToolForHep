import sys
import ROOT as R
import util


# [usage]:
# - python optimise.py file.root sig_dsid1,2,3 bkg_dsid1,2,3 cut_string criteria var_name min max n_step direction
# - python optimise.py myfile.root 002 202,203,204 "1" "m_2mu,115,135,10;m_2bj,93,137,10" pt2mu_ov_m2mu 0.2 0.8 20 right

# - python optimise.py /data/bond/botaoguo/farm221DNN/0531_version/output_3l.root vhmm dyjets,diboson,top "trg_single_mu24==1&&Flag_dimuon_Zmass_veto==1" "H_mass,110,150,16" dnn_score 0 1 100 right
# ^ test_var: optimise threshold on this variable
# * ranges in criteria will be added as cuts to cut_string
# [algo]:
# calculate signficance (s/sqrt(b) etc.) in bins along variable(s) and squared-sum then up
# - 1D s/sqrt(b) case: calculate significance on 1 variable
#   - build 2D hist x=this variable, y=test_var
#   - simply integrate along y and calculate s/sqrt(b) in bins of x
# - 2D s/sqrt(b) case: calculate significance on 2 variables
#   - use 3D hist accordingly
# direction represent the integral direction, which is left or right

# Licheng: Significance approx.
# Gaussian Proc. Z = \frac{\hat{\mu}S}{\sqrt{B}}
# Poisson Proc. Z = \sqrt{2((\hat{\mu}S + B) \times log(1+\frac{\hat{\mu}S}{B})-\hat{\mu}S)}

### inputs ###
infilenm = sys.argv[1]
sig_dsid = [ istr for istr in sys.argv[2].split(',') ]
bkg_dsid = [ istr for istr in sys.argv[3].split(',') ]
cut_string = sys.argv[4]
test_criteria = sys.argv[5]
test_var = sys.argv[6]
test_min = float(sys.argv[7])
test_max = float(sys.argv[8])
test_nstep = int(sys.argv[9])
inte_direct = sys.argv[10]
### inputs ###

### outputs ###
outputfile = 'opti.root'
### outputs ###

# file and tree
infile = R.TFile(infilenm)
tree = infile.Get('ntuple')

# test criteria
# prepare histograms
_test_criteria = test_criteria.split(';')
test_criteria_ndim = 0
if len(_test_criteria) == 1:
  test_criteria_ndim = 1
elif len(_test_criteria) == 2:
  test_criteria_ndim = 2
else:
  print('test criteria ndim is > 2. not supported atm!')
  exit(1)
test_criteria_hist = None
xvar = None # such as m_2mu
yvar = None # such as m_2bj
if test_criteria_ndim == 1:
  _parse = _test_criteria[0].split(',')
  xvar = _parse[0]
  _nx = int(_parse[3])
  _xmin = float(_parse[1])
  _xmax = float(_parse[2])
  test_cri_hsig = R.TH2F('test_cri_hsig', ';{0};{1};Significance'.format(xvar,test_var), _nx, _xmin, _xmax, test_nstep, test_min, test_max)
  test_cri_hbkg = R.TH2F('test_cri_hbkg', ';{0};{1};Significance'.format(xvar,test_var), _nx, _xmin, _xmax, test_nstep, test_min, test_max)
  # add x range to cut_string
  cut_string = '({0}) && ({1}>{2} && {1}<{3})'.format(cut_string, xvar, _xmin, _xmax)
elif test_criteria_ndim == 2:
  _parsex = _test_criteria[0].split(',')
  _parsey = _test_criteria[1].split(',')
  xvar = _parsex[0]
  _nx = int(_parsex[3])
  _xmin = float(_parsex[1])
  _xmax = float(_parsex[2])
  yvar = _parsey[0]
  _ny = int(_parsey[3])
  _ymin = float(_parsey[1])
  _ymax = float(_parsey[2])
  test_cri_hsig = R.TH3F('test_cri_hsig',';{0};{1};{2};Significance'.format(xvar,yvar,test_var),_nx,_xmin,_xmax,_ny,_ymin,_ymax,test_nstep,test_min,test_max)
  test_cri_hbkg = R.TH3F('test_cri_hbkg',';{0};{1};{2};Significance'.format(xvar,yvar,test_var),_nx,_xmin,_xmax,_ny,_ymin,_ymax,test_nstep,test_min,test_max)
  # add x,y ranges to cut_string
  cut_string = '({0}) && ({1}>{2} && {1}<{3})'.format(cut_string, xvar, _xmin, _xmax)
  cut_string = '({0}) && ({1}>{2} && {1}<{3})'.format(cut_string, yvar, _ymin, _ymax)
else:
  pass

# check inputs
print('input file: {}'.format(infilenm))
print('signal dsid: {0}; background dsid: {1}'.format(sig_dsid,bkg_dsid))
print('preselection: {}'.format(cut_string))
print('optimise the threshold for this variable: {}'.format(test_var))
print('range: [{0},{1}] with {2} steps'.format(test_min, test_max, test_nstep))
print('criteria hist is in {0} dim:'.format(test_criteria_ndim))
print('******************** integral direction is to the {} ********************'.format(inte_direct))
test_cri_hsig.Print("base")

# dsid(s)
# str_sig_dsid = '||'.join([ 'dsid=={0}'.format(_dsid) for _dsid in sig_dsid ])
# str_bkg_dsid = '||'.join([ 'dsid=={0}'.format(_dsid) for _dsid in bkg_dsid ])
str_sig_dsid = '||'.join([ 'is_{0}==1'.format(_dsid) for _dsid in sig_dsid ])
str_bkg_dsid = '||'.join([ 'is_{0}==1'.format(_dsid) for _dsid in bkg_dsid ])

# fill s,b hist
if test_criteria_ndim == 1:
  tree.Draw('abs({1}):{0}>>test_cri_hsig'.format(xvar,test_var),'Train_weight*(({0}) && ({1}))'.format(cut_string,str_sig_dsid),'goff')
  tree.Draw('abs({1}):{0}>>test_cri_hbkg'.format(xvar,test_var),'Train_weight*(({0}) && ({1}))'.format(cut_string,str_bkg_dsid),'goff')
elif test_criteria_ndim == 2:
  tree.Draw('abs({2}):{1}:{0}>>test_cri_hsig'.format(xvar,yvar,test_var),'Train_weight*(({0}) && ({1}))'.format(cut_string,str_sig_dsid),'goff')
  tree.Draw('abs({2}):{1}:{0}>>test_cri_hbkg'.format(xvar,yvar,test_var),'Train_weight*(({0}) && ({1}))'.format(cut_string,str_bkg_dsid),'goff')

# debug
##test_cri_hbkg.Draw('colz')
#test_cri_hbkg.Draw('box2') # 3d
#import time
#time.sleep(10000)

# scan thresholds and integrate hist
n_x = None
n_y = None
n_scan = None
tot_s = 0
tot_b = 0
list_threshold = []
list_sob_binned = []
list_sob_inclu = []
list_eff_sig = []
list_eff_bkg = []
list_sob_eff = []
# 1D binning
if test_criteria_ndim == 1:
  n_x = test_cri_hsig.GetNbinsX()
  n_scan = test_cri_hsig.GetNbinsY()
  tot_s = test_cri_hsig.Integral( 1, n_x, 1, n_scan+1 )
  tot_b = test_cri_hbkg.Integral( 1, n_x, 1, n_scan+1 )
  for ibiny in range(1,n_scan+1):
    _s_sum = 0
    _b_sum = 0
    _sob_inclu = 0
    _sob_binned = 0
    for ibinx in range(1,n_x+1):
      if inte_direct == 'right':
        _s = test_cri_hsig.Integral( ibinx, ibinx, ibiny, n_scan+1 )
        _b = test_cri_hbkg.Integral( ibinx, ibinx, ibiny, n_scan+1 )
      if inte_direct == 'left':
        _s = test_cri_hsig.Integral( ibinx, ibinx, 1, ibiny )
        _b = test_cri_hbkg.Integral( ibinx, ibinx, 1, ibiny )
      _s_sum += _s
      _b_sum += _b
      # print("_s: {}".format(_s))
      # print("_b: {}".format(_b))
      # if _b < 0:
      #   raise RuntimeError("_b < 0")
      _sob_binned += (util.sig_sob(_s,_b))**2
    _sob_binned = _sob_binned**0.5
    _sob_inclu = util.sig_sob(_s_sum,_b_sum)
    if inte_direct == 'right':
      list_threshold.append(test_cri_hsig.GetYaxis().GetBinLowEdge(ibiny))
    if inte_direct == 'left':
      list_threshold.append(test_cri_hsig.GetYaxis().GetBinLowEdge(ibiny+1))
    list_sob_binned.append(_sob_binned)
    list_sob_inclu.append(_sob_inclu)
    list_eff_sig.append(_s_sum/tot_s)
    list_eff_bkg.append(_b_sum/tot_b)
    list_sob_eff.append( util.sig_sob(_s_sum/tot_s,_b_sum/tot_b)  )

# 2D binning
elif test_criteria_ndim == 2:
  n_x = test_cri_hsig.GetNbinsX()
  n_y = test_cri_hsig.GetNbinsY()
  n_scan = test_cri_hsig.GetNbinsZ()
  tot_s = test_cri_hsig.Integral( 1, n_x, 1, n_y, 1, n_scan+1 )
  tot_b = test_cri_hbkg.Integral( 1, n_x, 1, n_y, 1, n_scan+1 )
  for ibinz in range(1,n_scan+1):
    _s_sum = 0
    _b_sum = 0
    _sob_inclu = 0
    _sob_binned = 0
    for ibinx in range(1,n_x+1):
      for ibiny in range(1,n_y+1):
        if inte_direct == 'right':
          _s = test_cri_hsig.Integral( ibinx, ibinx, ibiny, ibiny, ibinz, n_scan+1 )
          _b = test_cri_hbkg.Integral( ibinx, ibinx, ibiny, ibiny, ibinz, n_scan+1 )
        if inte_direct == 'left':
          _s = test_cri_hsig.Integral( ibinx, ibinx, ibiny, ibiny, 1, ibinz )
          _b = test_cri_hbkg.Integral( ibinx, ibinx, ibiny, ibiny, 1, ibinz )
        _s_sum += _s
        _b_sum += _b
        _sob_binned += (util.sig_sob(_s,_b))**2
    _sob_binned = _sob_binned**0.5
    _sob_inclu = util.sig_sob(_s_sum,_b_sum)
    if inte_direct == 'right':
      list_threshold.append(test_cri_hsig.GetZaxis().GetBinLowEdge(ibinz))
    if inte_direct == 'left':
      list_threshold.append(test_cri_hsig.GetZaxis().GetBinLowEdge(ibinz+1))
    list_sob_binned.append(_sob_binned)
    list_sob_inclu.append(_sob_inclu)
    list_eff_sig.append(_s_sum/tot_s)
    list_eff_bkg.append(_b_sum/tot_b)
    list_sob_eff.append( util.sig_sob(_s_sum/tot_s,_b_sum/tot_b)  )

# output
outfile = R.TFile.Open(outputfile, 'RECREATE')
test_cri_hsig.Write()
test_cri_hbkg.Write()
outfile.Close()
print('scan threshold: {}'.format(list_threshold))
print('sob binned: {}'.format(list_sob_binned))
print('sob inclusive: {}'.format(list_sob_inclu))
print('signal efficiency: {}'.format(list_eff_sig))
print('background efficiency: {}'.format(list_eff_bkg))
#print('sob efficiency: {}'.format(list_sob_eff))


sob_inclu_MAX = 0
sob_binned_MAX = 0
for i in list_sob_inclu :
   if i > sob_inclu_MAX :
       sob_inclu_MAX = i
for i in list_sob_binned :
   if i > sob_binned_MAX :
       sob_binned_MAX = i
print('threshold:{0}, inclu_MAX:{1}, sig_eff:{2}, bkg_eff:{3}, sob_eff:{4}'.format(list_threshold[list_sob_inclu.index(sob_inclu_MAX)],sob_inclu_MAX,list_eff_sig[list_sob_inclu.index(sob_inclu_MAX)],list_eff_bkg[list_sob_inclu.index(sob_inclu_MAX)],list_sob_eff[list_sob_inclu.index(sob_inclu_MAX)]))
print('threshold:{0}, binned_MAX:{1}, sig_eff:{2}, bkg_eff:{3}, sob_eff:{4}'.format(list_threshold[list_sob_binned.index(sob_binned_MAX)],sob_binned_MAX,list_eff_sig[list_sob_binned.index(sob_binned_MAX)],list_eff_bkg[list_sob_binned.index(sob_binned_MAX)],list_sob_eff[list_sob_binned.index(sob_binned_MAX)]))
