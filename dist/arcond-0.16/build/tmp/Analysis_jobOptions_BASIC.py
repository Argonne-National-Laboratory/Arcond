# example for ArCond created by S.Chekanov (ANL)

# Author: Ketevi A. Assamagan
# BNL, June 12, 2004

# get a handle on the ServiceManager which holds all the services
from AthenaCommon.AppMgr import ToolSvc

from AthenaCommon.AppMgr import ServiceMgr
# Event selector
import AthenaPoolCnvSvc.ReadAthenaPool
#EventSelector.BackNavigation = True

# Particle Properties
from PartPropSvc.PartPropSvcConf import PartPropSvc

# the POOL converters
include( "ParticleBuilderOptions/ESD_PoolCnv_jobOptions.py" )
include( "ParticleBuilderOptions/AOD_PoolCnv_jobOptions.py")
include( "ParticleBuilderOptions/McAOD_PoolCnv_jobOptions.py")
include( "EventAthenaPool/EventAthenaPool_joboptions.py" )

# The AOD input file
#ServiceMgr.EventSelector.InputCollections = [ "dcache:AOD.pool.root.1" ]
# ServiceMgr.EventSelector.InputCollections = [ "AOD.pool.root" ]
# getting the data files here using DQ2.  The list of input files

# this part for ArCond
include("InputCollection.py")
# get data
ServiceMgr.EventSelector.InputCollections = dataCollection



# Get the selection, overlap checking and overlap removal tools  
include ( "UserAnalysisUtils/UserAnalysisSelectionTool_jobOptions.py" )
include ( "UserAnalysisUtils/UserAnalysisPreparationTool_jobOptions.py" )
include ( "UserAnalysisUtils/UserAnalysisOverlapCheckingTool_jobOptions.py" )
include ( "UserAnalysisUtils/UserAnalysisOverlapRemovalTool_jobOptions.py" )

# Athena-Aware NTuple making Tools
CBNTAthenaAware = True
include ("CBNT_Athena/CBNT_AthenaAware_jobOptions.py")
# uncomment for more info
# include ("CBNT_Athena/CBNT_EventInfo_jobOptions.py")

# list of the algorithms to be executed at run time
from UserAnalysis.UserAnalysisConf import AnalysisSkeleton
topSequence.CBNT_AthenaAware += AnalysisSkeleton() 
AnalysisSkeleton = AnalysisSkeleton()

############# The properties of the AnalysisSkeleton Algorithm
AnalysisSkeleton.AnalysisSelectionTool       = ToolSvc.UserAnalysisSelectionTool
AnalysisSkeleton.AnalysisPreparationTool     = ToolSvc.UserAnalysisPreparationTool
AnalysisSkeleton.AnalysisOverlapCheckingTool = ToolSvc.UserAnalysisOverlapCheckingTool
AnalysisSkeleton.AnalysisOverlapRemovalTool  = ToolSvc.UserAnalysisOverlapRemovalTool

IsAtlfast = False

AnalysisSkeleton.McParticleContainer = "SpclMC"
AnalysisSkeleton.ElectronContainer = "ElectronAODCollection"
AnalysisSkeleton.MissingETObject = "MET_RefFinal"
AnalysisSkeleton.DeltaRMatchCut = 0.2
AnalysisSkeleton.MaxDeltaR = 0.9999
AnalysisSkeleton.ElectronEtCut  = 10.0*GeV
AnalysisSkeleton.ElectronEtaCut = 2.5
AnalysisSkeleton.ElectronCone   = 0.9
AnalysisSkeleton.bjetWt_IP3DSV1Cut = 6
AnalysisSkeleton.bjet_etaCut = 2.5
AnalysisSkeleton.bjet_etCut = 15.0*GeV
AnalysisSkeleton.MissingETCut = 20.0*GeV
AnalysisSkeleton.OutputLevel = INFO
AnalysisSkeleton.IsAtlFastData = IsAtlfast
AnalysisSkeleton.SusyJetMinEt      = 50*GeV

# Change the selections if necesary
# VJ: Feb 28, 2008:
# At the moment, we cannot seem to propagate new settings back to
# the various tools. So, you will have to edit the jO files in
# UserAnalysisUtils/ package
#
ToolSvc.UserAnalysisSelectionTool.IsAtlfastData = IsAtlfast
#AnalysisSkeleton.AnalysisSelectionTool.ElectronIsEMFlag="Loose"
ToolSvc.UserAnalysisSelectionTool.MuonPt=6.0*GeV
ToolSvc.UserAnalysisSelectionTool.JetPt=20.0*GeV

# configure the overlap checking tool
ToolSvc.UserAnalysisOverlapCheckingTool.OverlapDeltaR=0.2
ToolSvc.UserAnalysisOverlapCheckingTool.OverlapDeltaRWithJets=0.3

# Building the  containers of selected obejcts
ToolSvc.UserAnalysisPreparationTool.IsAtlfastData = IsAtlfast

#input cntainer keys to the pre-selection tool
ToolSvc.UserAnalysisPreparationTool.InputContainerKeys = [
    "ElectronAODCollection",
    "StacoMuonCollection",
    "TauRecContainer",
    "Cone4H1TopoJets",
    "PhotonAODCollection",
    "CaloCalTopoCluster",
    "TrackParticleCandidate"
   ]
# Output container keys after the pre-selections
ToolSvc.UserAnalysisPreparationTool.OutputContainerKeys=[ 
    "SelectedElectronCollection",
    "SelectedStacoMuonCollection",
    "SelectedTauRecContainer",
    "SelectedCone4H1TowerJets",
    "SelectedPhotonAODCollection",
    "SelectedCaloCalTopoCluster",
    "SelectedTrackParticleCandidate"
   ]

# Use the output containers fromi the selection tool as input to the overalp removal tool
ToolSvc.UserAnalysisOverlapRemovalTool.InputContainerKeys=[  
    "SelectedElectronCollection",
    "SelectedStacoMuonCollection",
    "SelectedTauRecContainer",
    "SelectedCone4H1TowerJets",
    "SelectedPhotonAODCollection",
    "SelectedCaloCalTopoCluster",
    "SelectedTrackParticleCandidate"
   ]

# The output container keys after the overlap-removal
# Note that a container of all leptons is provided on output
# as well as a container of all final state particles
AnalysisSkeleton.AnalysisOverlapRemovalTool.IsAtlfastData          = IsAtlfast
AnalysisSkeleton.AnalysisOverlapRemovalTool.OuputObjectKey         = "FinalStateObjectCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputLeptonKey        = "FinalStateLeptonCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputPhotonKey        = "FinalStatePhotonCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputElectronKey      = "FinalStateElectronCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputMuonKey          = "FinalStateMuonCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputTauJetKey        = "FinalStateTauJetCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputCalloClusterKey  = "FinalStateCaloClusterCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputTrackParticleKey = "FinalStateTrackParticleCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputJetKey           = "FinalStateJetCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputBJetKey          = "FinalStateBJetCollection"
AnalysisSkeleton.AnalysisOverlapRemovalTool.OutputLightJetKey      = "FinalStateLightJetCollection"

##
##########################################
## Set up trigger configuration service and metadata service is relies on, for analysis job without RecExCommon

AnalysisSkeleton.DoTrigger = False

if AnalysisSkeleton.DoTrigger:
   from AthenaCommon.GlobalFlags import GlobalFlags
   GlobalFlags.DetGeo.set_atlas()

   ## set up trigger decision tool
   from TrigDecision.TrigDecisionConfig import TrigDecisionTool
   tdt = TrigDecisionTool()
   ToolSvc += tdt

   # might be needed for TriggerConfigGetter...
   from RecExConfig.RecFlags  import rec
   rec.readAOD=True
   rec.doWriteAOD=False
   rec.doWriteESD=False

   # To read files with trigger config stored as in-file meta-data,
   # i.e. 13.0.40 and above: ds
   # To read AOD produced with 13.0.30 you need to change ds to aod: 
   from TriggerJobOpts.TriggerFlags import TriggerFlags
   TriggerFlags.configurationSourceList = ['ds']

   # set up trigger config service
   from TriggerJobOpts.TriggerConfigGetter import TriggerConfigGetter
   cfg =  TriggerConfigGetter()

## END of trigger setup

##########################################
# setup TTree registration Service
# save ROOT histograms and Tuple
from GaudiSvc.GaudiSvcConf import THistSvc
ServiceMgr += THistSvc()
ServiceMgr.THistSvc.Output = [ "AANT DATAFILE='Analysis.root' OPT='RECREATE'" ]
from AnalysisTools.AnalysisToolsConf import AANTupleStream
topSequence += AANTupleStream()
AANTupleStream = AANTupleStream()
AANTupleStream.ExtraRefNames = [ "" ]
AANTupleStream.OutputName = 'Analysis.root'
AANTupleStream.WriteInputDataHeader = True
AANTupleStream.OutputLevel = WARNING

# Set output level threshold (2=DEBUG, 3=INFO, 4=WARNING, 5=ERROR, 6=FATAL )
ServiceMgr.MessageSvc.OutputLevel = INFO

# Number of Events to process
# theApp.EvtMax = -1

###################### For interactive analysis
#include ("PyAnalysisCore/InitPyAnalysisCore.py")

from GaudiSvc.GaudiSvcConf import AuditorSvc
ServiceMgr.AuditorSvc.Auditors  += [ "ChronoAuditor"]

AthenaPoolCnvSvc = Service("AthenaPoolCnvSvc")
AthenaPoolCnvSvc.UseDetailChronoStat = TRUE

#### test MC dump ###

#theApp.Dlls  += ["TruthExamples" ]
#theApp.TopAlg = ["PrintMC"]
##-- PrintMC
#PrintMC = Algorithm( "PrintMC" )
##event SVC key
#PrintMC.McEventKey = "GEN_AOD"
## do you want output at all? TRUE/FALSE
#PrintMC.VerboseOutput = TRUE
## Event print style Vertex(traditional)/Barcode(barcode ordered)
#PrintMC.PrintStyle = "Barcode"
