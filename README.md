# Eligibility Rule Engine

A flexible 3-tier application for determining user eligibility based on configurable rules using Abstract Syntax Trees (AST). The system supports dynamic creation, combination, and modification of rules with attributes like age, department, income, spend, etc.


## Features

1. Abstract Syntax Tree (AST) based rule evaluation

2. Dynamic rule creation and combination

3. PostgreSQL backend for rule storage

4. REST API for rule evaluation

5. Simple web interface for testing rules

6. Support for complex nested conditions

7. Real-time rule evaluation

## Tech Stack

1. Frontend: HTML, CSS, JavaScript

2. Backend: Python, FastAPI

3. Database: PostgreSQL

## Project Setup

1. Clone the Repository

```bash
  git clone https://github.com/nomaankhaan/ZeoTapTask1.git
  cd ZeoTapTask1
```

2. Create and Activate Virtual Environment

```bash
  python -m venv venv
  venv\Scripts\activate
```
3. Install Dependencies

```bash
  pip install -r requirements.txt
```

4. Database Setup

1. Create PostgreSQL Database:

```bash
  psql -U postgres
  CREATE DATABASE eligibility_rules;
  \q
```
2. Update the database credentials in .env file

3. Run Database Migrations:

```bash
  psql -U postgres -d eligibility_rules -f database/migrations/001_initial_schema.sql
```

5. Running the Application

    1. Start the Backend Server:

```bash
  uvicorn backend.app:app --reload --port 8000
```
2. Access the Application:

Open your browser and navigate to http://localhost:8000

6. Using the Application

    1. Creating Rules

Rules can be created using the following syntax:

```bash
  ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
```
2. Web Interface
The web interface provides a simple form to:

1. Input user data (age, department, income, etc.)
2. Test eligibility against predefined rules
3. View evaluation results

7. Testing
Run the test suite:

```bash
  pytest backend/tests/test_rule_engine.py
```
