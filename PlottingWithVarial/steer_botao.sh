#usage
#1.
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.20.08/x86_64-centos7-gcc48-opt/bin/thisroot.sh
#2. 
export PYTHONPATH=$PYTHONPATH:/home/pku/botaoguo/workplace/bbmumu/rootdir/Varial-master
#3.
export PATH=$PATH:/home/pku/botaoguo/workplace/bbmumu/rootdir/Varial-master/bin
#4.
python run_plotting_with_varial.py plot_config_ggF.py
