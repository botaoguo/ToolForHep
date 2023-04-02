import os
import ROOT
import math
import imp
import sys

def truth_filter_bbmm( genparticles ):
    ctrHmm = 0
    ctrHbb = 0
    for particle in genparticles:
        if abs(particle.PID) == 13:   # for HH->bbmm
        #if abs(particle.PID) == 15:   # for HH->bbtautau
        #if abs(particle.PID) == 24:   # for HH->bbWW
            if abs(genparticles[particle.M1].PID) == 25:
                ctrHmm += 1
        elif abs(particle.PID) == 5:
            if abs(genparticles[particle.M1].PID) == 25:
                ctrHbb += 1
                
    if ctrHmm == 2 and ctrHbb == 2:
        return True
    return False

# significane s/sqrt(b)
def sig_sob( s, b ):
    if b == 0:
      return 0
    else:
      return s/math.sqrt(b)

# significance new sob
def newsig_sob( s,b ):
    if b == 0:
      return 0
    else:
      return math.sqrt(2*((s+b)*math.log(1+(s/b))-s))

# dynamic import 
def dynamic_imp(name, class_name):
      
    # find_module() method is used
    # to find the module and return
    # its description and path
    try:
        fp, path, desc = imp.find_module(name)
    except ImportError:
        print ("module not found: " + name)

    # load_modules loads the module 
    # dynamically and takes the filepath
    # module and description as parameter
    try:
        example_package = imp.load_module(name, fp, path, desc)
    except Exception as e:
        print(e)

    #try:
    #    myclass = imp.load_module("% s.% s" % (name,class_name), fp, path, desc)
    #except Exception as e:
    #    print(e)

    return example_package#, myclass
