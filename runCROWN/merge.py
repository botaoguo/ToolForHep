import os
import sys
import yaml
import time

##### usage #####
# python merge.py $anatype $channel
# python merge.py vhmm WplusH WminusH ZH
#################
# python merge.py $anatype
# python merge.py vhmm
# for all channels
#################


def merge_hadd():
    base_path='/data/pubfs/botaoguo/CROWN/sample_database/2018'
    ana_type=sys.argv[1]
    # print("len: {}".format(len(sys.argv)))
    if len(sys.argv) >=3:
        _channels = sys.argv[2:]
        print(_channels)
        # exit(0)
    else:
        _channels = ['e2m','m2m','eemm','mmmm','nnmm']
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
            # skip if already merge
            if os.path.isfile("input_test_{2}/{0}_{1}.root".format(in_txt, channel, channel_dir)):
                print("#############")
                print("NOTICE !!!")
                print("{0}_{1}.root exist, skip".format(in_txt, channel))
                print("#############")
                continue
            #
            if os.path.exists("jobs_{}".format(in_txt)) and os.path.isdir("jobs_{}".format(in_txt)):
                os.system('mkdir -p input_test_{}'.format(channel_dir)) 
                os.system('mkdir -p mergelog')
                _cmd = 'nohup hadd -f input_test_{2}/{0}_{1}.root jobs_{0}/*_{1}.root > mergelog/{2}_{0}_{1}.log 2>&1 &'.format(in_txt, channel, channel_dir)
                print(_cmd)
                os.system(_cmd)


def find_channel_dir(channel):
    _3lepton = ["e2m", "m2m"]
    _4lepton = ["eemm", "mmmm"]
    _2lepton = ["nnmm", "jjmm"]
    if channel in _3lepton:
        _dir = '3l'
        return _dir
    elif channel in _4lepton:
        _dir = '4l'
        return _dir
    elif channel in _2lepton:
        _dir = '2l'
        return _dir
    else:
        raise RuntimeError("Unknown channel")

if __name__ == '__main__':
    merge_hadd()
    print("Done!")