"""
Wrap parameters parsing
As it's quite ugly and messy
"""
from functools import wraps
from flask_restful import reqparse
from config import logging


def parse_params(*arguments):
    """
    Parse the parameters
    Forward them to the wrapped function as named parameters
    """
    def parse(func):
        """ Wrapper """
        @wraps(func)
        def resource_verb(*args, **kwargs):
            """ Decorated function """
            parser = reqparse.RequestParser()
            for argument in arguments:
                parser.add_argument(argument)
            parser.parse_args()
            return func(*args, **kwargs)
        return resource_verb
    return parse