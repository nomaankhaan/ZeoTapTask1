import unittest
from models import RuleParser, combine_rules, PostgresRuleEngine

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.parser = RuleParser()
        self.engine = PostgresRuleEngine()
        
        # Sample rule strings
        self.rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        self.rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
        
        # Sample data
        self.data1 = {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 3
        }
        
        self.data2 = {
            "age": 23,
            "department": "Marketing",
            "salary": 25000,
            "experience": 2
        }

    def test_create_rule(self):
        """Test rule string parsing"""
        ast = self.parser.create_rule(self.rule1)
        self.assertEqual(ast["type"], "operator")
        self.assertEqual(ast["operator"], "AND")
        
    def test_combine_rules(self):
        """Test rule combination"""
        rules = [self.rule1, self.rule2]
        combined_ast = combine_rules(rules)
        self.assertEqual(combined_ast["type"], "operator")
        self.assertEqual(combined_ast["operator"], "AND")
        
    def test_evaluate_rule(self):
        """Test rule evaluation"""
        ast = self.parser.create_rule(self.rule1)
        
        # Test data1 (should be True)
        result1 = self.engine.evaluate_node(ast, self.data1)
        self.assertTrue(result1)
        
        # Test data2 (should be False)
        result2 = self.engine.evaluate_node(ast, self.data2)
        self.assertFalse(result2)

if __name__ == '__main__':
    unittest.main()