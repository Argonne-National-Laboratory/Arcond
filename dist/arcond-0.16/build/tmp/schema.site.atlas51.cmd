# set universe to run job in local condor queue
universe        =       vanilla

#IO_COMMANDS

WhenToTransferOutput = ON_EXIT_OR_EVICT

executable      = SCRIPT
output          = job.local.out
error           = job.local.err
log             = job.local.log
environment     = RealID=USERNAME;
requirements    = ( machine == "atlas51.hep.anl.gov" )


# below stops the email notification
notification = never
