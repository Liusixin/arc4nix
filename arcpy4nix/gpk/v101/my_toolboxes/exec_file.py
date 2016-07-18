# coding=utf-8
"""This is the general module that allow ArcGIS Runtime to execute an arbitrary script.
In this case we just need the script be executed. We don't care its results.
So we call it "execute a script"
To keep everything simple, we must put all things in one, single, big file.
"""

import subprocess
import StringIO
import gzip
import json
# By any menas, we first import. This is a workaround to prevent ArcGIS Desktop detect imports when creating the gpk
# DO NOT USE ```import arcpy```
arc = __import__("arcpy")


def dump_gpresult(gpresult):
    """
    :param gpresult: arcpy.Result, an object representing geoprocessing result.
    :return: str, a JSON-dumped string.
    """
    assert type(gpresult) is arc.Result
    # Collect outputs, inputs, messages and status
    status = gpresult.status
    messages = [gpresult.getMessage(i) for i in range(gpresult.messageCount)]
    inputs = [gpresult.getInput(i) for i in range(gpresult.inputCount)]
    outputs = [gpresult.getOutput(i) for i in range(gpresult.outputCount)]

    return json.dumps({
        'status': status,
        'message': messages,
        'input': inputs,
        'output': outputs
    }, ensure_ascii=True)


def detect_wine():
    on_wine = True
    try:
        subprocess.check_call(["winepath"])
    except WindowsError:
        # If we are not in wine, we should not have winepath command.
        on_wine = False
    return on_wine


def decode_global_vars(global_variables):
    """
    :param global_variables: str the
    :return a dictionary of global variables and their values could be fed to the script body
    :rtype dict
    """
    var_list = global_variables.split(';')
    var_dict = {}
    for var_str in var_list:
        var_name, var_value_tuple = var_str.split('<-')
        ispath, encode, var_value_encoded = var_value_tuple.split('|')
        if encode.find('b64') != -1:
            var_value_encoded = var_value_encoded.decode('base64').replace('\n', '')
        if encode.find('zlib') != -1:
            r = StringIO.StringIO(var_value_encoded)
            s = gzip.GzipFile(fileobj=r)
            var_value_encoded = s.read()
        var_value = var_value_encoded.replace('\n', '')
        # On Linux, we need convert linux path to wine path to call it.
        # However, we have no way to determine if we are under wine because python-wine will tell it is one windows.
        # So we need a custom check.
        on_wine = detect_wine()
        if ispath.lower() == 'path' and on_wine:
            try:
                proc = subprocess.Popen(["winepath", "-w", var_value], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, err = proc.communicate()
                status = proc.returncode
                arc.AddMessage(output)
                if status == 0:
                    var_value = output
                    arc.AddMessage('the decoded path points -> %s' % var_value)
                else:
                    arc.AddWarning(output)
                    arc.AddWarning(err)
            except OSError, ex:
                arc.AddWarning(str(ex))
        var_dict[var_name] = eval(var_value)
    return var_dict


def execute_file():
    global_vars = arc.GetParameterAsText(0)
    predefined_block = arc.GetParameterAsText(1)
    script_body = arc.GetParameterAsText(2)

    for k, v in decode_global_vars(global_vars).iteritems():
        arc.AddMessage("Add %s=%s to global variables" % (k, v))
        globals()[k] = v

    # This is the default settings.
    arc.env.overwriteOutput = True
    arc.env.workspace = "in_memory"
    arc.AddMessage(__name__)

    exec predefined_block.decode('string_escape') in globals()

    # Check if script body can be evaluated, if not, execute it.
    try:
        script_ast = compile(script_body.decode('string_escape'), "<string>", "eval")
        result = eval(script_ast, globals())
        arc.AddMessage(str(result))

        if type(result) is arc.Result:
            # TODO: we have a GPResult, Let's wrap its result.
            result_string = json.dumps(result.__dict__)
        else:
            # We try to dump it as a json string. If no possible, just get the basic string
            try:
                result_string = json.dumps(result)
            except TypeError:
                result_string = str(result)
        # Put string result back to Geoprocessor
        arc.SetParameter(3, result_string)
    except SyntaxError:
        # Otherwise we simply execute the command, if everything is "OK" we return "true", otherwise "false"
        try:
            exec script_body in globals()
            arc.SetParameter(3, "true")
        except Exception, ex:
            arc.AddError(ex.message)
            arc.SetParameter(3, "false")

# Main entry
execute_file()




