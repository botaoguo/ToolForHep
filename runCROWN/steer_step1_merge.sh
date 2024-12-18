era=$1
echo "start merge $era"

nohup python merge.py --era ${era} --type data > ${era}_merge_data.log 2>&1 &
nohup python merge.py --era ${era} --type vhmm > ${era}_merge_vhmm.log 2>&1 &
sleep 60

nohup python merge.py --era ${era} --type top > ${era}_merge_top.log 2>&1 &
nohup python merge.py --era ${era} --type triboson > ${era}_merge_triboson.log 2>&1 &
sleep 60

nohup python merge.py --era ${era} --type dyjets > ${era}_merge_dyjets.log 2>&1 &
sleep 120

nohup python merge.py --era ${era} --type diboson > ${era}_merge_diboson.log 2>&1 &
