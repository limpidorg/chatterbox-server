from functools import wraps
from utils import returnMessage
import inspect


def parseData(func):
    '''
    A decorator that allows the use of keyword arguments in a socketio request.
    It assumes that the first positional argument is a dictionary that contains the key-value pair.
    '''
    _, nonOptional, optional = analyseParameters(func)

    @wraps(func)
    def __parseData(data):
        kwargs = {}
        if not data:
            return returnMessage(-400, 'No data was provided')
        if not isinstance(data, dict):
            return returnMessage(-400, 'First argument data must be a dictionary')
        for param in nonOptional:
            if param not in data:
                return returnMessage(-400, f'Missing required parameter {param}')
            kwargs[param] = data[param]
        for param in optional:
            if param in data:
                kwargs[param] = data[param]
        return func(**kwargs)
    return __parseData


def analyseParameters(func):
    parameters = inspect.signature(func).parameters
    varKeyword = None
    nonOptionalParameters = []
    optionalParameters = {}

    for name, parameter in parameters.items():
        if parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
            raise Exception(
                "Positional-only parameters are not supported. All parameters must be named and must not be positional-only.")
        elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            raise Exception(
                "Var-positional parameters are not supported. All parameters must be named and must not be positional-only.")
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            varKeyword = parameter.name
        else:
            if parameter.default != inspect.Parameter.empty:
                optionalParameters[name] = parameter.default
            else:
                nonOptionalParameters.append(name)
    return varKeyword, nonOptionalParameters, optionalParameters
