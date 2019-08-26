import asyncio
from home_automation_system.rule_set import Ruleset, Rule, rule_func


class TestRuleset(Ruleset):
    @rule_func(Test="yes")
    async def test(self, data):
        print("Rule Run!")
        print(data)


def get_ruleset():
    return TestRuleset()