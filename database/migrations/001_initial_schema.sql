-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
DO $$ BEGIN
    CREATE TYPE node_type AS ENUM ('operator', 'operand', 'comparison');
    EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE operator_type AS ENUM ('AND', 'OR', '>', '<', '=', '>=', '<=');
    EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Create rules table
CREATE TABLE IF NOT EXISTS rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    rule_json JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Create audit log table
CREATE TABLE IF NOT EXISTS rule_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID REFERENCES rules(id),
    action VARCHAR(50) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100)
);

-- Create function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updating timestamp
CREATE TRIGGER update_rules_updated_at
    BEFORE UPDATE ON rules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to save rules
CREATE OR REPLACE FUNCTION save_rule(
    p_name VARCHAR,
    p_description TEXT,
    p_rule_json JSONB
) RETURNS UUID AS $$
DECLARE
    rule_id UUID;
BEGIN
    INSERT INTO rules (name, description, rule_json)
    VALUES (p_name, p_description, p_rule_json)
    RETURNING id INTO rule_id;
    
    -- Log the creation
    INSERT INTO rule_audit_log (rule_id, action, new_value)
    VALUES (rule_id, 'CREATE', p_rule_json);
    
    RETURN rule_id;
END;
$$ LANGUAGE plpgsql;