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
