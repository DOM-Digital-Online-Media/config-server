#!/usr/bin/env python

from mangleconfigs import prepare, match
from json import dumps, load
from os.path import dirname

if __name__ == "__main__":

    rules, configs = prepare()

    with open('{0}/variables.json'.format(dirname(__file__)), 'r') as fp:
        variables = load(fp)

    config = match(variables, rules)
    print(dumps(configs[config].elements))
