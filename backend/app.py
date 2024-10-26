from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging

from .models import PostgresRuleEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Eligibility Checker")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="frontend/templates")

# Initialize rule engine
rule_engine = PostgresRuleEngine()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RuleRequest(BaseModel):
    rule: Dict[str, Any]
    user_data: Dict[str, Any]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the frontend application"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/evaluate")
async def evaluate_rule(request: RuleRequest):
    """Evaluate eligibility rules against user data"""
    try:
        logger.info(f"Evaluating rule for user data: {request.user_data}")
        result = rule_engine.evaluate_node(request.rule, request.user_data)
        logger.info(f"Evaluation result: {result}")
        return {"eligible": result}
    except Exception as e:
        logger.error(f"Error evaluating rule: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with rule_engine.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")