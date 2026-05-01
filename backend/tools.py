"""
MCP-style Tools for cap table analysis and equity insights
"""
from typing import Dict, List, Any, Optional
from models import (
    OwnershipSummary, DilutionResult, ESOPSummary
)
import json

class CapTableTools:
    """Tools for analyzing cap tables"""
    
    def __init__(self, cap_table_data: Dict[str, Any]):
        """Initialize with cap table data"""
        self.cap_table = cap_table_data
        self.shareholders = cap_table_data.get("shareholders", [])
        self.calculate_percentages()
    
    def calculate_percentages(self):
        """Calculate ownership percentages"""
        total_shares = sum(sh["shares"] for sh in self.shareholders)
        self.total_shares = total_shares
        for sh in self.shareholders:
            sh["percentage"] = (sh["shares"] / total_shares * 100) if total_shares > 0 else 0
    
    def get_cap_table(self) -> Dict[str, Any]:
        """
        Tool: get_cap_table
        Returns the full cap table with shareholders and ownership %
        """
        return {
            "company_name": self.cap_table.get("company_name", "Unknown"),
            "shareholders": self.shareholders,
            "total_shares": self.total_shares
        }
    
    def get_largest_shareholder(self) -> Dict[str, Any]:
        """
        Tool: get_largest_shareholder
        Returns the shareholder with the most equity
        """
        if not self.shareholders:
            return {"error": "No shareholders found"}
        
        largest = max(self.shareholders, key=lambda x: x["shares"])
        return {
            "name": largest["name"],
            "shares": largest["shares"],
            "percentage": largest["percentage"],
            "share_type": largest.get("share_type", "Common")
        }
    
    def calculate_ownership(self) -> List[OwnershipSummary]:
        """
        Tool: calculate_ownership
        Returns ownership breakdown ranked by percentage
        """
        sorted_shareholders = sorted(
            self.shareholders,
            key=lambda x: x["percentage"],
            reverse=True
        )
        
        return [
            OwnershipSummary(
                shareholder=sh["name"],
                shares=sh["shares"],
                percentage=round(sh["percentage"], 2),
                rank=i + 1
            )
            for i, sh in enumerate(sorted_shareholders)
        ]
    
    def calculate_dilution(self, new_investment_shares: int) -> List[DilutionResult]:
        """
        Tool: calculate_dilution
        Simulates dilution after new investment
        """
        new_total_shares = self.total_shares + new_investment_shares
        
        results = []
        for sh in self.shareholders:
            original_percentage = sh["percentage"]
            new_percentage = (sh["shares"] / new_total_shares * 100) if new_total_shares > 0 else 0
            dilution = original_percentage - new_percentage
            
            results.append(
                DilutionResult(
                    shareholder=sh["name"],
                    original_shares=sh["shares"],
                    original_percentage=round(original_percentage, 2),
                    new_shares=sh["shares"],
                    new_percentage=round(new_percentage, 2),
                    dilution_percentage=round(dilution, 2)
                )
            )
        
        return results
    
    def get_esop_summary(self) -> ESOPSummary:
        """
        Tool: get_esop_summary
        Returns ESOP pool breakdown
        """
        esop = next(
            (sh for sh in self.shareholders if "esop" in sh["name"].lower()),
            None
        )
        
        if not esop:
            return ESOPSummary(
                total_esop_shares=0,
                esop_percentage=0,
                allocated_shares=0,
                available_shares=0
            )
        
        return ESOPSummary(
            total_esop_shares=esop["shares"],
            esop_percentage=round(esop["percentage"], 2),
            allocated_shares=int(esop["shares"] * 0.6),  # Assume 60% allocated
            available_shares=int(esop["shares"] * 0.4)   # 40% available
        )
    
    def shareholder_summary(self, shareholder_name: str) -> Dict[str, Any]:
        """
        Tool: shareholder_summary
        Get detailed info about a specific shareholder
        """
        shareholder = next(
            (sh for sh in self.shareholders if sh["name"].lower() == shareholder_name.lower()),
            None
        )
        
        if not shareholder:
            return {"error": f"Shareholder '{shareholder_name}' not found"}
        
        return {
            "name": shareholder["name"],
            "shares": shareholder["shares"],
            "percentage": round(shareholder["percentage"], 2),
            "share_type": shareholder.get("share_type", "Common"),
            "rank": self.get_rank(shareholder_name)
        }
    
    def get_rank(self, shareholder_name: str) -> int:
        """Get shareholder rank by ownership"""
        sorted_shareholders = sorted(
            self.shareholders,
            key=lambda x: x["percentage"],
            reverse=True
        )
        
        for i, sh in enumerate(sorted_shareholders):
            if sh["name"].lower() == shareholder_name.lower():
                return i + 1
        return -1

# Tool registry for MCP-style invocation
TOOLS = {
    "get_cap_table": "get_cap_table",
    "get_largest_shareholder": "get_largest_shareholder",
    "calculate_ownership": "calculate_ownership",
    "calculate_dilution": "calculate_dilution",
    "get_esop_summary": "get_esop_summary",
    "shareholder_summary": "shareholder_summary"
}
