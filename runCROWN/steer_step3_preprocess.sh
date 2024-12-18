era=$1
echo "start running $era"

### change path to updated
nohup python post-processing.py --era ${era} --ch cr_fjmm >> ${era}_cr_fjmm.log 2>&1 &
nohup python post-processing.py --era ${era} --ch cr_bd >> ${era}_cr_bd.log 2>&1 &
