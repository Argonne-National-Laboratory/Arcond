# Arcond 
A front-end for HTCondor farm with distributted data storage 

ArCond (ARgonne CONDor) is a package to facilitate running multiple jobs in parallel using a PC farm with local data storage, i.e. when data scattered over many PCs. The package was designed for a Tier-3 type of clusters consisting of a number of independent computer notes (PCs) with a local file storage on each node (i.e. disks), and a common NFS-mounted user (or share) directories. No any server computer is necessary.

ArCond is a front-end of the Condor batch system. The main advantage of the ArCond is the possibility to run multiple jobs in parallel using data stored locally on each computing node, rather than using a single file storage on a NFS server (although this is also possible). This means that network is only used during job submission (retrieval), but not during data processing. This leads to a significant performance improvement. ArCond comes with data discovery tools, so it can locate any dataset on local file storage using a static database or build-it on-fly discovery mechanism during job submissions.

Using ArCond, any custom shell command (or a command sequence) defined in a submission script can be executed in parallel. For example, one can run multiple athena option files, perform user-specific tests, file merging etc. directly on the Linux boxes. Also, one can run any custom program defined in a shell script. In addition:

ArCond has a perfect debugging, which allows to check and resubmit jobs for a particular node, or even run failed jobs on the same node where they fail.
Arcond can combine and merge outputs, 
contains tools for administrators which allow to monitor a small cluster via ssh tunneling, 
redistribute data uniformly between different cluster nodes, run any shell command on all cluster nodes, and it is scalable (since network is not used at runtime).  

ArCond program was used at ANL-HEP in 2008-2015 to process terabytes of data 
from the LHC experiments (ATLAS) 
on a daily basis, to generate Monte Carlo models, NLO QCD calculations and more. 
All of this is done using relatively small Tier3 resources.

S.Chekanov (ANL) 
