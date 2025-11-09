import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase

class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'statements_kb4.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    def test1(self):
        ask1 = read.parse_input("fact: (motherof ada ?X)")
        if unittest.main.verbosity > 1:
            print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : bing")

    def test2(self):
        ask1 = read.parse_input("fact: (grandmotherof ada ?X)")
        if unittest.main.verbosity > 1:
            print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : felix")
        self.assertEqual(str(answer[1]), "?X : chen")
        
    def test6(self):
        KB = KnowledgeBase([], [])
        fact1 = read.parse_input("fact: (hero A)")
        fact2 = read.parse_input("fact: (person A)")
        rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")
        ask1 = read.parse_input("fact: (goodman A)")
        
        KB.kb_assert(fact1)
        KB.kb_assert(fact2)
        KB.kb_assert(rule1)
        answer = KB.kb_ask(ask1)

        self.assertTrue(answer is not None)
        self.assertTrue(len(answer) > 0)

    def test7(self):
        KB = KnowledgeBase([], [])
        fact1 = read.parse_input("fact: (hero A)")
        fact2 = read.parse_input("fact: (person B)")
        rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")
        ask1 = read.parse_input("rule: ((person A)) -> (goodman A)")
        ask2 = read.parse_input("rule: ((hero B)) -> (goodman B)")
        KB.kb_assert(fact1)
        KB.kb_assert(fact2)
        KB.kb_assert(rule1)

        self.assertTrue(ask1 in KB.rules)
        self.assertTrue(ask2 not in KB.rules)

    def test8(self):
        KB = KnowledgeBase([], [])
        fact1 = read.parse_input("fact: (hero A)")
        fact2 = read.parse_input("fact: (person A)")
        rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")
        rule2 = read.parse_input("rule: ((goodman ?x) (wenttoschool ?x)) -> (doctor ?x)")
        fact3 = read.parse_input("fact: (wenttoschool A)")
        ask1 = read.parse_input("fact: (goodman A)")
        ask2 = read.parse_input("fact: (doctor A)")
        
        KB.kb_assert(fact1)
        KB.kb_assert(fact2)
        KB.kb_assert(rule1)
        answer1 = KB.kb_ask(ask1)
        KB.kb_assert(rule2)
        KB.kb_assert(fact3)
        answer2 = KB.kb_ask(ask2)

        self.assertTrue(answer1 is not None)
        self.assertTrue(len(answer1) > 0)
        
        self.assertTrue(answer2 is not None)
        self.assertTrue(len(answer2) > 0)

    def test11(self):
        KB = KnowledgeBase([], [])
        fact1 = read.parse_input("fact: (rela A B)")
        fact2 = read.parse_input("fact: (relb B C)")
        fact3 = read.parse_input("fact: (reld C D)")
        fact4 = read.parse_input("fact: (relf D E)")
        fact5 = read.parse_input("fact: (relh E F)")

        rule1 = read.parse_input("rule: ((rela ?x ?y) (relb ?y ?z)) -> (relc ?x ?z)")
        rule2 = read.parse_input("rule: ((relc ?x ?y) (reld ?y ?z)) -> (rele ?x ?z)")
        rule3 = read.parse_input("rule: ((rele ?x ?y) (relf ?y ?z)) -> (relg ?x ?z)")
        rule4 = read.parse_input("rule: ((relg ?x ?y) (relh ?y ?z)) -> (reli ?x ?z)")

        ask1 = read.parse_input("fact: (reli A F)")

        KB.kb_assert(fact1)
        KB.kb_assert(fact2)
        KB.kb_assert(fact3)
        KB.kb_assert(fact4)
        KB.kb_assert(fact5)
        KB.kb_assert(rule1)
        KB.kb_assert(rule2)
        KB.kb_assert(rule3)
        KB.kb_assert(rule4)
        
        answer1 = KB.kb_ask(ask1)

        self.assertTrue(answer1 is not None)
        self.assertTrue(len(answer1) > 0)

    def test12(self):
        KB = KnowledgeBase([], [])
        fact1 = read.parse_input("fact: (rela A B C D E F)")
        fact2 = read.parse_input("fact: (relb D E F G H I)")
        fact3 = read.parse_input("fact: (reld G H I)")

        rule1 = read.parse_input("rule: ((rela ?a ?b ?c ?d ?e ?f) (relb ?d ?e ?f ?g ?h ?i)) -> (relc ?a ?b ?c ?g ?h ?i)")
        rule2 = read.parse_input("rule: ((relc ?a ?b ?c ?g ?h ?i) (reld ?g ?h ?i)) -> (rele ?a ?b ?c)")

        ask1 = read.parse_input("fact: (rele A B C)")

        KB.kb_assert(fact1)
        KB.kb_assert(fact2)
        KB.kb_assert(fact3)
        KB.kb_assert(rule1)
        KB.kb_assert(rule2)
        
        answer1 = KB.kb_ask(ask1)

        self.assertTrue(answer1 is not None)
        self.assertTrue(len(answer1) > 0)

    def test3(self):
        # test single statement LHS rule
        kb = KnowledgeBase([], [])
        f1 = read.parse_input("fact: (student john)")
        r1 = read.parse_input("rule: ((student ?x)) -> (person ?x)")
        
        kb.kb_assert(f1)
        kb.kb_assert(r1)
        
        q = read.parse_input("fact: (person john)")
        result = kb.kb_ask(q)
        
        self.assertTrue(result is not None)
        self.assertTrue(len(result) > 0)

    def test4(self):
        #testing rule with 3 statements on LHS
        KB = KnowledgeBase([], [])
        fact_a = read.parse_input("fact: (hasA X)")
        fact_b = read.parse_input("fact: (hasB X)")
        fact_c = read.parse_input("fact: (hasC X)")
        rule = read.parse_input("rule: ((hasA ?x) (hasB ?x) (hasC ?x)) -> (hasAll ?x)")
        
        KB.kb_assert(fact_a)
        KB.kb_assert(fact_b)
        KB.kb_assert(fact_c)
        KB.kb_assert(rule)
        
        # should create curried rules first
        # check that intermediate rule exists
        intermediate = read.parse_input("rule: ((hasB X) (hasC X)) -> (hasAll X)")
        self.assertTrue(intermediate in KB.rules)
        
        # then should infer final fact
        query = read.parse_input("fact: (hasAll X)")
        ans = KB.kb_ask(query)
        self.assertTrue(len(ans) > 0)

    def test5(self):
        # test that non-matching facts don't trigger rules
        kb_test = KnowledgeBase([], [])
        f = read.parse_input("fact: (color apple red)")
        r = read.parse_input("rule: ((color ?x blue)) -> (cool ?x)")
        
        kb_test.kb_assert(f)
        kb_test.kb_assert(r)
        
        # should not create any inferred facts
        q = read.parse_input("fact: (cool apple)")
        res = kb_test.kb_ask(q)
        self.assertEqual(len(res), 0)

    def test9(self):
        # test multiple variables in one statement
        KB = KnowledgeBase([], [])
        f1 = read.parse_input("fact: (parent alice bob)")
        f2 = read.parse_input("fact: (parent bob charlie)")
        r1 = read.parse_input("rule: ((parent ?x ?y) (parent ?y ?z)) -> (grandparent ?x ?z)")
        
        KB.kb_assert(f1)
        KB.kb_assert(f2)
        KB.kb_assert(r1)
        
        # should eventually infer the fact (might go through curried rules)
        q = read.parse_input("fact: (grandparent alice charlie)")
        a = KB.kb_ask(q)
        self.assertTrue(len(a) > 0)

    def test10(self):
        # test one fact triggering multiple rules
        kb = KnowledgeBase([], [])
        fact1 = read.parse_input("fact: (animal dog)")
        rule1 = read.parse_input("rule: ((animal ?x)) -> (living ?x)")
        rule2 = read.parse_input("rule: ((animal ?x)) -> (mortal ?x)")
        
        kb.kb_assert(fact1)
        kb.kb_assert(rule1)
        kb.kb_assert(rule2)
        
        # both rules should trigger
        q1 = read.parse_input("fact: (living dog)")
        q2 = read.parse_input("fact: (mortal dog)")
        a1 = kb.kb_ask(q1)
        a2 = kb.kb_ask(q2)
        
        self.assertTrue(len(a1) > 0)
        self.assertTrue(len(a2) > 0)

    def test13(self):
        # test support relationships are tracked correctly
        KB = KnowledgeBase([], [])
        f1 = read.parse_input("fact: (a 1)")
        f2 = read.parse_input("fact: (b 1)")
        r1 = read.parse_input("rule: ((a ?x) (b ?x)) -> (c ?x)")
        
        KB.kb_assert(f1)
        KB.kb_assert(f2)
        KB.kb_assert(r1)
        
        # find the inferred fact
        inferred_fact = None
        for fact in KB.facts:
            if str(fact.statement) == "(c 1)":
                inferred_fact = fact
                break
        
        self.assertIsNotNone(inferred_fact)
        # check it has support
        self.assertTrue(len(inferred_fact.supported_by) > 0)
        # f1 should support either a rule or fact
        self.assertTrue(len(f1.supports_facts) > 0 or len(f1.supports_rules) > 0)

    def test14(self):
        # test deep inference chain
        kb = KnowledgeBase([], [])
        f = read.parse_input("fact: (level1 start)")
        r1 = read.parse_input("rule: ((level1 ?x)) -> (level2 ?x)")
        r2 = read.parse_input("rule: ((level2 ?x)) -> (level3 ?x)")
        r3 = read.parse_input("rule: ((level3 ?x)) -> (level4 ?x)")
        
        kb.kb_assert(f)
        kb.kb_assert(r1)
        kb.kb_assert(r2)
        kb.kb_assert(r3)
        
        # should eventually infer level4
        query = read.parse_input("fact: (level4 start)")
        answer = kb.kb_ask(query)
        self.assertTrue(len(answer) > 0)

    def test15(self):
        # test rule with no match doesn't break anything
        KB = KnowledgeBase([], [])
        rule = read.parse_input("rule: ((nonexistent ?x)) -> (result ?x)")
        KB.kb_assert(rule)
        
        # should not crash, just no inference
        self.assertEqual(len(KB.facts), 0)  # no facts added yet
        self.assertEqual(len(KB.rules), 1)  # just the one rule we added

    def test16(self):
        # test variable binding across multiple statements
        kb = KnowledgeBase([], [])
        f1 = read.parse_input("fact: (owns alice car1)")
        f2 = read.parse_input("fact: (owns alice house1)")
        r = read.parse_input("rule: ((owns ?p ?c) (owns ?p ?h)) -> (hasBoth ?p)")
        
        kb.kb_assert(f1)
        kb.kb_assert(f2)
        kb.kb_assert(r)
        
        # should create curried rule with ?p bound to alice
        curried = read.parse_input("rule: ((owns alice ?h)) -> (hasBoth alice)")
        self.assertTrue(curried in kb.rules)
        
        # then should infer fact
        q = read.parse_input("fact: (hasBoth alice)")
        a = kb.kb_ask(q)
        self.assertTrue(len(a) > 0)


def pprint_justification(answer):
    """Pretty prints (hence pprint) justifications for the answer.
    """
    if not answer: print('Answer is False, no justification')
    else:
        print('\nJustification:')
        for i in range(0,len(answer.list_of_bindings)):
            # print bindings
            print(answer.list_of_bindings[i][0])
            # print justifications
            for fact_rule in answer.list_of_bindings[i][1]:
                pprint_support(fact_rule,0)
        print

def pprint_support(fact_rule, indent):
    """Recursive pretty printer helper to nicely indent
    """
    if fact_rule:
        print(' '*indent, "Support for")

        if isinstance(fact_rule, Fact):
            print(fact_rule.statement)
        else:
            print(fact_rule.lhs, "->", fact_rule.rhs)

        if fact_rule.supported_by:
            for pair in fact_rule.supported_by:
                print(' '*(indent+1), "support option")
                for next in pair:
                    pprint_support(next, indent+2)



if __name__ == '__main__':
    unittest.main()
