import json
import functools

from .wrap_base import create as basecreate


class Geoprocessor(object):
    """This is the passthrough gp function."""
    share_state = {}

    def __init__(self):
        self.__dict__ = Geoprocessor.share_state

    def create(self, name, *args):
        if not all([isinstance(a, basestring) for a in args]):
            raise ValueError("arcpy.gp requires all parameter must be string")
        print("arcpy.gp." + basecreate(name, *args))

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
