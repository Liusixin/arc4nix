import sys
import os
import functools
import uuid
import json
import shlex
from pprint import pprint
from base64 import b64encode
from .sa.wrap_class import Raster
import local_server

me = sys.modules[__name__]

__on_windows__ = sys.platform.find("win") != -1

__all__ = ['add_predefined_statement', 'map_path_var', '__predefined_block__', 'Result', 'Environment', 'Geoprocessor']

__all_functions__ = {
    'analysis': ['Buffer', 'Clip', 'Erase', 'Identity', 'Intersect', 'SymDiff', 'Update', 'Split', 'Near',
                 'PointDistance', 'Select', 'TableSelect', 'Frequency', 'Statistics', 'CreateThiessenPolygons',
                 'SpatialJoin', 'MultipleRingBuffer', 'GenerateNearTable', 'Union', 'TabulateIntersection',
                 'PolygonNeighbors'],
    'management': ['DeleteRows', 'CopyRows', 'CopyFeatures', 'Dissolve', 'MakeFeatureLayer', 'SaveToLayerFile',
                   'AddJoin', 'RemoveJoin', 'Copy', 'Delete', 'Rename', 'CreatePersonalGDB', 'CreateArcInfoWorkspace',
                   'CreateFolder', 'CreateFeatureDataset', 'PivotTable', 'CreateFeatureclass', 'CreateTable',
                   'MakeTableView', 'AddIndex', 'RemoveIndex', 'AddSpatialIndex', 'RemoveSpatialIndex', 'CreateDomain',
                   'DeleteDomain', 'AddCodedValueToDomain', 'DeleteCodedValueFromDomain', 'SetValueForRangeDomain',
                   'AssignDomainToField', 'RemoveDomainFromField', 'TableToDomain', 'DomainToTable', 'SelectData',
                   'AddXY', 'SelectLayerByAttribute', 'SelectLayerByLocation', 'CalculateDefaultGridIndex', 'GetCount',
                   'CreateVersion', 'DeleteVersion', 'RegisterAsVersioned', 'UnregisterAsVersioned', 'AlterVersion',
                   'Analyze', 'CreateRelationshipClass', 'TableToRelationshipClass', 'FeatureToPoint',
                   'FeatureVerticesToPoints', 'FeatureToLine', 'FeatureToPolygon', 'PolygonToLine', 'SplitLine',
                   'DefineProjection', 'Eliminate', 'RepairGeometry', 'CreateTopology', 'AddFeatureClassToTopology',
                   'RemoveFeatureClassFromTopology', 'AddRuleToTopology', 'RemoveRuleFromTopology', 'ValidateTopology',
                   'SetClusterTolerance', 'MakeQueryTable', 'MakeXYEventLayer', 'UpdateAnnotation', 'AppendAnnotation',
                   'MakeRasterLayer', 'Flip', 'Mirror', 'ProjectRaster', 'Rescale', 'Rotate', 'Shift', 'Warp', 'Append',
                   'DeleteFeatures', 'MakeRasterCatalogLayer', 'AddField', 'AssignDefaultToField', 'CalculateField',
                   'DeleteField', 'MultipartToSinglepart', 'Integrate', 'Merge', 'MergeBranch', 'FeatureCompare',
                   'FileCompare', 'RasterCompare', 'TableCompare', 'CreateCustomGeoTransformation', 'CreateFishnet',
                   'CreateFileGDB', 'UpgradeSpatialReference', 'Adjust3DZ', 'Compress', 'CompareReplicaSchema',
                   'CreateReplica', 'CreateReplicaFootPrints', 'CreateReplicaFromServer',
                   'ExportAcknowledgementMessage', 'ExportDataChangeMessage', 'ExportReplicaSchema', 'ImportMessage',
                   'ImportReplicaSchema', 'ReExportUnacknowledgedMessages', 'SynchronizeChanges', 'AddSubtype',
                   'RemoveSubtype', 'SetDefaultSubtype', 'SetSubtypeField', 'CalculateValue', 'CreateRandomPoints',
                   'AddColormap', 'BuildRasterAttributeTable', 'DeleteColormap', 'DeleteRasterAttributeTable',
                   'BuildPyramids', 'CalculateStatistics', 'GetRasterProperties', 'CopyRaster', 'CreateRandomRaster',
                   'CreateRasterDataset', 'Mosaic', 'WorkspaceToRasterDataset', 'CopyRasterCatalogItems',
                   'CreateRasterCatalog', 'DeleteRasterCatalogItems', 'WorkspaceToRasterCatalog',
                   'CreateOrthoCorrectedRasterDataset', 'CreatePansharpenedRasterDataset', 'Clip', 'CompositeBands',
                   'Resample', 'ExportRasterWorldFile', 'GetCellValue', 'RasterCatalogToRasterDataset',
                   'ExtractSubDataset', 'TINCompare', 'MakeImageServerLayer', 'MakeWCSLayer', 'ApplySymbologyFromLayer',
                   'ExportRasterCatalogPaths', 'RepairRasterCatalogPaths', 'MigrateStorage', 'MosaicToNewRaster',
                   'Dice', 'SplitLineAtPoint', 'UnsplitLine', 'SplitRaster', 'EliminatePolygonPart', 'MakeGraph',
                   'SaveGraph', 'PointsToLine', 'ChangeVersion', 'RegisterWithGeodatabase', 'UpgradeGDB',
                   'CalculateDefaultClusterTolerance', 'DeleteIdentical', 'FindIdentical', 'ConsolidateLayer',
                   'ConsolidateMap', 'PackageLayer', 'PackageMap', 'ChangePrivileges', 'CreateSpatialReference',
                   'RasterToDTED', 'BearingDistanceToLine', 'TableToEllipse', 'XYToLine', 'ConvertCoordinateNotation',
                   'CompressFileGeodatabaseData', 'UncompressFileGeodatabaseData', 'ExtractPackage', 'SharePackage',
                   'BuildPyramidsandStatistics', 'MakeMosaicLayer', 'MinimumBoundingGeometry',
                   'AddRastersToMosaicDataset', 'BuildBoundary', 'BuildFootprints', 'BuildOverviews', 'BuildSeamlines',
                   'CalculateCellSizeRanges', 'ColorBalanceMosaicDataset', 'ComputeDirtyArea', 'CreateMosaicDataset',
                   'CreateReferencedMosaicDataset', 'DefineMosaicDatasetNoData', 'DefineOverviews',
                   'GenerateExcludeArea', 'ImportMosaicDatasetGeometry', 'RemoveRastersFromMosaicDataset',
                   'SynchronizeMosaicDataset', 'CalculateEndTime', 'ConvertTimeField', 'ConvertTimeZone',
                   'TransposeFields', 'AddGlobalIDs', 'WarpFromFile', 'ExportXMLWorkspaceDocument',
                   'ImportXMLWorkspaceDocument', 'AlterMosaicDatasetSchema', 'AnalyzeMosaicDataset', 'Compact',
                   'ClearWorkspaceCache', 'AnalyzeDatasets', 'RebuildIndexes', 'CheckGeometry', 'ReconcileVersions',
                   'CreateArcSDEConnectionFile', 'AddEdgeEdgeConnectivityRuleToGeometricNetwork',
                   'AddEdgeJunctionConnectivityRuleToGeometricNetwork', 'CreateGeometricNetwork',
                   'RemoveConnectivityRuleFromGeometricNetwork', 'RemoveEmptyFeatureClassFromGeometricNetwork',
                   'TraceGeometricNetwork', 'AddAttachments', 'DisableAttachments', 'EnableAttachments',
                   'RemoveAttachments', 'ExportTopologyErrors', 'SetMosaicDatasetProperties', 'SetRasterProperties',
                   'MakeLasDatasetLayer', 'DownloadRasters', 'CreateEnterpriseGeodatabase',
                   'EnableEnterpriseGeodatabase', 'FeatureEnvelopeToPolygon', 'MakeQueryLayer', 'SetFlowDirection',
                   'CreateDatabaseConnection', 'DeleteMosaicDataset', 'CreateSpatialType',
                   'GenerateAttachmentMatchTable', 'ConsolidateLocator', 'PackageLocator', 'CreateDatabaseView',
                   'SortCodedValueDomain', 'DisableEditorTracking', 'EnableEditorTracking', 'TruncateTable',
                   'ConsolidateResult', 'PackageResult', 'UpgradeDataset', 'AddFilesToLasDataset', 'CreateLasDataset',
                   'LasDatasetStatistics', 'LasPointStatsAsRaster', 'RemoveFilesFromLasDataset',
                   'ExportMosaicDatasetPaths', 'RepairMosaicDatasetPaths', 'CreateDatabaseUser', 'JoinField',
                   'EditRasterFunction', 'BuildMosaicDatasetItemCache', 'CreateUnRegisteredFeatureclass',
                   'CreateUnRegisteredTable', 'BatchBuildPyramids', 'BatchCalculateStatistics', 'RecoverFileGDB',
                   'Sort', 'CreateMapTilePackage', 'MatchPhotosToRowsByTime', 'GeoTaggedPhotosToPoints',
                   'RegisterRaster', 'AddIncrementingIDField', 'CreateRole', 'ExportTileCache',
                   'GenerateTileCacheTilingScheme', 'ImportTileCache', 'ManageTileCache', 'DisableArchiving',
                   'EnableArchiving', 'MergeMosaicDatasetItems', 'SplitMosaicDatasetItems', 'ComputePansharpenWeights',
                   'DetectFeatureChanges', 'Project', 'BatchProject', 'AddGeometryAttributes',
                   'MigrateRelationshipClass', 'FindDisconnectedFeaturesInGeometricNetwork',
                   'ExportMosaicDatasetGeometry', 'ExportMosaicDatasetItems', 'AlterField', 'CreateRuntimeContent',
                   'RebuildGeometricNetwork', 'VerifyAndRepairGeometricNetworkConnectivity', 'AddFieldConflictFilter',
                   'RemoveFieldConflictFilter', 'CreateVersionedView', 'ReconcileVersion', 'Graph', 'GraphTemplate']
}

# GlobalVars
__path_expr_holder__ = []
# PreBlock
__predefined_block__ = []


class Geoprocessor(object):
    """This is the passthrough gp function."""
    share_state = {}

    def __init__(self):
        self.__dict__ = Geoprocessor.share_state

    def create(self, name, *args):
        if not all([isinstance(a, basestring) for a in args]):
            raise ValueError("arcpy.gp requires all parameter must be string")
        print("arcpy.gp." + create(name, *args))

    def __getattr__(self, name):
        return functools.partial(self.create, name)


class Result:
    """This is a dummy class to keep compatibility with arcpy.Result (GPResult)"""

    # arcpy.Result.__dict__
    # 'cancel', 'getInput', 'getMapImageURL', 'getMessage', 'getMessages', 'getOutput', 'getSeverity', 'inputCount',
    # 'maxSeverity', 'messageCount', 'outputCount', 'resultID', 'saveToFile', 'status'
    def __init__(self, json_string):
        # type: (string) -> object
        r = json.loads(json_string)
        inputs = r['input']
        outputs = r['output']
        messages = r['message']
        status = r['status']
        # Save values to fields
        self.__inputs = inputs
        self.inputCount = len(inputs)
        self.__messages = messages
        self.messageCount = len(messages)
        self.__outputs = outputs
        self.outputCount = len(outputs)
        self.maxSeverity = 0
        self.status = status
        self.resultID = None

    def getMapImageURL(self):
        return ""

    def getSeverity(self, *args, **kwargs):
        return 0

    def cancel(self):
        return 0

    def getInput(self, index):
        if not 0 <= index < self.inputCount:
            raise RuntimeError("Error in get input[%d]" % index)
        return self.__inputs[index]

    def getMessages(self):
        return u"\n".join(self.__messages)

    def getMessage(self, index):
        if not 0 <= index < self.messageCount:
            return u""
        return self.__messages[index]

    def getOutput(self, index):
        if not 0 <= index < self.outputCount:
            raise RuntimeError("Error in get output[%d]" % index)
        return self.__outputs[index]

    def saveToFile(self, *args):
        raise NotImplementedError("Save to file is meaningless in the dummy class")


class Environment(object):
    def __init__(self):
        pass


def add_predefined_statement(statement):
    if isinstance(statement, basestring):
        __predefined_block__.append(statement)


def map_path_var(in_path):
    var_name = "p_" + str(uuid.uuid4()).replace("-", "_")
    # Use base64 encoded value, remove trailing "\n"
    return var_name + "<-path|b64|" + b64encode(in_path), var_name


def parse_string_list(string_list):
    global __path_expr_holder__
    local_var_list = []
    args = string_list.split(";")
    # Remember, each arg may also splitted with space, but with quote enclosed space there. So we need a lexer for it.
    # e.g. '"/a b/s1.shp" 1;"/a b/s2.shp" 2'
    new_args = []
    for arg in args:
        elements = shlex.split(arg)
        new_elements = []
        for e in elements:
            if e.startswith("/"):
                path_expr, path_var = map_path_var(arg)
                local_var_list.append(path_var)
                __path_expr_holder__.append(path_expr)
                new_elements.append("%s")
            else:
                new_elements.append(repr(e))
        new_args.append(" ".join(new_elements))
        del elements, new_elements
    return '\"' + ";".join(new_args) + '\" % (' + ",".join(local_var_list) + ")"


def fix_paths_args(arg, force_repr=__on_windows__):
    global __path_expr_holder__
    if force_repr:
        return repr(arg)
    arg_repr = []
    # if args is list, recursively goes inside
    if isinstance(arg, list):
        sub_arg = map(fix_paths_args, arg)
        arg_repr.append("[%s]" % ",".join(sub_arg))
    elif isinstance(arg, tuple):
        sub_arg = map(fix_paths_args, arg)
        arg_repr.append("(%s)" % ",".join(sub_arg))
    # These are typically paths
    elif isinstance(arg, Raster):
        # TODO: if args is arc4nix.sa.Raster dummpy class, return its path
        arg_repr.append("Raster")
    # A path firstly must be a string
    elif isinstance(arg, basestring):
        is_path = False
        # If arg is a string list. arcpy may present it with ";". But it cannot be a nested list.
        if arg.find(";") != -1:
            arg_repr.append(parse_string_list(arg))
        # TODO: Allow user explicitly add "path:" prefix to say it is a path
        # elif arg.startswith("path:"):
        #    is_path = True
        #    arg = arg[5:]
        # Only absolute path need to be taken care of. Relative path should be fine because we switched to script path
        # before any commands.
        elif arg.startswith("/"):
            path_expr, path_var = map_path_var(arg)
            __path_expr_holder__.append(path_expr)
            arg_repr.append(path_var)
        else:
            arg_repr.append(repr(arg))
    else:
        arg_repr.append(repr(arg))

    return ",".join(arg_repr)


def fix_paths_kwargs(kwarg, force_repr=__on_windows__):
    var, arg = kwarg
    return '%s=%s' % (var, repr(arg) if force_repr else fix_paths_args(arg))


def send_wrap(name, *args, **kwargs):
    global __path_expr_holder__
    global __predefined_block__
    # Before send, we append current working directory here.
    _pwd = os.path.abspath(os.getcwd())
    # We add a predefined block to switch process in Local Server same as script's current dir.
    if __on_windows__:
        __predefined_block__.append('os.chdir(%s)' % repr(_pwd))
    else:
        _pwd_var_value, _pwd_var_name = map_path_var(_pwd)
        __path_expr_holder__.append(_pwd_var_value)
        __predefined_block__.append('os.chdir(%s)' % _pwd_var_name)

    func_sent = "arcpy." + create(name, *args, **kwargs)
    variable_sent = ";".join(__path_expr_holder__)
    preblock_sent = "\n".join(__predefined_block__)

    # FIXME: it is a dangerous assumption, __predefined_block__ is never empty
    command_sent = "execute b64:%s b64:%s b64:%s" % (b64encode(variable_sent), b64encode(preblock_sent), b64encode(func_sent))
    command_sent += os.linesep

    print >> sys.stderr, "GlobalVars=" + variable_sent
    print >> sys.stderr, "PreBlock=" + preblock_sent
    print >> sys.stderr, "ScriptBody=" + func_sent
    print "==================================================="

    local_server.local_server_process.stdin.write(command_sent)
    local_server.local_server_process.stdin.flush()
    # After sending, clean global variables.
    __path_expr_holder__ = []
    __predefined_block__ = []

    # Synchronize result back, block here.
    gp_result_str = local_server.error_queue.get(True)
    if gp_result_str.startswith("[JSON]"):
        try:
            gp_result = Result(gp_result_str[6:])
        except (TypeError, ValueError, IndexError, KeyError, RuntimeError):
            gp_result = json.loads(gp_result_str[6:])
    else:
        raise RuntimeError("Script failed. Please check error log!")


def create(name, *args, **kwargs):
    global __path_expr_holder__
    expr = name + "("
    if args:
        # list args
        new_args = map(fix_paths_args, args)
        expr += ", ".join(new_args)
    if kwargs:
        if args:
            expr += ", "
        # kw args
        new_kwargs = map(fix_paths_kwargs, kwargs.items())
        expr += ", ".join(new_kwargs)
    expr += ")"
    return expr


for cat, func_list in __all_functions__.items():
    for func_stub in func_list:
        func_name = "%s_%s" % (func_stub, cat)
        # We need actually do something tricky.
        setattr(me, func_name, functools.partial(send_wrap, func_name))
        __all__.append(func_name)

del me
