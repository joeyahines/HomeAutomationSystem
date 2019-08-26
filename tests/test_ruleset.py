from unittest import TestCase
from home_automation_system.rule_set import Ruleset, Rule, rule_func


def test_func():
    return 54321


class TestRuleSet(Ruleset):
    @rule_func(turtle="Yes")
    def better_test(self, data):
        print(data)
        return 321


class TestRuleset(TestCase):
    def test_check_rule(self):
        ruleset_obj = Rule(test_func, test="test", TEST="54321")

        self.assertTrue(ruleset_obj.check_rule(rule={"test": "test"}, TEST="54321"))

        self.assertTrue(ruleset_obj.check_rule(test="test", TEST="54321"))

        self.assertTrue(ruleset_obj.check_rule({"test": "test", "TEST": "54321"}))

    def test_match_rule(self):
        ruleset = TestRuleSet()

        rules = ruleset.match_rule(turtle="No")

        self.assertIsNone(rules)

        rules = ruleset.match_rule(turtle="Yes")

        self.assertEqual(321, rules[0].func(rules, None), 321)

    def test_run_rule(self):
        ruleset = TestRuleSet()

        ruleset.run_rules({"This is": "just a test"}, turtle="Yes")
