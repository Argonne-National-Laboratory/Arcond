# ArCond configuration file
# S.Chekanov (ANL)

####### admins, please correct:

# location of ArCondDB
ArcDBaseDIR='/users/condor/ArcondDB/'

# you should modify this for XROOTD.
# If you do not use XROOTD, just set it to an empty string
# REDIRECTOR_NAME="root://ascvmxrdr.hep.anl.gov/"

## if you do not use xrootd (why you would?), as in the case of ANL cluster
REDIRECTOR_NAME=""


## path to ROOTSYS env variables (necessary for file merging only)
## arcROOTSYS="/export/share/atlas/ATLASLocalRootBase/x86_64/root/current/"
arcROOTSYS="/share/cern/root/"
 

##### do not modify anything below #######
ARC_VERSION="1.6"



#################################
import os,sys
from arcondtools.TerminalController import TerminalController,ProgressBar
from math import sqrt,acos,exp
from array import array
from arcondtools.Conf import *
from arcondtools.duplicates import *
from arcondtools.checknodes import *
from arcondtools.checkstatus import *
from arcondtools.checkversion import *
from arcondtools.collect_db   import *
from arcondtools.arcutils     import *
from arcondtools.getcentral   import *
from arcondtools.nrcores      import *
