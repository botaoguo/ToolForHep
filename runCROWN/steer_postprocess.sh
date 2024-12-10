era=$1
echo "start running $era"

###
nohup python post-processing.py --era ${era} --ch 2l >> ${era}_2l.log 2>&1 &
nohup python post-processing.py --era ${era} --ch 3l >> ${era}_3l.log 2>&1 &
nohup python post-processing.py --era ${era} --ch 4l >> ${era}_4l.log 2>&1 &
nohup python post-processing.py --era ${era} --ch cr_c >> ${era}_cr_c.log 2>&1 &
###
### change path to updated
nohup python post-processing.py --era ${era} --ch cr_fjmm --updated True >> ${era}_cr_fjmm_updated.log 2>&1 &
nohup python post-processing.py --era ${era} --ch cr_bd --updated True >> ${era}_cr_bd_updated.log 2>&1 &

## change update_regionc as True
nohup python post-processing.py --era ${era} --ch cr_c --updated True --updatedC True >> ${era}_cr_c_updated.log 2>&1 &
