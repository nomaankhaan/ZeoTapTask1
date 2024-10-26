from typing import List, Dict
import re

class RuleParser:
    def __init__(self):
        self.tokens = []
        self.current = 0
    
    def tokenize(self, rule_string: str) -> List[str]:
        """Convert rule string into tokens"""
        # Add spaces around parentheses and operators
        rule_string = re.sub(r'([()=<>])', r' \1 ', rule_string)
        # Handle AND/OR operators
        rule_string = re.sub(r'\bAND\b', ' AND ', rule_string, flags=re.IGNORECASE)
        rule_string = re.sub(r'\bOR\b', ' OR ', rule_string, flags=re.IGNORECASE)
        return [token for token in rule_string.split() if token.strip()]
    
    def create_rule(self, rule_string: str) -> Dict:
        """Parse rule string into AST"""
        self.tokens = self.tokenize(rule_string)
        self.current = 0
        return self.parse_expression()
    
    def parse_expression(self) -> Dict:
        """Parse expressions recursively"""
        if self.current >= len(self.tokens):
            raise ValueError("Unexpected end of expression")
            
        token = self.tokens[self.current]
        
        if token == '(':
            self.current += 1
            left = self.parse_expression()
            
            if self.current >= len(self.tokens):
                raise ValueError("Expected operator after expression")
                
            operator = self.tokens[self.current].upper()
            self.current += 1
            
            right = self.parse_expression()
            
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ValueError("Expected closing parenthesis")
                
            self.current += 1
            
            return {
                "type": "operator",
                "operator": operator,
                "left": left,
                "right": right
            }
        else:
            # Parse comparison
            field = self.tokens[self.current]
            self.current += 1
            
            if self.current >= len(self.tokens):
                raise ValueError("Expected operator")
                
            operator = self.tokens[self.current]
            self.current += 1
            
            if self.current >= len(self.tokens):
                raise ValueError("Expected value")
                
            value = self.tokens[self.current]
            self.current += 1
            
            # Convert numeric values
            try:
                value = float(value)
            except ValueError:
                # Remove quotes if present
                value = value.strip("'\"")
            
            return {
                "type": "comparison",
                "field": field,
                "operator": operator,
                "value": value
            }

def combine_rules(rules: List[str]) -> Dict:
    """Combine multiple rules into a single AST using AND operator"""
    parser = RuleParser()
    if not rules:
        raise ValueError("No rules provided")
        
    if len(rules) == 1:
        return parser.create_rule(rules[0])
        
    # Convert all rules to ASTs
    rule_asts = [parser.create_rule(rule) for rule in rules]
    
    # Combine using AND operators
    combined = rule_asts[0]
    for rule_ast in rule_asts[1:]:
        combined = {
            "type": "operator",
            "operator": "AND",
            "left": combined,
            "right": rule_ast
        }
    
    return combined