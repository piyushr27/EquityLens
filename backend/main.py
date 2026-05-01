"""
FastAPI backend for AI Equity Assistant
"""
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, Any, List
import json
from datetime import datetime
import traceback

from config import settings
from database import db_connection
from models import (
    CapTable, Query, QueryResponse, OwnershipSummary
)
from agent import EquityAgent
from tools import CapTableTools

# Global state for current cap table
current_cap_table = None
current_agent = None

# ============================================================================
# Lifecycle Events (Modern FastAPI Lifespan Pattern)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle - startup and shutdown"""
    # Startup
    try:
        db_connection.connect()
        print("✓ Connected to MongoDB")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
    
    yield
    
    # Shutdown
    db_connection.disconnect()
    print("✓ Disconnected from MongoDB")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="AI-Powered Cap Table & Equity Insights Assistant",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Equity Assistant",
        "version": settings.api_version,
        "status": "running"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/upload-cap-table")
async def upload_cap_table(file: UploadFile = File(...)):
    """
    Upload a cap table JSON file
    Expected format: {"company_name": "...", "shareholders": [...]}
    """
    global current_cap_table, current_agent
    
    try:
        # Read and parse JSON file
        contents = await file.read()
        cap_table_data = json.loads(contents)
        
        # Validate required fields
        if "shareholders" not in cap_table_data:
            raise ValueError("Cap table must contain 'shareholders' field")
        
        # Store in global state
        current_cap_table = cap_table_data
        current_agent = EquityAgent(cap_table_data)
        
        # Calculate percentages
        total_shares = sum(sh["shares"] for sh in cap_table_data["shareholders"])
        for sh in cap_table_data["shareholders"]:
            sh["percentage"] = (sh["shares"] / total_shares * 100) if total_shares > 0 else 0
        
        # Save to MongoDB
        cap_table_data["uploaded_at"] = datetime.utcnow().isoformat()
        table_id = db_connection.insert_cap_table(cap_table_data)
        
        return {
            "success": True,
            "message": f"Cap table '{cap_table_data.get('company_name', 'Unknown')}' uploaded successfully",
            "table_id": str(table_id),
            "shareholders_count": len(cap_table_data["shareholders"])
        }
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-cap-table-json")
async def upload_cap_table_json(data: Dict[str, Any]):
    """
    Upload cap table as JSON body
    """
    global current_cap_table, current_agent
    
    try:
        if "shareholders" not in data:
            raise ValueError("Cap table must contain 'shareholders' field")
        
        current_cap_table = data
        current_agent = EquityAgent(data)
        
        # Calculate percentages
        total_shares = sum(sh["shares"] for sh in data["shareholders"])
        for sh in data["shareholders"]:
            sh["percentage"] = (sh["shares"] / total_shares * 100) if total_shares > 0 else 0
        
        # Save to MongoDB
        data["uploaded_at"] = datetime.utcnow().isoformat()
        table_id = db_connection.insert_cap_table(data)
        
        return {
            "success": True,
            "message": f"Cap table uploaded successfully",
            "table_id": str(table_id),
            "shareholders_count": len(data["shareholders"])
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cap-table")
async def get_cap_table():
    """Get current cap table"""
    if not current_cap_table:
        raise HTTPException(status_code=404, detail="No cap table loaded. Please upload one first.")
    
    return {
        "company_name": current_cap_table.get("company_name", "Unknown"),
        "shareholders": current_cap_table.get("shareholders", []),
        "total_shareholders": len(current_cap_table.get("shareholders", []))
    }

@app.post("/query")
async def query_equity(data: Dict[str, Any]):
    """
    Process natural language question about equity/cap table
    Expected: {"question": "Who owns the most equity?"}
    """
    if not current_agent:
        raise HTTPException(status_code=404, detail="No cap table loaded. Please upload one first.")
    
    try:
        question = data.get("question", "").strip()
        if not question:
            raise ValueError("Question cannot be empty")
        
        # Query using LangChain agent
        result = current_agent.query(question)
        
        # Save to MongoDB
        query_record = {
            "question": question,
            "answer": result.get("answer", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "company": current_cap_table.get("company_name", "Unknown")
        }
        db_connection.save_query(query_record)
        
        return {
            "question": question,
            "answer": result.get("answer", ""),
            "success": result.get("success", False)
        }
    
    except Exception as e:
        print(f"Error in query: {traceback.format_exc()}")
        return {
            "question": data.get("question", ""),
            "answer": f"Error: {str(e)}",
            "success": False
        }

@app.get("/tools")
async def get_tools():
    """Get available MCP-style tools"""
    if not current_agent:
        raise HTTPException(status_code=404, detail="No cap table loaded")
    
    return {
        "tools": current_agent.get_available_tools()
    }

@app.post("/analyze")
async def analyze_cap_table():
    """Get quick analysis of cap table"""
    if not current_cap_table:
        raise HTTPException(status_code=404, detail="No cap table loaded")
    
    try:
        tools = CapTableTools(current_cap_table)
        
        # Convert Pydantic models to dicts for JSON serialization
        ownership_list = tools.calculate_ownership()
        ownership_dicts = [item.model_dump() if hasattr(item, 'model_dump') else item for item in ownership_list]
        
        largest_sh = tools.get_largest_shareholder()
        esop = tools.get_esop_summary()
        esop_dict = esop.model_dump() if hasattr(esop, 'model_dump') else esop
        
        return {
            "company_name": current_cap_table.get("company_name"),
            "ownership": ownership_dicts,
            "largest_shareholder": largest_sh,
            "esop_summary": esop_dict
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/history")
async def get_query_history(limit: int = 10):
    """Get query history"""
    if not current_cap_table:
        raise HTTPException(status_code=404, detail="No cap table loaded")
    
    try:
        company = current_cap_table.get("company_name", "Unknown")
        history = db_connection.get_query_history(company, limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dilution-calculator")
async def get_dilution_calculator(new_shares: int):
    """Calculate dilution for a given number of new shares"""
    if not current_cap_table:
        raise HTTPException(status_code=404, detail="No cap table loaded")
    
    try:
        tools = CapTableTools(current_cap_table)
        results = tools.calculate_dilution(new_shares)
        
        # Convert Pydantic models to dicts for JSON serialization
        results_dicts = [item.model_dump() if hasattr(item, 'model_dump') else item for item in results]
        
        return {
            "new_shares": new_shares,
            "dilution_impact": results_dicts
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# Sample Data Endpoint (for demo)
# ============================================================================

@app.post("/load-sample-data")
async def load_sample_data():
    """Load sample cap table data for demonstration"""
    global current_cap_table, current_agent
    
    sample_data = {
        "company_name": "TechStartup Inc.",
        "shareholders": [
            {"name": "Founder Alice", "shares": 5000, "share_type": "Common"},
            {"name": "Founder Bob", "shares": 3000, "share_type": "Common"},
            {"name": "Seed Investor A", "shares": 2500, "share_type": "Preferred"},
            {"name": "Seed Investor B", "shares": 2000, "share_type": "Preferred"},
            {"name": "ESOP Pool", "shares": 2000, "share_type": "Options"},
            {"name": "Angel Investor", "shares": 1500, "share_type": "Common"},
        ]
    }
    
    # Set current cap table
    current_cap_table = sample_data
    current_agent = EquityAgent(sample_data)
    
    # Calculate percentages
    total_shares = sum(sh["shares"] for sh in sample_data["shareholders"])
    for sh in sample_data["shareholders"]:
        sh["percentage"] = (sh["shares"] / total_shares * 100)
    
    # Save to DB
    sample_data["uploaded_at"] = datetime.utcnow().isoformat()
    table_id = db_connection.insert_cap_table(sample_data)
    
    return {
        "success": True,
        "message": "Sample data loaded",
        "table_id": str(table_id),
        "data": sample_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
