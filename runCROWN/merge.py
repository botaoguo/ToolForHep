import os
import sys
import yaml
import time

##### usage #####
# python merge.py $era $anatype $channel
# python merge.py 2022preEE vhmm e2m m2m
#################
# python merge.py $era $anatype
# python merge.py 2022preEE vhmm fjmm_cr
# for all channels
#################


def merge_hadd():
    # check running era
    era = sys.argv[1]
    base_path='/data/bond/botaoguo/CROWN/sample_database/{}'.format(era)
    ana_type=sys.argv[2]
    # print("len: {}".format(len(sys.argv)))
    if len(sys.argv) >=4:
        _channels = sys.argv[3:]
        print(_channels)
        # exit(0)
    else:
        _channels = [
                     'e2m','m2m','eemm','mmmm',
                     'nnmm','fjmm',"fjmm_cr",
                     'e2m_dyfakeinge_regionb','e2m_dyfakeinge_regionc','e2m_dyfakeinge_regiond',
                     'm2m_dyfakeingmu_regionb','m2m_dyfakeingmu_regionc','m2m_dyfakeingmu_regiond'
                    ]
        print(_channels)
        # exit(0)

    for channel in _channels:
        print("*******************************************")
        print("Now is {} channel hadding".format(channel))
        #
        channel_dir = find_channel_dir(channel)
        #
        in_alltxt = os.listdir(base_path + '/' + ana_type)
        for in_txt in in_alltxt:
            in_txt=os.path.basename(in_txt)
            in_txt=os.path.splitext(in_txt)[0]
            print(in_txt)
            # skip if already merge
            if os.path.isfile("input_test_{2}/{0}_{1}.root".format(in_txt, channel, channel_dir)):
                print("#############")
                print("NOTICE !!!")
                print("{0}_{1}.root exist, skip".format(in_txt, channel))
                print("#############")
                continue
            #
            if os.path.exists("{}".format(in_txt)) and os.path.isdir("{}".format(in_txt)):
                os.system('mkdir -p input_test_{}'.format(channel_dir)) 
                os.system('mkdir -p mergelog')
                if in_txt == "DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8_Run3Summer22EENanoAODv12-130X":
                    _cmd = 'nohup hadd -f input_test_{2}/{0}_{1}.root {0}*/{1}/{0}_*.root > mergelog/{2}_{0}_{1}.log 2>&1 &'.format(in_txt, channel, channel_dir)
                elif in_txt == "DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8_Run3Summer22EENanoAODv12-130X_ext1":
                    print("************************")
                    print("************************")
                    print("************************")
                    print("DY ext merged with normal sample already")
                    print("************************")
                    print("************************")
                    print("************************")
                    continue
                elif in_txt == "DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8_Run3Summer22NanoAODv12-130X":
                    _cmd = 'nohup hadd -f input_test_{2}/{0}_{1}.root {0}*/{1}/{0}_*.root > mergelog/{2}_{0}_{1}.log 2>&1 &'.format(in_txt, channel, channel_dir)
                elif in_txt == "DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8_Run3Summer22NanoAODv12-130X_ext1":
                    print("************************")
                    print("************************")
                    print("************************")
                    print("DY ext merged with normal sample already")
                    print("************************")
                    print("************************")
                    print("************************")
                    continue
                else:
                    _cmd = 'nohup hadd -f input_test_{2}/{0}_{1}.root {0}/{1}/{0}_*.root > mergelog/{2}_{0}_{1}.log 2>&1 &'.format(in_txt, channel, channel_dir)
                print(_cmd)
                # os.system(_cmd)


def find_channel_dir(channel):
    _3lepton = ["e2m", "m2m"]
    _4lepton = ["eemm", "mmmm"]
    _2lepton = ["nnmm", "fjmm"]
    _fjmm_cr = ["fjmm_cr"]
    _dyfake_c = ["e2m_dyfakeinge_regionc","m2m_dyfakeingmu_regionc"]
    _dyfake_bd = ["m2m_dyfakeingmu_regionb","m2m_dyfakeingmu_regiond",
               "e2m_dyfakeinge_regionb","e2m_dyfakeinge_regiond"]
    if channel in _3lepton:
        _dir = '3l'
        return _dir
    elif channel in _4lepton:
        _dir = '4l'
        return _dir
    elif channel in _2lepton:
        _dir = '2l'
        return _dir
    elif channel in _dyfake_c:
        _dir = 'cr_c'
        return _dir
    elif channel in _dyfake_bd:
        _dir = 'cr_bd'
        return _dir
    elif channel in _fjmm_cr:
        _dir = 'cr_fjmm'
        return _dir
    else:
        raise RuntimeError("Unknown channel")

if __name__ == '__main__':
    merge_hadd()
    print("Done!")