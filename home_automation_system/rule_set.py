import asyncio


def rule_func(**kwargs):
    def decorator(func):
        return Rule(func, **kwargs)

    return decorator


class Ruleset:
    def get_rules(self):
        rules = []

        for member in dir(self):
            attr = getattr(self, member)

            if type(attr) == Rule:
                rules.append(attr)

        return rules

    def match_rule(self, rule=None, **kwargs):
        rule_matches = []
        for rule_obj in self.get_rules():
            if rule_obj.check_rule(rule=rule, **kwargs):
                rule_matches.append(rule_obj)

        if len(rule_matches) == 0:
            return None
        else:
            return rule_matches

    async def run_rules(self, data, rule=None, **kwargs):
        rule_matches = self.match_rule(rule=rule, **kwargs)

        for rule in rule_matches:
            await rule.func(self, data)


class Rule:
    def __init__(self, func, rule=None, **kwargs):
        self.rule = kwargs
        if rule is not None:
            self.rule.update(rule)

        self.func = func

    def check_rule(self, rule=None, **kwargs):
        match = True
        match_rule = kwargs

        if rule is not None:
            match_rule.update(rule)

        for key in self.rule:
            if key in kwargs:
                if self.rule[key] is dict:
                    for param in kwargs[key]:
                        if kwargs[key][param] != self.rule[key][param]:
                            match = False
                            continue
                elif kwargs[key] != self.rule[key]:
                    match = False
                    continue
            else:
                match = False
                continue

        return match

