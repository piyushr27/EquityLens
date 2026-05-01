from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class Shareholder(BaseModel):
    name: str
    shares: int
    share_type: str = "Common"  # Common, Preferred, Options
    percentage: Optional[float] = None

class CapTable(BaseModel):
    company_name: str
    shareholders: List[Shareholder]
    total_shares: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CapTableInDB(CapTable):
    id: Optional[str] = Field(default=None, alias="_id")

class Query(BaseModel):
    company_id: str
    question: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class QueryResponse(BaseModel):
    query: str
    answer: str
    data: Optional[Dict] = None
    timestamp: datetime

class OwnershipSummary(BaseModel):
    shareholder: str
    shares: int
    percentage: float
    rank: int

class DilutionResult(BaseModel):
    shareholder: str
    original_shares: int
    original_percentage: float
    new_shares: int
    new_percentage: float
    dilution_percentage: float

class ESOPSummary(BaseModel):
    total_esop_shares: int
    esop_percentage: float
    allocated_shares: int
    available_shares: int
