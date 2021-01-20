from tomlkit import parse
from tomlkit.exceptions import NonExistentKey
from tagexpressions import parse as exparse
from os.path import dirname


class Configuration(object):

    def __init__(self, raw, name):
        self.elements = dict(raw[name])
        inherit = self.elements.pop("inherit", "")
        if inherit != "":
            parent = Configuration(raw, inherit)
            parent.elements.update(self.elements)
            self.elements = parent.elements

class Condition(object):

    def __init__(self, cond, name):
        self.name = name
        self.comparator = cond['comparator']
        self.needed = cond['value']
        self.key = cond['key']

    def value(self, variables):
        try:
            clientvalue = variables[self.key]
        except KeyError:
            # if we don't have the proper variables for a condition, this condition is FALSE
            return ''

        if self.comparator == "==":
            if clientvalue == self.needed:
                return self.name
        if self.comparator == "!=":
            if clientvalue != self.needed:
                return self.name
        elif self.comparator == ">=":
            if clientvalue >= self.needed:
                return self.name
        elif self.comparator == ">":
            if clientvalue > self.needed:
                return self.name
        elif self.comparator == "<=":
            if clientvalue <= self.needed:
                return self.name
        elif self.comparator == "<":
            if clientvalue < self.needed:
                return self.name

        return ''



def prepare():
    toml = ""
    variables = dict()

    with open('{0}/configs.toml'.format(dirname(__file__)), 'r') as fp:
        toml = fp.read()

    raw = dict({"empty": {}, "default": {}})
    raw.update(parse(toml))

    rules = dict({"empty": {}, "default": {}})
    rules.update(raw.pop("rules", {}))

    configs = dict()

    # preparing rules
    for name, upd in rules.items():
        if name not in raw:
            print("[rules.{0}] this rule does not have a matching config. exiting!".format(name))
            exit()
        rule = {'prio': 0, 'expression': '(a)', 'conditions': dict()}
        rule.update(upd)
        rules[name] = rule
        configs[name] = Configuration(raw, name)

    return (rules, configs)

def match(variables, rules):
    # special case empty variables:
    
    if variables is None or len(variables) == 0:
        return 'empty'
    # sort rules by prio and check!
    for name, rule in sorted(rules.items(), key=lambda config: config[1]['prio'], reverse=True):
        data = list()
        for condition, rulecondition in rule['conditions'].items():
            c = Condition(rulecondition, condition)
            data.append(c.value(variables))

        compiled_expression = exparse(rule['expression'])
        if compiled_expression.evaluate(data):
            return name
    return 'default'
