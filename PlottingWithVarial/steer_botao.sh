# check if there exist Varial
if [ "$1" == "varial" ]; then
    echo "Installing Varial..."
    git clone https://github.com/HeinerTholen/Varial.git
fi

#usage
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.20.08/x86_64-centos7-gcc48-opt/bin/thisroot.sh

if [ $USER == "botaoguo" ]; then
    export PYTHONPATH=$PYTHONPATH:/home/pku/botaoguo/workplace/bbmumu/rootdir/Varial-master
    export PATH=$PATH:/home/pku/botaoguo/workplace/bbmumu/rootdir/Varial-master/bin
else
    export PYTHONPATH=$PYTHONPATH:$PWD/Varial
    export PATH=$PATH:$PWD/Varial/bin
fi

python run_plotting_with_varial.py plot_config_ggF.py

echo "Done!"