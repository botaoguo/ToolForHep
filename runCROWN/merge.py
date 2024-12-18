import os
import sys
import ROOT


##### usage #####
# python merge.py $era $anatype $channel
# python merge.py 2022preEE vhmm e2m m2m
#################
# python merge.py $era $anatype
# python merge.py 2022preEE vhmm fjmm_cr
# for all channels
#################


def is_valid_root_file(file_path):
    """
    Check if a ROOT file is valid (not a zombie and contains entries).
    """
    try:
        root_file = ROOT.TFile.Open(file_path)
        if not root_file or root_file.IsZombie():
            print(f"File {file_path} is a zombie or failed to open.")
            return False
        obj = root_file.Get("ntuple")
        if obj and hasattr(obj, "GetEntries") and obj.GetEntries() > 0 and obj.GetNbranches() > 0:
            root_file.Close()
            return True
        print(f"File {file_path} has no valid entries.")
        root_file.Close()
        return False
    except Exception as e:
        print(f"Error while checking file {file_path}: {e}")
        return False


def merge_hadd():
    # check running era
    era = sys.argv[1]
    base_path = '/data/bond/botaoguo/CROWN/sample_database/{}'.format(era)
    ana_type = sys.argv[2]

    if len(sys.argv) >= 4:
        _channels = sys.argv[3:]
        print(_channels)
    else:
        _channels = [
            'e2m', 'm2m', 'eemm', 'mmmm',
            'nnmm', 'fjmm', "fjmm_cr",
            'e2m_dyfakeinge_regionb', 'e2m_dyfakeinge_regionc', 'e2m_dyfakeinge_regiond',
            'm2m_dyfakeingmu_regionb', 'm2m_dyfakeingmu_regionc', 'm2m_dyfakeingmu_regiond'
        ]
        print(_channels)

    for channel in _channels:
        print("*******************************************")
        print(f"Now processing {channel} channel for hadding.")
        channel_dir = find_channel_dir(channel)
        in_alltxt = os.listdir(base_path + '/' + ana_type)

        for in_txt in in_alltxt:
            in_txt = os.path.basename(in_txt)
            in_txt = os.path.splitext(in_txt)[0]
            print(in_txt)

            # Skip if already merged
            output_file = f"input_test_{channel_dir}/{in_txt}_{channel}.root"
            if os.path.isfile(output_file):
                print(f"#############\nNOTICE !!!\n{output_file} exists, skipping.\n#############")
                continue

            # Check if directory exists
            if os.path.exists(f"{in_txt}") and os.path.isdir(f"{in_txt}"):
                os.system(f'mkdir -p input_test_{channel_dir}')
                os.system('mkdir -p mergelog')

                # Collect all valid input files
                input_dir = f"{in_txt}/{channel}/"
                input_files = []
                for root_file in os.listdir(input_dir):
                    file_path = os.path.join(input_dir, root_file)
                    if is_valid_root_file(file_path):
                        input_files.append(file_path)
                    else:
                        print(f"Skipping invalid file: {file_path}")

                if not input_files:
                    print(f"No valid input files for {in_txt} in {channel}. Skipping.")
                    continue

                # Construct hadd command
                input_files_str = " ".join(input_files)
                log_file = f"mergelog/{channel_dir}_{in_txt}_{channel}.log"
                _cmd = f'nohup hadd -f {output_file} {input_files_str} > {log_file} 2>&1 &'
                
                print(_cmd)
                os.system(_cmd)
            else:
                print(f"Directory {in_txt} does not exist, skipping.")


def find_channel_dir(channel):
    _3lepton = ["e2m", "m2m"]
    _4lepton = ["eemm", "mmmm"]
    _2lepton = ["nnmm", "fjmm"]
    _fjmm_cr = ["fjmm_cr"]
    _dyfake_c = ["e2m_dyfakeinge_regionc", "m2m_dyfakeingmu_regionc"]
    _dyfake_bd = ["m2m_dyfakeingmu_regionb", "m2m_dyfakeingmu_regiond",
                  "e2m_dyfakeinge_regionb", "e2m_dyfakeinge_regiond"]
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
