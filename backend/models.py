import os
import psycopg2
from psycopg2.extras import Json
from typing import Dict, Any, List, Optional, Tuple
import re
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class NodeType(Enum):
    OPERATOR = "operator"
    OPERAND = "operand"
    COMPARISON = "comparison"

class Operator(Enum):
    AND = "AND"
    OR = "OR"
    GT = ">"
    LT = "<"
    EQ = "="
    GTE = ">="
    LTE = "<="

class PostgresRuleEngine:
    def __init__(self):
        self.conn_params = {
            'dbname': os.getenv('DB_NAME', 'eligibility_rules'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432))
        }
        
    def get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def evaluate_node(self, node: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Evaluate a rule node against provided data"""
        if node['type'] == NodeType.OPERATOR.value:
            left_result = self.evaluate_node(node['left'], data)
            right_result = self.evaluate_node(node['right'], data)
            
            if node['operator'] == Operator.AND.value:
                return left_result and right_result
            elif node['operator'] == Operator.OR.value:
                return left_result or right_result
            else:
                raise ValueError(f"Unknown operator: {node['operator']}")
                
        elif node['type'] == NodeType.COMPARISON.value:
            field_value = data.get(node['field'])
            if field_value is None:
                raise ValueError(f"Field {node['field']} not found in data")
                
            compare_value = node['value']
            
            # Type coercion for numeric comparisons
            if isinstance(field_value, str) and isinstance(compare_value, (int, float)):
                try:
                    field_value = float(field_value)
                except ValueError:
                    raise ValueError(f"Cannot compare string '{field_value}' with number {compare_value}")
                    
            elif isinstance(compare_value, str) and isinstance(field_value, (int, float)):
                try:
                    compare_value = float(compare_value)
                except ValueError:
                    raise ValueError(f"Cannot compare number {field_value} with string '{compare_value}'")
            
            # Map the operator to enum value if it's not already
            operator = node['operator']
            
            if operator == ">":
                return field_value > compare_value
            elif operator == "<":
                return field_value < compare_value
            elif operator == "=":
                return field_value == compare_value
            elif operator == ">=":
                return field_value >= compare_value
            elif operator == "<=":
                return field_value <= compare_value
            else:
                raise ValueError(f"Unknown comparison operator: {operator}")
        else:
            raise ValueError(f"Unknown node type: {node['type']}")

    def save_rule(self, name: str, description: str, rule_string: str) -> int:
        """Save rule to database"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT save_rule(%s, %s, %s)",
                    (name, description, rule_string)
                )
                return cur.fetchone()[0]