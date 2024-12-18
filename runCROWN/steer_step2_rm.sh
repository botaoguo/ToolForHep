# remove the DY inclu in input_test_2l and input_test_cr_fjmm
echo "remove the DY inclu in input_test_2l and input_test_cr_fjmm"
rm input_test_2l/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV* input_test_cr_fjmm/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV*
rm input_test_2l/DYto2L-2Jets_MLL-50_[012]J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8*/
rm input_test_cr_fjmm/DYto2L-2Jets_MLL-50_[012]J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8*/

# remove all the DY in input_test_3l and input_test_4l
echo "remove all the DY in input_test_3l and input_test_4l"
rm input_test_[34]l/DYto2L*

# remove the PTLL slice DY in input_test_cr_bd and input_test_cr_c
echo "remove the PTLL slice DY in input_test_cr_bd and input_test_cr_c"
rm input_test_cr_[bc]*/DYto2L-2Jets_MLL-50_PTLL*

# remove all the signal in cr
echo "remove all the signal in cr"
rm input_test_cr_*/*Hto2Mu*
