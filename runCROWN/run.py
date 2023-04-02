import os
import sys
import yaml
import time

##### usage #####
# Plz run this code at the dir that exist a executable config file, like vhmm_config_vhmm_2018
# if you want to run all of the sample in a anatype 
# python run.py $anatype
# python run.py vhmm
# $anatype can be vhmm, diboson, dyjets, top, triboson, zjjew, data
#################
# if you just want to run some special sample in a anatype
# python run.py $anatype ZZTo4L WZTo3LNu
# python run.py diboson ZZTo4L WZTo3LNu
#################

def run_CROWN():
    # check running on farm or lxplus
    _cores = checkhost()
    #
    if _cores == 40: 
        base_path='/data/pubfs/botaoguo/CROWN/sample_database/2018'
    elif _cores == 5:
        base_path='/afs/cern.ch/user/b/boguo/CROWN/sample_database/2018'
    ana_type=sys.argv[1]
    process_name = None
    # print("len: {}".format(len(sys.argv)))
    if len(sys.argv) >=3:
        process_name = sys.argv[2:] # otherwise process_name = [] is not None
    # in_txt=sys.argv[2]
    # in_alltxt=sys.argv[2:]
    in_alltxt = os.listdir(base_path + '/' + ana_type)
    # print(in_alltxt)
    # exit(0)
    # print("process_name : {}".format(process_name))
    # exit(0)
    for in_txt in in_alltxt:
        in_txt=os.path.basename(in_txt)
        in_txt=os.path.splitext(in_txt)[0]
        #
        needRun = False
        if process_name is not None:
            print("DEBUG")
            # loop if there exist process want to run
            for item in process_name:
                if item in in_txt:
                    print("Need run {}".format(in_txt))
                    needRun = True
                    break
        # if (needRun is True) or (process_name is None):
        #     pass
        # else:
        if (needRun is not True) and (process_name is not None):
            print("No need to run {}".format(in_txt))
            continue
        # print(in_txt)
        # exit(0)
        idx = 0
        with open("{0}/{1}/{2}.yaml".format(base_path,ana_type,in_txt), "r") as f:
            print("***********************{}.yaml File Head!!!!!**************************************".format(in_txt))
            for line in f:
                if '.root' not in line:
                    continue
                # Remove the newline character at the end of the line
                line = line.strip().strip("- ")
                # Concatenate the line with a semicolon to run it as a single command
                cmd = "nohup ./vhmm_config_{}_2018".format(ana_type) + " " \
                    + "jobs_{}/".format(in_txt) + in_txt + "_{0:03d}.root".format(idx) + " " + line \
                    + " " + "> jobs_{}/".format(in_txt) + "nohup_{0}_{1:03d}.log 2>&1 &".format(in_txt,idx)
                # if idx < 1:
                #     exit()
                # if ((idx>=120 and idx<=999) or idx in idx_list):
                # if idx in idx_list:
                #     print(cmd)
                #     print("running {0:03d} job now.........................................".format(idx))
                #     # Run the command using os.system()
                #     os.system(cmd)
                if idx==0:
                    if os.path.exists("jobs_{}".format(in_txt)) and os.path.isdir("jobs_{}".format(in_txt)):
                        print("jobs_{}/ exist.".format(in_txt))
                    else:
                        os.system("mkdir jobs_{}".format(in_txt))
                ####
                # if (idx % 40 == 0) and (idx!=0):
                #     os.system('sleep 60')
                while checkrunning() >= _cores:
                    print("Many jobs are running now, plz wait 1 min......")
                    os.system('sleep 60')
                # Run the command using os.system()
                if checkjob("jobs_{}".format(in_txt) + "/" + "nohup_{0}_{1:03d}.log".format(in_txt,idx)):
                    pass
                    # print("jobs {0}_{1:03d} done successfully".format(in_txt, idx))
                else:
                    print(cmd)
                    print("running {0:03d} job now......................................................".format(idx))
                    os.system(cmd)
                idx += 1

def checkhost():
    os.system("echo $HOSTNAME > host.log")
    with open("host.log", "r") as f:
        _host = f.readlines()[0].strip('\n')
        if 'pku' in _host:
            print("PKU Running")
            cores = 40
            return cores
        elif 'cern' in _host:
            print("LXPLUS Running")
            cores = 5
            return cores
        else:
            raise RuntimeError("Can only support PKU and LXPLUS")

def checkjob(input_log):
    # print(input_log)
    # exit(0)
    # filelog = os.listdir(input_path)
    # print(filelog)
    # exit(0)
    if os.path.isfile(input_log):
        if '.log' in input_log:
            with open(input_log) as f:
                lines = f.readlines()
                try:
                    last_line = lines[-1].strip()
                    if 'Overall runtime' in last_line:
                        return True
                    else:
                        return False
                except:
                    return False
    else:
        return False

def checkrunning():
    _cmd = 'top -n 1 -u $USER | grep config | wc -l > count.log'
    os.system(_cmd)
    running_count_file = open('count.log')
    running_count = int(running_count_file.readlines()[0].strip('\n'))
    # print("{} jobs are running now".format(running_count))
    return running_count

if __name__ == '__main__':
    start_time = time.time()
    run_CROWN()
    end_time = time.time()
    running_time = end_time - start_time
    print("Running time: {:.2f} seconds".format(running_time))